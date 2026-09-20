#!/usr/bin/env node
// Portfolio MCP server (stdio transport) — Stage 2 of the API boundary.
// Same operations as `npm run q`, richer transport for agent clients.
// Laptop-only: this process reads the full case graph (key_facts, damages,
// events, counsel dossiers). The public Worker MCP at
// litigation-doc-api.ss8sxswwkt.workers.dev/mcp is the filing-safe subset.
//
//   node internal/mcp/server.mjs
//
// Speaks MCP 2024-11-05 over stdio: initialize, tools/list, tools/call.
// Dependency-free (node builtins only). Honors PORTFOLIO_ROOT for testing.
import { createInterface } from "node:readline";
import * as query from "../scripts/lib/query.mjs";
import * as mutate from "../scripts/lib/mutate.mjs";

const SERVER = { name: "litigation-portfolio", version: "0.2.0" };

// Every tool is (params) => result. The lib functions are the contract;
// these adapters normalize the few positional signatures.
const TOOLS = [
  {
    name: "getMatter",
    description: "Identity + index entry for one matter by number.",
    fn: ({ n }) => query.getMatter(n),
    schema: { n: { type: "integer", description: "Matter number" } },
    required: ["n"],
  },
  {
    name: "listMatters",
    description: "Index entries, optionally filtered by lifecycle, phase, or cluster.",
    fn: (p) => query.listMatters(p),
    schema: {
      lifecycle: { type: "string" },
      phase: { type: "string" },
      cluster: { type: "integer", description: "Numbered bucket from clusters.js, not a named-graph slug" },
    },
  },
  {
    name: "upcomingDeadlines",
    description: "Live clocks due within N days (or overdue), ranked. Reads index next_clock.",
    fn: (p) => query.upcomingDeadlines(p),
    schema: { days: { type: "integer", default: 14 }, matter: { type: "integer" } },
  },
  {
    name: "getTimeline",
    description: "Events, newest first. Split matters read events.jsonl.",
    fn: (p) => query.getTimeline(p),
    schema: {
      matter: { type: "integer" },
      since: { type: "string", description: "YYYY-MM-DD" },
      upcomingOnly: { type: "boolean" },
      limit: { type: "integer", default: 200 },
    },
  },
  {
    name: "getFuseBoard",
    description: "Fuse / Wait / Parked board as structured data.",
    fn: (p) => query.getFuseBoard(p),
    schema: { days: { type: "integer", default: 14 } },
  },
  {
    name: "fetchDocument",
    description: "One PDF from R2 by manifest sha256. Bytes re-hashed; mismatches refused.",
    fn: ({ sha256, out }) => query.fetchDocument(sha256, out),
    schema: {
      sha256: { type: "string", description: "64 hex chars" },
      out: { type: "string", description: "Destination path (default: <sha256>.pdf in cwd)" },
    },
    required: ["sha256"],
  },
  {
    name: "searchDocuments",
    description: "Full-text search over the .txt sidecars on main (no R2 touch).",
    fn: ({ query: q, limit }) => query.searchDocuments(q, { limit }),
    schema: { query: { type: "string" }, limit: { type: "integer", default: 20 } },
    required: ["query"],
  },
  {
    name: "getCounselDossier",
    description: "Opposing-counsel dossier by name (fuzzy slug match).",
    fn: ({ name }) => query.getCounselDossier(name),
    schema: { name: { type: "string" } },
    required: ["name"],
  },
  {
    name: "getJudgeDossier",
    description: "Judge dossier by name (fuzzy slug match).",
    fn: ({ name }) => query.getJudgeDossier(name),
    schema: { name: { type: "string" } },
    required: ["name"],
  },
  {
    name: "getClusters",
    description:
      "Named cross-matter graph (slug ids such as chp-nov2024). Not matter.cluster numbers — use getNumberedClusters for those.",
    fn: () => query.getClusters(),
    schema: {},
  },
  {
    name: "getNumberedClusters",
    description:
      "Numbered thematic buckets (1–6). Truth is clusters.js + matter.json cluster. 3 = Employment, 5 = Consumer Fraud.",
    fn: () => query.getNumberedClusters(),
    schema: {},
  },
  {
    name: "getMatterDocs",
    description: "Manifest entries for one matter's documents.",
    fn: ({ n }) => query.getMatterDocs(n),
    schema: { n: { type: "integer" } },
    required: ["n"],
  },
  {
    name: "recordTimelineEvent",
    description:
      "Append a timeline event (split→events.jsonl, legacy→timeline.json). " +
      "upcoming:true requires a /documents/ source in the manifest; duplicates refused. " +
      "Writes land on the working tree for review — nothing merges.",
    fn: (p) => mutate.recordTimelineEvent(p),
    schema: {
      date: { type: "string", description: "YYYY-MM-DD or 'Sep. 18, 2026'" },
      type: { type: "string" },
      actor: { type: "string", enum: ["you", "opposing", "agency", "court", "unknown"] },
      matters: { type: "array", items: { type: "integer" } },
      title: { type: "string" },
      source: { type: "string" },
      source_type: {
        type: "string",
        enum: ["portfolio", "courtlistener", "pacer", "email", "court_order", "manual"],
      },
      upcoming: { type: "boolean" },
      filed: { type: "boolean" },
    },
    required: ["date", "type", "matters", "title"],
  },
  {
    name: "retireUpcomingEvent",
    description:
      "Retire a live upcoming clock (split: append-only tombstone; legacy: flip in place, never delete).",
    fn: (p) => mutate.retireUpcomingEvent(p),
    schema: {
      matter: { type: "integer" },
      date: { type: "string" },
      reason: { type: "string" },
    },
    required: ["matter", "date", "reason"],
  },
  {
    name: "setNextClock",
    description:
      "Set a matter's next clock (split: clocks.json upsert; legacy: delegates to recordTimelineEvent). " +
      "One live clock per kind — same-kind conflicts refused unless supersedes names the old clock.",
    fn: (p) => mutate.setNextClock(p),
    schema: {
      matter: { type: "integer" },
      id: { type: "string" },
      date: { type: "string" },
      kind: { type: "string" },
      title: { type: "string" },
      status: { type: "string", default: "open" },
      source_dkt: { type: "integer" },
      source: { type: "string" },
      time: { type: "string" },
      tz: { type: "string" },
      supersedes: { type: "string" },
    },
    required: ["matter", "id", "date", "kind", "title"],
  },
  {
    name: "updateMatterIdentity",
    description:
      "Patch a matter's identity record. CI-equivalent validation; lifecycle/phase enums; 80-line/8KB budget on split identity files.",
    fn: (p) => mutate.updateMatterIdentity(p),
    schema: { n: { type: "integer" }, patch: { type: "object" } },
    required: ["n", "patch"],
  },
  {
    name: "catalogDocument",
    description:
      "Catalog one document across manifest + registry + matter documents[] atomically. R2 key derived from sha256.",
    fn: (p) => mutate.catalogDocument(p),
    schema: {
      matter: { type: "integer" },
      path: { type: "string" },
      sha256: { type: "string" },
      size: { type: "integer" },
      label: { type: "string" },
      matterLabel: { type: "string" },
      filed: { type: "boolean" },
    },
    required: ["matter", "path", "sha256", "size", "label"],
  },
  {
    name: "scaffoldMatter",
    description: "Scaffold a new matter via the existing script. Disabled under PORTFOLIO_ROOT.",
    fn: (p) => mutate.scaffoldMatter(p),
    schema: { n: { type: "integer" }, caption: { type: "string" } },
    required: ["n", "caption"],
  },
  {
    name: "splitMatter",
    description: "Split a legacy matter via the existing script. Disabled under PORTFOLIO_ROOT.",
    fn: (p) => mutate.splitMatter(p),
    schema: { n: { type: "integer" } },
    required: ["n"],
  },
];

