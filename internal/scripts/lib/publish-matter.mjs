// Single publish projection: full matter graph → filing-safe public shape.
//
// SPA summaries / lazy matter records and the D1 seed MUST both call this.
// Do not maintain a second allowlist. Laptop loaders (loadMatters, npm run q,
// npm run mcp) keep the assembled graph and never go through here.
//
// Fail closed: only listed identity fields, public-filing docket rows,
// court-facing clocks, filed/phone-tap PDFs, and pleading-caption people.

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { assembleSplitMatter, loadSplitParts, paddedMatterNumber } from "./matter-layout.mjs";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
export const REPO_ROOT = path.resolve(__dirname, "../../..");

/** Court-set appearance kinds. Other clocks need a docket number to ship. */
export const COURT_FACING_KINDS = new Set([
  "hearing",
  "cmc",
  "conference",
  "trial",
  "oral_argument",
  "osc",
]);

const COURT_TITLE_RE =
  /\b(hearing|case management conference|\bcmc\b|status conference|pretrial scheduling|trial|oral argument|order to show cause|\bosc\b)\b/i;
const DEMAND_OR_MONEY_RE = /\$[\d,.]+|\bfinal demand\b|\bdemand expir|\bsettlement posture\b/i;

/** Keys that must never appear on a published matter object (any depth except clock.status). */
export const PUBLISH_DENIED_KEYS = new Set([
  "key_facts",
  "procedural_status",
  "damages",
  "risk",
  "evidence",
  "policy_limits",
  "dossier",
  "email",
  "card",
  "settlement_note",
  "prose",
  "serviceTracking",
  "same_incident",
]);

/** Root-only denials — `status` is the long narrative; clock.status is public. */
export const PUBLISH_DENIED_ROOT_KEYS = new Set(["status", "note", "events"]);

const IDENTITY_KEYS = [
  "number",
  "caption",
  "case_no",
  "court",
  "judge",
  "lifecycle",
  "proceeding",
  "phase",
  "cluster",
  "status_label",
  "type",
  "filed",
  "archived",
  "badge",
  "defendants",
  "claims",
  "causes",
  "related",
  "last_updated",
];

const PERSONAL_EMAIL_RE =
  /[A-Za-z0-9._%+-]+@(?:gmail|yahoo|hotmail|icloud|outlook|me|proton\.me|protonmail)\.[A-Za-z]{2,}/gi;
const US_PHONE_RE =
  /(?<!\d)(?:\+1[-.\s]*)?(?:\(?\d{3}\)?[-.\s]*)\d{3}[-.\s]*\d{4}(?!\d)/g;

const isObj = (v) => v !== null && typeof v === "object" && !Array.isArray(v);
const asArray = (v) => (Array.isArray(v) ? v : []);

export function labelFromPublicPath(docPath) {
  const base = String(docPath).split("/").pop() ?? String(docPath);
  return base.replace(/\.pdf$/i, "").replace(/\.docx$/i, "").trim() || base;
}

export function sanitizePublicText(value) {
  if (typeof value !== "string") return value;
  return value
    .replace(PERSONAL_EMAIL_RE, "[redacted]")
    .replace(US_PHONE_RE, "[redacted]");
}

export function isPdfPath(docPath) {
  return typeof docPath === "string" && /\.pdf$/i.test(docPath);
}

export function isCourtFacingClock(clock) {
  if (!clock || typeof clock !== "object") return false;
  if (!clock.date) return false;
  const kind = String(clock.kind ?? "").toLowerCase();
  if (COURT_FACING_KINDS.has(kind)) return true;
  const dkt = clock.source_dkt;
  if (dkt != null && Number(dkt) > 0) return true;
  const title = String(clock.title ?? "");
  if (DEMAND_OR_MONEY_RE.test(title)) return false;
  if (COURT_TITLE_RE.test(title)) return true;
  if (clock.actor === "opposing" && /\b(response|answer|plead)\b/i.test(title)) return true;
  return false;
}

export function isPublicDocketRow(row) {
  return (
    isObj(row) &&
    row.filed === true &&
    isPdfPath(row.path) &&
    typeof row.title === "string" &&
    row.title.trim()
  );
}

export function isPublicDocument(doc, ctx = {}) {
  if (!isObj(doc) || !isPdfPath(doc.path)) return false;
  if (ctx.phoneTapPaths instanceof Set && ctx.phoneTapPaths.has(doc.path)) return true;
  if (ctx.filedDocketPaths instanceof Set && ctx.filedDocketPaths.has(doc.path)) return true;
  return doc.filed === true;
}

