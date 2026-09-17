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
- PDF bytes live in Cloudflare R2 (`litigation-documents` bucket, key `sha256/<first2>/<rest>.pdf` — deterministic from the manifest sha256). Fetch one with `npm run docs:fetch <sha256>` (needs `R2_*` env; bytes are re-hashed client-side). Search `.txt` / `.meta.json` sidecars on this branch. The `documents` branch is a cold backup.
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

## No CI — the gate is local

There is no GitHub Actions CI. The only workflows left are the CourtListener
ones (`courtlistener-sync`, `counsel-dossier`, `intel-fetch-briefs`) and the
R2 document-upload job (`r2-upload.yml`: `documents` branch → R2, upload-only,
never deletes; Node `r2-upload.mjs`; approved 2026-09-16). Do not add others. The checks the old CI job ran now run in the `pre-push` hook
(installed by `npm run prepare`): lint, typecheck, `validate-portfolio`,
golden damages math, the unit suite, and the fabricated-citation gate.
Before opening a PR, run `npm run validate` yourself and say so in the PR
body. Production deploys are scheduled, not per-push; see
`internal/docs/VERCEL_DEPLOYS.md`.

## Runtime boundary: Python vs Node

`internal/scripts/` contains two runtimes. Do not mix them.

**Node (.mjs)** — the build/validation/sync pipeline. These run in the git
hooks and `npm run` scripts:
- `validate-portfolio.mjs` — data validation (pre-push gate)
- `sync-*.mjs` — derived data generation (registry, manifest, summaries, upcoming, short-links)
- `documents-store.mjs` — `npm run documents:pull -- --matter N` for one folder. R2 holds the bytes (`npm run docs:fetch`); phone-tap slug PDFs stay on `main` until a public origin returns 200.
- `r2-upload.mjs` / `lib/r2-client.mjs` — `documents` branch → R2 (`r2-upload.yml`)
- `load-matters.mjs`, `lib/matter-schema.mjs` — shared loaders and schemas
- `courtlistener/*.mjs` — docket sync

**Python (.py)** — one-off document generation and filling. These are
matter-specific utilities (e.g. `fill-matter-12-*.py`, `build-citation-index.py`)
run manually by Aliko. They are **not** part of the build, the hooks, or any npm script.

Rules:
- New automation that runs in the hooks or `npm run` must be Node (.mjs).
- Python scripts must not be added to `package.json` scripts or workflow steps.
- Shared logic (matter loading, validation) lives in Node; do not duplicate it in Python.
