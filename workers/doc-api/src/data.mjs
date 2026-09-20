import { documentsKeyFromUrl, sha256ForPath } from "./documents.mjs";
import { CLOSED_CLOCK_SQL, isClosedClockStatus } from "../../../internal/scripts/lib/clock-status.mjs";

// Shared data layer for the litigation-doc-api Worker: R2 + D1 access and
// the portfolio query operations. Used by the REST routes (index.mjs) and
// the MCP endpoint (mcp.mjs).
//
// No request/response handling here — functions return plain data and throw
// HttpError on HTTP-mapped failures (400/404/503). Callers translate those
// into their own transport (REST JSON or MCP JSON-RPC errors).
//
// R2 is reached through the DOCS *binding* and D1 through the DB *binding* —
// this file contains no keys, tokens, or secrets.

export const BUCKET = "litigation-documents";
export const HEX64 = /^[0-9a-fA-F]{64}$/;

export class HttpError extends Error {
  constructor(status, body) {
    super(body && body.error ? String(body.error) : `http_${status}`);
    this.status = status;
    this.body = body;
  }
}

export const keyForSha256 = (sha) => `sha256/${sha.slice(0, 2)}/${sha.slice(2)}.pdf`;
export const keyForSha256Text = (sha) => {
  const c = String(sha ?? "").toLowerCase();
  return `text/${c.slice(0, 2)}/${c.slice(2)}.txt`;
};
export const utcToday = () => new Date().toISOString().slice(0, 10);
export const addDays = (key, n) => {
  const d = new Date(`${key}T12:00:00Z`);
  d.setUTCDate(d.getUTCDate() + n);
  return d.toISOString().slice(0, 10);
};

// Clamp a day-window parameter the same way the REST routes always have.
export function parseDays(value, fallback = 14) {
  let days = Number(value ?? fallback);
  if (!Number.isFinite(days)) days = fallback;
  return Math.min(90, Math.max(1, Math.round(days)));
}

// Clock statuses that no longer count as "upcoming". Canonical stored list is
// open | set | contingent | vacated | satisfied (clock-status.mjs). SQL also
// excludes unmigrated retired/cancelled/canceled aliases (treated as vacated).
// The D1 clocks table may predate the status column — every query that filters
// on it falls back to the unfiltered form when the column is absent.
const isClosedStatus = isClosedClockStatus;
const noStatusColumn = (e) => /no such column/i.test(e?.message ?? "");

function cleanSha(sha) {
  const c = String(sha ?? "").toLowerCase();
  if (!HEX64.test(c)) throw new HttpError(400, { error: "sha256 must be 64 hex chars" });
  return c;
}

// --- R2 ---------------------------------------------------------------------

export function r2Ready(env) {
  return !!env.DOCS;
}

// Resolves to { sha256, obj } where obj is the R2 object (has .body,
// .httpEtag, .size). Throws 503 when unbound, 400 on a bad hash, 404 when
// the key is absent.
export async function getDocObject(env, sha) {
  if (!r2Ready(env)) throw new HttpError(503, { error: "r2_not_bound" });
  const clean = cleanSha(sha);
  const obj = await env.DOCS.get(keyForSha256(clean));
  if (!obj) throw new HttpError(404, { error: "not_found", sha256: clean });
  return { sha256: clean, obj };
}

export async function headDocObject(env, sha) {
  if (!r2Ready(env)) throw new HttpError(503, { error: "r2_not_bound" });
  const clean = cleanSha(sha);
  const head = await env.DOCS.head(keyForSha256(clean));
  if (!head) throw new HttpError(404, { error: "not_found", sha256: clean });
  return { sha256: clean, size: head.size ?? null, etag: head.httpEtag ?? null };
}

