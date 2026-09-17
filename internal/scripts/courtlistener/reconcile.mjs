// Merge normalized CourtListener entries into timeline.json + review.json.
// Idempotent: entry ID / hash never create a second copy.
// Dkt. N provenance requires matter + docket + date + type/description similarity.
// Deadlines never become upcoming: true here.

import { matterRefsInclude } from "../../src/utils/matterRefs.js";
import {
  classifyNormalized,
  docketNumberFromEventText,
  formatTimelineDate,
  inferFactType,
  proposedClockFromDeadline,
  splitEventFromNormalized,
} from "./entries.mjs";
import { loadDocketRules } from "./rules.mjs";

// Family 3 extraction: interpretation strategy lives in
// internal/src/data/rules/docket-interpretation.json. This module only
// renders those rules.
const RULES = loadDocketRules();

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

function tokenize(text) {
  return new Set(
    String(text ?? "")
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, " ")
      .trim()
      .split(/\s+/)
      .filter((word) => word.length > RULES.timelineMatch.tokenMinLengthExclusive),
  );
}

export function descriptionSimilarity(a, b) {
  const left = tokenize(a);
  const right = tokenize(b);
  if (!left.size || !right.size) return 0;
  let inter = 0;
  for (const word of left) {
    if (right.has(word)) inter += 1;
  }
  return inter / new Set([...left, ...right]).size;
}

function eventDocketNumber(event) {
  const fromText = docketNumberFromEventText(event.event);
  if (fromText != null) return fromText;
  const fromExternal = event.external?.entry_number;
  return fromExternal == null ? null : Number(fromExternal);
}

export function scoreTimelineMatch(event, { dateFiled, description, factType }) {
  const M = RULES.timelineMatch;
  const expectedDate = formatTimelineDate(dateFiled);
  const dateMatch = Boolean(expectedDate && event.date === expectedDate);
  const typeMatch = Boolean(factType && event.type === factType);
  const similarity = descriptionSimilarity(event.event, description);
  let score = 0;
  if (dateMatch) score += M.dateWeight;
  if (typeMatch) score += M.typeWeight;
  if (similarity >= M.strongSimilarityThreshold) score += M.strongSimilarityWeight;
  else if (similarity >= M.plausibleSimilarityThreshold) score += M.plausibleSimilarityWeight;
  return { score, dateMatch, typeMatch, similarity };
}

function isPlausible(scored) {
  return Boolean(
    scored.dateMatch &&
      (scored.typeMatch || scored.similarity >= RULES.timelineMatch.plausibleSimilarityThreshold),
  );
}

/**
 * Match a CourtListener entry onto an existing timeline row.
 * Entry-id is unique. Dkt. N alone is not — require date + type/similarity.
 * Multiple plausible rows → { ambiguous: true } so the caller parks it in review.
 */
export function findMatchingTimelineEvent(
  timeline,
  { matter, entryId, entryNumber, dateFiled, description, factType } = {},
) {
  const plausible = [];
  for (let index = 0; index < timeline.length; index += 1) {
    const event = timeline[index];
    if (!matterRefsInclude(event.matters, matter)) continue;
    const externalId = event.external?.docket_entry_id;
    if (entryId != null && externalId != null && Number(externalId) === Number(entryId)) {
      return { index, event, via: "entry_id", ambiguous: false };
    }
    if (entryNumber == null) continue;
    if (eventDocketNumber(event) !== Number(entryNumber)) continue;
    const scored = scoreTimelineMatch(event, { dateFiled, description, factType });
    if (isPlausible(scored)) {
      plausible.push({ index, event, via: "dkt_date_type", ambiguous: false, ...scored });
    }
  }
  if (plausible.length === 1) return plausible[0];
  if (plausible.length > 1) {
    return { ambiguous: true, matches: plausible, via: "dkt_ambiguous" };
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
    ambiguousQueued: 0,
  };
  const splitEvents = [];

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
        dateFiled: normalized.date_filed,
        description: normalized.description,
        factType: inferFactType(normalized.description),
      });
      if (match?.ambiguous) {
        const candidate = {
          matter: normalized.matter,
          candidate_type: "ambiguous_timeline_match",
          trigger_entry: normalized.entry_number,
          courtlistener_entry_id: normalized.courtlistener_entry_id,
          proposed_date: normalized.date_filed,
          confidence: RULES.timelineMatch.ambiguousConfidence,
          reason: `Dkt. ${normalized.entry_number} matches ${match.matches.length} timeline rows on the same date; provenance not auto-attached.`,
          status: RULES.review.pendingStatus,
        };
        const dup = nextReview.candidates.some(
          (row) =>
            row.matter === candidate.matter &&
            row.candidate_type === candidate.candidate_type &&
            row.trigger_entry === candidate.trigger_entry &&
            row.courtlistener_entry_id === candidate.courtlistener_entry_id,
        );
        if (!dup) {
          nextReview.candidates.push(candidate);
          stats.candidatesAdded += 1;
        }
        stats.ambiguousQueued += 1;
      } else if (match) {
        nextTimeline[match.index] = attachProvenance(match.event, fact);
        stats.provenanceAttached += 1;
      } else {
        const event = { ...fact, external: cleanExternal(fact.external) };
        nextTimeline.unshift(event);
        stats.factsAdded += 1;
        const split = splitEventFromNormalized(normalized, event);
        if (split) splitEvents.push(split);
      }
    }

    if (deadline) {
      const proposed_clock = proposedClockFromDeadline(normalized, deadline);
      const candidate = {
        matter: normalized.matter,
        candidate_type: deadline.candidate_type,
        trigger_entry: normalized.entry_number,
        courtlistener_entry_id: normalized.courtlistener_entry_id,
        proposed_date: deadline.proposed_date,
        confidence: deadline.confidence,
        reason: deadline.reason,
        status: RULES.review.pendingStatus,
        ...(proposed_clock ? { proposed_clock } : {}),
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

  return { timeline: nextTimeline, ledger: nextLedger, review: nextReview, stats, splitEvents };
}
