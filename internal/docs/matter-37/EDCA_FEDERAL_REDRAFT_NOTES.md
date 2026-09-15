# Matter 37 — E.D. Cal. Federal Redraft Notes

## Objective

Replace the never-filed September 8, 2026 San Joaquin packet with a federal-first review draft engineered for a direct filing in the U.S. District Court for the Eastern District of California, Sacramento Division.

The state packet remains historical work product only. It was never clerk-filed.

## Recommended claim architecture

### Count 1 — FCRA § 1681b(b)(3)(A), Home Depot

This is the federal-question anchor.

The theory is deliberately narrow: Home Depot procured a First Advantage consumer report for employment purposes and took adverse action based in whole or in part on it without first giving Plaintiff (1) the report and (2) the written Summary of Rights.

The public-source record now materially strengthens this count even before the Home Depot-specific report is obtained. A Home Depot-branded background-check disclosure filed as an exhibit in *Ford v. Home Depot U.S.A., Inc.*, S.D. Cal. No. 3:19-cv-00754, identifies First Advantage Background Services Corp. as the CRA Home Depot would use for California investigative consumer reports and expressly states that Home Depot would provide the report and FCRA rights summary before adverse action. That supports both the vendor allegation and corporate knowledge of the pre-adverse requirement. The transaction-specific report remains necessary to prove what happened in Plaintiff's individual screening.

### Count 2 — ICRAA §§ 1786.40 / 1786.50, Home Depot

Use ICRAA for a **different omission** from Count 1: when employment was denied under circumstances in which an investigative report had been obtained, Home Depot failed to advise Plaintiff and supply the CRA’s name and address.

That distinction is intentional. Civil Code § 1786.52(a) contains an anti-duplication rule barring an ICRAA § 1786.50 suit for the **same act or omission** that is already the subject of an FCRA §§ 1681n / 1681o action. The federal draft therefore does **not** add a separate FCRA § 1681m(a) final-adverse-notice count that would substantially overlap § 1786.40.

### Count 3 — Penal Code § 290.46(j), Home Depot

The complaint now pleads source and use as **ultimate facts on information and belief**, with UPS/FedEx same-consumer First Advantage comparators as the factual basis. It does not wait for the Home Depot-specific report to state the claim, and it does not pretend those comparator reports are Home Depot's report.

Exact source-field wording, adjudication codes, and access timestamps remain reserved for discovery. If the Home Depot-specific First Advantage report is obtained before filing, replace the I&B source allegation with its exact wording after a hostile contradiction audit. That is an upgrade, not a precondition to stating Count 3.

## Claims intentionally omitted

- **UCL § 17200:** omitted. It adds standing/remedy complications in federal court and does not materially improve damages. *Yeh v. Barrington Pacific* reinforces that UCL standing is distinct from ICRAA standing.
- **CCRAA:** omitted unless the Home Depot report turns out to be a consumer credit report rather than an investigative employment background report.
- **Tameny / IIED:** omitted because the alleged adverse action dates to approximately August 2024 and the two-year limitations issue is facially unattractive.
- **FEHA / Fair Chance Act:** not pleaded without the required administrative/exhaustion record and a separate factual basis tied to conviction-history procedure.
- **FCRA § 1681b(b)(2)(A):** reserved unless the actual Home Depot disclosure/authorization form is in hand and defective.
- **FCRA § 1681m(a):** omitted to avoid needlessly colliding with ICRAA § 1786.40 under Civil Code § 1786.52(a).
- **First Advantage as a defendant:** not yet. Pilot and Randstad show the case can be strongest when the CRA is the document source and the employer is the user. Add First Advantage only if the Home Depot-specific records support an independent CRA violation (for example a well-supported § 1681k theory), not merely because it furnished the report.
- **Prospective injunction / UCL injunction / § 290.46(j)(4)(B):** omitted from the opening complaint. One transaction does not itself establish a pattern or practice, and federal Article III future-injury standing would create an avoidable side fight.

## The filing-critical limitations section

The direct federal filing needs an exact discovery allegation. This redraft still does **not** invent one.

FCRA § 1681p permits suit no later than the earlier of:
- two years after discovery of the violation; or
- five years after the violation.

ICRAA § 1786.52 provides two years from discovery.

Because the employment decision is alleged to have occurred around August 2024, using the ghosting date as discovery would make a September 2026 filing late. The complaint therefore pleads that 2024 revealed only the employment result. Home Depot never gave Plaintiff the report, identified First Advantage, or disclosed the report-based statutory omissions.

