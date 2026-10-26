// GateOrchestrator Durable Object: one singleton for every head SHA. The
// webhook queues the job here and returns; the alarm runs one job at a time
// with a 15-minute wall limit instead of the 30-second ctx.waitUntil() window
// that killed full runs. Logic lives in orchestrate.mjs so it is unit-tested
// without the Workers runtime.

import { DurableObject } from "cloudflare:workers";
import { getContainer } from "@cloudflare/containers";
import { GATE_RUNNER_ID } from "./constants.mjs";
import {
  clearPreempted,
  drainQueuedJob,
  isShaPreempted,
  queueJob,
  runGateJob,
} from "./orchestrate.mjs";

export class GateOrchestrator extends DurableObject {
  runner() {
    return getContainer(this.env.GATE_RUNNER, GATE_RUNNER_ID);
  }

  async enqueue(job) {
    const result = await queueJob(this.ctx.storage, job);
    // Kill the in-flight container for a superseded SHA so it does not burn
    // the rest of GATE_TIMEOUT_MS. The alarm's runJob then concludes cancelled
    // and the FIFO starts the newer SHA.
    if (result.preemptSha) {
      try {
        await this.runner().cancel("superseded");
      } catch {
        // previous SHA may have no live container
      }
    }
    return result;
  }

  async alarm() {
    await drainQueuedJob(this.ctx.storage, (job) =>
      runGateJob({
        job,
        env: this.env,
        getRunner: () => this.runner(),
        isPreempted: () => isShaPreempted(this.ctx.storage, job.sha),
      })
        .finally(() => clearPreempted(this.ctx.storage, job.sha))
        .catch((err) => {
          console.log(`portfolio-gate job failed: ${String(err?.message || err).slice(0, 240)}`);
        }),
    );
  }
}
