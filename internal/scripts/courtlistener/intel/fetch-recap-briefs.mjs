// Surgical RECAP brief fetcher.
//
// Given a docket number (+ optional CourtListener court id) and a list of
// docket entry numbers, resolves the CourtListener docket, lists its entries,
// and downloads every available RECAP PDF for the requested entries.
//
// Run on the laptop where COURTLISTENER_TOKEN exists. Writes PDFs +
// manifest.json to --out/<label>/. Never touches main; `npm run documents:push`
// puts the PDFs on R2 and the cold `documents` branch.
//
// Usage:
//   node fetch-recap-briefs.mjs --docket-number 5:25-cv-02931 --court cacd \
//     --entries 64,68,69,75 --label ventura-randstad --out /tmp/briefs
//   --entries "list" lists every entry (numbers + descriptions) without downloading.

import { mkdir, writeFile } from "node:fs/promises";
import { join } from "node:path";
import {
  CL_BASE,
  CL_UA,
  budgetAllows,
  createClient,
  readCourtListenerToken,
} from "../client.mjs";

function arg(name, def = null) {
  const ix = process.argv.indexOf(`--${name}`);
  if (ix === -1 || ix + 1 >= process.argv.length) return def;
  return process.argv[ix + 1];
}

const DOCKET_NUMBER = arg("docket-number");
const COURT_ID = arg("court", null);
const ENTRIES_RAW = arg("entries", "");
const LABEL = arg("label", "briefs");
const OUT = arg("out", "./briefs");

function sanitize(value) {
  return (
    String(value ?? "")
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, "-")
      .replace(/^-+|-+$/g, "")
      .slice(0, 60) || "doc"
  );
}

async function downloadPdf(url, token) {
  const response = await fetch(url, {
    headers: { Authorization: `Token ${token}`, "User-Agent": CL_UA },
  });
  if (!response.ok) {
    throw new Error(`HTTP ${response.status} for ${url}`);
  }
  const buf = Buffer.from(await response.arrayBuffer());
  const contentType = response.headers.get("content-type") || "";
  if (!contentType.includes("pdf") && buf.length < 1024) {
    throw new Error(`unexpected content-type ${contentType} (${buf.length} bytes) for ${url}`);
  }
  return buf;
}

