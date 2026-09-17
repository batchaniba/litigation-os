// Portfolio query operations — the Stage 1 read side of the API boundary.
// See internal/docs/API_OPERATIONS.md for the full operation catalog.
//
// These are pure reads against the JSON source of truth. They export
// functions; `internal/scripts/q.mjs` is the CLI dispatcher (`npm run q`).
// Legacy generator scripts stay untouched — this lib is the contract layer
// they will eventually be refactored to import from.
import fs from "node:fs";
import path from "node:path";
import { createHash } from "node:crypto";
import { todayKey, dateKeyFromLabel } from "./next-actions.mjs";
import { paddedMatterNumber } from "./matter-layout.mjs";
import { getObject, keyForSha256 } from "./r2-client.mjs";
import { REPO_ROOT } from "./root.mjs";
const readJSON = (rel) => JSON.parse(fs.readFileSync(path.join(REPO_ROOT, rel), "utf8"));

let _index = null;
let _timeline = null;
let _manifest = null;
let _clusters = null;

const index = () => (_index ??= readJSON("internal/src/data/index/matters.json"));
const timeline = () => (_timeline ??= readJSON("internal/src/data/timeline.json"));
const manifest = () => (_manifest ??= readJSON("internal/src/data/documents/manifest.json"));
const clusters = () => (_clusters ??= readJSON("internal/src/data/index/clusters.json"));

export const allMatters = () => index().matters ?? [];
export const matterByNumber = (n) => allMatters().find((m) => m.number === Number(n)) ?? null;

const slimClock = (m) => ({
  number: m.number,
  caption: m.caption,
  lifecycle: m.lifecycle,
  overdue: !!m.overdue,
  date: m.next_clock?.date ?? null,
  kind: m.next_clock?.kind ?? null,
  title: m.next_clock?.title ?? null,
});

const addDays = (key, n) => {
  const d = new Date(`${key}T12:00:00Z`);
  d.setUTCDate(d.getUTCDate() + n);
  return d.toISOString().slice(0, 10);
};

const byDate = (a, b) => {
  if (!!a.overdue !== !!b.overdue) return a.overdue ? -1 : 1;
  const da = a.next_clock?.date ?? a.date ?? "9999-99-99";
  const db = b.next_clock?.date ?? b.date ?? "9999-99-99";
  return da.localeCompare(db) || a.number - b.number;
};

// --- Reads ---------------------------------------------------------------

/** Identity + index entry for one matter. */
export function getMatter(n) {
  const m = matterByNumber(n);
  if (!m) throw new Error(`no matter ${n} in index`);
  return m;
}

/** Index entries, optionally filtered. */
export function listMatters({ lifecycle, phase, cluster } = {}) {
  return allMatters().filter(
    (m) =>
      (!lifecycle || m.lifecycle === lifecycle) &&
      (!phase || m.phase === phase) &&
      (cluster === undefined || m.cluster === Number(cluster)),
  );
}

/** Live clocks due within `days` (or overdue), ranked. Reads index next_clock:
 *  clocks.json wins for split matters, timeline for legacy — already folded. */
export function upcomingDeadlines({ days = 14, matter } = {}) {
  const horizon = addDays(todayKey(), Number(days));
  return allMatters()
    .filter((m) => m.next_clock?.date)
    .filter((m) => !matter || m.number === Number(matter))
    .filter((m) => m.overdue || m.next_clock.date <= horizon)
    .sort(byDate)
    .map(slimClock);
}

/** Events, newest first. Split matters read events.jsonl; legacy read
 *  timeline.json filtered by matter. `since` is YYYY-MM-DD. */
export function getTimeline({ matter, since, upcomingOnly = false, limit = 200 } = {}) {
  let events;
  const n = matter === undefined ? null : Number(matter);
  if (n !== null) {
    const m = matterByNumber(n);
    if (!m) throw new Error(`no matter ${n} in index`);
    if (m.layout === "split") {
      const p = path.join(
        REPO_ROOT,
        `internal/src/data/matters/${paddedMatterNumber(n)}/events.jsonl`,
      );
      const rows = fs
        .readFileSync(p, "utf8")
        .split("\n")
        .filter(Boolean)
        .map((line) => JSON.parse(line));
      // Retire tombstones (appended by retireUpcomingEvent) hide the events
      // they supersede. The log stays append-only; the read view filters.
      const retireKey = (ts, title) => JSON.stringify([ts, title]);
      const retired = new Set(
        rows
          .filter((e) => e.type === "retire" && e.supersedes_ts && e.supersedes_title)
          .map((e) => retireKey(e.supersedes_ts, e.supersedes_title)),
      );
      events = rows
        .filter((e) => e.type !== "retire")
        .filter((e) => !retired.has(retireKey(e.ts, e.title)))
        .map((e) => ({ date: e.ts?.slice(0, 10) ?? null, ...e }));
    } else {
      events = timeline().filter((e) => (e.matters ?? []).includes(n));
    }
  } else {
    events = timeline();
  }
  const keyOf = (e) => {
    if (e.dateKey) return e.dateKey;
    if (!e.date) return null;
    if (/^\d{4}-\d{2}-\d{2}$/.test(e.date)) return e.date;
    return dateKeyFromLabel(e.date);
  };
  return events
    .filter((e) => !upcomingOnly || e.upcoming === true)
    .filter((e) => !since || (keyOf(e) ?? "0000-00-00") >= since)
    .sort((a, b) => (keyOf(b) ?? "").localeCompare(keyOf(a) ?? ""))
    .slice(0, Number(limit));
}

