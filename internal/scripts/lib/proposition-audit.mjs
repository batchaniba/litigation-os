// Private reasoning ledger. Never imported by the SPA or public Worker.
const STATES = new Set(["allegation", "user_report", "inference", "supported", "disputed", "judicial_finding"]);
const ROLES = new Set(["supports", "opposes", "context"]);
const TYPES = new Set(["record", "authority"]);
const text = (v) => typeof v === "string" && v.trim().length > 0;
const object = (v) => v !== null && typeof v === "object" && !Array.isArray(v);
const date = (v) => text(v) && /^\d{4}-\d{2}-\d{2}$/.test(v) &&
  !Number.isNaN(Date.parse(v + "T00:00:00Z")) &&
  new Date(v + "T00:00:00Z").toISOString().slice(0, 10) === v;

export function auditPropositions({ propositions } = {}) {
  if (!Array.isArray(propositions)) throw new Error("propositions must be an array");
  const ids = new Set();
  const results = propositions.map((p) => {
    if (!object(p) || !text(p.id) || !text(p.statement) || !STATES.has(p.factual_status))
      throw new Error("each proposition needs id, statement and a valid factual_status");
    if (ids.has(p.id)) throw new Error("duplicate proposition id: " + p.id);
    ids.add(p.id);
    if (!Array.isArray(p.sources) || !Array.isArray(p.proof_gaps) || !Array.isArray(p.objections))
      throw new Error(p.id + ": sources, proof_gaps and objections must be arrays");
    if (!p.proof_gaps.every(text)) throw new Error(p.id + ": proof_gaps must contain nonempty strings");
    const issues = [];
    const add = (code, source = null) => issues.push({ code, source });
    for (const s of p.sources) {
      if (!object(s) || !text(s.id) || !TYPES.has(s.type) || !ROLES.has(s.role) ||
          !text(s.locator) || !text(s.pinpoint) || !text(s.quote))
        throw new Error(p.id + ": each source needs id, type, role, locator, pinpoint and quote");
      if (p.sources.filter((other) => other.id === s.id).length !== 1)
        throw new Error(p.id + ": duplicate source id: " + s.id);
      if (s.retrieved_at !== undefined && !date(s.retrieved_at))
        throw new Error(p.id + ": invalid retrieved_at");
      if (!object(s.review)) {
        add("source_not_reviewed", s.id);
        continue;
      }
      if (!text(s.review.reviewer) || !date(s.review.reviewed_at) || !text(s.review.reason))
        throw new Error(p.id + ": source review needs reviewer, reviewed_at and reason");
      if (!["supports", "opposes", "context", "unclear"].includes(s.review.relationship))
        throw new Error(p.id + ": invalid reviewed relationship");
      if (s.review.relationship === "unclear") add("relationship_unresolved", s.id);
      else if (s.review.relationship !== s.role) add("relationship_mismatch", s.id);
      if (s.type === "authority") {
        for (const field of ["proposition_fit", "jurisdiction_fit", "posture_fit", "treatment_checked"]) {
          if (s.review[field] !== true) add("authority_" + field + "_unconfirmed", s.id);
        }
      } else if (s.review.foundation_checked !== true) {
        add("record_foundation_unconfirmed", s.id);
      }
    }
    if (!p.sources.some((s) => s.type === "record" && s.role === "supports"))
      add("no_supporting_record");
    if (!p.sources.some((s) => s.type === "authority" && s.role === "supports"))
      add("no_supporting_authority");
    if (p.proof_gaps.length) add("open_proof_gaps");
    for (const o of p.objections) {
      if (!object(o) || !text(o.statement) || !Array.isArray(o.response_source_ids))
        throw new Error(p.id + ": objections need statement and response_source_ids");
      if (!o.response_source_ids.every((id) => p.sources.some((s) => s.id === id)))
        throw new Error(p.id + ": objection references an unknown source");
      if (!text(o.response) || !o.response_source_ids.length) add("unanswered_objection");
    }
    if (p.sources.some((s) => s.role === "opposes")) add("adverse_source_present");
    if (p.factual_status === "inference" && !text(p.inference_reason))
      add("inference_not_explained");
    if (p.factual_status === "judicial_finding" &&
        !p.sources.some((s) => s.type === "record" && s.role === "supports" && s.review?.judicial_finding === true))
      add("judicial_finding_unconfirmed");
    return { ...p, issues, review_status: issues.length ? "needs_review" : "checks_complete" };
  });
  return {
    propositions: results,
    summary: {
      total: results.length,
      needs_review: results.filter((p) => p.issues.length).length,
      checks_complete: results.filter((p) => !p.issues.length).length,
    },
    limitation: "Checks measure recorded review completeness. They do not verify quotations, decide admissibility, or establish legal correctness.",
  };
}
