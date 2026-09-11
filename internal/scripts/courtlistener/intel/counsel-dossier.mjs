#!/usr/bin/env node
// Opposing counsel dossier builder — Legal Intelligence layer.
//
// Builds a profile of opposing counsel from CourtListener:
//   - identity resolution (bound docket parties, or --name / --attorney-id)
//   - RECAP docket history (courts, volume, date range)
//   - client concentration (defendant-side party clustering over sampled cases)
//   - subject-matter concentration (keyword heuristic over sampled case names)
//   - motion-pattern analysis against YOU, from locally synced docket entries (zero API cost)
//
// Usage:
//   npm run intel:counsel -- --matter 28
//   npm run intel:counsel -- --matter 28 --link        # also write opposing_counsel onto the matter
//   npm run intel:counsel -- --name "Jane Smith" --matter 28
//   npm run intel:counsel -- --attorney-id 12345 --matter 28
//   npm run intel:counsel -- --name "Jane Smith" --firm "Big Law LLP"
//
// Output: internal/docs/legal-intel/counsel/<slug>.json + .md
// A dossier run costs <10 API calls. Run on demand, not on a schedule.

import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { loadMatters } from "../../load-matters.mjs";
import { budgetAllows, createClient, readCourtListenerToken } from "../client.mjs";
import { loadLedger } from "../io.mjs";
import { validateMatter } from "../../lib/matter-schema.mjs";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const INTEL_DIR = path.resolve(__dirname, "../../../docs/legal-intel/counsel");
const MATTERS_DIR = path.resolve(__dirname, "../../../src/data/matters");

const STOP_WORDS = new Set([
  "inc", "incorporated", "llc", "corp", "corporation", "co", "company", "ltd",
  "limited", "pllc", "pa", "lp", "llp", "the", "of", "d", "b", "a", "db", "dba",
  "aka", "fka", "et", "al",
]);

function parseArgs(argv) {
  const out = {};
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg.startsWith("--")) {
      const key = arg.slice(2);
      const next = argv[i + 1];
      if (next && !next.startsWith("--")) {
        out[key] = next;
        i += 1;
      } else {
        out[key] = true;
      }
    }
  }
  return out;
}

function slugify(name) {
  return String(name ?? "")
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .slice(0, 80) || "unknown";
}

function tokens(value) {
  return String(value ?? "")
    .toLowerCase()
    .replace(/[^a-z0-9\s]/g, " ")
    .split(/\s+/)
    .filter((t) => t.length > 1 && !STOP_WORDS.has(t));
}

/** Fraction of the party-name tokens that appear in the matter's defendants string. */
function defendantMatchScore(partyName, defendants) {
  const partyTokens = new Set(tokens(partyName));
  if (partyTokens.size === 0) return { score: 0, hits: 0 };
  const defenseTokens = new Set(tokens(defendants));
  let hits = 0;
  for (const t of partyTokens) if (defenseTokens.has(t)) hits += 1;
  return { score: hits / partyTokens.size, hits };
}

function attorneyName(attorney) {
  if (!attorney) return null;
  if (typeof attorney === "string") return null; // URL form; resolved separately
  return attorney.name ?? attorney.attorney_name ?? null;
}

function attorneyId(attorney) {
  if (!attorney || typeof attorney === "string") return null;
  return attorney.id ?? null;
}

/**
 * From a docket's party list, find attorneys whose party looks like one of the
 * matter's defendants. Returns ranked candidates; auto-picks only when one
 * candidate is clearly best (unique max, >=2 token hits, score >= 0.5).
 */
export function discoverCounselCandidates(parties, defendants) {
  const seen = new Map();
  for (const party of parties ?? []) {
    const partyName = party?.name ?? "";
    const { score, hits } = defendantMatchScore(partyName, defendants);
    const attorneys = Array.isArray(party?.attorneys) ? party.attorneys : [];
    for (const attorney of attorneys) {
      const name = attorneyName(attorney);
      if (!name) continue;
      const key = slugify(name);
      const prev = seen.get(key);
      const candidate = {
        name,
        attorney_id: attorneyId(attorney),
        party: partyName,
        score,
        hits,
      };
      if (!prev || candidate.score > prev.score) seen.set(key, candidate);
    }
  }
  const ranked = [...seen.values()].sort((a, b) => b.score - a.score || b.hits - a.hits);
  let autoPick = null;
  if (
    ranked.length > 0 &&
    ranked[0].hits >= 2 &&
    ranked[0].score >= 0.5 &&
    (ranked.length === 1 || ranked[0].score > ranked[1].score)
  ) {
    autoPick = ranked[0];
  }
  return { candidates: ranked, autoPick };
}

