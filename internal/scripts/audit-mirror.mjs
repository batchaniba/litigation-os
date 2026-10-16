#!/usr/bin/env node
// Repo ↔ D1 drift audit. D1 is supposed to be an exact projection of `main`
// (workers/doc-api/seed.mjs). This diffs the projection built from the
// current checkout against what the live Worker serves from D1:
//
//   matters    missing / extra, and identity fields that disagree
//   clocks     every row, keyed by matter + date + title (+ status)
//   documents  D1 rows the repo would not seed (e.g. assistant uploads that
//              never reached the manifest) and rows the repo expects but D1 lacks
//
// Read-only: uses the public GET routes, no keys. Run it BEFORE a reseed: a
// reseed replaces every row, so D1-only documents listed here would vanish
// from D1 (their R2 bytes stay, findable only by hash).
//
//   NODE_USE_ENV_PROXY=1 npm run audit:mirror
//   npm run audit:mirror -- --out drift.json
//   DOC_API_TOKEN=… npm run audit:mirror    # if reads are ever locked
//
// Documents: the Worker's /matters/<n> routes only list rows that HAVE a
// matter number and are servable (R2 object present / not denylisted), so
// they cannot see D1 rows with matter_number NULL (_form-library, unscoped)
// or rows whose R2 object is absent. When wrangler can reach D1 the audit
// also reads the full `documents` table with a read-only SELECT
// (`wrangler d1 execute litigation-portfolio --remote --command "SELECT …"`)
// and, when R2 credentials are in the environment, HEADs each D1 row the
// Worker did not serve. Expected documents found that way are NOT missing:
// rows without an R2 object are reported as documents.in_d1_no_r2_object
// (informational, does not fail the audit). Nothing is ever written.
//   WRANGLER="npx -y node@22 $(command -v wrangler)"   # override the binary
//   AUDIT_D1=worker                                  # skip the direct read
//
// Exit 0: no drift. Exit 1: drift found. Exit 2: could not run.
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { execFileSync } from "node:child_process";
import { buildProjection } from "../../workers/doc-api/seed.mjs";

const DEFAULT_API = "https://litigation-doc-api.ss8sxswwkt.workers.dev";
const IDENTITY_FIELDS = ["caption", "case_no", "court", "phase", "lifecycle", "status_label", "judge"];

const clockKey = (c) => `${c.matter_number}|${c.date}|${c.title}`;

/**
 * Pure diff of the expected projection against live D1 rows.
 * manifestShas (optional) splits D1-only documents into ones the manifest
 * knows but the filing-safe projection excludes (published beyond the public
 * set) and ones the repo has never heard of.
 */
export function diffMirror(expected, live, manifestShas = null) {
  // live.d1Documents: every row of D1 `documents` (incl. matter_number NULL),
  // when read directly. live.r2Missing: shas confirmed absent from R2.
  const exMatters = new Map(expected.matters.map((m) => [m.number, m]));
  const liveMatters = new Map(live.matters.map((m) => [m.number, m]));

  const fieldMismatches = [];
  for (const [n, m] of exMatters) {
    const d = liveMatters.get(n);
    if (!d) continue;
    for (const f of IDENTITY_FIELDS) {
      if ((m[f] ?? null) !== (d[f] ?? null)) fieldMismatches.push({ matter: n, field: f, repo: m[f] ?? null, d1: d[f] ?? null });
    }
  }

  const exClocks = new Map(expected.clocks.map((c) => [clockKey(c), c]));
  const liveClocks = new Map(live.clocks.map((c) => [clockKey(c), c]));
  const statusMismatches = [];
  for (const [k, c] of exClocks) {
    const d = liveClocks.get(k);
    if (d && (c.status ?? "open") !== (d.status ?? "open"))
      statusMismatches.push({ matter: c.matter_number, date: c.date, title: c.title, repo: c.status, d1: d.status });
  }

  const exDocs = new Set(expected.documents.map((d) => d.sha256));
  const servedDocs = new Map(live.documents.map((d) => [d.sha256, d]));
  const liveDocs = new Map(servedDocs);
  for (const d of live.d1Documents ?? []) if (!liveDocs.has(d.sha256)) liveDocs.set(d.sha256, d);
  const r2Missing = live.r2Missing ?? new Set();
  const inD1NoR2 = expected.documents.filter((d) => !servedDocs.has(d.sha256) && liveDocs.has(d.sha256) && r2Missing.has(d.sha256));
  const inD1NoMatter = expected.documents.filter((d) => liveDocs.has(d.sha256) && liveDocs.get(d.sha256).matter_number == null);

  const drift = {
    matters: {
      missing_in_d1: [...exMatters.keys()].filter((n) => !liveMatters.has(n)),
      extra_in_d1: [...liveMatters.keys()].filter((n) => !exMatters.has(n)),
      field_mismatches: fieldMismatches,
    },
    clocks: {
      missing_in_d1: [...exClocks.entries()].filter(([k]) => !liveClocks.has(k)).map(([, c]) => c),
      extra_in_d1: [...liveClocks.entries()].filter(([k]) => !exClocks.has(k)).map(([, c]) => c),
      status_mismatches: statusMismatches,
    },
    documents: {
      missing_in_d1: expected.documents.filter((d) => !liveDocs.has(d.sha256)),
      d1_only: [...liveDocs.values()].filter((d) => !exDocs.has(d.sha256)),
      in_d1_no_r2_object: inD1NoR2,
    },
  };
  const d1Only = drift.documents.d1_only;
  if (manifestShas) {
    drift.documents.d1_only_not_public = d1Only.filter((d) => manifestShas.has(d.sha256));
    drift.documents.d1_only_unknown_to_repo = d1Only.filter((d) => !manifestShas.has(d.sha256));
  }
  const counts = {
    matters_missing: drift.matters.missing_in_d1.length,
    matters_extra: drift.matters.extra_in_d1.length,
    matter_field_mismatches: fieldMismatches.length,
    clocks_missing: drift.clocks.missing_in_d1.length,
    clocks_extra: drift.clocks.extra_in_d1.length,
    clock_status_mismatches: statusMismatches.length,
    documents_missing: drift.documents.missing_in_d1.length,
    documents_d1_only: d1Only.length,
  };
  if (manifestShas) {
    counts.documents_d1_only_not_public = drift.documents.d1_only_not_public.length;
    counts.documents_d1_only_unknown_to_repo = drift.documents.d1_only_unknown_to_repo.length;
  }
  // Informational: present in D1, so not drift, but worth knowing.
  const info = {
    d1_documents_source: live.d1Documents ? "d1-direct" : "worker-only",
    documents_in_d1_no_r2_object: inD1NoR2.length,
    documents_in_d1_no_matter_number: inD1NoMatter.length,
  };
  return { ok: Object.values(counts).every((n) => n === 0), counts, info, drift };
}

