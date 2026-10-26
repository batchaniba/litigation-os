import { buildCheckOutput, failClosedConclusion } from "./check.mjs";
import { CHECK_NAME, DEFAULT_TIMEOUT_MS } from "./constants.mjs";
import { createGitHubClient, getInstallationToken } from "./github.mjs";

const QUEUE_KEY = "queue";
const RUNNING_KEY = "running";

function timeoutError(timeoutMs) {
  const err = new Error(`No result within ${timeoutMs}ms`);
  err.code = "gate_timeout";
  return err;
}

function withTimeout(promise, timeoutMs) {
  let timer;
  const timeout = new Promise((_, reject) => {
    timer = setTimeout(() => reject(timeoutError(timeoutMs)), timeoutMs);
  });
  return Promise.race([promise, timeout]).finally(() => clearTimeout(timer));
}

function preemptKey(sha) {
  return `preempted:${String(sha || "").toLowerCase()}`;
}

export function sameSha(a, b) {
  return Boolean(a?.sha && b?.sha && String(a.sha).toLowerCase() === String(b.sha).toLowerCase());
}

/** True when `incoming` should replace `existing` instead of running both. */
export function supersedes(incoming, existing) {
  if (!incoming || !existing || sameSha(incoming, existing)) return false;
  if (
    incoming.beforeSha &&
    existing.sha &&
    String(incoming.beforeSha).toLowerCase() === String(existing.sha).toLowerCase()
  ) {
    return true;
  }
  return Boolean(incoming.prNumber && existing.prNumber && incoming.prNumber === existing.prNumber);
}

/**
 * Pure FIFO + supersede planner. One container: newer SHAs for the same PR
 * drop waiting jobs; a rerequest of a SHA that is already queued is a no-op.
 */
export function planQueueChange(queue, incoming, running = null) {
  const list = Array.isArray(queue) ? queue : [];
  const dropped = [];
  const kept = [];
  let alreadyQueued = false;

  for (const job of list) {
    if (sameSha(job, incoming)) {
      alreadyQueued = true;
      kept.push(job);
      continue;
    }
    if (supersedes(incoming, job)) {
      dropped.push(job);
      continue;
    }
    kept.push(job);
  }

  const preemptSha = running && supersedes(incoming, running) ? running.sha : null;
  const alreadyRunningSame = Boolean(
    running && sameSha(running, incoming) && incoming.event !== "check_run",
  );

  let enqueued = false;
  if (!alreadyQueued && !alreadyRunningSame) {
    kept.push(incoming);
    enqueued = true;
  }

  return {
    queue: kept,
    dropped,
    preemptSha,
    enqueued,
    alreadyQueued,
    alreadyRunningSame,
  };
}

async function completeFailure(github, { checkId, sha, reason, log, timeoutMs }) {
  const output = buildCheckOutput({
    ok: false,
    reason,
    log,
    sha,
    timeoutMs,
  });
  if (checkId) {
    await github.completeCheckRun({
      id: checkId,
      conclusion: failClosedConclusion(reason),
      output,
    });
    return checkId;
  }
  const created = await github.createCheckRun({
    sha,
    title: `${CHECK_NAME} failed`,
    summary: output.summary,
  });
  await github.completeCheckRun({
    id: created.id,
    conclusion: failClosedConclusion(reason),
    output,
  });
  return created.id;
}

async function concludeCancelled(github, { checkId, sha, reason }) {
  const short = sha ? String(sha).slice(0, 12) : "unknown";
  const output = {
    title: `${CHECK_NAME} cancelled`,
    summary: reason || `${CHECK_NAME} on ${short} was superseded by a newer push.`,
  };
  if (checkId) {
    await github.completeCheckRun({
      id: checkId,
      conclusion: "cancelled",
      output,
    });
  }
  return { checkRunId: checkId || null, conclusion: "cancelled", started: Boolean(checkId) };
}

/**
 * Create / update the portfolio-gate Check Run. Fail-closed: any start,
 * timeout, or runner error concludes `failure` (never `neutral`). A run that
 * was preempted by a newer SHA for the same PR concludes `cancelled`.
 */