// Reads the pre-extracted text sidecar for one PDF: text/<first2>/<rest>.txt
// (poppler `pdftotext -layout`, written by internal/scripts/extract-doc-text.mjs
// and kept in sync by internal/scripts/r2-upload.mjs; an empty file means the
// PDF had no text layer). Returns a paginated slice so agents read document
// contents as tool results instead of fetching PDF bytes over HTTP.
// Throws 503 when unbound, 400 on a bad hash, 404 when no sidecar exists yet.
export async function getDocText(env, sha, offset = 0, limit = 20000) {
  if (!r2Ready(env)) throw new HttpError(503, { error: "r2_not_bound" });
  const clean = cleanSha(sha);
  const obj = await env.DOCS.get(keyForSha256Text(clean));
  if (!obj) throw new HttpError(404, { error: "text_not_extracted", sha256: clean });
  const text = await obj.text();
  const total = text.length;
  const start = Math.min(Math.max(0, Math.trunc(Number(offset) || 0)), total);
  const len = Math.min(Math.max(1, Math.trunc(Number(limit) || 20000)), 100000);
  const slice = text.slice(start, start + len);
  return {
    sha256: clean,
    total_chars: total,
    offset: start,
    limit: len,
    returned_chars: slice.length,
    truncated: start + slice.length < total,
    text: slice,
  };
}

// --- D1 ---------------------------------------------------------------------

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

