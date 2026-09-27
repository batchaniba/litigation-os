// MCP endpoint for the litigation-doc-api Worker: POST /mcp.
//
// Speaks MCP Streamable HTTP, stateless: each POST carries one JSON-RPC 2.0
// message (or a batch array) and gets a plain JSON response — no SSE stream,
// no session ids. Lets any MCP client (Cursor, Claude Code, claude.ai
// connectors, …) use the portfolio's R2 documents and D1 data without ever
// handling R2 keys: the Worker reaches the bucket through its binding.
//
// Read tools mirror `npm run q` / the stdio server in internal/mcp.
// readDocumentText returns pre-extracted PDF text inline (no separate fetch),
// and fetchDocument returns the /doc/<sha256> download URL for raw PDF bytes
// when those are needed. CORS is open so browser-based clients can call it.
//
// v2 adds write tools (create/update/delete over matters, clocks, and the
// document manifest). Writes require an "rw" Bearer <redacted> (see auth.mjs) and
// are recorded to the D1 `audit` table. Document bytes travel two ways:
// `uploadDocument` takes base64 bytes inline over JSON-RPC (handy for MCP
// clients that can only call tools — capped at 20 MB decoded), while large
// files should still use REST `PUT /doc/<sha256>` followed by
// `registerDocument`.

import {
  HttpError,
  fuseData,
  getDocText,
  getMatterData,
  headDocObject,
  listMattersData,
  searchDocumentsData,
  upcomingData,
} from "./data.mjs";
import { resolveAccess } from "./auth.mjs";
import { wwwAuthenticate } from "./oauth.mjs";
import {
  addClock,
  deleteClock,
  deleteDocBytes,
  deleteDocumentRow,
  deleteMatter,
  patchMatter,
  putDocBytes,
  recordAudit,
  upsertDocumentRow,
  upsertMatter,
} from "./writes.mjs";

const SERVER = { name: "litigation-doc-api", version: "2.1.0" };
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

// Inline-upload cap: 20 MB decoded. Base64 inflates ~33%, so the JSON-RPC
// body stays comfortably under Workers' request limits; larger files go
// through REST `PUT /doc/<sha256>`.
const MAX_UPLOAD_BYTES = 20 * 1024 * 1024;

async function sha256Hex(bytes) {
  const buf = await crypto.subtle.digest("SHA-256", bytes);
  return [...new Uint8Array(buf)].map((b) => b.toString(16).padStart(2, "0")).join("");
}

const LIFECYCLES = ["active", "pre_filing", "dismissed", "abandoned", "closed", "settled"];

