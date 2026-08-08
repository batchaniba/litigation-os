/**
 * Length budgets for the free-prose matter fields.
 *
 * `status_label` has had a hard 60-char cap since it went in; the long-form
 * prose fields never got one, and drifted — the portfolio median is ~280–420
 * words with outliers past 1,600. These budgets close that gap.
 *
 * Two levels, deliberately:
 *   target  — the length the field should be written to. Exceeding it is a
 *             validator warning, not an error: trimming legal prose is an
 *             editorial decision, not something a build should force.
 *   ceiling — a ratchet pinned just above today's worst record. Exceeding it
 *             fails the test suite, so prose can only get shorter over time.
 *
 * When you trim a matter, lower the ceiling to match the new worst case.
 *
 * Dated docket entries do not belong in `procedural_status` — they belong in
 * timeline.json, which already carries them (297 events across 33 matters) and
 * feeds the derived status labels. Prose that restates the timeline is the
 * single largest source of length here.
 */

export interface ProseBudget {
  /** Authoring target, in words. Over this is a warning. */
  target: number;
  /** Hard ratchet, in words. Over this fails tests. */
  ceiling: number;
}

export const PROSE_BUDGETS = {
  key_facts: { target: 350, ceiling: 1650 },
  procedural_status: { target: 400, ceiling: 1750 },
  risk: { target: 150, ceiling: 660 },
  status: { target: 60, ceiling: 1300 },
} satisfies Record<string, ProseBudget>;

export type ProseField = keyof typeof PROSE_BUDGETS;

export const PROSE_FIELDS = Object.keys(PROSE_BUDGETS) as ProseField[];

/** What to do about an over-budget field, per field. */
export const PROSE_HINTS: Record<ProseField, string> = {
  key_facts: "keep to the operative facts; dated docket entries belong in timeline.json",
  procedural_status: "move dated docket entries into timeline.json — it already carries them",
  risk: "keep to the defense theory and its answer; drop the procedural recap",
  status: "one posture sentence; the detail belongs in procedural_status",
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
