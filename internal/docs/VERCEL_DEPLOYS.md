# Vercel deploys: cost controls

Production is on Vercel Pro. Pro bills **Build CPU Minutes** with no included
allocation ($0.0035 per CPU-minute, drawn from the $20 monthly credit), and
the project used to build on every push to every branch. With 300+ commits a
week to `main` plus preview builds for each PR push, on a Turbo machine
(30 vCPU, ~$0.21 per build), the credit was gone within days and the
Spend-Management budget paused production.

Three layers fix that. The first is dashboard-only; the other two live here.

| Layer | Where | Effect |
|---|---|---|
| Build machine **Basic**, on-demand concurrency **off** | Vercel dashboard | ~15x cheaper per build |
| **Ignored Build Step** → `bash internal/scripts/vercel-ignore-build.sh` | dashboard field + repo script | no preview builds; no `main` build unless a build input changed |
| `git.deploymentEnabled: false` + scheduled Deploy Hook | `vercel.json` + `internal/workers/vercel-deploy-cron/` | pushes create no deployments at all; production advances on a cron |

## Dashboard settings (one time)

Project → **Settings → Build and Deployment**

- **Build Machine:** Basic. (Standard if builds exceed ~4 minutes; never Turbo.)
- **On-Demand Concurrent Builds:** off.
- **Prioritize Production Builds:** on.
- **Node.js Version:** 22.x matches CI; 24.x also builds.

Project → **Settings → Environment Variables**

- **Automatically expose System Environment Variables:** checked. The ignore
  script reads `VERCEL_GIT_COMMIT_REF` and `VERCEL_GIT_PREVIOUS_SHA`.

Project → **Settings → Git**

- **Ignored Build Step:** Behavior *Custom*, Command
  `bash internal/scripts/vercel-ignore-build.sh`.
  Not "Don't build anything" — that would cancel Deploy Hook builds too.
- **Deploy Hooks:** create one named `scheduled-main` for branch `main`. Paste
  the URL into the worker secret (below). It is the only thing that deploys
  production now.

Team → **Settings → Billing → Spend Management**

- **Pause Production Deployments:** off. A budget overrun should email you,
  not take down a site that filings link to.

## What lives in the repo

### `vercel.json` (committed, generated)

`npm run sync:short-links` writes it from `internal/public/short-links.json`:
short-link redirects, `Content-Disposition` headers, the `/documents/*` →
GitHub Pages rewrite, and

```json
"git": { "deploymentEnabled": false }
```

Vercel reads that key from the repository at push time, so the file must be
committed even though it is generated. The pre-commit hook re-runs the
generator when the catalog changes, and CI fails if the committed copy is
stale. Do not hand-edit it.

### `internal/scripts/vercel-ignore-build.sh`

Runs inside Vercel's build container before `npm ci`. Exit 0 skips, exit 1
builds (Vercel's convention is inverted). Skips every non-`main` ref, then
skips `main` when nothing under the build inputs changed since the last
successful production deploy. The input list is in the script; keep it in
step with `vite.config.js` and the `prebuild` scripts.

Because `git.deploymentEnabled` is off, this only sees Deploy Hook builds in
practice. It still matters: a hook fired while `main` gained only intel memos
is skipped in seconds.

Test locally:

```bash
VERCEL_GIT_COMMIT_REF=main VERCEL_GIT_PREVIOUS_SHA=HEAD~3 bash internal/scripts/vercel-ignore-build.sh; echo "exit=$?"
```

### `internal/workers/vercel-deploy-cron/`

Cloudflare Worker with a cron trigger (`0 1,13,17,21 * * *` UTC ≈ 06/10/14/18
Pacific). Each tick compares `main`'s HEAD (GitHub API) with
`${SITE_URL}/version.json` (written by `vite.config.js` into every build) and
POSTs the Deploy Hook only when production is behind. `POST /deploy` with a
bearer token forces a deploy between ticks. Setup is in its README.

### `postinstall`

`internal/scripts/postinstall-sync.mjs` runs `sync:derived` on a normal
install so a fresh clone has `summaries.json`, `upcoming.json`, and the
short-link outputs before `npm run dev` / `typecheck` / `test`. On Vercel it
exits immediately: `prebuild` runs the same scripts a moment later and paying
for them twice bought nothing.

### GitHub Pages

`deploy-gh-pages.yml` no longer runs on every push to `main`. It runs on the
same schedule as the worker and on dispatch; `npm run documents:push`
dispatches it after uploading new PDFs (the `documents` branch has no
workflow file, so a push there cannot trigger it directly).

## Deploying now

Any of:

```bash
curl -X POST -H "authorization: Bearer $DEPLOY_TRIGGER_TOKEN" "https://<worker-host>/deploy?force=1"
curl -X POST "$VERCEL_DEPLOY_HOOK_URL"
```

or Vercel dashboard → Deployments → latest → **Redeploy**.

## Expected cost

Basic machine, ~2-minute build, four ticks a day, most of them skipped:
well under $2 a month in build minutes. Before: $150–300.
