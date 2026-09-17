// Normalize CourtListener docket entries into portfolio facts + review candidates.
// Confirmed filings/orders are objective. Deadlines stay candidates until approved.

import { createHash } from "node:crypto";
import { loadDocketRules, matchFirstRule } from "./rules.mjs";

// Family 3 extraction: interpretation strategy lives in
// internal/src/data/rules/docket-interpretation.json. This module only
// renders those rules.
const RULES = loadDocketRules();

const MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

export function formatTimelineDate(isoDate) {
  const match = String(isoDate ?? "").match(/^(\d{4})-(\d{2})-(\d{2})/);
  if (!match) return null;
  const month = MONTHS[Number(match[2]) - 1];
  if (!month) return null;
  return `${month}. ${Number(match[3])}, ${match[1]}`;
}

export function addCalendarDays(isoDate, days) {
  const match = String(isoDate ?? "").match(/^(\d{4})-(\d{2})-(\d{2})/);
  if (!match) return null;
  const next = new Date(Date.UTC(Number(match[1]), Number(match[2]) - 1, Number(match[3]) + Number(days)));
  return `${next.getUTCFullYear()}-${String(next.getUTCMonth() + 1).padStart(2, "0")}-${String(next.getUTCDate()).padStart(2, "0")}`;
}

export function entryHash({
  docketId,
  entryId,
  entryNumber,
  dateFiled,
  description,
}) {
  return createHash("sha256")
    .update(
      [docketId ?? "", entryId ?? "", entryNumber ?? "", dateFiled ?? "", description ?? ""].join("|"),
      "utf8",
    )
    .digest("hex");
}

function firstRecapDocs(raw) {
  if (Array.isArray(raw?.recap_documents)) return raw.recap_documents;
  if (Array.isArray(raw?.recap_document)) return raw.recap_document;
  return [];
}

export function normalizeDocketEntry(raw, { matter, docketId, ingestedAt }) {
  const recapDocs = firstRecapDocs(raw);
  const entryId = raw?.id ?? raw?.docket_entry_id ?? recapDocs[0]?.docket_entry_id ?? null;
  const entryNumber = raw?.entry_number ?? raw?.document_number ?? recapDocs[0]?.entry_number ?? null;
  const dateFiled = raw?.date_filed ?? raw?.entry_date_filed ?? recapDocs[0]?.entry_date_filed ?? null;
  const description = String(
    raw?.description || raw?.short_description || recapDocs[0]?.short_description || recapDocs[0]?.description || "",
  ).trim();
  const documents = recapDocs.map((doc) => ({
    recap_document_id: doc.id ?? null,
    document_number: doc.document_number ?? null,
    is_available: Boolean(doc.is_available),
    filepath_local: doc.filepath_local ?? null,
  }));
  return {
    matter,
    courtlistener_docket_id: docketId,
    courtlistener_entry_id: entryId,
    entry_number: entryNumber == null ? null : Number(entryNumber),
    date_filed: dateFiled,
    description,
    documents,
    ingested_at: ingestedAt,
    hash: entryHash({
      docketId,
      entryId,
      entryNumber,
      dateFiled,
      description,
    }),
  };
}

export function inferFactType(text) {
  return matchFirstRule(RULES.factTypeRules, text)?.factType ?? "filing";
}

export function inferFactActor(text) {
  return matchFirstRule(RULES.factActorRules, text)?.actor ?? "unknown";
}

export function factPrefix(type) {
  if (type === "order") return "ORDER";
  if (type === "hearing") return "SET";
  return "FILED";
}

export function detectDeadlineCandidate(text, dateFiled) {
  const value = String(text ?? "");
  const explicit = RULES.deadlineCandidates.explicitDate;
  const stated = explicit.re.exec(value);
  if (stated) {
    const proposed = toIsoDate(stated[1]);
    if (proposed) {
      return {
        candidate_type: "deadline",
        proposed_date: proposed,
        confidence: explicit.confidence,
        reason: explicit.reasonTemplate.replace("{date}", stated[1]),
      };
    }
  }
  const within = RULES.deadlineCandidates.withinDays;
  const found = within.re.exec(value);
  if (found && within.requiredAny.some((re) => re.test(value))) {
    const days = Number(found[1]);
    const proposed = addCalendarDays(dateFiled, days);
    if (proposed) {
      return {
        candidate_type: "deadline",
        proposed_date: proposed,
        confidence: within.confidence,
        reason: within.reasonTemplate.replace("{days}", String(days)),
      };
    }
  }
  return null;
}

