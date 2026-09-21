# From Litigation Portfolio to Legal Operating System

**Status:** Proposed roadmap  
**Scope:** Software-engineering maturity, product readiness, and UI evolution  
**Audience:** Repository agents, maintainers, product designers, and future contributors  
**Source of truth:** This document records the current product direction. Implementation belongs in separate, reviewable PRs.
**Audit basis:** [`ENGINEERING_MATURITY_AUDIT_2026-09-21.md`](ENGINEERING_MATURITY_AUDIT_2026-09-21.md) — a read-only architecture and maturity audit against `main` @ `f4716cd`. Corrections it produced are applied below and itemized in that document's "Roadmap delta" section.

## Executive thesis

The Interactive Litigation Portfolio is already a sophisticated single-operator litigation system. It is not yet a dependable multi-user legal product.

Capability is ahead of reliability.

The next phase is not primarily about adding features. It is about hardening the existing machine, separating public presentation from private operations, extracting reusable domain primitives, and exposing the repository's agent capabilities through a controlled product interface.

The repository should remain the operational laboratory and reference implementation. The commercial product should be extracted from its repeatable operating model rather than treating the repository itself as the customer database.

## Current baseline

As of September 21, 2026:

- 41 structured matters, all using the split-matter architecture
- 1,629 manifest-tracked files
- Approximately 1.04 GB of tracked document inventory
- 1,190 canonical document-registry paths
- 222 operational script files (88 Node `.mjs` + 134 Python `.py`; 41 shared `lib/` modules)
- 54 package commands
- CourtListener synchronization and citation infrastructure
- R2/D1 document infrastructure and an MCP document API
- Typed repository mutations, validation gates, document sidecars, deadline clocks, evidence stores, and cross-matter intelligence
- A remote `portfolio-gate` Check Run already exists (`workers/portfolio-gate/`: GitHub App + Cloudflare Containers, locked check name, 25-minute fail-closed timeout, own test suite)
- Branch protection is configured on `main`, but `required_status_checks` is **not enabled**, `required_approving_review_count` is **0**, and `enforce_admins` is **false** — so the check is advisory and merges are unblocked
- No GitHub Actions, by standing policy (`AGENTS.md`: do not add `.github/workflows/`)

## Maturity assessment

| Dimension | Current | Target |
| --- | ---: | ---: |
| Domain model | 8.5/10 | 9.5/10 |
| Automation | 8.5/10 | 9.5/10 |
| AI-agent design | 9/10 | 9.5/10 |
| Testing and validation | 7/10 | 9/10 |
| CI enforcement | 3/10 | 9/10 |
| Data integrity | 6.5/10 | 9/10 |
| Maintainability | 6/10 | 8.5/10 |
| Deployment and operations | 6.5/10 | 9/10 |
| Security and permissions | 5/10 | 9/10 |
| Product UX | 6/10 | 8.5/10 |
| Multi-user readiness | 2/10 | 8/10 |

The system is approximately a Level 3 operational platform in capability, Level 2 in reliability, and Level 1 as a multi-user product.

The audit regrades three rows downward and adds one dimension this table omits:

| Dimension | This table | Audit | Why |
| --- | ---: | ---: | --- |
| CI enforcement | 3/10 | **2/10** | The machinery exists and is switched off, which is worse than absent — it produces the appearance of a control |
| Data integrity | 6.5/10 | **5/10** | 195 manifest entries assert files that cannot be retrieved |
| Recovery and backups | — | **3.5/10** | Not scored here. 195 entries plus 27 root files have no second copy, and no restore drill has been run |

## Product position

Do not build another general-purpose Clio clone.

The strongest position is:

> An AI-native litigation command system that turns case documents into a structured, auditable matter graph.

The initial customer wedge should be:

- Solo plaintiff lawyers
- Small civil-rights and employment firms
- Legal clinics with document-heavy portfolios
- High-capability self-represented litigants

The product's repeatable jobs are:

- Create a structured matter from uploaded documents and docket records
- Extract and reconcile procedural deadlines
- Connect evidence to allegations, claims, parties, and filings
- Verify citations and build research queues
- Detect missing documents, contradictory facts, and stale procedural data
- Preserve source provenance and an auditable activity history
- Allow typed AI operations subject to human review

## Architecture principles

