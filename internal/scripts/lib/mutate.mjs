// Portfolio mutation operations — the Stage 1b write side of the API boundary.
// See internal/docs/API_OPERATIONS.md for the operation catalog.
//
// Every operation validates its invariants BEFORE touching disk and refuses
// with a machine-readable error when they fail. Writes are atomic per file
// (read → validate → write). Nothing here merges or publishes: results land
// on the working tree for review, per the review/merge separation.
//
// Test against a scratch copy:
//   PORTFOLIO_ROOT=/tmp/pf-test node internal/scripts/q.mjs recordTimelineEvent ...
import fs from "node:fs";
import path from "node:path";
import { execFileSync } from "node:child_process";
import { todayKey, dateKeyFromLabel, ACTORS } from "./next-actions.mjs";
import { validateMatter } from "./matter-schema.mjs";
import { loadSplitMatter, paddedMatterNumber } from "./matter-layout.mjs";
import { MATTER_LIFECYCLES } from "../matter-lifecycle.mjs";
import { MATTER_PHASES } from "../matter-proceeding.mjs";
import { keyForSha256 } from "./r2-client.mjs";
import { DEAD_CLOCK_STATUS_SET, OPEN_CLOCK_STATUS_SET, clockStatusIssue } from "./clock-status.mjs";
import { REPO_ROOT } from "./root.mjs";
import { matterByNumber } from "./query.mjs";

const SOURCE_TYPES = new Set(["portfolio", "courtlistener", "pacer", "email", "court_order", "manual"]);

export const WRITE_POLICY =
  "Settlement framing is user-drawn and exact: Matter 27 communications are " +
  "'final demands', AG-office communications are 'offers' — this operation never " +
  "generates settlement language. Never sign anything on the user's behalf. " +
  "Operations propose; only the user merges.";

const MONTH_ABBR = ["Jan.", "Feb.", "Mar.", "Apr.", "May", "Jun.", "Jul.", "Aug.", "Sep.", "Oct.", "Nov.", "Dec."];

const readJSON = (rel) => JSON.parse(fs.readFileSync(path.join(REPO_ROOT, rel), "utf8"));
const writeJSON = (rel, obj) =>
  fs.writeFileSync(path.join(REPO_ROOT, rel), `${JSON.stringify(obj, null, 2)}\n`);

const fail = (message, detail) => {
  const error = new Error(message);
  if (detail !== undefined) error.detail = detail;
  throw error;
};

/** Accept "2026-09-18" or "Sep. 18, 2026" → { key, label }. */
function parseDateInput(value) {
  if (/^\d{4}-\d{2}-\d{2}$/.test(value ?? "")) {
    const d = new Date(`${value}T12:00:00Z`);
    if (Number.isNaN(d.getTime()) || d.toISOString().slice(0, 10) !== value) {
      fail(`unparseable date: ${value}`);
    }
    const [y, m, day] = value.split("-").map(Number);
    return { key: value, label: `${MONTH_ABBR[m - 1]} ${day}, ${y}` };
  }
  const key = dateKeyFromLabel(value);
  if (!key) fail(`unparseable date (want YYYY-MM-DD or "Sep. 18, 2026"): ${value}`);
  return { key, label: String(value).trim() };
}

function splitDirRel(n) {
  return `internal/src/data/matters/${paddedMatterNumber(n)}`;
}

function matterFileRel(n) {
  const m = matterByNumber(n);
  if (!m) fail(`no matter ${n} in index`);
  return m.layout === "split" ? `${splitDirRel(n)}/matter.json` : m.path;
}

function bumpLastUpdated(n) {
  const rel = matterFileRel(n);
  const data = readJSON(rel);
  data.last_updated = todayKey();
  writeJSON(rel, data);
}

const splitRows = (n) =>
  fs
    .readFileSync(path.join(REPO_ROOT, `${splitDirRel(n)}/events.jsonl`), "utf8")
    .split("\n")
    .filter(Boolean)
    .map((line) => JSON.parse(line));

const retiredKeys = (rows) =>
  new Set(
    rows
      .filter((e) => e.type === "retire" && e.supersedes_ts && e.supersedes_title)
      .map((e) => JSON.stringify([e.supersedes_ts, e.supersedes_title])),
  );

// --- Writes --------------------------------------------------------------

/** Append a timeline event. Routes per matter: split → events.jsonl,
 *  legacy → timeline.json. upcoming:true requires a source; duplicates
 *  (date, type, matters) are refused — the #826 rule, now structural. */
