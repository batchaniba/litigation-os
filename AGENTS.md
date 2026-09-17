# Repository Instructions

Crawl this repo as a graph. Do not reconstruct a docket from README or from `status` / `procedural_status`.

`internal/src/data/index/matters.json` is the front door. Then fetch only the sibling you need from `internal/src/data/matters/NN/` (`matter.json`, `docket.json`, `clocks.json`, `documents.json`, `events.jsonl`, …). Every matter is split.

`docket.json` is pleadings. `documents.json` is the file inventory. `clocks.json` is the live calendar — not `timeline.json`.

## Crawl order

0. Prefer the query interface over raw JSON: `npm run q <op>` (reads like `getMatter`, `upcomingDeadlines`, `getFuseBoard`, `getTimeline`; writes like `recordTimelineEvent`, `setNextClock`, `catalogDocument`) or the MCP server (`npm run mcp`). Writes validate before touching disk and land on the working tree for review. Drop to raw files only when an op can't express the question.
1. `internal/src/data/index/matters.json` — every matter: path, case_no, phase, next_clock, last_updated.
2. Fetch only the sibling files the question needs (`clocks.json`, `docket.json`, `events.jsonl`, `claims.json`, …). Identity is `matter.json`.
3. People, clusters, citations: `internal/src/data/index/{people,clusters,citations}.json`.
4. Schema and limits: `internal/src/data/index/schema.json`.

## Truth

- Never treat README as live.
- Never invent a docket number. If `dkt` is null, say so.
- `clocks.json` or index `next_clock` wins over prose. Vacated clocks are not live.
- `events.jsonl` is append-only. Do not rewrite it.
- Operative pleading is the docket row with `"operative": true`. ASK vs CRB name-conform packets: CRB supersedes; they are not two cases.
- PDF bytes live in Cloudflare R2 (`litigation-documents` bucket, key `sha256/<first2>/<rest>.pdf` — deterministic from the manifest sha256). Draft or replace a file under `internal/public/documents/matter-NN/`; `npm run documents:push` (needs `R2_*`) PUTs the bytes and rewrites `index/path-to-sha256.json` so the same `/documents/...` path serves the new object. Fetch one with `npm run docs:fetch <sha256>` (bytes are re-hashed client-side). Search `.txt` / `.meta.json` sidecars on this branch. Pre-extracted text sidecars live at `text/<first2>/<rest>.txt` in the same bucket (poppler `pdftotext -layout`; `internal/scripts/extract-doc-text.mjs` backfills, `r2-upload.mjs` keeps them in sync) and are served by the Worker's `readDocumentText` MCP tool. The `documents` branch is a cold backup.
- `R2_*` comes from the environment. Never paste keys into chat, files, or memory.
- Do not put GitHub or repo URLs in anything Plaintiff will send or file.

## Limits (what exists, and why)

Cap the first fetch, not the case. Numbers live in `GRAPH_LIMITS` (`assembleMatter.js`) and `index/schema.json` `x-limits`.

- **Keep:** `matter.json` ≤80 lines / 8KB (identity fetch). `status_label` ≤60 characters (UI chip). Index `next_clock.title` ≤240 characters when the source is a timeline blob.
- **Do not add:** line or word ceilings on `docket.json`, `events.jsonl`, `clocks.json`, claims, damages, or evidence. Schema failure for an overdue `next_clock`. Output-length caps on agent work. Literary line limits on the case.

## Standing locks

- Skip GitHub PR **#666**.
- Actual stipulations / extensions / stays: read `internal/docs/STIPULATION_DEFENSE.md`. Plaintiff-first. Do not import that voice into ordinary Plaintiff papers.
- Email close after the valediction:

```
Brendan Ngwa Nforbi
Plaintiff, In Propria Persona
```

No phone, no email address, no "In Pro Per" on the close.

## Counsel dossiers

Opposing-counsel identity/role research lives under `internal/docs/counsel/`. Seeded: Kabat Chapman & Ozmer (Williams / Chapman) at [`internal/docs/counsel/kcoz/`](internal/docs/counsel/kcoz/). Append PACER pulls there. Those dockets are not related cases. Do not email counsel about the research.

## No GitHub to outsiders

Never put a GitHub, `raw.githubusercontent.com`, git-repo, or document-store
URL in anything Plaintiff will send or file. Attach the file. A download
link in the agent chat for him is fine. It does not go in the email.

## Worker, not keys

