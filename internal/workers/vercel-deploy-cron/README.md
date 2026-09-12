# Scheduled Vercel production deploys

A [Cloudflare Worker](https://developers.cloudflare.com/workers/) with a cron
trigger that POSTs the portfolio project's Vercel **Deploy Hook** a few times a
day. Together with `git.deploymentEnabled: false` in the committed
[`vercel.json`](../../../vercel.json), it means production advances from `main`
at known times instead of on every one of the 100+ commits a busy day lands.

Cost model and the dashboard side of this are in
[`internal/docs/VERCEL_DEPLOYS.md`](../../docs/VERCEL_DEPLOYS.md).

## What it does on each tick

1. Reads `main`'s HEAD from the GitHub API (needs `GITHUB_TOKEN`; the repo is
   private).
2. Reads `${SITE_URL}/version.json` from production. `vite.config.js` writes
   `{ sha, ref, builtAt }` into every build.
3. If both are available and equal, logs `skip` and does nothing.
4. Otherwise POSTs `VERCEL_DEPLOY_HOOK_URL`. Vercel builds `main` at its
   current tip. The Ignored Build Step
   ([`internal/scripts/vercel-ignore-build.sh`](../../scripts/vercel-ignore-build.sh))
   still runs and skips the build if nothing under the build inputs changed
   since the last production deploy.

If `GITHUB_TOKEN` or `SITE_URL` is missing the comparison is skipped and the
hook fires on every tick. That costs roughly one Basic-machine build per tick
(about $0.014 each), which is still two orders of magnitude below deploying on
every push.

## Schedule

`wrangler.toml`: `0 1,13,17,21 * * *` (UTC) = 06:00, 10:00, 14:00, 18:00
Pacific during PDT, one hour later in PST. Change it there; nothing else reads
it.

## Manual deploy between ticks

For an urgent filing:

```bash
curl -X POST -H "authorization: Bearer $DEPLOY_TRIGGER_TOKEN" https://<worker-host>/deploy
# add ?force=1 to skip the version comparison
```

Or skip the worker and POST the Deploy Hook URL directly with `curl -X POST`.
Either way Vercel shows the deployment as hook-triggered in the dashboard.

`GET /` returns which pieces are configured (booleans only, no secrets).

## One-time setup (by hand — needs your credentials)

### 1. Vercel: create the Deploy Hook

Project → **Settings → Git → Deploy Hooks**. Name it `scheduled-main`, branch
`main`, Create. Copy the URL. Anyone with it can rebuild the site, so it lives
only in the worker secret below.

### 2. GitHub: a read-only token

Fine-grained PAT, **this repository only**, permission **Contents: Read-only**.
Nothing else. Optional but recommended; without it every tick builds.

### 3. Deploy the worker

```bash
cd internal/workers/vercel-deploy-cron
npx wrangler login
npx wrangler secret put VERCEL_DEPLOY_HOOK_URL
npx wrangler secret put GITHUB_TOKEN            # optional
npx wrangler secret put DEPLOY_TRIGGER_TOKEN    # optional; openssl rand -hex 32
```

Set `SITE_URL` in `wrangler.toml` to the production origin (custom domain or
the `*.vercel.app` production URL), then:

```bash
npx wrangler deploy
```

Cron triggers are created from `wrangler.toml` on deploy. Confirm under
Workers & Pages → the worker → **Settings → Triggers**.

### 4. Vercel: make sure hook builds are not ignored

Project → **Settings → Git → Ignored Build Step** should be **Custom** with
`bash internal/scripts/vercel-ignore-build.sh`. Do **not** pick "Don't build
anything"; that would cancel hook builds too.

### 5. First run

```bash
npx wrangler tail   # in one terminal
curl -X POST -H "authorization: Bearer $DEPLOY_TRIGGER_TOKEN" "https://<worker-host>/deploy?force=1"
```

You should see a `deploy-hook` log line with a Vercel `job.id`, and a new
deployment in the Vercel dashboard marked as triggered by the hook.

## Local test

```bash
cp dev.vars.example .dev.vars   # fill in
npx wrangler dev --test-scheduled
curl "http://localhost:8787/__scheduled?cron=0+1,13,17,21+*+*+*"
```
