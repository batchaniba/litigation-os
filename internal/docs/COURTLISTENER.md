# CourtListener bridge

CourtListener is an **upstream intelligence feed** into the portfolio that already exists. It is not a second dashboard. Confirmed docket facts can enter `timeline.json`. Deadlines cannot.

```
COURTLISTENER
     │
     ├── Search API     resolve docket_id once
     ├── Docket API     incremental entries newer than last seen
     └── Citation Lookup POST /citation-lookup/ (COURTLISTENER_TOKEN)
     │
CourtListener Bridge
     ├── confirmed events → timeline.json  (upcoming: false)
     └── candidates       → courtlistener/review.json
     │
npm run sync:all → Calendar / Matter UI / Next Actions
```

## What this phase does

1. **Bind** every federal matter to a stable `court_id` and, when RECAP has the case, `docket_id` / `docket_url`. After `docket_id` is stored, the resolver never searches by caption again.
2. **Sync** new docket entries incrementally. The hash + CourtListener entry ID make the job idempotent.
3. **Standing PR** from `automation/courtlistener-sync` titled **CourtListener Live Docket Sync**. Automation does not commit to `main`.

Phases not in this branch: webhook HTTP endpoint, RECAP document ingest, citation CI, research watches, Court Intelligence tab.

## Token

Store `COURTLISTENER_TOKEN` in a gitignored `.env` for local `court:sync` /
`citations:lookup`. `COURTLISTENER_API_TOKEN` is a deprecated alias for the
same value.

Never put it in a `VITE_*` variable, a Vite-loaded env file, or any file the browser bundle can see. The Node client throws if it finds a `VITE_*` CourtListener token.

Docket **resolution** can run unauthenticated against the Search API (`type=d`). Docket **entries**, `/api-usage/`, Citation Lookup, and the REST docket object require the token.

`court:sync` hits `/api/rest/v4/api-usage/` first and **refuses to run** if that call fails or if the body cannot be parsed. It reads `current_usage` rows with `scope: "user"` (defaults 5/min, 50/hour, 125/day) rather than guessing `daily_remaining`. Checking `/api-usage/` does not consume the main quota.

## Commands

```bash
npm run court:resolve                 # bind federal matters (Search API)
npm run court:resolve -- --dry-run
npm run court:resolve -- --matter 28
npm run court:sync -- --bootstrap     # first ingest: 24, 25, 26, 28, 29, 32, 33
npm run court:sync -- --bootstrap --since 2026-07-01
npm run court:sync -- --active-only
npm run court:sync -- --matter 28
npm run court:sync -- --all           # every bound federal docket; explicit
npm run court:sync -- --dry-run --bootstrap
npm run court:reconcile               # reminder: candidates stay in review.json
```

Empty cursors refuse a full historical backfill. Pass `--bootstrap`, `--active-only`, `--matter N`, or `--all`. `--since YYYY-MM-DD` is sent as `date_filed__gte` so a first pull does not paginate 2025 closed cases.

The hourly workflow is gone (no GitHub Actions). On the laptop:

```bash
npm run court:resolve
npm run court:sync -- --bootstrap
```

## Data

| Path | Role |
|---|---|
| `internal/src/data/matters/NN.json` → `courtlistener` | Stable binding (`court_id`, `docket_id`, `docket_url`) |
| `internal/src/data/courtlistener/sync-state.json` | Cursor: `last_entry_id`, `last_entry_number`, `last_synced_at` |
| `internal/src/data/courtlistener/ledger.json` | Idempotency ledger of ingested entries |
| `internal/src/data/courtlistener/review.json` | Deadline **candidates** (`status: pending`) |
| `internal/src/data/timeline.json` | Canonical facts. Next-actions still reads `upcoming: true` only |

State-court matters keep the same adapter shape later; RECAP/PACER is federal only.

## Deadlines

An order that says “Plaintiff shall file an amended complaint within 21 days” becomes a `review.json` candidate. It does **not** get `upcoming: true` and it does not enter the next-actions queue until a person (or a later approval command) copies it into `timeline.json` with a source PDF.

## Webhooks (not deployed yet)

CourtListener POSTs are not cryptographically signed. When an endpoint is added it must:

1. Use a long random URL, HTTPS only.
2. Allow-list `34.210.230.218` and `54.189.59.91`.
3. Deduplicate on the `Idempotency-Key` header.
4. Acknowledge immediately, then **re-query** the Docket API. The POST body is a hint (“look at docket 123”), never a record to commit.

Helpers live in `internal/scripts/courtlistener/webhook.mjs`. `applyPayloadEntries` is always `false`.

## Standing automation PR

There is no GitHub Actions workflow. Run `court:resolve` / `court:sync` on the
laptop and open a PR by hand if the working tree should be reviewed before
`main`. Deadline candidates stay in `review.json` until someone copies them
into `timeline.json` / `clocks.json`.
