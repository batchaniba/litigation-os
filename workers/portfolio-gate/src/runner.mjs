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
import { retryOnCapacity } from "./retry.mjs";

export class GateRunner extends Container {
  defaultPort = 8080;
  // Leak backstop only. cancel() destroy()s after every run, and an in-flight
  // POST /run counts as activity (incoming requests reset sleepAfter). 3m is
  // longer than portReadyTimeoutMS (90s) so startup cannot be slept; much
  // shorter than the old 15m idle bill if destroy() is skipped.
  sleepAfter = "3m";
  enableInternet = true;

  // Default onActivityExpired calls stop() (SIGTERM). destroy() is SIGKILL and
  // is what actually frees the max_instances slot.
  async onActivityExpired() {
    try {
      if (typeof this.destroy === "function") {
        await this.destroy();
      }
    } catch {
      // already stopped
    }
  }

  async runJob(job) {
    try {
      if (typeof this.renewActivityTimeout === "function") {
        this.renewActivityTimeout();
      }
      if (!this.ctx.container?.running) {
        await retryOnCapacity(() =>
          this.startAndWaitForPorts({
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
          }),
        );
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
