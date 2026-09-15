# Matter 39 — E.D. Cal. Federal Redraft Notes

## Objective

Replace the never-filed September 8, 2026 San Joaquin packet with a federal-first review draft engineered for a direct filing in the U.S. District Court for the Eastern District of California, Sacramento Division.

The state packet remains historical work product only. It was never clerk-filed.

Do **not** stamp this matter LOCKED. The live draft is `internal/scripts/matter39-edca-complaint.py`. Keep editing until Plaintiff signs and files.

## Recommended claim architecture

### Count 1 — FCRA § 1681b(b)(3)(A), Best Buy

This is the federal-question anchor.

The theory is deliberately narrow: Best Buy procured a First Advantage consumer report for employment purposes and took adverse action based in whole or in part on it without first giving Plaintiff (1) the report and (2) the written Summary of Rights.

Vendor identity is documentary, not a public-source inference. Best Buy's own October 17, 2023 authorization named First Advantage Consumer Center, and First Advantage ordered a Best Buy drug test the same afternoon (Q09078711; account BEST BUY 11759586). The transaction-specific report remains necessary to prove what the screen contained.

### Count 2 — ICRAA §§ 1786.40 / 1786.50, Best Buy

Use ICRAA for a **different omission** from Count 1: when employment was denied under circumstances in which an investigative report had been obtained, Best Buy failed to advise Plaintiff and supply the CRA's name and address **at adverse action**.

Naming First Advantage on the earlier authorization is not the § 1786.40 advice. Civil Code § 1786.52(a) bars an ICRAA § 1786.50 suit for the **same act or omission** already the subject of an FCRA §§ 1681n / 1681o action. Do **not** add FCRA § 1681m(a).

### Count 3 — Penal Code § 290.46(j), Best Buy

Source and use are **ultimate facts on information and belief**, with UPS/FedEx same-consumer First Advantage comparators as additional factual basis. Best Buy's own file already supplies the written offer, named vendor, same-day screen, and ghost. Do not attach a UPS or FedEx report as Best Buy's report.

**Count 3 does not use May 29.** It is timely under CCP § 338(a) from the October 2023 *use*. Three years from October 17, 2023 is **October 17, 2026**. That is the filing-critical clock on this count. Count 3 realleges ¶¶ 1–43 and 48–55 only — **not** ¶¶ 44–47.

## Claims intentionally omitted

- **UCL § 17200:** omitted. Federal standing/remedy side fight; limited upside.
- **CCRAA:** omitted unless the Best Buy product is an ordinary consumer credit report.
- **Tameny / IIED / contract / estoppel:** omitted. A two-year CCP § 335.1 clock from an October 2023 decision closed in October 2025.
- **FEHA / Fair Chance Act:** no CRD right-to-sue in the record.
- **FCRA § 1681b(b)(2)(A):** reserved. California disclosure PDFs were attached to the offer sequence but are not in this upload. Audit them if they arrive; do not plead a standalone-disclosure count without the form.
- **FCRA § 1681m(a):** omitted to avoid § 1786.52(a) overlap with ICRAA § 1786.40.
- **First Advantage as a defendant:** not yet. Add only if Best Buy-specific records support an independent CRA violation.
- **Prospective injunction / § 290.46(j)(4)(B):** omitted from the opening complaint.
- **DOES / Best Buy Stores, L.P.:** omitted from the opening federal caption. If the report or personnel file shows a different employing affiliate, fix the defendant before filing.

## The filing-critical limitations section

May 29, 2026 is pleaded **only for Counts One and Two** (FCRA and ICRAA). Do not name other cases in the complaint.

Count Three does **not** reallege paragraphs 44–47 and does **not** use May 29.

For Counts One and Two, May 29 is **not** “the day Plaintiff knew he had been harmed.” He knew he had lost the Tracy job in October 2023. May 29, 2026 is the date he first understood that Best Buy had obtained a consumer / investigative report and had skipped the FCRA pre-adverse package and the ICRAA § 1786.40 advice.

