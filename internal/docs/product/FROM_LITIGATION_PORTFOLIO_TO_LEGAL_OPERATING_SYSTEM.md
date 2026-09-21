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
| Job transport | Cloudflare Queues | Dispatch, retry, batching, dead-letter for ingest and extraction | Partition by workload when backlogs appear |
| Durable orchestration | Cloudflare Workflows | Resumable ingest, reconcile, human-review checkpoints | Only for jobs that outlive a request |
| Heavy document compute | One Cloudflare Container running the existing Python tools | OCRmyPDF, PyMuPDF, `verify-citations.py`, packet processing | Scale that one worker; no microservice fleet |
| Authentication | Clerk Organizations | Invites, sessions, roles `owner` / `attorney` / `staff` / `readonly` | Clerk Enterprise SSO first; WorkOS only if a signed buyer needs an IdP Clerk cannot satisfy |
| Models | One API (OpenAI or Anthropic) behind typed operations | Extraction, classification, chronology. Output is a review card, never a silent write | Second provider only for a measured capability, reliability, or cost advantage |
| Agent surface | Existing `q.mjs` / `mutate.mjs` catalog over HTTP + MCP | Approve / revise / reject. Anonymous `tools/list` must not advertise writes | — |
| Search | Postgres full-text on extracted text; pgvector only if a measured retrieval gap appears | Matter and document retrieval | Dedicated search vendor only after measured Postgres limits |
| Email | Resend (pick one; do not also run Postmark) | Invites, job failures, deadline digest | — |
| Errors | Sentry (operator app + Worker) + Cloudflare logs | Frontend, API, job, ingest failures | Log warehouse when incident volume justifies it |
| Product analytics | None at P3 start | — | PostHog at P4 or when you cannot explain churn |
| Billing | None at P3 | — | Stripe when the first invoice exists |
| Secrets | 1Password (humans) + Wrangler secrets + Vercel / Neon env | Separate development, staging, and production. Never chat | — |
| Backups | Neon PITR + R2 versioning or object lock + quarterly restore drill | A backup that has not been restored is not a backup | Independent secondary copy before paying customers |
| Staging | Separate Worker + R2 + Neon branch + Clerk instance | Synthetic PDFs only until a DPA is signed | — |

```
Public (Vercel) ──publishMatter──► Worker + D1 + signed R2 reads
Operator (Vercel, Clerk session)
        │
        ▼
Workers API ──► Neon Postgres
        ├──► R2 (tenant prefix)
        ├──► Queue / Workflow ──► Container (OCR / cite / extract)
        │                              └── model API (optional)
        └──► MCP / typed ops ──► approval row ──► apply
```

GitHub remains code plus this reference portfolio. The gate Worker remains how `main` is protected.

### Product-system boundary

The reference portfolio remains in Git and continues using its established R2/D1 and agent workflows. Customer runtime state belongs in PostgreSQL and R2. Product extraction must not move live Newanforbi matter data into the new tenant model.

| Today | P3 fate |
| --- | --- |
| `matters/NN/*.json` | Schema inspiration; not imported into a shared tenant database |
| `clocks.json` status enum | Same enum in Postgres |
| `mutate.mjs` / `q.mjs` | API handlers; add idempotency key + approval id |
| `events.jsonl` | `case_events` table, still append-only |
| Agent-action log (P1.2) | `agent_actions` table (proposal, diff, validator, actor) |
| R2 `sha256/…` | Keep content addressing; prefix tenant |
| `verify-citations.py --check` | Same binary inside the container job |
| `portfolio-gate` | Unchanged mechanism; required on `main` |
| Versus header / `internal/docs/counsel/` | Portfolio site only |
| Pleading generators | Portfolio only |

A normal request should follow this path:

1. The browser calls the authenticated Workers API.
2. The API authorizes the user against organization and matter membership.
3. Transactional metadata is read or written in PostgreSQL.
4. Document bytes are written to R2 under immutable content-addressed keys with a tenant prefix.
5. Queue messages dispatch OCR, extraction, citation, or indexing work.
6. The document worker writes derived artifacts to R2 and structured results to PostgreSQL.
7. Consequential agent proposals remain pending until a human approves them through a typed operation.

Matter ACL: organization default plus per-matter grants. Ethical wall = explicit deny list, not a comment in `AGENTS.md`. Conflicts check is a blocking create-matter step with an attestation row (P3.0).