function toIsoDate(value) {
  if (/^\d{4}-\d{2}-\d{2}$/.test(value)) return value;
  const parsed = new Date(String(value).replace(/\./g, ""));
  if (Number.isNaN(parsed.getTime())) return null;
  return `${parsed.getFullYear()}-${String(parsed.getMonth() + 1).padStart(2, "0")}-${String(parsed.getDate()).padStart(2, "0")}`;
}

function clip(text, max = 220) {
  const trimmed = String(text ?? "").replace(/\s+/g, " ").trim();
  if (trimmed.length <= max) return trimmed;
  return `${trimmed.slice(0, max - 1).trimEnd()}…`;
}

export function buildTimelineEvent(normalized, { verifiedAt } = {}) {
  const type = inferFactType(normalized.description);
  const actor = inferFactActor(normalized.description);
  const dkt = normalized.entry_number != null ? `Dkt. ${normalized.entry_number} ` : "";
  const date = formatTimelineDate(normalized.date_filed);
  if (!date) return null;
  const event = {
    date,
    event: `${factPrefix(type)} — ${dkt}${clip(normalized.description) || "docket entry"}`.trim(),
    matters: [normalized.matter],
    type,
    // Family 3 policy (rules/docket-interpretation.json): deadlines from
    // docket text never become live calendar clocks on their own.
    upcoming: RULES.policies.autoUpcomingFromDocket === true,
    filed: true,
    actor,
    source_type: "courtlistener",
    external: {
      provider: "courtlistener",
      docket_id: normalized.courtlistener_docket_id,
    },
  };
  const verified = verifiedAt ?? normalized.ingested_at;
  if (verified) event.verified_at = verified;
  if (normalized.courtlistener_entry_id != null) {
    event.external.docket_entry_id = normalized.courtlistener_entry_id;
  }
  const recapId = normalized.documents?.[0]?.recap_document_id;
  if (recapId != null) event.external.recap_document_id = recapId;
  if (normalized.entry_number != null) event.external.entry_number = normalized.entry_number;
  return event;
}

export function docketNumberFromEventText(eventText) {
  const match = String(eventText ?? "").match(
    /\b(?:Dkt\.|Doc(?:ument)?\.?|ECF(?:\s+No\.?)?)\s*#?\s*(\d+)\b/i,
  );
  return match ? Number(match[1]) : null;
}

export function classifyNormalized(normalized) {
  return {
    fact: buildTimelineEvent(normalized),
    deadline: detectDeadlineCandidate(normalized.description, normalized.date_filed),
  };
}

/** Split-matter events.jsonl row. Never upcoming — clocks.json is the calendar. */
export function splitEventFromNormalized(normalized, fact) {
  if (!fact) return null;
  const iso = String(normalized.date_filed ?? "").slice(0, 10);
  if (!/^\d{4}-\d{2}-\d{2}$/.test(iso)) return null;
  return {
    ts: `${iso}T00:00:00-07:00`,
    date: fact.date,
    matter: normalized.matter,
    matters: [normalized.matter],
    type: fact.type,
    title: fact.event,
    path: null,
    dkt: normalized.entry_number ?? null,
    filed: true,
    actor: fact.actor,
    source_type: "courtlistener",
    upcoming: false,
    external: fact.external,
  };
}

/** Args for `setNextClock`. Review only — never written to clocks.json here. */
export function proposedClockFromDeadline(normalized, deadline) {
  if (!deadline?.proposed_date) return null;
  const dkt = normalized.entry_number;
  const id =
    dkt != null
      ? `${normalized.matter}-deadline-cl-${dkt}`
      : `${normalized.matter}-deadline-cl-${normalized.courtlistener_entry_id ?? "unk"}`;
  return {
    matter: normalized.matter,
    id,
    date: deadline.proposed_date,
    kind: "deadline",
    title: deadline.reason,
    status: "open",
    ...(dkt != null ? { source_dkt: dkt } : {}),
  };
}
