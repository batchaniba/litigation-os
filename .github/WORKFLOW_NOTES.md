# Workflow and Data Pipeline Documentation

## Overview

This repository uses a multi-stage data pipeline to keep the interactive litigation portfolio in sync across the SPA bundle, README documentation, and validation gates.

There are **no GitHub Actions workflows**. Do not add `.github/workflows/`.
The spending limit already refuses every job. The **local** gate is
`.githooks/pre-push` and `npm run gate` (same steps; shared
`internal/scripts/portfolio-gate.mjs`). The **Phase 2 remote** gate is the
Cloudflare Worker + Container in `workers/portfolio-gate/`, which posts the
GitHub Check Run named `portfolio-gate` on PRs whose base is `main`.

## Data Sync Scripts

### Essential Scripts (must run in every build)

These scripts are **load-bearing** and ensure data consistency:

#### 1. `npm run sync:summaries`
- **When**: Runs in `prebuild` (before every production build)
- **What it does**: Generates `internal/src/data/matters/summaries.json` and `internal/src/data/matters/document-index.json`
- **Why**: The SPA shell bundle includes only lightweight matter summaries to keep initial load fast. Full matter data (key_facts, damages, evidence, etc.) is lazy-loaded on expand.
- **Output**: 
  - `summaries.json` — stripped-down matter records (number, caption, status, lifecycle, etc.) + counts
  - `document-index.json` — searchable index of all documents across matters
- **Failure mode**: If stale, the UI will show outdated matter lists or missing documents

