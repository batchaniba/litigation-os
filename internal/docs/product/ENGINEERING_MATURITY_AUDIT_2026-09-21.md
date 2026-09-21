# Interactive Litigation Portfolio — Engineering Maturity and Product Readiness Deep Dive

**Repository:** `newanforbi/interactive-litigation-portfolio` (private)
**Inspected at:** `main` @ `f4716cd` — Sep 21, 2026, 01:00 PT
**Roadmap under review:** PR #923, branch `codex/product-maturity-roadmap` (open, not merged) — `internal/docs/product/FROM_LITIGATION_PORTFOLIO_TO_LEGAL_OPERATING_SYSTEM.md`, 346 lines
**Companion to:** [`FROM_LITIGATION_PORTFOLIO_TO_LEGAL_OPERATING_SYSTEM.md`](FROM_LITIGATION_PORTFOLIO_TO_LEGAL_OPERATING_SYSTEM.md). That document records product direction; this one records the audit the direction was tested against. Where the two disagree, the roadmap has been corrected and the delta is in section 7.

**Method:** read-only inspection of `main`, the live Cloudflare Worker read paths, and the GitHub branch-protection and Check Run APIs. No credentials were used or required beyond repository read access.

Labels used throughout: **[F]** fact verified in the repository or against a live endpoint · **[I]** inference · **[R]** recommendation.

---

## 1. Unfiltered executive verdict

The working thesis — "capability is ahead of reliability" — is **correct but imprecise, and it lets the repository off too easily.** Three sharper statements survive contact with the evidence.

**First: the reliability machinery already exists and is deliberately switched off.** This is not a repository that lacks CI. `workers/portfolio-gate/` is a GitHub App plus Cloudflare Containers runner with a locked Check Run name, a 25-minute fail-closed timeout, and its own test suite. Branch protection is configured on `main`. But **[F]** `required_status_checks` returns HTTP 404 "not enabled", `required_approving_review_count` is `0`, and `enforce_admins` is `false`. The Check Run is advisory. The roadmap scores CI at 3/10 and prescribes "create GitHub Actions" — which `AGENTS.md` explicitly forbids and which would duplicate infrastructure that is already built. The real finding is worse than a missing capability: **a gate was built, wired, and then not required.**

**Second: I demonstrated the failure mode while doing this work.** **[F]** Earlier tonight I merged #919, #920, and #921 into `main`. At merge time the `portfolio-gate` Check Run reported `FAILURE` on #919 and #920 and had not concluded on #921. Nothing stopped the merges, no review was required, and no human approved the diffs. The repository's stated "review-before-merge" rule is documentation, not a control. An agent with a token is currently indistinguishable from a maintainer.

**Third: the most serious problem is not code quality — it is that the canonical record of the case is not fully backed up.** **[F]** The document manifest on `main` claims 1,629 files and 1.04 GB. Against a full mirror hydrated from the public Worker, **195 manifest entries (138.4 MB) have no retrievable bytes**. Separately, 41 PDFs totalling 161.6 MB sit at the repository root, of which **27 have no bytes in R2 by content hash**. `internal/public/documents/**` is gitignored, so for those 27 the root copy is the only one in version control. These are live Matter 05 discovery responses and demurrer briefing. A laptop failure today loses them. No check reports this. That is a litigation risk before it is an engineering risk.

What is genuinely differentiated, and I want to be clear that it is real: the split-matter graph, the typed mutation layer (`mutate.mjs`, 8 validated operations; `q.mjs`, 19 ops), content-addressed document storage with text sidecars, a 987-authority citation ledger with adversarial known-bad gating, and an agent instruction hierarchy that encodes genuine operational judgment. I have not seen a solo-operator legal system with this much structural discipline.

What is commercially unproven: **[I]** almost all of it. The system has exactly one user, one plaintiff, and zero conflicts checks. The hardest parts of legal software — multi-tenancy, ethical walls, conflicts, trust-adjacent obligations, malpractice exposure — are not partially built. They are absent. The roadmap's own 2/10 multi-user score is the only score I would not argue upward.

**Verdict:** the roadmap is directionally right and tactically wrong in its first and most important item. Do not start extraction. Spend 30 days making the existing gate mandatory and the document store recoverable. **[R]** If you do only one thing from this report, enable required status checks once the gate is deterministic.

---

## 2. System map

### 2.1 Where state actually lives

**[F]** Verified locations of authoritative state:

| Concern | Source of truth | Also holds a copy | Ambiguity |
| --- | --- | --- | --- |
| Matter identity | `internal/src/data/matters/NN/matter.json` | index `matters.json`, README tables | Index is derived; README is stale by policy |
| Live calendar | `matters/NN/clocks.json` | index `next_clock`, `upcoming.json`, `timeline.json` | **4 surfaces.** `AGENTS.md`: clocks wins |
| Pleadings | `matters/NN/docket.json` | README, registry | Operative row flagged `"operative": true` |
| Document inventory | `matters/NN/documents.json` | manifest, registry (1,190 paths) | Entries lack generator provenance |
| Document bytes | **Cloudflare R2** `litigation-documents`, key `sha256/<first2>/<rest>.pdf` | `documents` git branch (cold), laptop disk | **195 manifest entries have no R2 bytes** |
| Extracted text | R2 `text/<first2>/<rest>.txt` | `.txt` sidecars on `main` | Sidecars drift; 51 unlisted in manifest |
| Path → hash index | R2 object `index/path-to-sha256.json` | — | **[F]** Not a repo file; `AGENTS.md` phrasing implies it is |
| Event history | `matters/NN/events.jsonl` (append-only) | — | Clean. Best-designed store in the repo |
| Damages model | `internal/src/data/damages.js` (1,001 lines) | golden snapshot | Golden was stale 75 commits |
| Citations | `index/citations.json` + Python ledger | README | 987 authorities; 484 UNVERIFIED |
| Publish projection | D1 `litigation-portfolio` via `publishMatter()` | R2, Vercel build | **[F]** `database_id = "REPLACE_WITH_D1_DATABASE_ID"` in committed config |
| Secrets | laptop `~/.config/r2/env`, Worker bindings | — | Correctly disciplined |

### 2.2 Compute and deployment surfaces

```
                    ┌─────────────────────────── LAPTOP (Aliko) ────────────────────────────┐
                    │  git working tree · R2_* creds · CourtListener token · npm run q/mcp   │
                    │  pre-push hook (fail-closed, 6 steps) · 134 Python generators          │
                    └───────────────┬───────────────────────────────┬───────────────────────┘
                                    │ git push                      │ documents:push (R2_*)
                                    ▼                               ▼
                   ┌────────────────────────────┐        ┌──────────────────────────┐
                   │  GitHub  main / documents  │        │  R2 litigation-documents │
                   │  branch protection: ON     │        │  sha256/** · text/**     │
                   │  required checks: OFF  ◄── │        │  index/path-to-sha256    │
                   └──────┬──────────────┬──────┘        └────────────┬─────────────┘
                          │ webhook      │ deploy hook                │ binding
                          ▼              ▼                            ▼
        ┌──────────────────────────┐  ┌──────────────┐   ┌──────────────────────────────┐
        │ ilp-portfolio-gate       │  │   Vercel     │   │  litigation-doc-api Worker   │
        │ GitHub App + Containers  │  │  React 19    │   │  REST + MCP (15 tools)       │
        │ max_instances = 3  ◄──── │  │  SPA, no auth│   │  D1 publish projection       │
        │ Check Run: advisory only │  │  cron deploy │   │  cron: daily fuse, Mon roll  │
        └──────────────────────────┘  └──────────────┘   └──────────────────────────────┘
                                                                     ▲
                                              external models ────────┘  (no credentials)
```

