// Write data layer for the litigation-doc-api Worker: the C / U / D half of
// CRUD over R2 (document bytes) and D1 (matters, clocks, document manifest).
// Read ops live in data.mjs; these are kept separate so the mutating surface
// is easy to review and audit in one place.
//
// Every function returns plain data and throws HttpError (400/404/503) on
// mapped failures, exactly like data.mjs. No transport handling here. R2 and
// D1 are reached through the DOCS / DB bindings — no keys in this repo.

import { HttpError, HEX64, keyForSha256 } from "./data.mjs";

const LIFECYCLES = ["active", "pre_filing", "dismissed", "abandoned", "closed", "settled"];
// Columns a caller may set/patch on a matter. `number` is the key, set
// separately; everything else is here. Anything outside this list is rejected
// so a write can never touch an unknown/again-computed column.
const MATTER_COLS = [
  "caption",
  "case_no",
  "court",
  "phase",
  "status_label",
  "judge",
  "next_clock_title",
  "next_clock_date",
  "lifecycle",
];

const DATE_RE = /^\d{4}-\d{2}-\d{2}$/;

function cleanSha(sha) {
  const c = String(sha ?? "").toLowerCase();
  if (!HEX64.test(c)) throw new HttpError(400, { error: "sha256 must be 64 hex chars" });
  return c;
}

function needDb(env) {
  if (!env.DB) throw new HttpError(503, { error: "d1_not_provisioned" });
}

// D1 matters/clocks are a projection of main, rebuilt by every reseed. A
// direct write never reaches the repo and is erased by the next reseed, so it
// only creates a second, disagreeing calendar. Off unless the Worker sets
// ALLOW_DIRECT_D1_WRITES = "true".
export const DIRECT_D1_WRITE_TOOLS = new Set(["upsertMatter", "updateMatter", "addClock"]);

export function directD1WritesAllowed(env) {
  return env?.ALLOW_DIRECT_D1_WRITES === "true";
}

function needDirectD1Writes(env) {
  if (!directD1WritesAllowed(env))
    throw new HttpError(403, {
      error: "d1_writes_disabled",
      hint: "D1 is a read-only projection of main. Change matter.json / clocks.json in a pull request.",
    });
}

function needR2(env) {
  if (!env.DOCS) throw new HttpError(503, { error: "r2_not_bound" });
}

async function sha256HexBytes(bytes) {
  const buf = await crypto.subtle.digest("SHA-256", bytes);
  return [...new Uint8Array(buf)].map((b) => b.toString(16).padStart(2, "0")).join("");
}

function asMatterNumber(n) {
  const num = typeof n === "string" ? Number(n.trim()) : n;
  if (!Number.isInteger(num) || num < 1)
    throw new HttpError(400, { error: "matter number must be a positive integer" });
  return num;
}

// --- documents: bytes (R2) --------------------------------------------------

// Store bytes at sha256/<first2>/<rest>.pdf. By default the content hash is
// verified against the key, so the store can never disagree with its own
// addressing. Returns { sha256, size }.
export async function putDocBytes(env, sha, bytes, { verify = true, contentType } = {}) {
  needR2(env);
  const clean = cleanSha(sha);
  const buf = bytes instanceof ArrayBuffer ? bytes : bytes?.buffer ? bytes.buffer : null;
  if (!buf || buf.byteLength === 0)
    throw new HttpError(400, { error: "empty body: expected PDF bytes" });
  if (verify) {
    const actual = await sha256HexBytes(buf);
    if (actual !== clean)
      throw new HttpError(400, { error: "sha256 mismatch", expected: clean, actual });
  }
  await env.DOCS.put(keyForSha256(clean), buf, {
    httpMetadata: { contentType: contentType || "application/pdf" },
  });
  return { sha256: clean, size: buf.byteLength };
}

// --- documents: manifest row (D1) -------------------------------------------

export async function upsertDocumentRow(env, { sha256, matter_number, path, size }) {
  needDb(env);
  const clean = cleanSha(sha256);
  const mn = matter_number == null ? null : asMatterNumber(matter_number);
  const p = path == null ? null : String(path);
  const sz = size == null ? null : Number(size);
  if (sz != null && !Number.isFinite(sz))
    throw new HttpError(400, { error: "size must be a number" });
  await env.DB.prepare(
    `INSERT INTO documents (sha256, matter_number, path, size)
     VALUES (?, ?, ?, ?)
     ON CONFLICT(sha256) DO UPDATE SET
       matter_number = excluded.matter_number,
       path = excluded.path,
       size = excluded.size`,
  )
    .bind(clean, mn, p, sz)
    .run();
  return { sha256: clean, matter_number: mn, path: p, size: sz };
}

