// Cloudflare Worker: GitHub App webhook → Check Run `portfolio-gate`.
//
// Phase 2 remote gate. There is no `.github/workflows/`. The laptop gate is
// still `.githooks/pre-push` / `npm run gate`. This Worker posts the required
// Check Run for PRs whose base is `main`.
//
// Fail-closed:
//   - invalid webhook signature → 401, no container, no success conclusion
//   - container cannot start / no result within GATE_TIMEOUT_MS → Check Run failure
//   - never conclude `neutral`

import { getContainer } from "@cloudflare/containers";
import { handleWebhook, healthBody, json } from "./handler.mjs";
import { GateRunner } from "./runner.mjs";

export { GateRunner };

export default {
  async fetch(request, env, ctx) {
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
        ctx,
        getRunner: (sha) => getContainer(env.GATE_RUNNER, sha),
      });
    }

    return json({ error: "not found" }, 404);
  },
};
