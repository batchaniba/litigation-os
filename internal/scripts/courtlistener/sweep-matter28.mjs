// Verification sweep for Matter 28 (Newanforbi v. Shannon Smith, LCSW / HOPE Psychotherapy,
// N.D. Cal. 3:26-cv-07504-LJC).
//
// Two jobs:
//   1. Verify every authority the defense previewed in its Sept. 3, 2026 meet-and-confer,
//      plus the authorities Plaintiff's theory rests on, against CourtListener's opinion index.
//   2. Pull the docket entries for this case and the earlier federal HOPE case (Matter 6),
//      so the res judicata timeline rests on dockets rather than on counsel's characterization.
//
// Run on the laptop: COURTLISTENER_TOKEN in gitignored `.env`. There is no
// GitHub Actions job. The cloud-agent container's egress policy blocks
// courtlistener.com.

import { mkdirSync, writeFileSync } from "node:fs";
import path from "node:path";
import { budgetAllows, createClient, readCourtListenerToken } from "./client.mjs";
import { REPO_ROOT } from "./io.mjs";

const OUT_DIR = path.join(REPO_ROOT, "internal/docs/legal-intel/recon");
const OUT_PATH = path.join(OUT_DIR, "matter-28-verification-sweep.json");
const MIN_INTERVAL_MS = 13_000;

// Authorities to verify. `expect` records what the citing party asserts, so the
// sweep can surface a mismatch rather than silently confirming a wrong year.
const CITES = [
  // Defense's previewed 12(b)(6) authorities (Van Dine M&C, Sept. 3, 2026).
  { id: "az-students", q: '"Arizona Students\' Association"', expect: "824 F.3d 858 (9th Cir. 2016) — 1A retaliation chill" },
  { id: "kildare", q: '"Kildare v. Saenz"', expect: "325 F.3d 1078 (9th Cir. 2003) — due process" },
  { id: "dz-reserve", q: '"DZ Reserve"', expect: "96 F.4th 1223 (9th Cir. 2024) — reliance/intent" },
  { id: "zetz", q: '"Zetz v. Boston Scientific"', expect: "398 F. Supp. 3d 700 (E.D. Cal. 2019) — fraud pleading" },
  { id: "schreiber", q: '"Serv-Well Furniture"', expect: "806 F.2d 1393 — defense cites (9th Cir. 2004); actually 1986" },
  // Plaintiff-side load-bearing authorities.
  { id: "west-atkins", q: '"West v. Atkins"', expect: "487 U.S. 42 (1988) — private contractor state action" },
  { id: "richardson", q: '"Richardson v. McKnight"', expect: "521 U.S. 399 (1997) — no QI for private prison guards" },
  { id: "jensen", q: '"Jensen v. Lane County"', expect: "222 F.3d 570 (9th Cir. 2000) — private psychiatrist state actor" },
  { id: "halvorsen", q: '"Halvorsen v. Baird"', expect: "146 F.3d 680 (9th Cir. 1998) — private detox facility" },
  { id: "neal-shimoda", q: '"Neal v. Shimoda"', expect: "131 F.3d 818 (9th Cir. 1997) — sex offender classification liberty interest" },
  { id: "cedric-kushner", q: '"Cedric Kushner Promotions"', expect: "533 U.S. 158 (2001) — RICO person/enterprise distinctness" },
  // Does any court cite the treatment-completion statute or CASOMB at all?
  { id: "pc-3008", q: '"3008(d)(2)"', expect: "Penal Code 3008(d)(2) — treatment completion determination" },
  { id: "casomb", q: '"CASOMB"', expect: "CA Sex Offender Management Board — any judicial treatment" },
  { id: "hope-psychotherapy", q: '"HOPE Psychotherapy"', expect: "the corporate defendant, as a named party anywhere" },
];

// RECAP docket-text searches: is anyone else litigating this theory?
const RECAP_QUERIES = [
  { id: "recap-hope", q: '"HOPE Psychotherapy"' },
  { id: "recap-casomb", q: '"CASOMB"' },
  { id: "recap-3008", q: '"3008(d)(2)"' },
  { id: "recap-sotp-blanket", q: '"sex offender management program" "blanket"' },
];

const DOCKETS = [
  { id: 73646240, label: "Matter 28 — Newanforbi v. Smith (N.D. Cal. 3:26-cv-07504-LJC)" },
];

const dryRun = process.argv.includes("--dry-run");

async function runSearch(client, type, q) {
  const params = new URLSearchParams({ type, q, page_size: "20" });
  if (type === "r") params.set("order_by", "dateFiled desc");
  const page = await client.request(
    `https://www.courtlistener.com/api/rest/v4/search/?${params}`,
    { auth: true },
  );
  const rows = Array.isArray(page?.results) ? page.results : [];
  return { count: page?.count ?? null, rows };
}

