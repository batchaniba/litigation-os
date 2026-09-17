// Assemble a split matter folder into the legacy Matter shape the SPA,
// validator, and summaries still consume. Agents should fetch the sibling
// files directly; this projection exists so the dashboard does not fork.
//
// Limits live here as data because they are fetch/UI budgets, not style.
// Assessment: keep a cap on the *first* file an agent opens. Do not cap the
// case. docket.json / events.jsonl / claims / damages / evidence grow. An
// overdue clock is a fact. Do not add output-length caps on agent work.

const isObj = (v) => v !== null && typeof v === "object" && !Array.isArray(v);

export const SPLIT_JSON_FILES = [
  "matter.json",
  "docket.json",
  "clocks.json",
  "parties.json",
  "counsel.json",
  "claims.json",
  "damages.json",
  "evidence.json",
];

export const SPLIT_OPTIONAL_JSON = ["prose.json"];

export const EVENTS_FILE = "events.jsonl";

/**
 * Portfolio-wide limit policy. Cap the first fetch, not the case.
 *
 * Keep: identity file size (one tool call), status_label width (UI chip),
 * word ceilings on unsplit NN.json diaries, a short index next_clock title
 * when the source is a timeline blob.
 * Drop: line/word ceilings on docket, events, clocks, claims, damages,
 * evidence; schema failure for overdue clocks; agent output-length caps.
 */
export const GRAPH_LIMITS = Object.freeze({
  identity: Object.freeze({ lines: 80, bytes: 8 * 1024 }),
  statusLabelChars: 60,
  /** Legacy timeline blobs copied into index/matters.json. Split clocks.json titles are not sliced. */
  indexNextClockTitleChars: 240,
  /** Splitter only: long key_facts stay in prose.json. Not a validator ceiling. */
  identityKeyFactsChars: 800,
  docketLineCeiling: null,
  eventsLineCeiling: null,
  splitProseWordCeilings: false,
  legacyProseWordCeilings: true,
  overdueFailsSchema: false,
  agentOutputCaps: false,
});

/** Identity-file fetch budget. Not a prose style ceiling. */
export const MATTER_JSON_BUDGET = GRAPH_LIMITS.identity;

export function paddedMatterNumber(number) {
  return String(number).padStart(2, "0");
}

function asArray(v) {
  return Array.isArray(v) ? v : [];
}

function docketToDocuments(docket) {
  return asArray(docket)
    .map((row) => {
      if (!isObj(row) || typeof row.path !== "string") return null;
      const ref = { path: row.path };
      if (typeof row.filed === "boolean") ref.filed = row.filed;
      if (typeof row.label === "string" && row.label.trim()) ref.label = row.label.trim();
      return ref;
    })
    .filter(Boolean);
}

function evidenceToStrings(evidence) {
  return asArray(evidence)
    .map((row) => {
      if (typeof row === "string") return row;
      if (!isObj(row)) return null;
      return row.label || row.what_it_proves || row.id || null;
    })
    .filter(Boolean);
}

function claimsToCauses(claims) {
  const counts = asArray(claims?.counts);
  return counts.map((c) => c.title).filter((t) => typeof t === "string" && t.trim());
}

function claimsToString(claims, fallback) {
  if (typeof fallback === "string" && fallback.trim()) return fallback;
  const causes = claimsToCauses(claims);
  return causes.join("; ");
}

function damagesToString(damages, fallback) {
  if (typeof damages === "string") return damages;
  if (isObj(damages) && typeof damages.narrative === "string") return damages.narrative;
  return typeof fallback === "string" ? fallback : "";
}

function riskToString(damages, matter, fallback) {
  if (typeof matter?.risk === "string" && matter.risk.trim()) return matter.risk;
  if (isObj(damages) && typeof damages.risk === "string") return damages.risk;
  return typeof fallback === "string" ? fallback : "";
}

/**
 * @param {{
 *   matter: object,
 *   docket?: object[],
 *   clocks?: object[],
 *   parties?: object,
 *   counsel?: object,
 *   claims?: object,
 *   damages?: object|string,
 *   evidence?: object[]|string[],
 *   prose?: object,
 * }} parts
 */
export function assembleSplitMatter(parts) {
  const matter = isObj(parts.matter) ? parts.matter : {};
  const docket = asArray(parts.docket);
  const evidence = parts.evidence;
  const claims = parts.claims;
  const damages = parts.damages;
  const parties = isObj(parts.parties) ? parts.parties : {};
  const counsel = isObj(parts.counsel) ? parts.counsel : {};

  const documents = docketToDocuments(docket);
  const evidenceStrings = evidenceToStrings(evidence);
  const causes = claimsToCauses(claims);
  const appearances = asArray(counsel.appearances);

  // prose.json is opt-in. Never fold it into the first fetch / SPA projection.
  const assembled = {
    ...matter,
    claims: claimsToString(claims, matter.claims),
    causes: causes.length ? causes : asArray(matter.causes),
    key_facts: matter.key_facts ?? "",
    procedural_status: matter.procedural_status ?? "",
    damages: damagesToString(damages, matter.damages ?? ""),
    risk: riskToString(damages, matter, ""),
    evidence: evidenceStrings.length ? evidenceStrings : asArray(matter.evidence),
    documents: documents.length ? documents : asArray(matter.documents),
    defendants: parties.defendants_label ?? matter.defendants ?? "",
    __layout: "split",
  };

  if (Array.isArray(parties.serviceTracking) || Array.isArray(matter.serviceTracking)) {
    assembled.serviceTracking = parties.serviceTracking ?? matter.serviceTracking;
  }
  if (appearances.length) {
    assembled.opposing_counsel = appearances.map((row) => {
      const out = { name: row.name };
      if (row.attorney_id != null) out.attorney_id = row.attorney_id;
      if (row.firm) out.firm = row.firm;
      if (row.dossier) out.dossier = row.dossier;
      if (row.id) out.counsel_id = row.id;
      return out;
    });
  }
  return assembled;
}

export function inferDocketNumber(path, title = "") {
  const hay = `${path} ${title}`;
  const match = hay.match(/\b(?:Dkt|Doc(?:ument)?)\.?\s*(\d+)\b/i);
  if (!match) return null;
  const n = Number(match[1]);
  return Number.isInteger(n) && n > 0 ? n : null;
}
