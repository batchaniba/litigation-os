# Vercel cost audit — team `newanforbis-projects`

**Date:** 28 October 2026  
**Scope:** read-only inventory of Vercel team `newanforbis-projects` (`team_Im0u0AeSdczjotkekBRw2SOI`) and GitHub owner `newanforbi`. **No dashboard writes, no plan change, no add-on toggle, no deployment deletes.**  
**Method:** Vercel MCP (`list_projects`, `get_project`, `list_deployments`, `list_domains`, `get_domain`, `list_billing_charges` for 12 Oct 2026) plus GitHub repo reads. The Vercel CLI is installed via npx in this environment but is **not logged in** (`VERCEL_TOKEN` absent), so CLI `vercel list --policy` / per-deployment byte sizes were not available. Deployment *counts and states* come from the API; *storage dollars* come from the billing pages the user already captured plus one FOCUS sample day.

---

## Recommended plan (read this first)

Stay on **Pro for one more billing cycle**, cut the two line items that actually hurt, then leave Vercel.

1. **This week (dashboard only):** set a short Deployment Retention Policy on the whole team and apply it to existing projects; turn off **Speed Insights Plus**; set Spend Management to a **$5 on-demand** cap with email alerts. Leave “Pause production deployments” **off** until retention has drained storage — the last pause is why every site currently returns `402 DEPLOYMENT_DISABLED`.
2. **Do not unpause all 14 projects.** Unpause only the sites that must be public. Leave the rest paused; they still occupy Deployment Storage until retention deletes them.
3. **Over the next weeks:** move static sites to **Cloudflare Pages** (already started for the litigation portfolio). Keep the domains. Point DNS at Cloudflare.
4. **Do not downgrade to Hobby** while a law-firm site, a commercial calculator, a lottery product, or Citeproof still live on this team. Hobby is non-commercial and caps storage at 10 GB.
5. **After the static sites are off Vercel and storage has fallen inside the $20 credit:** cancel Pro. Ongoing hosting cost becomes **$0**. Remaining cost is domain renewals (~$67/year on Vercel’s registrar, plus Namecheap for two external domains).

**Expected monthly hosting after the dashboard cuts, still on Pro:** **$20** (platform fee). Usage should sit inside the included $20 credit once retention has run.  
**Expected monthly hosting after Cloudflare cutover and Pro cancel:** **$0**, plus domain renewals as they come due.  
**If nothing changes:** the 12 Nov invoice stays about **$30** (Pro $20 + Speed Insights Plus $10), and Deployment Storage will grow again the moment the 14 projects are unpaused with 180-day / 1-year retention still in force.

---

## 1. What the invoices already say

Billing period is the **12th to the 12th**. Pro is **$20/mo** and includes **$20 of usage credit**.

| Period | What happened |
|---|---|
| Jul–Aug 2026 | Domain registrations: **$17.99, $37.99, $5.99, $11.25** (see §5). |
| 12 Sep – 27 Oct | ~**$55**, of which Deployment Storage ~**$42.58**. Card failure; 12 Oct invoice **$64.05** went overdue; now paid. |
| 12 Oct – 12 Nov (in progress) | Usage so far **$15.28**, fully covered by the $20 credit. Biggest line: Deployment Storage **4.32 TB = $14.39**. Function Storage 36.41 GB = $0.12. Speed Insights events $0.65. Image optimization / ISR tiny. Upcoming invoice **est. $30** = Pro $20 + Speed Insights Plus $10 (1 project). |
| All 14 projects | `402 DEPLOYMENT_DISABLED` since ~12 Sep (spend-management / billing pause). Old deployments are **still stored**. |

FOCUS charges for **11–12 Oct 2026** (one UTC day at the previous-invoice boundary) match that story:

- Deployment Storage **$1.76 that day** across 14 projects → about **527 GB** sitting on disk that day (`$0.10` per GB-month, 1 day ≈ 1/30 of a month).
- Function Storage **$0.007** that day, **2.25 GB** total, almost all Citeproof + photo-album.
- Image Optimization cache writes that day: church website 129, Citeproof 21.
- Pro seat accrued at **$0.67/day** ($20 / 30).
- Speed Insights Plus appeared in the catalog with **$0 that day** (the $10 is a monthly add-on, not a daily usage line).

