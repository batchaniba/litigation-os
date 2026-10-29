import { describe, expect, it } from "vitest";
import { buildQueue } from "../../../scripts/lib/next-actions.mjs";
import {
  agendaCounts,
  agendaWeeks,
  laneStatus,
  monthStrip,
  needsAttention,
  nextCourtDate,
  shortCaption,
  shortCourt,
  shortTitle,
  stageBoard,
  syncAgeDays,
  weekRangeLabel,
} from "./dashboardModel";

const TODAY = "2026-10-28"; // Wednesday

const cases = [
  { number: 20, caption: "Newanforbi v. California Highway Patrol, et al.", court: "Alameda Sup. Ct.", lifecycle: "active", phase: "hearing", cluster: 1 },
  { number: 32, caption: "Nforbi v. Meza-Gonzalez, et al", court: "USDC N.D. Cal. (Oakland)", lifecycle: "active", phase: "mtd_briefing", cluster: 1 },
  { number: 36, caption: "Brendan Ngwa Nforbi v. AT&T Mobility Services LLC", court: "USDC E.D. Cal.", lifecycle: "active", phase: "service", cluster: 3 },
  { number: 42, caption: "Brendan Ngwa Nforbi v. Staples Retail et al.", court: "TBD", lifecycle: "pre_filing", phase: "pre_filing", cluster: 3, status_label: "Pending — FADV notice Oct. 7" },
  { number: 27, caption: "Newanforbi v. Randstad, et al.", court: "Alameda Sup. Ct.", lifecycle: "settled", phase: "terminal", cluster: 3, status_label: "Settled; dismissal pending" },
  { number: 9, caption: "Newanforbi v. Old Case", court: "USDC E.D. Cal.", lifecycle: "dismissed", phase: "terminal", cluster: 4 },
];

const ev = (date, matters, event, extra = {}) => ({ date, matters, event, upcoming: true, actor: "you", ...extra });

const timeline = [
  ev("Sep. 17, 2026", [32], "FILE — summons return / CCP § 415.20(b) declaration being refiled in Nforbi v. Meza-Gonzalez et al. (4:26-cv-08271-ASK). USER REPORT Oct. 28, 2026."),
  ev("Oct. 29, 2026", [36], "DEADLINE — USM service packet and Notice of Submission in Brendan Ngwa Nforbi v. AT&T Mobility Services LLC (E.D. Cal.)."),
  ev("Nov. 4, 2026", [20], "Case Management Conference — Newanforbi v. CHP et al. (26CV191136), Nov. 4, 2026, 4:00 p.m., Dept. 25", { type: "hearing" }),
  ev("Nov. 9, 2026", [32], "Opposition to Dkt. 22 motion to dismiss/strike due Nov. 9, 2026 — Nforbi v. Meza-Gonzalez et al."),
  ev("Nov. 16, 2026", [32], "WATCH — Defendants' reply in support of Dkt. 22 motion due Nov. 16, 2026", { actor: "opposing" }),
  ev("Jan. 8, 2027", [20], "HEARING — Motion for peremptory writ of mandate, 9:00 a.m., Dept. 25", { type: "hearing" }),
];

const queue = buildQueue(timeline, cases, { today: TODAY, horizonDays: 30 });

describe("shortTitle", () => {
  it("drops bookkeeping tags, the caption, restated dates and USER REPORT notes", () => {
    expect(shortTitle(timeline[0].event)).toBe("Summons return / CCP § 415.20(b) declaration being refiled");
    expect(shortTitle(timeline[3].event)).toBe("Opposition to Dkt. 22 motion to dismiss/strike");
    expect(shortTitle(timeline[2].event)).toBe("Case Management Conference");
  });

  it("does not cut a sentence at an abbreviation", () => {
    expect(shortTitle("Deadline to make initial disclosures (Fed. R. Civ. P. 26(a)(1)) and file the statement")).toBe(
      "Make initial disclosures (Fed. R. Civ. P. 26(a)(1)) and file the statement",
    );
  });

  it("sentence-cases a shouted lead and drops a verb the chip already says", () => {
    expect(shortTitle("EX PARTE HEARING — Application for Order")).toBe("Ex parte hearing — Application for Order");
    expect(shortTitle("Deadline to file ADR Certification (ADR L.R. 3)")).toBe("ADR Certification (ADR L.R. 3)");
  });

  it("stops at a redaction instead of showing half a word", () => {
    expect(shortTitle("OPTIONAL: last day to request a Zoom appearance [redacted]anding Order")).toBe("Request a Zoom appearance");
  });

  it("truncates on a word boundary", () => {
    const t = shortTitle("word ".repeat(40), 30);
    expect(t.length).toBeLessThanOrEqual(31);
    expect(t.endsWith("…")).toBe(true);
  });
});

