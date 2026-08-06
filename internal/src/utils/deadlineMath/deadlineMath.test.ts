import { describe, expect, it } from "vitest";
import {
  RECIPE_META,
  SOURCES,
  computeDeadlinesFromEvent,
  computeDemurrerBriefing,
  formatPortfolioDate,
  holidaysForCourt,
  isCourtDay,
  isCourtHoliday,
  rollForwardToCourtDay,
  subtractCourtDaysBefore,
  toDayKey,
} from "./index";

describe("deadlineMath — date grounding", () => {
  it("accepts portfolio dates, ISO keys, and HTML date values", () => {
    expect(toDayKey("Aug. 28, 2026")).toBe("2026-08-28");
    expect(toDayKey("2026-08-28")).toBe("2026-08-28");
    expect(toDayKey("Jul. 24, 2026")).toBe("2026-07-24");
  });

  it("formats day keys in portfolio style", () => {
    expect(formatPortfolioDate("2026-08-21")).toBe("Aug. 21, 2026");
    expect(formatPortfolioDate("2026-07-03")).toBe("July 3, 2026");
  });
});

describe("deadlineMath — court holidays from official calendars", () => {
  it("marks California Judicial Branch 2026 holidays for all four superior courts", () => {
    for (const court of [
      "San Joaquin Sup. Ct.",
      "Alameda Sup. Ct.",
      "Sacramento Sup. Ct.",
      "Santa Clara Sup. Ct.",
    ] as const) {
      expect(isCourtHoliday("2026-02-12", court)).toBe(true); // Lincoln's Birthday
      expect(isCourtHoliday("2026-03-31", court)).toBe(true); // Farmworkers Day
      expect(isCourtHoliday("2026-09-25", court)).toBe(true); // Native American Day
      expect(isCourtHoliday("2026-11-27", court)).toBe(true); // Day after Thanksgiving
      expect(isCourtHoliday("2026-10-12", court)).toBe(false); // Columbus Day is federal-only
    }
  });

  it("distinguishes E.D. Cal. Chief Judge closures from N.D. Cal.", () => {
    expect(isCourtHoliday("2026-11-27", "USDC E.D. Cal.")).toBe(true);
    expect(isCourtHoliday("2026-12-24", "USDC E.D. Cal.")).toBe(true);
    expect(isCourtHoliday("2026-12-31", "USDC E.D. Cal.")).toBe(true);
    expect(isCourtHoliday("2026-11-27", "USDC N.D. Cal.")).toBe(false);
    expect(isCourtHoliday("2026-12-24", "USDC N.D. Cal.")).toBe(false);
    expect(isCourtHoliday("2026-10-12", "USDC N.D. Cal.")).toBe(true);
  });

  it("treats weekends as non-court days even when not listed as holidays", () => {
    expect(isCourtDay("2026-08-22", "San Joaquin Sup. Ct.")).toBe(false); // Saturday
    expect(isCourtDay("2026-08-23", "San Joaquin Sup. Ct.")).toBe(false); // Sunday
    expect(isCourtDay("2026-08-24", "San Joaquin Sup. Ct.")).toBe(true);
  });

  it("attaches primary-source URLs for every holiday entry", () => {
    for (const h of holidaysForCourt("Alameda Sup. Ct.")) {
      expect(h.sourceId).toBeTruthy();
    }
    expect(SOURCES.caHolidays.url).toContain("courts.ca.gov");
    expect(SOURCES.caedHolidays.url).toContain("caed.uscourts.gov");
    expect(SOURCES.candHolidays.url).toContain("cand.uscourts.gov");
  });
});

describe("deadlineMath — CCP §1005 / demurrer hearing (Matter 20 golden)", () => {
  it("counts 5 court days before Aug. 28, 2026 hearing as Aug. 21 (AG reply)", () => {
    const reply = subtractCourtDaysBefore("2026-08-28", 5, "Alameda Sup. Ct.");
    expect(reply).toBe("2026-08-21");
  });

  it("computes full demurrer briefing from the Aug. 28 hearing", () => {
    const result = computeDemurrerBriefing("Aug. 28, 2026", {
      court: "Alameda Sup. Ct.",
      serviceMethod: "mail_ca",
    });

    const byId = Object.fromEntries(result.deadlines.map((d) => [d.id, d]));
    expect(byId.reply.date).toBe("2026-08-21");
    expect(byId.opposition.date).toBe("2026-08-17");
    expect(byId.moving_papers.date).toBe("2026-08-06");
    expect(byId.moving_papers_mail_service.date).toBe("2026-07-31");
    expect(byId.moving_papers_mail_service.rawDate).toBe("2026-08-01");
    expect(byId.moving_papers_mail_service.rolled).toBe(true);

    expect(byId.reply.citations.some((c) => c.id === "ccp1005")).toBe(true);
    expect(byId.reply.citations.some((c) => c.id === "crc31320")).toBe(true);
    expect(result.sources.some((s) => s.url.includes("leginfo.legislature.ca.gov"))).toBe(true);
    expect(result.sources.some((s) => s.url.includes("alameda.courts.ca.gov"))).toBe(true);
  });
});

