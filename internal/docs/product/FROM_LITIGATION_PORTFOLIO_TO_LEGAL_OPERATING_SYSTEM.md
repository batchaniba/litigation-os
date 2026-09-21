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
