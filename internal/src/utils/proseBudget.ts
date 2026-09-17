/**
 * Length budgets for the free-prose matter fields on **legacy** NN.json files.
 *
 * Split matters (`NN/matter.json` plus sibling tables) are not under these
 * word ceilings. Their fetch budget is `MATTER_JSON_BUDGET` on the identity
 * file. `events.jsonl` and `docket.json` have no line cap.
 *
 * `status_label` remains a hard 60-char UI chip on every matter.
 *
 * Two levels on legacy prose, deliberately:
 *   target  — authoring length. Exceeding it is a validator warning.
 *   ceiling — ratchet pinned just above today's worst unsplit record.
 *
 * When you trim a matter, lower the ceiling to match the new worst case.
 *
 * Dated docket entries do not belong in `procedural_status` / `status` — they
 * belong in timeline.json, which already carries them and feeds derived status
 * labels. Prose that restates the timeline is the single largest source of
 * length here. `docketLogIssues` warns when status/procedural_status still
 * look like a docket log (caps heads, SERVED/COMPUTED markers, dense dates).
 */

export interface ProseBudget {
  /** Authoring target, in words. Over this is a warning. */
  target: number;
  /** Hard ratchet, in words. Over this fails tests. */
  ceiling: number;
}

export const PROSE_BUDGETS = {
  key_facts: { target: 350, ceiling: 1650 },
  // Ratcheted down after round-2 docket-log trim (Matters 3/5–8/12/20/24/28/30).
  procedural_status: { target: 400, ceiling: 650 },
  risk: { target: 150, ceiling: 660 },
  status: { target: 60, ceiling: 100 },
} satisfies Record<string, ProseBudget>;

export type ProseField = keyof typeof PROSE_BUDGETS;

export const PROSE_FIELDS = Object.keys(PROSE_BUDGETS) as ProseField[];

/** What to do about an over-budget field, per field. */
export const PROSE_HINTS: Record<ProseField, string> = {
  key_facts: "keep to the operative facts; dated docket entries belong in timeline.json or clocks.json",
  procedural_status: "move dated docket entries into clocks.json / timeline.json — split the matter if this field is a diary",
  risk: "keep to the defense theory and its answer; drop the procedural recap",
  status: "one posture sentence; the detail belongs in clocks.json / timeline.json",
};

export function wordCount(value: unknown): number {
  if (typeof value !== "string") return 0;
  return value.trim().split(/\s+/).filter(Boolean).length;
}

export interface ProseBudgetIssue {
  field: ProseField;
  words: number;
  target: number;
  ceiling: number;
  level: "over-target" | "over-ceiling";
}

/** Every prose field on `matter` that breaches its target or ceiling. */
export function proseBudgetIssues(matter: Record<string, unknown>): ProseBudgetIssue[] {
  const issues: ProseBudgetIssue[] = [];
  for (const field of PROSE_FIELDS) {
    const { target, ceiling } = PROSE_BUDGETS[field];
    const words = wordCount(matter[field]);
    if (words > ceiling) issues.push({ field, words, target, ceiling, level: "over-ceiling" });
    else if (words > target) issues.push({ field, words, target, ceiling, level: "over-target" });
  }
  return issues;
}

const DOCKET_FIELDS = ["status", "procedural_status"] as const;

const DATE_RE =
  /\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:t(?:ember)?)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\.?\s+\d{1,2},?\s+\d{4}\b/gi;

const MARKER_RE =
  /\b(?:SERVED|COMPUTED|FILING|CLOSING OUT|PROOF OF SERVICE|PUNITIVE AMOUNT REVISED|SERVICE CONFIRMED|SERVICE SUBMITTED|ACTION ITEM|FALLBACK|BOTH DEFENDANTS NOW SERVED)\b/g;

const CAPS_HEAD_RE = /\b[A-Z][A-Z0-9 /§().-]{3,}(?:\s*[—–-]\s*|\s*:\s*)/g;

const PIPE_DATE_RE =
  /\|\s*(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+\d{1,2}/gi;

export interface DocketLogSignals {
  score: number;
  hits: string[];
  dates: number;
  markers: number;
  capsHeads: number;
  pipeDates: number;
}

/** Heuristic signals that prose is functioning as a docket log. */
export function docketLogSignals(text: unknown): DocketLogSignals {
  if (typeof text !== "string" || !text.trim()) {
    return { score: 0, hits: [], dates: 0, markers: 0, capsHeads: 0, pipeDates: 0 };
  }
  const dates = (text.match(DATE_RE) || []).length;
  const markers = (text.match(MARKER_RE) || []).length;
  const capsHeads = (text.match(CAPS_HEAD_RE) || []).length;
  const pipeDates = (text.match(PIPE_DATE_RE) || []).length;
  const words = wordCount(text);
  const hits: string[] = [];
  if (markers >= 2) hits.push(`markers:${markers}`);
  if (capsHeads >= 3) hits.push(`caps-heads:${capsHeads}`);
  if (words >= 80 && dates >= 5) hits.push(`dates:${dates}`);
  if (pipeDates >= 2) hits.push(`pipe-dates:${pipeDates}`);
  return { score: hits.length, hits, dates, markers, capsHeads, pipeDates };
}

export interface DocketLogIssue {
  field: (typeof DOCKET_FIELDS)[number];
  words: number;
  score: number;
  hits: string[];
}

/**
 * Warn-level issues when status / procedural_status still look like a docket
 * log. Advisory only — legal nuance sometimes needs dates.
 */
export function docketLogIssues(matter: Record<string, unknown>): DocketLogIssue[] {
  const issues: DocketLogIssue[] = [];
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