The **4.32 TB** on the current invoice is **not a 4.32 TB disk footprint**. Vercel bills GB-months. 4.32 TB of *GB-days* × $0.10 / ~30 days = **$14.40**, which is the $14.39 line. Over ~16 days of this period that is an **average of ~270 GB stored**, down from ~527 GB on 12 Oct. The Oct 23 existing-team storage cleanup may have started to bite; default Pro retention (1 year production / 180 days preview) is still long enough to keep hundreds of GB.

---

## 2. Inventory — 14 Vercel projects

Every project: `live: false` (paused). Node 24.x. SSO protection on (preview or all-except-custom-domains). No `crons` key in any `vercel.json` searched under `user:newanforbi`.

Deployment counts below are **currently listed** by the API (not historical lifetime). Byte sizes per deployment are **not** in the list payload; Function Storage GB from 12 Oct is the only per-project size proxy.

| Vercel project | GitHub repo | Framework / output | Custom domains | Deploys listed | Speed Insights / Analytics | Cron / functions / images / ISR | Notes |
|---|---|---|---|---|---|---|---|
| `interactive-litigation-portfolio` | `newanforbi/interactive-litigation-portfolio` (~888 MB git) | **Vite** SPA, `dist/`. `vercel.json` generated; `"git": { "deploymentEnabled": false }`. Ignore script `internal/scripts/vercel-ignore-build.sh`. Cloudflare Pages Function at `functions/documents/[[path]].js`. | vercel.app only | **58** (40 READY, 10 CANCELED, 6 BLOCKED, 2 ERROR). 21 prod / 37 preview. `documents` branch still creating records. | `@vercel/analytics` + `@vercel/speed-insights` in `App.tsx` | No Vercel cron. Production advances via Cloudflare Worker deploy hook. `/documents/*` rewrites to the doc-api Worker. PDFs used to copy into `dist/` (~660 MB); `VITE_COPY_DOCUMENTS=0` now skips that. | Latest deploy 24 Oct **ERROR** (`documents` branch, ignore script missing on that branch). Function Storage 0. |
| `book-of-brendan` | `meditations-blog` (private) | **Eleventy 3**, `_site/` | **bookofbrendan.blog**, www | **12** READY (mix prod/preview). Latest prod **8 Oct** (after the ~12 Sep pause). | none | Static. `noindex` / sitemap lastmod work in Oct. | Easy Cloudflare Pages move. |
| `lottery-assets` | `lottery-assets` (private) | **Vite** SPA, `dist/` | **lotteryassets.com**, www | **38** READY | none | Static. | Commercial-looking product. Easy Pages move. |
| `ngwa-nforbi-law-firm` | `ngwa-nforbi-law-firm` | **Next.js 15**, `next build` | vercel.app only | **39** READY | none | `next.config.ts` enables `images.formats` webp/avif. No cron. | **Commercial** (law firm). Hobby TOS problem. |
| `early-warning` | `early-warning` (private) | **Next.js 16** (`vercel.json` pins framework) | vercel.app only | **11** (READY + BLOCKED + 1 ERROR) | none | Next app. `.vercelignore` excludes PDFs. | Personal dashboard. |
| `citizen-by-2027` | `citizen-by-2027` (private) | Vite SPA (`frontend/dist`), SPA rewrites | vercel.app only | **30** READY. Last deploy **Mar 2026**. | none | Static. | Dead project; keep paused. |
| `nbnn-law-concept` | `nbnn-law-concept` (private) | **Vite** per Vercel; committed `vercel.json` is a **legacy Python** `@vercel/python` app | vercel.app only | **40** READY (20 prod / 20 preview) | `@vercel/analytics` | Function Storage 0.10 GB on 12 Oct (Python/Vite leftover). | Stale config. Keep paused or archive. |
| `pleading-paper-formatter` | `pleading-paper-formatter` | Vanilla HTML/JS (no `package.json` at root) | vercel.app only | **18** READY | Vercel Web Analytics installed Mar 2026 | Static. | Easy Pages / GitHub Pages. |
| `t-minus-may-2026` | `t-minus-may-2026` (private) | **Next.js** (`vercel.json` `outputDirectory: .next`) | vercel.app only | **6** READY. Last deploy **Apr 2026**. | none | Small Next app. Function Storage 0.007 GB. | Campaign dashboard; keep paused. |
| `church-website-scaffold` | `church-website-scaffold` | **Next.js 16** | **rccgorunshi.org**, www | **40** READY (20/20) | none | Image Optimization: **129 cache writes** on 12 Oct. ISR/image lines on the invoice. | Church site. Pages-capable if static-exported or OpenNext. |
| `newanforbi-pro-se` | `newanforbi-pro-se` (private; not in public search, still linked) | **Next.js** | vercel.app only | **15** READY. Last deploy **18 Jul**. | none | Function Storage 0.009 GB. | Scaffold; keep paused. |
| `equity2bitcoin` | `equity2bitcoin` | **Vite** SPA, SPA rewrite | **equity2bitcoin.com**, www (DNS at Namecheap) | **32** READY. Last deploy **2 Aug**. | none | Static. | **Commercial**. Hobby TOS problem. |
| `case-law-verification-engine` | `case-law-verification-engine` | **Next.js 15** | **citeproof.io**, www | **40** READY (20/20) | `@vercel/speed-insights` + `@vercel/analytics` + **`@vercel/blob`** | **Functions:** `/api/verify` 120s, `/api/verify-pdf` **300s**. Traces tesseract WASM + `@napi-rs/canvas` into the lambda. Function Storage **1.45 GB** on 12 Oct (largest). Image opt 21 writes. | The only project that *needs* a serverless host. Likely the Speed Insights Plus project. |
| `photo-album` | `photo-album` (~69 MB git) | **Next.js 15**, `next.config.mjs`, `middleware.ts` | **brendanngwanforbi.com**, www (Namecheap) | **8** READY | none | Default Next image pipeline. Function Storage **0.56 GB** on 12 Oct (second). Site is noindex / 410 on removed photo URLs. | JPEGs in-repo; keep off Google. |