// Every tool is run(args, ctx) -> plain data. ctx = { env, origin, access }.
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
  },  {
    name: "readDocumentText",
    description:
      "Read a document's contents as extracted text, paginated. Takes the 64-char manifest sha256 (from searchDocuments/getMatterDocs) and returns the text inline — no separate fetch needed. This is the preferred way to read a document; use fetchDocument only when raw PDF bytes are required.",
    inputSchema: {
      type: "object",
      properties: {
        sha256: { type: "string", pattern: "^[0-9a-fA-F]{64}$", description: "64 hex chars." },
        offset: { type: "integer", description: "Character offset into the extracted text. Default 0." },
        limit: {
          type: "integer",
          description: "Max characters to return, 1-100000. Default 20000.",
          default: 20000,
        },
      },
      required: ["sha256"],
    },
    run: async ({ sha256, offset, limit }, ctx) => getDocText(ctx.env, sha256, offset, limit),
  },
  // --- write tools (scope "rw"; enforced in callTool, audited) --------------
  // uploadDocument carries bytes inline as base64 (capped at 20 MB decoded)
  // for MCP clients that can only call tools. For large files prefer REST
  // `PUT /doc/<sha256>` + registerDocument.
  {
    name: "uploadDocument",
    write: true,
    description:
      "Upload a document's bytes (base64-encoded, max ~20 MB decoded) to R2 and register its D1 manifest row in one call. Returns the content sha256 and download URL. The sha256 is computed server-side, so the store can never disagree with its own addressing.",
    inputSchema: {
      type: "object",
      properties: {
        content_base64: {
          type: "string",
          description: "File bytes, base64-encoded. Decoded size must be 1 byte – 20 MB.",
        },
        path: {
          type: "string",
          description: "Manifest path, e.g. /documents/matter-26/Foo.pdf (required; D1 documents.path is NOT NULL).",
        },
        matter_number: { type: "integer", description: "Owning matter, or omit for an unscoped file." },
        content_type: {
          type: "string",
          description: "MIME type stored on the R2 object. Default application/pdf.",
        },
      },
      required: ["content_base64", "path"],
    },
    run: async ({ content_base64, path, matter_number, content_type }, ctx) => {
      if (typeof content_base64 !== "string" || content_base64.length === 0)
        throw new HttpError(400, { error: "content_base64 must be a non-empty string" });
      if (!/^[A-Za-z0-9+/=\s]+$/.test(content_base64))
        throw new HttpError(400, { error: "content_base64 is not valid base64" });
      let bytes;
      try {
        const bin = atob(content_base64.replace(/\s+/g, ""));
        bytes = new Uint8Array(bin.length);
        for (let i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
      } catch {
        throw new HttpError(400, { error: "content_base64 is not valid base64" });
      }
      if (bytes.byteLength === 0)
        throw new HttpError(400, { error: "empty content: nothing to upload" });
      if (bytes.byteLength > MAX_UPLOAD_BYTES)
        throw new HttpError(400, {
          error: `content too large: ${bytes.byteLength} bytes decoded (max ${MAX_UPLOAD_BYTES}); use REST PUT /doc/<sha256> for large files`,
        });
      const sha256 = await sha256Hex(bytes);
      const put = await putDocBytes(ctx.env, sha256, bytes.buffer, {
        verify: false, // sha256 was just computed from these exact bytes
        contentType: typeof content_type === "string" && content_type ? content_type : undefined,
      });
      const row = await upsertDocumentRow(ctx.env, {
        sha256: put.sha256,
        matter_number: matter_number ?? null,
        path,
        size: put.size,
      });
      return { ok: true, ...put, ...row, url: docUrl(ctx, put.sha256) };
    },
  },
  {
    name: "registerDocument",
    write: true,
    description:
      "Create or update a document manifest row (sha256 -> matter/path/size). Does not move bytes; PUT /doc/<sha256> uploads those.",
    inputSchema: {
      type: "object",
      properties: {
        sha256: { type: "string", pattern: "^[0-9a-fA-F]{64}$", description: "64 hex chars." },
        matter_number: { type: "integer", description: "Owning matter, or omit for an unscoped file." },
        path: { type: "string", description: "Manifest path, e.g. /documents/matter-26/Foo.pdf" },
        size: { type: "integer", description: "Byte size." },
      },
      required: ["sha256"],
    },
    run: (a, ctx) => upsertDocumentRow(ctx.env, a),
  },
  {
    name: "deleteDocument",
    write: true,
    description:
      "Delete a document: removes the D1 manifest row and (unless keepBytes) the R2 bytes. Requires confirm:true.",
    inputSchema: {
      type: "object",
      properties: {
        sha256: { type: "string", pattern: "^[0-9a-fA-F]{64}$", description: "64 hex chars." },
        keepBytes: { type: "boolean", description: "Keep the R2 object; drop only the manifest row." },
        confirm: { type: "boolean", description: "Must be true — deletes are irreversible." },
      },
      required: ["sha256", "confirm"],
    },
    run: async ({ sha256, keepBytes, confirm }, ctx) => {
      if (confirm !== true) throw new HttpError(400, { error: "confirm must be true to delete" });
      const row = await deleteDocumentRow(ctx.env, sha256);
      const bytes = keepBytes ? { kept: true } : await deleteDocBytes(ctx.env, sha256);
      return { ...row, bytes };
    },
  },
  {
    name: "upsertMatter",
    write: true,
    description:
      "Create or fully replace a matter row keyed by number (caption, case_no, court, phase, status_label, judge, lifecycle, next_clock_title, next_clock_date).",
    inputSchema: {
      type: "object",
      properties: {
        number: { type: "integer", description: "Matter number (key)." },
        caption: { type: "string" },
        case_no: { type: "string" },
        court: { type: "string" },
        phase: { type: "string" },
        status_label: { type: "string" },
        judge: { type: "string" },
        lifecycle: { type: "string", enum: LIFECYCLES },
        next_clock_title: { type: "string" },
        next_clock_date: { type: "string", description: "YYYY-MM-DD" },
      },
      required: ["number"],
    },
    run: (a, ctx) => upsertMatter(ctx.env, a),
  },
  {
    name: "updateMatter",
    write: true,
    description:
      "Patch only the given fields on an existing matter (e.g. correct a stale status_label). 404 if the matter is unknown.",
    inputSchema: {
      type: "object",
      properties: {
        n: { type: "integer", description: "Matter number to patch." },
        caption: { type: "string" },
        case_no: { type: "string" },
        court: { type: "string" },
        phase: { type: "string" },
        status_label: { type: "string" },
        judge: { type: "string" },
        lifecycle: { type: "string", enum: LIFECYCLES },
        next_clock_title: { type: "string" },
        next_clock_date: { type: "string", description: "YYYY-MM-DD" },
      },
      required: ["n"],
    },
    run: ({ n, ...patch }, ctx) => patchMatter(ctx.env, n, patch),
  },
  {
    name: "deleteMatter",
    write: true,
    description:
      "Delete a matter row. Refuses if it still owns clocks/documents unless cascade:true (which removes those D1 rows; R2 bytes are left). Requires confirm:true.",
    inputSchema: {
      type: "object",
      properties: {
        n: { type: "integer", description: "Matter number." },
        cascade: { type: "boolean", description: "Also delete its clocks and document rows." },
        confirm: { type: "boolean", description: "Must be true — deletes are irreversible." },
      },
      required: ["n", "confirm"],
    },
    run: ({ n, cascade, confirm }, ctx) => {
      if (confirm !== true) throw new HttpError(400, { error: "confirm must be true to delete" });
      return deleteMatter(ctx.env, n, { cascade: cascade === true });
    },
  },
  {
    name: "addClock",
    write: true,
    description: "Add a clock (deadline/hearing) to a matter.",
    inputSchema: {
      type: "object",
      properties: {
        matter_number: { type: "integer" },
        title: { type: "string" },
        date: { type: "string", description: "YYYY-MM-DD" },
        kind: { type: "string", description: "deadline | hearing | expiry | conference | ..." },
      },
      required: ["matter_number", "title"],
    },
    run: (a, ctx) => addClock(ctx.env, a),
  },
  {
    name: "deleteClock",
    write: true,
    description: "Delete clock rows matching a matter + title (+ date if given).",
    inputSchema: {
      type: "object",
      properties: {
        matter_number: { type: "integer" },
        title: { type: "string" },
        date: { type: "string", description: "YYYY-MM-DD (optional narrower match)" },
      },
      required: ["matter_number", "title"],
    },
    run: (a, ctx) => deleteClock(ctx.env, a),
  },
];

