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
| `src/index.mjs` | The Worker. Document routes (`/doc/<sha256>`, `/doc/<sha256>/meta`) + D1-backed data routes (`/matters`, `/matters/<n>`, `/upcoming?days=14`, `/fuse`) mirroring the `npm run q` op shapes, a `POST /mcp` MCP endpoint (Streamable HTTP, stateless JSON-RPC — see below), a guarded `POST /admin/reseed` endpoint (Bearer `RESEED_SECRET`; re-applies seed.sql to D1 in batches), plus a `scheduled` handler (daily fuse digest ~08:08 PT, Monday roll call ~07:08 PT) that POSTs to `ALERT_WEBHOOK` when set, else logs. |
| `src/data.mjs` | Shared data layer: R2/D1 access and the portfolio query ops. Both the REST routes and the MCP tools call into it, so the two surfaces can't drift. Throws `HttpError` (400/404/503) on mapped failures. |
| `src/mcp.mjs` | MCP endpoint handler: `initialize` / `ping` / `tools/list` / `tools/call` over the read ops **and the v2 write tools** (scope-gated, audited). CORS-open (`*`) so browser-based clients work. |
| `src/auth.mjs` | Scoped bearer-token auth. Tokens live only as SHA-256 hashes inside the `API_KEYS` Worker secret; scope `r` / `rw`. Resolves what a caller may do; surfaces gate with `requireRead` / `requireWrite`. |
| `src/writes.mjs` | Write data layer (C/U/D): R2 byte put/delete, D1 upsert/patch/delete over matters, clocks, and the document manifest, plus best-effort `recordAudit`. |
| `schema.sql` | Idempotent D1 schema: `matters`, `clocks`, `documents`, and the `audit` trail. |
| `seed.mjs` | Node script → stdout. Runs the same `publishMatter()` projection as the SPA (identity, court-facing clocks, filed / phone-tap PDFs) and emits idempotent DELETE + INSERTs. Never writes to the repo. Laptop `npm run mcp` keeps the full graph. |

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
Manual re-seed (required after this publish-strip lands, so live D1 drops
strategy clocks, unfiled drafts, and settlement chips):

```bash
cd workers/doc-api
node seed.mjs > seed.sql
# Preferred when RESEED_SECRET is set on the Worker:
curl -X POST https://litigation-doc-api.ss8sxswwkt.workers.dev/admin/reseed \
  -H "Authorization: Bearer $RESEED_SECRET" \
  --data-binary @seed.sql
# Or apply the SQL directly:
wrangler d1 execute litigation-portfolio --remote --file=schema.sql
wrangler d1 execute litigation-portfolio --remote --file=seed.sql
```

Then smoke-check `GET /matters`, `GET /fuse`, and `GET /matters/29`:
computed SOL backstops, `$35,000` / final-demand chips, `EMAIL_DRAFT_*`,
and unfiled screening-ID PDFs must be gone. Laptop `npm run mcp` is unchanged.

Re-seed after the manifest or matter data changes (`node seed.mjs` again —
statements are idempotent). Cron times in `wrangler.toml` are UTC
approximations of PT wall clock; they shift an hour with daylight saving,
documented in the file.

## Path-addressed documents & clock statuses

`GET /documents/<path>` serves a PDF by its portfolio path (e.g.
`/documents/matter-24/First Amended Complaint.pdf`), resolved through the R2
`index/path-to-sha256.json` path index, then the D1 `documents_by_path`
table (path is the identity — one sha256 can live under many court paths),
then the legacy sha256-PK `documents` table. Path-addressed bytes carry
`Cache-Control: public, max-age=60` (revalidatable: the same court path can
be re-filed under a new sha256) and an inline `Content-Disposition`
filename; hash-addressed `/doc/<sha256>` bytes stay immutable.

Clocks carry a `status` (`open | satisfied | retired | cancelled |
vacated`, seeded from `clocks.json`). `/upcoming` and the folded
`next_clock_*` exclude non-open clocks, so satisfied/retired/vacated rows no
longer leak into the fuse board. On a D1 that predates the column the
queries fall back to the unfiltered form; to backfill:

