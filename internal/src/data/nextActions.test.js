import { describe, expect, it } from "vitest";
import {
  buildQueue,
  dateKeyFromLabel,
  daysBetween,
  inferAction,
  inferActor,
  precedentPeers,
  touchesActiveMatter,
  urgencyFor,
  yourQueue,
} from "../../scripts/lib/next-actions.mjs";
import timeline from "./timeline.json";
import upcoming from "./upcoming.json";
import summaries from "./matters/summaries.json";
import graph from "./crossMatter.json";

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

  it("treats plaintiff as you and honors court as an explicit actor", () => {
    expect(inferActor(entry({ actor: "plaintiff" }))).toEqual({
      actor: "you",
      actorSource: "explicit",
    });
    expect(inferActor(entry({ actor: "court" }))).toEqual({
      actor: "court",
      actorSource: "explicit",
    });
  });

  it("flags clocks that run against the other side", () => {
    expect(inferActor(entry({ event: "AG reply deadline (computed) — Respondents' Reply" })).actor)
      .toBe("opposing");
    expect(inferActor(entry({ event: "Responsive pleading deadline (computed) — 30 days from service" })).actor)
      .toBe("opposing");
  });

  it("flags CCP §430.41 demurrer meet-and-confer as opposing", () => {
    expect(
      inferActor(
        entry({
          event:
            "Meet-and-confer deadline (computed) — CCP §430.41(a)(2); if FedEx intends to demur",
        }),
      ).actor,
    ).toBe("opposing");
    expect(
      inferActor(
        entry({
          event:
            "Meet-and-confer target date — if either defendant intends to demur",
        }),
      ).actor,
    ).toBe("opposing");
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

  it("keeps joint CMC meet-and-confer on this litigant's desk", () => {
    expect(
      inferActor(
        entry({
          event:
            "Meet-and-confer deadline — 30 calendar days before Jan. 13, 2027 CMC (CRC 3.724)",
        }),
      ).actor,
    ).toBe("you");
  });
});

