// Merge normalized CourtListener entries into timeline.json + review.json.
// Idempotent: entry ID / hash / Dkt. N never create a second copy.
// Deadlines never become upcoming: true here.

import { matterRefsInclude } from "../../src/utils/matterRefs.js";
import { classifyNormalized, docketNumberFromEventText } from "./entries.mjs";

function cleanExternal(external) {
  const out = {};
  for (const [key, value] of Object.entries(external)) {
    if (value !== undefined && value !== null) out[key] = value;
  }
  return out;
}

function attachProvenance(event, fact) {
  const next = { ...event };
  if (!next.source_type) next.source_type = "courtlistener";
  if (fact.verified_at && !next.verified_at) next.verified_at = fact.verified_at;
  next.external = cleanExternal({
    ...(typeof next.external === "object" && next.external ? next.external : {}),
    ...fact.external,
  });
  return next;
}

export function findMatchingTimelineEvent(timeline, { matter, entryId, entryNumber }) {
  for (let index = 0; index < timeline.length; index += 1) {
    const event = timeline[index];
    if (!matterRefsInclude(event.matters, matter)) continue;
    const externalId = event.external?.docket_entry_id;
    if (entryId != null && externalId != null && Number(externalId) === Number(entryId)) {
      return { index, event, via: "entry_id" };
    }
    if (entryNumber != null && docketNumberFromEventText(event.event) === Number(entryNumber)) {
      return { index, event, via: "dkt_text" };
    }
  }
  return null;
}

export function ledgerHas(ledger, normalized) {
  const entries = ledger.entries ?? [];
  return entries.some((row) => {
    if (normalized.courtlistener_entry_id != null && row.courtlistener_entry_id === normalized.courtlistener_entry_id) {
      return true;
    }
    return row.hash === normalized.hash;
  });
}

function emptyLedger() {
  return { version: 1, entries: [] };
}

function emptyReview() {
  return { version: 1, candidates: [] };
}

export function reconcileEntries({
  timeline,
  ledger = emptyLedger(),
  review = emptyReview(),
  normalizedEntries,
  applyFacts = true,
} = {}) {
  const nextTimeline = timeline.map((event) => ({ ...event }));
  const nextLedger = {
    version: 1,
    entries: [...(ledger.entries ?? [])],
  };
  const nextReview = {
    version: 1,
    candidates: [...(review.candidates ?? [])],
  };
  const stats = {
    seen: 0,
    skipped: 0,
    factsAdded: 0,
    provenanceAttached: 0,
    candidatesAdded: 0,
  };

  for (const normalized of normalizedEntries ?? []) {
    stats.seen += 1;
    if (ledgerHas(nextLedger, normalized)) {
      stats.skipped += 1;
      continue;
    }
    const { fact, deadline } = classifyNormalized(normalized);
    nextLedger.entries.push({
      matter: normalized.matter,
      courtlistener_docket_id: normalized.courtlistener_docket_id,
      courtlistener_entry_id: normalized.courtlistener_entry_id,
      entry_number: normalized.entry_number,
      date_filed: normalized.date_filed,
      description: normalized.description,
      documents: normalized.documents ?? [],
      ingested_at: normalized.ingested_at,
      hash: normalized.hash,
    });

    if (applyFacts && fact) {
      const match = findMatchingTimelineEvent(nextTimeline, {
        matter: normalized.matter,
        entryId: normalized.courtlistener_entry_id,
        entryNumber: normalized.entry_number,
      });
      if (match) {
        nextTimeline[match.index] = attachProvenance(match.event, fact);
        stats.provenanceAttached += 1;
      } else {
        const event = { ...fact, external: cleanExternal(fact.external) };
        nextTimeline.unshift(event);
        stats.factsAdded += 1;
      }
    }

    if (deadline) {
      const candidate = {
        matter: normalized.matter,
        candidate_type: deadline.candidate_type,
        trigger_entry: normalized.entry_number,
        courtlistener_entry_id: normalized.courtlistener_entry_id,
        proposed_date: deadline.proposed_date,
        confidence: deadline.confidence,
        reason: deadline.reason,
        status: "pending",
      };
      const dup = nextReview.candidates.some(
        (row) =>
          row.matter === candidate.matter &&
          row.trigger_entry === candidate.trigger_entry &&
          row.proposed_date === candidate.proposed_date &&
          row.candidate_type === candidate.candidate_type,
      );
      if (!dup) {
        nextReview.candidates.push(candidate);
        stats.candidatesAdded += 1;
      }
    }
  }

  return { timeline: nextTimeline, ledger: nextLedger, review: nextReview, stats };
}
