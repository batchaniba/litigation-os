// Cloudflare Worker: GitHub App webhook → Check Run `portfolio-gate`, plus
// the daily deadline digest read from `main`.
//
// Phase 2 remote gate. There is no `.github/workflows/`. The laptop gate is
// still `.githooks/pre-push` / `npm run gate`. This Worker posts the required
// Check Run for PRs whose base is `main`.
//
// Fail-closed:
//   - invalid webhook signature → 401, no container, no success conclusion
//   - container cannot start / no result within GATE_TIMEOUT_MS → Check Run failure
//   - runner lost without reporting → stale sweep concludes failure
//   - never conclude `neutral`

import { GATE_QUEUE_NAME } from "./constants.mjs";
import { handleWebhook, healthBody, json, timeoutMs } from "./handler.mjs";
import { GateRunner } from "./runner.mjs";
import { GateOrchestrator } from "./orchestrator.mjs";
import { createGitHubClient, getInstallationToken, resolveInstallationId } from "./github.mjs";
import { composeDigest, deliverDigest } from "./digest.mjs";
import { sweepStaleChecks } from "./sweep.mjs";

export { GateRunner, GateOrchestrator };

// Must match [triggers] crons in wrangler.toml.
const SWEEP_CRON = "*/30 * * * *";
// Grace past the gate timeout before a still-running check counts as lost.
const SWEEP_GRACE_MS = 5 * 60 * 1000;

async function githubFor(env) {
  const token = await getInstallationToken(env, await resolveInstallationId(env));
  return createGitHubClient({ token, repo: env.GITHUB_REPO });
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (request.method === "GET" && url.pathname === "/") {
      return json(healthBody(env));
    }

    if (request.method === "POST" && url.pathname === "/webhook") {
      const rawBody = await request.text();
      return handleWebhook({
        rawBody,
        signatureHeader: request.headers.get("x-hub-signature-256"),
        eventName: request.headers.get("x-github-event"),
        env,
        enqueue: (job) =>
          env.GATE_ORCHESTRATOR.get(env.GATE_ORCHESTRATOR.idFromName(GATE_QUEUE_NAME)).enqueue(job),
      });
    }

    return json({ error: "not found" }, 404);
  },

  async scheduled(event, env) {
    if (event.cron === SWEEP_CRON) {
      const github = await githubFor(env);
      const swept = await sweepStaleChecks({ github, maxAgeMs: timeoutMs(env) + SWEEP_GRACE_MS });
      if (swept.length) console.log(`portfolio-gate swept ${swept.length} stale check(s)`, swept);
      return;
    }

    // Daily digest. composeDigest never throws: a failure to read `main`
    // becomes a "digest failed" message, not silence.
    let payload;
    try {
      payload = await composeDigest({ github: await githubFor(env), now: new Date(event.scheduledTime) });
    } catch (err) {
      payload = {
        type: "deadline_digest_error",
        text: `DEADLINE DIGEST FAILED — GitHub App auth: ${String(err?.message || err).slice(0, 200)}. Today's deadlines were NOT checked.`,
      };
    }
    await deliverDigest(env, payload);
  },
};
