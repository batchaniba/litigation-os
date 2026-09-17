// Remote MCP (Streamable HTTP, JSON) for the litigation document store.
//
// Public, authless, read-only — same contract as the HTTP routes. R2 is
// reached through the Worker DOCS binding; clients never see keys.
// POST https://litigation-doc-api.ss8sxswwkt.workers.dev/mcp
//
// Stateless JSON-RPC (MCP 2024-11-05 / 2025-03-26). No Durable Objects,
// no Agents SDK, no OAuth in this cut. Writes stay on the laptop stdio
// server (`npm run mcp`).

import { documentsKeyFromUrl, sha256ForPath } from "./documents.mjs";

const SERVER = { name: "litigation-doc-api", version: "1.0.0" };
const PROTOCOLS = new Set(["2024-11-05", "2025-03-26", "2025-06-18"]);
const DEFAULT_PROTOCOL = "2024-11-05";
const HEX64 = /^[0-9a-fA-F]{64}$/;
const PATH_INDEX_KEY = "index/path-to-sha256.json";
const PUBLIC_ORIGIN = "https://litigation-doc-api.ss8sxswwkt.workers.dev";

const CORS = {
  "access-control-allow-origin": "*",
  "access-control-allow-methods": "GET, POST, OPTIONS",
  "access-control-allow-headers":
    "content-type, accept, mcp-session-id, mcp-protocol-version",
  "access-control-max-age": "86400",
};

const TOOLS = [
  {
    name: "search_documents",
    description:
      "Search the litigation document catalog (D1 path + caption). Returns sha256, path, size, matter. Does not return PDF bytes.",
    schema: {
      query: { type: "string", description: "Substring matched against path and caption" },
      matter: { type: "integer", description: "Optional matter number" },
      limit: { type: "integer", description: "Max rows (default 20, max 50)" },
    },
    required: ["query"],
  },
  {
    name: "fetch_document",
    description:
      "Resolve one cataloged PDF by sha256 or /documents/... path. Returns metadata and public Worker URLs, not bytes. GET those URLs for the PDF.",
    schema: {
      sha256: { type: "string", description: "64-hex content hash" },
      path: { type: "string", description: "Portfolio path, e.g. /documents/matter-24/...." },
    },
  },
  {
    name: "list_matters",
    description: "Index of all matters (caption, case_no, lifecycle, next clock).",
    schema: {},
  },
  {
    name: "get_matter",
    description: "One matter plus clocks and document catalog rows.",
    schema: { n: { type: "integer", description: "Matter number" } },
    required: ["n"],
  },
  {
    name: "upcoming_deadlines",
    description: "Clock rows due within N days (default 14), including overdue.",
    schema: { days: { type: "integer", default: 14 } },
  },
  {
    name: "get_fuse_board",
    description: "Fuse / Wait / Parked board.",
    schema: { days: { type: "integer", default: 14 } },
  },
];

const byName = new Map(TOOLS.map((t) => [t.name, t]));

export { SERVER, TOOLS };

const utcToday = () => new Date().toISOString().slice(0, 10);
const addDays = (key, n) => {
  const d = new Date(`${key}T12:00:00Z`);
  d.setUTCDate(d.getUTCDate() + n);
  return d.toISOString().slice(0, 10);
};
const keyForSha256 = (sha) => `sha256/${sha.slice(0, 2)}/${sha.slice(2)}.pdf`;

function clampDays(n) {
  let days = Number(n ?? 14);
  if (!Number.isFinite(days)) days = 14;
  return Math.min(90, Math.max(1, Math.round(days)));
}

function likeNeedle(query) {
  const q = String(query ?? "")
    .trim()
    .toLowerCase()
    .replace(/[%_\\]/g, "");
  return q ? `%${q}%` : "%";
}

async function dbAll(env, sql, params = []) {
  if (!env.DB) return null;
  try {
    const res = await env.DB.prepare(sql).bind(...params).all();
    return res.results ?? [];
  } catch (e) {
    if (/no such table/i.test(e?.message ?? "")) return null;
    throw e;
  }
}

async function loadPathIndex(env) {
  if (!env.DOCS) return null;
  const obj = await env.DOCS.get(PATH_INDEX_KEY);
  if (!obj) return null;
  try {
    return await obj.json();
  } catch {
    return null;
  }
}