Do **not**:
- fill August 2024 as the FCRA/ICRAA discovery date;
- treat UPS’s or FedEx’s First Advantage report as discovery of Home Depot’s violation;
- treat the *Ford* public-source research as a filled discovery date unless that is in fact when Plaintiff first learned a consumer report was used in *this* transaction.

The next operational step is serving the First Advantage §§ 1786.10 / 1786.22 request and the Home Depot Labor Code § 1198.5 request. If those files produce the Home Depot-specific report, that production can pin the date. The FCRA five-year outer bound from an August 2024 violation runs to approximately August 2029. The two-year discovery clock is the constraint that must be pleaded truthfully.

Do not file the federal complaint until this date is verified.

## E.D. Cal. engineering

- Federal question: 28 U.S.C. § 1331 + FCRA.
- Diversity in the alternative: 28 U.S.C. § 1332(a) — Delaware corporation, Atlanta principal place of business, California plaintiff. Amount in controversy is pleaded in the aggregate without inventing a wage rate.
- Supplemental jurisdiction: 28 U.S.C. § 1367(a).
- Venue: 28 U.S.C. § 1391(b)(2).
- San Joaquin County places the action in the Sacramento side of E.D. Cal. under Local Rule 120(d).
- Serve CSC at 2710 Gateway Oaks Drive, Suite 150N, Sacramento, CA 95833. Do not serve the Tracy warehouse.
- Complaint is intentionally unverified. Rule 11 supplies the federal certification; there is no strategic need to convert every information-and-belief allegation into a verification issue.
- Keep the pleading concise. Save *Donaleski*, *Lerma*, *Dutta*, *Walker*, and the UPS/Randstad comparison record for motion practice unless a short citation becomes necessary.
- Do not plead another employer’s First Advantage report as proof of what the Home Depot report says.
- Generate the review-draft PDF with `python3 internal/scripts/matter37-edca-complaint.py`. Use official JS-44 / AO-440 / AO-239 forms; do not homemade them.

## Public-source vendor upgrade

The First Advantage identity is no longer a bare placeholder.

The record now includes:

- a Home Depot-branded California disclosure in *Ford* identifying First Advantage as Home Depot's CRA;
- *Bolton v. First Advantage LNS Screening Solutions, Inc.*, S.D.N.Y. No. 1:14-cv-05735, recounting a First Advantage report furnished to prospective employer Home Depot in July 2013;
- First Advantage's December 2019 public workforce-screening webinar featuring a Home Depot representative; and
- later publicly indexed Home Depot / First Advantage reports and applicant accounts corroborating continuity.

The complaint therefore pleads First Advantage as Home Depot's CRA **on information and belief with a stated factual basis**. It still does not allege a Home Depot-specific source field, adjudication code, or registry component as known fact.

The supporting research and discovery targets are collected in `FIRST_ADVANTAGE_HOME_DEPOT_PUBLIC_SOURCE_MEMO.md`.

## Maximum-value discovery plan

If the complaint gets through Rule 12, the first discovery should be aimed at converting every information-and-belief allegation into a binary document fact:

1. complete Home Depot applicant/personnel file;
2. actual 2024 disclosure and authorization;
3. full First Advantage report and all versions;
4. order/profile/package metadata;
5. component results and raw source fields;
6. client-specific adjudication matrix;
7. ATS status and reason codes;
8. access and transmission logs;
9. pre-adverse/adverse-action workflow logs;
10. Home Depot–First Advantage contract/SOW and California screening configuration;
11. all communications regarding Plaintiff's screen and hire;
12. First Advantage consumer file and Home Depot user certification.

The central objective is to learn whether the report says, in substance: **California registry source → adverse/decisional result → Home Depot access/use → employment stopped.**

A second high-value target is Plaintiff's actual 2024 Home Depot disclosure/authorization. The *Ford* litigation challenged Home Depot's older standardized form under FCRA § 1681b(b)(2)(A). Do not add that count now, but if Plaintiff's 2024 form is materially similar, audit it for a separate stand-alone disclosure claim and additional willfulness evidence.

## Report-dependent upgrades

If the Home Depot report resembles UPS Exhibit A and expressly states a source such as “CALIFORNIA SEX OFFENDER REGISTRY,” Count 3 becomes materially stronger because the source element is documentary rather than inferential.