const MOTION_PATTERNS = [
  ["motion_to_dismiss", /\bmotion to dismiss\b|\brule\s*12\(b\)/i],
  ["summary_judgment", /\bsummary judgment\b/i],
  ["discovery_motion", /\bmotion to compel\b|\bprotective order\b/i],
  ["motion_to_strike", /\bmotion to strike\b/i],
  ["sanctions", /\bsanctions\b/i],
  ["settlement", /\bsettlement\b/i],
  ["voluntary_dismissal", /\bvoluntary dismissal\b|\bstipulat\w+\s+(of\s+)?dismissal\b/i],
  ["default", /\bdefault judgment\b|\bentry of default\b/i],
  ["appeal", /\bnotice of appeal\b/i],
];

/** Classify locally synced docket entries into motion-pattern counts (zero API cost). */
export function analyzeMotionPatterns(entries) {
  const counts = Object.fromEntries(MOTION_PATTERNS.map(([key]) => [key, 0]));
  let analyzed = 0;
  for (const entry of entries ?? []) {
    const text = String(entry?.description ?? "");
    if (!text) continue;
    analyzed += 1;
    for (const [key, re] of MOTION_PATTERNS) {
      if (re.test(text)) counts[key] += 1;
    }
  }
  return { entries_analyzed: analyzed, patterns: counts };
}

export function analyzeHistory(dockets) {
  const courts = {};
  const sample = [];
  let earliest = null;
  let latest = null;
  for (const d of dockets ?? []) {
    const court = d?.court ?? d?.court_id ?? "unknown";
    courts[court] = (courts[court] ?? 0) + 1;
    const filed = String(d?.dateFiled ?? d?.date_filed ?? "").slice(0, 10);
    if (filed) {
      if (!earliest || filed < earliest) earliest = filed;
      if (!latest || filed > latest) latest = filed;
    }
    if (sample.length < 25) {
      sample.push({
        case_name: d?.caseName ?? d?.case_name ?? null,
        docket_number: d?.docketNumber ?? d?.docket_number ?? null,
        court,
        date_filed: filed || null,
      });
    }
  }
  return {
    dockets_found: dockets?.length ?? 0,
    courts,
    date_range: { earliest, latest },
    sample,
    sample_truncated: (dockets?.length ?? 0) > sample.length,
  };
}

// --- Client & subject-matter concentration (v2) ---

const ENTITY_SUFFIXES = new Set([
  "inc", "incorporated", "corp", "corporation", "llc", "ltd", "limited",
  "co", "company", "pllc", "pa", "lp", "llp", "plc", "holdings", "group",
  "services", "solutions", "systems",
]);

/** Split "Plaintiff v. Defendant" into its parties. Null when no separator. */
export function splitCaseName(caseName) {
  const text = String(caseName ?? "").trim();
  const m = text.match(/^(.*?)\s+v(?:s?\.?)\s+(.*)$/i);
  if (!m) return null;
  const plaintiff = m[1].trim();
  const defendant = m[2].trim().replace(/\s+et\s+al\.?$/i, "").trim();
  if (!plaintiff || !defendant) return null;
  return { plaintiff, defendant };
}

/** Normalize a party name to a clustering key plus a display form. */
export function normalizeClientName(name) {
  const display = String(name ?? "")
    .replace(/\s+et\s+al\.?$/i, "")
    .replace(/\s+/g, " ")
    .trim();
  const key = display
    .toLowerCase()
    .replace(/[^a-z0-9\s]/g, " ")
    .split(/\s+/)
    .filter((t) => t && !ENTITY_SUFFIXES.has(t) && !STOP_WORDS.has(t))
    .join(" ");
  return { key: key || display.toLowerCase(), display };
}

/**
 * Cluster sampled cases by party. For defense-side counsel, repeat
 * defendant-side names are the client base. Pure function over the
 * history sample (case_name strings).
 */
