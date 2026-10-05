// Daily deadline digest, computed from clocks.json on `main`.
//
// Replaces the doc-api digest, which read one `next_clock` per matter out of
// the D1 publish projection. That mirror is only refreshed by a manual
// reseed, so it drifted (missing live deadlines, showing vacated ones), and
// the projection drops every clock that is not court-facing, including
// statute-of-limitations backstops. This reads the system of record instead:
// every clock on every matter, at the current head of `main`, with the commit
// stamped on the message.
//
// Fail-loud: if `main` cannot be read, the digest still goes out and says so.
// A day with nothing due still sends a message, so silence means the digest
// itself is broken.

import {
  isClosedClockStatus,
  OPEN_CLOCK_STATUS_SET,
} from "../../../internal/scripts/lib/clock-status.mjs";

export const DIGEST_TZ = "America/Los_Angeles";
export const WINDOW_DAYS = 14;
export const HORIZON_DAYS = 60;
const TITLE_MAX = 110;
const CLOCKS_PATH_RE = /^internal\/src\/data\/matters\/(\d{2})\/clocks\.json$/;
const INDEX_PATH = "internal/src/data/index/matters.json";
const DATE_RE = /^\d{4}-\d{2}-\d{2}$/;

/** YYYY-MM-DD and weekday for `now` in Pacific time. */
export function pacificDay(now) {
  const date = new Intl.DateTimeFormat("en-CA", {
    timeZone: DIGEST_TZ,
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
  }).format(now);
  const weekday = new Intl.DateTimeFormat("en-US", { timeZone: DIGEST_TZ, weekday: "short" }).format(now);
  return { date, weekday };
}

function dayNumber(dateKey) {
  const [y, m, d] = dateKey.split("-").map(Number);
  return Date.UTC(y, m - 1, d) / 86_400_000;
}

export function daysBetween(from, to) {
  return dayNumber(to) - dayNumber(from);
}

function shortDate(dateKey) {
  const [y, m, d] = dateKey.split("-").map(Number);
  const month = new Date(Date.UTC(y, m - 1, d)).toLocaleString("en-US", { month: "short", timeZone: "UTC" });
  return `${month} ${d}`;
}

function actorLabel(actor) {
  if (actor === "you") return "YOU";
  if (actor === "opposing") return "opp";
  if (actor === "court" || actor === "agency") return "court";
  return actor ? String(actor) : "—";
}

function clip(text, max = TITLE_MAX) {
  const s = String(text ?? "").replace(/\s+/g, " ").trim();
  return s.length > max ? `${s.slice(0, max - 1)}…` : s;
}

/** Normalize clocks.json (array or { clocks: [] }) into flat rows. */
export function clockRows(matterNumber, raw) {
  const list = Array.isArray(raw) ? raw : Array.isArray(raw?.clocks) ? raw.clocks : [];
  return list
    .filter((c) => c && typeof c === "object")
    .map((c) => ({
      matter: matterNumber,
      id: c.id ?? null,
      date: typeof c.date === "string" && DATE_RE.test(c.date) ? c.date : null,
      status: c.status ?? "open",
      kind: c.kind ?? "deadline",
      actor: c.actor ?? null,
      title: c.title ?? "",
      private: c.private === true,
    }));
}

function line(row, today) {
  const delta = daysBetween(today, row.date);
  const when =
    delta < 0 ? `${-delta}d ago` : delta === 0 ? "TODAY" : delta === 1 ? "tomorrow" : `${delta}d`;
  const title = row.private
    ? "Private clock — see the repo"
    : clip(
        row.status === "contingent" && !/^contingent\b/i.test(row.title)
          ? `(contingent) ${row.title}`
          : row.title,
      );
  return `${shortDate(row.date)} (${when}) · M${row.matter} · ${actorLabel(row.actor)} · ${title}`;
}

function publicRow(row, today) {
  return {
    matter: row.matter,
    id: row.id,
    date: row.date,
    days: daysBetween(today, row.date),
    status: row.status,
    kind: row.kind,
    actor: row.actor,
    title: row.private ? null : row.title,
    private: row.private,
  };
}

const byDate = (a, b) => a.date.localeCompare(b.date) || a.matter - b.matter;

/**
 * Pure digest builder.
 * @param {object} args
 * @param {Array} args.rows       flat clock rows (clockRows)
 * @param {string} args.today     YYYY-MM-DD, Pacific
 * @param {string} args.weekday   "Mon" … "Sun", Pacific
 * @param {{ sha: string, committedAt?: string|null }} args.source
 * @param {Record<number,string>} [args.captions]
 */
