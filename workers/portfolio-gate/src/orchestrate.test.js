import { describe, expect, it, vi } from "vitest";
import { CHECK_NAME, GATE_QUEUE_NAME, GATE_RUNNER_ID } from "./constants.mjs";
import {
  drainQueuedJob,
  executeGateJob,
  planQueueChange,
  queueJob,
  runGateJob,
  sameSha,
  supersedes,
} from "./orchestrate.mjs";

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

  it("concludes cancelled (not failure) when the in-flight run was preempted", async () => {
    const github = mockGithub();
    const result = await executeGateJob({
      job: { sha: SHA },
      github,
      getRunner: () => ({
        runJob: async () => ({ ok: false, reason: "container destroyed" }),
      }),
      isPreempted: async () => true,
    });
    expect(result.conclusion).toBe("cancelled");
    expect(github.completeCheckRun.mock.calls[0][0].conclusion).toBe("cancelled");
    expect(github.completeCheckRun.mock.calls[0][0].output.title).toBe("portfolio-gate cancelled");
  });

  it("concludes cancelled when a preempted run throws instead of returning", async () => {
    const github = mockGithub();
    const result = await executeGateJob({
      job: { sha: SHA },
      github,
      getRunner: () => ({
        runJob: async () => {
          throw new Error("container destroyed");
        },
      }),
      isPreempted: async () => true,
    });
    expect(result.conclusion).toBe("cancelled");
    expect(github.completeCheckRun.mock.calls[0][0].conclusion).toBe("cancelled");
  });
});

describe("planQueueChange", () => {
  const jobA = { sha: PREV, prNumber: 42, event: "pull_request" };
  const jobB = { sha: SHA, prNumber: 42, beforeSha: PREV, event: "pull_request" };
  const other = { sha: "ffffffffffffffffffffffffffffffffffffffff", prNumber: 7, event: "pull_request" };

  it("appends a new job onto an empty queue", () => {
    const plan = planQueueChange([], jobA);
    expect(plan.queue).toEqual([jobA]);
    expect(plan.enqueued).toBe(true);
    expect(plan.dropped).toEqual([]);
    expect(plan.preemptSha).toBeNull();
  });

  it("keeps unrelated PRs in FIFO order", () => {
    const plan = planQueueChange([other], jobA);
    expect(plan.queue).toEqual([other, jobA]);
    expect(plan.dropped).toEqual([]);
  });

  it("drops a waiting SHA when the same PR pushes a newer one", () => {
    const plan = planQueueChange([jobA, other], jobB);
    expect(plan.queue).toEqual([other, jobB]);
    expect(plan.dropped).toEqual([jobA]);
    expect(plan.enqueued).toBe(true);
  });

  it("does not queue a duplicate SHA that is already waiting", () => {
    const plan = planQueueChange([jobA], jobA);
    expect(plan.queue).toEqual([jobA]);
    expect(plan.enqueued).toBe(false);
    expect(plan.alreadyQueued).toBe(true);
  });

  it("does not queue a pull_request retry for a SHA that is already running", () => {
    const plan = planQueueChange([], jobA, jobA);
    expect(plan.enqueued).toBe(false);
    expect(plan.alreadyRunningSame).toBe(true);
    expect(plan.queue).toEqual([]);
  });

  it("queues a check_run rerequest after the same SHA finishes", () => {
    const rerequest = { ...jobA, event: "check_run" };
    const plan = planQueueChange([], rerequest, jobA);
    expect(plan.enqueued).toBe(true);
    expect(plan.queue).toEqual([rerequest]);
  });

  it("preempts an in-flight run for the same PR", () => {
    const plan = planQueueChange([], jobB, jobA);
    expect(plan.preemptSha).toBe(PREV);
    expect(plan.queue).toEqual([jobB]);
  });

  it("sameSha / supersedes are case-insensitive on the hex", () => {
    expect(sameSha({ sha: SHA.toUpperCase() }, { sha: SHA })).toBe(true);
    expect(supersedes({ sha: SHA, beforeSha: PREV.toUpperCase() }, { sha: PREV })).toBe(true);
    expect(supersedes({ sha: SHA, prNumber: 1 }, { sha: PREV, prNumber: 2 })).toBe(false);
  });
});

describe("singleton names", () => {
  it("pins the orchestrator and runner to one shared id", () => {
    expect(GATE_QUEUE_NAME).toBe("gate");
    expect(GATE_RUNNER_ID).toBe("gate");
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
    expect(storage.data.get("queue")).toEqual([{ sha: SHA }]);
    expect(storage.alarm).toBe(1234);
  });

  it("drainQueuedJob dequeues before running, so a retried alarm is a no-op", async () => {
    const storage = memoryStorage();
    await queueJob(storage, { sha: SHA });
    const run = vi.fn(async () => {
      expect(storage.data.get("queue")).toEqual([]);
      expect(storage.data.get("running").sha).toBe(SHA);
      throw new Error("alarm killed mid-run");
    });
    await expect(drainQueuedJob(storage, run)).rejects.toThrow("alarm killed");
    expect(await drainQueuedJob(storage, run)).toBeNull();
    expect(run).toHaveBeenCalledOnce();
    expect(storage.data.has("running")).toBe(false);
  });

  it("FIFO-queues a second SHA and arms the next alarm after the first run", async () => {
    const storage = memoryStorage();
    await queueJob(storage, { sha: PREV, prNumber: 1 }, 1);
    await queueJob(storage, { sha: SHA, prNumber: 2 }, 2);
    expect(storage.data.get("queue").map((j) => j.sha)).toEqual([PREV, SHA]);

    const seen = [];
    await drainQueuedJob(storage, async (job) => {
      seen.push(job.sha);
    }, 10);
    expect(seen).toEqual([PREV]);
    expect(storage.data.get("queue").map((j) => j.sha)).toEqual([SHA]);
    expect(storage.alarm).toBeGreaterThanOrEqual(10);

    await drainQueuedJob(storage, async (job) => {
      seen.push(job.sha);
    });
    expect(seen).toEqual([PREV, SHA]);
    expect(storage.data.get("queue") || []).toEqual([]);
  });

  it("records a preempt when a newer SHA arrives while the previous one is running", async () => {
    const storage = memoryStorage();
    await queueJob(storage, { sha: PREV, prNumber: 42, event: "pull_request" });
    await storage.put("running", { sha: PREV, prNumber: 42, event: "pull_request" });
    // Simulate: PREV already dequeued and running; a stale copy is not in the queue.
    await storage.put("queue", []);
    const result = await queueJob(storage, {
      sha: SHA,
      prNumber: 42,
      beforeSha: PREV,
      event: "pull_request",
    });
    expect(result.preemptSha).toBe(PREV);
    expect(result.enqueued).toBe(true);
    expect(storage.data.get("queue")).toEqual([
      expect.objectContaining({ sha: SHA, prNumber: 42 }),
    ]);
    expect(storage.data.get(`preempted:${PREV}`)).toBe(true);
  });

  it("does not start a superseded waiting SHA", async () => {
    const storage = memoryStorage();
    await queueJob(storage, { sha: PREV, prNumber: 42, event: "pull_request" });
    await queueJob(storage, {
      sha: SHA,
      prNumber: 42,
      beforeSha: PREV,
      event: "pull_request",
    });
    expect(storage.data.get("queue").map((j) => j.sha)).toEqual([SHA]);
    const seen = [];
    await drainQueuedJob(storage, async (job) => {
      seen.push(job.sha);
    });
    expect(seen).toEqual([SHA]);
    expect(await drainQueuedJob(storage, async (job) => seen.push(job.sha))).toBeNull();
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