export function analyzeClients(sample) {
  const defendants = new Map();
  const plaintiffs = new Map();
  let parsed = 0;
  for (const d of sample ?? []) {
    const parts = splitCaseName(d?.case_name);
    if (!parts) continue;
    parsed += 1;
    for (const [side, map] of [
      ["defendant", defendants],
      ["plaintiff", plaintiffs],
    ]) {
      const { key, display } = normalizeClientName(parts[side]);
      if (!key) continue;
      const prev = map.get(key) ?? { name: display, count: 0 };
      prev.count += 1;
      if (display.length > prev.name.length) prev.name = display;
      map.set(key, prev);
    }
  }
  const ranked = (map) =>
    [...map.values()].sort((a, b) => b.count - a.count || a.name.localeCompare(b.name));
  const defendantList = ranked(defendants);
  return {
    cases_parsed: parsed,
    defendants: defendantList,
    plaintiffs: ranked(plaintiffs),
    top_defendant: defendantList[0] ?? null,
  };
}

// Consumer-reporting agencies / background-screening companies. A repeat
// defendant-side appearance here is the FCRA/screening signal.
const KNOWN_CRAS = [
  "checkr",
  "disa",
  "equifax",
  "first advantage",
  "inflection",
  "sterling",
  "accurate background",
  "appfolio",
  "hireright",
  "goodhire",
  "certn",
  "transunion",
  "experian",
];

const SUBJECT_RULES = [
  [
    "fcra_background_screening",
    /\bfcra\b|fair credit reporting|background (check|screening)|consumer report|investigative consumer/i,
  ],
  [
    "employment_discrimination",
    /discrimination|harassment|retaliation|wrongful termination|title vii|\bfeha\b|\bada\b|\badea\b/i,
  ],
  [
    "wage_hour",
    /\bwage\b|overtime|\bflsa\b|\bpaga\b|meal (and|&) rest|rest break|minimum wage/i,
  ],
  [
    "consumer_protection",
    /\bucl\b|unfair competition|\bclra\b|false advertising/i,
  ],
  ["privacy", /\bcipa\b|\bccpa\b|\bbipa\b|biometric|invasion of privacy|wiretap/i],
  ["class_action", /class action|putative class/i],
];

/**
 * Keyword heuristic over sampled case names. Tags are directional, not legal
 * determinations. Also flags the background-screening ecosystem when a
 * defendant matches a known consumer-reporting agency.
 */
export function analyzeSubjects(sample) {
  const tags = {};
  const craHits = new Set();
  for (const d of sample ?? []) {
    const text = String(d?.case_name ?? "");
    const hit = new Set();
    for (const [tag, re] of SUBJECT_RULES) {
      if (re.test(text)) hit.add(tag);
    }
    const parts = splitCaseName(text);
    if (parts) {
      const defKey = normalizeClientName(parts.defendant).key;
      for (const cra of KNOWN_CRAS) {
        if (defKey.includes(cra)) {
          hit.add("fcra_background_screening");
          craHits.add(cra);
        }
      }
    }
    for (const t of hit) tags[t] = (tags[t] ?? 0) + 1;
  }
  const sorted = Object.entries(tags).sort((a, b) => b[1] - a[1]);
  return {
    tags,
    primary: sorted[0]?.[0] ?? null,
    screening_ecosystem: {
      detected: craHits.size > 0,
      matched_cra_clients: [...craHits].sort(),
    },
    note: "Keyword heuristic over sampled case names; directional, not a legal determination.",
  };
}

/** Honest identity labeling: pinned attorney ID vs name-based match. */
export function identityConfidence({ attorney_id, firm } = {}) {
  if (attorney_id != null) {
    return {
      level: "verified",
      label: `Pinned to CourtListener attorney ID ${attorney_id}`,
    };
  }
  return {
    level: "name-based",
    label:
      "Name-based match (no CourtListener attorney ID). Client and subject signals are directional; pin --attorney-id to verify.",
  };
}

