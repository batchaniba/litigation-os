#!/usr/bin/env node
// Incremental docket sync for bound federal matters.
// New entries become ledger rows + timeline archive facts + split events.jsonl.
// Deadline text becomes a review candidate with proposed_clock for setNextClock.
// Never writes clocks.json and never sets upcoming:true.
//
// Usage:
//   npm run court:sync -- --bootstrap
//   npm run court:sync -- --bootstrap --since 2026-07-01
//   npm run court:sync -- --active-only
//   npm run court:sync -- --matter 28
//   npm run court:sync -- --all
//   npm run court:sync -- --dry-run --bootstrap

import path from "node:path";
import { fileURLToPath } from "node:url";
import { loadMatters } from "../load-matters.mjs";
import { budgetAllows, createClient, readCourtListenerToken } from "./client.mjs";
import { isFederalMatter } from "./courts.mjs";
import { normalizeDocketEntry } from "./entries.mjs";
import { normalizeOpinion } from "./opinions.mjs";
import {
  loadLedger,
  loadReview,
  loadSyncState,
  loadTimeline,
  appendSplitEvents,
  writeLedger,
  writeReview,
  writeSyncState,
  writeTimeline,
} from "./io.mjs";
import { reconcileEntries } from "./reconcile.mjs";
import { loadDocketRules } from "./rules.mjs";

/** Live federal matters for the first controlled ingest. Historical / dismissed dockets stay off this list. */
export const BOOTSTRAP_MATTERS = Object.freeze([...loadDocketRules().bootstrapMatters]);
export const ACTIVE_LIFECYCLES = new Set(["active", "pre_filing"]);

export function parseArgs(argv) {
  const args = {
    dryRun: false,
    matter: null,
    bootstrap: false,
    activeOnly: false,
    all: false,
    since: null,
  };
  for (let i = 0; i < argv.length; i += 1) {
    const token = argv[i];
    if (token === "--dry-run") args.dryRun = true;
    else if (token === "--bootstrap") args.bootstrap = true;
    else if (token === "--active-only") args.activeOnly = true;
    else if (token === "--all") args.all = true;
    else if (token === "--matter") args.matter = Number(argv[++i]);
    else if (token === "--since") args.since = String(argv[++i] ?? "");
  }
  if (args.since && !/^\d{4}-\d{2}-\d{2}$/.test(args.since)) {
    const error = new Error("--since must be YYYY-MM-DD");
    error.code = "CL_SINCE_FORMAT";
    throw error;
  }
  return args;
}

export function boundMatters(matters, matterFilter = null) {
  return matters.filter((row) => {
    if (!isFederalMatter(row)) return false;
    if (matterFilter != null && row.number !== matterFilter) return false;
    return Number.isInteger(row.courtlistener?.docket_id);
  });
}

function cursorEmpty(syncState, matterNumber) {
  const cursor = syncState?.matters?.[String(matterNumber)];
  return !cursor?.last_entry_id && cursor?.last_entry_number == null;
}

export function selectSyncTargets(matters, args = {}, syncState = {}) {
  const bound = boundMatters(matters, Number.isInteger(args.matter) ? args.matter : null);
  if (Number.isInteger(args.matter)) return bound;
  if (args.bootstrap) return bound.filter((row) => BOOTSTRAP_MATTERS.includes(row.number));
  if (args.activeOnly) return bound.filter((row) => ACTIVE_LIFECYCLES.has(row.lifecycle));
  if (args.all) return bound;
  const empty = bound.some((row) => cursorEmpty(syncState, row.number));
  if (empty) {
    const error = new Error(
      "Cursors are empty. Refusing a full historical backfill. Pass --bootstrap (24, 25, 26, 28, 29, 32, 33), --active-only, --matter N, or --all.",
    );
    error.code = "CL_EMPTY_CURSOR_GUARD";
    throw error;
  }
  return bound;
}

