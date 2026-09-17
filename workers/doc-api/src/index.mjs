// Cloudflare Worker: litigation portfolio document + data API.
//
//   GET /health            -> { ok, bucket }
//   GET  /doc/<sha256>      -> R2 PDF bytes (application/pdf, ETag passthrough)
//   GET  /doc/<sha256>/meta -> { sha256, size, etag } from R2 HEAD
//   PUT  /doc/<sha256>      -> upload bytes (rw) + upsert manifest row
//   DELETE /doc/<sha256>?confirm=1 -> remove manifest row + R2 bytes (rw)
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
import { resolveAccess, requireWrite } from "./auth.mjs";
import {
  deleteDocBytes,
  deleteDocumentRow,
  putDocBytes,
  recordAudit,
  upsertDocumentRow,
} from "./writes.mjs";

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

// --- document writes (rw scope) ---------------------------------------------
// PUT /doc/<sha256>?matter=<n>&path=<path>[&verify=false]  body = PDF bytes
//   -> R2 put (sha verified against the key by default) + manifest upsert.
// DELETE /doc/<sha256>?confirm=1[&keepBytes=true]
//   -> manifest row + R2 bytes removed. confirm=1 is mandatory.
// Bytes live on REST (not MCP) because a PDF over JSON-RPC would be
// base64-bloated and some documents are >20 MB.

async function putDoc(request, env, sha, url, access) {
  try {
    requireWrite(access);
  } catch (e) {
    return json(e.body, e.status);
  }
  try {
    const bytes = await request.arrayBuffer();
    const verify = url.searchParams.get("verify") !== "false";
    const matterParam = url.searchParams.get("matter");
    const pathParam = url.searchParams.get("path");
    const put = await putDocBytes(env, sha, bytes, { verify });
    const row = await upsertDocumentRow(env, {
      sha256: put.sha256,
      matter_number: matterParam != null && matterParam !== "" ? Number(matterParam) : null,
      path: pathParam,
      size: put.size,
    });
    await recordAudit(env, {
      actor: access.actor,
      action: "putDocument",
      target: put.sha256,
      detail: { matter: matterParam, path: pathParam, size: put.size },
      ok: true,
    });
    return json({ ok: true, ...put, row }, 201);
  } catch (e) {
    if (e instanceof HttpError) {
      await recordAudit(env, {
        actor: access.actor,
        action: "putDocument",
        target: sha,
        detail: { error: e.body },
        ok: false,
      });
      return json(e.body, e.status);
    }
    throw e;
  }
}

async function deleteDoc(env, sha, url, access) {
  try {
    requireWrite(access);
  } catch (e) {
    return json(e.body, e.status);
  }
  if (url.searchParams.get("confirm") !== "1")
    return json({ error: "confirm=1 required to delete" }, 400);
  try {
    const keepBytes = url.searchParams.get("keepBytes") === "true";
    const row = await deleteDocumentRow(env, sha);
    const bytes = keepBytes ? { kept: true } : await deleteDocBytes(env, sha);
    await recordAudit(env, {
      actor: access.actor,
      action: "deleteDocument",
      target: sha,
      detail: { keepBytes },
      ok: true,
    });
    return json({ ok: true, ...row, bytes });
  } catch (e) {
    if (e instanceof HttpError) {
      await recordAudit(env, {
        actor: access.actor,
        action: "deleteDocument",
        target: sha,
        detail: { error: e.body },
        ok: false,
      });
      return json(e.body, e.status);
    }
    throw e;
  }
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

    const access = await resolveAccess(request, env);
    let m;

    // Mutating document routes (PUT/DELETE) are matched before the GET guard.
    if ((m = path.match(/^\/doc\/([^/]+)$/))) {
      if (request.method === "PUT") return putDoc(request, env, m[1], url, access);
      if (request.method === "DELETE") return deleteDoc(env, m[1], url, access);
    }

    if (request.method !== "GET") return json({ error: "method_not_allowed" }, 405);

    if (path === "/health") return json({ ok: true, bucket: BUCKET }); // open

    // Every read below honors the read gate (open unless the Worker locks
    // reads down with API_KEYS + PUBLIC_READ != "true").
    if (!access.canRead) return json({ error: "unauthorized" }, 401);

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
