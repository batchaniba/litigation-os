import { describe, expect, it } from "vitest";
import summaries from "./matters/summaries.json";

/** Must match STATUS_LABEL_MAX in internal/scripts/validate-portfolio.mjs. */
const STATUS_LABEL_MAX = 60;

describe("status_label", () => {
  it("is present and non-empty on every matter", () => {
    for (const matter of summaries) {
      expect(typeof matter.status_label, `matter ${matter.number}`).toBe("string");
      expect(matter.status_label.trim(), `matter ${matter.number}`).not.toBe("");
    }
  });

  it("stays inside the width the badge and strip can render", () => {
    for (const matter of summaries) {
      expect(matter.status_label.length, `matter ${matter.number}: ${matter.status_label}`).toBeLessThanOrEqual(
        STATUS_LABEL_MAX,
      );
    }
  });

  it("is a single line", () => {
    for (const matter of summaries) {
      expect(matter.status_label, `matter ${matter.number}`).not.toMatch(/\n/);
    }
  });

  it("renders whole in the badge — nothing hits the backstop truncation", () => {
    // StatusBadge shares STATUS_LABEL_MAX, so a conforming label is never
    // clipped. Clipped badges were the failure this split was meant to end.
    const overflowing = summaries.filter((m) => m.status_label.length > STATUS_LABEL_MAX);
    expect(
      overflowing.map((m) => `${m.number}: ${m.status_label} (${m.status_label.length})`),
    ).toEqual([]);
  });

  it("does not simply restate the full narrative", () => {
    for (const matter of summaries) {
      expect(matter.status_label, `matter ${matter.number}`).not.toBe(matter.status);
    }
  });
});