**GitHub repos with `vercel.json` but not a Vercel project in this team:** none extra of note. Repos under `newanforbi` that do **not** deploy here (resume generator, `ai-lawyer-book`, `truckers-against-trafficking`, `plan-my-life`, crypto notebooks, etc.) are out of scope.

**Vercel CLI:** not authenticated here. Project list, domains, deployment counts/states, and one billing day were pulled via MCP. Per-deployment artifact bytes are not in that payload.

---

## 3. Why Deployment Storage is 4.32 TB, and how to cut it

### How the meter works

- Each **successful** deployment stores build output (static assets) plus Function bundles in every region they occupy.
- Pro list price: **$0.10 per GB-month** for Deployment Storage and for Functions Storage. Hobby includes **10 GB**; Pro’s $20 credit is supposed to cover this until it doesn’t.
- Vercel records **each project’s max stored GB each billing day**, then sums those days. 1 GB held all month = 1 GB-month = $0.10.
- The usage UI’s **4.32 TB** is the **sum of daily GB** (GB-days), not “we are storing 4.32 terabytes right now.” $14.39 ÷ $0.10 × ~30 days ≈ 4,317 GB-days ≈ **~270 GB average** this period.
- A deployment **stops billing the moment it is first deleted**. The recovery window after delete is not billed.

### Why it got this big

Three multipliers, all present:

1. **Count.** The API still lists on the order of **380 deployments** across 14 projects. Historically this team built on every push to every branch (see `internal/docs/VERCEL_DEPLOYS.md`: 300+ commits/week on the portfolio plus a preview per PR). Default **Pro retention** is **canceled 30d / errored 90d / preview 180d / production 1 year**, plus exceptions (last 10 deploys, last 20 production Ready, last 20 preview Ready, anything with a production or custom alias, latest preview of an open PR).
2. **Size.** The litigation portfolio git tree is ~888 MB. Until `VITE_COPY_DOCUMENTS=0`, production copies of the PDF library went into `dist/`. Citeproof traces Tesseract + canvas into every function bundle (1.45 GB function storage for that project *alone* on 12 Oct). Photo-album keeps JPEGs in git (~69 MB) and runs Next image optimization. Church used Image Optimization on 12 Oct even while paused (cached assets still sitting).
3. **Time.** Pause stopped *new* production, but **did not delete old output**. Storage billed through September–October at ~$42. 9 Oct 2026 changelog: existing Pro teams start paying for Deployment Storage; deployments older than 30 days would be deleted from 23 Oct **unless retention was left longer**. This team’s remaining ~270–527 GB means retention was **not** shortened to 30 days (or exceptions kept a large set).

The `documents` branch on the portfolio is still opening deployment records in October (CANCELED via ignore-build, or ERROR because that branch does not contain `internal/scripts/vercel-ignore-build.sh`). Canceled/errored output has its own retention. `git.deploymentEnabled: false` on `main` does not protect a branch whose `vercel.json` predates that key.

### How to cut it (dashboard, in order)

