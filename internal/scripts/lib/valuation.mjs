// Proof map + valuation sheet: ties every settlement dollar to evidence.
//
// File: internal/private/negotiation/NN.valuation.json (private, like the
// ledger). Shape: { evidence[], elements[], defenses[], damages[], positions,
// repricing_events[] }. The walk-away stays in the ledger (NN.jsonl) so the
// negotiation guard has one source for it.
//
// Pure functions: validate the file, then compute what the evidence supports.

export const EVIDENCE_STATUS = new Set(["on_record", "in_hand", "requested_not_served", "requested", "produced", "pending"]);
export const PROOF = new Set(["admitted", "documented", "disputed", "unproven"]);
export const THREAT = new Set(["high", "medium", "low"]);
/** Evidence that can carry a trigger or a damages line today. */
const SOLID = new Set(["on_record", "in_hand", "produced"]);

export function validateValuation(v) {
  const errors = [];
  const ids = new Set();
  for (const e of v.evidence ?? []) {
    if (!e.id) errors.push("evidence entry without id");
    if (ids.has(e.id)) errors.push(`duplicate evidence id ${e.id}`);
    ids.add(e.id);
    if (!EVIDENCE_STATUS.has(e.status)) errors.push(`${e.id}: status must be one of ${[...EVIDENCE_STATUS].join(", ")}`);
    if (SOLID.has(e.status) && !e.pin) errors.push(`${e.id}: evidence in the record needs a pin`);
    if (e.status === "on_record" && !e.quote) errors.push(`${e.id}: quote the record, don't characterize it (memo Rule 12)`);
    if (e.sha256 != null && !/^[0-9a-f]{64}$/.test(e.sha256)) errors.push(`${e.id}: sha256 must be 64 hex`);
  }
  const ref = (where, list) => {
    for (const id of list ?? []) if (!ids.has(id)) errors.push(`${where}: unknown evidence '${id}'`);
  };
  for (const el of v.elements ?? []) {
    if (!PROOF.has(el.proof)) errors.push(`element ${el.id}: proof must be one of ${[...PROOF].join(", ")}`);
    ref(`element ${el.id}`, el.evidence);
  }
  const lineIds = new Set((v.damages ?? []).map((d) => d.id));
  for (const d of v.defenses ?? []) {
    if (!THREAT.has(d.threat)) errors.push(`defense ${d.id}: threat must be high|medium|low`);
    ref(`defense ${d.id}`, d.answered_by);
    for (const c of d.cuts ?? []) if (!lineIds.has(c)) errors.push(`defense ${d.id}: cuts unknown line '${c}'`);
  }
  for (const d of v.damages ?? []) {
    if (!(Number.isFinite(d.amount) && d.amount >= 0)) errors.push(`line ${d.id}: amount must be a number`);
    if (!(Number.isFinite(d.p) && d.p >= 0 && d.p <= 1)) errors.push(`line ${d.id}: p must be between 0 and 1`);
    ref(`line ${d.id}`, d.evidence);
  }
  ref("trigger", v.positions?.trigger?.met_by);
  return errors;
}

/**
 * What the evidence supports today.
 * walkaway comes from the ledger (or null).
 */
export function computeValuation(v, { walkaway = null } = {}) {
  const evidence = new Map((v.evidence ?? []).map((e) => [e.id, e]));
  const lines = (v.damages ?? []).map((d) => {
    const solid = (d.evidence ?? []).filter((id) => SOLID.has(evidence.get(id)?.status));
    const threats = (v.defenses ?? []).filter((x) => (x.cuts ?? []).includes(d.id)).map((x) => `${x.id} (${x.threat})`);
    return { ...d, expected: Math.round(d.amount * d.p), solid_evidence: solid, unsupported: solid.length === 0, threats };
  });
  const gross = lines.reduce((s, l) => s + l.amount, 0);
  const expected = lines.reduce((s, l) => s + l.expected, 0);

  const trigger = v.positions?.trigger ?? null;
  const triggerMet = Boolean(trigger?.met_by?.length) && trigger.met_by.every((id) => SOLID.has(evidence.get(id)?.status));
  const bracket = triggerMet ? v.positions?.bracket?.after_trigger : v.positions?.bracket?.early;
  const opening = v.positions?.opening ?? null;

  const findings = [];
  for (const l of lines) if (l.unsupported) findings.push({ level: "warn", text: `${l.id}: $${n(l.amount)} has no evidence in the record yet. Build it or expect it to be discounted to near zero.` });
  if (opening != null && opening < gross) findings.push({ level: "warn", text: `Opening $${n(opening)} is below the gross of the lines ($${n(gross)}).` });
  if (walkaway == null) findings.push({ level: "block", text: "No walk-away in the ledger. The negotiation guard will refuse every number." });
  else if (walkaway > expected) findings.push({ level: "warn", text: `Walk-away $${n(walkaway)} is above the evidence-weighted value $${n(expected)}: either the probabilities are too low or the walk-away is not reachable yet.` });
  if (bracket && expected < bracket[0]) findings.push({ level: "info", text: `Evidence-weighted value $${n(expected)} is below the ${triggerMet ? "after-trigger" : "early"} bracket floor $${n(bracket[0])}. The bracket assumes their defenses get answered; the open questions under THEIR DEFENSES are what close that gap.` });
  if (bracket && expected > bracket[1]) findings.push({ level: "info", text: `Evidence-weighted value $${n(expected)} is above the bracket ceiling $${n(bracket[1])}: the bracket may be stale.` });

  const letterSafe = (v.evidence ?? []).filter((e) => SOLID.has(e.status) && !e.reserve && !e.do_not_cite_in_letter).map((e) => e.id);
  const reserve = (v.evidence ?? []).filter((e) => e.reserve).map((e) => e.id);
  const doNotCite = (v.evidence ?? []).filter((e) => e.do_not_cite_in_letter).map((e) => e.id);
  const restricted = (v.evidence ?? []).filter((e) => e.use_restriction).map((e) => ({ id: e.id, restriction: e.use_restriction }));
  const pending = (v.evidence ?? []).filter((e) => !SOLID.has(e.status)).map((e) => ({ id: e.id, status: e.status, why: e.why }));

  return { lines, gross, expected, triggerMet, bracket, opening, walkaway, findings, letterSafe, reserve, doNotCite, restricted, pending };
}

