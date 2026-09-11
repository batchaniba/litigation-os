#!/usr/bin/env node
// Incremental docket sync for bound federal matters.
// New entries become ledger rows + optional timeline facts. Deadlines go to review.json.
//
// Usage:
//   npm run court:sync
//   npm run court:sync -- --dry-run
//   npm run court:sync -- --matter 28

import path from "node:path";
import { fileURLToPath } from "node:url";
import { loadMatters } from "../load-matters.mjs";
import { budgetAllows, createClient, readCourtListenerToken } from "./client.mjs";
import { isFederalMatter } from "./courts.mjs";
import { normalizeDocketEntry } from "./entries.mjs";
import {
  loadLedger,
  loadReview,
  loadSyncState,
  loadTimeline,
  writeLedger,
  writeReview,
  writeSyncState,
  writeTimeline,
} from "./io.mjs";
import { reconcileEntries } from "./reconcile.mjs";
import { appendEventLog, eventFromNormalizedEntry } from "../intelligence/emit-events.mjs";

function parseArgs(argv) {
  const args = { dryRun: false, matter: null };
  for (let i = 0; i < argv.length; i += 1) {
    const token = argv[i];
    if (token === "--dry-run") args.dryRun = true;
    else if (token === "--matter") args.matter = Number(argv[++i]);
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

export async function syncDockets({
  client,
  matters,
  timeline,
  ledger,
  review,
  syncState,
  dryRun = false,
  matter = null,
  now = () => new Date(),
} = {}) {
  const ingestedAt = now().toISOString();
  const targets = boundMatters(matters, matter);
  const normalized = [];
  const perMatter = [];

  for (const row of targets) {
    const docketId = row.courtlistener.docket_id;
    const cursor = syncState.matters?.[String(row.number)] ?? {};
    const entries = await client.listDocketEntries({
      docketId,
      afterEntryId: cursor.last_entry_id ?? null,
      afterEntryNumber: cursor.last_entry_id ? null : (cursor.last_entry_number ?? null),
    });
    const rows = entries.map((entry) =>
      normalizeDocketEntry(entry, { matter: row.number, docketId, ingestedAt }),
    );
    normalized.push(...rows);
    perMatter.push({ matter: row.number, docketId, pulled: rows.length });
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
    nextSync.matters[String(row.number)] = {
      docket_id: row.courtlistener.docket_id,
      last_entry_id: last?.courtlistener_entry_id ?? prior.last_entry_id ?? null,
      last_entry_number: last?.entry_number ?? prior.last_entry_number ?? null,
      last_synced_at: ingestedAt,
    };
  }

  if (!dryRun) {
    if (result.stats.factsAdded || result.stats.provenanceAttached) {
      writeTimeline(result.timeline);
    }
    if (result.stats.seen) writeLedger(result.ledger);
    if (result.stats.candidatesAdded) writeReview(result.review);
    writeSyncState(nextSync);
    const busEvents = normalized.map((entry) => eventFromNormalizedEntry(entry));
    appendEventLog(busEvents);
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
    console.warn(`api-usage lookup failed (${err.message}); continuing with live limits unknown.`);
  }
  if (usage) {
    const budget = budgetAllows(usage);
    console.log(`API budget: ${budget.reason}`);
    if (!budget.ok) {
      console.error("Aborting sync to preserve the CourtListener request budget.");
      process.exit(3);
    }
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
  });
  console.log(
    `${args.dryRun ? "Dry run — " : ""}entries ${outcome.stats.seen}, skipped ${outcome.stats.skipped}, ` +
      `facts +${outcome.stats.factsAdded}, provenance ${outcome.stats.provenanceAttached}, ` +
      `deadline candidates +${outcome.stats.candidatesAdded}.`,
  );
  for (const row of outcome.perMatter) {
    console.log(`  Matter ${row.matter} docket ${row.docketId}: ${row.pulled} new raw entries`);
  }
}

const isCli = process.argv[1] && fileURLToPath(import.meta.url) === path.resolve(process.argv[1]);
if (isCli) {
  main().catch((err) => {
    console.error(err.message || err);
    process.exit(1);
  });
}
