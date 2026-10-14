# CI Cloudflare deploy (phone-friendly)

Owner has no laptop. Worker deploys, D1 schema, and R2 document sync run
from GitHub Actions: `.github/workflows/cloudflare-deploy.yml`.

MCP is **not** a second Worker. It is `POST /mcp` on
`litigation-doc-api` (`workers/doc-api`). One `wrangler deploy` updates
REST and MCP together.

This workflow does **not** reseed D1 and does **not** drop tables. Schema
apply is `CREATE … IF NOT EXISTS` only (`workers/doc-api/schema.sql`, plus
any `workers/doc-api/migrations/*.sql` in name order).

Keep `PUBLIC_READ=true` on the live Worker. The workflow does not delete
or overwrite Worker secrets. `keep_vars = true` in `wrangler.toml` keeps
dashboard vars across deploys.

The portfolio **test** gate is still not Actions: `.githooks/pre-push` /
`npm run gate` locally, and `workers/portfolio-gate/` on PRs. Do not add
lint or vitest jobs to this workflow.

## What the workflow does

On push to `main` (path-filtered) and on **Run workflow**:

1. Fail immediately if `CLOUDFLARE_API_TOKEN` or `CLOUDFLARE_ACCOUNT_ID`
   are missing.
2. `wrangler d1 execute litigation-portfolio --remote --yes --file=schema.sql`
   (database id `5e920ba3-722d-448d-93ca-304c1e31bee9`). Idempotent.
3. `wrangler deploy` in `workers/doc-api` (REST + MCP).
4. `npm run documents:sync -- --apply` when R2 S3 secrets exist. If they
   are missing, that step **skips** (warning, exit 0). Never DELETE/DROP.

One production deploy at a time (`concurrency` group `cloudflare-deploy`).
In-flight runs are not cancelled.

## Repo secrets

| Secret | Required | What it is |
|---|---|---|
| `CLOUDFLARE_API_TOKEN` | **Yes** | Account API token (permissions below). Workflow fails if empty. |
| `CLOUDFLARE_ACCOUNT_ID` | **Yes** | Cloudflare account id (also used as `R2_ACCOUNT_ID`). |
| `R2_ACCESS_KEY_ID` | Optional | R2 **S3** access key for `litigation-documents`. |
| `R2_SECRET_ACCESS_KEY` | Optional | Matching R2 S3 secret. Both R2 secrets must be set or sync skips. |

Do not put R2 admin / Cloudflare dashboard keys in chat. These secrets
live only in GitHub Actions secrets (and, on a future laptop,
`~/.config/r2/env`).

## Minimal custom API token

Create an **account** API token (not the Global API Key). Start from
**Create Token → Custom token**, not “Edit Cloudflare Workers”, then add
only:

| Scope | Permission | Why |
|---|---|---|
| Account | **Account Settings — Read** | Wrangler `whoami` / account select |
| Account | **Workers Scripts — Edit** | `wrangler deploy` of existing `litigation-doc-api` |
| Account | **D1 — Edit** | `wrangler d1 execute` (schema / FTS) |
| Account | **Workers R2 Storage — Edit** | Wrangler R2 if a later step uses it |

**Not needed today** (doc-api has no custom zone route and no KV):

| Scope | Permission | When to add |
|---|---|---|
| Zone | **Workers Routes — Edit** | Only if you attach a custom domain / route |
| Account | **Workers KV Storage — Edit** | Only if a Worker binds KV |

Do **not** grant Users / Billing / Account Settings Edit, D1 delete-beyond-Edit,
or Workers Scripts Admin unless you are creating a brand-new Worker name.
`litigation-doc-api` already exists, so **Edit** is enough.

R2 **object** uploads in `documents:sync` do **not** use this API token.
They use a separate **R2 S3 API token** stored as `R2_ACCESS_KEY_ID` /
`R2_SECRET_ACCESS_KEY`. Scope that token to bucket `litigation-documents`,
Object Read & Write (not admin).

## iPhone setup (Safari, Request Desktop Website)

