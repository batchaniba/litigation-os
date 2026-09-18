# Matter 40 — Pleading Engineering v2.1 — Maximum-Value Rebuild

**PR:** #861  
**Branch:** cursor/matter-40-close-taskus-loop-29a6  
**Operative review draft:** internal/docs/matter-40/ND_CAL_COMPLAINT_REVIEW_DRAFT_V2.md  
**Record cutoff:** September 17, 2026

This memo replaces the earlier five-count filing theory.

## 1. Core change

The old v2 over-concentrated value in the idea that the September 14 hold already supplied the FCRA adverse action and § 290.46 use.

That is vulnerable because PRINSOS was still In Progress when the hold issued, the California-registry-sourced result was furnished September 15, the saliva-confirmation failure arrived September 16, and the anticipated September 23 start is still in the future as of the record cutoff.

The rebuild separates two categories.

### Procurement-side claims

Potentially complete when Order WPS-361214148 was procured:

1. FCRA § 1681b(b)(2)(A) — standalone employment disclosure / authorization architecture.
2. ICRAA § 1786.16 — California standalone investigative-report disclosure requirements.

Both are **audit-gated**. The repo identifies a United States Background Consent Form but no separate compliant FCRA/ICRAA disclosure. Do not assume an unseen Profile Advantage screen did not exist.

### Adverse-use claims

These require a verified post-furnishing employment event:

3. FCRA § 1681b(b)(3)(A).
4. Penal Code § 290.46(j)(2)(E).
5. ICRAA § 1786.40 if employment is actually denied.

The September 14 hold remains evidence that background screening affected release of the start. It is not treated as adverse action based on a completed registry result.

## 2. Why procurement materially improves leverage

FCRA § 1681b(b)(2)(A) regulates procurement itself. If the complete authorization flow lacks the required standalone disclosure, liability does not turn on whether the registry, saliva test, MVR, or another screening component caused the later employment outcome.

ICRAA § 1786.16 is also important. In **Parsonage v. Wal-Mart Associates, Inc., D083831 (Cal. Ct. App. Feb. 4, 2026)**, the court enforced the standalone disclosure requirements and held that Civil Code § 1786.50 supplies the statutory $10,000 alternative to actual damages in an individual action under California law.

Federal Article III remains a separate forum issue. The cleanest federal posture is obtained once concrete economic injury from a post-report employment decision is also present.

## 3. Claims removed from the lean complaint

### Tameny / wrongful failure to hire — remove

**Williams v. Sacramento River Cats Baseball Club, LLC, 40 Cal.App.5th 280 (2019)** requires a preexisting employment relationship for the common-law Tameny tort. An accepted offer improves damages proof, but it should not be used to plead around Williams.

If Plaintiff actually begins work and is later terminated, reassess.

### UCL — remove

The UCL adds little monetary leverage in this posture. Expected future wages are a poor restitution fit and the complaint already seeks legal/statutory remedies. Keeping the UCL invites an avoidable equitable-remedy fight.

### ICRAA § 1786.40 — gate

Use only after an actual employment denial and only if the denial-time advice required by the statute was not given.

## 4. § 290.46 — actual use, not transmission

The report expressly says:

> SOURCE OF RECORD: CALIFORNIA SEX OFFENDER REGISTRY.

That sharply improves source proof.

But **Mendoza v. ADP Screening & Selection Services, Inc., 182 Cal.App.4th 1644 (2010)** distinguishes republication by a screening company from an employer's actual use of the information as the basis for an employment decision.

Therefore:

- do not treat First Advantage's furnishing alone as prohibited employment use;
- do not treat the September 14 hold as use of a completed California-registry result;
- identify the actual post-September-15 decision actor and the conduct showing the registry information was applied.

The complaint should answer: **who used it, when, and what employment decision did that use cause?**

## 5. September 15–16 is the value center

Timeline:

- Sep. 14 ~10:20 a.m. — PRINSOS In Progress.
- Sep. 14 11:24 a.m. — TaskUs holds start pending background report.
- Sep. 15 — First Advantage furnishes report to TASKUS HOLDINGS INC USA; California registry source expressly identified.
- Sep. 16 3:05 p.m. — saliva confirmation failure.
- Sep. 17 — saliva schedule expires.

Highest-value missing proof:

1. First Advantage transmission/access timestamps.
2. TaskUs access and audit logs.
3. adjudication matrix output.
4. WorkDay status changes.
5. eligibility codes.
6. TA Ops / BGV messages.
7. Uber start-authorization or veto records.
8. Uber↔TaskUs package configuration.

A registry-triggered review, consider, ineligible, hold-extension, or start-veto event **before the saliva failure** would materially strengthen both FCRA causation and § 290.46 actual use.

## 6. Actor-specific pleading

### TaskUs USA, LLC

The background-consent/release paperwork identifies TaskUs USA. If the disclosure audit supports procurement claims, it should not remain buried in DOES.

### TaskUs Holdings, Inc.

First Advantage identifies TASKUS HOLDINGS INC USA as the report-recipient account. Holdings is also tied to other onboarding documents.

### TaskUs, LLC

Offer-letter entity; California record is Converted Out. Preserve its factual role but do not serve the former agent by habit.

### Uber Technologies, Inc.

Keep Uber only to the extent evidence supports campaign-level control or actual use. Campaign branding proves the assignment, not report receipt or statutory use.

Do not use alter-ego boilerplate without corporate-separateness facts.

## 7. Damages engineering

- FCRA: negligent and willful noncompliance in the alternative; §§ 1681n and 1681o according to proof.
- ICRAA: preserve § 1786.50 actual-or-statutory relief, fees/costs, and punitive damages upon the required showing.
- § 290.46(j)(4)(A): plead actual damages; the additional statutory amount determined by the trier of fact subject to the statutory cap/floor; attorney's fees; exemplary damages and/or civil penalty according to proof.
- Economic loss: the offer proves the $22 hourly rate, anticipated assignment window, and $1,000 retention opportunity. It does **not** prove 40 guaranteed weekly hours. Do not invent them.

## 8. Filing timing

As of September 17, do not plead that a September 23 start "never occurred."

Activate the post-report counts only after one of these occurs:

1. unequivocal pre-adverse/final adverse or rescission communication;
2. documented post-report ineligible/decision code;
3. September 23 passes and the record supports a report-based refusal to release the start;
4. other evidence proves actual post-report use.

If only disclosure-form defects remain, reassess Article III and forum strategy before filing.

## 9. Current count architecture

| Count | Theory | Status |
|---|---|---|
| 1 | FCRA § 1681b(b)(2)(A) procurement disclosure | Audit gate |
| 2 | ICRAA § 1786.16 / § 1786.50 | Audit gate |
| 3 | FCRA § 1681b(b)(3)(A) | Post-report action gate |
| 4 | Penal Code § 290.46(j)(2)(E) | Actual-use gate |
| 5 | ICRAA § 1786.40 | Denial gate |

Dropped: UCL; Tameny failure-to-hire.

## 10. Do-not-do list

- Do not file v1 by habit.
- Do not allege a September 23 non-start before September 23.
- Do not describe the September 14 hold as adverse action based on a completed report.
- Do not turn First Advantage transmission into employer "use" under § 290.46.
- Do not hide the saliva event.
- Do not plead Uber use from branding alone.
- Do not use alter ego as boilerplate.
- Do not bury TaskUs USA in DOES if the disclosure audit makes it a procurement actor.
- Do not calculate 40-hour lost wages absent schedule proof.
- Do not attach the evidence stack at pleading.
- Do not serve TaskUs, LLC's former agent merely because that name appears on the offer.
