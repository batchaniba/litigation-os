import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { fuseData, listMattersData, portfolioToday, seedSource } from "./data.mjs";

// Read-only D1 stub: answers SELECTs from in-memory tables by table name.
function d1(tables) {
  return {
    prepare(sql) {
      const stmt = {
        bind: () => stmt,
        async all() {
          const table = /FROM\s+(\w+)/i.exec(sql)?.[1];
          if (!(table in tables)) throw new Error(`no such table: ${table}`);
          return { results: tables[table] };
        },
      };
      return stmt;
    },
  };
}

// Matter rows carry STALE next_clock_* columns on purpose: the Worker must not
// read them. M29's real next clock (Oct 13) exists only in the clocks table;
// M26's stored next clock is a hearing that was vacated.
const MATTERS = [
  { number: 26, caption: "v. UPS", lifecycle: "active", next_clock_date: "2026-10-07", next_clock_title: "HEARING (vacated)" },
  { number: 29, caption: "v. Amazon", lifecycle: "active", next_clock_date: "2026-09-22", next_clock_title: "old answer deadline" },
  { number: 41, caption: "v. Nuro", lifecycle: "pre_filing", next_clock_date: null, next_clock_title: null },
];
const CLOCKS = [
  { matter_number: 26, title: "HEARING (vacated)", date: "2026-10-07", kind: "hearing", status: "vacated" },
  { matter_number: 29, title: "old answer deadline", date: "2026-09-22", kind: "deadline", status: "satisfied" },
  { matter_number: 29, title: "Opposition due on Dkt. 19", date: "2026-10-13", kind: "deadline", status: "open" },
  { matter_number: 29, title: "Hearing on Dkt. 19", date: "2026-11-18", kind: "hearing", status: "open" },
];

describe("D1 reads derive the next clock from the clocks table", () => {
  beforeEach(() => {
    vi.useFakeTimers();
    vi.setSystemTime(new Date("2026-10-05T18:00:00Z"));
  });
  afterEach(() => vi.useRealTimers());

  it("fuse board uses live clocks, not the stored next_clock columns", async () => {
    const env = { DB: d1({ matters: MATTERS, clocks: CLOCKS, meta: [] }) };
    const board = await fuseData(env, 14);
    expect(board.fuse.map((m) => [m.number, m.date, m.title])).toEqual([
      [29, "2026-10-13", "Opposition due on Dkt. 19"],
    ]);
    // M26's only clock is vacated: it waits with no date, it is not "due Oct 7".
    expect(board.wait.find((m) => m.number === 26)).toMatchObject({ date: null, overdue: false });
    expect(board.parked.map((m) => m.number)).toEqual([41]);
  });

  it("matter list reports the computed next clock", async () => {
    const env = { DB: d1({ matters: MATTERS, clocks: CLOCKS }) };
    const list = await listMattersData(env);
    expect(list.find((m) => m.number === 29).next_clock).toEqual({
      date: "2026-10-13",
      title: "Opposition due on Dkt. 19",
    });
    expect(list.find((m) => m.number === 26).next_clock).toBeNull();
  });

  it("uses the Pacific date, not UTC", () => {
    vi.setSystemTime(new Date("2026-10-06T03:00:00Z")); // 8 pm Oct 5 in Los Angeles
    expect(portfolioToday()).toBe("2026-10-05");
  });
});

describe("seedSource", () => {
  const NOW = Date.parse("2026-10-05T18:00:00Z");

  it("reports the commit and flags a seed older than a day as stale", async () => {
    const env = {
      DB: d1({ meta: [{ key: "source_commit", value: "8e86d6e" }, { key: "seeded_at", value: "2026-09-27T17:31:00Z" }] }),
    };
    expect(await seedSource(env, NOW)).toEqual({
      source_commit: "8e86d6e",
      seeded_at: "2026-09-27T17:31:00Z",
      age_days: 8,
      stale: true,
    });
  });

  it("treats a missing meta table as unknown and stale", async () => {
    expect(await seedSource({ DB: d1({}) }, NOW)).toMatchObject({ source_commit: null, stale: true });
  });

  it("is fresh within a day of seeding", async () => {
    const env = { DB: d1({ meta: [{ key: "source_commit", value: "abc" }, { key: "seeded_at", value: "2026-10-05T12:00:00Z" }] }) };
    expect(await seedSource(env, NOW)).toMatchObject({ stale: false, age_days: 0 });
  });
});
