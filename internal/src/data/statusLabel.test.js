import { describe, expect, it } from "vitest";
import summaries from "./matters/summaries.json";
import { STATUS_LABEL_MAX, effectiveStatusLabel } from "../utils/statusLabel";
import { eventsForMatter } from "../utils/matterTimeline";

describe("status_label overrides + effective labels", () => {
  it("keeps hand overrides inside the width cap when present", () => {
    for (const matter of summaries) {
      if (!matter.status_label) continue;
      expect(matter.status_label.length, `matter ${matter.number}: ${matter.status_label}`).toBeLessThanOrEqual(
        STATUS_LABEL_MAX,
      );
      expect(matter.status_label, `matter ${matter.number}`).not.toMatch(/\n/);
      expect(matter.status_label.trim(), `matter ${matter.number}`).not.toBe("");
    }
  });

  it("produces an effective label for every matter", () => {
    for (const matter of summaries) {
      const label = effectiveStatusLabel(matter, { events: eventsForMatter(matter.number) });
      expect(label.trim(), `matter ${matter.number}`).not.toBe("");
      expect(label.length, `matter ${matter.number}: ${label}`).toBeLessThanOrEqual(STATUS_LABEL_MAX);
    }
  });
});
