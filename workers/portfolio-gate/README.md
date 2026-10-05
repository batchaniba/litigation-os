# portfolio-gate — Phase 2 remote gate (Cloudflare Worker + Container)

Posts the GitHub Check Run named **`portfolio-gate`** (exact string) for pull
requests whose **base is `main`**. This is the remote replacement for the
Actions job that used to run the six-step suite. It is **not** GitHub Actions
and it must not grow a `.github/workflows/` file.

The laptop bar is unchanged: `.githooks/pre-push` / `npm run gate`
(`internal/scripts/portfolio-gate.mjs`, PR #904). This Worker runs the same
command on the PR head SHA and writes the result to Checks so branch
protection can require it.

Scaffold only. Creating the GitHub App, putting secrets, deploying, and
turning on the required check are **operator** steps after merge. This
environment does not need live App credentials.

## Architecture (locked)

```
GitHub pull_request (base=main)
        │  HMAC (GITHUB_WEBHOOK_SECRET)
        ▼
Orchestrator Worker  (this directory)
        │  GitHub App JWT → installation token
        │  Checks:write  →  pending Check Run `portfolio-gate`
        ▼
GateRunner Durable Object + Cloudflare Container
        │  clone head SHA → npm ci → npm run gate
        │  PORTFOLIO_SKIP_DISK_DOCS=1  VITE_COPY_DOCUMENTS=0
        ▼
PATCH Check Run  success | failure
```

Why official **Containers** and not Sandbox SDK: the Sandbox SDK
([docs](https://developers.cloudflare.com/sandbox/), fetched 2026-09-20) is a
1.0 preview with its own image. This gate needs a pinned **Node ≥22.22** +
**python3** + **git** image and a custom `npm run gate` command. That is a
custom Dockerfile on [`@cloudflare/containers`](https://developers.cloudflare.com/containers/)
(`startAndWaitForPorts` + `containerFetch`, wrangler `containers` +
`durable_objects` + `migrations.new_sqlite_classes`).

## Policy

| Event | Behavior |
|---|---|
| `pull_request` `opened` / `synchronize` / `reopened` and `base.ref === "main"` | Create pending `portfolio-gate`, start one Container for that SHA |
| Same events, `base.ref !== "main"` | **No-op** (HTTP 200, no Check Run, no Container) |
| `check_run` `rerequested` for name `portfolio-gate` on a PR targeting `main` | Re-run that SHA |
| Fork head (head repo ≠ installation repo) | Check Run **failure** — clone is same-repo only |
| Invalid / missing webhook signature | HTTP **401**. No Container. No success conclusion. |
| Container cannot start, or no result within the timeout | Check Run conclusion **`failure`** (never `neutral`) |
| New `synchronize` on the same PR | Cancel in-progress `portfolio-gate` runs on the previous SHA; one live run per SHA |

Required check missing also blocks merge once branch protection requires
`portfolio-gate`. Unsigned payloads are not trusted enough to pick a SHA, so
auth failures do not create a Check Run — they still cannot conclude success.

## Timeout (fail-closed)

Default **`GATE_TIMEOUT_MS=720000` (12 minutes)**, set in `wrangler.toml`.
If the Container does not return a result in that window, the Worker
concludes the Check Run as **`failure`**.

Where the run executes matters. The webhook only **queues** the job on the
`GateOrchestrator` Durable Object (one per head SHA) and answers 202; the
DO's **alarm** runs it. Do not move the run back into the webhook's
`ctx.waitUntil()`: Cloudflare cancels that work 30 seconds after the response
([Workers limits](https://developers.cloudflare.com/workers/platform/limits/)),
which killed every full run until Oct. 2026 and left Check Runs
`in_progress` forever (#958, #962) while the orphaned containers filled the
`max_instances` slots (#961: "Maximum number of running container instances
exceeded"). Alarms get 15 minutes, so the timeout stays under that. After
each run the container is stopped to free its slot.

**Stale sweep.** Every 30 minutes a cron concludes as `failure` any
`portfolio-gate` check on an open PR to `main` still `in_progress` more than
timeout + 5 minutes after it started (runner lost without reporting). Use
"Re-run" on the check to try again.

Cloudflare does not document a hard max instance runtime; the Container class
`sleepAfter` is **15 minutes** here: longer than the 12-minute gate timeout,
so idle-sleep cannot end a live run.

**Freeing instances.** After every run the orchestrator calls `cancel()`,
which `destroy()`s (SIGKILL) the container so its `max_instances` slot is
free at once. The image runs `node server.mjs` as PID 1, and Linux ignores
SIGTERM sent to PID 1 unless the process handles it; `server.mjs` therefore
handles SIGTERM/SIGINT explicitly. Before Oct. 2026 neither was true:
`stop()` (SIGTERM) was a no-op, finished containers kept running, and the
fourth run in a window failed with "Maximum number of running container
instances exceeded". Host moves can still SIGTERM a container (see
[Containers FAQ](https://developers.cloudflare.com/containers/faq/)); that
path is also concluded as failure.

## Runner command

Inside the image, for the PR head SHA:

```bash
git fetch --depth 1 origin <sha> && git checkout --detach FETCH_HEAD
npm ci --no-audit --no-fund
PORTFOLIO_SKIP_DISK_DOCS=1 VITE_COPY_DOCUMENTS=0 npm run gate
```

`SKIP_PORTFOLIO_GATE` is unset. If `package.json` has no `gate` script (an
old branch), the image falls back to the documented six steps: lint,
typecheck, `validate-portfolio`, golden damages, `vitest run`, citation
`--check`.

Instance type **`standard-2`** (1 vCPU / 6 GiB / 12 GB). `lite` / `basic`
will OOM on `npm ci`.

## Secrets (Worker only — never commit)

| Secret | What it is |
|---|---|
| `GITHUB_APP_ID` | Numeric GitHub App id |
| `GITHUB_APP_PRIVATE_KEY` | App private key PEM (`BEGIN PRIVATE KEY` PKCS#8 **or** `BEGIN RSA PRIVATE KEY` PKCS#1 — the Worker wraps PKCS#1) |
| `GITHUB_WEBHOOK_SECRET` | Random webhook HMAC secret (`openssl rand -hex 32`) |
| `GITHUB_APP_INSTALLATION_ID` | Installation id on this repo. Optional if every webhook includes `installation.id` (they do after the App is installed). Set it anyway so a rerequest or a missed field still fail-closes with a Check Run. |

Plain `[vars]` in `wrangler.toml` (not secrets): `GITHUB_REPO`, `CHECK_NAME`,
`GATE_TIMEOUT_MS`.

The Container receives only a **short-lived installation token** for
`git fetch`. App PEM and webhook secret never leave the Worker.

---

## Operator runbook (after merge)

Do these on the laptop. Do not add workflow YAML.

### 1. Create the GitHub App

GitHub → **Settings → Developer settings → GitHub Apps → New GitHub App**.

- **Name:** `ILP portfolio-gate` (or similar; not the Check name)
- **Homepage URL:** the portfolio site or this repo (operator only)
- **Webhook:** Active
- **Webhook URL:** `https://ilp-portfolio-gate.<your-workers-subdomain>.workers.dev/webhook`
  (use the URL `wrangler deploy` prints; you can edit the App after first deploy)
- **Webhook secret:** `openssl rand -hex 32` → this is `GITHUB_WEBHOOK_SECRET`
- **SSL:** enable
- **Permissions** — this repository only, nothing else:
  - **Checks:** Read and write
  - **Contents:** Read-only (clone the head SHA)
  - **Metadata:** Read-only (default)
  - **Pull requests:** Read-only (rerequest → confirm `base.ref`)
- **Subscribe to events:**
  - Pull request
  - Check run
- **Where can this GitHub App be installed?** Only on this account
- **Repository access:** **Only
  `newanforbi/interactive-litigation-portfolio`**

Generate a **private key**. Download the PEM. Convert to PKCS#8 if you
prefer (optional; the Worker accepts either):

```bash
openssl pkcs8 -topk8 -nocrypt -in app.pem -out app-pkcs8.pem
```

Install the App on **this repo only**. The installation URL looks like
`https://github.com/settings/installations/<id>` — that `<id>` is
`GITHUB_APP_INSTALLATION_ID`.

### 2. Put Worker secrets and deploy

Needs Docker (Wrangler builds and pushes the image on deploy) and a
Cloudflare account on the **Workers Paid** plan (Containers).

```bash
cd workers/portfolio-gate
npm install
npx wrangler login
npx wrangler secret put GITHUB_APP_ID
npx wrangler secret put GITHUB_APP_PRIVATE_KEY   # paste PEM, then Ctrl-D
npx wrangler secret put GITHUB_WEBHOOK_SECRET
npx wrangler secret put GITHUB_APP_INSTALLATION_ID
npx wrangler deploy
```

Confirm `GET https://<worker>/` shows `"check": "portfolio-gate"` and all
`configured` flags `true`. Paste the `/webhook` URL back into the GitHub
App if the first deploy minted a new host.

`npx wrangler tail` in another terminal while you open a test PR.

### 3. Enable the required check

GitHub → this repo → **Settings → Branches →** rule for `main`:

- [ ] Require a pull request before merging
- [ ] Do not allow force pushes
- [ ] Do not allow deletions of `main`
- [ ] **Require status checks to pass** → add exactly **`portfolio-gate`**
- [ ] Do **not** add `.github/workflows/`
- [ ] Do **not** require any Actions check (Actions is off; this Check is
      posted by the Worker)

The check name must be `portfolio-gate`. A different string will not satisfy
the rule.

### 4. Smoke-check

1. Open a PR against `main`. GitHub should show `portfolio-gate` pending,
   then success or failure with a truncated log.
2. Push a new commit (`synchronize`). The previous SHA's pending run is
   cancelled; the new SHA gets its own run.
3. Open a PR against some other branch. The Worker returns `ignored` and
   does **not** create a check.
4. **Re-run** on the Check Run should start a new run for that SHA.

## Local tests (no live Cloudflare, no App secrets)

From the repo root (vitest already on the laptop):

```bash
npx vitest run workers/portfolio-gate
```

Covers webhook HMAC, main-only no-op, fail-closed conclusions (start
failure + timeout), JWT signing, and superseded-SHA cancel. Does not start
a Container.

`npx wrangler dev --enable-containers=false` exercises the Worker process
without Docker.

## Files

<!-- smoke-test: verify portfolio-gate check run -->


| Path | Role |
|---|---|
| `src/index.mjs` | Worker `fetch` + `scheduled` (sweep, digest); exports `GateRunner`, `GateOrchestrator` |
| `src/handler.mjs` | Signature check, routing, queue the job |
| `src/orchestrator.mjs` | `GateOrchestrator` DO: queue + alarm runs the job |
| `src/policy.mjs` | Main-only / rerequest / fork policy |
| `src/webhook.mjs` | `X-Hub-Signature-256` |
| `src/github.mjs` | App JWT + Checks API |
| `src/orchestrate.mjs` | Pending check → runner → success/failure; queue/drain; stop container |
| `src/sweep.mjs` | Fail checks left `in_progress` past the timeout |
| `src/digest.mjs` | Daily deadline digest from `main`'s `clocks.json` |
| `src/runner.mjs` | `@cloudflare/containers` `Container` subclass |
| `src/check.mjs` | Locked name, truncated log, fail-closed conclusion |
| `container/server.mjs` | HTTP server on 8080 inside the image |
| `container/run-gate.sh` | clone + `npm ci` + `npm run gate` |
| `Dockerfile` | Node 22.22.0-bookworm + python3 + git |
| `wrangler.toml` | containers + DO + sqlite migration |

## Daily deadline digest

The `8 15 * * *` cron (08:08 PDT / 07:08 PST) reads **every**
`internal/src/data/matters/NN/clocks.json` at the head of `main` through the
GitHub App and POSTs JSON (with a phone-readable `text` field) to the
`ALERT_WEBHOOK` secret. Without that secret it only reaches Worker logs.

- **Needs disposition**: `open` / `set` clocks whose date has passed.
- **Next 14 days**: every live clock (`open`, `set`, `contingent`), any
  actor, any matter lifecycle. Several per matter are listed.
- **Mondays**: a 15–60 day horizon (statute-of-limitations backstops on
  dismissed matters included).
- Every message names the `main` commit it read. `private: true` clock
  titles are masked.
- If `main` cannot be read, a "DIGEST FAILED — deadlines were NOT checked"
  message is sent instead. A quiet day still sends a message.

This replaces the doc-api digest, which read one `next_clock` per matter
from the D1 publish projection (stale between manual reseeds, and blind to
non-court-facing clocks).

## Out of scope

- Creating the GitHub App for you
- Turning on branch protection for you (see the operator steps in the PR that added the alarm runner)
- Re-adding Actions
- Public-strip / cluster / clock edits
- Auto-reseed