// Null (no DB / no schema) becomes the standard 503; callers get rows.
function needDb(rows) {
  if (!rows) throw new HttpError(503, { error: "d1_not_provisioned" });
  return rows;
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

const slimMatter = (today, r) => ({
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
});

// Mirrors `npm run q listMatters`.
export async function listMattersData(env) {
  const rows = needDb(
    await dbAll(
      env,
      `SELECT number, caption, case_no, court, phase, lifecycle, status_label,
              judge, next_clock_title, next_clock_date
       FROM matters ORDER BY number`,
    ),
  );
  const today = utcToday();
  return rows.map((r) => slimMatter(today, r));
}

// Mirrors getMatter: identity + clocks + document manifest rows.
// Throws 404 when the matter number is unknown.
export async function getMatterData(env, n) {
  const rows = needDb(
    await dbAll(
      env,
      `SELECT number, caption, case_no, court, phase, lifecycle, status_label,
              judge, next_clock_title, next_clock_date
       FROM matters WHERE number = ?`,
      [n],
    ),
  );
  if (!rows.length) throw new HttpError(404, { error: "not_found", matter: n });
  const r = rows[0];
  const today = utcToday();
  let clocks;
  try {
    clocks =
      (await dbAll(
        env,
        `SELECT title, date, kind, status FROM clocks WHERE matter_number = ? ORDER BY date`,
        [n],
      )) ?? [];
  } catch (e) {
    if (!noStatusColumn(e)) throw e;
    clocks =
      (await dbAll(
        env,
        `SELECT title, date, kind FROM clocks WHERE matter_number = ? ORDER BY date`,
        [n],
      )) ?? [];
  }
  const documents =
    (await dbAll(
      env,
      `SELECT sha256, path, size FROM documents WHERE matter_number = ? ORDER BY path`,
      [n],
    )) ?? [];
  return {
    ...slimMatter(today, r),
    clocks: clocks.map((c) => ({
      title: c.title,
      date: c.date,
      kind: c.kind,
      status: c.status ?? null,
      overdue: !!c.date && c.date < today && !isClosedStatus(c.status),
    })),
    documents,
    document_count: documents.length,
  };
}

// Mirrors upcomingDeadlines: clock rows due within the window (days, clamped
// 1..90), oldest first, including overdue ones.
export async function upcomingData(env, days) {
  const window = parseDays(days);
  const today = utcToday();
  const horizon = addDays(today, window);
  let rows;
  try {
    rows = await dbAll(
      env,
      `SELECT c.matter_number AS number, c.title, c.date, c.kind,
              m.caption, m.lifecycle
       FROM clocks c JOIN matters m ON m.number = c.matter_number
       WHERE c.date <= ?
         AND lower(ifnull(c.status, 'open')) NOT IN ${CLOSED_CLOCK_SQL}
       ORDER BY c.date, c.matter_number`,
      [horizon],
    );
  } catch (e) {
    if (!noStatusColumn(e)) throw e;
    rows = await dbAll(
      env,
      `SELECT c.matter_number AS number, c.title, c.date, c.kind,
              m.caption, m.lifecycle
       FROM clocks c JOIN matters m ON m.number = c.matter_number
       WHERE c.date <= ? ORDER BY c.date, c.matter_number`,
      [horizon],
    );
  }
  rows = needDb(rows);
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

export const PATH_INDEX_KEY = "index/path-to-sha256.json";

// Path -> sha256 for GET /documents/<path>: the R2 path index first, then the
// D1 documents_by_path table (path is the identity — one sha256 can live
// under many court paths), then the legacy sha256-PK documents table.
// Throws 404 { error: "not_found", path } when nothing has the path.
export async function sha256ForDocumentPath(env, pathname) {
  const docPath = documentsKeyFromUrl(pathname);
  if (r2Ready(env)) {
    try {
      const obj = await env.DOCS.get(PATH_INDEX_KEY);
      const sha = sha256ForPath(obj ? await obj.json().catch(() => null) : null, pathname);
      if (sha) return { sha256: sha, path: docPath };
    } catch {
      // fall through to D1
    }
  }
  if (env.DB) {
    const byPath = await dbAll(env, `SELECT sha256 FROM documents_by_path WHERE path = ?`, [docPath]);
    let hit = byPath?.[0]?.sha256;
    if (!hit) {
      const legacy = await dbAll(env, `SELECT sha256 FROM documents WHERE path = ?`, [docPath]);
      hit = legacy?.[0]?.sha256;
    }
    if (typeof hit === "string" && hit) return { sha256: hit.toLowerCase(), path: docPath };
  }
  throw new HttpError(404, { error: "not_found", path: docPath });
}

// Mirrors getFuseBoard: { fuse, wait, parked } partitioned off the folded
// next_clock, exactly like the REST /fuse route.
export async function fuseData(env, days) {
  const window = parseDays(days);
  const today = utcToday();
  const horizon = addDays(today, window);
  const rows = needDb(
    await dbAll(
      env,
      `SELECT number, caption, lifecycle, next_clock_title, next_clock_date FROM matters`,
    ),
  );
  const slim = rows.map((r) => slimClock(today, r));
  const fuseRows = slim
    .filter((m) => m.lifecycle === "active" && m.date && (m.overdue || m.date <= horizon))
    .sort((a, b) => a.date.localeCompare(b.date) || a.number - b.number);
  const inFuse = new Set(fuseRows.map((m) => m.number));
  const wait = slim
    .filter((m) => m.lifecycle === "active" && !inFuse.has(m.number))
    .sort(
      (a, b) => (a.date ?? "9999").localeCompare(b.date ?? "9999") || a.number - b.number,
    );
  const parked = slim
    .filter((m) => m.lifecycle === "pre_filing")
    .sort((a, b) => a.number - b.number);
  return { generated: today, today, horizon, fuse: fuseRows, wait, parked };
}

// Escape LIKE metacharacters so the query is a literal substring match.
const escapeLike = (s) => String(s).replace(/[\\%_]/g, (c) => `\\${c}`);

// Substring search over document manifest paths and matter captions.
// D1 holds no .txt sidecar text, so this matches filenames/labels and
// captions — the same rows getMatterData returns, ranked by path.
export async function searchDocumentsData(env, query, limit = 20) {
  const q = String(query ?? "").trim();
  if (!q) throw new HttpError(400, { error: "query must be a non-empty string" });
  let n = Number(limit ?? 20);
  if (!Number.isFinite(n)) n = 20;
  n = Math.min(100, Math.max(1, Math.round(n)));
  const like = `%${escapeLike(q)}%`;
  const rows = needDb(
    await dbAll(
      env,
      `SELECT d.sha256, d.matter_number, d.path, d.size, m.caption
       FROM documents d LEFT JOIN matters m ON m.number = d.matter_number
       WHERE d.path LIKE ? ESCAPE '\\' OR m.caption LIKE ? ESCAPE '\\'
       ORDER BY d.path LIMIT ?`,
      [like, like, n],
    ),
  );
  return rows.map((r) => ({
    sha256: r.sha256,
    matter_number: r.matter_number,
    matter_caption: r.caption,
    path: r.path,
    size: r.size,
  }));
}

// --- scheduled digests ------------------------------------------------------
// Computed from D1 with zero dependencies. POSTed to ALERT_WEBHOOK when set,
// otherwise logged.

function isRollcallCron(cron) {
  const parts = String(cron || "").trim().split(/\s+/);
  return parts[4] === "1" || new Date().getUTCDay() === 1;
}

export async function buildDigest(env, cron) {
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
