// Shared prose-length budgets for Node scripts (validate-portfolio).
// Keep in sync with internal/src/utils/proseBudget.ts — proseBudget.test.js
// asserts the two agree.

export const PROSE_BUDGETS = {
  key_facts: { target: 350, ceiling: 1650 },
  procedural_status: { target: 400, ceiling: 1750 },
  risk: { target: 150, ceiling: 660 },
  status: { target: 60, ceiling: 1300 },
};

export const PROSE_FIELDS = Object.keys(PROSE_BUDGETS);

export const PROSE_HINTS = {
  key_facts: "keep to the operative facts; dated docket entries belong in timeline.json",
  procedural_status: "move dated docket entries into timeline.json — it already carries them",
  risk: "keep to the defense theory and its answer; drop the procedural recap",
  status: "one posture sentence; the detail belongs in procedural_status",
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