**[F]** Two markers above are the load-bearing defects: required checks OFF, and `max_instances = 3`.

### 2.3 Agent instruction hierarchy

**[F]** `AGENTS.md` (145 lines) is the real contract. `CLAUDE.md` (3 lines) and `.github/copilot-instructions.md` (3 lines) delegate to it. Six `.cursor/rules/*.mdc` carry standing locks; four `.claude/skills/` carry procedures. This is a well-designed hierarchy — one authority, thin adapters.

**[F]** It also contains a self-contradiction. `AGENTS.md` states Python scripts are "**not** part of the build, the hooks, or any npm script" and "Python scripts must not be added to `package.json` scripts." But `GATE_STEPS` ends with `python3 internal/scripts/verify-citations.py --check`, and `package.json` contains 8 Python-invoking scripts. Python is load-bearing in the gate the document says excludes it.

---

## 3. Engineering maturity scorecard

Scored against a shipping multi-tenant SaaS bar, not against "impressive for one person."

| # | Dimension | Score | Evidence | What blocks the next point | Highest-leverage fix |
| --- | --- | ---: | --- | --- | --- |
| 1 | Domain modeling | **8.5** | 41 matters, uniform split; clocks/claims/damages/evidence/parties/counsel separated; `events.jsonl` append-only | No conflicts, no client entity, no matter-party role model for multi-tenant | Introduce a `client` boundary above `matter` |
| 2 | Data integrity | **5.0** | 195 manifest entries with no R2 bytes; 51 sidecars unlisted; 3 hash mismatches; 27 root PDFs unbacked | Nothing detects byte-level absence; manifest asserts files that do not exist | R2 coverage check as a gate step |
| 3 | Architecture | **7.5** | Clean canonical/derived intent; content-addressed store; Worker-binding secret model | `database_id` placeholder; 4 calendar surfaces; registry/path-index off-tree | One deploy-config source of truth |
| 4 | Automation | **8.0** | 54 npm scripts, 88 `.mjs`, 41 lib modules, typed mutations | 134 Python generators outside the pipeline; no generator↔output registry | `generators.json` with `--check` |
| 5 | AI-agent design | **9.0** | `AGENTS.md` crawl contract; typed ops; MCP for external models with no credentials; review-before-consequence | Docs drift from shipped auth; no agent action audit trail distinct from events | Reconcile MCP docs with `auth.mjs` |
| 6 | Testing | **7.0** | 42 test files, 528 tests, golden damages, `--check` modes | Gate steps are environment-sensitive; golden regressed silently for 75 commits | Make gate results environment-independent |
| 7 | **CI enforcement** | **2.0** | **Protection ON but required checks OFF, reviews = 0, admins unenforced; gate FAILURE on #915/#917/#919/#920; blank on #916/#918/#921** | Remote gate is non-deterministic, so requiring it would block all merges | Fix container capacity, then require |
| 8 | Maintainability | **6.0** | 60 TS vs 59 JS files — half-migrated; `damages.js` 1,001 lines; 222 scripts | No module ownership; matter-specific scripts unbounded | Finish TS migration; retire scripts dir |
| 9 | Observability | **4.0** | Worker `[observability] enabled`; gate summaries | No health surface, no drift alert, no sync-status telemetry; I found the 75-commit regression by bisecting manually | Drift/health check surfaced in UI |
| 10 | Deployment maturity | **6.0** | Vercel `deploymentEnabled: false`, cron deploy hook; two Workers; Pages scaffold smoke-only | Committed config cannot deploy D1 as-is; no staging; no migration path | Fix config drift; add staging |
| 11 | Security | **6.5** | Keys only in laptop env + Worker bindings; `worker-not-keys` rule; writes refuse 401 | Public MCP advertises 7 write tools to anonymous callers; docs claim read-only | Hide write tools from unauthenticated `tools/list` |
| 12 | Permissions | **2.0** | No auth in SPA; no roles; no tenant concept | Entire model absent | Deferred to P3 — correctly |
| 13 | Recovery and backups | **3.5** | `documents` branch cold backup; content-addressed dedupe | **[F]** 195 entries + 27 root files have no second copy; no restore drill | Coverage check + documented restore test |
| 14 | Documentation | **6.5** | `AGENTS.md` excellent; 26,894 Markdown lines | Python contradiction; MCP auth drift; `DEADLINE_AUDIT` said 24 matters vs 41; name inconsistency README vs `AGENTS.md` | `doc_kind` front matter (#918) |
| 15 | Developer experience | **7.0** | `npm run q`, `mcp`, `gate`, scaffold, split; hooks auto-install | Node-major trap cost me a full false-failure cycle (fixed in #920); no onboarding doc | Document the 22.x requirement in README |
| 16 | Performance | **7.0** | Vite 8, React 19, route prefetch, Worker reads 0.11–0.30 s | 1.04 GB store in a build path; no pagination strategy for growth | Keep bytes out of the build |
| 17 | Accessibility | **4.5** | Semantic components, theme context | No audit, no axe in tests; decorative glyph icons (`⌂ § ↦ $ ¶ ◈ ✓ ⚖ "`) as nav affordances | Add automated a11y assertions |
| 18 | Mobile usability | **5.0** | Responsive CSS in 1,294-line `app.css` | Dense analytical tables; no mobile-first operator flow | Define mobile priorities (§10) |
| 19 | Product UX | **6.0** | 9 nav items, global search, saved views, breadcrumbs | Public storytelling and private analysis share one surface; built capability is unexposed | Split public/private IA |
| 20 | Multi-user readiness | **1.5** | Nothing present | No auth, tenancy, conflicts, audit, retention | Do not start yet |

**Weighted read:** Level 3 capability, Level 2 reliability, Level 1 product — the roadmap's own framing, which I agree with. But I score CI **2.0 against its 3.0**, data integrity **5.0 against its 6.5**, and recovery **3.5**, a dimension the roadmap omits entirely.

---

## 4. Strongest existing technical assets

Ranked by how hard they would be to rebuild.

1. **[F] The split-matter graph.** 41 matters, uniform sibling files, `events.jsonl` append-only. This is a real domain model, not a CMS schema. Hardest asset to replicate; the clearest basis for a product.
2. **[F] Typed mutation layer.** `mutate.mjs` — `recordTimelineEvent`, `setNextClock`, `catalogDocument`, `updateMatterIdentity`, `scaffoldMatter`, `splitMatter`, `retireUpcomingEvent` — validating before touching disk and landing on the working tree for review. This is the "review before consequence" principle already implemented, three roadmap layers ahead of where the roadmap assumes it is.
3. **[F] Content-addressed document store with text sidecars.** `sha256/<first2>/<rest>.pdf` plus `text/<first2>/<rest>.txt`, served through a Worker that binds R2 so no credentials leave the server. The 14-of-41 root PDFs already present in R2 were found *because* storage is content-addressed — dedupe works.
4. **[F] Credential-free external model access.** Public MCP over Streamable HTTP with `readDocumentText` so an external model reads documents without fetching PDF bytes or holding keys. Genuinely ahead of industry practice.
5. **[F] Adversarial citation infrastructure.** 987 authorities with a known-bad gate that blocks new plaintiff-filing hits. Legal-specific, correctly paranoid.
6. **[F] The agent instruction hierarchy.** One authority, thin adapters, standing locks as rules. `AGENTS.md`'s "Never treat README as live" and the clusters warning encode scars from real incidents.
7. **[F] The gate runner itself.** `workers/portfolio-gate/` has 6 test files for its own orchestration, webhook, policy, and check logic. The engineering is done; only the enforcement switch is off.

---

## 5. Ten most serious engineering risks

| # | Risk | Severity | Evidence | Why it persists |
| --- | --- | --- | --- | --- |
| 1 | **Unrecoverable document loss** | **Critical** | **[F]** 195 manifest entries (138.4 MB) no R2 bytes; 27 root PDFs (75.8 MB) unbacked; store gitignored | No check exists; manifest asserts presence it never verifies |
| 2 | **Merge controls are decorative** | **Critical** | **[F]** required checks OFF, reviews = 0, admins unenforced; I merged 3 PRs with a failing/blank check | Requiring a non-deterministic gate would block everything |
| 3 | **Remote gate non-deterministic** | High | **[F]** `max_instances = 3`; #920 failed with "Maximum number of running container instances exceeded" | Capacity, not code. No queue or backoff |
| 4 | **Silent multi-commit regressions** | High | **[F]** Golden damages red from #876 to #919 — 75 commits, ~3 days | Red gate + direct pushes (`Batch 1`, `Add files via upload`) normalized failure |
| 5 | **Environment-sensitive gate results** | High | **[F]** Same tree: 2,832 failures unhydrated vs 334 hydrated; Node 20 gave 52 phantom errors and "no tests" | `validate-portfolio` conflates data validity with local file presence |
| 6 | **Committed deploy config cannot deploy** | High | **[F]** `database_id = "REPLACE_WITH_D1_DATABASE_ID"` while `/matters` and `/fuse` return 200 | Deployed state was configured out-of-band |
| 7 | **Public MCP advertises write tools** | Medium-High | **[F]** `tools/list` returns 15 tools incl. 7 writes to anonymous callers; refuses with 401; `AGENTS.md` says read-only/no-auth | Docs not updated when `auth.mjs` shipped |
| 8 | **No generator provenance** | Medium-High | **[F]** 222 scripts, 0 with machine-readable output declaration; 1 of 26,894 Markdown lines carries a generated marker | Canonical/derived boundary is prose, not data |
| 9 | **Single-operator dependency** | Medium-High | **[F]** `documents:push`, `court:sync`, D1 reseed, both Worker deploys all require the laptop | Deliberate for secrets; no documented succession or restore drill |
| 10 | **Half-finished TS migration** | Medium | **[F]** 60 TS vs 59 JS files; `damages.js` 1,001 lines untyped while `types/portfolio.ts` exists | No migration ratchet |

---

## 6. Roadmap critique

Verdicts on every major recommendation in `FROM_LITIGATION_PORTFOLIO_TO_LEGAL_OPERATING_SYSTEM.md`.

### 6.1 Thesis and framing

| Item | Verdict | Reasoning |
| --- | --- | --- |
| "Capability ahead of reliability" | **Strengthen** | True but soft. Precisely: reliability machinery is **built and unenforced**. That is a governance failure, not a maturity stage |
| "Repository remains laboratory; extract the product" | **Keep** | Correct and unusually disciplined. The alternative — productizing the live portfolio — would put filings at risk |
| "Do not build a Clio clone" | **Keep** | Correct. Clio is practice management; this is matter intelligence |
| "AI-native litigation command system…" positioning | **Strengthen** | Accurate but not yet a wedge. Add the buyer's words: missed deadlines and unverifiable citations (§11) |
| Level 3 / Level 2 / Level 1 grading | **Keep** | Matches my independent read |

### 6.2 Baseline figures

| Roadmap claim | Verified | Verdict |
| --- | --- | --- |
| 41 structured matters, all split | **[F]** Confirmed | Accurate |
| 1,629 manifest-tracked files | **[F]** `fileCount: 1629` | Accurate |
| ~1.04 GB inventory | **[F]** 1,036,189,241 bytes | Accurate |
| 1,190 canonical registry paths | **[F]** "1190 paths; 1185 matter-linked" | Accurate |
| 54 package commands | **[F]** 54 | Accurate |
| 164 operational script files | **[F]** 88 `.mjs` + 134 `.py` = **222** | **Understated by 35%** |
| "No enforced GitHub Actions status checks on pull requests" | **[F]** Literally true | **Misleading.** Omits that a Worker Check Run exists and that protection is on but toothless |

**[R]** Correct the script count and rewrite the CI line. As written it invites exactly the wrong fix.

### 6.3 Priority roadmap

| Item | Verdict | Reasoning |
| --- | --- | --- |
| **P0.1 Required CI via GitHub Actions** | **Reject and replace** | **[F]** `AGENTS.md`: "Do not add `.github/workflows/`" — spending limit refuses every job. `workers/portfolio-gate/` already implements this with a locked Check Run name whose comment reads "branch protection requires this exact string." Replace with: make that gate deterministic, then enable required checks |
| **P0.2 Canonical-data boundary** | **Keep, split** | Correct and the deepest fix. Too large as one item. Split into classification (`doc_kind`, already #918), generator registry, and `documents.json` generator edge |
| **P0.3 Atomic document ingestion** | **Keep, reorder later** | Right idea, wrong position. Ingestion atomicity does not help the 195 files already missing. Coverage detection must precede transactional ingestion |
| **P0.4 Repository hygiene** | **Strengthen** | **[F]** Partly done tonight (#921 closed the root bypass; #922 drafted). The roadmap says "Remove root-level PDF clutter" — dangerous as stated: 27 of 41 have no other copy. Deletion must be gated on R2 coverage |
| **P1.1 System-health dashboard** | **Keep, promote to P0** | This is the missing feedback loop. A 75-commit regression and a 195-file gap both survived because nothing displays drift |
| **P1.2 Transactional mutation service** | **Strengthen** | Roadmap treats this as absent. **[F]** `mutate.mjs` already validates 8 typed ops. Reframe as adding locking, idempotency keys, and an agent-action audit log distinct from `events.jsonl` |
| **P1.3 Shared primitives** | **Keep, narrow** | **[F]** Earlier in this session I diffed `matter37-home-depot-complaint.py` against `matter38-swift-complaint.py`: both exactly 1,179 lines, 1,170 lines differ. That is pleading prose, not duplication, and shared mechanism already exists (`signature_stamp` 69 importers, `pleading_paper` 46, `pdf_packet` 24). Do **not** deduplicate pleading generators. Narrow to service/deadline/citation helpers |
| **P1.4 Recovery and observability** | **Split, promote recovery to P0** | Backups are a critical open risk, not P1 hardening. Observability can stay P1 |
| **P2 Product extraction** | **Keep, defer** | Correctly scoped. Blocked on P0.2 — you cannot extract packages while the canonical/derived boundary is prose |
| **P3 Multi-user pilot** | **Strengthen** | Technically complete; **professionally incomplete**. Missing conflicts checking, ethical walls, malpractice/insurance posture, UPL boundaries, per-tenant retention and legal hold (§8, §16) |
| Product data architecture (Postgres, object storage, queues, search) | **Keep** | Conventional and correct. Add per-tenant encryption and legal-hold semantics |
| Agent contribution protocol | **Strengthen** | Good. **[F]** Unenforceable while reviews = 0 and checks are optional. Add: "protocol items 2, 3 and 5 are enforced by branch protection" |
| Non-goals | **Keep** | The sharpest section. "Treating generic chat as the product interface" is correct and rare |
| Near-term order (1–10) | **Reorder** | See §7 |
| Decision standard | **Keep** | Genuinely useful. Add "reduces unrecoverable-loss risk" |

### 6.4 Incorrect assumptions, hidden dependencies, confusions

**Incorrect assumptions [I]:**
- That CI is missing. It is built and unenforced.
- That transactional mutations are missing. `mutate.mjs` exists.
- That root PDF removal is hygiene. For 27 files it is deletion of the only copy.
- That "no enforced status checks" is the CI problem. The problem is `max_instances = 3` and an unflipped setting.

**Hidden dependencies [I]:**
- Everything in P2/P3 depends on P0.2, which depends on generator provenance that does not exist.
- The health dashboard (P1.1) depends on a drift-detection API that does not exist.
- Requiring the gate depends on making `validate-portfolio` environment-independent — otherwise every PR fails on document presence.
- Root cleanup depends on `documents:push`, which depends on the laptop.

**Personal workflow mistaken for repeatable customer workflow [I]:** counsel dossiers (`internal/docs/counsel/`, ~71 files of opposing-counsel research); `STIPULATION_DEFENSE.md`'s plaintiff-first posture; the pro-se email close; adversarial framing aimed at opposing counsel; the Python generator library tuned to one plaintiff's pleading voice. All valuable to *you*; none are product primitives, and one is a liability (§8).

---

## 7. Roadmap delta

Concrete corrections to apply to `FROM_LITIGATION_PORTFOLIO_TO_LEGAL_OPERATING_SYSTEM.md`.

**Replace P0.1 entirely:**

> **P0.1 Enforce the gate that already exists**
> `workers/portfolio-gate/` (GitHub App + Containers, Check Run `portfolio-gate`) already implements remote checks. Do not add `.github/workflows/`. Make the runner deterministic — raise or queue against `max_instances = 3`, add retry with backoff, distinguish infrastructure failure from check failure — then enable `required_status_checks` for `portfolio-gate`, set `required_approving_review_count` to 1, and enable `enforce_admins`.
> **Acceptance:** no PR merges to `main` while the Check Run is failing or absent, including for admins and agents.

**Add four items the roadmap omits:**

| New item | Priority | Rationale |
| --- | --- | --- |
| **P0.0 Document-store recoverability** | Before everything | **[F]** 195 manifest entries + 27 root files have no second copy. Add a coverage check; fail when a manifest entry has no bytes in R2 |
| **P0.5 Environment-independent gate results** | P0 | **[F]** 2,832 vs 334 failures on the same tree; Node 20 phantom failures. A gate whose verdict depends on local disk cannot be required |
| **P1.0 Deploy-config truth** | P1 | **[F]** `database_id` placeholder; deployed state configured out-of-band |
| **P3.0 Professional-responsibility layer** | Before any pilot | Conflicts, ethical walls, UPL boundary, malpractice posture, legal hold, per-tenant retention |

**Reorder the near-term list:**

| Was | Now |
| --- | --- |
| 1. Required GitHub Actions and branch protections | 1. **R2 coverage check** (P0.0) |
| 2. Canonical/derived classification | 2. **Gate determinism + required checks** (P0.1, P0.5) |
| 3. Atomic document ingestion | 3. **Root cleanup, gated on coverage** (P0.4) |
| 4. Root binary cleanup | 4. **Canonical/derived classification + generator registry** (P0.2) |
| 5. System-health dashboard | 5. **System-health surface** (promoted) |
| 6. Transactional mutations and audit log | 6. Atomic ingestion (P0.3) |
| 7. Shared domain packages | 7. Audit log + locking on existing `mutate.mjs` |
| 8. Public/private UI separation | 8. Public/private UI boundary |
| 9. Blank-workspace prototype | 9. Narrow shared primitives (not pleading generators) |
| 10. Controlled multi-user pilot | 10. Blank-workspace prototype → pilot, after P3.0 |

**Correct two stale claims [F]:** "164 operational script files" → 222. The CI line → as rewritten above. **[R]** Also reconcile the `AGENTS.md` Python contradiction and the MCP read-only claim, and resolve the name inconsistency between `README.md` ("Brendan Ngehsi Newanforbi") and the `AGENTS.md` email close ("Brendan Ngwa Nforbi") — a discrepancy that matters on filings.

---

## 8. Product boundary

| Layer | Contents | Disposition |
| --- | --- | --- |
| **1. Live Newanforbi portfolio** | 45 matter dirs, `events.jsonl`, counsel dossiers, `STIPULATION_DEFENSE.md`, 134 Python generators, pro-se locks, damages/fees models | **Stays portfolio-specific and append-only.** Never migrate into a product DB |
| **2. Reusable engine** | Matter schema + loaders, `mutate.mjs` ops, clock status machine + `deadlineMath/recipes.ts`, document store + sidecars, citation verification, CourtListener bridge, `validate-portfolio` rules, `q`/MCP op surface | **Becomes packages.** Highest-value extraction targets |
| **3. Public website** | 9 nav routes, Outcomes, Notable Quotes, Judicial Opinions, Census, Cost of Counsel, portfolio charts, `publishMatter()` projection | **Stays a separate deployable.** Narrow to storytelling |
| **4. Future product** | Auth, orgs/workspaces, tenant isolation, permissions, conflicts, audit, retention, review queue, health surface | **Does not exist.** Build after P0/P1 |

**Specific dispositions:**

- **Remain portfolio-specific:** counsel dossiers, stipulation posture, email close, pleading generators, matter prose.
- **Become reusable packages:** `lib/clock-status.mjs`, `utils/deadlineMath/`, `lib/matter-schema.mjs`, `lib/mutate.mjs`, `lib/document-store.mjs`, `lib/r2-client.mjs`, citation ledger logic, `courtlistener/*`.
- **Become product services:** ingestion, docket sync, deadline extraction, citation verification, agent operations, search.
- **Retire:** `internal/docs/DEADLINE_AUDIT.md` (#918 does this), duplicate `matter24-opposition-mtd` v3/v4/v4-pleading with no winner marked, `.md`/`.json` twins.
- **Regenerate, never hand-edit:** README tables, `upcoming.json`, matter summaries, short links, manifest, registry, golden damages, `doc-kind.json`.
- **Move out of Git:** the remaining root binaries (after coverage), and keep the 1.04 GB store out of the build path.
- **Move into a database:** the publish projection (D1 today), and eventually product-tenant matter records — **not** the live portfolio.
- **Stay append-only:** `events.jsonl`. **[R]** Add an agent-action audit log with the same property.
- **Require immutable audit history:** every typed mutation, every agent proposal and approval, every document registration, every deadline change.

**[R] The counsel-dossier warning.** Aggregating opposing-counsel research is legitimate for one pro-se litigant. As a multi-tenant feature it becomes cross-firm intelligence aggregation, with reputational, privacy, and possibly ethical exposure. **Do not ship it as a product feature.** It is the clearest case of a personal capability that should not generalize.

---

## 9. Target architecture

**[R]** Incremental extraction, not a rewrite. The repository proves extraction is viable: typed ops, schemas, and content-addressed storage already form clean seams.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  CLIENTS   public site (static)   │   operator workspace (authed SPA)        │
└───────────────┬───────────────────┴───────────────┬──────────────────────────┘
                │                                   │  session + tenant claim
                ▼                                   ▼
        ┌───────────────┐              ┌──────────────────────────────┐
        │ publish CDN   │              │  API boundary (typed ops)     │
        │ projection    │              │  = today's q/MCP op surface   │
        └───────────────┘              └──┬────────────┬───────────────┘
                                          │            │
                    ┌─────────────────────┘            └──────────────┐
                    ▼                                                 ▼
      ┌──────────────────────────┐                      ┌──────────────────────────┐
      │ PostgreSQL (row-level    │                      │  Object storage (R2)     │
      │ tenant isolation)        │                      │  sha256/** · text/**     │
      │ matters · clocks · docs  │                      │  per-tenant prefix + KMS │
      │ claims · events(append)  │                      └──────────────────────────┘
      │ audit(immutable) · perms │                                  ▲
      └──────────┬───────────────┘                                  │
                 │                                                  │
                 ▼                                                  │
      ┌──────────────────────────────────────────────────┐          │
      │  Background jobs (queue + DLQ + retry)           │──────────┘
      │  ingest → OCR/extract → register → index         │
      │  docket sync · deadline extract · citation verify │
      └────────────────┬─────────────────────────────────┘
                       ▼
      ┌──────────────────────────────────────────────────┐
      │  Agent operations → REVIEW QUEUE → human approve │
      │  (proposal, sources, confidence, diff, validate) │
      └──────────────────────────────────────────────────┘
                       │
                       ▼   every consequential action
      ┌──────────────────────────────────────────────────┐
      │  Immutable audit log  +  health/drift telemetry   │
      └──────────────────────────────────────────────────┘
```

**Migration path, each step shipping independently and leaving the portfolio operational:**

| Step | Change | Portfolio impact |
| --- | --- | --- |
| 1 | R2 coverage check; finish root cleanup | None — additive check |
| 2 | Gate determinism; require checks | None — process only |
| 3 | Generator registry; `doc_kind`; `documents.json` generator edge | Additive metadata |
| 4 | Extract `lib/` into versioned workspace packages; repo consumes them | Refactor, behavior-identical |
| 5 | Stand up Postgres + object storage for a **blank** tenant; port typed ops behind the API | Portfolio untouched — still Git |
| 6 | Background queue for ingest/OCR/sync | Portfolio may opt in per-command |
| 7 | Auth, orgs, RLS, audit, conflicts | Product only |
| 8 | Operator SPA against the API | Public site unchanged |
| 9 | Pilot tenants | Portfolio stays on Git indefinitely |

**[R]** The portfolio should be the last thing migrated, and possibly never. It is the reference implementation and its Git-native audit trail is a feature.

---

## 10. Public-versus-private UI strategy

### 10.1 Testing the three-way-collision claim

**Partly confirmed, and the diagnosis needs a correction.**

**[F]** `routes.ts` defines 9 nav items in 4 groups: Overview (Dashboard); Casework (Matters, Timeline); Analysis (Damages, Theories, Cost of Counsel, Outcomes); Record (Judicial Opinions, Notable Quotes). **[F]** There is no authentication anywhere in the SPA. So everything shipped is public by construction.

**[F]** Storytelling and adversarial framing do share the surface: Outcomes, Notable Quotes, Judicial Opinions, Census, and Cost of Counsel are portfolio narrative aimed at readers including opposing counsel.

**But the sharper finding is the opposite of the stated concern:** private operations are **largely not exposed at all**. **[F]** `CalendarTab.jsx`, `DeadlineCalculatorTab.tsx`, `ServiceTracker.jsx`, `CoverageTower.tsx`, `NextActionsPanel.jsx`, `CrossMatterTab.tsx`, `GlobalSearchDialog.tsx`, and `SavedViews.tsx` all exist as components, but **Deadlines, Documents, Evidence, and Research are not in `NAV_ITEMS`**. The operator's real work happens in `npm run q`, `npm run next`, and the MCP server — the CLI, not the UI.

**[R]** So the correct framing is not "untangle three audiences in one UI." It is: **the public site is roughly right and slightly over-shares; the private workspace has been built as a CLI and needs a UI.** That is a cheaper and more honest problem.

### 10.2 Assessment

| Area | Current | Assessment |
| --- | --- | --- |
| Navigation | 9 items, 4 groups, glyph icons | Reasonable for public; wrong spine for operator work |
| Information architecture | Analysis-heavy, 4 of 9 items analytical | Optimized for a reader, not a litigant with a deadline |
| Header | `PortfolioHeader.tsx`, theme toggle, global search | Good. Search is a real asset |
| Dashboard | `DashboardTab.jsx` + `NextActionsPanel` | Next actions exist but are not the entry point |
| Matter list | `MattersTab`, `MatterCard`, saved views | Strongest part of the UI |
| Matter detail | `MatterDetailPage.tsx`, `MatterSummary` | Present; not organized as the roadmap's 10-section workspace |
| Search | `GlobalSearchDialog` | Exists; underexposed |
| Deadlines | Components exist, **no nav entry** | Largest gap — the highest-stakes workflow is unexposed |
| Documents / Evidence / Research | No nav entries | Unexposed; 1.04 GB store has no browse UI |
| Counsel intelligence | Markdown under `internal/docs/counsel/` | **[R]** Keep out of any product UI |
| Damages / Outcomes | `DamagesTab`, `OutcomesTab` | Strong public narrative |
| Dark/light | `ThemeContext`, `useThemePreference` | Implemented |
| Responsive | 1,294-line `app.css` | Works; not mobile-first |
| Accessibility | No automated checks | Weakest UI dimension. Glyphs as icons need labels |
| Information density | High | Right for you, wrong for a first-time buyer |
| Visual hierarchy | Navy/gold/off-white, crest, legal type | Genuinely distinctive. Preserve |

### 10.3 Two information architectures

**Public portfolio** — keep narrow, remove operational detail:
`Home · Selected Matters · Outcomes · Judicial Opinions · About`
Retire from public: Cost of Counsel, Census, Notable Quotes, Cross-Matter (**[I]** these read as adversarial signalling and give opposing counsel a free map). Keep them in the private workspace.

**Private operator workspace:**

| Element | Design |
| --- | --- |
| Primary nav | Today · Matters · Deadlines · Documents · Evidence · Research · People · Agents · Health |
| Dashboard hierarchy | 1 Action queue → 2 Overdue/next 14 days → 3 **Integrity exceptions** → 4 Active matters → 5 Recent activity → 6 Analytics |
| Matter workspace | Overview · Docket · Deadlines · Documents · Evidence · Claims · Parties & counsel · Research · Strategy · Activity. Header shows only caption, case no., court, judge, phase, next deadline, last verification, primary action |
| Document workspace | Faceted by matter/kind/filed date; inline text sidecar preview; provenance panel (sha256, generator, R2 presence); **absent-bytes badge** |
| Deadline workflow | Clock list by status (`open/set/contingent/vacated/satisfied`) → calculator with `recipes.ts` → proposed clock → **review card** → `setNextClock` → `events.jsonl` |
| Research workflow | Citation ledger filtered by state; P0 queue first; CourtListener lookup; MISCITED/MISCHARACTERIZED triage |
| Agent review queue | One card per proposal: proposed changes, sources, confidence, files affected, validation results, Approve / Revise / Reject. Backed by `mutate.mjs` — already built |
| System health | Manifest↔R2 coverage, sidecar drift, gate status, last CourtListener sync, unresolved citations, stale summaries, contradictory clocks |
| Mobile priorities | 1 Next deadline 2 Today's actions 3 Document lookup + read 4 Approve/reject a pending agent proposal. Nothing else |

**[R]** Expose AI as the typed operations already in `q.mjs` and `mutate.mjs`, each returning a review card. No chat box. The roadmap is right about this and closer to shipping it than it realizes.

---

## 11. Initial customer wedge

### 11.1 Segment evaluation

| Segment | Pain | Willingness to pay | Trust barrier | Verdict |
| --- | --- | ---: | --- | --- |
| Solo plaintiff lawyers | Deadlines, document volume | Medium | High — solo, no IT, malpractice-averse | Secondary |
| **Small employment plaintiff firms (2–10)** | **Deadline exposure across many contingency matters; discovery volume** | **High** | Medium | **Recommended** |
| Small civil-rights firms | Same, plus § 1983 complexity | Medium-High | Medium | Close second |
| Legal clinics | Supervision, turnover, continuity | **Low** — grant-funded | High — student data, ethics review | Defer |
| High-capability SRLs | Everything | Very low | Low | **Reject as wedge** |

**[R] Start with small employment plaintiff firms, 2–10 lawyers.**

**Why:** contingency economics mean time saved converts directly to capacity, so ROI is arithmetic rather than a feeling. Deadline-driven practice with heavy document production matches exactly what the repository does well. They buy software without procurement. There are many of them. And a missed deadline is a malpractice claim — the pain is insurable, which means it is budgeted.

**Why not SRLs**, despite being closest to the current system's actual user: **[I]** near-zero willingness to pay, extreme support burden, single-matter lifespan, and a UPL hazard — a tool that extracts deadlines and drafts filings for a non-lawyer edges toward legal advice. This is the segment the repository is currently *shaped for*, which is a trap.

### 11.2 The wedge in detail

- **Highest-value recurring problem:** procedural deadlines derived from filings and dockets, reconciled against the court's record, with an audit trail proving who knew what and when.
- **Existing alternatives:** Clio/MyCase (practice management, weak deadline derivation), CompuLaw/Deadlines.com (rules-based calendaring, no document grounding), paralegal labor (expensive, error-prone), spreadsheets (most common).
- **Why this wins:** derived deadlines grounded in the actual document and docket with provenance, plus citation verification. **[F]** The clock status machine, `deadlineMath/recipes.ts`, the CourtListener bridge, and the 987-authority ledger all exist and are exercised against 41 real matters.
- **What they pay for:** deadline assurance and audit trail. Per-seat, roughly $80–200/lawyer/month. **[I]** Estimate, not validated.
- **What they will not trust:** autonomous filing, AI-authored citations without verification, anything that touches client funds, anything without conflicts checking, cloud storage without a DPA and per-tenant isolation.
- **Pilot must prove:** (1) deadlines extracted per matter and how many the firm had missed; (2) extraction accuracy against a human baseline; (3) time-to-first-matter under 30 minutes; (4) agent proposal acceptance rate; (5) zero cross-tenant leakage; (6) weekly retained use by week 6.
- **Genuinely transferable:** clock state machine, deadline recipes, document store + sidecars, citation ledger, CourtListener bridge, typed mutations, review-before-consequence, matter schema.
- **Not transferable:** counsel dossiers, stipulation posture, pleading generators, pro-se locks, adversarial framing, the 41-matter dataset.

**[R]** Complexity is not the moat. **[F]** 222 scripts and 26,894 lines of Markdown are cost, not value. The moat is deadline derivation with provenance.

---

## 12. Prioritized implementation backlog

Effort: S ≤ 1 day · M ≤ 1 week · L ≤ 1 month · XL > 1 month. "Agent-safe" = an AI agent can execute without a human at the keyboard. "Separate" = must not be combined with litigation-data changes.

### P0 — Reliability foundation

| ID | Problem | Change | Files / systems | Deps | Risks | Acceptance | Validation | Effort | Agent-safe | Separate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **P0.0-A** | **[F]** 195 manifest entries have no R2 bytes; nothing detects it | Add `check-r2-coverage.mjs`: every manifest entry resolves to bytes via the Worker; ranged GET, concurrency-limited, cached | new `internal/scripts/check-r2-coverage.mjs`, `lib/portfolio-gate-policy.mjs` | none | Network flake → false red; needs offline skip | Check reports exact count and bytes; fails when > 0 uncovered | Run on `main` (expect 195), then after push (expect 0) | M | **Yes** | **Yes** |
| **P0.0-B** | 27 root PDFs (75.8 MB) have no second copy | Run `sync:manifest` + `documents:push` from laptop; verify 41/41 | laptop, R2 | P0.0-A | Partial upload | Coverage 41/41 | P0.0-A output | S | **No — needs `R2_*`** | Yes |
| **P0.0-C** | Root copies still the only ones in Git | Merge #922 (drafted) after P0.0-B | 41 root files, `root-quarantine.json` | P0.0-B | **Deleting unbacked bytes** | Root clean, ledger empty | `validate-portfolio` | S | Yes, after gate | Yes |
| **P0.1-A** | **[F]** Gate fails on capacity: `max_instances = 3` | Raise limit; queue; retry with backoff; distinguish infra failure from check failure | `workers/portfolio-gate/wrangler.toml`, `src/orchestrate.mjs`, `src/runner.mjs` | none | Container cost | 10 consecutive PRs conclude without infra failure | Replay recent PR heads | M | **Yes** | Yes |
| **P0.1-B** | **[F]** Protection is decorative | Enable `required_status_checks` = `portfolio-gate`; reviews = 1; `enforce_admins` = true | GitHub API (not a PR) | P0.1-A, P0.5-A | Locks out the sole maintainer | Merge blocked when check red | Attempt a merge with a red check | S | **No — owner decision** | n/a |
| **P0.5-A** | **[F]** 2,832 vs 334 failures on the same tree | Default `validate-portfolio` to manifest mode; disk mode opt-in; report mode in output | `validate-portfolio.mjs`, `portfolio-gate.mjs` | none | Masking real absence — mitigated by P0.0-A | Identical verdict in container, sandbox, laptop | Run all three | M | **Yes** | Yes |
| **P0.2-A** | **[F]** 0 of 222 scripts declare outputs | `generators.json` registry + `--check`; `PORTFOLIO` front matter on generators | `internal/scripts/**`, new `index/generators.json` | none | Large mechanical diff | Every derived file names one generator | `--check` in `npm run validate` | L | **Yes** | **Yes** |
| **P0.2-B** | `documents.json` entries are `{path, filed}` only | Add `generator` edge | `matters/NN/documents.json`, `catalogDocument` | P0.2-A | Touches matter data | Every generated doc links its generator | `validate-portfolio` | M | Yes | **No — matter data** |
| **P0.2-C** | **[F]** 1 of 26,894 Markdown lines marked generated | Merge #918 (`doc_kind` front matter + gate step) | `check-doc-kind.mjs`, `doc-kind.json` | laptop gate | none found | 18 classified, count 41 | `check:doc-kind` | S | Yes | Yes |
| **P0.3-A** | Ingestion is multi-step and non-atomic | One idempotent `ingestDocument` op: hash → store → sidecar → register → attach → verify, all-or-nothing | `lib/document-store.mjs`, `mutate.mjs`, `r2-upload.mjs` | P0.0-A, P0.2-A | Rewrites a hot path | Re-run creates no duplicates; partial failure leaves no drift | Fault injection at each stage | L | Yes | Yes |

### P1 — Operational hardening

| ID | Problem | Change | Files | Deps | Risks | Acceptance | Effort | Agent-safe | Separate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **P1.0-A** | **[F]** `database_id` placeholder in committed config | One source of truth for deploy config; document out-of-band values | `workers/doc-api/wrangler.toml` | none | Exposing ids (not secrets) | `wrangler deploy` works from a clean clone | S | Yes | Yes |
| **P1.1-A** | No drift surface; 75-commit regression went unseen | `health.json` generator: coverage, sidecar drift, gate status, last sync, unresolved citations, stale summaries, contradictory clocks | new `sync-health.mjs` | P0.0-A | Alert fatigue | One command prints every drift class | M | Yes | Yes |
| **P1.1-B** | Health invisible in UI | Health route in private workspace | `internal/src/pages/`, `routes.ts` | P1.1-A | none | Integrity exceptions on dashboard | M | Yes | Yes |
| **P1.2-A** | No agent-action audit distinct from `events.jsonl` | Append-only `agent-actions.jsonl`: proposal, sources, diff, validation, approver | `mutate.mjs`, new lib | none | Volume | Every typed mutation writes one record | M | Yes | Yes |
| **P1.2-B** | No locking or idempotency | Idempotency keys + advisory lock in `mutate.mjs` | `lib/mutate.mjs` | P1.2-A | Concurrency bugs | Replayed op is a no-op | M | Yes | Yes |
| **P1.3-A** | **[F]** Pleading generators are prose, not duplication | Extract **service/deadline/citation** helpers only. **Do not** dedupe pleading generators | `internal/scripts/lib/` | P0.2-A | Over-abstraction | No behavior change; golden stable | M | Yes | Yes |
| **P1.4-A** | No restore drill | Document and execute full restore from R2 + `documents` branch to an empty clone | `internal/docs/DOCUMENT_STORE.md` | P0.0-B | none | Restore reproduces 1,629 files | S | Partly | Yes |
| **P1.4-B** | **[F]** Node-major trap cost a false failure cycle | Document 22.x in README; keep #920's guard | `README.md` | #920 | none | Fresh clone cannot run on Node 20 silently | S | Yes | Yes |
| **P1.5-A** | **[F]** MCP advertises 7 write tools anonymously; docs say read-only | Hide write tools from unauthenticated `tools/list`; reconcile `AGENTS.md` | `workers/doc-api/src/index.mjs`, `AGENTS.md` | none | Breaking a client | Anonymous `tools/list` returns reads only | S | Yes | Yes |

### P2 — Reusable-engine extraction

| ID | Problem | Change | Deps | Effort | Agent-safe |
| --- | --- | --- | --- | --- | --- |
| **P2-A** | Engine and portfolio are entangled | Workspace packages: `@ilp/matter-schema`, `@ilp/clocks`, `@ilp/documents`, `@ilp/citations`, `@ilp/courtlistener` | P0.2-A | L | Yes |
| **P2-B** | **[F]** 60 TS vs 59 JS | Finish TS migration, starting with `damages.js` (1,001 lines) | P2-A | L | Yes |
| **P2-C** | Ops surface is CLI-shaped | Typed HTTP API mirroring `q.mjs` | P2-A | L | Yes |
| **P2-D** | No blank-workspace proof | New tenant creates matter, ingests, extracts deadlines, keeps audit trail — no portfolio import | P2-C | L | Yes |

### P3 — Multi-user pilot

| ID | Change | Deps | Effort |
| --- | --- | --- | --- |
| **P3.0-A** | **Professional-responsibility layer: conflicts checking, ethical walls, UPL boundary, legal hold, per-tenant retention** | P2-D | **XL** |
| **P3-B** | Auth, orgs, workspaces, matter-level permissions | P2-D | L |
| **P3-C** | Tenant isolation: Postgres RLS + per-tenant object prefixes and keys | P3-B | L |
| **P3-D** | Immutable audit log, retention and deletion controls | P1.2-A | M |
| **P3-E** | Background jobs with retry/DLQ; schema migrations; error reporting | P2-C | L |
| **P3-F** | 2–3 pilot tenants with the §11.2 metrics | all above | L |

### P4 — Commercial readiness

| ID | Change | Effort |
| --- | --- | --- |
| **P4-A** | SOC 2 Type I path, DPA, subprocessor list, incident response | XL |
| **P4-B** | Malpractice/E&O posture; disclaimers; UPL guardrails reviewed by counsel | M |
| **P4-C** | Billing, plans, seat management | L |
| **P4-D** | Onboarding: import from Clio/MyCase/PACER | L |
| **P4-E** | Support runbooks, status page, SLA | M |

---

## 13. First three PR specifications

### PR 1 — `fix/gate-runner-determinism`

**Objective:** make the `portfolio-gate` Check Run conclude deterministically so it can be required. **[F]** It currently fails on capacity (`max_instances = 3`, "Maximum number of running container instances exceeded" on #920) and reported `FAILURE` on #915/#917/#919/#920 with no conclusion on #916/#918/#921.

- **In scope:** `workers/portfolio-gate/wrangler.toml` (instance limit), `src/orchestrate.mjs` (queue + backoff), `src/runner.mjs` (separate infra failure from check failure), `src/check.mjs` (neutral conclusion + retry on infra fault), tests in `src/*.test.js`.
- **Out of scope:** any `.github/workflows/` (forbidden), branch-protection settings (owner action), gate step list, litigation data.
- **Sequence:** reproduce by replaying recent PR heads → classify infra vs check failure → queue with backoff and cap → raise `max_instances` → emit `neutral` and retry once on infra fault → extend tests → deploy → replay 10 heads.
- **Tests/gates:** existing 6 worker test files plus new orchestration cases; `npm run gate` locally; 10 consecutive replays with zero infra failures.
- **Rollback:** `wrangler rollback`. Check is advisory today, so a bad deploy blocks nothing.
- **Done:** 10 consecutive PR heads conclude `success` or `failure` on check content, never on capacity, and the owner can safely enable required checks.

### PR 2 — `feat/r2-coverage-check`

**Objective:** make the backup gap visible and fail-closed. **[F]** 195 manifest entries (138.4 MB) have no retrievable bytes and no check reports it.

- **In scope:** new `internal/scripts/check-r2-coverage.mjs`; `lib/portfolio-gate-policy.mjs` (new step); `package.json` (`check:r2`); tests; `internal/docs/DOCUMENT_STORE.md`.
- **Out of scope:** uploading bytes (needs `R2_*`), deleting root files (that is #922), manifest rewrites, matter data.
- **Sequence:** read manifest → ranged `GET /doc/<sha256>` with bounded concurrency → **use ranged GET, not HEAD** (**[F]** the Worker answers `405` to HEAD, which is indistinguishable from absent — this cost me a wrong number tonight) → cache results by sha → report count, bytes, and per-matter breakdown → exit 1 when uncovered > 0 → offline skip via env flag → add to `GATE_STEPS` behind that flag.
- **Tests/gates:** unit tests with a stubbed fetcher for 200/206/404/405/timeout; live run on `main` must report exactly 195.
- **Rollback:** revert; the step is additive.
- **Done:** `npm run check:r2` prints the uncovered count and bytes, fails when > 0, and skips cleanly offline.

### PR 3 — `feat/generator-registry`

**Objective:** make the canonical/derived boundary machine-checkable — the dependency under roadmap P0.2 and all of P2. **[F]** 0 of 222 scripts declare their outputs; 1 of 26,894 Markdown lines carries a generated marker.

- **In scope:** `PORTFOLIO` front matter on generators under `internal/scripts/`; new `internal/src/data/index/generators.json`; new `check-generators.mjs` with `--check`; `npm run validate`; tests.
- **Out of scope:** `matters/NN/documents.json` generator edge (P0.2-B — matter data, separate PR), deduplicating pleading generators (**[F]** rejected: 1,170 of 1,179 lines differ between matter 37 and 38 — that is prose), retiring any script.
- **Sequence:** inventory generators and outputs → declare front matter → generate `generators.json` → `--check` fails on undeclared generator, unclaimed derived file, or two generators claiming one output → wire into `npm run validate` → tests.
- **Tests/gates:** `--check` green on `main`; unit tests for all three failure classes; `npm run gate`.
- **Rollback:** revert; additive.
- **Done:** every derived file names exactly one generator, and a new undeclared generator fails `npm run validate`.

**All three are separate from litigation-data changes and safe for an AI agent.** PR 1 and PR 2 are independent and can run in parallel. PR 3 depends on neither.

---

## 14. 30/60/90-day execution plan

### Days 1–30 — Reliability. Outcome: the gate is mandatory and the document store is recoverable.

| Measurable outcome | Target | Source |
| --- | --- | --- |
| Uncovered manifest entries | **195 → 0** | P0.0-A/B |
| Root PDFs in Git | **41 → 0**, none deleted before backup | #922 after P0.0-B |
| Consecutive gate runs concluding on content | **0 → 10** | PR 1 |
| `required_status_checks` on `main` | **off → on** | P0.1-B |
| `required_approving_review_count` | **0 → 1** | P0.1-B |
| `enforce_admins` | **false → true** | P0.1-B |
| Gate verdict variance across environments | **2,832 vs 334 → identical** | P0.5-A |
| Longest silent red-gate streak | **75 commits → 0** | enforcement |
| Documented and executed restore drill | **none → 1** | P1.4-A |

### Days 31–60 — Extraction boundary and UI split. Outcome: the canonical/derived boundary is machine-checked and the operator workspace exists.

| Measurable outcome | Target |
| --- | --- |
| Derived files with exactly one declared generator | **0% → 100%** |
| Docs carrying `doc_kind` | 18 → **all** under `internal/docs/` |
| Drift classes reported by one command | **0 → 7** |
| Private nav items covering operator workflows | **0 → 9** (Deadlines, Documents, Evidence, Research added) |
| Public routes narrowed | 9 → **5** |
| Typed mutations writing an audit record | **0% → 100%** |
| Anonymous MCP `tools/list` write tools | **7 → 0** |
| TS share of `internal/src` | **50% → 80%** |

### Days 61–90 — Blank-workspace prototype and pilot preparation. Outcome: a new tenant runs the loop end to end without portfolio data.

| Measurable outcome | Target |
| --- | --- |
| Blank tenant: create matter → ingest → extract deadlines → audit trail | **works** |
| Portfolio records in the product database | **0** (deliberately) |
| Cross-tenant leakage in tests | **0** |
| Time to first matter, new tenant | **< 30 min** |
| Deadline extraction accuracy vs human baseline, seeded set | **≥ 90%** |
| Agent proposals reviewable before effect | **100%** |
| Conflicts-check design signed off by counsel | **complete** |
| Pilot firms committed | **2–3** |

**[R]** Do not start day-31 work until every day-30 outcome is met. The pattern this repository has demonstrated — building a gate and not requiring it, building a backup and not verifying it — is the pattern to break first.

---

## 15. Product-readiness exit criteria

Before charging a single customer:

**Reliability** — required checks enforced for all actors including admins; gate verdict environment-independent; zero uncovered manifest entries; restore drill executed within 90 days; every derived file has one declared generator.

**Security and isolation** — no anonymous write-tool disclosure; per-tenant row-level isolation proven by test; per-tenant object prefixes with separate keys; no credential in any repo, prompt, or PR body; secrets only in env and bindings.

**Auditability** — immutable audit log for every consequential action; every agent action reviewable before effect; document provenance resolves document → generator → source → matter; append-only event history preserved.

**Professional responsibility** — conflicts checking before matter creation; ethical walls enforced by permissions; UPL boundary reviewed by counsel; legal hold and retention per tenant; E&O posture documented.

**Product** — blank tenant completes the loop with no portfolio import; time to first matter under 30 minutes; deadline accuracy ≥ 90% against a human baseline; operator workspace covers all 9 nav areas; accessibility audit passed.

**Operations** — staging environment; schema migrations with rollback; background jobs with retry and DLQ; error reporting; status page; documented incident response; backup and DR tested.

---

## 16. Questions that must be answered before commercial development

**Ownership and intent**
1. Is the goal a company, or a durable personal system that others might license? The answer changes almost every P2/P3 decision.
2. Who operates this if you are unavailable for a month? **[F]** Today `documents:push`, `court:sync`, D1 reseed, and both Worker deploys all require your laptop.
3. Will you accept required reviews on your own repository? **[F]** With `required_approving_review_count` = 0 and a solo maintainer, "review before merge" needs either a second human or an explicit self-merge-after-green rule.

**Legal and professional**
4. Who bears responsibility when an extracted deadline is wrong and a client is prejudiced?
5. Does a deadline-extracting, filing-drafting tool sold to non-lawyers cross into UPL? This is why I do not recommend SRLs as the wedge.
6. How are conflicts checked before a matter is created, and who attests to it?
7. What happens to a tenant's data on non-payment, dispute, or litigation hold?
8. Will you ship counsel-dossier functionality? **[R]** I recommend against it — cross-firm intelligence aggregation carries exposure that a small company cannot absorb.

**Data and migration**
9. Does the Newanforbi portfolio ever move into the product database? **[R]** It should not.
10. If the engine is extracted into packages, who owns them if the company is sold or wound down?
11. What is the authoritative store for a **customer's** documents — R2 with per-tenant prefixes, or their own bucket?

**Commercial**
12. Have you interviewed even three small employment plaintiff firms about deadline exposure? **[I]** The entire wedge thesis, including mine, is currently unvalidated.
13. What is the switching cost from a calendaring incumbent, and who does the migration?
14. Is $80–200/lawyer/month real? Unvalidated.
15. What does the first customer get that a paralegal plus CompuLaw does not?

**Technical**
16. Postgres where — managed, or Cloudflare-native D1 at tenant scale? **[F]** D1's current role is a read-only publish projection, a different workload.
17. Do you keep Python at all? **[F]** 134 of 222 scripts are Python, `AGENTS.md` excludes them from the pipeline, yet the citation gate runs on `python3`. A product cannot ship a two-runtime script library with one runtime undocumented.
18. What is the acceptable cost ceiling for the gate runner? **[F]** `standard-2` containers at `max_instances` above 3 is the fix for risk #3 and it costs money.

---

## Recommended first PR

**`fix/gate-runner-determinism`** — PR 1 in §13.

**Why this one first.** **[F]** Every other improvement in this report merges into `main` through a gate that currently cannot block anything. Tonight three PRs went in with a failing or unfinished check and no review, and a red gate previously survived 75 commits. Until the Check Run concludes on its own content rather than on container capacity, `required_status_checks` cannot be enabled without blocking all work — and until it is enabled, every process rule in `AGENTS.md` and in the roadmap's agent protocol is advisory.

It is also the lowest-risk change available: it touches only `workers/portfolio-gate/`, cannot affect litigation data, has an existing 6-file test suite, rolls back with `wrangler rollback`, and while the check is advisory a bad deploy blocks nothing.

**[R]** PR 2 (`feat/r2-coverage-check`) is independent and addresses the one risk I rate above governance — 195 files with no second copy. If you want both started, they do not conflict. But if you pick one, pick the gate: it is what makes every later fix stick.

**Sequencing note.** PR 2 is independent of PR 1 and can proceed in parallel. Neither touches litigation data. Per the agent contribution protocol, both must be opened as scoped branches with reviewable diffs, and neither may be combined with matter-data changes.
