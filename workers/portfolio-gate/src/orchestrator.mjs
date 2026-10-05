// GateOrchestrator Durable Object: one instance per head SHA. The webhook
// queues the job here and returns; the alarm runs it with a 15-minute wall
// limit instead of the 30-second ctx.waitUntil() window that killed full
// runs. Logic lives in orchestrate.mjs so it is unit-tested without the
// Workers runtime.

import { DurableObject } from "cloudflare:workers";
import { getContainer } from "@cloudflare/containers";
import { drainQueuedJob, queueJob, runGateJob } from "./orchestrate.mjs";

export class GateOrchestrator extends DurableObject {
  async enqueue(job) {
    return queueJob(this.ctx.storage, job);
  }

  async alarm() {
    await drainQueuedJob(this.ctx.storage, (job) =>
      runGateJob({
        job,
        env: this.env,
        getRunner: (sha) => getContainer(this.env.GATE_RUNNER, sha),
      }).catch((err) => {
        console.log(`portfolio-gate job failed: ${String(err?.message || err).slice(0, 240)}`);
      }),
    );
  }
}
