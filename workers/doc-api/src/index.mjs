// Cloudflare Worker: litigation portfolio document + data API.
//
//   GET /health            -> { ok, bucket }
//   GET /doc/<sha256>      -> R2 PDF bytes (application/pdf, ETag passthrough)
//   GET /doc/<sha256>/meta -> { sha256, size, etag } from R2 HEAD
//   GET /matters           -> D1 matter rows (mirrors `npm run q listMatters`)
//   GET /matters/<n>       -> one matter + clocks + documents (mirrors getMatter)
//   GET /upcoming?days=14  -> clock rows due within window (mirrors upcomingDeadlines)
//   GET /fuse              -> { fuse, wait, parked } (mirrors getFuseBoard)
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

const BUCKET = "litigation-documents";
const HEX64 = /^[0-9a-fA-F]{64}$/;

const json = (data, status = 200) =>
  new Response(JSON.stringify(data), {
    status,
    headers: { "content-type": "application/json; charset=utf-8" },
  });

const keyForSha256 = (sha) => `sha256/${sha.slice(0, 2)}/${sha.slice(2)}.pdf`;
const utcToday = () => new Date().toISOString().slice(0, 10);
const addDays = (key, n) => {
  const d = new Date(`${key}T12:00:00Z`);
  d.setUTCDate(d.getUTCDate() + n);
  return d.toISOString().slice(0, 10);
};

// --- R2 -----------------------------------------------------------------

function r2Ready(env) {
  return !!env.DOCS;
}

async function serveDoc(env, sha) {
  if (!r2Ready(env)) return json({ error: "r2_not_bound" }, 503);
  const clean = sha.toLowerCase();
  if (!HEX64.test(clean)) return json({ error: "sha256 must be 64 hex chars" }, 400);
  const obj = await env.DOCS.get(keyForSha256(clean));
  if (!obj) return json({ error: "not_found", sha256: clean }, 404);
  const headers = new Headers();
  headers.set("content-type", "application/pdf");
  if (obj.httpEtag) headers.set("etag", obj.httpEtag);
  if (obj.size != null) headers.set("content-length", String(obj.size));
  return new Response(obj.body, { headers });
}

async function docMeta(env, sha) {
  if (!r2Ready(env)) return json({ error: "r2_not_bound" }, 503);
  const clean = sha.toLowerCase();
  if (!HEX64.test(clean)) return json({ error: "sha256 must be 64 hex chars" }, 400);
  const head = await env.DOCS.head(keyForSha256(clean));
  if (!head) return json({ error: "not_found", sha256: clean }, 404);
  return json({ sha256: clean, size: head.size ?? null, etag: head.httpEtag ?? null });
}

// --- D1 -------------------------------------------------------------------

async function dbAll(env, sql, params = []) {
  if (!env.DB) return null;
  try {
    const res = await env.DB.prepare(sql).bind(...params).all();
    return res.results ?? [];
  } catch (e) {
    // Binding exists but our schema was never applied (e.g. fresh local D1).
    if (/no such table/i.test(e?.message ?? "")) return null;
    throw e;
  }
}

const slimClock = (today, r) => ({
  number: r.number,
  caption: r.caption,
  lifecycle: r.lifecycle,
  overdue: !!r.next_clock_date && r.next_clock_date < today,
  date: r.next_clock_date ?? null,
  kind: null,
  title: r.next_clock_title ?? null,
});

async function listMatters(env) {
  const rows = await dbAll(
    env,
    `SELECT number, caption, case_no, court, phase, lifecycle, status_label,
            judge, next_clock_title, next_clock_date
     FROM matters ORDER BY number`,
  );
  if (!rows) return json({ error: "d1_not_provisioned" }, 503);
  const today = utcToday();
  return json(
    rows.map((r) => ({
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
    })),
  );
}

async function getMatter(env, n) {
  const rows = await dbAll(
    env,
    `SELECT number, caption, case_no, court, phase, lifecycle, status_label,
            judge, next_clock_title, next_clock_date
     FROM matters WHERE number = ?`,
    [n],
  );
  if (!rows) return json({ error: "d1_not_provisioned" }, 503);
  if (!rows.length) return json({ error: "not_found", matter: n }, 404);
  const r = rows[0];
  const today = utcToday();
  const clocks =
    (await dbAll(
      env,
      `SELECT title, date, kind FROM clocks WHERE matter_number = ? ORDER BY date`,
      [n],
    )) ?? [];
  const documents =
    (await dbAll(
      env,
      `SELECT sha256, path, size FROM documents WHERE matter_number = ? ORDER BY path`,
      [n],
    )) ?? [];
  return json({
    number: r.number,
    caption: r.caption,
    case_no: r.case_no,
    court: r.court,
    phase: r.phase,
    lifecycle: r.lifecycle,
    status_label: r.status_label,
    judge: r.judge,
    overdue: r.lifecycle === "active" && !!r.next_clock_date && r.next_clock_date < today,
    next_clock: r.next_clock_date ? { date: r.next_clock_date, title: r.next_clock_title } : null,
    clocks: clocks.map((c) => ({
      title: c.title,
      date: c.date,
      kind: c.kind,
      overdue: !!c.date && c.date < today,
    })),
    documents,
    document_count: documents.length,
  });
}