export function recordTimelineEvent({
  date,
  type,
  actor = "unknown",
  matters,
  title,
  source,
  source_type,
  upcoming = false,
  filed,
} = {}) {
  if (!title || !String(title).trim()) fail("title is required");
  if (!type || !String(type).trim()) fail("type is required");
  if (!Array.isArray(matters) || !matters.length) fail("matters must be a non-empty array");
  if (!ACTORS.includes(actor)) fail(`actor must be one of ${ACTORS.join(", ")}`);
  const { key, label } = parseDateInput(date);
  if (upcoming && !(source && String(source).trim())) {
    fail("upcoming:true requires a source (source PDF, docket, or filing reference)");
  }
  // Mirror validate-portfolio: an upcoming event's source must be a
  // /documents/ path present in the manifest, so the fuse is verifiable.
  if (upcoming) {
    const src = String(source).trim();
    if (!src.startsWith("/documents/")) {
      fail(`upcoming event source must be a "/documents/..." path (got "${src}")`);
    }
    const manifestPaths = new Set(
      readJSON("internal/src/data/documents/manifest.json").files.map((f) => f.path),
    );
    if (!manifestPaths.has(src)) {
      fail(`upcoming event source not in the document manifest: ${src}`);
    }
  }
  if (source_type !== undefined && !SOURCE_TYPES.has(source_type)) {
    fail(`source_type must be one of ${[...SOURCE_TYPES].join(", ")}`);
  }
  const nums = matters.map(Number);
  for (const n of nums) matterByNumber(n) ?? fail(`no matter ${n} in index`);

  const created = [];
  const splitNums = nums.filter((n) => matterByNumber(n).layout === "split");
  const legacyNums = nums.filter((n) => matterByNumber(n).layout !== "split");

  for (const n of splitNums) {
    const rows = splitRows(n);
    const retired = retiredKeys(rows);
    const dup = rows.some(
      (e) =>
        e.type !== "retire" &&
        e.ts?.slice(0, 10) === key &&
        e.type === type &&
        !retired.has(JSON.stringify([e.ts, e.title])),
    );
    if (dup) fail(`duplicate event refused: matter ${n} already has a live ${type} on ${key}`);
    const row = {
      ts: `${key}T00:00:00-07:00`,
      matter: n,
      type,
      title,
      actor,
      upcoming: !!upcoming,
      ...(source ? { source } : {}),
      ...(source_type ? { source_type } : {}),
    };
    fs.appendFileSync(
      path.join(REPO_ROOT, `${splitDirRel(n)}/events.jsonl`),
      `${JSON.stringify(row)}\n`,
    );
    created.push({ store: "events.jsonl", matter: n, event: row });
  }

  if (legacyNums.length) {
    const tl = readJSON("internal/src/data/timeline.json");
    const dup = tl.some(
      (e) =>
        e.upcoming === !!upcoming &&
        dateKeyFromLabel(e.date) === key &&
        e.type === type &&
        JSON.stringify([...(e.matters ?? [])].sort()) === JSON.stringify([...legacyNums].sort()),
    );
    if (dup) {
      fail(
        `duplicate event refused: matters [${legacyNums}] already have a live ${type} on ${key}`,
      );
    }
    const event = {
      date: label,
      event: title,
      matters: legacyNums,
      type,
      upcoming: !!upcoming,
      filed: filed ?? !upcoming,
      actor,
      ...(source ? { source } : {}),
      ...(source_type ? { source_type } : {}),
    };
    tl.push(event);
    writeJSON("internal/src/data/timeline.json", tl);
    created.push({ store: "timeline.json", matters: legacyNums, event });
  }

  for (const n of nums) bumpLastUpdated(n);
  return { ok: true, policy: WRITE_POLICY, created };
}

/** Retire a live upcoming clock. Split matters get an append-only tombstone;
 *  legacy timeline.json flips the event in place (never deletes). */
