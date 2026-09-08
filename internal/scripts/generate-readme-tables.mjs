#!/usr/bin/env node
// ==========================================================
// Regenerate marked README sections from portfolio data.
//
// Source of truth:
//   - internal/src/data/matters/NN.json  (matter tables + counts)
//   - internal/src/data/timeline.json    (upcoming deadlines)
//   - internal/src/data/damages.js       (damages summary + aggregates)
//   - internal/src/data/lawyerFees.js    (attorney-fees cluster table)
//
// Markers (HTML comments) in README.md delimit regenerable blocks:
//   <!-- PORTFOLIO:<NAME>:START -->
//   ...
//   <!-- PORTFOLIO:<NAME>:END -->
//
// Usage:
//   npm run generate:readme           # write README.md
//   npm run generate:readme -- --check  # exit 1 if stale
// ==========================================================
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { loadMatters } from "./load-matters.mjs";
import { isSettledLifecycle, lifecycleLabel, readmeBucket } from "./matter-lifecycle.mjs";
import { effectiveStatusLabel } from "./status-label.mjs";
import { formatMatterRefs, parseMatterRefs } from "../src/utils/matterRefs.js";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = path.resolve(__dirname, "..", "..");
const README = path.join(REPO_ROOT, "README.md");
const checkOnly = process.argv.includes("--check");

const MONTHS = {
  jan: 0,
  january: 0,
  feb: 1,
  february: 1,
  mar: 2,
  march: 2,
  apr: 3,
  april: 3,
  may: 4,
  jun: 5,
  june: 5,
  jul: 6,
  july: 6,
  aug: 7,
  august: 7,
  sep: 8,
  sept: 8,
  september: 8,
  oct: 9,
  october: 9,
  nov: 10,
  november: 10,
  dec: 11,
  december: 11,
};

function escapeCell(value) {
  return String(value ?? "")
    .replace(/\r?\n/g, " ")
    .replace(/\|/g, "\\|")
    .trim();
}

function truncate(text, max) {
  const s = String(text ?? "").replace(/\s+/g, " ").trim();
  if (s.length <= max) return s;

  // Prefer a natural clause break before hard truncation.
  const clauseBreaks = [];
  for (const re of [/;\s+/g, /\s+[—–-]\s+/g, /\.\s+(?=[A-Z])/g]) {
    let m;
    while ((m = re.exec(s)) !== null) {
      const end = m.index + (s[m.index] === "." ? 1 : 0);
      if (end >= 48 && end <= max) clauseBreaks.push(end);
    }
  }
  if (clauseBreaks.length) {
    return s.slice(0, Math.max(...clauseBreaks)).trim();
  }

  const cut = s.slice(0, max);
  const word = cut.lastIndexOf(" ");
  return `${(word > 40 ? cut.slice(0, word) : cut).trim()}…`;
}

/** Populated after timeline.json loads — maps matter number → events. */
const eventsByMatter = new Map();

// A table cell wants the short posture label (hand override or derived from
// phase + next posture event). The narrative `status` stays out of README tables.
function shortStatus(matter, { closed = false } = {}) {
  const events = eventsByMatter.get(matter.number) ?? [];
  const label = effectiveStatusLabel(matter, events).replace(/\s+/g, " ").trim();
  if (closed && matter.lifecycle && matter.lifecycle !== "closed") {
    const lifecycle = lifecycleLabel(matter.lifecycle).toUpperCase();
    if (!label.toUpperCase().startsWith(lifecycle)) {
      return escapeCell(`**${lifecycle}** — ${label}`);
    }
  }
  return escapeCell(label);
}

function bucket(matter) {
  return readmeBucket(matter.lifecycle);
}

function parsePortfolioDate(dateStr) {
  const s = String(dateStr || "").trim();
  const m = s.match(/^([A-Za-z]+)\.?\s+(\d{1,2}),?\s+(\d{4})$/);
  if (!m) return null;
  const month = MONTHS[m[1].toLowerCase()];
  if (month == null) return null;
  return new Date(Date.UTC(Number(m[3]), month, Number(m[2])));
}

function money(n) {
  const rounded = Math.round(Number(n) || 0);
  return `$${rounded.toLocaleString("en-US")}`;
}

