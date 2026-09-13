// Full-text sweep for Penal Code § 290.46 across CourtListener opinions and RECAP.
//
// Closes the one gap the 2026-09-12 § 290.46 case survey could not: a docket-level
// search for complaints and briefing that cite the statute where no opinion exists.
// Runs in GitHub Actions because that is where COURTLISTENER_TOKEN lives; the agent
// container's egress policy blocks courtlistener.com outright.
//
// Usage:
//   node internal/scripts/courtlistener/sweep-290-46.mjs
//   node internal/scripts/courtlistener/sweep-290-46.mjs --dry-run   # no writes

import { mkdirSync, writeFileSync } from "node:fs";
import path from "node:path";
import { budgetAllows, createClient, readCourtListenerToken } from "./client.mjs";
import { REPO_ROOT } from "./io.mjs";

const OUT_DIR = path.join(REPO_ROOT, "internal/docs/legal-intel/recon");
const OUT_PATH = path.join(OUT_DIR, "290-46-recap-sweep.json");

// CourtListener's minute budget is 5/min, so space requests well clear of it.
const MIN_INTERVAL_MS = 13_000;

// type=o searches opinion text; type=r searches RECAP filings (complaints, briefs).
//
// A bare "290.46" is useless: CourtListener tokenizes it so it also matches the
// dollar amount $290.46, and the first sweep drowned in bankruptcy claim schedules
// (540 RECAP "hits", almost all noise). Query the subdivision strings instead. Both
// numberings are searched because the employment restriction sat at (l) before the
// renumbering and at (j)(2)(E) after it, so old and new filings spell it differently.
const QUERIES = [
  { id: "opinions-subdiv-j", type: "o", q: '"290.46(j)"' },
  { id: "opinions-subdiv-l", type: "o", q: '"290.46(l)"' },
  { id: "opinions-mlw-employment", type: "o", q: '"Megan\'s Law" employment "290.46"' },
  { id: "recap-subdiv-j2E", type: "r", q: '"290.46(j)(2)(E)"' },
  { id: "recap-subdiv-j", type: "r", q: '"290.46(j)"' },
  { id: "recap-subdiv-l", type: "r", q: '"290.46(l)"' },
  { id: "recap-mlw-website", type: "r", q: '"Megan\'s Law website" employment' },
  { id: "recap-parallel-290-4", type: "r", q: '"290.4(d)"' },
];

// Dockets whose entry list the survey needs in full. Carrillo is the live
// employment case whose complaint pleads (j)(2)(E) and whose posture is unknown;
// Pastrana's Nov. 2008 order is cited portfolio-wide as a defense summary-judgment
// win, but the docket labels it "granting in part and denying in part", so the
// entries decide which is right.
const DOCKETS = [
  { id: 69602414, label: "Roberto Sandoval Carrillo v. The Vons Companies, Inc. (8:25-cv-00191)" },
  { id: 5983762, label: "Pastrana v. Local 9509, CWA, AFL-CIO (3:06-cv-01779)" },
];

const dryRun = process.argv.includes("--dry-run");

function summarize(type, row) {
  if (type === "o") {
    return {
      caseName: row.caseName ?? null,
      court: row.court ?? row.court_id ?? null,
      dateFiled: row.dateFiled ?? null,
      docketNumber: row.docketNumber ?? null,
      status: row.status ?? null,
      citation: row.citation ?? null,
      absoluteUrl: row.absolute_url ? `https://www.courtlistener.com${row.absolute_url}` : null,
    };
  }
  // RECAP rows nest matched filings under recap_documents.
  const docs = Array.isArray(row.recap_documents) ? row.recap_documents : [];
  return {
    caseName: row.caseName ?? null,
    court: row.court ?? row.court_id ?? null,
    dateFiled: row.dateFiled ?? null,
    docketNumber: row.docketNumber ?? null,
    docketId: row.docket_id ?? null,
    assignedTo: row.assignedTo ?? null,
    dateTerminated: row.dateTerminated ?? null,
    absoluteUrl: row.docket_absolute_url
      ? `https://www.courtlistener.com${row.docket_absolute_url}`
      : null,
    matchedFilings: docs.map((doc) => ({
      entryNumber: doc.entry_number ?? null,
      description: doc.short_description ?? doc.description ?? null,
      dateFiled: doc.entry_date_filed ?? null,
      snippet: doc.snippet ?? null,
    })),
  };
}