export function retireUpcomingEvent({ matter, date, reason } = {}) {
  const n = Number(matter);
  matterByNumber(n) ?? fail(`no matter ${n} in index`);
  if (!reason || !String(reason).trim()) fail("reason is required");
  const { key } = parseDateInput(date);
  const m = matterByNumber(n);

  if (m.layout === "split") {
    const rows = splitRows(n);
    const retired = retiredKeys(rows);
    const live = rows.filter(
      (e) =>
        e.type !== "retire" &&
        e.upcoming === true &&
        e.ts?.slice(0, 10) === key &&
        !retired.has(JSON.stringify([e.ts, e.title])),
    );
    if (!live.length) fail(`no live upcoming event on ${key} for matter ${n}`);
    if (live.length > 1) {
      fail(`ambiguous: ${live.length} live upcoming events on ${key} for matter ${n}`, {
        candidates: live.map((e) => ({ ts: e.ts, type: e.type, title: e.title })),
      });
    }
    const orig = live[0];
    const tombstone = {
      ts: `${todayKey()}T00:00:00-07:00`,
      matter: n,
      type: "retire",
      title: `Retired: ${orig.title}`,
      actor: "you",
      upcoming: false,
      supersedes_ts: orig.ts,
      supersedes_title: orig.title,
      reason,
    };
    fs.appendFileSync(
      path.join(REPO_ROOT, `${splitDirRel(n)}/events.jsonl`),
      `${JSON.stringify(tombstone)}\n`,
    );
    const clockRel = `${splitDirRel(n)}/clocks.json`;
    const clocks = readJSON(clockRel);
    const liveOnDay = clocks.filter(
      (c) => c.date === key && !DEAD_CLOCK_STATUS_SET.has(c.status),
    );
    let matched = liveOnDay;
    if (liveOnDay.length > 1) {
      matched = liveOnDay.filter((c) =>
        orig.title.startsWith(String(c.title ?? "").replace(/…$/, "").trim()),
      );
    }
    if (matched.length === 1) {
      matched[0].status = "satisfied";
      matched[0].retired_reason = reason;
      writeJSON(clockRel, clocks);
    }
    bumpLastUpdated(n);
    return { ok: true, policy: WRITE_POLICY, retired: { matter: n, ts: orig.ts, title: orig.title, reason } };
  }

  const tl = readJSON("internal/src/data/timeline.json");
  const live = tl.filter(
    (e) => e.upcoming === true && (e.matters ?? []).includes(n) && dateKeyFromLabel(e.date) === key,
  );
  if (!live.length) fail(`no live upcoming event on ${key} for matter ${n}`);
  if (live.length > 1) {
    fail(`ambiguous: ${live.length} live upcoming events on ${key} for matter ${n}`, {
      candidates: live.map((e) => ({ date: e.date, type: e.type, event: e.event })),
    });
  }
  const orig = live[0];
  orig.upcoming = false;
  orig.retired_reason = reason;
  orig.retired_date = todayKey();
  writeJSON("internal/src/data/timeline.json", tl);
  bumpLastUpdated(n);
  return { ok: true, policy: WRITE_POLICY, retired: { matter: n, date: orig.date, event: orig.event, reason } };
}

const LIVE_CLOCK = OPEN_CLOCK_STATUS_SET;

/** Set (or replace by id) a matter's next clock. Split matters write
 *  clocks.json; legacy matters delegate to recordTimelineEvent — the event
 *  IS the clock. One live clock per kind: a same-kind live clock must be
 *  named in `supersedes` or the write is refused. */
export function setNextClock({
  matter,
  id,
  date,
  kind,
  title,
  status = "open",
  source_dkt,
  source,
  time,
  tz = "America/Los_Angeles",
  supersedes,
} = {}) {
  const n = Number(matter);
  const m = matterByNumber(n) ?? fail(`no matter ${n} in index`);
  if (!id || !String(id).trim()) fail("id is required");
  if (!kind || !String(kind).trim()) fail("kind is required");
  if (!title || !String(title).trim()) fail("title is required");
  const statusIssue = clockStatusIssue(status, "setNextClock");
  if (statusIssue) fail(statusIssue);
  const { key } = parseDateInput(date);

  if (m.layout !== "split") {
    const src = source ?? (source_dkt !== undefined ? `Dkt. ${source_dkt}` : undefined);
    if (!src) fail("legacy matters need a source (or source_dkt) — the event is the clock");
    return recordTimelineEvent({
      date: key,
      type: kind,
      actor: "you",
      matters: [n],
      title,
      source: src,
      upcoming: true,
    });
  }

  const rel = `${splitDirRel(n)}/clocks.json`;
  const clocks = readJSON(rel);
  const idx = clocks.findIndex((c) => c.id === id);
  const clock = {
    id,
    date: key,
    ...(time ? { time } : {}),
    tz,
    kind,
    status,
    ...(source_dkt !== undefined ? { source_dkt } : {}),
    ...(source ? { source } : {}),
    title,
    actor: "you",
  };
  if (idx >= 0) {
    clocks[idx] = clock;
  } else {
    if (LIVE_CLOCK.has(status)) {
      const conflict = clocks.find(
        (c) => c.id !== id && c.kind === kind && LIVE_CLOCK.has(c.status),
      );
      if (conflict) {
        if (supersedes === conflict.id) {
          conflict.status = "vacated";
          conflict.superseded_by = id;
        } else {
          fail(
            `live ${kind} clock "${conflict.id}" already open for matter ${n} — pass supersedes:"${conflict.id}" to replace it`,
            { conflict },
          );
        }
      }
    }
    clocks.push(clock);
  }
  writeJSON(rel, clocks);
  bumpLastUpdated(n);
  return { ok: true, policy: WRITE_POLICY, clock };
}

