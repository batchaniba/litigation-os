// Cloudflare Worker: litigation portfolio document + data API.
//
//   GET /health            -> { ok, bucket }
//   GET /doc/<sha256>      -> R2 PDF bytes (application/pdf, ETag passthrough)
//   GET /doc/<sha256>/meta -> { sha256, size, etag } from R2 HEAD
//   GET /matters           -> D1 matter rows (mirrors `npm run q listMatters`)
//   GET /matters/<n>       -> one matter + clocks + documents (mirrors getMatter)
//   GET /upcoming?days=14  -> clock rows due within window (mirrors upcomingDeadlines)
//   GET /fuse              -> { fuse, wait, parked } (mirrors getFuseBoard)
//   POST /mcp              -> MCP endpoint (Streamable HTTP, stateless JSON-RPC):
//                             initialize / ping / tools/list / tools/call over the
//                             same read operations. CORS-open so browser-based
//                             MCP clients can call it.
//   POST /admin/reseed     -> guarded D1 re-apply of seed.sql
//                             (Authorization: Bearer <RESEED_SECRET>)
//
// R2 is reached through the DOCS *binding* — this file contains no keys,
// tokens, or secrets. D1 is optional at runtime: data routes return
// 503 { error: "d1_not_provisioned" } when the DB binding is absent, so the
// document routes work before D1 is ever seeded.
//
// scheduled(): daily fuse digest (~08:08 PT) and Monday roll call, computed
// from D1 with zero dependencies. POSTs JSON to ALERT_WEBHOOK when set,
// otherwise console.log.

import {
  HttpError,
  buildDigest,
  fuseData,
  getDocObject,
  getMatterData,
  headDocObject,
  listMattersData,
  upcomingData,
} from "./data.mjs";
import { handleMcp } from "./mcp.mjs";

const BUCKET = "litigation-documents";

const json = (data, status = 200) =>
  new Response(JSON.stringify(data), {
    status,
    headers: { "content-type": "application/json; charset=utf-8" },
  });

// Run a data-layer op and translate HttpError into its REST response.
// Unexpected exceptions propagate (the runtime turns them into 500s),
// exactly like the pre-refactor worker.
const route = (op) => async (...args) => {
  try {
    return json(await op(...args));
  } catch (e) {
    if (e instanceof HttpError) return json(e.body, e.status);
    throw e;
  }
};

// --- R2 routes --------------------------------------------------------------

async function serveDoc(env, sha) {
  try {
    const { obj } = await getDocObject(env, sha);
    const headers = new Headers();
    headers.set("content-type", "application/pdf");
    if (obj.httpEtag) headers.set("etag", obj.httpEtag);
    if (obj.size != null) headers.set("content-length", String(obj.size));
    return new Response(obj.body, { headers });
  } catch (e) {
    if (e instanceof HttpError) return json(e.body, e.status);
    throw e;
  }
}

const docMeta = route(headDocObject);
const listMatters = route(listMattersData);
const getMatter = route((env, n) => getMatterData(env, n));
const upcoming = route((env, params) => upcomingData(env, params.get("days")));
const fuse = route((env, params) => fuseData(env, params.get("days")));

// --- admin: D1 self-reseed --------------------------------------------------
// POST /admin/reseed with `Authorization: Bearer <RESEED_SECRET>` and the
// seed.sql text as the body (one `INSERT ...;` per line, see seed.mjs).
// Applies the statements to the D1 binding in small batches, so the
// `d1-reseed.yml` workflow can keep D1 in sync with the repo after every
// portfolio-data merge. Fail-closed: 503 when RESEED_SECRET is not
// configured on the Worker, 403 on a Bearer <redacted>
async function handleReseed(request, env) {
  if (!env.RESEED_SECRET) return json({ error: "reseed_not_configured" }, 503);
  const auth = request.headers.get("authorization") || "";
  if (auth !== `Bearer ${env.RESEED_SECRET}`)
    return json({ error: "forbidden" }, 403);
  if (!env.DB) return json({ error: "d1_not_provisioned" }, 503);
  const body = await request.text();
  const statements = body
    .split("\n")
    .map((l) => l.trim())
    .filter((l) => /^INSERT\s/i.test(l));
  let applied = 0;
  for (let i = 0; i < statements.length; i += 50) {
    const chunk = statements.slice(i, i + 50);
    await env.DB.batch(chunk.map((sql) => env.DB.prepare(sql)));
    applied += chunk.length;
  }
  return json({ ok: true, statements: applied });
}

// --- entrypoint ---------------------------------------------------------------

export default {
  async fetch(request, env, _ctx) {
    const url = new URL(request.url);
    const path = url.pathname;

    if (path === "/mcp") return handleMcp(request, env);

    if (path === "/admin/reseed") {
      if (request.method !== "POST")
        return json({ error: "method_not_allowed" }, 405);
      return handleReseed(request, env);
    }
    if (request.method !== "GET") return json({ error: "method_not_allowed" }, 405);

    if (path === "/health") return json({ ok: true, bucket: BUCKET });

    let m;
    if ((m = path.match(/^\/doc\/([^/]+)\/meta$/))) return docMeta(env, m[1]);
    if ((m = path.match(/^\/doc\/([^/]+)$/))) return serveDoc(env, m[1]);
    if (path.startsWith("/doc/")) return json({ error: "sha256 must be 64 hex chars" }, 400);

    if (path === "/matters") return listMatters(env);
    if ((m = path.match(/^\/matters\/(\d{1,2})$/))) return getMatter(env, Number(m[1]));
    if (path === "/upcoming") return upcoming(env, url.searchParams);
    if (path === "/fuse") return fuse(env, url.searchParams);

    return json({ error: "not_found" }, 404);
  },

  async scheduled(event, env, ctx) {
    ctx.waitUntil(
      (async () => {
        const payload = await buildDigest(env, event.cron);
        if (env.ALERT_WEBHOOK) {
          await fetch(env.ALERT_WEBHOOK, {
            method: "POST",
            headers: { "content-type": "application/json" },
            body: JSON.stringify(payload),
          });
        } else {
          console.log(JSON.stringify(payload));
        }
      })(),
    );
  },
};