const byName = new Map(TOOLS.map((t) => [t.name, t]));

const ok = (id, result) => ({ jsonrpc: "2.0", id, result });
const err = (id, code, message, data) => ({
  jsonrpc: "2.0",
  id,
  error: { code, message, ...(data !== undefined ? { data } : {}) },
});

async function handle(msg) {
  const { id, method, params = {} } = msg;
  switch (method) {
    case "initialize":
      return ok(id, {
        protocolVersion: "2024-11-05",
        capabilities: { tools: {} },
        serverInfo: SERVER,
      });
    case "notifications/initialized":
      return null;
    case "tools/list":
      return ok(id, {
        tools: TOOLS.map((t) => ({
          name: t.name,
          description: t.description,
          inputSchema: {
            type: "object",
            properties: t.schema,
            ...(t.required ? { required: t.required } : {}),
          },
        })),
      });
    case "tools/call": {
      const tool = byName.get(params.name);
      if (!tool) return err(id, -32602, `unknown tool: ${params.name}`);
      const args = params.arguments ?? {};
      for (const key of tool.required ?? []) {
        if (args[key] === undefined) return err(id, -32602, `missing required argument: ${key}`);
      }
      try {
        const data = await tool.fn(args);
        return ok(id, { content: [{ type: "text", text: JSON.stringify(data) }] });
      } catch (e) {
        const payload = { error: e instanceof Error ? e.message : String(e) };
        if (e instanceof Error && e.detail !== undefined) payload.detail = e.detail;
        return ok(id, { content: [{ type: "text", text: JSON.stringify(payload) }], isError: true });
      }
    }
    default:
      return err(id, -32601, `method not found: ${method}`);
  }
}

const rl = createInterface({ input: process.stdin, terminal: false });
for await (const line of rl) {
  if (!line.trim()) continue;
  let msg;
  try {
    msg = JSON.parse(line);
  } catch {
    process.stdout.write(`${JSON.stringify(err(null, -32700, "parse error"))}\n`);
    continue;
  }
  try {
    const res = await handle(msg);
    if (res) process.stdout.write(`${JSON.stringify(res)}\n`);
  } catch (e) {
    process.stdout.write(
      `${JSON.stringify(err(msg.id ?? null, -32603, e instanceof Error ? e.message : String(e)))}\n`,
    );
  }
}