function replaceBlock(readme, name, body) {
  const start = `<!-- PORTFOLIO:${name}:START -->`;
  const end = `<!-- PORTFOLIO:${name}:END -->`;
  const startIdx = readme.indexOf(start);
  const endIdx = readme.indexOf(end);
  if (startIdx === -1 || endIdx === -1 || endIdx < startIdx) {
    throw new Error(`README.md missing markers for PORTFOLIO:${name}`);
  }
  const before = readme.slice(0, startIdx + start.length);
  const after = readme.slice(endIdx);
  const inner = body.endsWith("\n") ? body : `${body}\n`;
  return `${before}\n${inner}${after}`;
}

const cases = loadMatters();
const timeline = JSON.parse(
  fs.readFileSync(path.join(REPO_ROOT, "internal/src/data/timeline.json"), "utf8"),
);
for (const event of timeline) {
  for (const matter of parseMatterRefs(event.matters).numbers) {
    if (!matter) continue;
    if (!eventsByMatter.has(matter)) eventsByMatter.set(matter, []);
    eventsByMatter.get(matter).push(event);
  }
}
const { damages_table } = await import(pathToFileURL(path.join(REPO_ROOT, "internal/src/data/damages.js")).href);
const { lawyer_fees_summary: feeSummary, lawyer_fees: feeRows } = await import(
  pathToFileURL(path.join(REPO_ROOT, "internal/src/data/lawyerFees.js")).href
);

const citationVerificationPath = path.join(
  REPO_ROOT,
  "internal/docs/citation_verification.json",
);
let citationVerification = null;
if (fs.existsSync(citationVerificationPath)) {
  citationVerification = JSON.parse(fs.readFileSync(citationVerificationPath, "utf8"));
}

// Active/Open now includes settled matters -- still on the docket, same as
// isOpenLifecycle. "settled" here is a separate, non-exclusive annotation
// (a matter can be both open and settled at once), not a third partition
// member, so it's tracked apart from bucket() and doesn't double-count
// against Total Matters below.
const active = cases.filter((m) => bucket(m) === "active");
const closed = cases.filter((m) => bucket(m) === "closed");
const settled = cases.filter((m) => isSettledLifecycle(m.lifecycle));