Do these once. After that, every merge to `main` that touches the Worker
or `documents/` deploys itself.

### 1. Raise the Actions spending limit

Older jobs were refused because the Actions budget was $0.

1. Open [github.com](https://github.com) in Safari.
2. Tap **aA → Request Desktop Website**.
3. Profile picture → **Settings → Billing and plans**.
4. **Metered billing / Spending limits → Actions**.
5. Set a small limit (a few dollars). First `documents:sync` of the
   public library is the expensive run; later runs HEAD-skip existing
   R2 objects.
6. Repo → **Settings → Actions → General → Allow all actions and
   reusable workflows**. Save.

If a run never starts and the Actions tab says the budget is preventing
further use, this is the fix — not a workflow bug.

### 2. Cloudflare account id

1. Open [dash.cloudflare.com](https://dash.cloudflare.com).
2. **Workers & Pages**.
3. Copy **Account ID** from the right sidebar. That is
   `CLOUDFLARE_ACCOUNT_ID`.

### 3. Cloudflare API token

1. [dash.cloudflare.com/?to=/:account/api-tokens](https://dash.cloudflare.com/?to=/:account/api-tokens)
   (Account API tokens).
2. **Create Token → Custom token**.
3. Name: `github-actions-litigation-deploy`.
4. Permissions — add the four Account rows in the table above
   (Account Settings Read, Workers Scripts Edit, D1 Edit,
   Workers R2 Storage Edit).
5. Account resources: **Include** → this account only.
6. **Continue to summary → Create Token**.
7. Copy the token **now**. Cloudflare will not show it again.

### 4. R2 S3 token (optional, needed for PDF upload)

1. Dashboard → **R2**.
2. **Manage R2 API Tokens → Create API token**.
3. Permission: **Object Read & Write**.
4. Specify bucket: `litigation-documents` only, if the UI allows.
5. Create. Copy **Access Key ID** and **Secret Access Key**.
6. These become `R2_ACCESS_KEY_ID` and `R2_SECRET_ACCESS_KEY`.

### 5. Paste secrets into GitHub

1. Open the repo on github.com (desktop site).
2. **Settings → Secrets and variables → Actions**.
3. **New repository secret** for each row:

   - `CLOUDFLARE_API_TOKEN` = the custom token
   - `CLOUDFLARE_ACCOUNT_ID` = the account id
   - `R2_ACCESS_KEY_ID` = R2 S3 access key (optional)
   - `R2_SECRET_ACCESS_KEY` = R2 S3 secret (optional)

4. Do not put these in Issues, chat, or the repo.

### 6. First run (leftover from PR #988)

1. Repo → **Actions**.
2. Left list → **Cloudflare deploy**.
3. **Run workflow** (branch `main`). Leave both skip boxes unchecked.
4. Wait for **Deploy worker + D1 schema** (green) and
   **Sync documents to R2** (green, or a yellow warning if R2 secrets
   were skipped).

That applies FTS (`documents_fts`), deploys `litigation-doc-api` (and
`/mcp`), and uploads repo-only public PDFs. Do **not** run a D1 reseed.

Manual laptop equivalents remain:

```bash
cd workers/doc-api && wrangler deploy
wrangler d1 execute litigation-portfolio --remote --yes --file=schema.sql
npm run documents:sync -- --apply
```

## After it is working

- Push to `main` that changes `workers/doc-api/**` → schema + deploy.
- Push that changes `documents/**` (or the sync scripts) →
  `documents:sync --apply` when R2 secrets exist.
- Changing this workflow file itself runs both (bootstrap).
- **Actions → Cloudflare deploy → Run workflow** any time from the phone.
- Check `https://litigation-doc-api.ss8sxswwkt.workers.dev/health`.
- MCP URL is unchanged:
  `https://litigation-doc-api.ss8sxswwkt.workers.dev/mcp`.

`portfolio-gate`, `ilp-vercel-deploy-cron`, and
`ilp-courtlistener-webhook` are **not** deployed by this workflow
(container image / extra secrets). Deploy those from a laptop or a
future dedicated workflow.
