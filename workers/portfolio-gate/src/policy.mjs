// Webhook routing policy. Only pull_request events targeting main start a
// run. Other bases are a no-op (200, no Check Run, no container).

import { ALLOWED_REPO, CHECK_NAME, PR_ACTIONS, SHA_RE } from "./constants.mjs";

export function isAllowedRepo(fullName, allowed = ALLOWED_REPO) {
  return typeof fullName === "string" && fullName === allowed;
}

export function isMainBase(ref) {
  return ref === "main";
}

export function extractPrJob(payload, allowedRepo = ALLOWED_REPO) {
  const pr = payload?.pull_request || {};
  const head = pr.head || {};
  const sha = typeof head.sha === "string" ? head.sha : "";
  const before = typeof payload?.before === "string" && SHA_RE.test(payload.before) ? payload.before : null;
  return {
    sha,
    beforeSha: before && before.toLowerCase() !== sha.toLowerCase() ? before : null,
    prNumber: Number(payload?.number || pr.number || 0) || null,
    cloneUrl: `https://github.com/${allowedRepo}.git`,
    headRepo: head.repo?.full_name || null,
    baseRef: pr.base?.ref || null,
    installationId: payload?.installation?.id ?? null,
    event: "pull_request",
    action: payload?.action || null,
  };
}

export function extractRerequestJob(payload, allowedRepo = ALLOWED_REPO) {
  const run = payload?.check_run || {};
  const sha = typeof run.head_sha === "string" ? run.head_sha : "";
  const prs = Array.isArray(run.pull_requests) ? run.pull_requests : [];
  const targetingMain = prs.find((pr) => isMainBase(pr?.base?.ref));
  return {
    sha,
    beforeSha: null,
    prNumber: targetingMain?.number ?? prs[0]?.number ?? null,
    cloneUrl: `https://github.com/${allowedRepo}.git`,
    headRepo: allowedRepo,
    baseRef: targetingMain?.base?.ref || prs[0]?.base?.ref || null,
    installationId: payload?.installation?.id ?? null,
    event: "check_run",
    action: payload?.action || null,
    checkRunId: run.id ?? null,
  };
}

/**
 * @returns {{
 *   action: "pong" | "ignore" | "run" | "fail",
 *   reason?: string,
 *   job?: object
 * }}
 */
export function decideWebhookAction(eventName, payload, { allowedRepo = ALLOWED_REPO } = {}) {
  if (eventName === "ping") {
    return { action: "pong" };
  }

  const repo = payload?.repository?.full_name;
  if (eventName === "pull_request") {
    if (!PR_ACTIONS.has(payload?.action)) {
      return { action: "ignore", reason: `pull_request ${payload?.action || "unknown"}` };
    }
    if (!isAllowedRepo(repo, allowedRepo)) {
      return { action: "ignore", reason: "repository not allowed" };
    }
    if (!isMainBase(payload?.pull_request?.base?.ref)) {
      return { action: "ignore", reason: "base is not main" };
    }
    const job = extractPrJob(payload, allowedRepo);
    if (!SHA_RE.test(job.sha)) {
      return { action: "fail", reason: "missing or invalid head SHA", job };
    }
    if (!isAllowedRepo(job.headRepo, allowedRepo)) {
      return {
        action: "fail",
        reason: "fork heads are refused — portfolio-gate clones only the installation repository",
        job,
      };
    }
    return { action: "run", job };
  }

  if (eventName === "check_run") {
    if (payload?.action !== "rerequested") {
      return { action: "ignore", reason: `check_run ${payload?.action || "unknown"}` };
    }
    if (payload?.check_run?.name !== CHECK_NAME) {
      return { action: "ignore", reason: "check name is not portfolio-gate" };
    }
    if (!isAllowedRepo(repo, allowedRepo)) {
      return { action: "ignore", reason: "repository not allowed" };
    }
    const job = extractRerequestJob(payload, allowedRepo);
    if (!isMainBase(job.baseRef)) {
      return { action: "ignore", reason: "rerequest is not on a PR targeting main" };
    }
    if (!SHA_RE.test(job.sha)) {
      return { action: "fail", reason: "missing or invalid head SHA", job };
    }
    return { action: "run", job };
  }

  return { action: "ignore", reason: `event ${eventName || "unknown"}` };
}
