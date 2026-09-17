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
| `src/index.mjs` | The Worker. Document routes (`/doc/<sha256>`, `/doc/<sha256>/meta`) + D1-backed data routes (`/matters`, `/matters/<n>`, `/upcoming?days=14`, `/fuse`) mirroring the `npm run q` op shapes, a guarded `POST /admin/reseed` endpoint (Bearer `RESEED_SECRET`; re-applies seed.sql to D1 in batches), plus a `scheduled` handler (daily fuse digest ~08:08 PT, Monday roll call ~07:08 PT) that POSTs to `ALERT_WEBHOOK` when set, else logs. |
| `schema.sql` | Idempotent D1 schema: `matters`, `clocks`, `documents`. |
| `seed.mjs` | Node script → stdout. Reads repo JSON (split `matters/NN/` preferred, legacy `NN.json` fallback, folded `next_clock` from the index, documents from the manifest) and emits idempotent INSERTs. Never writes to the repo. |

## Deploy

Deploys run from `main` via `.github/workflows/cloudflare-deploy.yml`
(path-filtered to `workers/doc-api/**`; also `workflow_dispatch`). The
workflow resolves the D1 `database_id` by name at deploy time, so
`wrangler.toml` keeps its placeholder. Needs the repo secret
`CLOUDFLARE_API_TOKEN` (custom token: Workers Scripts Edit + D1 Edit) —
workflow-only, never visible to agents. Manual deploys still work:

```bash
cd workers/doc-api
wrangler deploy
wrangler secret put ALERT_WEBHOOK   # optional; without it digests go to the Worker logs
wrangler secret put RESEED_SECRET   # required for POST /admin/reseed; same value as the repo secret
```

## D1 re-seed

`.github/workflows/d1-reseed.yml` keeps D1 in sync with the repo: on every
portfolio-data merge to `main` it regenerates `seed.sql` (`node seed.mjs`)
and POSTs it to `/admin/reseed` with the `RESEED_SECRET` bearer. The
endpoint applies the statements idempotently in batches of 50 and is
fail-closed (503 when the secret isn't configured, 403 on mismatch).
Manual re-seed still works: `node seed.mjs > seed.sql`, then POST the file
(or paste chunks into the D1 console — keep pastes ≤ ~80KB with no `--`
comment lines; the console strips newlines).

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

- `ALERT_WEBHOOK` secret (optional — without it, the scheduled digests go to
  the Worker logs instead of posting anywhere).
- `CLOUDFLARE_API_TOKEN` repo secret (required for `cloudflare-deploy.yml`).
- `RESEED_SECRET` repo secret + matching Worker secret (required for
  `d1-reseed.yml` / `POST /admin/reseed`).
