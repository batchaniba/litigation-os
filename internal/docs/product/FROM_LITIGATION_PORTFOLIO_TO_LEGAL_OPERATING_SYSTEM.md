# From Litigation Portfolio to Legal Operating System

**Status:** Proposed roadmap  
**Scope:** Software-engineering maturity, product readiness, and UI evolution  
**Audience:** Repository agents, maintainers, product designers, and future contributors  
**Source of truth:** This document records the current product direction. Implementation belongs in separate, reviewable PRs.

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
- 164 operational script files
- 54 package commands
- CourtListener synchronization and citation infrastructure
- R2/D1 document infrastructure and an MCP document API
- Typed repository mutations, validation gates, document sidecars, deadline clocks, evidence stores, and cross-matter intelligence
- No enforced GitHub Actions status checks on pull requests

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

**P0.1 Required CI**

Create GitHub Actions that run on every PR:

- Lint
- Typecheck
- Unit tests
- Schema validation
- Generated-file drift checks
- Registry and manifest checks
- Document-sidecar checks
- Citation known-bad gate
- Golden tests

Require successful checks before merge.

**Acceptance:** A PR cannot merge when canonical data, generated artifacts, tests, or document inventories disagree.

**P0.2 Canonical-data boundary**

Classify every repository data file as canonical, derived, analysis, runbook, or artifact. Document which command owns each derived file.

**Acceptance:** Every generated file has one deterministic generator and can be deleted and reproduced from canonical state.

**P0.3 Atomic document ingestion**

Replace multi-step document cataloging with one idempotent operation.

**Acceptance:** Re-running the same ingest creates no duplicates; partial failure leaves no catalog, storage, sidecar, or matter-membership drift.

**P0.4 Repository hygiene**

- Remove root-level PDF clutter
- Finish the Git-to-object-store boundary
- Prevent new binaries from landing outside approved locations
- Define retention and archival rules

**Acceptance:** A clean clone contains code, metadata, and intentionally retained artifacts without an uncontrolled root document dump.

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

Move repository mutations behind a reusable service boundary with validation, locking, idempotency keys, and append-only audit records.

**P1.3 Shared primitives**

Replace repeated matter-specific scripts with reusable filing, service, deadline, document, citation, and evidence operations.

**P1.4 Recovery and observability**

Add structured logs, retryable background jobs, backup/restore procedures, failure alerts, and migration checks.

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

**Acceptance:** A new blank workspace can create a matter, ingest documents, extract deadlines, and preserve an audit trail without importing the Newanforbi portfolio.

### P3 — Multi-user pilot

Build the minimum secure product layer:

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

1. Required GitHub Actions and branch protections
2. Canonical/derived file classification
3. Atomic document ingestion
4. Root binary cleanup and storage boundary
5. System-health dashboard
6. Transactional mutations and audit log
7. Shared domain packages
8. Public/private UI separation
9. Blank-workspace product prototype
10. Controlled multi-user pilot

## Decision standard

A proposed feature should advance at least one of these outcomes:

- Reduces procedural risk
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