describe("inferAction", () => {
  it("reads the verb the day demands", () => {
    expect(inferAction(entry({ type: "hearing", event: "Demurrer Hearing — 9:00 a.m." }))).toBe("appear");
    expect(inferAction(entry({ event: "Meet-and-confer deadline (computed)" }))).toBe("meet & confer");
    expect(inferAction(entry({ event: "Proof-of-service filing deadline" }))).toBe("serve");
    expect(inferAction(entry({ event: "Deadline to file amended complaint" }))).toBe("file");
    expect(inferAction(entry({ event: "Reply deadline — Motion for Protective Order" }))).toBe("file");
    expect(inferAction(entry({ event: "Opposition due — Demurrer" }))).toBe("file");
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

describe("touchesActiveMatter", () => {
  const byNumber = new Map([
    [3, { number: 3, lifecycle: "abandoned", archived: true }],
    [24, { number: 24, lifecycle: "active", archived: false }],
    [31, { number: 31, lifecycle: "pre_filing", archived: false }],
  ]);

  it("is true when any linked matter is still live", () => {
    expect(touchesActiveMatter([3, 24], byNumber)).toBe(true);
    expect(touchesActiveMatter([31], byNumber)).toBe(true);
  });

  it("is false when every linked matter is archived or terminal", () => {
    expect(touchesActiveMatter([3], byNumber)).toBe(false);
  });
});

describe("buildQueue", () => {
  const fixtureSummaries = [
    { number: 3, caption: "Newanforbi v. Derrick", case_no: "2:26-cv-00004", lifecycle: "abandoned", archived: true },
    { number: 20, caption: "Newanforbi v. CHP", case_no: "26CV191136", lifecycle: "active" },
    { number: 24, caption: "Newanforbi v. Serrato", case_no: "4:26-cv-05953", lifecycle: "active" },
    { number: 26, caption: "Newanforbi v. UPS", lifecycle: "active" },
    { number: 31, caption: "Newanforbi v. First Advantage", lifecycle: "active" },
    { number: 9, caption: "Closed matter", lifecycle: "dismissed", archived: true },
  ];
  const fixtureTimeline = [
    entry({ date: "Aug. 7, 2026", event: "Deadline to file amended complaint", matters: [3] }),
    entry({ date: "Aug. 14, 2026", event: "Deadline — file opposition brief", matters: [20] }),
    entry({
      date: "Aug. 21, 2026",
      event: "AG reply deadline (computed)",
      matters: [20],
    }),
    entry({
      date: "Aug. 19, 2026",
      event:
        "Meet-and-confer deadline (computed) — CCP §430.41(a)(2); if UPS intends to demur",
      matters: [26],
    }),
    entry({
      date: "Aug. 25, 2026",
      event: "Deadline — ADR certification",
      matters: [24],
      source: "/documents/matter-24/Order Setting Initial CMC and ADR Deadlines (Doc 4, Filed Jun 17 2026).pdf",
    }),
    entry({ date: "Dec. 2026", event: "Trial setting window", matters: [20] }),
    entry({ date: "Mar. 1, 2027", event: "OUTER STATUTE OF LIMITATIONS", matters: [24] }),
    entry({ date: "Jun. 1, 2026", event: "Already-logged filing", matters: [20], upcoming: false }),
  ];
  const queue = buildQueue(fixtureTimeline, fixtureSummaries, { today: TODAY, horizonDays: 30 });

  it("only picks up entries still flagged upcoming", () => {
    expect(queue.items.some((i) => i.event === "Already-logged filing")).toBe(false);
  });

  it("parks upcoming flags that only touch archived matters", () => {
    expect(queue.retired.map((i) => i.event)).toEqual(["Deadline to file amended complaint"]);
    expect(queue.items.some((i) => i.matters.includes(3))).toBe(false);
  });

  it("puts past-due items first and counts the days negatively", () => {
    // With the abandoned Matter 3 entry retired, the opposition brief is first.
    expect(queue.items[0].event).toBe("Deadline — file opposition brief");
    expect(queue.items[0].urgency).toBe("soon");
    expect(queue.items[0].daysOut).toBe(6);
  });

  it("ranks the litigant's own obligations above other parties' clocks in the same band", () => {
    const adr = queue.items.findIndex((i) => i.event === "Deadline — ADR certification");
    const agReply = queue.items.findIndex((i) => i.event === "AG reply deadline (computed)");
    // ADR is the later date but it is the litigant's to do, so it sorts first.
    expect(adr).toBeLessThan(agReply);
  });

  it("does not treat defendant §430.41 meet-and-confer as this litigant's task", () => {
    const mnc = queue.items.find((i) => i.matters.includes(26));
    expect(mnc.actor).toBe("opposing");
    expect(yourQueue(queue).some((i) => i.matters.includes(26))).toBe(false);
  });

  it("keeps ungroundable dates instead of dropping them", () => {
    expect(queue.undated.map((i) => i.event)).toEqual(["Trial setting window"]);
  });

  it("bands beyond-horizon dates as later rather than hiding them", () => {
    const sol = queue.items.find((i) => i.event === "OUTER STATUTE OF LIMITATIONS");
    expect(sol.urgency).toBe("later");
  });

  it("resolves matter labels from the summaries", () => {
    expect(queue.items[0].matterLabels).toEqual(["20 — Newanforbi v. CHP (26CV191136)"]);
  });

  it("reports active matters with nothing scheduled and ignores closed ones", () => {
    expect(queue.gaps.map((g) => g.number)).toEqual([31]);
  });

  it("yourQueue drops other parties' clocks and beyond-horizon items", () => {
    const mine = yourQueue(queue);
    expect(mine.map((i) => i.event)).toEqual([
      "Deadline — file opposition brief",
      "Deadline — ADR certification",
    ]);
  });

  it("copies a /documents/ source onto the queue row", () => {
    const adr = queue.items.find((i) => i.event === "Deadline — ADR certification");
    expect(adr.source).toMatch(/^\/documents\/matter-24\//);
  });
});

describe("precedentPeers", () => {
  it("lists the other §290.46 dockets from a same_statute link", () => {
    expect(precedentPeers(26, graph.clusters)).toEqual([22, 25, 27, 29]);
  });

  it("attaches those peers on a live UPS queue row", () => {
    const withClusters = buildQueue(
      [entry({ date: "Oct. 7, 2026", event: "UPS MTD hearing", matters: [26], type: "hearing" })],
      [{ number: 26, caption: "Newanforbi v. UPS", lifecycle: "active" }],
      { today: TODAY, horizonDays: 90, clusters: graph.clusters },
    );
    expect(withClusters.items[0].precedentPeers).toEqual([22, 25, 27, 29]);
  });
});

describe("buildQueue against the real portfolio data", () => {
  const queue = buildQueue(timeline, summaries, {
    today: TODAY,
    horizonDays: 30,
    clusters: graph.clusters,
  });

  it("upcoming.json is a sufficient input for the dashboard queue", () => {
    const fromFull = buildQueue(timeline, summaries, {
      today: TODAY,
      horizonDays: 30,
      clusters: graph.clusters,
    });
    const fromUpcoming = buildQueue(upcoming, summaries, {
      today: TODAY,
      horizonDays: 30,
      clusters: graph.clusters,
    });
    expect(fromUpcoming.items).toEqual(fromFull.items);
    expect(fromUpcoming.undated).toEqual(fromFull.undated);
    expect(fromUpcoming.retired).toEqual(fromFull.retired);
    expect(fromUpcoming.gaps).toEqual(fromFull.gaps);
  });

  it("covers every timeline entry flagged upcoming", () => {
    const flagged = timeline.filter((t) => t.upcoming === true).length;
    expect(queue.items.length + queue.undated.length + queue.retired.length).toBe(flagged);
  });

  it("grounds every live upcoming date on a single calendar day", () => {
    expect(queue.undated).toEqual([]);
  });

  it("does not surface archived-only upcoming flags in the ranked queue", () => {
    expect(queue.retired).toEqual([]);
    expect(queue.items.every((i) => i.matters.some((n) => {
      const m = summaries.find((s) => Number(s.number) === n);
      return m && !m.archived && (m.lifecycle === "active" || m.lifecycle === "pre_filing");
    }))).toBe(true);
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

  it("keeps §430.41 meet-and-confer out of yourQueue", () => {
    const mine = yourQueue(queue);
    expect(mine.some((i) => /430\.41|intends to demur/i.test(i.event))).toBe(false);
  });

  it("pins a known actor and a /documents/ source on every upcoming event", () => {
    const flagged = timeline.filter((t) => t.upcoming === true);
    expect(flagged.length).toBeGreaterThan(0);
    for (const event of flagged) {
      expect(inferActor(event).actorSource, event.event).toBe("explicit");
      expect(event.source, event.event).toMatch(/^\/documents\//);
    }
  });
});
