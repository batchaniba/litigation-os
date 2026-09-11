// Normalize CourtListener docket entries into portfolio facts + review candidates.
// Confirmed filings/orders are objective. Deadlines stay candidates until approved.

import { createHash } from "node:crypto";

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

const BODY_MAX = 80_000;

function firstPlainText(value) {
  if (typeof value !== "string") return "";
  return value.trim();
}

/** Capture RECAP / OCR text so the intelligence OS can extract arguments without a catalog edit. */
export function recapPlainText(raw, recapDocs = firstRecapDocs(raw)) {
  const candidates = [
    raw?.plain_text,
    raw?.ocr_text,
    ...recapDocs.flatMap((doc) => [doc.plain_text, doc.ocr_text, doc.plain_text_short]),
  ];
  for (const candidate of candidates) {
    const text = firstPlainText(candidate);
    if (text) return text.length > BODY_MAX ? text.slice(0, BODY_MAX) : text;
  }
  return "";
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
  const body = recapPlainText(raw, recapDocs);
  return {
    matter,
    courtlistener_docket_id: docketId,
    courtlistener_entry_id: entryId,
    entry_number: entryNumber == null ? null : Number(entryNumber),
    date_filed: dateFiled,
    description,
    body,
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
  const value = String(text ?? "");
  if (/\b(?:minute\s+order|order|opinion|findings?\s+and\s+recommendations?)\b/i.test(value)) {
    return "order";
  }
  if (/\b(?:hearing|conference|calendar)\b/i.test(value)) return "hearing";
  return "filing";
}

export function inferFactActor(text) {
  const value = String(text ?? "");
  if (/\b(?:order|clerk|court|magistrate|judge)\b/i.test(value) && !/\bmotion\b/i.test(value)) {
    return "court";
  }
  if (/\b(?:defendant|respondent|opposing)\b/i.test(value)) return "opposing";
  if (/\bplaintiff\b/i.test(value)) return "you";
  if (/\bmotion\s+to\s+dismiss\b/i.test(value)) return "opposing";
  return "unknown";
}

export function factPrefix(type) {
  if (type === "order") return "ORDER";
  if (type === "hearing") return "SET";
  return "FILED";
}

const EXPLICIT_DATE_RE =
  /\b(?:due|deadline|on or before|no later than)\s+(?:on\s+|by\s+)?(\d{4}-\d{2}-\d{2}|[A-Z][a-z]{2,8}\.?\s+\d{1,2},\s+\d{4})/i;
const WITHIN_DAYS_RE = /\bwithin\s+(\d+)\s+days?\b/i;
const SHALL_FILE_RE = /\bshall\s+(?:file|serve|respond|amend|submit)\b/i;

function toIsoDate(value) {
  if (/^\d{4}-\d{2}-\d{2}$/.test(value)) return value;
  const parsed = new Date(String(value).replace(/\./g, ""));
  if (Number.isNaN(parsed.getTime())) return null;
  return `${parsed.getFullYear()}-${String(parsed.getMonth() + 1).padStart(2, "0")}-${String(parsed.getDate()).padStart(2, "0")}`;
}

export function detectDeadlineCandidate(text, dateFiled) {
  const value = String(text ?? "");
  const explicit = value.match(EXPLICIT_DATE_RE);
  if (explicit) {
    const proposed = toIsoDate(explicit[1]);
    if (proposed) {
      return {
        candidate_type: "deadline",
        proposed_date: proposed,
        confidence: 0.9,
        reason: `Entry states a due date of ${explicit[1]}.`,
      };
    }
  }
  const within = value.match(WITHIN_DAYS_RE);
  if (within && (SHALL_FILE_RE.test(value) || /\b(?:due|deadline|must|amended complaint)\b/i.test(value))) {
    const days = Number(within[1]);
    const proposed = addCalendarDays(dateFiled, days);
    if (proposed) {
      return {
        candidate_type: "deadline",
        proposed_date: proposed,
        confidence: 0.7,
        reason: `Order or entry states an obligation within ${days} days.`,
      };
    }
  }
  return null;
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
    upcoming: false,
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
