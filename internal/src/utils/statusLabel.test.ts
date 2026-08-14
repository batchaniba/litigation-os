import { describe, expect, it } from "vitest";
import { cases } from "../data/matters";
import { timeline } from "../data/timeline";
import {
  STATUS_LABEL_MAX,
  clampStatusLabel,
  deriveStatusLabel,
  effectiveStatusLabel,
  pickPostureEvent,
  postureEventScore,
} from "./statusLabel";
import type { TimelineEvent } from "../types/portfolio";
import { matterRefsInclude } from "./matterRefs.js";
import { parseEventDatePDT } from "./dateUtils";

function eventsFor(matterNumber: number): TimelineEvent[] {
  return timeline.filter((event) => matterRefsInclude(event.matters, matterNumber));
}

describe("statusLabel derivation", () => {
  it("clamps long labels without breaking mid-word when possible", () => {
    const long = "A".repeat(70);
    expect(clampStatusLabel(long).length).toBeLessThanOrEqual(STATUS_LABEL_MAX);
    expect(clampStatusLabel("Short label")).toBe("Short label");
  });

  it("prefers demurrer hearings over earlier reply deadlines", () => {
    const matter = cases.find((item) => item.number === 20)!;
    const events = eventsFor(20);
    const posture = pickPostureEvent(events, matter.phase);
    expect(posture?.date).toBe("Aug. 28, 2026");
    expect(deriveStatusLabel(matter, { events })).toContain("Aug. 28, 2026");
    expect(deriveStatusLabel(matter, { events })).toMatch(/Demurrer hearing/i);
  });

  it("derives default prove-up and CMC dates from upcoming hearings", () => {
    const proveUpHearing: TimelineEvent = {
      date: "Aug. 12, 2026",
      event:
        "Default prove-up hearing (CMC converted per clerk phone statement) — Ngwa Nforbi v. Diamond Truck Sales, Inc. et al. (STK-CV-UF-2026-0001094)",
      type: "hearing",
      matters: [12],
      upcoming: true,
    };
    expect(
      deriveStatusLabel(cases.find((item) => item.number === 12)!, {
        events: [proveUpHearing],
        now: +parseEventDatePDT("Aug. 10, 2026"),
      }),
    ).toBe("Default prove-up — Aug. 12, 2026");
    expect(deriveStatusLabel(cases.find((item) => item.number === 24)!, { events: eventsFor(24) })).toContain(
      "CMC Sep. 15, 2026",
    );
  });

  it("pairs served milestones with later CMC / response deadlines", () => {
    expect(deriveStatusLabel(cases.find((item) => item.number === 25)!, { events: eventsFor(25) })).toBe(
      "Served Jul. 24, 2026 — CMC Jan. 14, 2027",
    );
    expect(deriveStatusLabel(cases.find((item) => item.number === 27)!, { events: eventsFor(27) })).toBe(
      "Served Jul. 30, 2026 — Response due Aug. 31, 2026",
    );
  });

  it("keeps waiting phases from collapsing to an old Filed/Served date", () => {
    expect(deriveStatusLabel(cases.find((item) => item.number === 1)!, { events: eventsFor(1) })).toBe("F&R pending");
    expect(deriveStatusLabel(cases.find((item) => item.number === 19)!, { events: eventsFor(19) })).toBe(
      "Under submission",
    );
  });

  it("uses status_label overrides when present", () => {
    const matter = cases.find((item) => item.number === 22)!;
    expect(matter.status_label).toBeTruthy();
    expect(effectiveStatusLabel(matter, { events: eventsFor(22) })).toBe(matter.status_label);
    expect(deriveStatusLabel(matter, { events: eventsFor(22) })).toBe("Settled");
  });

  it("produces an effective label ≤ 60 chars for every matter", () => {
    for (const matter of cases) {
      const label = effectiveStatusLabel(matter, { events: eventsFor(matter.number) });
      expect(label.trim(), `matter ${matter.number}`).not.toBe("");
      expect(label.length, `matter ${matter.number}: ${label}`).toBeLessThanOrEqual(STATUS_LABEL_MAX);
      expect(label, `matter ${matter.number}`).not.toMatch(/\n/);
    }
  });

  it("does not let a contingent SOL deadline make a waiting phase look scheduled", () => {
    const matter = cases.find((item) => item.number === 1)!;
    const solDeadline = {
      date: "Nov. 1, 2026",
      event: "CCP §335.1 two-year statute of limitations (computed) — Matter 1",
      type: "deadline",
      matters: [1],
      upcoming: true,
    } as TimelineEvent;
    expect(deriveStatusLabel(matter, { events: [...eventsFor(1), solDeadline] })).toBe("F&R pending");
  });

  it("scores meet-and-confer below posture hearings", () => {
    const hearing = {
      date: "Aug. 28, 2026",
      event: "Demurrer Hearing — Matter 20",
      type: "hearing",
      matters: [20],
      upcoming: true,
    } as TimelineEvent;
    const chore = {
      date: "Aug. 21, 2026",
      event: "Meet-and-confer deadline — Matter 20",
      type: "deadline",
      matters: [20],
      upcoming: true,
    } as TimelineEvent;
    expect(postureEventScore(hearing, "demurrer")).toBeGreaterThan(postureEventScore(chore, "demurrer"));
  });
});
