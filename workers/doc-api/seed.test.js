import { execFileSync } from "node:child_process";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { describe, expect, it } from "vitest";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const SEED = path.join(HERE, "seed.mjs");

function generatedClockRows() {
  const sql = execFileSync(process.execPath, [SEED], {
    encoding: "utf8",
    maxBuffer: 4 * 1024 * 1024,
  });
  return sql.split("\n").filter((line) => line.startsWith("INSERT INTO clocks"));
}

function hasClock(rows, matter, date) {
  return rows.some(
    (line) => line.includes(`VALUES (${matter},`) && line.includes(`'${date}'`),
  );
}

describe("D1 seed clock filtering", () => {
  it("omits retired clocks and keeps live dated clocks", () => {
    const rows = generatedClockRows();

    // Matter 26: Rule 15 window was satisfied; live remand/hearing clocks remain.
    expect(hasClock(rows, 26, "2026-09-16")).toBe(false);
    expect(hasClock(rows, 26, "2026-09-21")).toBe(true);
    expect(hasClock(rows, 26, "2026-10-07")).toBe(true);

    // Matter 30: anticipated Sep. 16 filing was satisfied; outer GCA window remains.
    expect(hasClock(rows, 30, "2026-09-16")).toBe(false);
    expect(hasClock(rows, 30, "2027-03-01")).toBe(true);

    // Matter 24: the Sep. 30 hearing was vacated; current November clocks remain.
    expect(hasClock(rows, 24, "2026-09-30")).toBe(false);
    expect(hasClock(rows, 24, "2026-11-16")).toBe(true);
    expect(hasClock(rows, 24, "2026-11-20")).toBe(true);
  });
});