Do **not** plead that Plaintiff first learned First Advantage's identity on May 29. Best Buy named First Advantage on October 17, 2023. That fact stays in the chronology. Delayed discovery is of the *process omissions*, not of the vendor's name.

Do not write “I learned of the law” as a standalone theory.

Internal provenance (keep out of the complaint): May 29, 2026 is the Pilot filing date. If asked at deposition what happened that day, the truthful answer is that this is when Plaintiff first pursued the employment-screening statutory theory. Do not deny that. Do not volunteer other captions in the Best Buy pleading.

If Plaintiff actually understood the FCRA/ICRAA omissions earlier while drafting, use that earlier date for Counts One and Two.

Best Buy will argue inquiry notice from the October 2023 ghosting **and** from having named First Advantage on day one. That is a stronger inquiry-notice defense than Home Depot. It is a defense. It is not a reason to volunteer October 2023 as FCRA/ICRAA discovery.

FCRA § 1681p: earlier of two years from discovery or five years from the violation. Two years from May 29, 2026 runs to May 29, 2028. Five years from an October 17, 2023 violation runs to approximately October 17, 2028. ICRAA § 1786.52 is two years from knew or should have known.

Count 3: CCP § 338(a) three years from the use. If accrual is the October 17, 2023 offer / same-day screen week, the outer bound is **October 17, 2026**. File Count 3 before that date. Do not try to save Count 3 with May 29.

## E.D. Cal. engineering

- Federal question: 28 U.S.C. § 1331 + FCRA.
- Diversity in the alternative: 28 U.S.C. § 1332(a) — Minnesota corporation, Richfield principal place of business, California plaintiff. Amount in controversy aggregates the offered $22.60 hourly rate according to proof plus statutory remedies. Do not invent hours or a start date. The offer states neither.
- Supplemental jurisdiction: 28 U.S.C. § 1367(a).
- Venue: 28 U.S.C. § 1391(b)(2).
- San Joaquin County places the action in the Sacramento side of E.D. Cal. under Local Rule 120(d).
- Serve the current California SOS agent, not 6653 Hopkins Road. Public records in other jurisdictions and an older Prop 65 notice use C T Corporation System. Confirm the SOS listing immediately before service. Do not invent CSC. Do not serve Jose Tapia's phone number.
- Complaint is intentionally unverified. Rule 11 supplies the federal certification.
- Arbitration: the October 13, 2023 application email recites an arbitration policy. The policy PDF is not in this upload. Best Buy will move to compel. That is a defense, not a claim. Do not volunteer a waiver in the complaint.
- Generate the review-draft PDF with `python3 internal/scripts/matter39-edca-complaint.py`. Use official JS-44 / AO-440 / AO-239 forms; do not homemade them.

## Maximum-value discovery plan

1. complete Best Buy applicant/personnel file;
2. actual October 17, 2023 disclosure and authorization PDFs;
3. full First Advantage report and all versions;
4. order/profile/package metadata, including Q09078711 / account 11759586;
5. component results and raw source fields;
6. client-specific adjudication matrix;
7. ATS status and reason codes;
8. access and transmission logs;
9. pre-adverse/adverse-action workflow logs;
10. Best Buy–First Advantage contract/SOW and California screening configuration;
11. all communications regarding Plaintiff's screen and hire, including Jose Tapia and Daisy Calvary;
12. First Advantage consumer file and Best Buy user certification.

If the Best Buy report shows ordinary court records as the operative adverse source and no California-registry sourcing, do **not** force the § 290.46 theory.

## Pre-filing inspection (highest-value next step)

Unsigned demand drafts:

- `internal/docs/matter-39/INSPECTION_DEMAND_FIRST_ADVANTAGE.md`
- `internal/docs/matter-39/PERSONNEL_FILE_DEMAND_BEST_BUY.md`
- generator: `internal/scripts/matter39-inspection-demands.py`

Serve First Advantage at the address Best Buy itself used: P.O. Box 105292, Atlanta, GA 30348. Serve Best Buy through the current SOS agent, not 6653 Hopkins Road. Plaintiff signs. Do not treat the drafts as served until they go out.
