// MCP endpoint for the litigation-doc-api Worker: POST /mcp.
//
// Speaks MCP Streamable HTTP, stateless: each POST carries one JSON-RPC 2.0
// message (or a batch array) and gets a plain JSON response — no SSE stream,
// no session ids. Lets any MCP client (Cursor, Claude Code, claude.ai
// connectors, …) use the portfolio's R2 documents and D1 data without ever
// handling R2 keys: the Worker reaches the bucket through its binding.
//
// Read-only by design (v1): the same read operations as `npm run q` / the
// stdio server in internal/mcp. PDF bytes are not embedded in tool results —
// fetchDocument returns the /doc/<sha256> download URL and the model fetches
// it over HTTP. CORS is open so browser-based clients can call it.

import {
  HttpError,
  fuseData,
  getMatterData,
  headDocObject,
  listMattersData,
  searchDocumentsData,
  upcomingData,
} from "./data.mjs";

const SERVER = { name: "litigation-doc-api", version: "1.1.0" };
// Newest first; the initialize handshake negotiates the client's version
// when we speak it, otherwise our newest.
const PROTOCOLS = ["2025-06-18", "2025-03-26", "2024-11-05"];

const CORS = {
  "access-control-allow-origin": "*",
  "access-control-allow-methods": "POST, OPTIONS",
  "access-control-allow-headers": "content-type, authorization",
  "access-control-max-age": "86400",
};

const json = (data, status = 200) =>
  new Response(JSON.stringify(data), {
    status,
    headers: { "content-type": "application/json; charset=utf-8", ...CORS },
  });

const rpcOk = (id, result) => ({ jsonrpc: "2.0", id, result });
const rpcErr = (id, code, message, data) => ({
  jsonrpc: "2.0",
  id,
  error: { code, message, ...(data !== undefined ? { data } : {}) },
});

const toInt = (v) => {
  if (typeof v === "number" && Number.isInteger(v)) return v;
  if (typeof v === "string" && /^\d{1,3}$/.test(v.trim())) return Number(v.trim());
  return NaN;
};

const docUrl = (ctx, sha256) => `${ctx.origin}/doc/${sha256}`;
const withUrls = (ctx, docs) =>
  (docs ?? []).map((d) => ({ ...d, url: docUrl(ctx, d.sha256) }));

const LIFECYCLES = ["active", "pre_filing", "dismissed", "abandoned", "closed", "settled"];

// Every tool is run(args, ctx) -> plain data. ctx = { env, origin }.
const TOOLS = [
  {
    name: "listMatters",
    description:
      "Every tracked matter: number, caption, case number, court, phase, lifecycle, judge, and next clock.",
    inputSchema: {
      type: "object",
      properties: {
        lifecycle: {
          type: "string",
          enum: LIFECYCLES,
          description: "Filter to one lifecycle (e.g. 'active'). Omit for all matters.",
        },
      },
    },
    run: async ({ lifecycle }, ctx) => {
      const rows = await listMattersData(ctx.env);
      return lifecycle ? rows.filter((m) => m.lifecycle === lifecycle) : rows;
    },
  },
  {
    name: "getMatter",
    description:
      "One matter by number: identity, live clocks, and its document manifest rows (each with a download URL).",
    inputSchema: {
      type: "object",
      properties: {
        n: { type: "integer", description: "Matter number, e.g. 27." },
      },
      required: ["n"],
    },
    run: async ({ n }, ctx) => {
      const num = toInt(n);
      if (!Number.isInteger(num)) throw new HttpError(400, { error: "n must be an integer matter number" });
      const m = await getMatterData(ctx.env, num);
      return { ...m, documents: withUrls(ctx, m.documents) };
    },
  },
  {
    name: "upcomingDeadlines",
    description:
      "Clock rows due within N days (default 14), oldest first, including overdue ones. Mirrors the fuse board's live clocks.",
    inputSchema: {
      type: "object",
      properties: {
        days: { type: "integer", description: "Window in days, 1-90. Default 14.", default: 14 },
        matter: { type: "integer", description: "Restrict to one matter number." },
      },
    },
    run: async ({ days, matter }, ctx) => {
      const rows = await upcomingData(ctx.env, days);
      if (matter === undefined || matter === null) return rows;
      const num = toInt(matter);
      if (!Number.isInteger(num)) throw new HttpError(400, { error: "matter must be an integer matter number" });
      return rows.filter((r) => r.number === num);
    },
  },
  {
    name: "getFuseBoard",
    description:
      "Fuse / Wait / Parked board: active matters with a clock inside the window, active matters waiting, and pre-filing matters parked.",
    inputSchema: {
      type: "object",
      properties: {
        days: { type: "integer", description: "Fuse window in days, 1-90. Default 14.", default: 14 },
      },
    },
    run: async ({ days }, ctx) => fuseData(ctx.env, days),
  },
  {
    name: "getMatterDocs",
    description: "Document manifest rows for one matter, each with a download URL.",
    inputSchema: {
      type: "object",
      properties: {
        n: { type: "integer", description: "Matter number, e.g. 26." },
      },
      required: ["n"],
    },
    run: async ({ n }, ctx) => {
      const num = toInt(n);
      if (!Number.isInteger(num)) throw new HttpError(400, { error: "n must be an integer matter number" });
      const m = await getMatterData(ctx.env, num);
      return withUrls(ctx, m.documents);
    },
  },
  {
    name: "searchDocuments",
    description:
      "Substring search over document manifest paths (filenames carry the labels) and matter captions. Returns matching rows with download URLs.",
    inputSchema: {
      type: "object",
      properties: {
        query: { type: "string", description: "Substring to match, e.g. 'settlement demand'." },
        limit: { type: "integer", description: "Max rows, 1-100. Default 20.", default: 20 },
      },
      required: ["query"],
    },
    run: async ({ query, limit }, ctx) => {
      const rows = await searchDocumentsData(ctx.env, query, limit);
      return withUrls(ctx, rows);
    },
  },
  {
    name: "fetchDocument",
    description:
      "Resolve one PDF by its 64-char manifest sha256. Returns size, ETag, and the download URL — fetch the bytes with an HTTP GET on the URL (application/pdf).",
    inputSchema: {
      type: "object",
      properties: {
        sha256: { type: "string", pattern: "^[0-9a-fA-F]{64}$", description: "64 hex chars." },
      },
      required: ["sha256"],
    },
    run: async ({ sha256 }, ctx) => {
      if (typeof sha256 !== "string" || !/^[0-9a-fA-F]{64}$/.test(sha256))
        throw new HttpError(400, { error: "sha256 must be 64 hex chars" });
      const meta = await headDocObject(ctx.env, sha256);
      return { ...meta, url: docUrl(ctx, meta.sha256) };
    },
  },
];

