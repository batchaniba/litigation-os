# Recovery Runbook

**Purpose:** Restore the interactive-litigation-portfolio from scratch if the
local machine, GitHub account, or repository is lost. Written for someone with
no prior context (bus factor = 1).

**Last verified:** 2026-09-11

## What lives where

| Data | Location | Size | Backup status |
|------|----------|------|---------------|
| Source code, matter JSONs, timeline | `main` branch | ~small | GitHub only |
| PDF document store (1,196 files) | `documents` branch | ~large | GitHub only |
| Generated build outputs | Built at deploy time | — | Regenerable |

**Critical:** As of 2026-09-11, there is **no off-GitHub backup**. If GitHub
loses both branches, the data is gone. See "Create an off-GitHub backup" below.

## Restore from GitHub (full loss)

```bash
# 1. Clone both branches
git clone --branch main https://github.com/newanforbi/interactive-litigation-portfolio.git
cd interactive-litigation-portfolio
git worktree add ../portfolio-documents documents
# OR: git fetch origin documents:documents

# 2. Restore the document store (whole tree, or one matter)
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
| `COURTLISTENER_TOKEN` | CourtListener docket sync | Add as repo secret in GitHub Settings → Secrets |
| GitHub account access | Pushing, Actions | Aliko's GitHub account (`newanforbi`) |

## Contacts

- **Owner:** Aliko (GitHub: `newanforbi`)
- **Repo:** https://github.com/newanforbi/interactive-litigation-portfolio
