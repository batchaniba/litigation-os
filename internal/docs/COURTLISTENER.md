# CourtListener bridge

CourtListener is an **upstream intelligence feed** into the portfolio that already exists. It is not a second dashboard. Confirmed docket facts can enter `timeline.json`. Deadlines cannot.

```
COURTLISTENER
     │
     ├── Search API     resolve docket_id once
     ├── Docket API     incremental entries newer than last seen
     └── Citation API   later (CiteProof)
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

Store `COURTLISTENER_TOKEN` as a **GitHub Actions repository secret** (and in the local shell when you run `court:sync`).

Never put it in a `VITE_*` variable, `.env` that Vite loads, or any file the browser bundle can see. The client throws if it finds a `VITE_*` CourtListener token.

Docket **resolution** can run unauthenticated against the Search API (`type=d`). Docket **entries**, `/api-usage/`, and the REST docket object require the token.

## Commands

```bash
npm run court:resolve                 # bind federal matters (Search API)
npm run court:resolve -- --dry-run
npm run court:resolve -- --matter 28
npm run court:sync                    # pull new entries; needs COURTLISTENER_TOKEN
npm run court:sync -- --dry-run
npm run court:reconcile               # reminder: candidates stay in review.json
```

`court:sync` hits `/api/rest/v4/api-usage/` first and aborts if the remaining budget is too small. Limits are read from the account, not hard-coded to 125/day.

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

`.github/workflows/courtlistener-sync.yml` runs hourly (`17 * * * *`) and on `workflow_dispatch`. It resolves, syncs, runs `sync:all` + tests, and opens or updates **one** PR from `automation/courtlistener-sync`. Inspect that PR the same way as any other agent branch.
