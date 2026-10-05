import { buildCheckOutput, failClosedConclusion } from "./check.mjs";
import { CHECK_NAME, DEFAULT_TIMEOUT_MS } from "./constants.mjs";
import { createGitHubClient, getInstallationToken } from "./github.mjs";

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

/**
 * Create / update the portfolio-gate Check Run. Fail-closed: any start,
 * timeout, or runner error concludes `failure` (never `neutral`).
 */
export async function executeGateJob({
  job,
  github,
  getRunner,
  timeoutMs = DEFAULT_TIMEOUT_MS,
  skipRunner = false,
  skipReason = "",
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
// the GateOrchestrator Durable Object; its alarm (15-minute wall limit) runs
// it. The job is dequeued before it runs, so an alarm retry never runs the
// same webhook twice; a run that dies anyway is failed by the stale sweep.

export async function queueJob(storage, job, now = Date.now()) {
  await storage.put("job", job);
  await storage.setAlarm(now);
  return { queued: true, sha: job.sha };
}

export async function drainQueuedJob(storage, run) {
  const job = await storage.get("job");
  if (!job) return null;
  await storage.delete("job");
  return run(job);
}

/**
 * Mint a token, run the gate, and always stop the container afterwards so a
 * finished run does not hold one of the `max_instances` slots for the full
 * `sleepAfter` window.
 */
export async function runGateJob({
  job,
  env,
  getRunner,
  getToken = getInstallationToken,
  makeClient = createGitHubClient,
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