1. **Canonical records first.** Matter data and document metadata are authoritative. README tables, indexes, summaries, registries, and dashboards are derived.
2. **Typed mutations only.** Agents should use validated operations instead of editing generated JSON directly.
3. **Transactional ingestion.** Hashing, deduplication, storage, sidecar creation, registration, matter attachment, indexing, and availability checks succeed or fail together.
4. **Git is not the binary store.** Git should retain code, structured metadata, text extraction, and small artifacts. Object storage should own PDFs and other large binaries.
5. **Review before consequence.** Agent-proposed changes must show sources, files affected, validation results, and a reviewable diff.
6. **Public and private surfaces are separate.** Public storytelling and private litigation operations must not compete inside one interface.
7. **Every important operation is observable.** Failures, drift, stale data, unavailable documents, and synchronization status must be visible.
8. **The current portfolio remains protected.** Product extraction must not destabilize live litigation operations.

## UI direction

### Public portfolio

The public surface should communicate professional identity and selected results:

- Selected matters and filings
- Outcomes and published opinions
- Portfolio statistics
- Professional branding
- Carefully selected opposing-counsel context
- Navy, gold, off-white, crest, and formal legal typography

### Private workspace

A correction from the audit on the premise here. The concern that the UI mixes public storytelling, private operations, and adversarial presentation is only partly right. `routes.ts` exposes nine nav items, and **Deadlines, Documents, Evidence, and Research are not among them** — even though `CalendarTab`, `DeadlineCalculatorTab`, `ServiceTracker`, `CoverageTower`, `NextActionsPanel`, `CrossMatterTab`, `GlobalSearchDialog`, and `SavedViews` are all built. There is also no authentication anywhere in the SPA, so everything shipped is public by construction.

So private operations are not competing with the public surface so much as absent from it: the operator workspace has been built as a CLI (`npm run q`, `npm run next`, `npm run mcp`) and needs a UI. That is a cheaper problem than untangling three audiences, and it means the work below is mostly exposure rather than invention.

The private product surface should prioritize action:

- Home
- Matters
- Deadlines
- Documents
- Evidence
- Research
- People and organizations
- Agents
- System health

The top bar should provide global search, add-document, create-matter, notifications, and workspace controls.

The private dashboard should lead with:

1. Action queue
2. Upcoming and overdue deadlines
3. Data-integrity exceptions
4. Active matters
5. Recent activity
6. Portfolio analytics

### Matter workspace

Every matter should expose:

- Overview
- Docket
- Deadlines
- Documents
- Evidence
- Claims
- Parties and counsel
- Research
- Strategy
- Activity log

The matter header should show only caption, case number, court, judge, phase, next deadline, last verification, and primary action.

### AI operations interface

Expose typed operations rather than a generic chat box:

- Ingest documents
- Reconcile docket
- Extract deadlines
- Verify citations
- Build evidence map
- Compare pleadings
- Audit service
- Generate matter summary
- Identify contradictions
- Prepare research queue

Every operation should return a review card containing:

- Proposed changes
- Sources and provenance
- Confidence or unresolved questions
- Files and records affected
- Validation results
- Approve, revise, or reject controls

## Priority roadmap

### P0 — Reliability foundation

**P0.0 Document-store recoverability** *(added by audit — precedes everything)*

195 manifest entries (138.4 MB) have no retrievable bytes in R2, and 27 of the 41 root PDFs have no bytes in R2 by content hash. `internal/public/documents/**` is gitignored, so for those files the only copy in version control is the root copy, and the only other copy is the laptop. Nothing detects this.

- Add a coverage check: every manifest entry must resolve to bytes in R2
- Use ranged `GET` — the Worker answers `405` to `HEAD`, which is indistinguishable from absent
- Run `npm run sync:manifest` and `npm run documents:push`, then confirm full coverage
- Only then remove the root binaries (see P0.4)

**Acceptance:** zero manifest entries without bytes in R2, and the check fails closed when that regresses.

**P0.1 Enforce the gate that already exists**

Do **not** create GitHub Actions. `AGENTS.md` forbids `.github/workflows/`, the spending limit refuses every job, and the remote check is already built: `workers/portfolio-gate/` runs the same steps as the `pre-push` hook through a GitHub App and Cloudflare Containers, under the locked Check Run name `portfolio-gate`.

The gap is enforcement and determinism, not capability:

- The runner fails on capacity rather than on check content — `max_instances = 3` produces `Maximum number of running container instances exceeded`. Raise or queue against that limit, add retry with backoff, and distinguish infrastructure failure from check failure
- Then enable `required_status_checks` for `portfolio-gate`, set `required_approving_review_count` to 1, and enable `enforce_admins`