### Tenant isolation, audit, and conflicts

The table above names PostgreSQL as the tenant system of record. "Organization default plus per-matter grants" is a policy statement; the following is how it becomes testable.

**Row-level security, not application filtering.** Every tenant-scoped table carries `tenant_id` and enables RLS with `FORCE`, so the policy binds the table owner too:

```sql
alter table matters enable row level security;
alter table matters force row level security;

create policy tenant_isolation on matters
  using (tenant_id = current_setting('app.tenant_id')::uuid);

-- Ethical wall: per-matter grants inside one organization
create policy matter_acl on matters
  using (id in (select matter_id from matter_access
                where user_id = current_setting('app.user_id')::uuid));
```

`app.tenant_id` is set per connection from the verified session, never from a request parameter. The API connects as a non-superuser role.

**The isolation test is the deliverable, not the policy.** A suite that authenticates as organization A and attempts to read every tenant-scoped table as organization B, asserting zero rows, is what answers a buyer's security questionnaire. Ship it with the schema, not after it.

**Audit must be tamper-evident, not merely append-only.**

```sql
create table audit (
  id         bigserial primary key,
  tenant_id  uuid not null,
  actor      text not null,
  action     text not null,
  payload    jsonb not null,
  prev_hash  bytea,
  row_hash   bytea not null,      -- sha256(prev_hash || payload)
  at         timestamptz not null default now()
);
revoke update, delete on audit from app_role;
```

Append-only by permission, chained by hash. `events.jsonl` already has the first property; the chain adds "this record was not altered afterwards," which is the property that matters in a dispute. Add the chain to `mutate.mjs` under P1.2 — cheap now, expensive to backfill.

**Conflicts (P3.0) needs a mechanism, not just a checkpoint.** Tenant-scoped fuzzy match with `pg_trgm` across every party and adverse party in the organization, run before matter creation, with the result — hit or clean — written to `audit` as the attestation. A conflicts check that leaves no record is not a conflicts check.

### Model layer

The stack table leaves the provider open. The contract below is provider-neutral and stands on its own; the binding after it is the recommended default and is the open decision.

| Rule | Implementation |
| --- | --- |
| Typed operations, not a chatbot | Map the `q.mjs` / `mutate.mjs` catalog one-to-one onto tool definitions. No agent framework — that catalog is already the right abstraction |
| Schema-valid arguments | `strict: true` on every tool (`additionalProperties: false` plus `required`). The API-level twin of "validate before touching disk" |
| Extraction returns structure | Structured outputs (`output_config.format`), not prose parsing |
| Every proposal is reviewable | The model writes an approval row, never a table |

**Recommended binding — Anthropic.** Rates are per million tokens, current as of this writing; verify before budgeting.

| Use | Model | Rate |
| --- | --- | --- |
| Extraction, chronology, agent operations | `claude-opus-5` (1M context) | $5 in / $25 out |
| Bulk classification and triage only | `claude-haiku-4-5` (200K context) | $1 in / $5 out |

Three API features map onto commitments this document already makes:

- **Document citations.** `citations: {enabled: true}` on a document block returns `page_location` spans (`start_page_number` / `end_page_number`) for each cited passage — the document → page → assertion provenance chain this roadmap promises, available rather than built. Send PDFs where a page citation must be produced; use the cheaper `.txt` sidecars (99.3% coverage on stored documents) for search and summarization, accepting the loss of page anchors.
- **Batch API.** 50% cost, suited to the 484 UNVERIFIED authorities and any extraction backfill.
- **Prompt caching.** Cache matter context across operations on one matter; confirm with `usage.cache_read_input_tokens`.

Use adaptive thinking (`thinking: {type: "adaptive"}`); fixed `budget_tokens` is removed on current models and is rejected.

**Estimate, not a measurement:** a 20-page PDF is roughly 30K input tokens; extraction at ~2K output is about $0.20 per document on `claude-opus-5`, so 500 documents per month lands near $100, or half that through Batch. Model spend is not the binding constraint at pilot scale — Postgres, document compute, and counsel are. Record actual cost per ingested document from the first pilot rather than carrying this estimate forward.

### Two current defects to fix during migration, not after

Both are verified in the audit, and both become permanent if the migration copies the current shape.