```bash
wrangler d1 execute litigation-portfolio --remote \
  --command "ALTER TABLE clocks ADD COLUMN status TEXT"   # ignore duplicate-column
wrangler d1 execute litigation-portfolio --remote --file=schema.sql
node seed.mjs > seed.sql
wrangler d1 execute litigation-portfolio --remote --file=seed.sql
```

## Verified (2026-09-17)

- `node --check` passes on `src/index.mjs` and `seed.mjs`; `wrangler.toml` parses.
- Route harness against mocked R2/D1 bindings: `/health`, `/doc/<sha256>`
  happy path (PDF bytes, ETag passthrough), 400 on bad hash, JSON 404 on
  missing object, `/doc/<sha256>/meta`, `/matters`, `/matters/26`,
  `/upcoming?days=14`, `/fuse`, and 503 `d1_not_provisioned` with no DB.
- `seed.mjs` runs against the checkout: 40 matters, clock rows, and
  manifest document rows emitted; SQL is single-quote-safe.
- `src/index.mjs` was refactored onto `src/data.mjs` (shared with `src/mcp.mjs`)
  with zero REST behavior change: a stubbed-binding harness replays every route
  against the pre-refactor snapshot and diffs status + body byte-for-byte
  (102 assertions, all green 2026-09-17), then covers `POST /mcp`
  (`initialize` negotiation, `tools/list`, all 7 tools happy-path + 400/404/503
  mappings, CORS, batch, notifications).

## MCP endpoint — `POST /mcp`

Stateless MCP (Streamable HTTP): each POST carries one JSON-RPC 2.0 message
and gets a plain JSON response — no SSE stream, no session ids. Protocol
versions negotiated: `2025-06-18`, `2025-03-26`, `2024-11-05`. CORS is open
(`*`) so browser-based clients (Claude/ChatGPT web connectors) can call it.

Reads stay open and filing-safe: D1 is seeded from `publishMatter()`, not
the laptop graph. The stdio server in `internal/mcp` (`npm run mcp`) is the
full-graph laptop client — do not treat the two MCP endpoints as equivalent.

**Read tools.** Eight tools, mirroring the *shape* of the stdio server in
`internal/mcp` and the `npm run q` ops, backed by the same D1/R2 bindings:

| Tool | Args | Returns |
|---|---|---|
| `listMatters` | `lifecycle?` | matters with next clocks |
| `getMatter` | `n` | identity + clocks + documents (each with a download `url`) |
| `upcomingDeadlines` | `days=14`, `matter?` | clock rows, oldest first |
| `getFuseBoard` | `days=14` | `{ fuse, wait, parked }` |
| `getMatterDocs` | `n` | manifest rows with download `url`s |
| `searchDocuments` | `query`, `limit=20` | substring over manifest paths + matter captions, with `url`s |
| `fetchDocument` | `sha256` | `{ sha256, size, etag, url }` — fetch the bytes with `GET url` |
| `readDocumentText` | `sha256`, `offset=0`, `limit=20000` | `{ sha256, total_chars, offset, limit, returned_chars, truncated, text }` — extracted PDF text, inline |

`readDocumentText` is the preferred way to *read* a document: it serves the
pre-extracted text sidecar (`text/<first2>/<rest>.txt` in the same R2 bucket,
written by `internal/scripts/extract-doc-text.mjs` and kept in sync by
`internal/scripts/r2-upload.mjs`) as paginated tool-result text, so the model
never has to fetch PDF bytes over HTTP. `fetchDocument` stays for the cases
that need raw bytes (`application/pdf`). Timelines, counsel/judge dossiers,
and the cluster map are not in D1, so they are not tools yet — a seed
expansion could add them later.

**Write tools (v2).** Create / update / delete over matters, clocks, and the
document manifest. Each needs an `rw` token (see **Auth & scopes**) and is
written to the `audit` table. Document *bytes* go over REST (`PUT /doc`), not
JSON-RPC — a base64 PDF over the wire is wasteful and some documents are
>20 MB.