**Acceptance:** no PR merges to `main` while the Check Run is failing or absent — including for admins and for agents holding a token.

**P0.2 Canonical-data boundary**

Classify every repository data file as canonical, derived, analysis, runbook, or artifact. Document which command owns each derived file.

**Acceptance:** Every generated file has one deterministic generator and can be deleted and reproduced from canonical state.

**P0.3 Atomic document ingestion**

Replace multi-step document cataloging with one idempotent operation.

**Acceptance:** Re-running the same ingest creates no duplicates; partial failure leaves no catalog, storage, sidecar, or matter-membership drift.

**P0.4 Repository hygiene**

- Remove root-level PDF clutter — **but only after P0.0 confirms the bytes exist in R2.** 27 of the 41 root files currently have no second copy anywhere; deleting them first destroys the only tracked copy of live Matter 05 discovery responses and demurrer briefing
- Finish the Git-to-object-store boundary
- Prevent new binaries from landing outside approved locations — the blanket `.pdf`/`.docx` bypass in `checkRepoRootIsClean()` is closed, and `internal/src/data/index/root-quarantine.json` is the explicit allowlist that must drain to empty
- Define retention and archival rules

**Acceptance:** A clean clone contains code, metadata, and intentionally retained artifacts without an uncontrolled root document dump, and the quarantine ledger is empty.

**P0.5 Environment-independent gate results** *(added by audit)*

The same tree currently yields 2,832 `validate-portfolio` failures without a hydrated document store and 334 with one, and the unit suite reports 52 unhandled errors and "no tests" on a Node major below `engines.node`. A gate whose verdict depends on local disk or runtime cannot be required, which makes this a prerequisite for P0.1.

- Default `validate-portfolio` to manifest mode; make disk mode an explicit opt-in
- Report which mode produced the verdict
- Keep the Node-major preflight guard

**Acceptance:** identical verdict from the container, a clean sandbox, and the laptop on the same commit.

### P1 — Operational hardening

**P1.1 System-health dashboard**

Display:

- Catalog drift
- Worker and object-store availability
- Failed document extraction
- Missing or empty sidecars
- Unresolved citations
- Stale matter summaries
- Deadline contradictions
- Referenced but unavailable documents
- Last successful synchronization

**P1.2 Transactional mutation service**

Note what already exists: `internal/scripts/lib/mutate.mjs` provides eight validated operations (`recordTimelineEvent`, `retireUpcomingEvent`, `setNextClock`, `updateMatterIdentity`, `catalogDocument`, `scaffoldMatter`, `splitMatter`) that validate before touching disk and land changes on the working tree for review. `q.mjs` exposes 19 ops. This item is therefore not "build a mutation layer" but:

- Add locking and idempotency keys to the existing ops
- Add an append-only agent-action log — proposal, sources, diff, validation result, approver — kept distinct from `events.jsonl`, which records case events rather than agent activity

**P1.3 Shared primitives**

Narrow this item. Do **not** deduplicate the pleading generators: `matter37-home-depot-complaint.py` and `matter38-swift-complaint.py` are both exactly 1,179 lines and 1,170 of those lines differ, because they are pleading prose rather than copy-paste. Shared mechanism already exists and is widely imported (`signature_stamp` in 69 generators, `pleading_paper` in 46, `pdf_packet` in 24).

Extract reusable service, deadline, document, citation, and evidence helpers only.

**P1.4 Observability**

Add structured logs, retryable background jobs, failure alerts, and migration checks.

Backup and restore has moved to **P0.0** — it is an open critical risk, not P1 hardening. A documented and executed restore drill belongs there.

**P1.0 Deploy-configuration truth** *(added by audit)*

`workers/doc-api/wrangler.toml` commits `database_id = "REPLACE_WITH_D1_DATABASE_ID"` while the deployed Worker serves D1-backed reads, so the committed configuration cannot reproduce the running system. Establish one source of truth for deploy configuration and document any value that is intentionally set out of band.

### P2 — Product extraction

Extract reusable packages without moving live litigation data:

- Domain model
- Document ingestion
- Deadline engine
- Citation engine
- Agent operations
- Audit log
- Search and retrieval
- UI component system

**P2-E Court model de-typing** *(added by audit)* — `CourtKey` is a closed union of six courts and the holiday tables are keyed to the same six, so adding a court is a type change rather than a configuration row. Convert it to a `courts` table and make `matter.court` a foreign key instead of free text. This is the smallest change that makes the deadline engine — the strongest transferable asset here — usable by a second tenant, and it precedes the blank-workspace prototype. See "Two current defects to fix during migration, not after."

