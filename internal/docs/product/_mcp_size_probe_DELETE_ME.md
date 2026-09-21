# probe

This is a size probe for MCP create_or_update_file. DELETE ME.

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

## Section A

P3 is a private design-partner workspace. P4 is the same spine once someone pays. Neither is the next 30 days (P0). Do not stand up this stack to run an R2 coverage check.

### Stack summary (locked)

Locked choices from the maturity audit for the P3/P4 product path. The detailed tables below remain the working design notes; when they disagree with this summary, this summary wins.

One-liner: **Cloudflare (Pages + Workers + Queues + R2) · Postgres+RLS (Neon or Hyperdrive) · Clerk/WorkOS · Stripe · Sentry · typed AI review queue** — portfolio Git remains the gold-sample, not the multi-tenant store.

| Layer | Choice | Why |
| --- | --- | --- |
| Compute / API | Cloudflare Workers (+ Queues / Cron Triggers) | Already run doc-api, portfolio-gate, deploy cron |
| Object storage | R2 with per-tenant prefix `tenants/{id}/sha256/…` | Content-addressed model already trusted |
| Relational DB | Postgres with RLS — prefer **Neon** or **Hyperdrive → Postgres** (D1 only for publish cache, not multi-tenant SoR) | Orgs, matters, clocks, audit, conflicts |
| Auth | Clerk or WorkOS | Small employment firms; don't build auth |
| Private web | Vite/React → Cloudflare Pages | Phase 1 already pointed here |
| Public site | Same Pages project, publish projection only (#901 strip) | Separate routes/host if needed |
| Search | Postgres FTS + R2 text sidecars first; Vectorize/OpenSearch later only if needed | Don't buy Elastic on day one |
| Jobs | Cloudflare Queues + Consumers + DLQ | ingest, OCR, cite, docket sync |
| OCR / extract | Keep existing extract pipeline; paid OCR only for scans (Azure Document Intelligence or Google Document AI) | |
| Docket sync | CourtListener (keep) + manual upload | |
| AI | Typed ops over mutate-style API; Workers AI and/or one frontier API behind a review queue — **no product chat box** | |
| Email | Resend or Postmark | |
| Observability | Cloudflare Analytics + Sentry + structured Worker logs | |
| Billing (P4) | Stripe | |
| E&O / compliance | Counsel-drafted policies before any tenant PII | P4-00 gate |

**Portfolio-only forever:** live Newanforbi Git tree as reference; counsel dossiers; plaintiff-first stipulation locks; matter-specific pleading generators; public adversarial storytelling as *your* site, not the product default.

**Explicitly not needed for P3/P4:** Clio/MyCase dependency; Kubernetes / full AWS; replacing R2 with S3 "for enterprise"; a second monorepo rewrite before package extract works.

**Sequencing:** P3 packages + blank tenant on Postgres+R2 while portfolio stays on Git → P4-00 professional-responsibility layer → P4-01 orgs + RLS + per-tenant R2 + immutable audit → P4-02 pilots with 2–3 employment plaintiff firms.

## Padding to grow payload

AAA AAA AAA AAA AAA AAA AAA AAA AAA AAA AAA AAA AAA AAA AAA AAA AAA AAA AAA AAA
BBB BBB BBB BBB BBB BBB BBB BBB BBB BBB BBB BBB BBB BBB BBB BBB BBB BBB BBB BBB
CCC CCC CCC CCC CCC CCC CCC CCC CCC CCC CCC CCC CCC CCC CCC CCC CCC CCC CCC CCC
DDD DDD DDD DDD DDD DDD DDD DDD DDD DDD DDD DDD DDD DDD DDD DDD DDD DDD DDD DDD
EEE EEE EEE EEE EEE EEE EEE EEE EEE EEE EEE EEE EEE EEE EEE EEE EEE EEE EEE EEE
FFF FFF FFF FFF FFF FFF FFF FFF FFF FFF FFF FFF FFF FFF FFF FFF FFF FFF FFF FFF
GGG GGG GGG GGG GGG GGG GGG GGG GGG GGG GGG GGG GGG GGG GGG GGG GGG GGG GGG GGG
HHH HHH HHH HHH HHH HHH HHH HHH HHH HHH HHH HHH HHH HHH HHH HHH HHH HHH HHH HHH
III III III III III III III III III III III III III III III III III III III III
JJJ JJJ JJJ JJJ JJJ JJJ JJJ JJJ JJJ JJJ JJJ JJJ JJJ JJJ JJJ JJJ JJJ JJJ JJJ JJJ
