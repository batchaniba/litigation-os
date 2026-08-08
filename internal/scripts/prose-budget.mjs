// Shared prose-length budgets for Node scripts (validate-portfolio).
// Keep in sync with internal/src/utils/proseBudget.ts — proseBudget.test.js
// asserts the two agree.

export const PROSE_BUDGETS = {
  key_facts: { target: 350, ceiling: 1650 },
  // Ratcheted down after Matter 22/25/26/27/29 docket-log trim (Aug 2026).
  procedural_status: { target: 400, ceiling: 1640 },
  risk: { target: 150, ceiling: 660 },
  status: { target: 60, ceiling: 290 },
};

export const PROSE_FIELDS = Object.keys(PROSE_BUDGETS);

export const PROSE_HINTS = {
  key_facts: "keep to the operative facts; dated docket entries belong in timeline.json",
  procedural_status: "move dated docket entries into timeline.json — it already carries them",
  risk: "keep to the defense theory and its answer; drop the procedural recap",
  status: "one posture sentence; the detail belongs in procedural_status / timeline.json",
};

export function wordCount(value) {
  if (typeof value !== "string") return 0;
  return value.trim().split(/\s+/).filter(Boolean).length;
}

export function proseBudgetIssues(matter) {
  const issues = [];
  for (const field of PROSE_FIELDS) {
    const { target, ceiling } = PROSE_BUDGETS[field];
    const words = wordCount(matter[field]);
    if (words > ceiling) issues.push({ field, words, target, ceiling, level: "over-ceiling" });
    else if (words > target) issues.push({ field, words, target, ceiling, level: "over-target" });
  }
  return issues;
}

const DOCKET_FIELDS = ["status", "procedural_status"];

const DATE_RE =
  /\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:t(?:ember)?)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\.?\s+\d{1,2},?\s+\d{4}\b/gi;

const MARKER_RE =
  /\b(?:SERVED|COMPUTED|FILING|CLOSING OUT|PROOF OF SERVICE|PUNITIVE AMOUNT REVISED|SERVICE CONFIRMED|SERVICE SUBMITTED|ACTION ITEM|FALLBACK|BOTH DEFENDANTS NOW SERVED)\b/g;

const CAPS_HEAD_RE = /\b[A-Z][A-Z0-9 /§().-]{3,}(?:\s*[—–-]\s*|\s*:\s*)/g;

const PIPE_DATE_RE =
  /\|\s*(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+\d{1,2}/gi;

export function docketLogSignals(text) {
  if (typeof text !== "string" || !text.trim()) {
    return { score: 0, hits: [], dates: 0, markers: 0, capsHeads: 0, pipeDates: 0 };
  }
  const dates = (text.match(DATE_RE) || []).length;
  const markers = (text.match(MARKER_RE) || []).length;
  const capsHeads = (text.match(CAPS_HEAD_RE) || []).length;
  const pipeDates = (text.match(PIPE_DATE_RE) || []).length;
  const words = wordCount(text);
  const hits = [];
  if (markers >= 2) hits.push(`markers:${markers}`);
  if (capsHeads >= 3) hits.push(`caps-heads:${capsHeads}`);
  if (words >= 80 && dates >= 5) hits.push(`dates:${dates}`);
  if (pipeDates >= 2) hits.push(`pipe-dates:${pipeDates}`);
  return { score: hits.length, hits, dates, markers, capsHeads, pipeDates };
}

export function docketLogIssues(matter) {
  const issues = [];
  for (const field of DOCKET_FIELDS) {
    const signals = docketLogSignals(matter[field]);
    if (signals.score >= 2) {
      issues.push({
        field,
        words: wordCount(matter[field]),
        score: signals.score,
        hits: signals.hits,
      });
    }
  }
  return issues;
}