#### 1b. `npm run sync:all`
- **When**: After editing matter JSON, `timeline.json`, documents, or short-links. The pre-commit hook runs this automatically when those paths are staged (`core.hooksPath = .githooks`, installed by `npm run prepare`).
- **What it does**: `sync:registry` → `sync:manifest` → `sync:summaries` → `sync:upcoming` → `sync:short-links` → `generate:readme`
- **Why**: Stops generated-file merge wars from a commit that updates a matter but leaves `summaries.json` / README stale (the #627 failure mode). `sync:manifest` reuses sha256 values when file size is unchanged, so a matter-only commit does not re-read the PDF library.
- **Companion**: `npm run retire:upcoming` flips past-dated `upcoming: true` flags to `false` (America/Los_Angeles). Run it when validate complains that a clock rolled past today, then `sync:upcoming`. The hook also stages `internal/src/data/documents/manifest.json` when it rewrites it.

#### 2. `npm run sync:upcoming`
- **When**: Runs in `prebuild` (before every production build)
- **What it does**: Generates `internal/src/data/upcoming.json` by filtering `timeline.json` for events marked `upcoming: true`
- **Why**: The deadline clock component needs a separate, lightweight file to avoid loading the entire 300+ entry timeline on page load
- **Output**: `upcoming.json` — filtered subset of timeline events
- **Failure mode**: If stale, upcoming deadlines won't appear on the dashboard

#### 3. `npm run gate` / `npm run validate`
- **When**: `npm run gate` before a push or PR — same six steps as `.githooks/pre-push`. `npm run validate` is the fuller local check (generated-file `--check` plus coverage). Remote CI is the Phase 2 Worker (`workers/portfolio-gate/`), not Actions.
- **What `npm run gate` does** (fail-closed; hook and script share `internal/scripts/portfolio-gate.mjs`):
  1. `npm run lint`
  2. `npm run typecheck`
  3. `node internal/scripts/validate-portfolio.mjs`
  4. `node internal/scripts/test-golden.mjs`
  5. `npx vitest run --reporter=dot`
  6. `python3 internal/scripts/verify-citations.py --check`
- **What `validate-portfolio` checks**: matter JSON schema, timeline references, document paths (disk or committed manifest when `PORTFOLIO_SKIP_DISK_DOCS=1`), damages/fees/coverage cross-checks, stale summaries/upcoming/README.
- **Why**: Prevents silent data corruption. A missing document, broken reference, or fabricated cite should fail the push.
- **Failure mode**: The push is refused. Missing `node_modules` or `python3` is a refusal, not a skip. `SKIP_PORTFOLIO_GATE=EMERGENCY` may skip the hook on a **feature branch only**; a push that updates `refs/heads/main` cannot bypass. `SKIP_PORTFOLIO_GATE=1` is ignored.

#### 4. `npm run generate:readme` (README sync)
- **When**: Manually run by developer (not automatic)
- **What it does**: Regenerates README.md tables from:
  - Matter JSON records → Active/Settled/Closed tables + case counts
  - timeline.json → Upcoming Deadlines table
  - damages.js → Damages Summary table
- **How it works**: Looks for HTML comment markers in README.md:
  ```html
  <!-- PORTFOLIO:ACTIVE_MATTERS:START -->
  ...table content...
  <!-- PORTFOLIO:ACTIVE_MATTERS:END -->
  ```
- **Why**: Keeps README documentation in sync without manual editing
- **Manual step**: After updating matters or timeline, run:
  ```bash
  npm run generate:readme
  git add README.md
  ```
- **CI check**: The `validate` script includes `generate:readme --check` to ensure README is current before merge

### Developer-Only Scripts

These are optional and not part of the build pipeline:

- `npm run scaffold:matter -- <N> "<caption>"` — Create a new matter JSON boilerplate
- `npm run index:build` — Build PDF document index (Python script)
- `npm run index:search` — Search documents by index
- Matter-specific Python scripts in `internal/scripts/` — Pleading generation, form filling, etc.

## Workflow Files

There is **no GitHub Actions CI** and no `.github/workflows/`. GitHub Actions
was dropped in September 2026 (billing; the remaining jobs then failed with
“Actions budget is preventing further use”). The local gate is
`.githooks/pre-push` / `npm run gate`. Phase 2 remote status is the
Cloudflare Worker in `workers/portfolio-gate/` (GitHub App + Containers),
which posts Check Run `portfolio-gate`. Do not add workflow YAML to invent
an Actions job.

```
1. npm run lint
2. npm run typecheck
3. node internal/scripts/validate-portfolio.mjs   (CRITICAL: data integrity gate)
4. node internal/scripts/test-golden.mjs
5. npx vitest run                                  (includes the prose-ceiling tests)
6. python3 internal/scripts/verify-citations.py --check
```

The hook is fail-closed: missing `node_modules` or `python3` exits 1.
`PORTFOLIO_SKIP_DISK_DOCS=1` is set automatically when the PDF tree is not on
disk (manifest mode — not a gate skip). Production deploys are scheduled from
a Cloudflare Worker, not from pushes; see `internal/docs/VERCEL_DEPLOYS.md`.

### Phase 2 remote gate (Cloudflare Worker — not Actions)

After the operator creates the GitHub App and deploys
`workers/portfolio-gate/` (runbook in that directory's `README.md`):

1. GitHub sends `pull_request` webhooks only; the Worker ignores any base
   other than `main`.
2. The Worker creates a pending Check Run named exactly `portfolio-gate`.
3. A Container clones the head SHA, runs `npm ci` then `npm run gate` with
   `PORTFOLIO_SKIP_DISK_DOCS=1` and `VITE_COPY_DOCUMENTS=0`.
4. The Check Run is patched success or **failure**. Fail-closed: webhook
   HMAC failure (401, no success path), Container cannot start, or no
   result within **25 minutes** (`GATE_TIMEOUT_MS`) → conclusion `failure`,
   never `neutral`.

One run per SHA. A new `synchronize` cancels older pending runs on the
previous SHA. Optional `check_run` rerequest is supported for this check
name on a main-targeting PR.

Do not add `.github/workflows/`. Do not point branch protection at an
Actions job.

### Branch protection (GitHub settings)

`main` must not be a free-for-all from the web UI. Configure this in GitHub
**Settings → Branches → Branch protection rule** for `main`. Still **no**
`.github/workflows/`. The required check is posted by the Worker, not by
Actions.

- [ ] Require a pull request before merging into `main`
- [ ] Do not allow force pushes
- [ ] Do not allow deletions of `main`
- [ ] Require status checks to pass → add exactly **`portfolio-gate`**
      (after the Worker is deployed; before that, the check does not exist)
- [ ] Do **not** require any Actions check (Actions is off)
- [ ] Do **not** add workflow YAML to invent those checks

The local hook still runs on every laptop/agent push to a code branch.
`SKIP_PORTFOLIO_GATE=EMERGENCY` cannot push to `main`; emergencies go through
a feature branch and a PR.

Laptop jobs that used to be Actions:

| Job | Command |
|---|---|
| CourtListener sync | `npm run court:sync -- --bootstrap` |
| R2 upload + path index | `npm run documents:push` |
| Worker deploy | `cd workers/doc-api && wrangler deploy` |
| Phase 2 portfolio-gate | `cd workers/portfolio-gate && wrangler deploy` (after App secrets; see that README) |
| D1 reseed | `node workers/doc-api/seed.mjs > seed.sql` then POST `/admin/reseed` |
| Dependency report | `npm run deps:outdated` |
| In-range npm bump | `npm run deps:update` |

Do not add workflow YAML. Do not add `.github/dependabot.yml`. Dependabot
version updates now run on GitHub Actions runners and a spending limit that
blocks Actions will block them (or put jobs back in the Actions tab).

External AIs get the Worker (`https://litigation-doc-api.ss8sxswwkt.workers.dev`),
not R2 admin keys. See `.cursor/rules/worker-not-keys.mdc`.

## Dependency updates (no Actions)

Weekly on the laptop:

```bash
npm run deps:outdated   # npm wanted/latest + requirements.txt floors vs PyPI
npm run deps:update     # npm update (lockfile, in-range only)
```

Majors are printed, not applied. Keep peer groups together (React stack,
Vitest stack). TypeScript majors stay ignored until typescript-eslint peers
TS 7+. `deps:outdated` exits 1 when something is stale so a missed week is
visible. Python floors live in `requirements.txt`; bump the `>=` line by
hand after the report.

Optional PR factory, still off Actions: install the
[Mend Renovate GitHub App](https://github.com/apps/renovate) on **this
repository only**, choose **Renovate only**, and leave GitHub Actions
disabled. Mend hosts the scan; `.github/renovate.json` already encodes the old
Dependabot groups (weekly npm, monthly pip, no `github-actions` manager).
Mend clones the private repo for the scan and deletes it afterward — if
that is unacceptable, stay on the laptop commands.


## Testing

Tests run in the pre-push hook / `npm run gate` and locally:

```bash
npm run gate          # Same six steps as pre-push
npm run test          # Unit suite only
```

### Test Coverage

Tests validate:
- **Matter schema** — all required fields, types, lifecycle/phase consistency
- **Data sync** — summaries.json, upcoming.json, README tables are current
- **Router basename** — base path handling for Vercel vs GitHub Pages
- **Timeline integrity** — events have required fields and valid matter references

## Troubleshooting

### "npm run gate failed" / pre-push refused

**Common causes:**
1. `node_modules` missing → `npm install`, then `npm run gate` (the hook no longer skips)
2. `python3` missing → install Python 3; the citation gate is required
3. `SKIP_PORTFOLIO_GATE=EMERGENCY` on a push to `main` → push a feature branch and open a PR
4. Matter JSON file missing a required field → Fix the JSON file
5. Document path doesn't exist → Add the file or update the reference
6. summaries.json is stale → Run `npm run sync:summaries`
7. upcoming.json is stale → Run `npm run sync:upcoming`
8. README.md tables are out of sync → Run `npm run generate:readme`
9. Matter number referenced in timeline doesn't exist → Check timeline.json

**To fix locally:**
```bash
npm run sync:summaries
npm run sync:upcoming
npm run generate:readme
npm run gate
```

### Production is stale

Vercel does not deploy on push. Check the deploy worker's cron ran
(`internal/workers/vercel-deploy-cron/`), or force a deploy:
`curl -X POST -H "authorization: Bearer $DEPLOY_TRIGGER_TOKEN" "https://<worker>/deploy?force=1"`.
`/version.json` on the live site shows which commit is deployed.

### Matter appears in dashboard but not in README

Run `npm run generate:readme` to regenerate README tables from current matter data.

## Data Flow Diagram

```
Developer commits (pre-commit hook syncs registry/manifest/README/vercel.json/Pages _redirects)
       ↓
Developer pushes (pre-push hook / npm run gate)
       ↓
  Lint + typecheck pass?
       ↓ YES
  validate-portfolio passes?
       ├─ Check matter JSON schema
       ├─ Check timeline references
       ├─ Check document paths (manifest when PDFs not on disk)
       └─ Cross-check damages/fees/coverage
       ↓ YES
  Golden math + unit suite + citation gate pass?
       ↓ YES
  Push accepted → PR targeting main
       ↓
Phase 2 Worker posts Check Run `portfolio-gate` (Container runs npm run gate)
       ↓
Required check green → merge to main
       ↓
Cloudflare cron (4x/day) sees main ahead of production → POSTs Vercel Deploy Hook
       ↓
Vercel Ignored Build Step: build inputs changed? → vite build → production
```

## Key Takeaways

1. **The validate script is critical** — It's the only place that checks cross-module consistency before code lands.
2. **Data sync runs in prebuild** — Ensures summaries and upcoming lists are always fresh on every build.
3. **README tables are generated, not edited** — Use `npm run generate:readme` to keep docs in sync with source of truth (matter JSON + timeline).
4. **Nothing deploys on push** — production advances from the scheduled Deploy Hook; `/version.json` tells you what is live.
5. **Tests catch regressions** — Router basename bugs are easy to introduce; tests prevent them.
