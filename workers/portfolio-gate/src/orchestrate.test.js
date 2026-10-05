import { describe, expect, it, vi } from "vitest";
import { CHECK_NAME } from "./constants.mjs";
import { drainQueuedJob, executeGateJob, queueJob, runGateJob } from "./orchestrate.mjs";

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

describe("queued execution", () => {
  function memoryStorage() {
    const data = new Map();
    let alarm = null;
    return {
      data,
      get alarm() {
        return alarm;
      },
      put: async (k, v) => void data.set(k, v),
      get: async (k) => data.get(k),
      delete: async (k) => void data.delete(k),
      setAlarm: async (t) => {
        alarm = t;
      },
    };
  }

  it("queueJob stores the job and arms an immediate alarm", async () => {
    const storage = memoryStorage();
    await queueJob(storage, { sha: SHA }, 1234);
    expect(storage.data.get("job")).toEqual({ sha: SHA });
    expect(storage.alarm).toBe(1234);
  });

  it("drainQueuedJob dequeues before running, so a retried alarm is a no-op", async () => {
    const storage = memoryStorage();
    await queueJob(storage, { sha: SHA });
    const run = vi.fn(async () => {
      expect(storage.data.has("job")).toBe(false);
      throw new Error("alarm killed mid-run");
    });
    await expect(drainQueuedJob(storage, run)).rejects.toThrow("alarm killed");
    expect(await drainQueuedJob(storage, run)).toBeNull();
    expect(run).toHaveBeenCalledOnce();
  });

  it("runGateJob stops the container after the run", async () => {
    const github = mockGithub();
    const runner = { runJob: vi.fn(async () => ({ ok: true })), cancel: vi.fn(async () => ({})) };
    const result = await runGateJob({
      job: { sha: SHA, timeoutMs: 1000 },
      env: { GITHUB_REPO: "o/r" },
      getRunner: () => runner,
      getToken: async () => "tok",
      makeClient: () => github,
    });
    expect(result.conclusion).toBe("success");
    expect(runner.runJob.mock.calls[0][0].installationToken).toBe("tok");
    expect(runner.cancel).toHaveBeenCalledWith("finished");
  });

  it("runGateJob fails a refused job without starting a container", async () => {
    const github = mockGithub();
    const getRunner = vi.fn(() => ({ runJob: vi.fn(), cancel: vi.fn() }));
    const result = await runGateJob({
      job: { sha: SHA, refusal: "fork head" },
      env: { GITHUB_REPO: "o/r" },
      getRunner,
      getToken: async () => "tok",
      makeClient: () => github,
    });
    expect(result.conclusion).toBe("failure");
    expect(getRunner).not.toHaveBeenCalled();
  });
});