export function n(x) {
  return Number(x).toLocaleString("en-US", { maximumFractionDigits: 0 });
}

/** Phone-readable sheet. */
export function formatValuation(v, c) {
  const out = [];
  out.push(`MATTER ${v.matter} VALUATION — as of ${v.as_of}`, v.caption, "");
  out.push("WHAT IS PROVEN");
  for (const el of v.elements ?? []) out.push(`  [${el.proof.toUpperCase()}] ${el.element}${el.evidence?.length ? ` ← ${el.evidence.join(", ")}` : ""}`);
  out.push("", "DAMAGES (amount × your probability = evidence-weighted)");
  for (const l of c.lines)
    out.push(`  ${l.label}: $${n(l.amount)} × ${l.p} = $${n(l.expected)}${l.unsupported ? "  ⚠ no evidence yet" : ""}${l.threats.length ? `  — cut by ${l.threats.join(", ")}` : ""}`);
  out.push(`  Gross $${n(c.gross)} · evidence-weighted $${n(c.expected)}`);
  out.push("", "POSITIONS");
  if (c.opening != null) out.push(`  Opening $${n(c.opening)}${v.positions?.opening_basis ? ` (${v.positions.opening_basis})` : ""}`);
  if (c.bracket) out.push(`  Settlement bracket now: $${n(c.bracket[0])}–$${n(c.bracket[1])} (${c.triggerMet ? "trigger MET" : "pre-trigger"})`);
  if (v.positions?.trigger) out.push(`  Trigger: ${v.positions.trigger.label} — ${c.triggerMet ? `met by ${v.positions.trigger.met_by.join(", ")}` : "not yet"}${v.positions.trigger.note ? `\n    ${v.positions.trigger.note}` : ""}`);
  out.push(`  Walk-away: ${c.walkaway != null ? `$${n(c.walkaway)} (private, from ledger)` : "NOT SET"}`);
  out.push("", "THEIR DEFENSES");
  for (const d of v.defenses ?? []) {
    out.push(`  [${d.threat}] ${d.name}${d.answered_by?.length ? ` — answered by ${d.answered_by.join(", ")}` : " — no answer in hand"}`);
    for (const q of d.open_questions ?? []) out.push(`      ? ${q}`);
  }
  out.push("", "USE OF EVIDENCE");
  out.push(`  Cite in a letter: ${c.letterSafe.join(", ") || "—"}`);
  out.push(`  Hold in reserve: ${c.reserve.join(", ") || "—"}`);
  out.push(`  Never cite in a letter: ${c.doNotCite.join(", ") || "—"}`);
  if (c.restricted.length) for (const r of c.restricted) out.push(`  RESTRICTED ${r.id}: ${r.restriction}`);
  if (c.pending.length) out.push(`  Still coming: ${c.pending.map((p) => `${p.id} (${p.status})`).join(", ")}`);
  out.push("", "WHAT MOVES THE NUMBER");
  for (const e of v.repricing_events ?? []) out.push(`  • ${e.event}\n      + ${e.if_favorable}\n      − ${e.if_unfavorable}`);
  if (c.findings.length) {
    out.push("", "CHECKS");
    for (const f of c.findings) out.push(`  ${f.level === "block" ? "✗" : f.level === "warn" ? "!" : "·"} ${f.text}`);
  }
  return out.join("\n");
}