**1. The object key is PDF-only.** The tenant prefix above (`t/{orgId}/sha256/…`) preserves the existing scheme, and that scheme hardcodes `.pdf` (`keyForSha256`), serves `content-type: application/pdf` unconditionally, and is fed by an upload path documented as "local PDFs → R2." The result is that 299 manifest entries — 141 `.txt`, 103 `.json`, 17 `.docx`, 35 images, 1 `.xlsx` — are 100% absent from R2. That is not a backlog; it is a structural impossibility, and it is why the P0.0 acceptance criterion had to be split by cause. The product key must carry the extension and the stored content type:

```
t/{orgId}/sha256/<first2>/<rest><ext>      bytes, with content-type metadata
t/{orgId}/text/<first2>/<rest>.txt         extracted text
```

Do this once, inside the tenant-prefix migration. Fixing it later means rewriting keys underneath customer data.

**2. Courts are a type, not data.** `CourtKey` in `internal/src/utils/deadlineMath/types.ts` is a closed union of exactly six courts — the six this portfolio litigates in — and the holiday tables are keyed to the same six. The deadline engine is the strongest transferable asset in the repository, yet adding a seventh California superior court is currently a TypeScript change rather than a configuration row. California has 58.

Add to the product-system boundary: `CourtKey` union → a `courts` table (jurisdiction, forum, holiday calendar, court-day rules), with `matter.court` a foreign key instead of free text. This is the smallest change that converts the deadline engine from a personal tool into a product primitive, and it belongs in P2 extraction, ahead of any second tenant.

**Scope note on docket sync.** Docket reconciliation does not generalize the way deadline computation does: CourtListener covers 7 of 41 matters and 0 of 19 state-court matters, because RECAP is PACER-derived and California superior courts are not in it. The rule-cited computation in `deadlineMath/` requires no external service and does transfer. For any state-court customer, product claims should rest on the computation and its provenance, not on docket synchronization.

### P4 — add only when money or a second org forces it

| Layer | Pick | Trigger |
| --- | --- | --- |
| Billing | Stripe + Clerk org metadata | First invoice |
| Product analytics | PostHog | Cannot explain why people stay or leave |
| SSO | Clerk Enterprise SSO (WorkOS only if Clerk cannot satisfy the buyer) | First firm with an IdP requirement |
| Legal hold / retention | Tenant settings in Postgres + R2 object lock | First employment-firm customer |
| Observability | Sentry performance + Cloudflare trace + queue-lag alerts | First missed ingest SLA |
| Security review | Independent pentest + dependency audit | Before a third paying org |
| Paper | Cyber liability, ToS, privacy notice, DPA, subprocessors list | Before any non-synthetic client file in production |
| Compliance | Start SOC 2; do not claim certified | Buyer questionnaire that needs a timeline |

### Environment strategy

Maintain three isolated environments:

- **Development:** synthetic fixtures, local tooling, disposable database, and non-production buckets.
- **Staging:** production-shaped infrastructure with synthetic or specifically approved test documents.
- **Production:** customer data, separately scoped credentials, backups, retention controls, and alerting. The live Newanforbi portfolio may keep using the current R2/D1 path until a deliberate cutover.

No production credential should be accepted by development code. Every schema migration and deployment must run against staging first.

### Backup and recovery standard

- PostgreSQL point-in-time recovery plus scheduled encrypted exports
- R2 lifecycle rules and an independent secondary copy for production documents
- Versioned infrastructure and migration definitions in Git
- Quarterly restore drills with measured recovery time and documented results
- Tenant export and deletion procedures tested before a multi-user pilot

### Acquisition sequence

**Not this stack (P0, already owned)**

- R2 coverage check, gate-runner determinism, required Check Run, then root-PDF removal
- Laptop `R2_*` and Wrangler secrets stay where they are. Do not buy Clerk or Neon to make `main` safe

**Private prototype (start of P3)**

- Keep Vercel and the existing Cloudflare deployment
- Add Neon, Clerk Organizations, one processing container, Sentry, Resend, and staging
- Use PostgreSQL search before buying a dedicated search product
- Use synthetic data until tenant isolation and restore tests pass

**Controlled pilot**

- Add queue-backed retries, tenant exports, retention controls, and an independent security review
- Pilot with two or three solo or small plaintiff-side firms — not SRLs, pending the P3.0 UPL memo
- Measure time-to-matter, successful ingestion, deadlines caught, recommendation acceptance, corrections, and weekly retention

**Commercial launch (P4)**

