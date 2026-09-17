# doc-api — Cloudflare Worker + D1 for the litigation portfolio

Scaffolding (not yet deployed). Lets any agent, phone shortcut, or future
machine use the portfolio's R2 documents and derived data **without ever
handling R2 keys**: the Worker reaches the `litigation-documents` bucket
through an R2 *binding*. No key pairs, tokens, or secrets exist in this
directory — by design, there is nowhere to leak them from.

## What's here

| File | Purpose |
|---|---|
| `wrangler.toml` | Worker config: `DOCS` R2 binding → `litigation-documents`, `DB` D1 binding, UTC cron triggers for the digests. `database_id` is a placeholder until D1 is created. |
| `src/index.mjs` | The Worker. Document routes (`/doc/<sha256>`, `/doc/<sha256>/meta`) + D1-backed data routes (`/matters`, `/matters/<n>`, `/upcoming?days=14`, `/fuse`) mirroring the `npm run q` op shapes, plus a `scheduled` handler (daily fuse digest ~08:08 PT, Monday roll call ~07:08 PT) that POSTs to `ALERT_WEBHOOK` when set, else logs. |
| `schema.sql` | Idempotent D1 schema: `matters`, `clocks`, `documents`. |
| `seed.mjs` | Node script → stdout. Reads repo JSON (split `matters/NN/` preferred, legacy `NN.json` fallback, folded `next_clock` from the index, documents from the manifest) and emits idempotent INSERTs. Never writes to the repo. |

## Deploy (needs Aliko's Cloudflare login — not done)

```bash
cd workers/doc-api
wrangler login
wrangler d1 create litigation-portfolio
# copy the printed database_id into wrangler.toml
wrangler d1 execute litigation-portfolio --remote --file=schema.sql
node seed.mjs > seed.sql
wrangler d1 execute litigation-portfolio --remote --file=seed.sql
wrangler deploy
wrangler secret put ALERT_WEBHOOK   # optional; without it digests go to the Worker logs
```

Re-seed after the manifest or matter data changes (`node seed.mjs` again —
statements are idempotent). Cron times in `wrangler.toml` are UTC
approximations of PT wall clock; they shift an hour with daylight saving,
documented in the file.

## Verified locally (2026-09-17)

- `node --check` passes on `src/index.mjs` and `seed.mjs`; `wrangler.toml` parses.
- Route harness against mocked R2/D1 bindings: `/health`, `/doc/<sha256>`
  happy path (PDF bytes, ETag passthrough), 400 on bad hash, JSON 404 on
  missing object, `/doc/<sha256>/meta`, `/matters`, `/matters/26`,
  `/upcoming?days=14`, `/fuse`, and 503 `d1_not_provisioned` with no DB.
- `seed.mjs` runs against the checkout: 40 matters, clock rows, and
  manifest document rows emitted; SQL is single-quote-safe.

## Not yet done

- `wrangler login` / `d1 create` / `deploy` (needs Cloudflare auth — absent here).
- `database_id` in `wrangler.toml` (comes from `d1 create`).
- `ALERT_WEBHOOK` secret (optional).
- Live smoke test against the deployed Worker + real R2 binding.
