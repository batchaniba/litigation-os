import { describe, expect, it } from "vitest";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import {
  CLOCK_STATUSES,
  CLOSED_CLOCK_SQL,
  LEGACY_CLOCK_STATUS_MAP,
  STORED_CLOCK_STATUSES,
  clockStatusIssue,
  isClockOverdue,
  isClosedClockStatus,
  isStoredClockStatus,
  normalizeClockStatus,
  validateClockRows,
} from "./clock-status.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const repoRoot = path.resolve(here, "../../..");

describe("canonical stored clock statuses", () => {
  it("is exactly open | set | contingent | vacated | satisfied", () => {
    expect([...STORED_CLOCK_STATUSES]).toEqual([
      "open",
      "set",
      "contingent",
      "vacated",
      "satisfied",
    ]);
    expect(CLOCK_STATUSES.has("overdue")).toBe(false);
    expect(CLOCK_STATUSES.has("undated")).toBe(false);
    expect(CLOCK_STATUSES.has("retired")).toBe(false);
    expect(CLOCK_STATUSES.has("cancelled")).toBe(false);
  });

  it("accepts each stored status and rejects retired / cancelled / overdue", () => {
    for (const status of STORED_CLOCK_STATUSES) {
      expect(isStoredClockStatus(status)).toBe(true);
      expect(clockStatusIssue(status)).toBeNull();
      expect(validateClockRows([{ id: "ok", kind: "deadline", status }])).toEqual([]);
    }

    expect(validateClockRows([{ id: "x", kind: "deadline", status: "retired" }])).toEqual([
      'clocks.json[0]: unknown stored clock status "retired" (allowed: open | set | contingent | vacated | satisfied)',
    ]);
    expect(validateClockRows([{ id: "x", kind: "deadline", status: "cancelled" }])).toEqual([
      'clocks.json[0]: unknown stored clock status "cancelled" (allowed: open | set | contingent | vacated | satisfied)',
    ]);
    expect(validateClockRows([{ id: "x", kind: "deadline", status: "overdue" }])).toEqual([
      'clocks.json[0]: "overdue" is derived from date + open/set, never a stored status',
    ]);
  });

  it("maps legacy D1 aliases to vacated and still treats them as closed", () => {
    expect(LEGACY_CLOCK_STATUS_MAP).toEqual({
      retired: "vacated",
      cancelled: "vacated",
      canceled: "vacated",
    });
    expect(normalizeClockStatus("retired")).toBe("vacated");
    expect(normalizeClockStatus("cancelled")).toBe("vacated");
    expect(isClosedClockStatus("retired")).toBe(true);
    expect(isClosedClockStatus("satisfied")).toBe(true);
    expect(isClosedClockStatus("open")).toBe(false);
    expect(CLOSED_CLOCK_SQL).toBe("('vacated','satisfied','retired','cancelled','canceled')");
  });

  it("derives overdue from date + open/set and never from contingent or dead", () => {
    expect(isClockOverdue({ date: "2026-09-01", status: "open" }, "2026-09-17")).toBe(true);
    expect(isClockOverdue({ date: "2026-09-01", status: "set" }, "2026-09-17")).toBe(true);
    expect(isClockOverdue({ date: "2026-09-01", status: "contingent" }, "2026-09-17")).toBe(false);
    expect(isClockOverdue({ date: "2026-09-01", status: "vacated" }, "2026-09-17")).toBe(false);
    expect(isClockOverdue({ date: "2026-09-20", status: "open" }, "2026-09-17")).toBe(false);
  });

  it("keeps schema.json and D1 schema.sql comments on the same stored list", () => {
    const graphSchema = JSON.parse(
      fs.readFileSync(path.join(repoRoot, "internal/src/data/index/schema.json"), "utf8"),
    );
    expect(graphSchema.$defs.clock.properties.status.enum).toEqual([...STORED_CLOCK_STATUSES]);

    const sql = fs.readFileSync(path.join(repoRoot, "workers/doc-api/schema.sql"), "utf8");
    expect(sql).toMatch(/status\s+TEXT\s+-- open \| set \| contingent \| vacated \| satisfied/);
    expect(sql).not.toMatch(/retired \| cancelled/);
  });
});