describe("captions and courts", () => {
  it("strips the plaintiff and corporate suffixes", () => {
    expect(shortCaption("Brendan Ngwa Nforbi v. Hertz Global Holdings, Inc.")).toBe("Hertz Global Holdings");
    expect(shortCaption("Newanforbi v. Randstad, et al.")).toBe("Randstad");
    expect(shortCaption("Nforbi v. Meza-Gonzalez, et al")).toBe("Meza-Gonzalez");
  });

  it("shortens court names", () => {
    expect(shortCourt("USDC N.D. Cal. (Oakland)")).toBe("N.D. Cal.");
    expect(shortCourt("San Joaquin Sup. Ct.")).toBe("San Joaquin");
  });

  it("drops a stage word the lane already says", () => {
    expect(laneStatus("Pending — FADV notice Oct. 7")).toBe("FADV notice Oct. 7");
    expect(laneStatus("")).toBe("No date set");
  });
});

describe("needsAttention", () => {
  it("lists your past-due items, then the next three days", () => {
    const a = needsAttention(queue, cases);
    expect(a.items.map((i) => i.matterLabel)).toEqual(["M32", "M36"]);
    expect(a.items[0].relative).toBe("Past due · 41 days");
    expect(a.items[1].relative).toBe("Tomorrow");
    expect(a.overdue).toBe(1);
    expect(a.soon).toBe(1);
  });
});

describe("agenda", () => {
  it("groups the next 30 days by Sunday–Saturday week, in date order", () => {
    const weeks = agendaWeeks(queue, cases);
    expect(weeks.map((w) => w.label)).toEqual(["This week", "Next week", "Nov. 8 – 14", "Nov. 15 – 21"]);
    expect(weeks[0].range).toBe("Oct. 25 – 31");
    expect(weeks.flatMap((w) => w.rows).map((r) => r.dateKey)).toEqual([
      "2026-10-29", "2026-11-04", "2026-11-09", "2026-11-16",
    ]);
  });

  it("marks the other side's deadlines and filters them out of My moves", () => {
    const rows = agendaWeeks(queue, cases).flatMap((w) => w.rows);
    expect(rows.find((r) => r.dateKey === "2026-11-16").verb.label).toBe("Their move");
    expect(agendaWeeks(queue, cases, { filter: "mine" }).flatMap((w) => w.rows)).toHaveLength(3);
    expect(agendaWeeks(queue, cases, { filter: "court" }).flatMap((w) => w.rows).map((r) => r.dateKey)).toEqual(["2026-11-04"]);
    expect(agendaCounts(queue)).toEqual({ all: 4, mine: 3, court: 1 });
  });

  it("labels weeks that cross a month", () => {
    expect(weekRangeLabel("2026-11-29")).toBe("Nov. 29 – Dec. 5");
  });
});

describe("monthStrip", () => {
  it("starts on this Sunday, marks today, and colours each day by task", () => {
    const strip = monthStrip(queue);
    expect(strip.days).toHaveLength(35);
    expect(strip.days[0].key).toBe("2026-10-25");
    expect(strip.days.find((d) => d.today).key).toBe(TODAY);
    expect(strip.days.find((d) => d.key === "2026-11-04").tones).toEqual(["court"]);
    expect(strip.days.find((d) => d.key === "2026-11-16").tones).toEqual(["theirs"]);
    expect(strip.label).toBe("Oct. 25 – Nov. 28");
  });
});

describe("stageBoard", () => {
  it("places every open matter in one lane and leaves closed matters off", () => {
    const board = stageBoard(cases, queue);
    expect(board.total).toBe(5);
    const lane = (key) => board.lanes.find((l) => l.key === key);
    expect(lane("hearings").items.map((c) => c.number)).toEqual([20]);
    expect(lane("settled").items[0].line).toBe("Settled; dismissal pending");
    expect(board.lanes.flatMap((l) => l.items).some((c) => c.number === 9)).toBe(false);
  });

  it("flags past due in red and undated matters in amber", () => {
    const items = stageBoard(cases, queue).lanes.flatMap((l) => l.items);
    expect(items.find((c) => c.number === 32).tone).toBe("late");
    expect(items.find((c) => c.number === 42)).toMatchObject({ tone: "undated", line: "FADV notice Oct. 7" });
    expect(items.find((c) => c.number === 20).line).toMatch(/^Nov\. 4 · /);
  });
});

describe("pulse figures", () => {
  it("finds the next court appearance and the docket-sync age", () => {
    expect(nextCourtDate(queue, cases).dateKey).toBe("2026-11-04");
    expect(syncAgeDays("2026-09-12", TODAY)).toBe(46);
    expect(syncAgeDays(null, TODAY)).toBe(null);
  });
});