function originOf(request) {
  try {
    return new URL(request.url).origin;
  } catch {
    return PUBLIC_ORIGIN;
  }
}

function jsonRpc(id, result) {
  return { jsonrpc: "2.0", id, result };
}
function jsonRpcError(id, code, message, data) {
  return {
    jsonrpc: "2.0",
    id,
    error: { code, message, ...(data !== undefined ? { data } : {}) },
  };
}

function toolList() {
  return {
    tools: TOOLS.map((t) => ({
      name: t.name,
      description: t.description,
      inputSchema: {
        type: "object",
        properties: t.schema,
        ...(t.required ? { required: t.required } : {}),
        additionalProperties: false,
      },
    })),
  };
}

function matterRow(today, r) {
  return {
    number: r.number,
    caption: r.caption,
    case_no: r.case_no,
    court: r.court,
    phase: r.phase,
    lifecycle: r.lifecycle,
    status_label: r.status_label,
    judge: r.judge,
    overdue: r.lifecycle === "active" && !!r.next_clock_date && r.next_clock_date < today,
    next_clock: r.next_clock_date
      ? { date: r.next_clock_date, title: r.next_clock_title }
      : null,
  };
}

async function searchDocuments(env, args) {
  const needle = likeNeedle(args.query);
  if (needle === "%") {
    throw Object.assign(new Error("query must be a non-empty string"), { http: 400 });
  }
  let limit = Number(args.limit ?? 20);
  if (!Number.isFinite(limit)) limit = 20;
  limit = Math.min(50, Math.max(1, Math.round(limit)));
  const matter =
    args.matter === undefined || args.matter === null ? null : Number(args.matter);
  if (matter !== null && (!Number.isInteger(matter) || matter < 1 || matter > 99)) {
    throw Object.assign(new Error("matter must be an integer 1–99"), { http: 400 });
  }
  const sql = matter
    ? `SELECT d.sha256, d.path, d.size, d.matter_number, m.caption
       FROM documents d LEFT JOIN matters m ON m.number = d.matter_number
       WHERE d.matter_number = ? AND (LOWER(d.path) LIKE ? OR LOWER(IFNULL(m.caption, '')) LIKE ?)
       ORDER BY d.path LIMIT ?`
    : `SELECT d.sha256, d.path, d.size, d.matter_number, m.caption
       FROM documents d LEFT JOIN matters m ON m.number = d.matter_number
       WHERE LOWER(d.path) LIKE ? OR LOWER(IFNULL(m.caption, '')) LIKE ?
       ORDER BY d.path LIMIT ?`;
  const params = matter ? [matter, needle, needle, limit] : [needle, needle, limit];
  const rows = await dbAll(env, sql, params);
  if (!rows) throw Object.assign(new Error("d1_not_provisioned"), { http: 503 });
  return { query: String(args.query).trim(), count: rows.length, documents: rows };
}

async function fetchDocument(env, args, origin) {
  const shaArg = args.sha256 ? String(args.sha256).trim().toLowerCase() : "";
  const pathArg = args.path ? documentsKeyFromUrl(String(args.path).trim()) : "";
  if (!shaArg && !pathArg) {
    throw Object.assign(new Error("sha256 or path is required"), { http: 400 });
  }
  if (shaArg && !HEX64.test(shaArg)) {
    throw Object.assign(new Error("sha256 must be 64 hex chars"), { http: 400 });
  }

  let sha = shaArg;
  let path = pathArg || null;
  if (!sha && path) {
    const index = await loadPathIndex(env);
    sha = sha256ForPath(index, path);
    if (!sha) {
      const rows = await dbAll(env, `SELECT sha256 FROM documents WHERE path = ?`, [path]);
      const hit = rows?.[0]?.sha256;
      sha = typeof hit === "string" ? hit.toLowerCase() : null;
    }
    if (!sha) throw Object.assign(new Error("not_found"), { http: 404, path });
  }
  if (sha && !path) {
    const rows = await dbAll(env, `SELECT path, size FROM documents WHERE sha256 = ?`, [sha]);
    if (rows?.[0]?.path) path = rows[0].path;
  }

  let size = null;
  let etag = null;
  let in_r2 = false;
  if (env.DOCS) {
    const head = await env.DOCS.head(keyForSha256(sha));
    if (head) {
      in_r2 = true;
      size = head.size ?? null;
      etag = head.httpEtag ?? null;
    }
  }

  return {
    sha256: sha,
    path,
    size,
    etag,
    in_r2,
    url: `${origin}/doc/${sha}`,
    ...(path ? { documents_url: `${origin}${path}` } : {}),
  };
}