async function main() {
  if (!DOCKET_NUMBER) throw new Error("--docket-number is required");
  if (!ENTRIES_RAW) throw new Error("--entries is required (CSV entry numbers or \"all\")");
  const token = readCourtListenerToken();
  if (!token) throw new Error("COURTLISTENER_TOKEN is required");

  const client = createClient({ token });
  const usage = await client.getApiUsage();
  const budget = budgetAllows(usage, { minDaily: 5, minHourly: 2, minMinute: 1 });
  if (!budget.ok) throw new Error(`CourtListener budget too low: ${budget.reason}`);
  console.log(
    `budget ok (daily=${budget.remaining.daily} hourly=${budget.remaining.hourly} minute=${budget.remaining.minute})`,
  );

  const dir = join(OUT, LABEL);
  await mkdir(dir, { recursive: true });

  const manifest = {
    label: LABEL,
    requested: { docket_number: DOCKET_NUMBER, court: COURT_ID, entries: ENTRIES_RAW },
    docket: null,
    fetched_at: new Date().toISOString(),
    error: null,
    documents: [],
  };
  const fail = async (message) => {
    manifest.error = String(message);
    await writeFile(join(dir, "manifest.json"), JSON.stringify(manifest, null, 2));
    throw new Error(message);
  };

  const dockets = await client.searchDockets({ docketNumber: DOCKET_NUMBER, courtId: COURT_ID });
  if (!dockets.length) {
    // Retry without judge-suffix etc: try the bare number core.
    await fail(
      `no CourtListener docket for "${DOCKET_NUMBER}" (court=${COURT_ID || "any"}). ` +
        `Try the full number with judge initials as filed on the docket.`,
    );
  }
  const docket =
    dockets.find((d) => String(d.docket_number) === String(DOCKET_NUMBER)) ?? dockets[0];
  // v4 search hits carry docket_id (not id) — see bindingFromHit in resolve-dockets.
  const docketId = docket.docket_id ?? docket.id ?? null;
  if (!docketId) {
    await fail(
      `search hit for "${DOCKET_NUMBER}" has no docket_id (keys: ${Object.keys(docket).join(",")})`,
    );
  }
  manifest.docket = {
    id: docketId,
    case_name: docket.case_name,
    docket_number: docket.docket_number,
    court: docket.court_id ?? docket.court,
  };
  console.log(
    `docket: ${docket.case_name} (${docket.docket_number}) id=${docket.id} court=${docket.court}`,
  );
  if (dockets.length > 1) {
    console.log(`note: ${dockets.length} candidates; picked first exact docket_number match`);
  }

  const nums =
    ENTRIES_RAW === "all"
      ? null
      : new Set(
          ENTRIES_RAW.split(",")
            .map((n) => Number(String(n).trim()))
            .filter(Number.isFinite),
        );
  const LIST_ONLY = ENTRIES_RAW === "list";
  if (LIST_ONLY) {
    // Discovery mode: full entry listing into the manifest, no downloads.
    const entries = await client.listDocketEntries({ docketId });
    manifest.documents = entries.map((e) => ({
      entry_number: e.entry_number,
      entry_id: e.id,
      description: e.description,
      date_filed: e.date_filed,
      status: "listed",
    }));
    await writeFile(join(dir, "manifest.json"), JSON.stringify(manifest, null, 2));
    console.log(`listed ${entries.length} entries -> ${dir}/manifest.json`);
    return;
  }
  const wanted = [];
  // List the docket's entries (same path as list mode, which is proven reliable)
  // and match the requested numbers client-side. The v4 entry_number query
  // filter proved unreliable in production; do not reintroduce it.
  const allEntries = await client.listDocketEntries({ docketId });
  manifest.entry_count = allEntries.length;
  const byNumber = new Map();
  for (const e of allEntries) {
    if (!byNumber.has(Number(e.entry_number))) byNumber.set(Number(e.entry_number), e);
  }
  for (const n of nums) {
    const hit = byNumber.get(n) ?? null;
    if (hit) wanted.push(hit);
    else console.log(`warning: entry_number ${n} not found among ${allEntries.length} docket entries`);
  }
  console.log(`matched ${wanted.length}/${nums.size} entries`);


  for (const entry of wanted) {
    const docs = [];
    let url = `${CL_BASE}/recap-documents/?docket_entry=${entry.id}`;
    while (url) {
      const page = await client.request(url, { auth: true });
      const rows = Array.isArray(page?.results) ? page.results : [];
      docs.push(...rows);
      url = page?.next || null;
    }
    if (!docs.length) {
      console.log(`entry ${entry.entry_number}: no recap-documents rows`);
      manifest.documents.push({
        entry_number: entry.entry_number,
        entry_id: entry.id,
        description: entry.description,
        status: "no-recap-rows",
      });
      continue;
    }
    for (const doc of docs) {
      const rec = {
        entry_number: entry.entry_number,
        entry_id: entry.id,
        description: entry.description,
        date_filed: entry.date_filed,
        document_number: doc.document_number,
        attachment_number: doc.attachment_number,
        pacer_doc_id: doc.pacer_doc_id,
        is_available: !!doc.is_available,
        status: "skipped",
        file: null,
      };
      if (!doc.is_available) {
        rec.status = "unavailable";
        console.log(`entry ${entry.entry_number} doc ${doc.document_number}: not available on CourtListener`);
      } else {
        const pdfUrl = doc.filepath_ia
          ? `https://storage.courtlistener.com/${doc.filepath_ia}`
          : null;
        if (!pdfUrl) {
          rec.status = "no-filepath";
          console.log(`entry ${entry.entry_number} doc ${doc.document_number}: available but no filepath_ia`);
        } else {
          const fname = `entry-${entry.entry_number}-doc-${doc.document_number ?? "0"}-${sanitize(entry.description)}.pdf`;
          try {
            const buf = await downloadPdf(pdfUrl, token);
            await writeFile(join(dir, fname), buf);
            rec.status = "downloaded";
            rec.file = fname;
            rec.bytes = buf.length;
            console.log(`entry ${entry.entry_number}: downloaded ${fname} (${buf.length} bytes)`);
          } catch (err) {
            rec.status = "download-failed";
            rec.error = String(err?.message || err);
            console.log(`entry ${entry.entry_number}: download failed: ${rec.error}`);
          }
        }
      }
      manifest.documents.push(rec);
    }
  }

  await writeFile(join(dir, "manifest.json"), JSON.stringify(manifest, null, 2));
  const okCount = manifest.documents.filter((d) => d.status === "downloaded").length;
  console.log(`done: ${okCount}/${manifest.documents.length} documents downloaded -> ${dir}`);
}

main().catch(async (err) => {
  console.error(`fetch-recap-briefs failed: ${err?.message || err}`);
  try {
    const dir = join(OUT, LABEL);
    await mkdir(dir, { recursive: true });
    const mfPath = join(dir, "manifest.json");
    let manifest;
    try {
      manifest = JSON.parse(await (await import("node:fs/promises")).readFile(mfPath, "utf8"));
    } catch {
      manifest = { label: LABEL, error: null, documents: [] };
    }
    if (!manifest.error) {
      manifest.error = String(err?.message || err);
      await (await import("node:fs/promises")).writeFile(mfPath, JSON.stringify(manifest, null, 2));
    }
  } catch {
    // manifest write is best-effort; the console error above is the record.
  }
  process.exit(1);
});
