#!/usr/bin/env node
// Bind federal matters to stable CourtListener docket IDs.
// Search by docket number + court_id once; never rediscover a bound case by caption.
//
// Usage:
//   npm run court:resolve
//   npm run court:resolve -- --dry-run
//   npm run court:resolve -- --matter 28
//   npm run court:resolve -- --force   # ignore existing docket_id (repair only)

import path from "node:path";
import { fileURLToPath } from "node:url";
import { loadMatters } from "../load-matters.mjs";
import { createClient } from "./client.mjs";
import { courtIdFromCourt, isFederalMatter } from "./courts.mjs";
import { officeVariants, parseFederalDocket } from "./docket-number.mjs";
import { bindingFromHit, bindingsEqual, writeMatterRecord } from "./io.mjs";

function parseArgs(argv) {
  const args = { dryRun: false, force: false, matter: null };
  for (let i = 0; i < argv.length; i += 1) {
    const token = argv[i];
    if (token === "--dry-run") args.dryRun = true;
    else if (token === "--force") args.force = true;
    else if (token === "--matter") args.matter = Number(argv[++i]);
  }
  return args;
}

export async function resolveMatter(matter, client, { force = false } = {}) {
  const existing = matter.courtlistener && typeof matter.courtlistener === "object" ? matter.courtlistener : {};
  if (existing.docket_id && !force) {
    return { status: "bound", binding: existing, reason: "already_bound" };
  }
  const courtId = existing.court_id || courtIdFromCourt(matter.court);
  if (!courtId) {
    return { status: "skipped", binding: existing, reason: "unmapped_court" };
  }
  const parsed = parseFederalDocket(matter.case_no);
  if (!parsed) {
    return { status: "unresolved", binding: { court_id: courtId }, reason: "no_docket_number" };
  }
  let lastHits = [];
  for (const docketNumber of officeVariants(parsed, courtId)) {
    const hits = await client.searchDockets({ docketNumber, courtId });
    lastHits = hits;
    if (hits.length === 1) {
      return {
        status: "resolved",
        binding: bindingFromHit(hits[0], courtId),
        reason: `search ${docketNumber}`,
      };
    }
    if (hits.length > 1) {
      return {
        status: "ambiguous",
        binding: { court_id: courtId },
        reason: `${hits.length} hits for ${docketNumber}`,
        hits,
      };
    }
  }
  return {
    status: "unresolved",
    binding: { court_id: courtId },
    reason: lastHits.length ? "no_unique_hit" : "not_in_recap",
  };
}

export async function resolveDockets({ client, matters, dryRun = false, force = false, matter = null } = {}) {
  const targets = matters.filter((row) => isFederalMatter(row) && (matter == null || row.number === matter));
  const report = [];
  let wrote = 0;
  for (const row of targets) {
    const result = await resolveMatter(row, client, { force });
    const nextBinding = result.binding;
    const changed = !bindingsEqual(row.courtlistener, nextBinding);
    if (changed && !dryRun && nextBinding?.court_id) {
      writeMatterRecord({ ...row, courtlistener: nextBinding });
      wrote += 1;
    }
    report.push({
      matter: row.number,
      caption: row.caption,
      case_no: row.case_no,
      status: result.status,
      reason: result.reason,
      binding: nextBinding,
      wrote: Boolean(changed && !dryRun && nextBinding?.court_id),
      wouldWrite: Boolean(changed && dryRun && nextBinding?.court_id),
    });
  }
  return { report, wrote };
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const matters = loadMatters();
  const client = createClient();
  const { report, wrote } = await resolveDockets({
    client,
    matters,
    dryRun: args.dryRun,
    force: args.force,
    matter: Number.isInteger(args.matter) ? args.matter : null,
  });
  for (const row of report) {
    const id = row.binding?.docket_id ? `docket_id=${row.binding.docket_id}` : "unbound";
    console.log(
      `Matter ${row.matter} ${row.status} (${row.reason}) court_id=${row.binding?.court_id ?? "—"} ${id}`,
    );
  }
  console.log(
    args.dryRun
      ? `Dry run — ${report.filter((row) => row.wouldWrite).length} matter file(s) would change.`
      : `Wrote ${wrote} matter file(s). Re-run npm run sync:summaries if bindings changed.`,
  );
}

const isCli = process.argv[1] && fileURLToPath(import.meta.url) === path.resolve(process.argv[1]);
if (isCli) {
  main().catch((err) => {
    console.error(err.message || err);
    process.exit(1);
  });
}