**Acceptance:** A new blank workspace can create a matter, ingest documents, extract deadlines, and preserve an audit trail without importing the Newanforbi portfolio — and a court the portfolio does not litigate in can be added without a code change.

### P3 — Multi-user pilot

**P3.0 Professional-responsibility layer** *(added by audit — precedes any pilot)*

The technical list below is close to complete. The professional list is missing entirely, and no amount of infrastructure substitutes for it:

- Conflicts checking before a matter is created, with an attestation record
- Ethical walls enforced by permissions, not convention
- A reviewed position on the unauthorized-practice-of-law boundary — this is the reason self-represented litigants are a hazardous first segment rather than an obvious one
- Legal hold, retention, and deletion controls per tenant
- A documented malpractice / errors-and-omissions posture

Also note a capability that should **not** generalize: opposing-counsel dossiers under `internal/docs/counsel/` are legitimate research for one pro-se litigant, but as a multi-tenant feature they become cross-firm intelligence aggregation, carrying privacy, reputational, and possibly ethical exposure. Keep them portfolio-specific.

Then build the minimum secure product layer:

- Authentication
- Organizations and workspaces
- Matter-level permissions
- Tenant-isolated database and object storage
- Encryption and secrets management
- Immutable audit logs
- Retention and deletion controls
- Background-job retries
- Schema migrations
- Error reporting
- Human approval boundaries

Pilot with two or three serious users.

Measure:

- Time to create a matter
- Deadlines caught
- Classification accuracy
- Documents successfully ingested
- Agent recommendations accepted
- Corrections required
- Weekly retained use

## Product data architecture

The product should use a database and object storage rather than Git as the customer runtime:

- PostgreSQL for normalized matter records, permissions, events, deadlines, document metadata, and audit state
- Object storage for original documents and generated artifacts
- Background queues for extraction, OCR, citation work, synchronization, and agent jobs
- Search index for document text and matter retrieval
- Typed API or operation layer for all writes
- Git retained for code, schemas, migrations, policy definitions, fixtures, and the reference portfolio

## Recommended product stack

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

Decision rules:

- Cloudflare is the edge, object store, jobs, and merge gate. It is not the system of record for tenants.
- Git stays the Newanforbi laboratory. Customer data never lands in this repository.
- Writes go through typed operations and human approval. The product interface is not a chatbot.
- No `.github/workflows/` in this repository. Remote CI remains `workers/portfolio-gate/` under the locked Check Run name `portfolio-gate`.
- Counsel dossiers, the public versus header, and the pleading generators stay portfolio-only.

### P3 — pilot stack (2–3 users; synthetic documents, then one firm)

Use Cloudflare as the infrastructure spine, not as the entire application platform. Preserve the current Vercel deployment during the pilot; migration is justified only when operating simplicity or cost clearly improves.

| Layer | P3 pick | Responsibility | Scale trigger |
| --- | --- | --- | --- |
| Public site | Existing React/Vite app on Vercel | Current portfolio origin; no Pages migration | Move only if consolidating onto Cloudflare materially reduces complexity |
| Operator app | Same Vite/React codebase, separate origin + Clerk session (`app.` vs public host) | Authenticated workspace; split shells, not a rewrite | — |
| Edge API | Cloudflare Workers on the `litigation-doc-api` lineage | Authorization, signed R2 URLs, webhooks, rate limits, MCP gateway | Split services only when deploy or reliability boundaries demand it |
| Merge / CI | Existing `ilp-portfolio-gate` Containers + required Check Run `portfolio-gate` | Same steps as `pre-push`. Do **not** add GitHub Actions | Raise container concurrency when PRs queue, not by adding Actions |
| Document storage | R2 buckets `litigation-documents-prod` and `…-staging`; tenant prefix `t/{orgId}/sha256/…` | Originals, OCR text, sidecars, exports. Upload-only, never deletes | Second backup target before external customer data |
| Product database | Neon Postgres (RDS Postgres acceptable later) | Orgs, members, matters, permissions, clocks, evidence links, document metadata, approvals, audit. PITR on | Read replicas and pooling when connections or isolation demand it |
| Public / lightweight index | Cloudflare D1 (keep) | Current publish projection (`publishMatter`) and public document API | Never the sole source of truth for a permissions-heavy product |
