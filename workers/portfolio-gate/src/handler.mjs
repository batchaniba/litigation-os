import { CHECK_NAME, DEFAULT_TIMEOUT_MS } from "./constants.mjs";
import { createGitHubClient, getInstallationToken } from "./github.mjs";
import { executeGateJob } from "./orchestrate.mjs";
import { decideWebhookAction } from "./policy.mjs";
import { verifyGitHubSignature } from "./webhook.mjs";

export function json(body, status = 200) {
  return new Response(JSON.stringify(body, null, 2), {
    status,
    headers: { "content-type": "application/json", "cache-control": "no-store" },
  });
}

export function timeoutMs(env) {
  const n = Number(env.GATE_TIMEOUT_MS);
  return Number.isFinite(n) && n > 0 ? n : DEFAULT_TIMEOUT_MS;
}

export function healthBody(env) {
  return {
    ok: true,
    worker: "ilp-portfolio-gate",
    check: CHECK_NAME,
    timeout_ms: timeoutMs(env),
    configured: {
      appId: Boolean(env.GITHUB_APP_ID),
      privateKey: Boolean(env.GITHUB_APP_PRIVATE_KEY),
      webhookSecret: Boolean(env.GITHUB_WEBHOOK_SECRET),
      installationId: Boolean(env.GITHUB_APP_INSTALLATION_ID),
      repo: Boolean(env.GITHUB_REPO),
    },
  };
}

/**
 * @param {object} args
 * @param {string} args.rawBody
 * @param {string|null} args.signatureHeader
 * @param {string|null} args.eventName
 * @param {object} args.env
 * @param {{ waitUntil: (p: Promise<unknown>) => void }} args.ctx
 * @param {(sha: string) => { runJob: Function, cancel?: Function }} [args.getRunner]
 */
export async function handleWebhook({ rawBody, signatureHeader, eventName, env, ctx, getRunner }) {
  const verified = await verifyGitHubSignature(rawBody, signatureHeader, env.GITHUB_WEBHOOK_SECRET);
  if (!verified) {
    return json({ ok: false, error: "invalid signature" }, 401);
  }

  let payload;
  try {
    payload = JSON.parse(rawBody);
  } catch {
    return json({ ok: false, error: "invalid JSON" }, 400);
  }

  const allowedRepo = env.GITHUB_REPO || "";
  const decision = decideWebhookAction(eventName, payload, { allowedRepo });

  if (decision.action === "pong") {
    return json({ ok: true, event: "ping" });
  }
  if (decision.action === "ignore") {
    return json({ ok: true, ignored: true, reason: decision.reason });
  }

  const job = decision.job;
  job.timeoutMs = timeoutMs(env);

  const kick = async () => {
    const installationId = job.installationId || env.GITHUB_APP_INSTALLATION_ID;
    const token = await getInstallationToken(env, installationId);
    job.installationToken = token;
    const github = createGitHubClient({ token, repo: allowedRepo });
    return executeGateJob({
      job,
      github,
      timeoutMs: job.timeoutMs,
      skipRunner: decision.action === "fail",
      skipReason: decision.reason,
      getRunner,
    });
  };

  ctx.waitUntil(
    kick().catch((err) => {
      console.log(`portfolio-gate job failed: ${String(err?.message || err).slice(0, 240)}`);
    }),
  );

  return json(
    {
      ok: true,
      accepted: true,
      check: CHECK_NAME,
      sha: job.sha,
      action: decision.action,
    },
    202,
  );
}