/** Fuse / Wait / Parked board as structured data (same bucketing as
 *  generate-fuse-board.mjs; the .md file is the rendered view). */
export function getFuseBoard({ days = 14 } = {}) {
  const today = todayKey();
  const horizon = addDays(today, Number(days));
  const ms = allMatters();
  const fuse = ms
    .filter(
      (m) =>
        m.lifecycle === "active" && m.next_clock?.date && (m.overdue || m.next_clock.date <= horizon),
    )
    .sort(byDate)
    .map(slimClock);
  const inFuse = new Set(fuse.map((m) => m.number));
  const wait = ms
    .filter((m) => m.lifecycle === "active" && !inFuse.has(m.number))
    .sort(byDate)
    .map(slimClock);
  const parked = ms
    .filter((m) => m.lifecycle === "pre_filing")
    .sort((a, b) => a.number - b.number)
    .map(slimClock);
  return { generated: today, today, horizon, fuse, wait, parked };
}

/** One PDF from R2 by manifest sha256. Bytes are re-hashed; mismatches throw
 *  and nothing is written. Returns { path, bytes }. */
export async function fetchDocument(sha256, outPath) {
  const key = keyForSha256(sha256);
  const { body } = await getObject(key);
  const actual = createHash("sha256").update(body).digest("hex");
  if (actual !== sha256.toLowerCase()) {
    throw new Error(`refused: R2 object ${key} hashes to ${actual}, not ${sha256}`);
  }
  const dest = outPath || path.join(process.cwd(), `${sha256.toLowerCase()}.pdf`);
  fs.writeFileSync(dest, body);
  return { path: dest, bytes: body.length };
}

/** Full-text search over the .txt sidecars on main (no R2 touch). */
export function searchDocuments(query, { limit = 20 } = {}) {
  const root = path.join(REPO_ROOT, "internal/public/documents");
  const q = query.toLowerCase();
  const hits = [];
  const walk = (dir) => {
    for (const name of fs.readdirSync(dir, { withFileTypes: true })) {
      if (hits.length >= limit * 3) return;
      const p = path.join(dir, name.name);
      if (name.isDirectory()) walk(p);
      else if (name.name.endsWith(".txt")) {
        const lines = fs.readFileSync(p, "utf8").split("\n");
        lines.forEach((line, i) => {
          if (line.toLowerCase().includes(q) && hits.length < limit * 3) {
            hits.push({ file: path.relative(REPO_ROOT, p), line: i + 1, text: line.slice(0, 200) });
          }
        });
      }
    }
  };
  if (fs.existsSync(root)) walk(root);
  return hits.slice(0, Number(limit));
}

const slugify = (s) =>
  s.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");

function readDossier(kind, name) {
  const dir = path.join(REPO_ROOT, `internal/docs/legal-intel/${kind}`);
  const slug = slugify(name);
  for (const ext of [".md", ".json"]) {
    const p = path.join(dir, `${slug}${ext}`);
    if (fs.existsSync(p)) return { found: true, path: path.relative(REPO_ROOT, p), body: fs.readFileSync(p, "utf8") };
  }
  const available = fs.existsSync(dir)
    ? fs.readdirSync(dir).filter((f) => f.endsWith(".md")).map((f) => f.replace(/\.md$/, ""))
    : [];
  return { found: false, available };
}

/** Opposing-counsel dossier by name (fuzzy slug match). */
export function getCounselDossier(name) {
  return readDossier("counsel", name);
}

/** Judge dossier by name (fuzzy slug match). */
export function getJudgeDossier(name) {
  return readDossier("judges", name);
}

/** Cluster map. */
export function getClusters() {
  return clusters();
}

/** Manifest entries for one matter's documents. */
export function getMatterDocs(n) {
  const num = Number(n);
  return (manifest().files ?? []).filter((f) => f.path.includes(`/matter-${num}/`));
}