function renderMarkdown(dossier) {
  const ident = dossier.identity ?? identityConfidence(dossier);
  const lines = [
    `# Counsel dossier: ${dossier.name}`,
    ``,
    `- Generated: ${dossier.generated_at}`,
    `- Identity: ${ident.label}`,
    `- Firm: ${dossier.firm ?? "unknown"}`,
    `- Linked matters: ${(dossier.linked_matters ?? []).join(", ") || "none"}`,
    ``,
  ];

  const clients = dossier.clients;
  if (clients?.defendants?.length) {
    lines.push(`## Client concentration (defendant-side, sampled cases)`, ``);
    if (clients.top_defendant) {
      lines.push(
        `- Top repeat defendant: **${clients.top_defendant.name}** (${clients.top_defendant.count} of ${clients.cases_parsed} parsed cases)`,
      );
    }
    for (const c of clients.defendants.slice(0, 10)) {
      if (clients.top_defendant && c.name === clients.top_defendant.name) continue;
      lines.push(`- ${c.name} — ${c.count} case${c.count === 1 ? "" : "s"}`);
    }
    lines.push(``);
  }

  const subjects = dossier.subjects;
  if (subjects && Object.keys(subjects.tags).length > 0) {
    lines.push(`## Subject-matter concentration`, ``);
    if (subjects.primary) lines.push(`- Primary signal: **${subjects.primary}**`);
    for (const [tag, count] of Object.entries(subjects.tags).sort((a, b) => b[1] - a[1])) {
      if (tag !== subjects.primary) lines.push(`- ${tag}: ${count} case${count === 1 ? "" : "s"}`);
    }
    if (subjects.screening_ecosystem?.detected) {
      lines.push(
        `- Background-screening ecosystem: **yes** — ${subjects.screening_ecosystem.matched_cra_clients.join(", ")}`,
      );
    }
    lines.push(`- _${subjects.note}_`, ``);
  }

  lines.push(
    `## Docket history (RECAP search)`,
    ``,
    `- Dockets found: ${dossier.history.dockets_found}`,
    `- Date range: ${dossier.history.date_range.earliest ?? "?"} to ${dossier.history.date_range.latest ?? "?"}`,
    `- Courts:`,
  );
  for (const [court, count] of Object.entries(dossier.history.courts).sort((a, b) => b[1] - a[1])) {
    lines.push(`  - ${court}: ${count}`);
  }
  lines.push(``);

  if (dossier.history.sample?.length) {
    lines.push(`## Sampled cases`, ``);
    for (const s of dossier.history.sample) {
      lines.push(
        `- ${s.case_name ?? "?"} — ${s.docket_number ?? "?"} (${s.court ?? "?"}, filed ${s.date_filed ?? "?"})`,
      );
    }
    if (dossier.history.sample_truncated) {
      lines.push(`- …truncated at 25; ${dossier.history.dockets_found} dockets total`);
    }
    lines.push(``);
  }

  if (dossier.vs_you) {
    lines.push(`## Motion patterns against you`, ``);
    if (dossier.vs_you.entries_analyzed > 0) {
      lines.push(`- Entries analyzed: ${dossier.vs_you.entries_analyzed} (locally synced; no API cost)`);
      for (const [key, count] of Object.entries(dossier.vs_you.patterns)) {
        if (count > 0) lines.push(`- ${key}: ${count}`);
      }
    } else {
      lines.push(
        `- No locally synced docket entries for the linked matter(s) — source not connected. This is not evidence of no activity.`,
      );
    }
    lines.push(``);
  }
  lines.push(`## Caveats`, ``);
  for (const caveat of dossier.caveats) lines.push(`- ${caveat}`);
  lines.push(``);
  return lines.join("\n");
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const matterNumber = args.matter ? Number(args.matter) : null;
  if (!args.name && !args["attorney-id"] && !matterNumber) {
    console.error("Provide --matter N, --name \"...\", or --attorney-id N.");
    process.exit(2);
  }

  const token = readCourtListenerToken();
  if (!token) {
    console.error("COURTLISTENER_TOKEN is required for counsel dossiers.");
    process.exit(2);
  }
  const client = createClient({ token });
  let usage = null;
  try {
    usage = await client.getApiUsage();
  } catch (err) {
    console.error(`api-usage lookup failed (${err.message}); refusing without a budget reading.`);
    process.exit(3);
  }
  const budget = budgetAllows(usage);
  console.log(`API budget: ${budget.ok ? "ok" : "EXCEEDED"} (${budget.used ?? "?"} used)`);
  if (!budget.ok) process.exit(4);

  const matters = loadMatters();
  const matter = matterNumber ? matters.find((m) => Number(m.number) === matterNumber) : null;
  if (matterNumber && !matter) {
    console.error(`Matter ${matterNumber} not found.`);
    process.exit(2);
  }

  // --- Resolve counsel identity ---
  let name = args.name ?? null;
  let attorneyIdValue = args["attorney-id"] ? Number(args["attorney-id"]) : null;
  let firm = args.firm ?? null;

  if (attorneyIdValue) {
    const attorney = await client.getAttorney({ attorneyId: attorneyIdValue });
    name = attorney?.name ?? name ?? `attorney-${attorneyIdValue}`;
  } else if (!name && matter && matter.courtlistener?.docket_id) {
    // Auto-discovery runs only when no explicit --name/--attorney-id was given.
    const parties = await client.listParties({ docketId: matter.courtlistener.docket_id });
    const discovery = discoverCounselCandidates(parties, matter.defendants);
    if (discovery.autoPick) {
      name = discovery.autoPick.name;
      attorneyIdValue = discovery.autoPick.attorney_id;
      console.log(`Resolved opposing counsel: ${name} (via "${discovery.autoPick.party}")`);
    } else {
      console.log("Could not auto-resolve opposing counsel. Candidates:");
      for (const c of discovery.candidates.slice(0, 10)) {
        console.log(`  - ${c.name} (party: "${c.party}", score: ${c.score.toFixed(2)})`);
      }
      console.log('Re-run with --attorney-id <id> or --name "...".');
      process.exit(0);
    }
  }

  if (!name) {
    console.error("No counsel name resolved.");
    process.exit(2);
  }

  // --- RECAP docket history ---
  const dockets = await client.searchRecap({ query: `"${name}"`, maxPages: 3 });
  const history = analyzeHistory(dockets);

  // --- Motion patterns against you (local ledger; zero API cost) ---
  let vsYou = null;
  if (matterNumber) {
    const ledger = loadLedger();
    const entries = (ledger.entries ?? []).filter((e) => Number(e.matter) === matterNumber);
    vsYou = { matters: [matterNumber], ...analyzeMotionPatterns(entries) };
  }

  const dossier = {
    version: 2,
    name,
    attorney_id: attorneyIdValue,
    firm,
    linked_matters: matterNumber ? [matterNumber] : [],
    generated_at: new Date().toISOString(),
    source: "courtlistener",
    identity: identityConfidence({ attorney_id: attorneyIdValue, firm }),
    history,
    clients: analyzeClients(history.sample),
    subjects: analyzeSubjects(history.sample),
    vs_you: vsYou,
    caveats: [
      "Name-based RECAP search can conflate attorneys with common names; pin --attorney-id when ambiguous.",
      "History is a docket sample (up to ~60 most recent), not an exhaustive record.",
      "Client and subject signals are keyword heuristics over sampled case names; directional, not adjudicated.",
      "Outcome signals (settlement/dismissal mentions) are directional, not adjudicated results.",
      "Motion patterns cover only matters with locally synced docket entries.",
    ],
  };

  mkdirSync(INTEL_DIR, { recursive: true });
  const slug = slugify(name);
  const jsonPath = path.join(INTEL_DIR, `${slug}.json`);
  const mdPath = path.join(INTEL_DIR, `${slug}.md`);
  writeFileSync(jsonPath, `${JSON.stringify(dossier, null, 2)}\n`, "utf8");
  writeFileSync(mdPath, renderMarkdown(dossier), "utf8");
  console.log(`Dossier written: ${jsonPath}`);
  console.log(`Summary: ${mdPath}`);
  console.log(
    `History: ${history.dockets_found} dockets across ${Object.keys(history.courts).length} courts ` +
      `(${history.date_range.earliest ?? "?"} to ${history.date_range.latest ?? "?"})`,
  );
  const topClient = dossier.clients.top_defendant;
  if (topClient) {
    console.log(`Top client signal: ${topClient.name} (${topClient.count}/${dossier.clients.cases_parsed})`);
  }
  if (dossier.subjects.primary) {
    console.log(`Primary subject: ${dossier.subjects.primary}`);
  }

  // --- Optionally link onto the matter record ---
  if (args.link && matter) {
    const file = path.join(MATTERS_DIR, `${String(matter.number).padStart(2, "0")}.json`);
    const record = JSON.parse(readFileSync(file, "utf8"));
    const existing = Array.isArray(record.opposing_counsel) ? record.opposing_counsel : [];
    const key = slugify(name);
    const entry = { name, dossier: `counsel/${slug}.json` };
    if (attorneyIdValue != null) entry.attorney_id = attorneyIdValue;
    if (firm) entry.firm = firm;
    const next = existing.some((c) => slugify(c.name) === key) ? existing : [...existing, entry];
    record.opposing_counsel = next;
    const issues = validateMatter(record);
    if (issues.length > 0) {
      console.error(`Matter validation failed: ${issues.join("; ")}`);
      process.exit(5);
    }
    writeFileSync(file, `${JSON.stringify(record, null, 2)}\n`, "utf8");
    console.log(`Linked ${name} onto matter ${matter.number}.`);
  }
}

const isMain = process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url);
if (isMain) {
  main().catch((err) => {
    console.error(err?.stack ?? String(err));
    process.exit(1);
  });
}