export function loadPhoneTapPaths(repoRoot = REPO_ROOT) {
  const filePath = path.join(repoRoot, "internal/public/short-links.json");
  const paths = new Set();
  if (!fs.existsSync(filePath)) return paths;
  const json = JSON.parse(fs.readFileSync(filePath, "utf8"));
  for (const link of json.links ?? []) {
    if (typeof link.source === "string" && link.source) paths.add(link.source);
    if (typeof link.slug === "string" && link.slug) paths.add(`/${link.slug}.pdf`);
  }
  return paths;
}

function publishStatusLabel(label) {
  if (typeof label !== "string" || !label.trim()) return undefined;
  const cleaned = sanitizePublicText(label.trim());
  if (DEMAND_OR_MONEY_RE.test(cleaned)) return undefined;
  return cleaned;
}

function pickIdentity(matter) {
  const out = {};
  for (const key of IDENTITY_KEYS) {
    if (key === "status_label") {
      const label = publishStatusLabel(matter.status_label);
      if (label) out.status_label = label;
      continue;
    }
    if (matter[key] !== undefined) out[key] = sanitizePublicDeep(matter[key]);
  }
  if (isObj(matter.courtlistener)) {
    const cl = {};
    if (typeof matter.courtlistener.court_id === "string") cl.court_id = matter.courtlistener.court_id;
    if (typeof matter.courtlistener.docket_id === "number") cl.docket_id = matter.courtlistener.docket_id;
    if (typeof matter.courtlistener.docket_url === "string") cl.docket_url = matter.courtlistener.docket_url;
    if (Object.keys(cl).length) out.courtlistener = cl;
  }
  if (!Array.isArray(out.causes)) out.causes = [];
  if (typeof out.defendants !== "string") out.defendants = "";
  if (typeof out.claims !== "string") out.claims = "";
  return out;
}

function publishDocket(docket) {
  return asArray(docket)
    .filter(isPublicDocketRow)
    .map((row) => {
      const out = {
        dkt: row.dkt ?? null,
        filed: true,
        title: sanitizePublicText(row.title.trim()),
        path: row.path,
      };
      if (typeof row.date === "string" && row.date.trim()) out.date = row.date.trim();
      return out;
    });
}

function publishClocks(clocks) {
  return asArray(clocks)
    .filter(isCourtFacingClock)
    .map((clock) => {
      const out = {
        date: clock.date,
        kind: clock.kind ?? "deadline",
        status: clock.status ?? "open",
        title: sanitizePublicText(String(clock.title ?? "").trim()),
      };
      if (typeof clock.actor === "string" && clock.actor.trim()) out.actor = clock.actor.trim();
      return out;
    });
}

function publishDocuments(documents, ctx) {
  const seen = new Set();
  const out = [];
  for (const doc of asArray(documents)) {
    if (!isPublicDocument(doc, ctx) || seen.has(doc.path)) continue;
    seen.add(doc.path);
    out.push({ path: doc.path, filed: true });
  }
  return out;
}

function publishPeople(counsel, matter) {
  const people = [];
  const seen = new Set();
  for (const row of asArray(counsel?.appearances)) {
    if (!isObj(row) || typeof row.name !== "string" || !row.name.trim()) continue;
    const name = row.name.trim();
    const key = name.toLowerCase();
    if (seen.has(key)) continue;
    seen.add(key);
    const person = { name, kind: "counsel" };
    if (typeof row.firm === "string" && row.firm.trim()) person.firm = sanitizePublicText(row.firm.trim());
    if (typeof row.role === "string" && row.role.trim()) person.role = row.role.trim();
    if (row.attorney_id != null) person.attorney_id = row.attorney_id;
    if (typeof row.bar === "string" && row.bar.trim()) person.bar = row.bar.trim();
    people.push(person);
  }
  if (typeof matter?.judge === "string" && matter.judge.trim()) {
    const name = matter.judge.trim();
    if (!seen.has(name.toLowerCase())) {
      people.push({ name, kind: "judge" });
    }
  }
  return people;
}

function sanitizePublicDeep(value) {
  if (typeof value === "string") return sanitizePublicText(value);
  if (Array.isArray(value)) return value.map(sanitizePublicDeep);
  if (isObj(value)) {
    const out = {};
    for (const [k, v] of Object.entries(value)) out[k] = sanitizePublicDeep(v);
    return out;
  }
  return value;
}

/**
 * Map a full matter (assembled identity + sibling tables) to the public shape.
 *
 * @param {{
 *   matter: object,
 *   docket?: object[],
 *   clocks?: object[] | { clocks?: object[] },
 *   documents?: object[],
 *   counsel?: object,
 *   parties?: object,
 *   phoneTapPaths?: Set<string>|string[],
 * }} input
 */