/** Validate a would-be identity file the way CI does: legacy flat files
 *  against the matter schema directly; split matters against the assembled
 *  record (identity + sibling files). */
function validateIdentityWrite(num, layout, identityData) {
  if (layout === "split") {
    const dir = path.join(REPO_ROOT, "internal/src/data/matters", String(num).padStart(2, "0"));
    const merged = { ...loadSplitMatter(dir), ...identityData };
    const issues = validateMatter(merged);
    if (issues.length) fail(`assembled matter ${num} would fail schema validation`, { issues });
  } else {
    const issues = validateMatter(identityData);
    if (issues.length) fail(`schema validation failed for matter ${num}`, { issues });
  }
}
/** Patch a matter's identity record. Validated the way CI validates it:
 *  legacy flat files against the matter schema; split matters against the
 *  assembled record (identity + sibling files), plus the identity file's
 *  80-line / 8KB budget. Refuses identity-key changes. */
export function updateMatterIdentity({ n, patch } = {}) {
  const num = Number(n);
  const m = matterByNumber(num) ?? fail(`no matter ${num} in index`);
  if (!patch || typeof patch !== "object" || Array.isArray(patch)) fail("patch must be an object");
  if ("number" in patch) fail("refusing to change matter number");
  // The schema only checks types; the lifecycle enum lives in the lifecycle
  // module, so check it here where the value actually changes.
  if ("lifecycle" in patch && !MATTER_LIFECYCLES.includes(patch.lifecycle)) {
    fail(`invalid lifecycle "${patch.lifecycle}" — must be one of ${MATTER_LIFECYCLES.join(", ")}`);
  }
  if ("phase" in patch && !MATTER_PHASES.includes(patch.phase)) {
    fail(`invalid phase "${patch.phase}" — must be one of ${MATTER_PHASES.join(", ")}`);
  }
  const rel = matterFileRel(num);
  const data = readJSON(rel);
  const applied = { ...data, ...patch, last_updated: todayKey() };
  validateIdentityWrite(num, m.layout, applied);

  const serialized = `${JSON.stringify(applied, null, 2)}\n`;
  if (m.layout === "split") {
    if (serialized.length > 8192) fail(`matter ${num} would exceed the 8KB identity cap`);
    if (serialized.split("\n").length > 80) fail(`matter ${num} would exceed the 80-line identity cap`);
  }
  fs.writeFileSync(path.join(REPO_ROOT, rel), serialized);
  return { ok: true, policy: WRITE_POLICY, patched: Object.keys(patch) };
}

/** Catalog one document across all three stores — manifest, registry, and
 *  the matter's documents[] — or none. The R2 key is derived from the
 *  sha256, never supplied. (The #762 invariant, now structural.)
 *  Same path + new sha256 replaces the row (a redraft), so the Worker
 *  path index can move `/documents/...` to the new object. */