describe("deadlineMath — CCP §412.20 answer clocks (portfolio goldens)", () => {
  it("FedEx service Jul. 24 → Aug. 24 after Sunday §12a roll (Matter 25)", () => {
    const result = computeDeadlinesFromEvent({
      recipe: "ca_summons_service",
      anchorDate: "Jul. 24, 2026",
      court: "San Joaquin Sup. Ct.",
    });
    const d = result.deadlines[0];
    expect(d.rawDate).toBe("2026-08-23");
    expect(d.date).toBe("2026-08-24");
    expect(d.rolled).toBe(true);
    expect(d.displayDate).toBe("Aug. 24, 2026");
    expect(d.explanation).toMatch(/CCP §12a/);
  });

  it("UPS service Jul. 22 → Aug. 21 with no roll (Matter 26)", () => {
    const result = computeDeadlinesFromEvent({
      recipe: "ca_summons_service",
      anchorDate: "2026-07-22",
      court: "San Joaquin Sup. Ct.",
    });
    expect(result.deadlines[0]).toMatchObject({
      date: "2026-08-21",
      rawDate: "2026-08-21",
      rolled: false,
    });
  });

  it("Randstad service Jul. 30 → Aug. 31 after Saturday §12a roll (Matter 27)", () => {
    const result = computeDeadlinesFromEvent({
      recipe: "ca_summons_service",
      anchorDate: "Jul. 30, 2026",
      court: "Alameda Sup. Ct.",
    });
    expect(result.deadlines[0].rawDate).toBe("2026-08-29");
    expect(result.deadlines[0].date).toBe("2026-08-31");
  });

  it("Amazon service Jul. 31 → Aug. 31 after Sunday §12a roll (Matter 29)", () => {
    const result = computeDeadlinesFromEvent({
      recipe: "ca_summons_service",
      anchorDate: "Jul. 31, 2026",
      court: "Alameda Sup. Ct.",
    });
    expect(result.deadlines[0].rawDate).toBe("2026-08-30");
    expect(result.deadlines[0].date).toBe("2026-08-31");
  });
});

describe("deadlineMath — CCP §430.41 meet-and-confer", () => {
  it("lands 5 calendar days before the responsive deadline", () => {
    const result = computeDeadlinesFromEvent({
      recipe: "ca_demurrer_meet_confer",
      anchorDate: "Aug. 24, 2026",
      court: "San Joaquin Sup. Ct.",
    });
    expect(result.deadlines[0].date).toBe("2026-08-19");
  });

  it("flags a practical prior-court-day target when day −5 is a Sunday", () => {
    const result = computeDeadlinesFromEvent({
      recipe: "ca_demurrer_meet_confer",
      anchorDate: "Aug. 21, 2026",
      court: "San Joaquin Sup. Ct.",
    });
    expect(result.deadlines[0].date).toBe("2026-08-16");
    expect(result.deadlines[1].date).toBe("2026-08-14");
    expect(result.deadlines[1].rolled).toBe(true);
  });
});

describe("deadlineMath — CRC service / CMC", () => {
  it("CRC 3.110(b) 60 days from Jul. 15 filing: raw Sep. 13 (Sunday) rolls to Sep. 14", () => {
    const result = computeDeadlinesFromEvent({
      recipe: "ca_crc_service_deadline",
      anchorDate: "July 15, 2026",
      court: "San Joaquin Sup. Ct.",
    });
    expect(result.deadlines[0].rawDate).toBe("2026-09-13");
    expect(result.deadlines[0].date).toBe("2026-09-14");
    expect(result.deadlines[0].rolled).toBe(true);
  });

  it("CRC 3.110(b) Amazon Jul. 28 filing: Sep. 26 Saturday → Sep. 28 (Matter 29)", () => {
    const result = computeDeadlinesFromEvent({
      recipe: "ca_crc_service_deadline",
      anchorDate: "Jul. 28, 2026",
      court: "Alameda Sup. Ct.",
    });
    expect(result.deadlines[0].rawDate).toBe("2026-09-26");
    expect(result.deadlines[0].date).toBe("2026-09-28");
  });

  it("CRC 3.725 / 3.724 from Jan. 13, 2027 CMC (Matter 26)", () => {
    const result = computeDeadlinesFromEvent({
      recipe: "ca_cmc_statement",
      anchorDate: "Jan. 13, 2027",
      court: "San Joaquin Sup. Ct.",
    });
    const byId = Object.fromEntries(result.deadlines.map((d) => [d.id, d]));
    expect(byId.cmc_meet_confer.date).toBe("2026-12-14");
    expect(byId.cmc_statement.date).toBe("2026-12-29");
  });
});

