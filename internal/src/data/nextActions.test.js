import { describe, expect, it } from "vitest";
import {
  buildQueue,
  dateKeyFromLabel,
  daysBetween,
  inferAction,
  inferActor,
  urgencyFor,
  yourQueue,
} from "../../scripts/lib/next-actions.mjs";
import timeline from "./timeline.json";
import summaries from "./matters/summaries.json";

const TODAY = "2026-08-08";

const entry = (over = {}) => ({
  date: "Aug. 19, 2026",
  event: "Deadline — file opposition",
  matters: [24],
  type: "deadline",
  upcoming: true,
  ...over,
});

describe("dateKeyFromLabel", () => {
  it("parses the portfolio's abbreviated and full month forms", () => {
    expect(dateKeyFromLabel("Aug. 19, 2026")).toBe("2026-08-19");
    expect(dateKeyFromLabel("May 12, 2026")).toBe("2026-05-12");
    expect(dateKeyFromLabel("September 8, 2026")).toBe("2026-09-08");
    expect(dateKeyFromLabel("~Sep. 1, 2026")).toBe("2026-09-01");
  });

  it("rejects anything that isn't one calendar day", () => {
    // Native Date parsing silently turns "Jul. 9-10, 2026" into July 9, 2010.
    expect(dateKeyFromLabel("Jul. 9-10, 2026")).toBeNull();
    expect(dateKeyFromLabel("Aug. 2025")).toBeNull();
    expect(dateKeyFromLabel("Mar.–Apr. 2025")).toBeNull();
    expect(dateKeyFromLabel("Mid-2025")).toBeNull();
    expect(dateKeyFromLabel(undefined)).toBeNull();
  });
});

describe("daysBetween", () => {
  it("counts whole calendar days in both directions", () => {
    expect(daysBetween(TODAY, "2026-08-19")).toBe(11);
    expect(daysBetween(TODAY, TODAY)).toBe(0);
    expect(daysBetween(TODAY, "2026-08-07")).toBe(-1);
  });

  it("crosses month and year boundaries", () => {
    expect(daysBetween("2026-12-29", "2027-01-06")).toBe(8);
  });
});

describe("inferActor", () => {
  it("honors an explicit actor field over the text heuristics", () => {
    expect(inferActor(entry({ actor: "opposing", event: "Deadline — file opposition" }))).toEqual({
      actor: "opposing",
      actorSource: "explicit",
    });
  });

  it("ignores an unrecognized explicit actor and falls back to inference", () => {
    expect(inferActor(entry({ actor: "nobody" })).actorSource).toBe("inferred");
  });

  it("flags clocks that run against the other side", () => {
    expect(inferActor(entry({ event: "AG reply deadline (computed) — Respondents' Reply" })).actor)
      .toBe("opposing");
    expect(inferActor(entry({ event: "Responsive pleading deadline (computed) — 30 days from service" })).actor)
      .toBe("opposing");
  });

  it("flags court and agency clocks", () => {
    expect(inferActor(entry({ event: "Outer bound for Sheriff Civil Bureau to process order" })).actor)
      .toBe("agency");
    expect(inferActor(entry({ event: "Anticipated deemed-rejection date (computed) — Gov. Claims Act" })).actor)
      .toBe("agency");
  });

  it("defaults to the litigant's own docket", () => {
    expect(inferActor(entry()).actor).toBe("you");
  });
});

describe("inferAction", () => {
  it("reads the verb the day demands", () => {
    expect(inferAction(entry({ type: "hearing", event: "Demurrer Hearing — 9:00 a.m." }))).toBe("appear");
    expect(inferAction(entry({ event: "Meet-and-confer deadline (computed)" }))).toBe("meet & confer");
    expect(inferAction(entry({ event: "Proof-of-service filing deadline" }))).toBe("serve");
    expect(inferAction(entry({ event: "Deadline to file amended complaint" }))).toBe("file");
    expect(inferAction(entry({ event: "Reply — Motion for Protective Order" }))).toBe("prepare");
  });
});

describe("urgencyFor", () => {
  it("bands by days out", () => {
    expect(urgencyFor(-1, 30)).toBe("overdue");
    expect(urgencyFor(0, 30)).toBe("critical");
    expect(urgencyFor(3, 30)).toBe("critical");
    expect(urgencyFor(7, 30)).toBe("soon");
    expect(urgencyFor(30, 30)).toBe("upcoming");
    expect(urgencyFor(31, 30)).toBe("later");
  });
});

