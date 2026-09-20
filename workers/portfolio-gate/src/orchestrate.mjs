import { buildCheckOutput, failClosedConclusion } from "./check.mjs";
import { CHECK_NAME, DEFAULT_TIMEOUT_MS } from "./constants.mjs";

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
