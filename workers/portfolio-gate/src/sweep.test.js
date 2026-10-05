import { describe, expect, it, vi } from "vitest";
import { CHECK_NAME } from "./constants.mjs";
import { sweepStaleChecks } from "./sweep.mjs";

const NOW = Date.parse("2026-10-05T12:00:00Z");
const MIN = 60_000;

function github(runs) {
  return {
    listOpenPulls: vi.fn(async () => [
      { number: 1, base: { ref: "main" }, head: { sha: "a".repeat(40) } },
      { number: 2, base: { ref: "feature" }, head: { sha: "b".repeat(40) } },
    ]),
    listCheckRuns: vi.fn(async () => runs),
    completeCheckRun: vi.fn(async () => ({})),
  };
}

describe("sweepStaleChecks", () => {
  it("fails in-progress gate runs older than the limit", async () => {
    const gh = github([
      { id: 10, name: CHECK_NAME, status: "in_progress", started_at: new Date(NOW - 30 * MIN).toISOString() },
      { id: 11, name: CHECK_NAME, status: "in_progress", started_at: new Date(NOW - 5 * MIN).toISOString() },
      { id: 12, name: CHECK_NAME, status: "completed", started_at: new Date(NOW - 90 * MIN).toISOString() },
      { id: 13, name: "other", status: "in_progress", started_at: new Date(NOW - 90 * MIN).toISOString() },
    ]);
    const swept = await sweepStaleChecks({ github: gh, now: NOW, maxAgeMs: 17 * MIN });
    expect(swept).toEqual([{ pr: 1, checkRunId: 10 }]);
    expect(gh.listCheckRuns).toHaveBeenCalledOnce();
    const call = gh.completeCheckRun.mock.calls[0][0];
    expect(call).toMatchObject({ id: 10, conclusion: "failure" });
    expect(call.output.title).toContain("lost its runner");
  });
});