async function main() {
  const token = readCourtListenerToken();
  if (!token) {
    console.error("COURTLISTENER_TOKEN is not set.");
    process.exit(1);
  }
  const client = createClient({ token, minIntervalMs: MIN_INTERVAL_MS });

  let usage;
  try {
    usage = await client.getApiUsage();
  } catch (err) {
    console.error(`Could not read /api-usage/: ${err.message}. Refusing to run.`);
    process.exit(1);
  }
  const need = CITES.length + RECAP_QUERIES.length + DOCKETS.length * 2;
  const budget = budgetAllows(usage, { minDaily: need, minHourly: 2 });
  if (!budget.ok) {
    console.error(`Quota too low: ${budget.reason} (need ~${need})`);
    process.exit(1);
  }
  console.log(`Quota OK — daily ${budget.remaining.daily}, hourly ${budget.remaining.hourly}`);

  const cites = [];
  for (const c of CITES) {
    try {
      const { count, rows } = await runSearch(client, "o", c.q);
      console.log(`\n[${c.id}] ${c.q} -> ${count} opinion hits   (expect: ${c.expect})`);
      for (const r of rows.slice(0, 5)) {
        console.log(`    ${r.caseName ?? "?"} | ${r.court ?? "?"} | ${r.dateFiled ?? "?"} | ${r.citation ?? ""}`);
      }
      cites.push({
        ...c,
        count,
        hits: rows.slice(0, 5).map((r) => ({
          caseName: r.caseName ?? null,
          court: r.court ?? null,
          dateFiled: r.dateFiled ?? null,
          citation: r.citation ?? null,
          docketNumber: r.docketNumber ?? null,
          absoluteUrl: r.absolute_url ? `https://www.courtlistener.com${r.absolute_url}` : null,
        })),
      });
    } catch (err) {
      console.error(`[${c.id}] FAILED: ${err.message}`);
      cites.push({ ...c, error: err.message });
    }
  }

  const recap = [];
  for (const c of RECAP_QUERIES) {
    try {
      const { count, rows } = await runSearch(client, "r", c.q);
      console.log(`\n[${c.id}] ${c.q} -> ${count} RECAP hits`);
      for (const r of rows.slice(0, 10)) {
        console.log(`    ${r.caseName ?? "?"} | ${r.court ?? "?"} | ${r.dateFiled ?? "?"} | ${r.docketNumber ?? "?"}`);
      }
      recap.push({ ...c, count, hits: rows.slice(0, 10).map((r) => ({
        caseName: r.caseName ?? null, court: r.court ?? null,
        dateFiled: r.dateFiled ?? null, docketNumber: r.docketNumber ?? null,
        absoluteUrl: r.docket_absolute_url ? `https://www.courtlistener.com${r.docket_absolute_url}` : null,
      })) });
    } catch (err) {
      console.error(`[${c.id}] FAILED: ${err.message}`);
      recap.push({ ...c, error: err.message });
    }
  }

  const dockets = [];
  for (const d of DOCKETS) {
    try {
      const entries = await client.listDocketEntries({ docketId: d.id });
      console.log(`\n[docket ${d.id}] ${d.label} -> ${entries.length} entries`);
      for (const e of entries) {
        const desc = String(e.description ?? "").replace(/\s+/g, " ").slice(0, 260);
        console.log(`    #${e.entry_number ?? "?"} [${e.date_filed ?? "?"}] ${desc}`);
      }
      dockets.push({ ...d, entryCount: entries.length, entries: entries.map((e) => ({
        entryNumber: e.entry_number ?? null, dateFiled: e.date_filed ?? null,
        description: String(e.description ?? "").replace(/\s+/g, " ") || null,
      })) });
    } catch (err) {
      console.error(`[docket ${d.id}] FAILED: ${err.message}`);
      dockets.push({ ...d, error: err.message });
    }
  }

  const payload = {
    generated_at: new Date().toISOString(),
    purpose:
      "Matter 28 verification sweep: confirm the authorities in defense counsel's Sept. 3, 2026 previewed 12(b)(6) grounds and Plaintiff's load-bearing authorities, and pull the docket for the res judicata timeline.",
    api: "CourtListener REST v4",
    cites,
    recap,
    dockets,
  };
  if (dryRun) { console.log("--dry-run: not writing"); return; }
  mkdirSync(OUT_DIR, { recursive: true });
  writeFileSync(OUT_PATH, `${JSON.stringify(payload, null, 2)}\n`, "utf8");
  console.log(`\nWrote ${path.relative(REPO_ROOT, OUT_PATH)}`);
}

main().catch((err) => { console.error(err); process.exit(1); });