async function upcoming(env, params) {
  let days = Number(params.get("days") ?? 14);
  if (!Number.isFinite(days)) days = 14;
  days = Math.min(90, Math.max(1, Math.round(days)));
  const today = utcToday();
  const horizon = addDays(today, days);
  const rows = await dbAll(
    env,
    `SELECT c.matter_number AS number, c.title, c.date, c.kind,
            m.caption, m.lifecycle
     FROM clocks c JOIN matters m ON m.number = c.matter_number
     WHERE c.date <= ? ORDER BY c.date, c.matter_number`,
    [horizon],
  );
  if (!rows) return json({ error: "d1_not_provisioned" }, 503);
  return json(
    rows.map((r) => ({
      number: r.number,
      caption: r.caption,
      lifecycle: r.lifecycle,
      overdue: !!r.date && r.date < today,
      date: r.date,
      kind: r.kind,
      title: r.title,
    })),
  );
}

async function fuse(env, params) {
  let days = Number(params.get("days") ?? 14);
  if (!Number.isFinite(days)) days = 14;
  days = Math.min(90, Math.max(1, Math.round(days)));
  const today = utcToday();
  const horizon = addDays(today, days);
  const rows = await dbAll(
    env,
    `SELECT number, caption, lifecycle, next_clock_title, next_clock_date FROM matters`,
  );
  if (!rows) return json({ error: "d1_not_provisioned" }, 503);
  const slim = rows.map((r) => slimClock(today, r));
  const fuseRows = slim
    .filter(
      (m) =>
        m.lifecycle === "active" && m.date && (m.overdue || m.date <= horizon),
    )
    .sort((a, b) => a.date.localeCompare(b.date) || a.number - b.number);
  const inFuse = new Set(fuseRows.map((m) => m.number));
  const wait = slim
    .filter((m) => m.lifecycle === "active" && !inFuse.has(m.number))
    .sort((a, b) => (a.date ?? "9999").localeCompare(b.date ?? "9999") || a.number - b.number);
  const parked = slim
    .filter((m) => m.lifecycle === "pre_filing")
    .sort((a, b) => a.number - b.number);
  return json({ generated: today, today, horizon, fuse: fuseRows, wait, parked });
}

// --- scheduled digests ------------------------------------------------------

function isRollcallCron(cron) {
  const parts = String(cron || "").trim().split(/\s+/);
  return parts[4] === "1" || new Date().getUTCDay() === 1;
}

async function buildDigest(env, cron) {
  const today = utcToday();
  const rows = await dbAll(
    env,
    `SELECT number, caption, lifecycle, status_label, next_clock_title, next_clock_date
     FROM matters ORDER BY number`,
  );
  if (!rows) return { type: "error", generated: today, error: "d1_not_provisioned" };

  if (isRollcallCron(cron)) {
    const live = rows.filter((r) => r.lifecycle === "active" || r.lifecycle === "pre_filing");
    const lines = live.map((r) => {
      const clock = r.next_clock_date ? `next: ${r.next_clock_date} — ${r.next_clock_title}` : "no clock";
      return `#${r.number} ${r.caption} — ${r.lifecycle} — ${clock}`;
    });
    const closed = rows.length - live.length;
    return {
      type: "roll_call",
      generated: today,
      text: [`ROLL CALL ${today} — ${live.length} live matters (${closed} closed/other)`, ...lines].join("\n"),
      matters: live.map((r) => ({
        number: r.number,
        caption: r.caption,
        lifecycle: r.lifecycle,
        next_clock_date: r.next_clock_date,
        next_clock_title: r.next_clock_title,
      })),
    };
  }

  const horizon = addDays(today, 14);
  const fuseRows = rows
    .filter(
      (r) =>
        r.lifecycle === "active" &&
        r.next_clock_date &&
        (r.next_clock_date < today || r.next_clock_date <= horizon),
    )
    .sort((a, b) => a.next_clock_date.localeCompare(b.next_clock_date) || a.number - b.number);
  const lines = fuseRows.map((r) => {
    const flag = r.next_clock_date < today ? "!!OVERDUE" : "!";
    return `${flag} #${r.number} ${r.caption} — ${r.next_clock_date} — ${r.next_clock_title}`;
  });
  return {
    type: "fuse_digest",
    generated: today,
    horizon,
    text: [`FUSE DIGEST ${today} — ${fuseRows.length} live clocks (14d window)`, ...lines].join("\n"),
    clocks: fuseRows.map((r) => ({
      number: r.number,
      caption: r.caption,
      date: r.next_clock_date,
      title: r.next_clock_title,
      overdue: r.next_clock_date < today,
    })),
  };
}

// --- admin: D1 self-reseed --------------------------------------------------
// POST /admin/reseed with `Authorization: Bearer <RESEED_SECRET>` and the
// seed.sql text as the body (one `INSERT ...;` per line, see seed.mjs).
// Applies the statements to the D1 binding in small batches, so the
// `d1-reseed.yml` workflow can keep D1 in sync with the repo after every
// portfolio-data merge. Fail-closed: 503 when RESEED_SECRET is not
// configured on the Worker, 403 on a bearer mismatch.
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