export function buildDigest({ rows, today, weekday, source, captions = {} }) {
  const live = rows.filter((r) => r.date && !isClosedClockStatus(r.status));
  const needsDisposition = live
    .filter((r) => r.date < today && OPEN_CLOCK_STATUS_SET.has(r.status))
    .sort(byDate);
  const window = live
    .filter((r) => r.date >= today && daysBetween(today, r.date) <= WINDOW_DAYS)
    .sort(byDate);
  const monday = weekday === "Mon";
  const horizon = monday
    ? live
        .filter((r) => {
          const d = daysBetween(today, r.date);
          return d > WINDOW_DAYS && d <= HORIZON_DAYS;
        })
        .sort(byDate)
    : [];
  const undated = rows.filter((r) => !r.date && !isClosedClockStatus(r.status)).length;

  const sha7 = String(source.sha || "").slice(0, 7);
  const committed = source.committedAt ? `, committed ${String(source.committedAt).slice(0, 10)}` : "";
  const text = [
    `DEADLINES ${weekday} ${today} (PT) — main @ ${sha7}${committed}`,
    `${needsDisposition.length} need disposition · ${window.length} in next ${WINDOW_DAYS} days`,
  ];
  if (needsDisposition.length) {
    text.push("", "NEEDS DISPOSITION — date passed, still open (mark satisfied, vacated, or missed)");
    for (const r of needsDisposition) text.push(`  ${line(r, today)}`);
  }
  text.push("", `NEXT ${WINDOW_DAYS} DAYS`);
  if (window.length) {
    for (const r of window) text.push(`  ${line(r, today)}`);
  } else {
    text.push("  Nothing dated in the window.");
  }
  if (monday) {
    text.push("", `HORIZON — ${WINDOW_DAYS + 1} to ${HORIZON_DAYS} days`);
    if (horizon.length) for (const r of horizon) text.push(`  ${line(r, today)}`);
    else text.push("  Nothing dated in the horizon.");
  }
  if (undated) text.push("", `${undated} live clock(s) have no date.`);

  const matters = [...new Set([...needsDisposition, ...window, ...horizon].map((r) => r.matter))]
    .sort((a, b) => a - b)
    .map((n) => ({ number: n, caption: captions[n] ?? null }));

  return {
    type: "deadline_digest",
    generated: today,
    source: { ref: "main", sha: source.sha, committed_at: source.committedAt ?? null },
    text: text.join("\n"),
    needs_disposition: needsDisposition.map((r) => publicRow(r, today)),
    clocks: window.map((r) => publicRow(r, today)),
    horizon: horizon.map((r) => publicRow(r, today)),
    matters,
  };
}

/** Message sent when `main` could not be read. Never silent. */
export function digestFailure({ today, weekday, error }) {
  const reason = String(error?.message || error || "unknown error").slice(0, 300);
  return {
    type: "deadline_digest_error",
    generated: today,
    error: reason,
    text: [
      `DEADLINE DIGEST FAILED ${weekday} ${today} (PT)`,
      "Could not read clocks.json from main. Today's deadlines were NOT checked.",
      "Check the calendar directly (npm run next, or the whats-next skill).",
      `Reason: ${reason}`,
    ].join("\n"),
  };
}

/**
 * Read every matter's clocks.json (and captions) at the head of `main`.
 * @param {ReturnType<import("./github.mjs").createGitHubClient>} github
 */
export async function loadMainClocks(github) {
  const head = await github.getBranchHead("main");
  const tree = await github.getTree(head.sha);
  const paths = tree
    .map((entry) => entry.path)
    .filter((p) => CLOCKS_PATH_RE.test(p))
    .sort();
  if (paths.length === 0) throw new Error(`no matters/NN/clocks.json found at ${head.sha.slice(0, 12)}`);

  const rows = [];
  for (const p of paths) {
    const matter = Number(CLOCKS_PATH_RE.exec(p)[1]);
    const text = await github.getFileText(p, head.sha);
    let raw;
    try {
      raw = JSON.parse(text);
    } catch {
      throw new Error(`${p} is not valid JSON at ${head.sha.slice(0, 12)}`);
    }
    rows.push(...clockRows(matter, raw));
  }

  const captions = {};
  try {
    const index = JSON.parse(await github.getFileText(INDEX_PATH, head.sha));
    for (const m of index?.matters ?? []) {
      if (Number.isInteger(m?.number)) captions[m.number] = m.caption ?? null;
    }
  } catch {
    // Captions are decoration; the clock rows above are what matter.
  }

  return { sha: head.sha, committedAt: head.committedAt, rows, captions, files: paths.length };
}

/** Build today's digest from `main`, or a failure notice. Never throws. */
export async function composeDigest({ github, now }) {
  const { date: today, weekday } = pacificDay(now);
  try {
    const loaded = await loadMainClocks(github);
    return buildDigest({
      rows: loaded.rows,
      today,
      weekday,
      source: { sha: loaded.sha, committedAt: loaded.committedAt },
      captions: loaded.captions,
    });
  } catch (error) {
    return digestFailure({ today, weekday, error });
  }
}

/** POST to ALERT_WEBHOOK; without one, the digest only reaches Worker logs. */
export async function deliverDigest(env, payload, fetchImpl = fetch) {
  if (!env.ALERT_WEBHOOK) {
    console.log(JSON.stringify({ alert_webhook: "unset", ...payload }));
    return { delivered: false, reason: "ALERT_WEBHOOK unset" };
  }
  const res = await fetchImpl(env.ALERT_WEBHOOK, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    console.log(`digest delivery failed: HTTP ${res.status}`);
    return { delivered: false, reason: `HTTP ${res.status}` };
  }
  return { delivered: true };
}