describe("buildQueue", () => {
  const fixtureSummaries = [
    { number: 3, caption: "Newanforbi v. Derrick", case_no: "2:26-cv-00004", lifecycle: "active" },
    { number: 20, caption: "Newanforbi v. CHP", case_no: "26CV191136", lifecycle: "active" },
    { number: 24, caption: "Newanforbi v. Serrato", case_no: "4:26-cv-05953", lifecycle: "active" },
    { number: 31, caption: "Newanforbi v. First Advantage", lifecycle: "active" },
    { number: 9, caption: "Closed matter", lifecycle: "dismissed" },
  ];
  const fixtureTimeline = [
    entry({ date: "Aug. 7, 2026", event: "Deadline to file amended complaint", matters: [3] }),
    entry({ date: "Aug. 21, 2026", event: "AG reply deadline (computed)", matters: [20] }),
    entry({ date: "Aug. 25, 2026", event: "Deadline — ADR certification", matters: [24] }),
    entry({ date: "Dec. 2026", event: "Trial setting window", matters: [20] }),
    entry({ date: "Mar. 1, 2027", event: "OUTER STATUTE OF LIMITATIONS", matters: [24] }),
    entry({ date: "Jun. 1, 2026", event: "Already-logged filing", matters: [3], upcoming: false }),
  ];
  const queue = buildQueue(fixtureTimeline, fixtureSummaries, { today: TODAY, horizonDays: 30 });

  it("only picks up entries still flagged upcoming", () => {
    expect(queue.items.some((i) => i.event === "Already-logged filing")).toBe(false);
  });

  it("puts past-due items first and counts the days negatively", () => {
    expect(queue.items[0].event).toBe("Deadline to file amended complaint");
    expect(queue.items[0].urgency).toBe("overdue");
    expect(queue.items[0].daysOut).toBe(-1);
  });

  it("ranks the litigant's own obligations above other parties' clocks in the same band", () => {
    const adr = queue.items.findIndex((i) => i.event === "Deadline — ADR certification");
    const agReply = queue.items.findIndex((i) => i.event === "AG reply deadline (computed)");
    // ADR is the later date but it is the litigant's to do, so it sorts first.
    expect(adr).toBeLessThan(agReply);
  });

  it("keeps ungroundable dates instead of dropping them", () => {
    expect(queue.undated.map((i) => i.event)).toEqual(["Trial setting window"]);
  });

  it("bands beyond-horizon dates as later rather than hiding them", () => {
    const sol = queue.items.find((i) => i.event === "OUTER STATUTE OF LIMITATIONS");
    expect(sol.urgency).toBe("later");
  });

  it("resolves matter labels from the summaries", () => {
    expect(queue.items[0].matterLabels).toEqual(["3 — Newanforbi v. Derrick (2:26-cv-00004)"]);
  });

  it("reports active matters with nothing scheduled and ignores closed ones", () => {
    expect(queue.gaps.map((g) => g.number)).toEqual([31]);
  });

  it("yourQueue drops other parties' clocks and beyond-horizon items", () => {
    const mine = yourQueue(queue);
    expect(mine.map((i) => i.event)).toEqual([
      "Deadline to file amended complaint",
      "Deadline — ADR certification",
    ]);
  });
});

describe("buildQueue against the real portfolio data", () => {
  const queue = buildQueue(timeline, summaries, { today: TODAY, horizonDays: 30 });

  it("covers every timeline entry flagged upcoming", () => {
    const flagged = timeline.filter((t) => t.upcoming === true).length;
    expect(queue.items.length + queue.undated.length).toBe(flagged);
  });

  it("grounds every upcoming date on a single calendar day", () => {
    expect(queue.undated).toEqual([]);
  });

  it("resolves every referenced matter number to a caption", () => {
    const unresolved = queue.items.flatMap((i) => i.matterLabels).filter((l) => !l.includes(" — "));
    expect(unresolved).toEqual([]);
  });

  it("returns a stable ordering: no band ever precedes an earlier band", () => {
    const order = ["overdue", "critical", "soon", "upcoming", "later"];
    const ranks = queue.items.map((i) => order.indexOf(i.urgency));
    expect(ranks).toEqual([...ranks].sort((a, b) => a - b));
  });
});