async function main() {
  const token = readCourtListenerToken();
  if (!token) {
    console.error("COURTLISTENER_TOKEN is not set. The search API needs it for RECAP text.");
    process.exit(1);
  }
  const client = createClient({ token, minIntervalMs: MIN_INTERVAL_MS });

  // Repo convention: check the usage endpoint first and refuse to run blind.
  let usage;
  try {
    usage = await client.getApiUsage();
  } catch (err) {
    console.error(`Could not read /api-usage/: ${err.message}. Refusing to run.`);
    process.exit(1);
  }
  const budget = budgetAllows(usage, { minDaily: QUERIES.length * 2, minHourly: 2 });
  if (!budget.ok) {
    console.error(`Quota too low to sweep: ${budget.reason}`);
    process.exit(1);
  }
  console.log(
    `Quota OK — daily ${budget.remaining.daily}, hourly ${budget.remaining.hourly}, minute ${budget.remaining.minute}`,
  );

  const results = [];
  for (const query of QUERIES) {
    const params = new URLSearchParams({ type: query.type, q: query.q, page_size: "20" });
    if (query.type === "r") params.set("order_by", "dateFiled desc");
    const url = `https://www.courtlistener.com/api/rest/v4/search/?${params}`;
    try {
      const page = await client.request(url, { auth: true });
      const rows = Array.isArray(page?.results) ? page.results : [];
      console.log(`[${query.id}] type=${query.type} q=${query.q} -> ${page?.count ?? rows.length} hits`);
      for (const row of rows) console.log(`    ${row.caseName ?? "?"} | ${row.court ?? "?"} | ${row.dateFiled ?? "?"}`);
      results.push({
        ...query,
        count: page?.count ?? null,
        returned: rows.length,
        hits: rows.map((row) => summarize(query.type, row)),
      });
    } catch (err) {
      console.error(`[${query.id}] FAILED: ${err.message}`);
      results.push({ ...query, error: err.message });
    }
  }

  const dockets = [];
  for (const d of DOCKETS) {
    try {
      const entries = await client.listDocketEntries({ docketId: d.id });
      console.log(`\n[docket ${d.id}] ${d.label} -> ${entries.length} entries`);
      for (const e of entries) {
        const desc = String(e.description ?? "").replace(/\s+/g, " ").slice(0, 220);
        console.log(`    #${e.entry_number ?? "?"} [${e.date_filed ?? "?"}] ${desc}`);
      }
      dockets.push({
        ...d,
        entryCount: entries.length,
        entries: entries.map((e) => ({
          entryNumber: e.entry_number ?? null,
          dateFiled: e.date_filed ?? null,
          description: String(e.description ?? "").replace(/\s+/g, " ") || null,
        })),
      });
    } catch (err) {
      console.error(`[docket ${d.id}] FAILED: ${err.message}`);
      dockets.push({ ...d, error: err.message });
    }
  }

  const payload = {
    generated_at: new Date().toISOString(),
    purpose:
      "Docket-level and opinion-level full-text sweep for California Penal Code 290.46, closing gap 3 of the 2026-09-12 employment-use case survey.",
    api: "CourtListener REST v4 /search/",
    queries: results,
    dockets,
  };

  if (dryRun) {
    console.log("--dry-run: not writing");
    return;
  }
  mkdirSync(OUT_DIR, { recursive: true });
  writeFileSync(OUT_PATH, `${JSON.stringify(payload, null, 2)}\n`, "utf8");
  console.log(`Wrote ${path.relative(REPO_ROOT, OUT_PATH)}`);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
