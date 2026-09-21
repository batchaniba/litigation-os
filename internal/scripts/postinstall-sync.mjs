#!/usr/bin/env node
// ==========================================================
// postinstall: refresh the gitignored derived snapshots a fresh clone
// needs before `npm run dev`, `npm run typecheck`, or `npm test`
// (summaries.json, upcoming.json, vercel.json, Pages redirects, slug landings).
//
// On Vercel / Cloudflare Pages the only thing that runs after install is
// `npm run build`, whose `prebuild` regenerates the same files. Running
// them here too just bills the same work twice, so skip when VERCEL or
// CF_PAGES is set (Pages injects CF_PAGES=1).
// ==========================================================
import { spawnSync } from "node:child_process";

if (process.env.VERCEL || process.env.CF_PAGES) {
  const host = process.env.VERCEL ? "Vercel" : "Cloudflare Pages";
  console.log(`postinstall: ${host} build — skipping sync:derived (prebuild runs it)`);
  process.exit(0);
}

const result = spawnSync("npm", ["run", "sync:derived"], { stdio: "inherit" });
process.exit(result.status ?? 1);