// --- matters (D1) -----------------------------------------------------------

function validateMatterFields(fields, { partial }) {
  const out = {};
  for (const [k, v] of Object.entries(fields ?? {})) {
    if (k === "number") continue;
    if (!MATTER_COLS.includes(k))
      throw new HttpError(400, { error: `unknown matter field: ${k}` });
    if (k === "lifecycle" && v != null && !LIFECYCLES.includes(v))
      throw new HttpError(400, { error: `lifecycle must be one of ${LIFECYCLES.join(", ")}` });
    if (k === "next_clock_date" && v != null && v !== "" && !DATE_RE.test(String(v)))
      throw new HttpError(400, { error: "next_clock_date must be YYYY-MM-DD" });
    out[k] = v === "" ? null : v;
  }
  if (partial && Object.keys(out).length === 0)
    throw new HttpError(400, { error: "no updatable fields provided" });
  return out;
}

// Create or fully replace a matter row (upsert on `number`).
export async function upsertMatter(env, matter) {
  needDirectD1Writes(env);
  needDb(env);
  const number = asMatterNumber(matter?.number);
  const fields = validateMatterFields(matter, { partial: false });
  const cols = ["number", ...MATTER_COLS];
  const values = [number, ...MATTER_COLS.map((c) => (c in fields ? fields[c] : null))];
  await env.DB.prepare(
    `INSERT INTO matters (${cols.join(", ")})
     VALUES (${cols.map(() => "?").join(", ")})
     ON CONFLICT(number) DO UPDATE SET
       ${MATTER_COLS.map((c) => `${c} = excluded.${c}`).join(", ")}`,
  )
    .bind(...values)
    .run();
  return { number, ...fields };
}

// Patch only the provided columns on an existing matter (e.g. correcting a
// stale status_label). Throws 404 if the matter does not exist.
export async function patchMatter(env, n, patch) {
  needDirectD1Writes(env);
  needDb(env);
  const number = asMatterNumber(n);
  const fields = validateMatterFields(patch, { partial: true });
  const exists = await env.DB.prepare(`SELECT number FROM matters WHERE number = ?`)
    .bind(number)
    .first();
  if (!exists) throw new HttpError(404, { error: "not_found", matter: number });
  const cols = Object.keys(fields);
  await env.DB.prepare(`UPDATE matters SET ${cols.map((c) => `${c} = ?`).join(", ")} WHERE number = ?`)
    .bind(...cols.map((c) => fields[c]), number)
    .run();
  return { number, updated: cols };
}

// --- clocks (D1) ------------------------------------------------------------

export async function addClock(env, { matter_number, title, date, kind }) {
  needDirectD1Writes(env);
  needDb(env);
  const mn = asMatterNumber(matter_number);
  if (!title || typeof title !== "string")
    throw new HttpError(400, { error: "title is required" });
  if (date != null && date !== "" && !DATE_RE.test(String(date)))
    throw new HttpError(400, { error: "date must be YYYY-MM-DD" });
  await env.DB.prepare(`INSERT INTO clocks (matter_number, title, date, kind) VALUES (?, ?, ?, ?)`)
    .bind(mn, title, date || null, kind || null)
    .run();
  return { matter_number: mn, title, date: date || null, kind: kind || null };
}

// --- audit (D1, best-effort) ------------------------------------------------
// Records every mutation. Never throws into the caller: an audit-table that
// isn't provisioned must not break a write, but a configured store gets a
// durable who/what/when trail.
export async function recordAudit(env, { actor, action, target, detail, ok }) {
  if (!env.DB) return;
  try {
    await env.DB.prepare(
      `INSERT INTO audit (ts, actor, action, target, detail, ok) VALUES (?, ?, ?, ?, ?, ?)`,
    )
      .bind(
        new Date().toISOString(),
        String(actor ?? "anon"),
        String(action ?? ""),
        target == null ? null : String(target),
        detail == null ? null : (typeof detail === "string" ? detail : JSON.stringify(detail)),
        ok ? 1 : 0,
      )
      .run();
  } catch (e) {
    if (!/no such table/i.test(e?.message ?? "")) console.log("audit_write_failed", e?.message);
  }
}
