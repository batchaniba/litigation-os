# Workflow and Data Pipeline Documentation

## Overview

This repository uses a multi-stage data pipeline to keep the interactive litigation portfolio in sync across the SPA bundle, README documentation, and validation gates.

There are **no GitHub Actions workflows**. Do not add `.github/workflows/`.
The spending limit already refuses every job. The gate is `.githooks/pre-push`.

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

#### 3. `npm run validate` (the gate)
- **When**: By hand before a PR. The `pre-push` hook runs the same checks (minus coverage thresholds) on every push to a code branch; there is no CI.
- **What it does**: Comprehensive portfolio integrity checks:
  - Validates matter JSON schema (required fields, types, lifecycle/phase consistency)
  - Checks timeline references (all matter numbers exist)
  - Verifies document paths (all referenced files exist on disk)
  - Cross-references damages.js and lawyerFees.js (no orphaned or missing entries)
  - Reports orphan documents and missing `filed` status
  - Re-checks that summaries.json, upcoming.json, and README are current
- **Why**: Prevents silent data corruption. A missing document or broken reference should fail the build.
- **Failure mode**: The push is refused; fix the issue (or `SKIP_PORTFOLIO_GATE=1` for a genuine emergency)

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

There is **no CI** and no `.github/workflows/`. GitHub Actions was dropped in
September 2026 (billing; the remaining jobs then failed with “Actions budget
is preventing further use”) and the gate is `.githooks/pre-push`:

```
1. npm run lint
2. npm run typecheck
3. node internal/scripts/validate-portfolio.mjs   (CRITICAL: data integrity gate)
4. node internal/scripts/test-golden.mjs
5. npx vitest run                                  (includes the prose-ceiling tests)
6. python3 internal/scripts/verify-citations.py --check
```

`PORTFOLIO_SKIP_DISK_DOCS=1` is set automatically when the PDF tree is not on
disk. Production deploys are scheduled from a Cloudflare Worker, not from
pushes; see `internal/docs/VERCEL_DEPLOYS.md`.

Laptop jobs that used to be Actions:

| Job | Command |
|---|---|
| CourtListener sync | `npm run court:sync -- --bootstrap` |
| R2 upload + path index | `npm run documents:push` |
| Worker deploy | `cd workers/doc-api && wrangler deploy` |
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

Tests run in the pre-push hook and locally:

```bash
npm run test          # Run once
npm run test:watch    # Watch mode
```

### Test Coverage

Tests validate:
- **Matter schema** — all required fields, types, lifecycle/phase consistency
- **Data sync** — summaries.json, upcoming.json, README tables are current
- **Router basename** — base path handling for Vercel vs GitHub Pages
- **Timeline integrity** — events have required fields and valid matter references

## Troubleshooting

### "npm run validate failed" / pre-push refused

**Common causes:**
1. Matter JSON file missing a required field → Fix the JSON file
2. Document path doesn't exist → Add the file or update the reference
3. summaries.json is stale → Run `npm run sync:summaries`
4. upcoming.json is stale → Run `npm run sync:upcoming`
5. README.md tables are out of sync → Run `npm run generate:readme`
6. Matter number referenced in timeline doesn't exist → Check timeline.json

**To fix locally:**
```bash
npm run sync:summaries
npm run sync:upcoming
npm run generate:readme
npm run validate
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
Developer commits (pre-commit hook syncs registry/manifest/README/vercel.json)
       ↓
Developer pushes (pre-push hook)
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
  Push accepted → PR → main
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
