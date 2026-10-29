# Matter 29 Research Branch

This private research room is the think tank for **Newanforbi v. Amazon.com Services, LLC et al.**, N.D. Cal. No. **4:26-cv-09249-ASK**, Magistrate Judge Ajay S. Krishnan (Oakland). Plaintiff appears in propria persona.

It follows the Matter 20 gold-standard layout (`research/matter-20-2026-10-24` → `internal/private/research/matter-20/`) and the Matter 28 hearing-room conventions (`research/matter-28-cisneros-hearing-2026-10-25`). It preserves sources, independent graph snapshots, extracted text, audit/provenance, a record-to-argument map, and separately authored analysis. It does **not** change the portfolio's live docket, calendar, public registry, or R2 objects.

Prepared October 28, 2026. Private working analysis. Nothing here has been filed, served, or adopted by the Court.

## Matter identity

| Field | Value | Source |
|---|---|---|
| Portfolio id | **Matter 29** (already assigned; not a new id) | `internal/src/data/matters/29/matter.json` |
| Caption | Newanforbi v. Amazon.com Services, LLC | matter.json |
| Case no. | 4:26-cv-09249-ASK (formerly 3:26-cv-09249-ASK) | matter.json |
| Court | USDC N.D. Cal., Oakland | matter.json |
| Judge | Hon. Ajay S. Krishnan, U.S. Magistrate Judge | matter.json; Dkt. 9 |
| Defendants | Amazon.com Services, LLC; Accurate Background LLC; DOES 1–10 | parties.json |
| Amazon counsel | Morgan, Lewis & Bockius LLP — Andrew P. Frederick, Douglass G. Brown, Suga A. Ikeda | events.jsonl; clocks `29-rule26f-meet-confer` |
| Accurate counsel | Seyfarth Shaw LLP — Jasmine J. Stanzick, John Drury | events.jsonl; counsel.json |
| Phase | `mtd_briefing` | matter.json snapshot |
| Cluster (numbered) | 3 = Employment Violations | matter.json `cluster` |

No `internal/private/research/matter-29/` path existed on scanned remotes before this branch. Prior Matter 29 work lives in `internal/docs/matter-29/`, `internal/docs/counsel/frederick-stanzick/`, `documents/matter-29/`, and `internal/private/negotiation/29.jsonl`.

## Start here

1. **[26(f) prep sheet (Nov. 6)](10-rule26f-prep/00-26F-PREP-SHEET.md)** — conference identity, objectives, agenda, what to say, what not to volunteer.
2. **[Deadline list](11-deadlines/DEADLINE-LIST.md)** — live clocks plus statutory watches; this room is not a substitute for `clocks.json`.
3. **[Open questions](12-open-questions/OPEN-QUESTIONS.md)** — P0/P1/P2 confirmations. Companion: [gaps](08-audit/GAPS-AND-CONFLICTS.md).
4. **[Oct. 28 reinvestigation analysis](09-merits-analysis/REINVESTIGATION-ANALYSIS.md)** — letter + revised report vs. the Oct. 14 report and the Oct. 14 dispute.
5. **[Amazon / Accurate strategy assessment](09-merits-analysis/DEFENSE-STRATEGY-ASSESSMENT.md)** — separate defense desks, causal tests, first-wave discovery, decision rules.
6. **[Facts](09-evidence-map/FACTS.md)** — FACT / INFERENCE / UNVERIFIED / QUESTION.
7. **[Chronology](09-evidence-map/TIMELINE.md)**.
8. **[Claims matrix](09-merits-analysis/CLAIMS-MATRIX.md)**.
9. **[Record-to-argument map](09-evidence-map/RECORD-TO-ARGUMENT-MAP.md)**.
10. **[Exhibit / evidence index](09-evidence-map/EXHIBIT-INDEX.md)**.
11. **[Authority ledger](09-merits-analysis/AUTHORITY-LEDGER.md)** — statutes and repo-verified cases only; no invented citations.
12. **[Discovery plan](03-discovery-production/DISCOVERY-PLAN.md)**.

