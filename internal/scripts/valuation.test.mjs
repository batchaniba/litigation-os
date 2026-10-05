import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { describe, expect, it } from "vitest";
import { LEDGER_DIR } from "./lib/negotiation.mjs";
import { computeValuation, validateValuation } from "./lib/valuation.mjs";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..");
const SHA = "a".repeat(64);

function sample(overrides = {}) {
  return {
    matter: 99,
    evidence: [
      { id: "adm", status: "on_record", pin: "Dkt. 4 ¶ 26", quote: "admits ...", sha256: SHA },
      { id: "rpt", status: "requested_not_served", pin: "RFP 1" },
      { id: "res", status: "on_record", pin: "Dkt. 4 aff. def.", quote: "in part", reserve: true },
    ],
    elements: [{ id: "use", element: "registry use", evidence: ["adm"], proof: "admitted" }],
    defenses: [{ id: "d1", name: "misrep", threat: "high", answered_by: ["res"], cuts: ["wages"] }],
    damages: [
      { id: "wages", amount: 50000, p: 0.5, evidence: ["adm"] },
      { id: "distress", amount: 20000, p: 0.5, evidence: [] },
    ],
    positions: { opening: 100000, bracket: { early: [20000, 40000], after_trigger: [40000, 80000] }, trigger: { label: "t", met_by: ["adm"] } },
    ...overrides,
  };
}

describe("validateValuation", () => {
  it("accepts a well-formed file", () => {
    expect(validateValuation(sample())).toEqual([]);
  });
  it("rejects unknown evidence references, bad probabilities, and unquoted record evidence", () => {
    const v = sample();
    v.damages[0].evidence = ["nope"];
    v.damages[1].p = 1.4;
    v.evidence[0].quote = undefined;
    const errs = validateValuation(v).join("\n");
    expect(errs).toMatch(/unknown evidence 'nope'/);
    expect(errs).toMatch(/p must be between 0 and 1/);
    expect(errs).toMatch(/quote the record/);
  });
});

describe("computeValuation", () => {
  it("weights each line, flags unsupported lines, and picks the bracket by trigger", () => {
    const c = computeValuation(sample(), { walkaway: 30000 });
    expect(c.gross).toBe(70000);
    expect(c.expected).toBe(35000);
    expect(c.lines.find((l) => l.id === "distress").unsupported).toBe(true);
    expect(c.triggerMet).toBe(true);
    expect(c.bracket).toEqual([40000, 80000]);
    expect(c.letterSafe).toEqual(["adm"]);
    expect(c.reserve).toEqual(["res"]);
  });
  it("does not count a trigger met by evidence that is not in the record yet", () => {
    const v = sample();
    v.positions.trigger.met_by = ["rpt"];
    expect(computeValuation(v, { walkaway: 30000 }).bracket).toEqual([20000, 40000]);
  });
  it("blocks when no walk-away is recorded and warns when the walk-away exceeds the evidence", () => {
    expect(computeValuation(sample()).findings.some((f) => f.level === "block")).toBe(true);
    expect(computeValuation(sample(), { walkaway: 60000 }).findings.map((f) => f.text).join()).toMatch(/above the evidence-weighted value/);
  });
});

describe("valuation files", () => {
  it("every internal/private/negotiation/*.valuation.json validates", () => {
    const dir = path.join(ROOT, LEDGER_DIR);
    const files = fs.readdirSync(dir).filter((f) => f.endsWith(".valuation.json"));
    expect(files.length).toBeGreaterThan(0);
    for (const f of files) expect(validateValuation(JSON.parse(fs.readFileSync(path.join(dir, f), "utf8"))), f).toEqual([]);
  });
});