If the report also shows:
- ordinary criminal searches clear / eligible;
- registry component alone adverse / decisional;
- a Home Depot client criterion;
- a centralized adjudication or final ineligibility field;

then plead those exact fields and let the report carry causation. Avoid adjectives when the document can do the work.

If the report instead shows ordinary court records as the operative adverse source and no California-registry sourcing, do **not** force the § 290.46 theory. Rebuild around the FCRA / ICRAA process claims and whatever the actual report supports.


## Rule 12(b)(6) engineering — affirmative fact, not conditional theory

The federal complaint now pleads the critical § 290.46 elements as **ultimate facts on information and belief**:

- First Advantage furnished Home Depot Plaintiff's § 290.46 information;
- Home Depot received, accessed, considered, and used that information;
- the use was for a purpose relating to employment; and
- the registry information was a substantial factor in the adverse employment decision.

The complaint does not plead those elements as “possibly true depending on discovery.” Discovery is reserved for the evidentiary details — precise source-field wording, adjudication code, access timestamps, reason codes, and decisionmaker identity.

That distinction matters under *Soo Park v. Thompson*, 851 F.3d 910, 928–29 (9th Cir. 2017): the plausibility standard does not bar information-and-belief pleading where the relevant facts are peculiarly within the defendant's possession and the belief is supported by factual information making the inference plausible.

### Comparator architecture

The complaint now pleads the UPS and FedEx First Advantage screenings as **comparators concerning the same consumer and same CRA**, not as Home Depot's report:

- UPS: First Advantage report concerning Plaintiff during the same general period; ordinary criminal searches non-adverse; sex-offender-registry component adverse/decisional; source expressly identified as California Sex Offender Registry.
- FedEx: separate First Advantage employment screen; FedEx later admitted in its responsive pleading that the report identified Plaintiff as a California registrant.

The underlying California registry entry is employer-invariant. What can vary by employer is the package, configuration, and presentation. Those comparator facts make the allegation that First Advantage's Home Depot screen contained the same California registry information substantially more concrete than a naked inference.

### FCRA injury / Dutta distinction

The FCRA allegations are now tied to the lost employment itself. Plaintiff alleges that if Home Depot had furnished the report and Summary of Rights before adverse action, he could have identified the California-registry source and objected that § 290.46(j)(2)(E) prohibited Home Depot from using that information for the employment decision.

That is designed to distinguish *Dutta v. State Farm*, 895 F.3d 1166 (9th Cir. 2018), where the missing pre-adverse process could not have changed the outcome because an accurate, independently disqualifying credit item remained. Here, the pleaded theory is that the information driving the decision was itself legally prohibited from employment use.

## Pleading repairs in this revision

- **Former chronology paragraph (old ¶49):** no longer states as known fact that “First Advantage reported Plaintiff’s registry information.” The sequence now carries the same I&B qualifier used in Count 3. A contrary sentence was MTD bait.
- **DOT / (b)(3)(B)-(C):** the Tracy site is a warehouse, distribution, and fulfillment DC. The complaint now pleads that the position was not a commercial-driving assignment and that the FCRA driving exception does not apply. Rewrite only if a later Home Depot document shows a DOT-regulated driving job.
- **Count 3 posture:** source and use are pleaded as I&B ultimate facts with comparator support. They are not labeled “[REPORT-CONDITIONED]” in the matter record. Exact source-field wording remains reserved for discovery.
- **Willfulness color:** *Harris v. Home Depot U.S.A., Inc.*, 114 F. Supp. 3d 868 (N.D. Cal. 2015), is pleaded only as additional evidence that Home Depot is a sophisticated FCRA employment-screening user. It is a standalone-disclosure decision. It is **not** a § 1681b(b)(2)(A) claim in this complaint and is not treated as a holding that Home Depot violated § 1681b(b)(3)(A) in Plaintiff’s transaction.

## Pre-filing inspection (highest-value next step)

Unsigned demand drafts:

- `internal/docs/matter-37/INSPECTION_DEMAND_FIRST_ADVANTAGE.md`
- `internal/docs/matter-37/PERSONNEL_FILE_DEMAND_HOME_DEPOT.md`
- generator: `internal/scripts/matter37-inspection-demands.py`

Serve First Advantage at the Ford-form consumer address (P.O. Box 105292, Atlanta, GA 30348). Serve Home Depot at CSC, not 5395 Hopkins Road. Plaintiff signs. Do not treat the drafts as served until they go out.