## Collection structure

| Directory | Purpose |
|---|---|
| `00-user-inputs/` | This request and the Oct. 28 Accurate letter + enclosed revised report (25 pp.) |
| `01-portfolio-records/` | Locators to live `documents/matter-29/` pleadings. Bytes are not duplicated. |
| `02-consumer-reports/` | Oct. 14 vs. Oct. 28 comparison and locators |
| `03-discovery-production/` | Discovery plan, ESI notes, locator to the Oct. 17 discovery-set-one branch (not on main) |
| `04-drafts-and-working-papers/` | Conference-only drafts. Nothing is certified for filing or service |
| `05-prior-analysis/` | Snapshots of the Oct. 14 accuracy audit, 60-day calendar, dispute draft, and discovery-set-one README/ESI proposal. Historical; not re-adopted |
| `06-source-snapshots/` | Frozen Matter 29 graph siblings as of branch creation. Consult live `clocks.json` / `docket.json` for current dates |
| `07-source-text/` | Extracted text of the Oct. 28 PDF. The PDF controls |
| `08-audit/` | Inventory, hashes, gaps, verification limits |
| `09-evidence-map/` | Facts, chronology, exhibit index, record-to-argument map |
| `09-merits-analysis/` | Claims matrix, authority ledger, reinvestigation analysis, defense-strategy assessment |
| `10-rule26f-prep/` | Nov. 6 conference prep (this room's `10-*` tail, analogous to Matter 28 `10-hearing-prep/`) |
| `11-deadlines/` | Deadline list for the user |
| `12-open-questions/` | Open-questions list for the user |

Two `09-*` siblings are intentional (Matter 20 / Matter 28). Parallel `10-*` workstreams are allowed; this room uses one `10-rule26f-prep/` plus numbered `11`/`12` for the requested deliverables.

## Working rules

- Keep allegations, evidence, judicial findings, historical analysis, and proposed conference positions distinct.
- Label **FACT**, **INFERENCE**, **UNVERIFIED**, **QUESTION**, **MISSING**.
- Never invent a docket number. If `dkt` is null, say so. Plaintiff's opposition to Dkt. 19 has **no ingested ECF number**.
- Live calendar truth is `internal/src/data/matters/29/clocks.json`, not this README and not the Oct. 14 sixty-day calendar snapshot (which still said no 26(f) date had been agreed).
- Do not put settlement figures, walk-aways, or ledger contents in anything defense counsel will see. Settlement-guard: `internal/docs/settlement/SETTLEMENT_REANCHOR_MEMO.md` § 3; ledger `internal/private/negotiation/29.jsonl`.
- Do not email counsel about the Frederick–Stanzick playbook, *Lerma*, *Carrillo*, *Varela*, or *Santee*. Those dockets are not Civil L.R. 3-12 related cases unless a court says they are.
- Never write that Amazon settled the identical § 290.46 claim. *Lerma* Dkt. 36 dismissed that theory; the later settlement was on the surviving Fair Chance Act claim against Amazon.
- This directory stays under `internal/private/`. Do not register its contents in the public SPA, Worker/D1 publication, public document manifest, or calendar merely because they were collected here.
- A research revision does not establish user approval, operative status, or filing readiness.

## Relationship to other rooms

| Room | Role |
|---|---|
| Matter 20 `internal/private/research/matter-20/` | Gold-standard numbered collection + audit + maps |
| Matter 28 `internal/private/research/matter-28/` | Leaner federal 26(f)/hearing analog (two-defendant N.D. Cal.) |
| Matter 32 `internal/private/research/matter-32/` | Heavy MTD-opposition workshop; not copied wholesale |
| `internal/docs/matter-29/` | Accuracy audit, 60-day calendar (snapshot here; some dates stale) |
| `origin/matter-29/discovery-set-one-amazon-accurate-2026-10-17` | 71-request packet + ESI proposal. **Not on main.** Locator only |
| `internal/docs/counsel/frederick-stanzick/` | Two-desk playbook. Do not send |