export function publishMatter(input) {
  const matter = isObj(input?.matter) ? input.matter : {};
  const docket = asArray(input?.docket);
  const rawClocks = input?.clocks;
  const clocks = Array.isArray(rawClocks) ? rawClocks : asArray(rawClocks?.clocks);
  const documents = asArray(input?.documents);
  const counsel = isObj(input?.counsel) ? input.counsel : {};
  const parties = isObj(input?.parties) ? input.parties : {};
  const phoneTapPaths = input?.phoneTapPaths instanceof Set
    ? input.phoneTapPaths
    : new Set(asArray(input?.phoneTapPaths));

  const identity = pickIdentity({
    ...matter,
    defendants: parties.defendants_label ?? matter.defendants ?? "",
  });

  const publishedDocket = publishDocket(docket);
  const filedDocketPaths = new Set(publishedDocket.map((row) => row.path));
  const publishedDocuments = publishDocuments(documents.length ? documents : docket, {
    phoneTapPaths,
    filedDocketPaths,
  });

  return {
    ...identity,
    docket: publishedDocket,
    clocks: publishClocks(clocks),
    documents: publishedDocuments,
    people: publishPeople(counsel, identity),
  };
}

export function publishMatterFromDir(dir, opts = {}) {
  const parts = loadSplitParts(dir);
  const assembled = assembleSplitMatter(parts);
  return publishMatter({
    matter: assembled,
    docket: parts.docket,
    clocks: parts.clocks,
    documents: parts.documents,
    counsel: parts.counsel,
    parties: parts.parties,
    phoneTapPaths: opts.phoneTapPaths,
  });
}

export function publishDir(mattersDir, number) {
  return path.join(mattersDir, "publish", `${paddedMatterNumber(number)}.json`);
}

/** Walk a published object and return denylisted key paths. */
export function collectDeniedKeyPaths(value, trail = "") {
  const hits = [];
  if (Array.isArray(value)) {
    value.forEach((item, i) => hits.push(...collectDeniedKeyPaths(item, `${trail}[${i}]`)));
    return hits;
  }
  if (!isObj(value)) return hits;
  for (const [key, child] of Object.entries(value)) {
    const here = trail ? `${trail}.${key}` : key;
    if (PUBLISH_DENIED_KEYS.has(key)) hits.push(here);
    if (!trail && PUBLISH_DENIED_ROOT_KEYS.has(key)) hits.push(here);
    hits.push(...collectDeniedKeyPaths(child, here));
  }
  return hits;
}

const LEAK_VALUE_RES = [
  { id: "personal_gmail", re: /bnn\.cdl@gmail\.com/i },
  { id: "plaintiff_phone", re: /\(209\)\s*801-4442/ },
  { id: "housing_status", re: /homeless since july 2/i },
  { id: "infomart_id", re: /\binfomart\b/i },
  { id: "settlement_note_field", re: /"settlement_note"/ },
  { id: "key_facts_field", re: /"key_facts"/ },
  { id: "pilot_settlement_figure", re: /\$35,000/ },
  { id: "final_demand", re: /final demand/i },
];

function distinctiveSnippet(text) {
  if (typeof text !== "string") return null;
  const cleaned = text.replace(/\s+/g, " ").trim();
  if (cleaned.length < 90) return null;
  const slice = cleaned.slice(48, 128).trim();
  return slice.length >= 40 ? slice : null;
}

function leakMarkersFromMatter(matter) {
  const markers = [];
  for (const field of ["key_facts", "procedural_status", "damages", "risk"]) {
    const snippet = distinctiveSnippet(matter?.[field]);
    if (snippet) markers.push({ id: `${field}_snippet`, snippet });
  }
  return markers;
}

function scanText(label, text) {
  const issues = [];
  const hay = String(text ?? "");
  for (const { id, re } of LEAK_VALUE_RES) {
    if (re.test(hay)) issues.push(`${label}: denylisted value (${id})`);
  }
  return issues;
}

/**
 * Validate one published object (and optional seed SQL / artifact text).
 * Returns human-readable issues (empty = clean).
 */
export function collectPublishStripIssues({
  published,
  sourceMatter,
  artifactText,
  artifactLabel = "publish artifact",
} = {}) {
  const issues = [];
  if (published != null) {
    for (const keyPath of collectDeniedKeyPaths(published)) {
      issues.push(`published matter ${published.number ?? "?"}: denied key ${keyPath}`);
    }
    const json = JSON.stringify(published);
    issues.push(...scanText(`published matter ${published.number ?? "?"}`, json));
    if (sourceMatter) {
      for (const { id, snippet } of leakMarkersFromMatter(sourceMatter)) {
        if (json.includes(snippet)) {
          issues.push(`published matter ${published.number ?? "?"}: leaked ${id}`);
        }
      }
    }
  }
  if (artifactText != null) {
    issues.push(...scanText(artifactLabel, artifactText));
    if (/"key_facts"/.test(artifactText)) {
      issues.push(`${artifactLabel}: contains key_facts field`);
    }
  }
  return issues;
}
