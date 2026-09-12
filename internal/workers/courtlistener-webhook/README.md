# CourtListener webhook -> GitHub dispatch adapter

A tiny [Cloudflare Worker](https://developers.cloudflare.com/workers/) that receives
[CourtListener webhook events](https://www.courtlistener.com/help/api/webhooks/) and
translates them into a `repository_dispatch` on
`newanforbi/interactive-litigation-portfolio` (event type `courtlistener-webhook`),
so the [CourtListener sync workflow](../../../.github/workflows/courtlistener-sync.yml)
runs on docket changes instead of on a fixed hourly poll. The schedule is kept at
every 6 hours purely as a backstop for events the webhook misses.

## How it works

1. CourtListener POSTs a JSON event (`{payload, webhook}`) to
   `https://<worker-host>/wh/<WEBHOOK_PATH_SECRET>` when a subscribed docket gets
   new filings (event type `DOCKET_ALERT = 1`), a search alert fires, etc.
2. The worker authenticates the request two ways, exactly as CourtListener's docs
   prescribe (their webhook system has **no** signature/HMAC mechanism):
   - the URL path must contain the long random `WEBHOOK_PATH_SECRET` (else 404), and
   - the source IP must be one of CourtListener's published egress IPs
     (`34.210.230.218`, `54.189.59.91`; else 403).
3. It extracts the docket IDs from `payload.results[].docket` (DOCKET_ALERT) or the
   alert identity (SEARCH_ALERT) and POSTs a `repository_dispatch` with
   `client_payload` containing the event name, docket IDs, and CourtListener's
   `Idempotency-Key` header.
4. The sync workflow re-queries the CourtListener API for anything the event
   mentions. **Nothing from the webhook POST body is committed to the repo** —
   the webhook is a wake-up call, not a data source.

On dispatch failure the worker returns 5xx so CourtListener retries (exponential
backoff over ~54h). Duplicate deliveries are harmless: the sync workflow is
idempotent and its runs are serialized.

## One-time setup (all by hand — needs your credentials)

### 1. Create the GitHub token

Create a token that can fire `repository_dispatch` on this repo:

- **Classic PAT:** `repo` scope (the repo is private).
- **Fine-grained PAT (preferred):** this repository only, with **Contents:
  read & write** (Metadata read is auto-selected).

GitHub's own `GITHUB_TOKEN` cannot be used here — dispatch must come from
outside the repo. Name it something like `ILP_WEBHOOK_DISPATCH`.

### 2. Deploy the worker

```bash
cd internal/workers/courtlistener-webhook

# Generate the secret URL path component (64 hex chars). Keep it private —
# anyone with the full URL can wake the sync workflow.
openssl rand -hex 32

npx wrangler login
npx wrangler secret put GITHUB_TOKEN        # paste the token from step 1
npx wrangler secret put WEBHOOK_PATH_SECRET  # paste the openssl output
npx wrangler deploy
```

Note the worker URL from the deploy output, e.g.
`https://ilp-courtlistener-webhook.<you>.workers.dev`. Your webhook URL is:

```
https://ilp-courtlistener-webhook.<you>.workers.dev/wh/<WEBHOOK_PATH_SECRET>
```

### 3. Register the webhook in CourtListener

1. Log in to CourtListener with the **same account that owns the API token**
   used by the repo's sync (`COURTLISTENER_TOKEN` repo secret).
2. Go to **Developer Tools > Webhooks** (your screenshot: the Webhooks tab under
   the account menu) and click **Add webhook**.
3. Paste the full webhook URL from step 2.
4. Subscribe to **Docket Alert** events — these fire when a subscribed docket
   gets new filings. (Search Alert events are also supported by the worker if
   you later add query alerts.)

### 4. Subscribe to your dockets

Webhook docket events only fire for dockets your account is subscribed to.
Subscribe to each bound federal docket either on the CourtListener website
(the bell/"Get Alerts" control on the docket page) or via the API:

```bash
curl -X POST https://www.courtlistener.com/api/rest/v4/docket-alerts/ \
  --header 'Authorization: Token <your-token-here>' \
  --data 'docket=<courtlistener-docket-id>'
```

Use the docket IDs in `internal/src/data/matters/*.json` (`courtlistener.docket_id`).
The repo's `npm run court:resolve` step prints the bound docket IDs.

### 5. Test end-to-end

- **Worker first:** `curl -X POST https://<worker>/wh/<secret> -H 'Content-Type: application/json' -d '{}'`
  from your own machine should return **403** (your IP isn't CourtListener's) —
  that proves the path secret and IP check are live.
- **CourtListener test event:** use the "send test event" control in the
  Webhooks panel. Test events don't come from the egress IPs, so temporarily
  allow them: `npx wrangler secret put SKIP_IP_CHECK` → `true`, send the test,
  confirm a `courtlistener-webhook` dispatch run appears under the repo's
  Actions tab, then set `SKIP_IP_CHECK` back to `false` (`npx wrangler deploy`
  isn't needed — secrets take effect immediately).
- **Real event:** the next filing on any subscribed docket should trigger a
  sync run within seconds, visible in Actions as a `repository_dispatch` run.

## Files

- `worker.mjs` — the adapter. No dependencies, no build step.
- `wrangler.toml` — worker name, entry point, compatibility date. Secrets are
  **not** in this file; they live in the worker's encrypted secret store.
- `dev.vars.example` — local-dev vars template (`wrangler dev --var`); never
  commit real secrets.

## Secrets reference

| Name | Where set | Purpose |
|---|---|---|
| `GITHUB_TOKEN` | `wrangler secret put` | PAT that POSTs `repository_dispatch` (never logged) |
| `WEBHOOK_PATH_SECRET` | `wrangler secret put` | long random path component; the URL is the credential |
| `SKIP_IP_CHECK` | `wrangler.toml` `[vars]` / `wrangler secret put` | `true` only for local/test-event testing; `false` in production |

## Operational notes

- **Quota win:** each webhook-triggered sync costs the same API calls as a
  scheduled one, but runs only when something changed — the 6-hour schedule is
  a safety net, not the driver.
- **Endpoint disabled?** If the worker is down or returns non-2xx 8 times,
  CourtListener disables the webhook and emails the account. Re-enable it in
  the Webhooks panel after fixing the worker; they'll redeliver events from
  the last 2 days.
- **Dormant dockets:** CourtListener auto-disables docket alerts on terminated
  cases with no updates for ~180 days (event type 4,
  `OLD_DOCKET_ALERTS_REPORT`). The worker forwards these; re-up alerts you
  still care about via `PATCH /api/rest/v4/docket-alerts/{id}/` with
  `alert_type=1`.
- **Webhooks are a paid-tier feature conversation:** Free Law Project notes
  that organizations starting webhook projects should talk to them about an
  agreement. A membership (Tier 1+, $10/mo) also raises the API quota that the
  sync consumes — both help here.