async function listMatters(env) {
  const rows = await dbAll(
    env,
    `SELECT number, caption, case_no, court, phase, lifecycle, status_label,
            judge, next_clock_title, next_clock_date
     FROM matters ORDER BY number`,
  );
  if (!rows) throw Object.assign(new Error("d1_not_provisioned"), { http: 503 });
  const today = utcToday();
  return rows.map((r) => matterRow(today, r));
}

async function getMatter(env, n) {
  const num = Number(n);
  if (!Number.isInteger(num) || num < 1 || num > 99) {
    throw Object.assign(new Error("n must be an integer 1–99"), { http: 400 });
  }
  const rows = await dbAll(
    env,
    `SELECT number, caption, case_no, court, phase, lifecycle, status_label,
            judge, next_clock_title, next_clock_date
     FROM matters WHERE number = ?`,
    [num],
  );
  if (!rows) throw Object.assign(new Error("d1_not_provisioned"), { http: 503 });
  if (!rows.length) throw Object.assign(new Error("not_found"), { http: 404, matter: num });
  const today = utcToday();
  const clocks =
    (await dbAll(
      env,
      `SELECT title, date, kind FROM clocks WHERE matter_number = ? ORDER BY date`,
      [num],
    )) ?? [];
  const documents =
    (await dbAll(
      env,
      `SELECT sha256, path, size FROM documents WHERE matter_number = ? ORDER BY path`,
      [num],
    )) ?? [];
  return {
    ...matterRow(today, rows[0]),
    clocks: clocks.map((c) => ({
      title: c.title,
      date: c.date,
      kind: c.kind,
      overdue: !!c.date && c.date < today,
    })),
    documents,
    document_count: documents.length,
  };
}

async function upcoming(env, days) {
  const window = clampDays(days);
  const today = utcToday();
  const horizon = addDays(today, window);
  const rows = await dbAll(
    env,
    `SELECT c.matter_number AS number, c.title, c.date, c.kind,
            m.caption, m.lifecycle
     FROM clocks c JOIN matters m ON m.number = c.matter_number
     WHERE c.date <= ? ORDER BY c.date, c.matter_number`,
    [horizon],
  );
  if (!rows) throw Object.assign(new Error("d1_not_provisioned"), { http: 503 });
  return rows.map((r) => ({
    number: r.number,
    caption: r.caption,
    lifecycle: r.lifecycle,
    overdue: !!r.date && r.date < today,
    date: r.date,
    kind: r.kind,
    title: r.title,
  }));
}

async function fuse(env, days) {
  const window = clampDays(days);
  const today = utcToday();
  const horizon = addDays(today, window);
  const rows = await dbAll(
    env,
    `SELECT number, caption, lifecycle, next_clock_title, next_clock_date FROM matters`,
  );
  if (!rows) throw Object.assign(new Error("d1_not_provisioned"), { http: 503 });
  const slim = rows.map((r) => ({
    number: r.number,
    caption: r.caption,
    lifecycle: r.lifecycle,
    overdue: !!r.next_clock_date && r.next_clock_date < today,
    date: r.next_clock_date ?? null,
    kind: null,
    title: r.next_clock_title ?? null,
  }));
  const fuseRows = slim
    .filter((m) => m.lifecycle === "active" && m.date && (m.overdue || m.date <= horizon))
    .sort((a, b) => a.date.localeCompare(b.date) || a.number - b.number);
  const inFuse = new Set(fuseRows.map((m) => m.number));
  const wait = slim
    .filter((m) => m.lifecycle === "active" && !inFuse.has(m.number))
    .sort((a, b) => (a.date ?? "9999").localeCompare(b.date ?? "9999") || a.number - b.number);
  const parked = slim
    .filter((m) => m.lifecycle === "pre_filing")
    .sort((a, b) => a.number - b.number);
  return { generated: today, today, horizon, fuse: fuseRows, wait, parked };
}

