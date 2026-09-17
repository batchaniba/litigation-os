# doc-api — Cloudflare Worker + D1 for the litigation portfolio

Live at `https://litigation-doc-api.ss8sxswwkt.workers.dev` (deployed
2026-09-17). Lets any agent, phone shortcut, or future machine use the
portfolio's R2 documents and derived data **without ever handling R2
keys**: the Worker reaches the `litigation-documents` bucket through an
R2 *binding*. No key pairs, tokens, or secrets exist in this directory —
by design, there is nowhere to leak them from.

## What's here

| File | Purpose |
|---|---|
| `wrangler.toml` | Worker config: `DOCS` R2 binding → `litigation-documents`, `DB` D1 binding, UTC cron triggers for the digests. `database_id` is a placeholder until D1 is created. |
| `src/index.mjs` | The Worker. `/doc/<sha256>` (immutable cache) and `/documents/<path>` (60s cache, path index then D1) plus D1 data routes, guarded `/admin/reseed`, and the scheduled digests. |
| `src/documents.mjs` | Path → sha256 helpers shared with `r2-upload.mjs --index`. A later row at the same path wins (redraft). |
| `schema.sql` | Idempotent D1 schema: `matters`, `clocks`, `documents`. |
| `seed.mjs` | Node script → stdout. Reads repo JSON (split `matters/NN/` preferred, legacy `NN.json` fallback, folded `next_clock` from the index, documents from the manifest) and emits idempotent INSERTs. Never writes to the repo. |

## Deploy

There is no GitHub Actions job. From a machine that is logged into wrangler
(Workers Scripts Edit + D1 Edit on the token):

```bash
cd workers/doc-api
wrangler deploy
wrangler secret put ALERT_WEBHOOK   # optional; without it digests go to the Worker logs
wrangler secret put RESEED_SECRET   # required for POST /admin/reseed
```

`wrangler.toml` keeps a placeholder `database_id`. Resolve it by name at
deploy time (`wrangler d1 list`) or wrangler will prompt.

## D1 re-seed

D1 is a second copy of the graph. Nothing reseeds it on merge. When it
needs a refresh: `node seed.mjs > seed.sql`, then POST the file to
`/admin/reseed` with the `RESEED_SECRET` bearer (or paste chunks into the
D1 console — keep pastes ≤ ~80KB with no `--` comment lines; the console
strips newlines). The endpoint applies the statements idempotently in
batches of 50 and is fail-closed (503 when the secret isn't configured,
403 on mismatch).

Re-seed after the manifest or matter data changes (`node seed.mjs` again —
statements are idempotent). Cron times in `wrangler.toml` are UTC
approximations of PT wall clock; they shift an hour with daylight saving,
documented in the file.

## Verified (2026-09-17)

- `node --check` passes on `src/index.mjs` and `seed.mjs`; `wrangler.toml` parses.
- Route harness against mocked R2/D1 bindings: `/health`, `/doc/<sha256>`
  happy path (PDF bytes, ETag passthrough), 400 on bad hash, JSON 404 on
  missing object, `/doc/<sha256>/meta`, `/matters`, `/matters/26`,
  `/upcoming?days=14`, `/fuse`, and 503 `d1_not_provisioned` with no DB.
- `seed.mjs` runs against the checkout: 40 matters, clock rows, and
  manifest document rows emitted; SQL is single-quote-safe.

## Not yet done

- `ALERT_WEBHOOK` Worker secret (optional — without it, the scheduled
  digests go to the Worker logs instead of posting anywhere).
- `RESEED_SECRET` Worker secret (required for a manual `POST /admin/reseed`).