const settledLabel = settled.length
  ? settled
      .map((m) => {
        const when = (m.status.match(/SETTLED\s*[—-]\s*([^;(]+)/i) || [])[1]?.trim();
        return `${m.number} — ${m.caption}${when ? `, ${when}` : ""}`;
      })
      .join("; ")
  : "none";

const cons = damages_table.reduce((s, r) => s + (r.conservative || 0), 0);
const mod = damages_table.reduce((s, r) => s + (r.moderate || 0), 0);
const agg = damages_table.reduce((s, r) => s + (r.aggressive || 0), 0);

const roundK = (n) => Math.round(Number(n) / 1000) * 1000;

// One contiguous GFM table — HTML comments between rows break GitHub rendering.
const overviewTable = [
  `| Field | Detail |`,
  `|---|---|`,
  `| Plaintiff | Brendan Ngehsi Newanforbi |`,
  `| Representation | Pro Se / In Propria Persona |`,
  `| Jurisdictions | USDC E.D. Cal., USDC N.D. Cal., San Joaquin Sup. Ct., Alameda Sup. Ct., Sacramento Sup. Ct., Santa Clara Sup. Ct. |`,
  `| Total Matters | ${cases.length} |`,
  `| Active / Open | ${active.length} |`,
  `| — of which Settled | ${settled.length}${settled.length ? ` (Matter ${settledLabel})` : ""} |`,
  `| Dismissed / Closed / Abandoned | ${closed.length} |`,
  `| Aggregate Exposure (Conservative) | ~${money(roundK(cons))}+ |`,
  `| Aggregate Exposure (Moderate) | ~${money(roundK(mod))}+ |`,
  `| Aggregate Exposure (Aggressive) | ~${money(roundK(agg))}+ |`,
  `| Last Updated | September 7, 2026 |`,
].join("\n");

const activeTable = [
  `| # | Caption | Case No. | Court | Type | Status |`,
  `|---|---|---|---|---|---|`,
  ...active.map(
    (m) =>
      `| ${m.number} | ${escapeCell(m.caption)} | ${escapeCell(m.case_no)} | ${escapeCell(m.court)} | ${escapeCell(m.type)} | ${shortStatus(m)} |`,
  ),
].join("\n");

const closedTable = [
  `| # | Caption | Case No. | Court | Disposition |`,
  `|---|---|---|---|---|`,
  ...closed.map(
    (m) =>
      `| ${m.number} | ${escapeCell(m.caption)} | ${escapeCell(m.case_no)} | ${escapeCell(m.court)} | ${shortStatus(m, { closed: true })} |`,
  ),
].join("\n");

const upcoming = timeline
  .filter((t) => t.upcoming === true)
  .map((t, i) => ({ ...t, _i: i, _d: parsePortfolioDate(t.date) }))
  .sort((a, b) => {
    if (a._d && b._d) return a._d - b._d || a._i - b._i;
    if (a._d) return -1;
    if (b._d) return 1;
    return a._i - b._i;
  });

const deadlinesTable = [
  `| Date | Matter | Event |`,
  `|---|---|---|`,
  ...upcoming.map(
    (t) => `| ${escapeCell(t.date)} | ${escapeCell(formatMatterRefs(t.matters))} | ${escapeCell(truncate(t.event, 220))} |`,
  ),
].join("\n");

const damagesTable = [
  `| Category | Matters | Conservative | Moderate | Aggressive |`,
  `|---|---|---|---|---|`,
  ...damages_table.map(
    (r) =>
      `| ${escapeCell(r.category)} | ${escapeCell(formatMatterRefs(r.matters))} | ${money(r.conservative)} | ${money(r.moderate)} | ${money(r.aggressive)} |`,
  ),
  `| **Portfolio Total (pre-deduplication)** | | **${money(cons)}** | **${money(mod)}** | **${money(agg)}** |`,
].join("\n");

const abandoned = closed.filter((m) => m.lifecycle === "abandoned");
const dismissed = closed.filter((m) => m.lifecycle === "dismissed");
const otherClosed = closed.filter((m) => m.lifecycle === "closed");
const closedCountNote =
  `*Of the ${closed.length} dismissed/closed/abandoned matters: ${abandoned.length} abandoned, ` +
  `${dismissed.length} dismissed, ${otherClosed.length} otherwise closed ` +
  `(structured \`lifecycle\` on each matter JSON). See [All Matters](#all-matters) below for the full disposition table. ` +
  `Pre-filing matters stay in the Active table.*`;

const feeByNumber = new Map((feeRows || []).map((row) => [row.number, row]));
const m32 = feeByNumber.get(32);
const m33 = feeByNumber.get(33);
const feeDate = feeSummary.analysisDate || "2026-08-08";
const [fy, fm, fd] = String(feeDate).split("-").map(Number);
const feeDateLabel = new Date(Date.UTC(fy, fm - 1, fd)).toLocaleDateString("en-US", {
  month: "long",
  day: "numeric",
  year: "numeric",
  timeZone: "UTC",
});
const clusterOrder = ["cluster1", "cluster2", "cluster3", "cluster4", "cluster6"];
const feeClusterRows = clusterOrder
  .map((key) => feeSummary.byCluster[key])
  .filter(Boolean)
  .map(
    (c) =>
      `| ${escapeCell(c.label)} | ${escapeCell(c.matters.join(", "))} | ${money(c.costLow)} | ${money(c.costMid)} | ${money(c.costHigh)} |`,
  );
const attorneyFeesBlock = [
  `Plaintiff is representing himself pro se across all ${feeSummary.totalMatters} matters. The figures below represent what he would have been required to spend on private counsel to litigate this portfolio — costs he has absorbed entirely through self-representation. Based on real page counts extracted from ${feeSummary.totalDocumentsAnalyzed} documents / ${feeSummary.totalPagesReal.toLocaleString("en-US")} pages across matters with uploaded filings (Matter 32: ${m32?.documentsCount ?? "—"} PDFs / ${m32?.totalPagesReal?.toLocaleString("en-US") ?? "—"} pages — N.D. Cal. ndcal/ filing billed; from-01|02|20|24/ stay attributed to source matters; Matter 33: ${m33?.documentsCount ?? "—"} PDFs / ${m33?.totalPagesReal?.toLocaleString("en-US") ?? "—"} pages — N.D. Cal. refile + Nov. 1 / APS evidence; from-07/from-08 drafting stays on Matters 7/8; Matter 31 has no uploaded PDFs of its own), classified by document type and priced at a blended rate of **$${feeSummary.methodology.blendedHourlyRate}/hour** (senior partner $${feeSummary.methodology.rateRange.seniorPartner[0]}–$${feeSummary.methodology.rateRange.seniorPartner[1]} / mid-associate $${feeSummary.methodology.rateRange.midAssociate[0]}–$${feeSummary.methodology.rateRange.midAssociate[1]} / paralegal $${feeSummary.methodology.rateRange.paralegal[0]}–$${feeSummary.methodology.rateRange.paralegal[1]}). Opposing-party filings billed at light review rate only. Fee analysis date: ${feeDateLabel}.`,
  ``,
  `| Cluster | Matters | Low | Mid | High |`,
  `|---|---|---|---|---|`,
  ...feeClusterRows,
  `| **Portfolio Total** | **${feeSummary.totalMatters} matters** | **${money(feeSummary.totalEstimatedCost.low)}** | **${money(feeSummary.totalEstimatedCost.mid)}** | **${money(feeSummary.totalEstimatedCost.high)}** |`,
  `| **Estimated Hours** | | **${feeSummary.totalEstimatedHours.low.toLocaleString("en-US")} hrs** | **${feeSummary.totalEstimatedHours.mid.toLocaleString("en-US")} hrs** | **${feeSummary.totalEstimatedHours.high.toLocaleString("en-US")} hrs** |`,
  ``,
  `*Plaintiff has litigated all ${feeSummary.totalMatters} matters pro se, absorbing the full economic equivalent of the above without compensation. Fee-shifting statutes (42 U.S.C. §1988, PC §290.46(j)(4)(A), RICO 18 U.S.C. §1964(c), FCRA, ICRAA) apply across the majority of active matters — mandatory fee recovery upon prevailing substantially offsets or eliminates the above costs.*`,
].join("\n");

const statusOrder = [
  "VERIFIED",
  "MISCITED",
  "MISCHARACTERIZED",
  "MISQUOTED",
  "NOT_FOUND",
  "UNVERIFIED",
];
const statusCounts = citationVerification?.statusCounts || {};
const citationScoreboard = citationVerification
  ? [
      `| Status | Count |`,
      `|---|---|`,
      ...statusOrder
        .filter((k) => statusCounts[k] != null)
        .map((k) => `| ${k} | ${statusCounts[k]} |`),
      ...Object.keys(statusCounts)
        .filter((k) => !statusOrder.includes(k))
        .sort()
        .map((k) => `| ${k} | ${statusCounts[k]} |`),
      ``,
      `Paired authorities: **${citationVerification.corpusAuthorities ?? "—"}**. ` +
        `P0 (plaintiff-only UNVERIFIED): **${citationVerification.queue?.plaintiffOnlyUnverified ?? "—"}**. ` +
        `P1 (plaintiff-only bad status): **${citationVerification.queue?.plaintiffOnlyBad ?? "—"}**. ` +
        `Ledger date: ${citationVerification.generatedDate || "—"}.`,
    ].join("\n")
  : [
      `| Status | Count |`,
      `|---|---|`,
      `| _(run \`npm run citations:verify\`)_ | — |`,
    ].join("\n");

let readme = fs.readFileSync(README, "utf8");
const replacements = {
  OVERVIEW_TABLE: overviewTable,
  CLOSED_COUNT_NOTE: closedCountNote,
  ACTIVE_MATTERS: activeTable,
  CLOSED_MATTERS: closedTable,
  UPCOMING_DEADLINES: deadlinesTable,
  DAMAGES_SUMMARY: damagesTable,
  ATTORNEY_FEES: attorneyFeesBlock,
  CITATION_SCOREBOARD: citationScoreboard,
};

for (const [name, body] of Object.entries(replacements)) {
  readme = replaceBlock(readme, name, body);
}

if (checkOnly) {
  const current = fs.readFileSync(README, "utf8");
  if (current !== readme) {
    console.error("README.md generated tables are stale — run npm run generate:readme");
    process.exit(1);
  }
  console.log(
    `OK — README portfolio tables are current (${active.length} active/open, incl. ${settled.length} settled, ${closed.length} closed, ${upcoming.length} upcoming` +
      (citationVerification
        ? `, ${citationVerification.corpusAuthorities} citation authorities`
        : "") +
      ").",
  );
  process.exit(0);
}

fs.writeFileSync(README, readme);
console.log(
  `Updated ${path.relative(REPO_ROOT, README)} ` +
    `(${active.length} active/open, incl. ${settled.length} settled / ${closed.length} closed / ${upcoming.length} upcoming).`,
);
