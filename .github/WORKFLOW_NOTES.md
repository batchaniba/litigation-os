# Workflow and Data Pipeline Documentation

## Overview

This repository uses a multi-stage data pipeline to keep the interactive litigation portfolio in sync across the SPA bundle, README documentation, and validation gates.

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

#### 3. `npm run validate` (CI gate)
- **When**: Runs in CI before build, and before GitHub Pages deployment
- **What it does**: Comprehensive portfolio integrity checks:
  - Validates matter JSON schema (required fields, types, lifecycle/phase consistency)
  - Checks timeline references (all matter numbers exist)
  - Verifies document paths (all referenced files exist on disk)
  - Cross-references damages.js and lawyerFees.js (no orphaned or missing entries)
  - Reports orphan documents and missing `filed` status
  - Re-checks that summaries.json, upcoming.json, and README are current
- **Why**: Prevents silent data corruption. A missing document or broken reference should fail the build.
- **Failure mode**: Build stops; forces developer to fix the issue

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

### `.github/workflows/ci.yml`

Runs on every push to any branch:

```
1. Checkout
2. Setup Node 22
3. npm ci (install dependencies)
4. npm run typecheck (TypeScript check)
5. npm run validate (CRITICAL: data integrity gate)
6. npm run test (Vitest suite)
7. npm run build (vite build)
```

### Dependabot (`.github/dependabot.yml`)

Configured for parallel human + bot work:

- **`rebase-strategy: auto`** on npm, github-actions, and pip — when a Dependabot PR conflicts with `main`, Dependabot rebases it instead of leaving it `DIRTY`.
- **Grouped minor/patch** updates (dev tooling, build tooling, React ecosystem, Actions, pip) so routine bumps arrive as a few weekly PRs rather than a dozen stale branches.
- **Peer-locked majors are grouped** (`react-majors`, `vitest-majors`) so Dependabot cannot open half-upgrades that fail `npm ci`.
- **TypeScript majors ignored** until `typescript-eslint` supports TS 7+.
- **`open-pull-requests-limit: 8`** (npm) / **3** (Actions, pip).

If a Dependabot PR still looks stuck after a large `main` merge, comment `@dependabot recreate` on that PR (you need push access). `@dependabot rebase` is enough when the only issue is a content conflict.

**Why this order?**
- Typecheck first (fast, catches syntax errors early)
- Validate before build (prevents corrupted data from being bundled)
- Tests after validate (tests assume valid data)
- Build last (most expensive step, only after all checks pass)

### `.github/workflows/deploy-gh-pages.yml`

Runs on push to `main` and manual dispatch:

```
1-6: Same as CI (checkout, setup, install, typecheck, validate, test)
7. npm run build with GITHUB_PAGES=true (sets base path to /interactive-litigation-portfolio/)
8. Upload dist/ to GitHub Pages artifact
9. Deploy to GitHub Pages
```

**Key difference**: Sets environment variable `GITHUB_PAGES=true` so vite.config.js can set the correct base path:

```javascript
export default defineConfig({
  base: process.env.GITHUB_PAGES === 'true' 
    ? '/interactive-litigation-portfolio/' 
    : '/',
})
```

This allows the same codebase to deploy to both:
- **Vercel** (https://interactive-litigation-portfolio.vercel.app) — base: `/`
- **GitHub Pages** (https://newanforbi.github.io/interactive-litigation-portfolio/) — base: `/interactive-litigation-portfolio/`

### `.github/workflows/courtlistener-sync.yml`

Hourly (`17 * * * *`) plus `workflow_dispatch`. Needs repository secret `COURTLISTENER_TOKEN` (never a `VITE_*` variable).

```
1. Checkout (same sparse skip of the PDF tree as CI)
2. npm ci
3. npm run court:resolve     # bind new federal dockets; skip already-bound IDs
4. npm run court:sync        # incremental docket entries
5. npm run sync:all
6. npm test
7. Open/update standing PR from automation/courtlistener-sync
```

The job does **not** commit to `main`. Deadline candidates stay in `internal/src/data/courtlistener/review.json` until someone copies them into `timeline.json`. See `internal/docs/COURTLISTENER.md`.


## Testing

Tests run in CI (both workflows) and can be run locally:

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

### "npm run validate failed" in CI

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

### Deployment fails but CI passes

If CI passes but GitHub Pages deployment fails:
1. Check that `GITHUB_PAGES=true` is set (see deploy-gh-pages.yml)
2. Check that router basename is using `BASE_URL` correctly (see vite.config.js, main.tsx)
3. Check GitHub Pages settings (should be set to "Deploy from a branch")

### Matter appears in dashboard but not in README

Run `npm run generate:readme` to regenerate README tables from current matter data.

## Data Flow Diagram

```
Developer commits → GitHub
       ↓
  CI Workflow runs
       ↓
  Typecheck passes?
       ↓ YES
  Validate passes?
       ├─ Check matter JSON schema
       ├─ Check timeline references
       ├─ Check document paths
       ├─ Cross-check damages/fees
       └─ Ensure summaries/upcoming/README current
       ↓ YES
  Tests pass?
       ↓ YES
  Build passes?
       ↓ YES
  ✅ CI passes
       ↓
       ├─→ Regular branch: CI-only
       │
       └─→ main branch:
           Deploy to GitHub Pages
           (with GITHUB_PAGES=true for correct base path)
```

## Key Takeaways

1. **The validate script is critical** — It's the only place that checks cross-module consistency before code lands.
2. **Data sync runs in prebuild** — Ensures summaries and upcoming lists are always fresh on every build.
3. **README tables are generated, not edited** — Use `npm run generate:readme` to keep docs in sync with source of truth (matter JSON + timeline).
4. **GitHub Pages needs GITHUB_PAGES=true** — Without it, all routes fail because the base path is wrong.
5. **Tests catch regressions** — Router basename bugs are easy to introduce; tests prevent them.
Copilot cloud agent access test - safe to delete this line.