Do not give ChatGPT, Grok, or any third-party chat R2 admin keys or
`~/.config/r2/env`. Point them at
`https://litigation-doc-api.ss8sxswwkt.workers.dev`
(`/matters`, `/fuse`, `/doc/<sha256>`, `/doc/<sha256>/meta`, `/documents/<path>`).
The Worker binds R2; keys stay server-side. Cursor reads `~/.config/r2/env`
for writes or calls the Worker for reads. If a chat needs a secret, a
rotatable Worker bearer — never the Cloudflare admin pair. Direct R2, if
ever: a read-only token scoped to `litigation-documents`. Admin keys live
in exactly two places: the laptop env file and the Worker's bindings.
See `.cursor/rules/worker-not-keys.mdc`.

### MCP endpoint — the document-fetch path for external models

`POST https://litigation-doc-api.ss8sxswwkt.workers.dev/mcp` — stateless
Streamable HTTP (JSON-RPC 2.0, no auth, CORS `*`). Any MCP-capable model or
agent (Claude Code, Cursor, Claude Desktop, ChatGPT, Grok) points its client
at that URL and gets read-only tools over the same store: `listMatters`,
`getMatter`, `upcomingDeadlines`, `getFuseBoard`, `getMatterDocs`,
`searchDocuments`, `fetchDocument` (returns size/ETag plus the
`GET /doc/<sha256>` download URL), and `readDocumentText` (returns the
document's extracted text inline, paginated — the preferred way for an
external model to *read* a document, so it never has to fetch PDF bytes over
HTTP). This is the preferred way for an external model to fetch documents:
no R2 keys, no repo clone, no credentials of any kind. Local agents with
`R2_*` keep using `npm run docs:fetch` and the query interface.

## No GitHub Actions

Do not add `.github/workflows/`. The spending limit already refuses every job.
The checks the old CI job ran live in the `pre-push` hook (installed by
`npm run prepare`): lint, typecheck, `validate-portfolio`, golden damages math,
the unit suite, and the fabricated-citation gate. Before opening a PR, run
`npm run validate` yourself and say so in the PR body.

Laptop replacements (never paste keys into chat; other AIs get the Worker URL, not `R2_*`):

- CourtListener: `npm run court:sync -- --bootstrap` (token in gitignored `.env`)
- R2 bytes + path index: `npm run documents:push` (`R2_*` from `~/.config/r2/env`)
- Worker: `cd workers/doc-api && wrangler deploy`
- D1: `node workers/doc-api/seed.mjs > seed.sql`, then POST `/admin/reseed`
- Dependencies: `npm run deps:outdated` / `npm run deps:update` (do not restore Dependabot; it runs on Actions runners). Optional PR factory is the Mend Renovate GitHub App + `.github/renovate.json`, not a workflow.

Production deploys are the Vercel Deploy Hook from the Cloudflare cron, not
per-push; see `internal/docs/VERCEL_DEPLOYS.md`.

## Runtime boundary: Python vs Node

`internal/scripts/` contains two runtimes. Do not mix them.

**Node (.mjs)** — the build/validation/sync pipeline. These run in the git
hooks and `npm run` scripts:
- `validate-portfolio.mjs` — data validation (pre-push gate)
- `sync-*.mjs` — derived data generation (registry, manifest, summaries, upcoming, short-links)
- `documents-store.mjs` — `npm run documents:pull -- --matter N` (R2 when `R2_*` is set, else the git branch). `documents:push` updates the cold `documents` branch and, with credentials, PUTs PDFs + the path index to R2. Phone-tap slug PDFs stay on `main` until a public `/documents/...` origin returns 200.
- `r2-upload.mjs` / `lib/r2-client.mjs` — PDF bytes + `index/path-to-sha256.json` → R2 (called by `documents:push`)
- `load-matters.mjs`, `lib/matter-schema.mjs` — shared loaders and schemas
- `courtlistener/*.mjs` — docket sync

**Python (.py)** — one-off document generation and filling. These are
matter-specific utilities (e.g. `fill-matter-12-*.py`, `build-citation-index.py`)
run manually by Aliko. They are **not** part of the build, the hooks, or any npm script.

Rules:
- New automation that runs in the hooks or `npm run` must be Node (.mjs).
- Python scripts must not be added to `package.json` scripts. Do not add GitHub Actions workflows.
- Shared logic (matter loading, validation) lives in Node; do not duplicate it in Python.