export function catalogDocument({
  matter,
  path: docPath,
  sha256,
  size,
  label,
  matterLabel,
  filed = false,
} = {}) {
  const n = Number(matter);
  matterByNumber(n) ?? fail(`no matter ${n} in index`);
  if (!docPath?.startsWith("/documents/")) fail('path must start with "/documents/"');
  if (!/^[0-9a-f]{64}$/i.test(sha256 ?? "")) fail("sha256 must be 64 hex chars");
  if (!Number.isInteger(size) || size <= 0) fail("size must be a positive integer");
  if (!label || !String(label).trim()) fail("label (registry canonical) is required");
  if (matterLabel !== undefined && matterLabel === label) {
    fail("matter label override must differ from the registry canonical label (or omit it)");
  }
  const r2Key = keyForSha256(sha256.toLowerCase());
  const layout = matterByNumber(n).layout;

  const manifest = readJSON("internal/src/data/documents/manifest.json");
  const hash = sha256.toLowerCase();
  const pathHit = manifest.files.find((f) => f.path === docPath);
  if (pathHit) {
    pathHit.size = size;
    pathHit.sha256 = hash;
  } else {
    manifest.files.push({ path: docPath, size, sha256: hash });
  }
  manifest.fileCount = manifest.files.length;
  manifest.totalBytes = manifest.files.reduce((s, f) => s + f.size, 0);
  const registry = readJSON("internal/src/data/documents/registry.json");
  const regHit = registry.documents.find((d) => d.path === docPath);
  if (regHit) {
    regHit.label = label;
    regHit.ownerMatter = n;
  } else {
    registry.documents.push({ path: docPath, label, ownerMatter: n });
  }

  const matEntry = { path: docPath, filed: !!filed };
  if (matterLabel !== undefined) matEntry.label = matterLabel;

  // Split matters keep inventory in documents.json (identity cap on matter.json).
  // Legacy flat files still store documents[] on the matter record.
  if (layout === "split") {
    const docsRel = `${splitDirRel(n)}/documents.json`;
    const docs = fs.existsSync(path.join(REPO_ROOT, docsRel)) ? readJSON(docsRel) : [];
    if (!Array.isArray(docs)) fail(`matter ${n} documents.json must be an array`);
    const matHit = docs.find((d) => d.path === docPath);
    if (matHit) Object.assign(matHit, matEntry);
    else docs.push(matEntry);
    writeJSON("internal/src/data/documents/manifest.json", manifest);
    writeJSON("internal/src/data/documents/registry.json", registry);
    writeJSON(docsRel, docs);
    bumpLastUpdated(n);
    validateIdentityWrite(n, layout, readJSON(matterFileRel(n)));
  } else {
    const rel = matterFileRel(n);
    const data = readJSON(rel);
    data.documents ??= [];
    const matHit = data.documents.find((d) => d.path === docPath);
    if (matHit) Object.assign(matHit, matEntry);
    else data.documents.push(matEntry);
    data.last_updated = todayKey();
    validateIdentityWrite(n, layout, data);
    writeJSON("internal/src/data/documents/manifest.json", manifest);
    writeJSON("internal/src/data/documents/registry.json", registry);
    writeJSON(rel, data);
  }
  return { ok: true, policy: WRITE_POLICY, r2Key, path: docPath };
}

/** Scaffold a new matter via the existing script. Always targets the real
 *  repo (the script resolves its own root) — refused under PORTFOLIO_ROOT
 *  so tests can't accidentally scaffold into production. */
export function scaffoldMatter({ n, caption } = {}) {
  if (process.env.PORTFOLIO_ROOT) fail("scaffoldMatter is disabled under PORTFOLIO_ROOT");
  const num = Number(n);
  if (!Number.isInteger(num) || num <= 0) fail("n must be a positive integer");
  if (matterByNumber(num)) fail(`matter ${num} already exists`);
  if (!caption || !String(caption).trim()) fail("caption is required");
  const out = execFileSync(
    "node",
    [path.join(REPO_ROOT, "internal/scripts/scaffold-matter.mjs"), String(num), caption],
    { cwd: REPO_ROOT, encoding: "utf8" },
  );
  return { ok: true, policy: WRITE_POLICY, n: num, output: out.trim() };
}

/** Split a legacy matter via the existing script. Same PORTFOLIO_ROOT guard. */
export function splitMatter({ n } = {}) {
  if (process.env.PORTFOLIO_ROOT) fail("splitMatter is disabled under PORTFOLIO_ROOT");
  const num = Number(n);
  const m = matterByNumber(num) ?? fail(`no matter ${num} in index`);
  if (m.layout === "split") fail(`matter ${num} is already split`);
  const out = execFileSync(
    "node",
    [path.join(REPO_ROOT, "internal/scripts/split-matter.mjs"), String(num)],
    { cwd: REPO_ROOT, encoding: "utf8" },
  );
  return { ok: true, policy: WRITE_POLICY, n: num, output: out.trim() };
}
