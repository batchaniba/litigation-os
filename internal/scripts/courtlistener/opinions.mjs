// Normalize CourtListener opinion clusters into portfolio facts.
// Opinions are confirmed court issuances: they become timeline facts
// (upcoming stays false), deduplicated by hash like docket entries.

import { entryHash, formatTimelineDate } from "./entries.mjs";

const OPINION_TYPE_LABELS = {
  "010combined": "Combined Opinion",
  "015united_states_federal_district": "District Opinion",
  "020lead": "Lead Opinion",
  "025plurality": "Plurality Opinion",
  "030concurrence": "Concurrence",
  "035concurrence_in_part": "Concurrence in Part",
  "040dissent": "Dissent",
  "045dissent_in_part": "Dissent in Part",
  "050addendum": "Addendum",
  "060remittitur": "Remittitur",
  "070rehearing": "Rehearing Order",
  "080on_the_merits": "On the Merits",
  "090on_motion_to_strike_cost_bill": "Cost Bill Ruling",
};

export function opinionTypeLabel(type) {
  return OPINION_TYPE_LABELS[String(type ?? "")] ?? String(type ?? "opinion");
}

export function normalizeOpinion(opinion, cluster, { matter, docketId, ingestedAt }) {
  const opinionId = opinion?.id ?? null;
  const clusterId = cluster?.id ?? null;
  const dateFiled = String(cluster?.date_filed ?? "").slice(0, 10) || null;
  const caseName = String(cluster?.case_name ?? "").trim();
  const typeLabel = opinionTypeLabel(opinion?.type);
  const description = `OPINION (${typeLabel}): ${caseName}`.trim();
  return {
    matter,
    courtlistener_docket_id: docketId,
    courtlistener_entry_id: opinionId,
    courtlistener_cluster_id: clusterId,
    entry_number: null,
    date_filed: dateFiled,
    description,
    documents: [],
    opinion_url: cluster?.absolute_url
      ? `https://www.courtlistener.com${cluster.absolute_url}`
      : null,
    download_url: opinion?.download_url ?? null,
    ingested_at: ingestedAt,
    hash: entryHash({
      docketId,
      entryId: `opinion-${opinionId}`,
      entryNumber: null,
      dateFiled,
      description,
    }),
  };
}