Do these **before** unpausing anything.

1. **Team → Settings → Security / Retention → Deployment Retention Policy**  
   Set and **apply to all existing projects**:
   - Canceled: **1 day**
   - Errored: **1 day**
   - Preview / pre-production: **7 days**
   - Production: **30 days**  
   Production aliases and the latest preview of an open PR are kept anyway (exceptions). 30-day production is enough to roll back a bad release; 1-year production is how this bill happened.

2. **Optional one-time prune (you, not this agent):** in each project → Deployments, delete old preview rows that are not the current production alias. Not required if (1) is applied; the policy will catch them within ~48 hours, then up to 30 days for exception re-evaluation.

3. **Project → Settings → Git** on every project you might unpause:
   - Ignored Build Step → Custom: skip non-`main` (snippet in §6).
   - Or Ignored Build Step “Don’t build” for projects that should stay frozen.
   - Turn off automatic deploy of the `documents` branch on the portfolio (Deployments still fire there).

4. **Smaller outputs (repo, after unpause):** keep `VITE_COPY_DOCUMENTS=0` / `PORTFOLIO_SKIP_DISK_DOCS=1` on the portfolio; serve PDFs from R2 via the Worker. Do not put the photo library in every Next build if the album stays on Vercel — object storage (R2) is cheaper than Deployment Storage at $0.10/GB-month. Citeproof: the tesseract trace is why Function Storage is 1.45 GB; shrinking that bundle is a later optimization, not this week’s $10.

5. **Do not unpause the 10 projects that have no public domain.** Every extra Ready production is another copy of `.next` or `dist` held for the retention window.

---

## 4. Plan comparison

Assumptions: sites actually need to be up; domains stay registered; no surprise on-demand after controls.