export async function executeGateJob({
  job,
  github,
  getRunner,
  timeoutMs = DEFAULT_TIMEOUT_MS,
  skipRunner = false,
  skipReason = "",
  isPreempted,
}) {
  if (job.beforeSha) {
    try {
      await github.cancelPendingChecks(job.beforeSha, `superseded by ${job.sha.slice(0, 12)}`);
    } catch (err) {
      console.log(`cancel previous checks failed: ${String(err?.message || err).slice(0, 200)}`);
    }
    try {
      await getRunner(job.beforeSha).cancel("superseded");
    } catch {
      // previous SHA may have no live container
    }
  }

  if (skipRunner) {
    const checkId = await completeFailure(github, {
      sha: job.sha,
      reason: skipReason || "refused before start",
      log: "",
      timeoutMs,
    });
    return { checkRunId: checkId, conclusion: "failure", started: false };
  }

  let check = null;
  try {
    check = await github.createCheckRun({
      sha: job.sha,
      title: `${CHECK_NAME}`,
      summary: `Running ${CHECK_NAME} on ${job.sha.slice(0, 12)}…`,
    });
  } catch (err) {
    const checkId = await completeFailure(github, {
      sha: job.sha,
      reason: `could not create pending check: ${err?.message || err}`,
      log: "",
      timeoutMs,
    });
    return { checkRunId: checkId, conclusion: "failure", started: false };
  }

  try {
    const runner = getRunner(job.sha);
    const result = await withTimeout(runner.runJob(job), timeoutMs);
    if (!result?.ok && (await isPreempted?.(job.sha))) {
      return concludeCancelled(github, {
        checkId: check.id,
        sha: job.sha,
        reason: `${CHECK_NAME} on ${job.sha.slice(0, 12)} was superseded by a newer push.`,
      });
    }
    const ok = Boolean(result?.ok);
    const output = buildCheckOutput({
      ok,
      reason: result?.reason,
      log: result?.log,
      sha: job.sha,
      timeoutMs,
    });
    await github.completeCheckRun({
      id: check.id,
      conclusion: ok ? "success" : failClosedConclusion(result?.reason),
      output,
    });
    return { checkRunId: check.id, conclusion: ok ? "success" : "failure", started: true };
  } catch (err) {
    if (await isPreempted?.(job.sha)) {
      return concludeCancelled(github, {
        checkId: check.id,
        sha: job.sha,
        reason: `${CHECK_NAME} on ${job.sha.slice(0, 12)} was superseded by a newer push.`,
      });
    }
    const reason =
      err?.code === "gate_timeout"
        ? `No result within ${timeoutMs}ms`
        : `container could not start or finish: ${err?.message || err}`;
    await completeFailure(github, {
      checkId: check.id,
      sha: job.sha,
      reason,
      log: err?.log || "",
      timeoutMs,
    });
    return { checkRunId: check.id, conclusion: "failure", started: true, error: reason };
  }
}

// --- queued execution --------------------------------------------------------
// The webhook must answer GitHub fast, and work handed to ctx.waitUntil() is
// cancelled 30 seconds after that response. A gate run (clone, npm ci, gate)
// takes minutes, so running it there killed every full run mid-flight and left
// the Check Run `in_progress` forever. The webhook now only queues the job on
// the singleton GateOrchestrator Durable Object; its alarm (15-minute wall
// limit) runs one job at a time. Extra SHAs wait in FIFO instead of starting
// another container (max_instances = 1). The job is dequeued before it runs,
// so an alarm retry never runs the same webhook twice; a run that dies anyway
// is failed by the stale sweep.

export async function queueJob(storage, job, now = Date.now()) {
  const queue = (await storage.get(QUEUE_KEY)) || [];
  const running = (await storage.get(RUNNING_KEY)) || null;
  const plan = planQueueChange(queue, job, running);
  await storage.put(QUEUE_KEY, plan.queue);
  if (plan.preemptSha) {
    await storage.put(preemptKey(plan.preemptSha), true);
  }
  // Always arm. If an alarm is already executing this becomes the next one,
  // so a job that arrived while the container was busy still runs.
  await storage.setAlarm(now);
  return {
    queued: plan.enqueued || plan.alreadyQueued || plan.alreadyRunningSame,
    sha: job.sha,
    dropped: plan.dropped.map((queued) => queued.sha),
    preemptSha: plan.preemptSha,
    enqueued: plan.enqueued,
  };
}

export async function drainQueuedJob(storage, run, now = Date.now()) {
  const queue = (await storage.get(QUEUE_KEY)) || [];
  if (queue.length === 0) {
    await storage.delete(RUNNING_KEY);
    return null;
  }
  const job = queue[0];
  await storage.put(QUEUE_KEY, queue.slice(1));
  await storage.put(RUNNING_KEY, {
    sha: job.sha,
    prNumber: job.prNumber ?? null,
    event: job.event ?? null,
    startedAt: now,
  });
  try {
    return await run(job);
  } finally {
    await storage.delete(RUNNING_KEY);
    const remaining = (await storage.get(QUEUE_KEY)) || [];
    if (remaining.length > 0) {
      await storage.setAlarm(Date.now());
    }
  }
}

export async function isShaPreempted(storage, sha) {
  return Boolean(await storage.get(preemptKey(sha)));
}

export async function clearPreempted(storage, sha) {
  await storage.delete(preemptKey(sha));
}

/**
 * Mint a token, run the gate, and always stop the container afterwards so a
 * finished run does not hold the `max_instances` slot for the `sleepAfter`
 * window.
 */
export async function runGateJob({
  job,
  env,
  getRunner,
  getToken = getInstallationToken,
  makeClient = createGitHubClient,
  isPreempted,
}) {
  const token = await getToken(env, job.installationId || env.GITHUB_APP_INSTALLATION_ID);
  const github = makeClient({ token, repo: env.GITHUB_REPO });
  const refused = Boolean(job.refusal);
  try {
    return await executeGateJob({
      job: { ...job, installationToken: token },
      github,
      getRunner,
      timeoutMs: job.timeoutMs,
      skipRunner: refused,
      skipReason: job.refusal || "",
      isPreempted,
    });
  } finally {
    if (!refused) {
      try {
        await getRunner(job.sha).cancel("finished");
      } catch {
        // already stopped
      }
    }
  }
}