const byName = new Map(TOOLS.map((t) => [t.name, t]));

async function callTool(name, args, ctx) {
  const tool = byName.get(name);
  if (!tool) return rpcErr(null, -32602, `unknown tool: ${name}`);
  const a = args && typeof args === "object" ? args : {};
  for (const key of tool.inputSchema.required ?? []) {
    if (a[key] === undefined) return rpcErr(null, -32602, `missing required argument: ${key}`);
  }
  return tool
    .run(a, ctx)
    .then((data) => rpcOk(null, { content: [{ type: "text", text: JSON.stringify(data) }] }))
    .catch((e) => {
      // 400s are client input errors; 404/503 surface as tool-level errors
      // with the payload, mirroring the stdio server's isError shape.
      if (e instanceof HttpError && e.status === 400)
        return rpcErr(null, -32602, e.body.error ?? "invalid params");
      const payload = {
        error: e instanceof HttpError ? (e.body.error ?? `http_${e.status}`) : (e?.message ?? "internal_error"),
      };
      return rpcOk(null, {
        content: [{ type: "text", text: JSON.stringify(payload) }],
        isError: true,
      });
    });
}

async function handleMessage(msg, ctx) {
  if (!msg || typeof msg !== "object" || msg.jsonrpc !== "2.0" || typeof msg.method !== "string") {
    return rpcErr(msg?.id ?? null, -32600, "invalid request");
  }
  const id = msg.id === undefined ? null : msg.id;
  const params = msg.params ?? {};
  switch (msg.method) {
    case "initialize": {
      const asked = params.protocolVersion;
      const negotiated = PROTOCOLS.includes(asked) ? asked : PROTOCOLS[0];
      return rpcOk(id, {
        protocolVersion: negotiated,
        capabilities: { tools: {} },
        serverInfo: SERVER,
      });
    }
    case "ping":
      return rpcOk(id, {});
    case "tools/list":
      return rpcOk(
        id,
        { tools: TOOLS.map(({ run: _r, ...t }) => t) },
      );
    case "tools/call": {
      const res = await callTool(params.name, params.arguments, ctx);
      return { ...res, id };
    }
    default:
      // Unknown notifications are ignored; unknown requests get -32601.
      if (msg.id === undefined) return null;
      return rpcErr(id, -32601, `method not found: ${msg.method}`);
  }
}

export async function handleMcp(request, env) {
  if (request.method === "OPTIONS") return new Response(null, { status: 204, headers: CORS });
  if (request.method !== "POST") return json({ error: "method_not_allowed" }, 405);

  let body;
  try {
    body = await request.json();
  } catch {
    return json(rpcErr(null, -32700, "parse error"), 400);
  }

  const ctx = { env, origin: new URL(request.url).origin };
  if (Array.isArray(body)) {
    const out = [];
    for (const m of body) {
      const r = await handleMessage(m, ctx);
      if (r) out.push(r);
    }
    return json(out);
  }
  const res = await handleMessage(body, ctx);
  // Notifications (no id) get a bare 202 per the Streamable HTTP spec.
  if (res === null) return new Response(null, { status: 202, headers: CORS });
  return json(res);
}
