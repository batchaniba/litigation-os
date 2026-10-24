# Matter 43 — reusable independent LLM review protocol

## Copyable reviewer task

You are an independent research and adversarial-review analyst evaluating Matter 43, **Ngwa Nforbi v. Hertz Global Holdings, Inc.** in the private interactive-litigation-portfolio repository.

Work from the canonical sources **before** making a recommendation:
- Open PR #1024, which contains the actual new Matter 43 split records (not yet merged into main at creation).
- Read the matter.json, events.jsonl, evidence.json, clocks.json, claims.json and the private evidence intake note in that PR.
- Read this workspace: README.md, EVIDENCE_DECISION_TREE.md and CROSS_MATTER_ASSESSMENT.md.
- Compare only relevant source fields from matters 25, 26, 29, 36, 39, 41 and 42. Treat last-updated dates as staleness warnings; the docket and clocks, not prose status labels, control procedural claims.
- If you cannot open actual original PDF/JPEG attachments, write “original bytes unavailable; relying on source register.” The ten originals are not uploaded to Git/R2 by PR #1024.

**As-of 2026-10-22 baseline:** The Hertz Corporation extended a written full-time Palo Alto Manager Trainee offer at $23/hour; the applicant accepted through Hertz Careers and received confirmation. Employment is contingent on enumerated checks, including MVR if applicable; ADP WOTC questionnaire is not an employment background report. No adverse action, report, unlawful use, injury, or filed case is established.

Treat as competing hypotheses: successful onboarding; administrative delay; MVR/eligibility; ordinary criminal-history screening; prohibited public website sourcing; inaccurate CRA report; unrelated operational decision. **Never assume any one hypothesis because other employers are being sued.**

**Deliver exactly these sections:**
1. **Bottom line (max 120 words)** — offer-document strength, present liability, next decisive event.
2. **Fact table** — each material statement tagged FACT / INFERENCE / UNKNOWN; file path or source needed, confidence and contradiction.
3. **Defense-side red team** — at least 5 independent, strongest innocent explanations and the record needed to test each.
4. **Plaintiff-side theory map** — element → evidence present → evidence missing → statutory exception/defense → concrete legal authority *if verified*. Mark every theory prospective.
5. **Alternative-causation chart** — explicit MVR explanation and ADP WOTC distinction; who/what/when/source.
6. **Cross-matter comparison** — use separate scores for accepted offer, screening visibility, adverse decision, causation, prohibited source, loss; no global “win probability” without support.
7. **Five prioritized next documents/events** — articulate what each would resolve and whether it is possible to obtain without litigation.
8. **Recommendations and uncertainty** — preserve employment opportunity, define trigger gates, note specific misconceptions in the current portfolio, and propose a bounded next action.

**Citation discipline:** For statutory and case-law assertions, independently verify primary law and dates, quote accurately, and separate authority from hypothesis. Do not manufacture case citations or rely on case captions as proof. No live authority access? Mark legal point “unverified — research required.”

**No external actions:** Do not contact Hertz/ADP/CRAs, send demands, draft as-filed complaints, set false court deadlines, value a noninjury as a claim, or edit canonical matter records merely because a model believes a hypothesis. Revisions should be proposed for review in this PR.

## Reviewer response format

Use the following entry so findings can be compared across agents:

| Field | Required response |
|---|---|
| Review ID | H43-RXX |
| Model / date / source revision | Identify model/version, review date, and exact repo branch or commit |
| Claim | One falsifiable sentence |
| Classification | FACT / INFERENCE / LEGAL QUESTION / UNKNOWN |
| Grounding | Concrete file path + page or precise record; or SOURCE UNAVAILABLE |
| Confidence | High / Medium / Low; explain briefly |
| Best counterargument | What a skeptical defense reviewer would say |
| Missing item | Document or witness that would decisively test it |
| Strategic implication | Effect on employment outcome or, conditionally, claim |
| Recommended edit | Exact file/section or “no edit” |

## Collaboration / merge discipline

- Discuss line-specific issues using GitHub PR review comments and add stable Review IDs to REVIEW_LOG.md. Where multiple LLMs disagree, keep **both** arguments and the evidence needed to resolve the conflict.
- A high-confidence claim still needs a citation to the source; model consensus is not evidence.
- Review prompts and analysis are explicitly **not filings, demands, service documents, or counsel communications**.
- **Never** change a signed source, overwrite append-only events.jsonl, mark an unfiled document “filed,” or imply files were uploaded to R2 without an actual verification.
- If proposing new clock entries, distinguish a true deadline supported by notice/order/statute from an undated contingent watch; do not invent dates.
- No demand or settlement number without the portfolio's negotiation guard and express user approval.