describe("deadlineMath — FRCP 6", () => {
  it("rolls a federal answer deadline off a weekend under Rule 6(a)", () => {
    // Service Friday 2026-08-14 → +21 = 2026-09-04 (Friday) — no roll.
    const fri = computeDeadlinesFromEvent({
      recipe: "federal_answer_after_service",
      anchorDate: "2026-08-14",
      court: "USDC N.D. Cal.",
    });
    expect(fri.deadlines[0].date).toBe("2026-09-04");

    // Service Saturday 2026-08-15 → exclude Sat, +21 calendar = Sep 5 Saturday → Monday Sep 7 is Labor Day → Tue Sep 8.
    const sat = computeDeadlinesFromEvent({
      recipe: "federal_answer_after_service",
      anchorDate: "2026-08-15",
      court: "USDC N.D. Cal.",
    });
    expect(sat.deadlines[0].rawDate).toBe("2026-09-05");
    expect(sat.deadlines[0].date).toBe("2026-09-08");
  });

  it("adds FRCP 6(d) three mail days after the 6(a) expiration", () => {
    const result = computeDeadlinesFromEvent({
      recipe: "federal_response_after_mail_service",
      anchorDate: "2026-08-03",
      court: "USDC E.D. Cal.",
    });
    const byId = Object.fromEntries(result.deadlines.map((d) => [d.id, d]));
    // Aug 3 + 14 = Aug 17
    expect(byId.federal_period_before_mail.date).toBe("2026-08-17");
    // +3 = Aug 20
    expect(byId.federal_period_with_mail.rawDate).toBe("2026-08-20");
    expect(byId.federal_period_with_mail.date).toBe("2026-08-20");
  });

  it("computes FRCP 6(c) motion notice backward from a hearing", () => {
    const result = computeDeadlinesFromEvent({
      recipe: "federal_motion_hearing",
      anchorDate: "2026-09-18",
      court: "USDC E.D. Cal.",
    });
    const byId = Object.fromEntries(result.deadlines.map((d) => [d.id, d]));
    expect(byId.federal_motion_notice.date).toBe("2026-09-04");
    expect(byId.federal_opposing_affidavit.date).toBe("2026-09-11");
  });
});

describe("deadlineMath — service-method variants", () => {
  it("applies overnight +2 calendar days without a weekend roll", () => {
    const result = computeDeadlinesFromEvent({
      recipe: "ca_motion_hearing",
      anchorDate: "2026-08-28",
      court: "Alameda Sup. Ct.",
      serviceMethod: "overnight",
    });
    const mail = result.deadlines.find((d) => d.id === "moving_papers_mail_service");
    expect(mail?.date).toBe("2026-08-04");
    expect(mail?.rolled).toBe(false);
  });

  it("surfaces an electronic-service baseline note instead of inventing an add-on", () => {
    const result = computeDeadlinesFromEvent({
      recipe: "ca_demurrer_hearing",
      anchorDate: "2026-08-28",
      court: "Alameda Sup. Ct.",
      serviceMethod: "electronic",
    });
    const note = result.deadlines.find((d) => d.id === "moving_papers_electronic_note");
    expect(note?.date).toBe("2026-08-06");
    expect(note?.explanation).toMatch(/1010\.6/);
  });
});

describe("deadlineMath — guards", () => {
  it("rejects mixing a California recipe with a federal court", () => {
    expect(() =>
      computeDeadlinesFromEvent({
        recipe: "ca_demurrer_hearing",
        anchorDate: "2026-08-28",
        court: "USDC E.D. Cal.",
      }),
    ).toThrow(/california/);
  });

  it("exposes a recipe catalog for the UI", () => {
    expect(Object.keys(RECIPE_META).length).toBeGreaterThanOrEqual(8);
  });

  it("rollForward is a no-op on court days", () => {
    expect(rollForwardToCourtDay("2026-08-24", "San Joaquin Sup. Ct.")).toEqual({
      date: "2026-08-24",
      rolled: false,
    });
  });
});