- Add Stripe, PostHog, customer-facing administration, formal support and incident processes, contractual documents, and enterprise identity only when demanded
- Introduce additional infrastructure from observed constraints rather than anticipated scale

### Planning range

For a small private pilot, budget approximately **$100–$400 per month** for base infrastructure (Neon + Clerk + Vercel + Sentry + Resend + Workers/R2/Queues + burst `standard-2` containers), excluding usage-variable AI, OCR, and document-processing compute. At 10–25 active users, use **$500–$2,000 per month** as an operating-planning range until measured workloads replace estimates.

These are planning bands, not procurement commitments. Record actual cost per ingested document, active matter, and retained user from the first pilot.

### Explicit deferrals

Do not introduce the following during the private-prototype phase:

- Kubernetes
- A microservice fleet
- A native mobile application
- A dedicated vector database
- Elasticsearch
- Multiple AI providers
- Enterprise SSO
- SOC 2 certification work
- Mass-market billing
- GitHub Actions in this repository
- Treating OpenAI (or any model vendor) as the product interface
- Parallel vendors serving the same infrastructure role
- Loading the Newanforbi matter graph into a shared tenant database

### P3 → P4 exit criteria

- Staging restore tested in the last 90 days
- Ingest is idempotent (same PDF does not double-catalog)
- Every write has an actor and an approval
- Public site cannot see operator routes
- One design partner completed a matter without this git repo
- Written UPL, conflicts, retention, incident, and subprocessors list

## Agent contribution protocol

Future agents building from this plan should:

1. Reference the roadmap item being implemented.
2. Create a scoped branch and reviewable PR.
3. Avoid combining litigation-data changes with product-infrastructure changes.
4. Identify canonical and derived files before editing.
5. Run the strongest available validation suite.
6. Record blockers without weakening invariants.
7. Preserve the existing public site and live litigation workflows unless the PR explicitly migrates them.
8. Update this roadmap only when a decision, priority, status, or acceptance criterion changes.

Items 2, 3, and 5 are currently unenforceable: `required_status_checks` is not enabled, required reviews are set to 0, and `enforce_admins` is false, so any actor holding a token — including an agent — can merge a failing branch to `main` unreviewed. After P0.1 they become enforced rather than advisory. Until then, treat them as honor-system rules and state in each PR body which validation actually ran.

## Non-goals for the next phase

- Rewriting the application from scratch
- Building every Clio feature
- Supporting every court and jurisdiction
- Launching mass-market billing
- Replacing attorney judgment with autonomous filing
- Adding more dashboard tabs without a validated user need
- Treating generic chat as the product interface
- Moving live portfolio data into an immature product database

## Near-term implementation order

Reordered by the audit. The governing principle: nothing is recoverable-loss-safe until step 1, and no later step sticks until step 3, because every improvement merges through a gate that currently cannot block anything.

1. **R2 coverage check** — make the 195 unbacked manifest entries visible and fail-closed (P0.0)
2. **Gate determinism** — conclude on check content, not container capacity (P0.1, P0.5)
3. **Enable required checks, one review, and admin enforcement** (P0.1)
4. **Push the missing bytes, then remove the root binaries** (P0.0, P0.4)
5. **Canonical/derived classification and a generator registry** (P0.2)
6. **System-health surface** — promoted, because a red gate survived 75 commits and a 195-file gap survived unnoticed (P1.1)
7. **Atomic document ingestion** (P0.3)
8. **Locking, idempotency, and the agent-action audit log on the existing mutation layer** (P1.2)
9. **Public/private UI boundary** (UI direction)
10. **Narrow shared primitives** — not the pleading generators (P1.3)
11. **Blank-workspace product prototype** (P2)
12. **Professional-responsibility layer, then a controlled multi-user pilot** (P3.0, P3)

## Decision standard

A proposed feature should advance at least one of these outcomes:

- Reduces procedural risk
- Reduces the risk of unrecoverable loss
- Improves data integrity
- Saves operator time
- Increases auditability
- Makes agent actions safer
- Generalizes a proven workflow
- Improves onboarding or repeated use

If it does none of these, it should not outrank reliability work.

## End state

The target is not merely a more polished portfolio.

The target is a litigation operating system in which documents, deadlines, evidence, claims, authorities, people, and agent actions form one source-grounded, auditable graph—and in which the human operator retains control over every consequential action.
