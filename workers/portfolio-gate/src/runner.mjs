// Cloudflare Container Durable Object. APIs match
// https://developers.cloudflare.com/containers/ (fetched 2026-09-20):
//   class extends Container from @cloudflare/containers
//   startAndWaitForPorts + containerFetch
//   wrangler: containers + durable_objects + migrations.new_sqlite_classes
//
// Sandbox SDK was considered (CI/CD is a listed use case) but the preview
// ships its own image. This gate needs Node ≥22.22 + python3 + git, so a
// custom Dockerfile on official Containers is the documented fit.

import { Container } from "@cloudflare/containers";

export class GateRunner extends Container {
  defaultPort = 8080;
  // Idle backstop if a run's cleanup never ran. Longer than GATE_TIMEOUT_MS
  // (12m) so idling can never end a live run; short enough that a leaked
  // container frees its max_instances slot quickly.
  sleepAfter = "15m";
  enableInternet = true;

  async runJob(job) {
    try {
      if (!this.ctx.container?.running) {
        await this.startAndWaitForPorts({
          startOptions: {
            enableInternet: true,
            envVars: {
              PORTFOLIO_SKIP_DISK_DOCS: "1",
              VITE_COPY_DOCUMENTS: "0",
            },
          },
          cancellationOptions: {
            instanceGetTimeoutMS: 60_000,
            portReadyTimeoutMS: 90_000,
          },
        });
      }

      const res = await this.containerFetch("http://container/run", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({
          sha: job.sha,
          cloneUrl: job.cloneUrl,
          token: job.installationToken,
          timeoutMs: job.timeoutMs,
        }),
      });

      const body = await res.json().catch(() => ({}));
      if (!res.ok) {
        return {
          ok: false,
          reason: `container HTTP ${res.status}`,
          log: typeof body.log === "string" ? body.log : JSON.stringify(body).slice(0, 4000),
        };
      }
      return {
        ok: Boolean(body.ok),
        reason: body.reason || (body.ok ? "" : `exit ${body.exitCode ?? "?"}`),
        log: typeof body.log === "string" ? body.log : "",
        exitCode: body.exitCode ?? null,
      };
    } catch (err) {
      return {
        ok: false,
        reason: `container could not start or run: ${err?.message || err}`,
        log: "",
      };
    }
  }

  // Free the instance slot now. destroy() is SIGKILL: the run is over (or
  // superseded), so there is nothing to drain. stop() only sends SIGTERM and
  // returns, which left containers running (see container/server.mjs).
  async cancel(_reason) {
    try {
      if (typeof this.destroy === "function") {
        await this.destroy();
      } else if (this.ctx.container?.running && typeof this.ctx.container.destroy === "function") {
        await this.ctx.container.destroy();
      }
    } catch {
      // already stopped
    }
    return { ok: true, cancelled: true };
  }
}
