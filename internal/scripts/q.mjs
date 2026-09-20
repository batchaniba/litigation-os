#!/usr/bin/env node
// Portfolio query CLI — Stage 1 of the API boundary.
//   npm run q <op> [--key value] [...]
// Emits JSON on stdout; errors as {"error": "..."} with exit 1.
// See internal/docs/API_OPERATIONS.md for the operation catalog.
import {
  getMatter,
  listMatters,
  upcomingDeadlines,
  getTimeline,
  getFuseBoard,
  fetchDocument,
  searchDocuments,
  getCounselDossier,
  getJudgeDossier,
  getClusters,
  getNumberedClusters,
  getMatterDocs,
} from "./lib/query.mjs";
import {
  recordTimelineEvent,
  retireUpcomingEvent,
  setNextClock,
  updateMatterIdentity,
  catalogDocument,
  scaffoldMatter,
  splitMatter,
} from "./lib/mutate.mjs";

const OPS = {
  getMatter: { fn: getMatter, args: ["n"] },
  listMatters: { fn: listMatters, opts: true },
  upcomingDeadlines: { fn: upcomingDeadlines, opts: true },
  getTimeline: { fn: getTimeline, opts: true, bool: ["upcomingOnly"] },
  getFuseBoard: { fn: getFuseBoard, opts: true },
  fetchDocument: { fn: fetchDocument, args: ["sha256"], flags: ["out"] },
  searchDocuments: { fn: searchDocuments, args: ["query"], flags: ["limit"] },
  getCounselDossier: { fn: getCounselDossier, args: ["name"] },
  getJudgeDossier: { fn: getJudgeDossier, args: ["name"] },
  getClusters: { fn: getClusters },
  getNumberedClusters: { fn: getNumberedClusters },
  getMatterDocs: { fn: getMatterDocs, args: ["n"] },
  // --- writes (Stage 1b): validated before touching disk ---
  recordTimelineEvent: { fn: recordTimelineEvent, opts: true, json: ["matters"], bool: ["upcoming", "filed"] },
  retireUpcomingEvent: { fn: retireUpcomingEvent, opts: true },
  setNextClock: { fn: setNextClock, opts: true, int: ["source_dkt"] },
  updateMatterIdentity: { fn: updateMatterIdentity, opts: true, json: ["patch"], int: ["n"] },
  catalogDocument: { fn: catalogDocument, opts: true, int: ["matter", "size"], bool: ["filed"] },
  scaffoldMatter: { fn: scaffoldMatter, opts: true, int: ["n"] },
  splitMatter: { fn: splitMatter, opts: true, int: ["n"] },
};

function coerce(spec, params) {
  const out = { ...params };
  for (const k of spec.json ?? []) {
    if (typeof out[k] === "string") {
      try {
        out[k] = JSON.parse(out[k]);
      } catch {
        throw new Error(`--${k} must be JSON`);
      }
    }
  }
  for (const k of spec.int ?? []) {
    if (out[k] !== undefined) out[k] = Number(out[k]);
  }
  for (const k of spec.bool ?? []) {
    if (typeof out[k] === "string") out[k] = out[k].toLowerCase() === "true";
  }
  return out;
}

function usage() {
  console.error(`Usage: npm run q <op> [--key value] [...]\n\nOperations:\n${Object.keys(OPS).map((o) => `  ${o}`).join("\n")}`);
  process.exit(2);
}

const [op, ...rest] = process.argv.slice(2);
if (!op || !OPS[op]) usage();

const params = {};
const positional = [];
for (let i = 0; i < rest.length; i++) {
  if (rest[i].startsWith("--")) {
    const key = rest[i].slice(2);
    params[key] = rest[i + 1]?.startsWith("--") || rest[i + 1] === undefined ? true : rest[++i];
  } else {
    positional.push(rest[i]);
  }
}

try {
  const { fn, args = [], opts = false, flags = [] } = OPS[op];
  let result;
  if (opts) {
    result = await fn(coerce(OPS[op], params));
  } else if (args.length) {
    const values = args.map((a, i) => positional[i] ?? params[a]);
    if (values.some((v) => v === undefined)) usage();
    const extra = Object.fromEntries(flags.map((f) => [f, params[f]]).filter(([, v]) => v !== undefined));
    // fetchDocument takes (sha256, outPath); the rest take an options object.
    result = op === "fetchDocument" ? await fn(values[0], extra.out) : await fn(...values, extra);
  } else {
    result = await fn();
  }
  console.log(JSON.stringify(result));
} catch (error) {
  console.log(JSON.stringify({ error: error instanceof Error ? error.message : String(error) }));
  process.exit(1);
}
