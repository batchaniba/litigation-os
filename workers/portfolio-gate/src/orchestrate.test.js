import { describe, expect, it, vi } from "vitest";
import { CHECK_NAME } from "./constants.mjs";
import { executeGateJob } from "./orchestrate.mjs";

const SHA = "dddddddddddddddddddddddddddddddddddddddd";
const PREV = "eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee";

function mockGithub(overrides = {}) {
  return {
    createCheckRun: vi.fn(async ({ sha }) => ({ id: 101, head_sha: sha, name: CHECK_NAME })),
    completeCheckRun: vi.fn(async (args) => args),
    cancelPendingChecks: vi.fn(async () => [99]),
    ...overrides,
  };
}

describe("executeGateJob", () => {
  it("posts success when the runner returns ok", async () => {
    const github = mockGithub();
    const runner = { runJob: vi.fn(async () => ({ ok: true, log: "gate passed" })), cancel: vi.fn() };
    const result = await executeGateJob({
      job: { sha: SHA },
      github,
      getRunner: () => runner,
    });
    expect(result.conclusion).toBe("success");
    expect(github.createCheckRun).toHaveBeenCalledOnce();
    expect(github.completeCheckRun.mock.calls[0][0].conclusion).toBe("success");
    expect(github.completeCheckRun.mock.calls[0][0].output.title).toBe("portfolio-gate passed");
  });

  it("concludes failure (not neutral) when the container cannot start", async () => {
    const github = mockGithub();
    const result = await executeGateJob({
      job: { sha: SHA },
      github,
      getRunner: () => ({
        runJob: async () => {
          throw new Error("no instance available");
        },
      }),
    });
    expect(result.conclusion).toBe("failure");
    expect(github.completeCheckRun.mock.calls[0][0].conclusion).toBe("failure");
    expect(github.completeCheckRun.mock.calls[0][0].output.summary).toMatch(/could not start/);
  });

  it("concludes failure (not neutral) when the runner does not return in time", async () => {
    const github = mockGithub();
    const result = await executeGateJob({
      job: { sha: SHA },
      github,
      timeoutMs: 20,
      getRunner: () => ({
        runJob: () => new Promise(() => {}),
      }),
    });
    expect(result.conclusion).toBe("failure");
    expect(github.completeCheckRun.mock.calls[0][0].conclusion).toBe("failure");
    expect(github.completeCheckRun.mock.calls[0][0].output.summary).toMatch(/No result within 20ms/);
  });

  it("concludes failure without starting a runner when skipRunner is set", async () => {
    const github = mockGithub();
    const runJob = vi.fn();
    const result = await executeGateJob({
      job: { sha: SHA },
      github,
      skipRunner: true,
      skipReason: "fork heads are refused",
      getRunner: () => ({ runJob }),
    });
    expect(runJob).not.toHaveBeenCalled();
    expect(result.conclusion).toBe("failure");
    expect(result.started).toBe(false);
    expect(github.completeCheckRun.mock.calls[0][0].conclusion).toBe("failure");
  });

  it("cancels older pending runs on the previous SHA when a new synchronize arrives", async () => {
    const github = mockGithub();
    const cancelled = [];
    const result = await executeGateJob({
      job: { sha: SHA, beforeSha: PREV },
      github,
      getRunner: (id) => ({
        runJob: async () => ({ ok: true, log: "ok" }),
        cancel: async (reason) => {
          cancelled.push({ id, reason });
        },
      }),
    });
    expect(result.conclusion).toBe("success");
    expect(github.cancelPendingChecks).toHaveBeenCalledWith(PREV, expect.stringMatching(/superseded/));
    expect(cancelled).toEqual([{ id: PREV, reason: "superseded" }]);
  });
});
