# Recovery Runbook

**Purpose:** Restore the interactive-litigation-portfolio from scratch if the
local machine, GitHub account, or repository is lost. Written for someone with
no prior context (bus factor = 1).

**Last verified:** 2026-10-05, by hash (`npm run audit:backup`, full re-hash of R2).

## What lives where

| Data | Location | Verified copies (2026-10-05) |
|------|----------|------------------------------|
| Source code, matter JSONs, clocks, manifest | `main` branch | GitHub only |
| Document bytes (1,684 manifest entries, 1,561 unique hashes) | Cloudflare R2 `litigation-documents`, key `sha256/<2>/<rest>.pdf` | 1,391 hashes present and re-hashed OK; **170 missing** |
| Same bytes, older | `documents` branch **history** | 1,526 hashes. The branch *tip* holds only ~13 PDFs: it was emptied around the 2026-09-17 R2 move (1,234 files on Sep 14, 49 on Sep 18). Its commits still hold the bytes. |
| Root PDFs, phone-tap slugs, `.txt`/`.meta.json` sidecars | `main` tree | 283 manifest hashes |
| D1 (matters, clocks, document rows, audit, OAuth) | Cloudflare D1 `litigation-portfolio` | Cloudflare only; rebuildable from `main` except `audit` and OAuth tables |

Copies per manifest hash: **32 have none** reachable (not in R2, any git
history, or D1), 137 have one, 1,392 have two or more. R2 and git history
are two providers, but neither is off-provider from both, and nothing is
offline. Re-run before trusting this table:

```bash
NODE_USE_ENV_PROXY=1 npm run audit:backup -- --out backup.json   # exit 1 lists every hash below 2 copies
```

The 32 with no copy were cataloged into the manifest (Matter 20 writ
package of Sep 30, Matter 32 default / mailing papers of Sep 16–18, Matter 40
Uber filing packet of Sep 23) but their bytes never reached R2 or git. If
they exist anywhere it is the machine that produced them. Find and push
them (`npm run documents:push`) before anything else.

### Restore one document from `documents` branch history

```bash
git fetch origin documents
F='internal/public/documents/matter-NN/<file>.pdf'
C=$(git log origin/documents --diff-filter=A --format=%H -- "$F" | tail -1)   # commit that added it
git show "$C:$F" > restored.pdf
sha256sum restored.pdf   # must equal the manifest sha256
```

## Restore from GitHub (full loss)

```bash
# 1. Clone both branches
git clone --branch main https://github.com/newanforbi/interactive-litigation-portfolio.git
cd interactive-litigation-portfolio
git worktree add ../portfolio-documents documents
# OR: git fetch origin documents:documents

# 2. Restore the document store (whole tree, or one matter).
#    Needs R2_* to read R2. Without it this falls back to the documents
#    branch TIP, which holds only ~13 PDFs; use the history recipe below.
npm run documents:pull -- --matter 24
# npm run documents:pull   # whole origin/documents tree

# 3. Install and build
npm ci
npm run build

# 4. Verify
npm run validate
```

## Restore a single deleted file

```bash
# From main branch history
git log --oneline -- path/to/file
git checkout <commit> -- path/to/file

# From documents branch (PDFs)
git checkout documents -- internal/public/documents/path/to/file.pdf
```

## Create an off-GitHub backup (do this)

The document store should exist in at least two places. Options:

### Option A: Backblaze B2 (recommended, cheap)
```bash
# Install rclone, configure a B2 remote named "b2"
git checkout documents
rclone sync ./internal/public/documents/ b2:litigation-portfolio-documents/ --progress
```

### Option B: External drive
```bash
git bundle create /Volumes/Backup/portfolio-documents.bundle documents
git bundle create /Volumes/Backup/portfolio-main.bundle main
```

### Verify the backup
```bash
# B2: compare file counts
rclone ls b2:litigation-portfolio-documents/ | wc -l
# Should match: git ls-tree -r documents --name-only | wc -l

# Bundle: verify it loads
git bundle verify /Volumes/Backup/portfolio-documents.bundle
```

## Secrets and credentials

These are **not** in the repo and must be re-created:

| Secret | Where it's used | How to re-create |
|--------|-----------------|------------------|
| `COURTLISTENER_TOKEN` | CourtListener docket sync (laptop `.env`; no Actions) | courtlistener.com profile → API token |
| `R2_*` | `documents:push` / `docs:fetch` (laptop `~/.config/r2/env`) | Cloudflare → R2 → API tokens |
| Worker secrets (`API_KEYS`, `RESEED_SECRET`, `ALERT_WEBHOOK`, GitHub App) | doc-api / portfolio-gate | `wrangler secret put …` in each worker dir |
| GitHub account access | Pushing, Actions | Aliko's GitHub account (`newanforbi`) |

## Contacts

- **Owner:** Aliko (GitHub: `newanforbi`)
- **Repo:** https://github.com/newanforbi/interactive-litigation-portfolio