async function getJson(api, route, token) {
  const res = await fetch(`${api}${route}`, { headers: token ? { authorization: `Bearer ${token}` } : {} });
  if (!res.ok) throw new Error(`GET ${route} → HTTP ${res.status}`);
  return res.json();
}

/** Live D1 rows via the public Worker routes. */
export async function fetchLive(api, token) {
  const health = await getJson(api, "/health", token);
  const list = await getJson(api, "/matters", token);
  const matters = [];
  const clocks = [];
  const documents = [];
  for (const m of list) {
    const full = await getJson(api, `/matters/${m.number}`, token);
    matters.push(full);
    for (const c of full.clocks ?? [])
      clocks.push({ matter_number: m.number, title: c.title, date: c.date, kind: c.kind, status: c.status ?? "open" });
    for (const d of full.documents ?? []) documents.push({ ...d, matter_number: m.number });
  }
  return { source: health.d1 ?? null, matters, clocks, documents };
}

/** Every D1 `documents` row via a read-only wrangler SELECT, or null if unavailable. */
export function fetchD1Documents() {
  if (process.env.AUDIT_D1 === "worker") return null;
  const cmd = (process.env.WRANGLER || "npx wrangler").split(/\s+/).filter(Boolean);
  const sql = "SELECT sha256, matter_number, path, size FROM documents";
  try {
    const out = execFileSync(
      cmd[0],
      [...cmd.slice(1), "d1", "execute", "litigation-portfolio", "--remote", "--json", "--command", sql],
      { cwd: path.join(path.dirname(fileURLToPath(import.meta.url)), "../../workers/doc-api"), encoding: "utf8", stdio: ["ignore", "pipe", "pipe"], maxBuffer: 64 << 20 },
    );
    const rows = JSON.parse(out.slice(out.indexOf("[")))[0]?.results;
    if (!Array.isArray(rows)) throw new Error("unexpected wrangler output");
    return rows.map((r) => ({ ...r, sha256: String(r.sha256).toLowerCase() }));
  } catch (err) {
    process.stderr.write(`audit:mirror: direct D1 read unavailable (${String(err?.message || err).split("\n")[0]}); worker-only document view\n`);
    return null;
  }
}

/** shas (from the given list) with no R2 object; null if R2 creds are absent. */
export async function findR2Missing(shas) {
  const r2 = await import("./lib/r2-client.mjs");
  if (!r2.isConfigured()) return null;
  const missing = new Set();
  const list = [...shas];
  for (let i = 0; i < list.length; i += 16) {
    await Promise.all(
      list.slice(i, i + 16).map(async (sha) => {
        if (!(await r2.objectExists(r2.keyForSha256(sha)))) missing.add(sha);
      }),
    );
  }
  return missing;
}

async function main() {
  const args = process.argv.slice(2);
  const outIdx = args.indexOf("--out");
  const out = outIdx >= 0 ? args[outIdx + 1] : null;
  const api = (process.env.DOC_API_URL || DEFAULT_API).replace(/\/+$/, "");

  const expected = buildProjection();
  const live = await fetchLive(api, process.env.DOC_API_TOKEN);
  live.d1Documents = fetchD1Documents();
  if (live.d1Documents) {
    const served = new Set(live.documents.map((d) => d.sha256));
    const unserved = live.d1Documents.filter((d) => !served.has(d.sha256)).map((d) => d.sha256);
    const missing = await findR2Missing(unserved);
    if (missing) live.r2Missing = missing;
    else process.stderr.write("audit:mirror: R2 credentials not set; in_d1_no_r2_object not checked\n");
  }
  const manifest = JSON.parse(
    fs.readFileSync(path.join(path.dirname(fileURLToPath(import.meta.url)), "../src/data/documents/manifest.json"), "utf8"),
  );
  const manifestShas = new Set((manifest.files ?? []).map((f) => String(f.sha256).toLowerCase()));
  const result = { generated: new Date().toISOString(), d1_source: live.source, ...diffMirror(expected, live, manifestShas) };

  if (out) fs.writeFileSync(out, `${JSON.stringify(result, null, 2)}\n`);
  else process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
  process.stderr.write(
    (result.ok ? "audit:mirror OK — D1 matches the repo projection" : `audit:mirror DRIFT — ${JSON.stringify(result.counts)}`) +
      ` | info ${JSON.stringify(result.info)}\n`,
  );
  process.exit(result.ok ? 0 : 1);
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  main().catch((err) => {
    process.stderr.write(`audit:mirror error: ${err?.stack || err}\n`);
    process.exit(2);
  });
}