export async function syncDockets({
  client,
  matters,
  timeline,
  ledger,
  review,
  syncState,
  dryRun = false,
  matter = null,
  bootstrap = false,
  activeOnly = false,
  all = false,
  since = null,
  now = () => new Date(),
} = {}) {
  const ingestedAt = now().toISOString();
  const targets = selectSyncTargets(matters, { matter, bootstrap, activeOnly, all }, syncState);
  const normalized = [];
  const perMatter = [];

  for (const row of targets) {
    const docketId = row.courtlistener.docket_id;
    const cursor = syncState.matters?.[String(row.number)] ?? {};
    const entries = await client.listDocketEntries({
      docketId,
      afterEntryId: cursor.last_entry_id ?? null,
      afterEntryNumber: cursor.last_entry_id ? null : (cursor.last_entry_number ?? null),
      dateFiledGte: since,
    });
    const rows = entries.map((entry) =>
      normalizeDocketEntry(entry, { matter: row.number, docketId, ingestedAt }),
    );
    normalized.push(...rows);

    // Opinions: new published opinions on bound dockets become timeline facts.
    const clusters = await client.listOpinionClusters({
      docketId,
      afterClusterId: cursor.last_opinion_cluster_id ?? null,
    });
    const opinionRows = [];
    for (const cluster of clusters) {
      const opinions = await client.listClusterOpinions({ clusterId: cluster.id });
      for (const opinion of opinions) {
        opinionRows.push(
          normalizeOpinion(opinion, cluster, { matter: row.number, docketId, ingestedAt }),
        );
      }
    }
    normalized.push(...opinionRows);
    perMatter.push({
      matter: row.number,
      docketId,
      pulled: rows.length,
      opinionsPulled: opinionRows.length,
    });
  }

  const result = reconcileEntries({
    timeline,
    ledger,
    review,
    normalizedEntries: normalized,
    applyFacts: true,
  });

  const nextSync = {
    version: 1,
    matters: { ...(syncState.matters ?? {}) },
  };
  for (const row of targets) {
    const incoming = normalized.filter((entry) => entry.matter === row.number);
    const prior = nextSync.matters[String(row.number)] ?? {};
    const last = incoming.at(-1);
    const incomingOpinions = normalized.filter(
      (entry) =>
        entry.matter === row.number && entry.courtlistener_cluster_id != null,
    );
    const lastCluster = incomingOpinions.at(-1);
    nextSync.matters[String(row.number)] = {
      docket_id: row.courtlistener.docket_id,
      last_entry_id: last?.courtlistener_entry_id ?? prior.last_entry_id ?? null,
      last_entry_number: last?.entry_number ?? prior.last_entry_number ?? null,
      last_opinion_cluster_id:
        lastCluster?.courtlistener_cluster_id ?? prior.last_opinion_cluster_id ?? null,
      last_synced_at: ingestedAt,
    };
  }

  if (!dryRun) {
    if (result.stats.factsAdded || result.stats.provenanceAttached) {
      writeTimeline(result.timeline);
    }
    if (result.splitEvents?.length) appendSplitEvents(result.splitEvents);
    if (result.stats.seen) writeLedger(result.ledger);
    if (result.stats.candidatesAdded) writeReview(result.review);
    writeSyncState(nextSync);
  }

  return { ...result, syncState: nextSync, perMatter, ingestedAt };
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const token = readCourtListenerToken();
  if (!token) {
    console.error("COURTLISTENER_TOKEN is required for docket-entry sync (resolve can run without it).");
    process.exit(2);
  }
  const client = createClient({ token });
  let usage = null;
  try {
    usage = await client.getApiUsage();
  } catch (err) {
    console.error(`api-usage lookup failed (${err.message}); refusing to sync without a budget reading.`);
    process.exit(3);
  }
  const budget = budgetAllows(usage);
  console.log(`API budget: ${budget.reason}`);
  if (!budget.ok) {
    console.error("Aborting sync to preserve the CourtListener request budget.");
    process.exit(3);
  }

  const outcome = await syncDockets({
    client,
    matters: loadMatters(),
    timeline: loadTimeline(),
    ledger: loadLedger(),
    review: loadReview(),
    syncState: loadSyncState(),
    dryRun: args.dryRun,
    matter: Number.isInteger(args.matter) ? args.matter : null,
    bootstrap: args.bootstrap,
    activeOnly: args.activeOnly,
    all: args.all,
    since: args.since,
  });
  console.log(
    `${args.dryRun ? "Dry run — " : ""}entries ${outcome.stats.seen}, skipped ${outcome.stats.skipped}, ` +
      `facts +${outcome.stats.factsAdded}, provenance ${outcome.stats.provenanceAttached}, ` +
      `deadline candidates +${outcome.stats.candidatesAdded}` +
      `${outcome.stats.ambiguousQueued ? `, ambiguous ${outcome.stats.ambiguousQueued}` : ""}.`,
  );
  for (const row of outcome.perMatter) {
    console.log(`  Matter ${row.matter} docket ${row.docketId}: ${row.pulled} new raw entries`);
  }
}

const isCli = process.argv[1] && fileURLToPath(import.meta.url) === path.resolve(process.argv[1]);
if (isCli) {
  main().catch((err) => {
    console.error(err.message || err);
    process.exit(err.code === "CL_EMPTY_CURSOR_GUARD" || err.code === "CL_SINCE_FORMAT" ? 2 : 1);
  });
}