| Tool | Args | Effect |
|---|---|---|
| `upsertMatter` | `number`, + any matter fields | create or replace a matter row |
| `updateMatter` | `n`, + fields to patch | patch only the given columns (e.g. fix a stale `status_label`); 404 if unknown |
| `deleteMatter` | `n`, `confirm`, `cascade?` | delete a matter; refuses if it owns clocks/docs unless `cascade` |
| `addClock` | `matter_number`, `title`, `date?`, `kind?` | add a deadline/hearing |
| `deleteClock` | `matter_number`, `title`, `date?` | remove matching clock rows |
| `registerDocument` | `sha256`, `matter_number?`, `path?`, `size?` | upsert a manifest row (bytes uploaded separately) |
| `deleteDocument` | `sha256`, `confirm`, `keepBytes?` | remove the manifest row and (unless `keepBytes`) the R2 bytes |

## Auth & scopes

Reads shipped open and stay that way by default. Writes require a **scoped
bearer token**. Tokens exist only as SHA-256 hashes inside the `API_KEYS`
Worker secret — a JSON map of `{ "<sha256-of-token>": { "name", "scope" } }`
— so the plaintext never lives in this repo or the D1/R2 stores. Scope is
`r` (read) or `rw` (read + write).

Behavior is fail-safe:

- **`API_KEYS` unset** → reads open (unchanged); **writes hard-refused**
  (`503 auth_not_configured`). You can't get a writable-but-open API by
  accident.
- **`API_KEYS` set** → writes need an `rw` token; reads need any valid token
  **unless** `PUBLIC_READ="true"`, which keeps reads open while gating writes.

Recommended rollout — do **not** break existing read clients:

```bash
cd workers/doc-api
# 1) mint a token locally, store only its hash in the secret:
TOKEN=$(openssl rand -hex 32)
HASH=$(printf %s "$TOKEN" | shasum -a 256 | cut -d' ' -f1)
printf '{"%s":{"name":"cursor","scope":"rw"}}' "$HASH" | wrangler secret put API_KEYS
wrangler secret put PUBLIC_READ   # value: true   (keep reads open for now)
# 2) hand $TOKEN to the agent that needs write access. Rotate by editing the
#    secret; revoke by removing the entry. Never commit $TOKEN.
```

Later, drop `PUBLIC_READ` and issue `r` tokens to lock reads down too. Every
write records `{ ts, actor, action, target, detail, ok }` to `audit` —
`actor` is the key's `name`, so you can see which agent changed what.

## Write API — REST

```
PUT    /doc/<sha256>?matter=<n>&path=<path>[&verify=false]   body = PDF bytes   (rw)
DELETE /doc/<sha256>?confirm=1[&keepBytes=true]                                  (rw)
```

`PUT` verifies the uploaded bytes hash to `<sha256>` (the R2 key) before
storing, then upserts the manifest row. `DELETE` needs `confirm=1`.

## Connecting clients

URL: `https://litigation-doc-api.ss8sxswwkt.workers.dev/mcp`. For read-only
use while `PUBLIC_READ` is on, no header is needed; for writes (or once reads
are locked), send `Authorization: Bearer <token>`.

- **Claude Code:** `claude mcp add --transport http litigation-portfolio https://litigation-doc-api.ss8sxswwkt.workers.dev/mcp --header "Authorization: Bearer <token>"`
- **Cursor:** Settings → MCP → Add server → Streamable HTTP URL, and set an `Authorization` header in the server entry.
- **Claude Desktop:** remote server entry in `claude_desktop_config.json` with a `headers` map.
- **claude.ai / ChatGPT:** add as a custom connector with the URL (+ auth header where the connector supports it).

The same token model applies to every client — access is decided at the
Worker, not per-agent, so any MCP-capable model or agent gets identical CRUD
with its own scoped token.

## Not yet done

- `ALERT_WEBHOOK` secret (optional — without it, the scheduled digests go to
  the Worker logs instead of posting anywhere).
- `CLOUDFLARE_API_TOKEN` repo secret (required for `cloudflare-deploy.yml`).
- `RESEED_SECRET` repo secret + matching Worker secret (required for
  `d1-reseed.yml` / `POST /admin/reseed`).
- `API_KEYS` Worker secret (required to enable write tools / the REST write
  API; without it writes are refused). `PUBLIC_READ` Worker var (`"true"` to
  keep reads open once `API_KEYS` is set). Apply the `audit` table with
  `wrangler d1 execute litigation-portfolio --remote --file=schema.sql`.