async function callTool(name, args, env, origin) {
  switch (name) {
    case "search_documents":
      return searchDocuments(env, args);
    case "fetch_document":
      return fetchDocument(env, args, origin);
    case "list_matters":
      return listMatters(env);
    case "get_matter":
      return getMatter(env, args.n);
    case "upcoming_deadlines":
      return upcoming(env, args.days);
    case "get_fuse_board":
      return fuse(env, args.days);
    default:
      throw Object.assign(new Error(`unknown tool: ${name}`), { http: 400 });
  }
}

async function handleMessage(msg, env, origin) {
  if (!msg || typeof msg !== "object" || msg.jsonrpc !== "2.0") {
    return jsonRpcError(msg?.id ?? null, -32600, "invalid request");
  }
  const { id, method, params = {} } = msg;
  const isNotification = id === undefined;
  switch (method) {
    case "initialize": {
      const asked = params?.protocolVersion;
      const protocolVersion = PROTOCOLS.has(asked) ? asked : DEFAULT_PROTOCOL;
      return jsonRpc(id, {
        protocolVersion,
        capabilities: { tools: { listChanged: false } },
        serverInfo: SERVER,
        instructions:
          "Read-only litigation portfolio. search_documents / fetch_document resolve the R2 catalog; GET the returned url for PDF bytes. No admin keys. Writes are not available on this server.",
      });
    }
    case "notifications/initialized":
    case "notifications/cancelled":
      return isNotification ? null : jsonRpc(id, {});
    case "ping":
      return jsonRpc(id, {});
    case "tools/list":
      return jsonRpc(id, toolList());
    case "tools/call": {
      const tool = byName.get(params.name);
      if (!tool) return jsonRpcError(id, -32602, `unknown tool: ${params.name}`);
      const args = params.arguments ?? {};
      for (const key of tool.required ?? []) {
        if (args[key] === undefined || args[key] === null || args[key] === "") {
          return jsonRpcError(id, -32602, `missing required argument: ${key}`);
        }
      }
      try {
        const data = await callTool(params.name, args, env, origin);
        return jsonRpc(id, { content: [{ type: "text", text: JSON.stringify(data) }] });
      } catch (e) {
        const payload = { error: e instanceof Error ? e.message : String(e) };
        if (e?.path) payload.path = e.path;
        if (e?.matter) payload.matter = e.matter;
        return jsonRpc(id, {
          content: [{ type: "text", text: JSON.stringify(payload) }],
          isError: true,
        });
      }
    }
    case "resources/list":
      return jsonRpc(id, { resources: [] });
    case "prompts/list":
      return jsonRpc(id, { prompts: [] });
    default:
      return jsonRpcError(id ?? null, -32601, `method not found: ${method}`);
  }
}

function mcpResponse(body, status = 200, extra = {}) {
  const headers = {
    "content-type": "application/json; charset=utf-8",
    ...CORS,
    ...extra,
  };
  if (body === null) return new Response(null, { status, headers });
  return new Response(JSON.stringify(body), { status, headers });
}

export async function handleMcp(request, env) {
  const origin = originOf(request);
  if (request.method === "OPTIONS") return mcpResponse(null, 204);
  if (request.method === "GET") {
    return mcpResponse({
      name: SERVER.name,
      version: SERVER.version,
      transport: "streamable-http",
      protocol: DEFAULT_PROTOCOL,
      endpoint: "/mcp",
      tools: TOOLS.map((t) => t.name),
      note: "POST JSON-RPC to this path. Read-only. No credentials.",
    });
  }
  if (request.method !== "POST") {
    return mcpResponse({ error: "method_not_allowed" }, 405);
  }

  let parsed;
  try {
    parsed = await request.json();
  } catch {
    return mcpResponse(jsonRpcError(null, -32700, "parse error"), 400);
  }

  const batch = Array.isArray(parsed);
  const messages = batch ? parsed : [parsed];
  const results = [];
  for (const msg of messages) {
    const res = await handleMessage(msg, env, origin);
    if (res) results.push(res);
  }
  if (results.length === 0) return mcpResponse(null, 202);
  return mcpResponse(batch ? results : results[0]);
}