| Option | Monthly hosting | What you get | What breaks / TOS | When to choose |
|---|---|---|---|---|
| **A. Pro, untrimmed (status quo after unpause)** | **~$30–65+** | Everything. Speed Insights Plus $10. Storage returns to September levels if retention stays 180d/1y and previews build again. | Card failure already paused all 14 sites. | Never. |
| **B. Pro, trimmed (recommended bridge)** | **$20** | One deploying seat, $20 usage credit, Spend Management, 300s functions (Citeproof’s 300s `verify-pdf` fits). Drop Speed Insights Plus. Short retention. Basic build machine, no Turbo, no on-demand concurrency (already documented for the portfolio). | Still $20 even if usage is $0. | Now, until Cloudflare cutover. Covers Citeproof and any commercial site. |
| **C. Hobby** | **$0** | 10 GB deployment storage, 100 GB Fast Data Transfer, 100 deploys/day, 4 CPU-hrs, 10k Speed Insights events / 30 days, no Spend Management, no extra usage purchase. Retention 30 days all states. | **Non-commercial only.** Law firm, Equity2Bitcoin, Lottery Assets, and Citeproof-as-a-product are commercial under [Fair Use](https://vercel.com/docs/limits/fair-use-guidelines). Current ~270 GB stored **already exceeds 10 GB**. Hobby cannot buy more storage. Vercel may disable Hobby deployments without notice. One Hobby team per account; downgrade removes other members and requires moving domains/stores first. | Only after commercial sites are off Vercel **and** storage is under 10 GB. Not a path for this team today. |
| **D. Cloudflare Pages + Workers (recommended destination)** | **$0** on the Free plan | Unlimited static bandwidth and static requests. 500 builds/month, 1 concurrent build, 100 custom domains/project, 20k files/site, 25 MiB/file. Pages Functions share Workers Free (100k requests/day). Portfolio Phase 1 already exists: `interactive-litigation-portfolio.pages.dev`. PDFs live in R2; `/documents/*` is already a Pages Function proxy. | Citeproof’s 300s OCR/canvas lambda is **not** a drop-in Pages Function (10 ms CPU on Workers Free). Move it last, or keep **one** Vercel Pro project for Citeproof only ($20) until a Worker port exists. Photo-album and church Next apps need `output: 'export'` or OpenNext, not a blind git connect. ILP `vercel.json` has many redirects; Pages uses generated `_redirects` / `_headers` (already in this repo). | Static sites now. Citeproof when you can spare the port — or keep Pro just for that one project. |
| **E. GitHub Pages** | **$0** | Fine for tiny static sites (`pleading-paper-formatter`, `citizen-by-2027`). | This **portfolio repo must not add `.github/workflows/`** (spending limit / `AGENTS.md`). Other repos can. Custom domains work. No serverless. Worse CDN than Cloudflare, which you already use. | Only as a backup for repos that are not the portfolio. Prefer Cloudflare. |

**Citeproof-only Pro:** $20/mo forever if you want the 300s function and Blob without porting. That is still cheaper than 14 paused projects plus Speed Insights Plus.

**Do not** run Hobby and Pro in parallel as a “cheap Pro.” Downgrade mechanics force a merge or delete of the extra team.

---

## 5. Domains — renewals to watch

Vercel registrar (`ns1/ns2.vercel-dns.com`, `renew: true`) — purchase prices from the Jul/Aug 2026 invoices, mapped by TLD. `get_domain_price` returned a null purchase price in this environment; treat renewal as **at least last year’s registration**, and confirm on the domain’s Vercel page before the date.

| Domain | Registrar | Bought | Expires | Last paid (inferred) | Project |
|---|---|---|---|---|---|
| **citeproof.io** | Vercel | 9 Aug 2026 | **9 Aug 2027** | **$37.99** (.io) | case-law-verification-engine |
| **bookofbrendan.blog** | Vercel | 14 Aug 2026 | **14 Aug 2027** | **$17.99** (.blog) | book-of-brendan |
| **lotteryassets.com** | Vercel | 24 Aug 2026 | **24 Aug 2027** | **$11.25** (.com) | lottery-assets |
| **rccgorunshi.org** | Vercel (transferred 5 Aug 2026; original buy 10 Sep 2023) | 10 Sep 2023 | **10 Sep 2028** | Transfer **$5.99** (not a 2026 full-year registration) | church-website-scaffold |

External DNS (`dns1/dns2.registrar-servers.com` = Namecheap). `renew: false` on Vercel (Vercel is not the registrar). Check Namecheap; this audit cannot see those invoices.

| Domain | Created on Vercel | Expires | Project |
|---|---|---|---|
| **equity2bitcoin.com** | 2 Aug 2026 | unknown here | equity2bitcoin |
| **brendanngwanforbi.com** | 17 Jul 2026 | unknown here | photo-album |

Moving a site to Cloudflare Pages does **not** require dropping the Vercel-registered domain. Either:

- keep the domain at Vercel and CNAME/ALIAS the apex to Pages, or  
- change nameservers to Cloudflare and leave registration at Vercel (or transfer out later).

Turn **auto-renew off** on any domain you do not intend to keep (Lottery / Book of Brendan are currently `noindex` / takedown-oriented). Leaving `renew: true` on a domain you no longer want is a silent $18–38 next August.

---

## 6. Ranked actions

Do 1–4 this week in the dashboard. Do not ask an agent to click them; this run is read-only on purpose.

### 1. Shorten retention — largest saving (~$14–42/mo)

**Team `newanforbis-projects` → Settings → Deployment Retention** (or Security → Retention):

- Canceled 1 day, Errored 1 day, Preview 7 days, Production 30 days.
- Apply to **all existing projects**.

Wait 48 hours and check Usage → Deployment Storage. Expect the GB-day total to fall as old previews drop. Production URLs stay up (alias exception).

### 2. Drop Speed Insights Plus — **$10/mo** guaranteed

**Project with the Plus badge (almost certainly Citeproof or the litigation portfolio) → Speed Insights → disable Plus.**

The npm packages `@vercel/speed-insights` / `@vercel/analytics` can stay; they degrade to the included quota (Hobby/Pro included events). Plus is **$10 per project per month plus $0.65 / 10k events**. Upcoming 12 Nov invoice is $20 + this $10.

Do **not** enable Web Analytics Plus ($10) or Observability Plus either.

### 3. Spend Management — surprise-charge fuse

**Team → Settings → Billing → Spend Management:**

- Amount: **$5** on-demand usage (on top of the $20 credit), so a bad month cannot exceed about **$25** before you are notified.
- Emails at 50% / 75% / 100%.
- **Pause production: off** until storage has drained and only the sites you want are unpaused. The September pause is why filings-linked hosts currently 402. After the fleet is trimmed, turning pause **on** at $5 is reasonable.

Also confirm: Build Machine **Basic**, On-Demand Concurrent Builds **off** (already in `internal/docs/VERCEL_DEPLOYS.md`).

### 4. Unpause only what must be live

Suggested live set, after (1)–(3):

| Keep / unpause | Why |
|---|---|
| `interactive-litigation-portfolio` | Filings and short-links. Already has ignore-build + `git.deploymentEnabled: false` + Cloudflare Pages parallel host. |
| `case-law-verification-engine` | citeproof.io; serverless. Disable Plus first. |
| `church-website-scaffold` | rccgorunshi.org is a real public site. |
| `book-of-brendan` | Only if you still want the blog up; it is currently noindex. |

Leave paused (then archive when storage is gone): `citizen-by-2027`, `t-minus-may-2026`, `nbnn-law-concept`, `newanforbi-pro-se`, `early-warning`, `pleading-paper-formatter` unless you use it weekly, `lottery-assets` / `equity2bitcoin` / `photo-album` / `ngwa-nforbi-law-firm` unless those products are actually launching.

Archiving a project in the dashboard is a **write**; this report does not do it.

### 5. Stop preview builds on any project you unpause — repo config

The litigation portfolio **already has** this. Do not hand-edit its `vercel.json` (`npm run sync:short-links` owns it). No config PR is required on this repo.

For **other** repos, a draft PR with **only** this is safe. It skips every non-`main` Git deploy; production on `main` still deploys. Do **not** set `"deploymentEnabled": false` on those repos unless you also add a deploy hook (the portfolio is the special case).

```json
{
  "$schema": "https://openapi.vercel.sh/vercel.json",
  "git": {
    "deploymentEnabled": {
      "main": true
    }
  }
}
```

Dashboard equivalent if you would rather not touch git: **Settings → Git → Ignored Build Step → Custom:**

```bash
if [ "$VERCEL_ENV" = "production" ]; then exit 1; else exit 0; fi
```

(Vercel: exit 0 = skip, exit 1 = build.)

Highest-value targets if you unpause them: `lottery-assets` (38 deploys, many preview), `ngwa-nforbi-law-firm` (39), `case-law-verification-engine` (40), `church-website-scaffold` (40), `nbnn-law-concept` (40). This agent did **not** open PRs on those repositories (separate git remotes; `git.deploymentEnabled: false` would freeze production without a hook).

On the portfolio, disconnect or ignore the **`documents`** branch so October ERROR/CANCELED rows stop. That branch does not contain `internal/scripts/vercel-ignore-build.sh`.

### 6. Move static sites to Cloudflare Pages

Already in-repo for the portfolio (`internal/docs/CLOUDFLARE_PAGES.md`). Same pattern for:

- `meditations-blog` (Eleventy, `_site`)
- `lottery-assets` (Vite, `dist`)
- `equity2bitcoin` (Vite, `dist`)
- `citizen-by-2027` (`frontend/dist`)
- `pleading-paper-formatter` (static)

Then CNAME the domain. Cancel Vercel Pro only after citeproof is either ported or accepted as the remaining $20 project.

GitHub Pages is a fallback for the tiny static repos only. Do not add Actions YAML to **this** repo.

### 7. Smaller build outputs (later)

- Keep PDFs on R2; never copy `internal/public/documents` into Vercel `dist/`.
- Photo-album: R2 or Cloudflare Images instead of git-hosted JPEGs in every deployment.
- Citeproof: stop tracing all of `tesseract.js-core` if a slimmer OCR path exists — Function Storage 1.45 GB is this project.

---

## 7. What this audit did not change

- No deployments deleted.
- No plan downgrade/upgrade.
- No Speed Insights / Analytics / Blob / Spend Management toggle.
- No DNS change.
- No merge. This file is the only new artifact.

---

## Sources

- Vercel MCP, 28 Oct 2026, team `team_Im0u0AeSdczjotkekBRw2SOI`.
- User billing snapshot, 28 Oct 2026 (Pro $20, Oct invoice $64.05 paid, Nov est. $30, usage $15.28, Deployment Storage 4.32 TB = $14.39).
- [Deployment Storage](https://vercel.com/docs/deployment-storage), [Deployment Retention](https://vercel.com/docs/deployment-retention), [Hobby](https://vercel.com/docs/plans/hobby), [Pro](https://vercel.com/docs/plans/pro), [Fair Use / commercial](https://vercel.com/docs/limits/fair-use-guidelines), changelog 9 Oct 2026 (storage billing for existing Pro teams).
- [Cloudflare Pages limits](https://developers.cloudflare.com/pages/platform/limits/).
- In-repo: `internal/docs/VERCEL_DEPLOYS.md`, `internal/docs/CLOUDFLARE_PAGES.md`, `vercel.json`, `internal/scripts/vercel-ignore-build.sh`.