const byName = new Map(TOOLS.map((t) => [t.name, t]));

// Names of tools that mutate state. Used by handleMcp to issue an HTTP-level
// 401 + WWW-Authenticate challenge (MCP / RFC 9728 auth discovery) when an
// unauthenticated caller attempts a write, instead of a bare JSON-RPC error.
// OAuth-only clients (e.g. claude.ai connectors, which cannot send a static
// Authorization header) need that challenge to discover the authorization
// server and start the sign-in flow; without it they fail closed with no
// path to authenticate.
const WRITE_TOOL_NAMES = new Set(TOOLS.filter((t) => t.write).map((t) => t.name));

function bodyAttemptsWrite(body) {
  const msgs = Array.isArray(body) ? body : [body];
  return msgs.some(
    (m) =>
      m &&
      typeof m === "object" &&
      m.method === "tools/call" &&
      m.params &&
      typeof m.params.name === "string" &&
      WRITE_TOOL_NAMES.has(m.params.name),
  );
}

async function callTool(name, args, ctx) {
  const tool = byName.get(name);
  if (!tool) return rpcErr(null, -32602, `unknown tool: ${name}`);
  const a = args && typeof args === "object" ? args : {};

  // Scope gate. Write tools need an "rw" token; reads need canRead (open
  // unless the Worker locks reads down). -32003 = auth denied.
  const access = ctx.access;
  if (tool.write) {
    if (!access.configured)
      return rpcErr(null, -32003, "writes disabled: API_KEYS is not configured on the Worker");
    if (!access.canWrite)
      return rpcErr(null, -32003, access.hasToken ? "forbidden: rw scope required" : "unauthorized: bearer token required");
  } else if (!access.canRead) {
    return rpcErr(null, -32003, "unauthorized: bearer token required");
  }

  for (const key of tool.inputSchema.required ?? []) {
    if (a[key] === undefined) return rpcErr(null, -32602, `missing required argument: ${key}`);
  }

  const target = () => a.sha256 ?? a.n ?? a.number ?? a.matter_number ?? null;

  // Never persist document bytes to the audit table: redact the base64
  // payload, keeping only its length for forensics.
  const auditDetail = () =>
    name === "uploadDocument" && a && typeof a === "object"
      ? { ...a, content_base64: `[redacted ${String(a.content_base64 ?? "").length} chars]` }
      : a;

  return tool
    .run(a, ctx)
    .then(async (data) => {
      if (tool.write)
        await recordAudit(ctx.env, { actor: access.actor, action: name, target: target(), detail: auditDetail(), ok: true });
      return rpcOk(null, { content: [{ type: "text", text: JSON.stringify(data) }] });
    })
    .catch(async (e) => {
      if (tool.write)
        await recordAudit(ctx.env, {
          actor: access.actor,
          action: name,
          target: target(),
          detail: { args: auditDetail(), error: e instanceof HttpError ? e.body : e?.message },
          ok: false,
        });
      // 400s are client input errors; 404/409/503 surface as tool-level
      // errors with the payload, mirroring the stdio server's isError shape.
      if (e instanceof HttpError && e.status === 400)
        return rpcErr(null, -32602, e.body.error ?? "invalid params");
      const payload =
        e instanceof HttpError && e.body && typeof e.body === "object"
          ? { ...e.body, error: e.body.error ?? `http_${e.status}` }
          : { error: e?.message ?? "internal_error" };
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

  const access = await resolveAccess(request, env);
  const origin = new URL(request.url).origin;
  // Spec-compliant auth challenge: an unauthenticated write attempt gets an
  // HTTP 401 with WWW-Authenticate pointing at the protected-resource
  // metadata, so OAuth-capable clients can discover the authorization
  // server and sign in. (Reads stay open; the tool-level -32003 gate in
  // callTool remains as defense in depth.) Only challenge when auth is
  // actually configured — otherwise no token could ever satisfy it.
  if (access.configured && !access.canWrite && bodyAttemptsWrite(body)) {
    return new Response(
      JSON.stringify({
        error: "unauthorized",
        error_description:
          "This operation requires an 'rw' bearer token. Authenticate via OAuth: see " +
          `${origin}/.well-known/oauth-protected-resource`,
      }),
      {
        status: 401,
        headers: {
          "content-type": "application/json; charset=utf-8",
          "www-authenticate": wwwAuthenticate(origin),
          ...CORS,
        },
      },
    );
  }
  const ctx = { env, origin, access };
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
