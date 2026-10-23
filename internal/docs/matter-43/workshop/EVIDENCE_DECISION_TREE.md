# Matter 43 — evidence matrix and decision gates

As of 2026-10-22. This is an evidence-to-question map, **not** a claim chart or a calendar.

## Source inventory (source hashes and original names in PR #1024)

| ID | Evidence type | Supports | Does **not** establish |
|---|---|---|---|
| E01 | iMessage interview invitation and travel-delay screenshot, IMG_8701.jpeg | Recruiter contact, Ridder Park location, applicant's arrival message | Definitive interview day; hiring decision |
| E02 | iMessage offer-intent screenshot, IMG_8702.jpeg | Kathleen's representation that a Palo Alto offer was forthcoming | Full terms or binding offer on its own |
| E03 | Gloria Williams email, “Following Up On Your Application with Hertz.pdf” | Recruiting team desired to extend a Manager Trainee offer | Acceptance, vetting outcome |
| E04 | Hertz Careers “offer ... extended” email | Offer issuance notification | The complete conditions without the letter |
| E05 | “Hertz Careers.pdf” offer letter (3 pages) | **The Hertz Corporation**, role, workplace, $23/hour, supervisor, conditions and at-will terms | Fixed weekly hours, guaranteed employment, specific reporting vendor |
| E06 | “Congratulations, you accepted the job offer Manager Trainee!.pdf” | Hertz portal's acceptance confirmation, Oct 22 at 5:00 p.m. | Background-check clearance or start date |
| E07 | “My Applications - Hertz Careers.pdf” | Job application #43711, status “Offer Accepted” | Background result |
| E08 | ADP WOTC request email | A tax-credit questionnaire requested for Hertz Global Holdings, Inc. | Criminal-background report authorization/vendor identity |
| E09 | ADP WOTC confirmation page | Questionnaire completion | Qualification for WOTC or screening clearance |
| E10 | Hertz Careers additional-information email | Outstanding request shown October 22 | Completion, deadline, or nature of unsubmitted fields |

**Integrity:** SHA-256 checksums and file descriptions are in internal/private/matters/43/EVIDENCE_INTAKE.md, on the #1024 branch. Original evidence bytes are not present in this workshopping PR. No path should be added to documents.json unless the bytes are actually ingested and retrievable.

## Dated sequence: preserve conflicts

| Timestamp (PT, if shown) | Event | Confidence / ambiguity |
|---|---|---|
| “Yesterday 12:27 PM” in screenshot | Interview message mentions “Thursday 10/21 at 1pm” | **Literal text conflicts with 2026 calendar**. Neither Wednesday Oct 21 nor Thursday Oct 22 is silently selected. |
| Oct 22, 1:03 p.m. | Applicant texts rain/traffic delay | Screenshot “Today” interpreted with Oct 22 context |
| Oct 22, 3:38 p.m. | Gloria Williams emails offer forecast | Source email timestamp |
| Oct 22, 3:39 p.m. | Hertz Careers offer notification | Source email timestamp |
| Oct 22, 3:40 p.m. | Kathleen texts offer forecast | Screenshot timestamp |
| Oct 22, 4:49 p.m. | Applicant replies accepting | Email timestamp |
| Oct 22, 5:00 p.m. | Hertz Careers confirms offer accepted | Email timestamp |
| Oct 22, 5:00 p.m. | ADP WOTC request and Hertz additional-information request | Separate, simultaneous notices; neither is proof a criminal report was issued |
| Oct 22, 5:44 p.m. (capture) | WOTC confirmation page shows completion | Capture time is not proof of exact submission time |

## Decision gate tree

**G0 — Accepted offer / routine onboarding (current state).** Continue onboarding, retain confirmations, obtain written start details if provided. No adverse-action claim.

**G1 — Administrative gap or missed onboarding task.** Determine whether the missing task, identity mismatch, scheduling, or response timing accounts for a delay; document requests and completion. Do not assign screening causation prematurely.

**G2 — Background/MVR process begins.** Archive the employer's authorization, all notices, provider identity, applicant copy requests, report date and source labels. WOTC forms are a different workflow.

**G3 — Report arrives and is accurate / approved.** Record result and job commencement. This is a win; no need to manufacture a litigation theory.

**G4 — Report disputed or inaccurate.** Preserve exact disputed fields, source, time of dispute, and correction result. Evaluate consumer-reporting rights only against the actual provider, report, and statutory framework.

**G5 — Employer announces preliminary or final adverse action.** Preserve decisionmaker, communication, report version, notice contents, reason given, time allowed to respond, individualized assessment documentation (if implicated), and any other independent reason. Analyze the relevant hiring jurisdiction and exceptions only with primary law.

**G6 — Final no-start / rescission / changed terms.** Establish the factual causal chain: offer → conditions → documented report/source → employer knowledge → rationale → final decision → demonstrated injury. Keep alternative lawful explanations in the chart.

## Competing hypotheses (none established beyond current G0)

| Hypothesis | What would support it | Best falsifier / alternative |
|---|---|---|
| H0 — Hired normally | Start/assignment/pay record, background pass | Actual rescission/no-start |
| H1 — Onboarding logistics | Incomplete additional-info task, timeline emails | Completed tasks and independent reason |
| H2 — MVR/driver eligibility | Driving-related selection rule and MVR result | Employer record identifies a distinct reason |
| H3 — Conviction-history selection | Assessment, relevant report and decision note | Unrelated reason or no assessment activity |
| H4 — Misuse of Megan's Law **website** data | Public-site source trace, access/use documents, causal decision | Court-record/criminal check source without website use; statutory exception |
| H5 — Consumer-report process/accuracy defect | Disclosure, authorization, report, notices, disputed field, attributable process lapse | Compliant documents or no consumer report used |
| H6 — Operational or role cancellation | Vacancy cancellation, position eliminated, location capacity | Personalized screening-based rationale |

The hypotheses are **mutually compatible in some combinations**; do not force a single-cause story without proof.

## Evidence requests to prioritize if triggered

1. Onboarding completion status and all outstanding tasks; confirmation of actual start date, expected hours, and benefit terms.
2. Separate standalone background disclosures, authorization, selection of reporting vendor, notices, and user copy election.
3. Complete MVR and consumer report with exact creation/finalization/delivery times, originating source labels, dispute records, and versions.
4. Employer's exact stated reason, internal hiring decision timestamps, decisionmaker, and any individualized assessment communications.
5. Proof of consequence: start delayed or rescinded, wage evidence, mitigation records, costs, and benefit loss if any.

These are **collection categories**, not discovery requests for service on a non-party or unfiled action. Do not falsely label a watch item a statutory deadline.

## Conditional economics

Offered hourly base = **$23.00**. Simple annual sensitivity if **40 paid hours x 52 weeks** = **$47,840** gross. This is **not** a guaranteed contract term, established lost wages, case value, or settlement floor. Required for any quantified loss: actual start, paid hours, duty/mitigation period, intervening earnings, and causation.
