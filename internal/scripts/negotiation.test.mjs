import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { describe, expect, it } from "vitest";
import { LEDGER_DIR, checkMove, parseLedger } from "./lib/negotiation.mjs";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..");
const read = (n) => parseLedger(fs.readFileSync(path.join(ROOT, LEDGER_DIR, `${n}.jsonl`), "utf8"), `${n}.jsonl`);

// Matter 27 through the Sep. 17 agreement in principle. History is append-only,
// so this prefix is stable as later moves are recorded.
const randstad = read("27").filter((m) => m.date <= "2026-09-17");

/** Check each Plaintiff demand/withdrawal against only the moves before it. */
function replay(ledger) {
  return ledger
    .map((m, i) => ({ m, i }))
    .filter(({ m }) => m.side === "plaintiff" && (m.kind === "demand" || m.kind === "withdraw"))
    .map(({ m, i }) => ({ move: m, result: checkMove(ledger.slice(0, i), m) }));
}
const rulesOf = (r) => r.blocks.map((b) => b.rule).sort();

describe("Randstad replay (Matter 27): the guard would have stopped the slide", () => {
  const steps = replay(randstad);
  const at = (date, kind, amount) =>
    steps.find((s) => s.move.date === date && s.move.kind === kind && (amount == null || s.move.amount === amount));

  it("Aug. 19 $55k Randstad-only: a cut from the $85k pre-filing ask with no Randstad number, and the $250k draft unsent", () => {
    const r = at("2026-08-19", "demand", 55000).result;
    expect(r.ok).toBe(false);
    expect(rulesOf(r)).toEqual(expect.arrayContaining(["R1", "R3", "R4", "R6"]));
    expect(r.blocks.find((b) => b.rule === "R6" && /250,000/.test(b.why))).toBeTruthy();
  });

  it("Sep. 9 withdrawal: no replacement, and the defense had only asked for time", () => {
    const r = at("2026-09-09", "withdraw").result;
    expect(rulesOf(r)).toEqual(expect.arrayContaining(["R1", "R2"]));
    expect(r.blocks.find((b) => b.rule === "R1").why).toMatch(/request_time/);
  });

  it("Sep. 12 $25k global: against yourself, price cut plus extra time, nothing bought, $40k draft unsent", () => {
    const sent = { ...at("2026-09-12", "demand", 25000).move, gives_time: true };
    const r = checkMove(randstad.slice(0, randstad.indexOf(at("2026-09-12", "demand", 25000).move)), sent);
    expect(rulesOf(r)).toEqual(expect.arrayContaining(["R1", "R2", "R3", "R4", "R6"]));
    expect(r.blocks.find((b) => b.rule === "R6" && /40,000/.test(b.why))).toBeTruthy();
  });

  it("restating the same figures (Aug. 28) is not a concession", () => {
    const r = at("2026-08-28", "demand", 55000).result;
    expect(rulesOf(r)).not.toContain("R1");
    expect(rulesOf(r)).not.toContain("R3");
  });
});

describe("checkMove", () => {
  const base = [
    { date: "2026-08-19", side: "plaintiff", kind: "walkaway", amount: 30000, scope: "global" },
    { date: "2026-08-19", side: "plaintiff", kind: "demand", amount: 85000, scope: "global" },
  ];

  it("allows a lower figure once the defense has put a number down, if it buys something and rests on an event", () => {
    const ledger = [...base, { date: "2026-09-01", side: "defense", kind: "counter", amount: 15000, scope: "global" }];
    const r = checkMove(ledger, {
      kind: "demand",
      amount: 60000,
      scope: "global",
      buys: "defense_number",
      event: "RK produced the InfoMart report showing the registry flag",
    });
    expect(r).toMatchObject({ ok: true, blocks: [] });
  });

  it("treats a deadline or a default motion as pressure, not an event", () => {
    const ledger = [...base, { date: "2026-09-01", side: "defense", kind: "counter", amount: 15000, scope: "global" }];
    const r = checkMove(ledger, { kind: "demand", amount: 60000, scope: "global", buys: "defense_number", event: "their answer deadline is Monday" });
    expect(rulesOf(r)).toEqual(["R4"]);
  });

  it("blocks a figure below the walk-away, and any figure with no walk-away written", () => {
    expect(rulesOf(checkMove(base, { kind: "demand", amount: 85000, scope: "global" }))).toEqual([]);
    const ledger = [...base, { date: "2026-09-01", side: "defense", kind: "counter", amount: 5000, scope: "global" }];
    expect(rulesOf(checkMove(ledger, { kind: "demand", amount: 20000, scope: "global", buys: "defense_number", event: "ruling on demurrer" }))).toEqual(["WALKAWAY"]);
    expect(rulesOf(checkMove(base.slice(1), { kind: "demand", amount: 85000, scope: "global" }))).toEqual(["R6"]);
  });

  it("blocks trading a default or waiver for procedure alone", () => {
    const r = checkMove(base, { kind: "demand", amount: 85000, scope: "global", trades: ["default"] });
    expect(rulesOf(r)).toEqual(["R7"]);
    expect(checkMove(base, { kind: "demand", amount: 85000, scope: "global", trades: ["default"], for_money: true }).ok).toBe(true);
  });
});

describe("ledger files", () => {
  it("every internal/private/negotiation/*.jsonl parses and validates", () => {
    const dir = path.join(ROOT, LEDGER_DIR);
    const files = fs.readdirSync(dir).filter((f) => f.endsWith(".jsonl"));
    expect(files.length).toBeGreaterThan(0);
    for (const f of files) expect(() => parseLedger(fs.readFileSync(path.join(dir, f), "utf8"), f)).not.toThrow();
  });
});

describe("superseded drafts", () => {
  it("an unsent draft stops counting once a later figure is actually sent", () => {
    const ledger = [
      { date: "2026-09-01", side: "plaintiff", kind: "walkaway", amount: 10000, scope: "global" },
      { date: "2026-09-12", side: "plaintiff", kind: "draft", amount: 40000, scope: "global" },
      { date: "2026-09-12", side: "plaintiff", kind: "demand", amount: 25000, scope: "global" },
      { date: "2026-09-17", side: "defense", kind: "counter", amount: 15000, scope: "global" },
    ];
    const r = checkMove(ledger, { kind: "demand", amount: 20000, scope: "global", buys: "defense_number", event: "RK confirmed coverage" });
    expect(r.blocks.map((b) => b.rule)).not.toContain("R6");
  });
});
