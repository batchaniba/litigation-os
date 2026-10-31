# Matter 26: First Amended Complaint (draft)

*Newanforbi v. United Parcel Service, Inc.*, USDC E.D. Cal. No. 2:26-cv-02847-DAD-CKD.

**Status:** draft for Plaintiff's review. Nothing has been filed, served, or sent.

## Files

| File | What it is |
|---|---|
| `matter26_ups_fac.py` | FAC source: the full pleading text plus the build. |
| `First Amended Complaint - Newanforbi v UPS (E.D. Cal. 2-26-cv-02847) DRAFT (Oct 31 2026).pdf` | Formatted output, 38 pages: 24 pages of pleading, then Exhibit 1 and Exhibit 2, each behind a cover sheet. |
| `README.md` | This file. |

## Formatter used

- **Pleading paper:** `internal/scripts/lib/pleading_paper.py` (`PleadingPaper`). This is the portfolio's shared pleading-paper engine: 28 numbered lines, ruled margins, page footer. It is the same engine `internal/scripts/matter26-opposition-to-mtd.py` used for Dkt 10.
- **Signature:** `internal/scripts/signature_stamp.py` (`SIGNATURE_PATH`, `SIGNATURE_NATIVE_PX`). This stamps the canonical image `internal/assets/signature/brendan-newanforbi-signature.png`. No typed `/s/` is used.
- **Exhibit covers:** `internal/scripts/lib/exhibit_cover.py`.
- **PDF assembly:** `internal/scripts/lib/pdf_packet.py`.

To regenerate the PDF:

```bash
python3 internal/private/research/matter-26-fac-draft/matter26_ups_fac.py
```

The only blank in the draft is the signature date (`Dated: ____`).

## What changed from the original Complaint, and why

| Original | FAC | Why |
|---|---|---|
| Count I, § 290.46. ¶12 called the statute "categorical." ¶13 and the prayer misquoted the remedy as "greater of actual damages or $25,000." | **Count I** quotes § 290.46(j)(1)–(4) verbatim. It pleads the source-to-use chain element by element: Exhibit A's "SOURCE OF RECORD: CALIFORNIA SEX OFFENDER REGISTRY"; NSOPW real-time search of state sites (DOJ fact sheet); the "Decisional"/"INELIGIBLE" scoring; the July 21 cancellation; and UPS's admissions of use. It negates (j)(1) and § 432.7(n) with facts. | Cures Dkt 7 § IV.B and Dkt 14 §§ II.A–B. Fixes the remedy misquotation flagged by both reviews. |
| No injunctive count apart from the UCL. | **Count II**, § 290.46(j)(4)(B): preventive relief against a pattern or practice. | Statutory injunction vehicle. Avoids the UCL standing, *Korea Supply*, and *Sonner* problems. |
| Count III, ICRAA. ¶46 relied on the statute's "spirit and purpose." ¶47 was a "one or more of the following" list. ¶19 conceded the notices were compliant. ¶48 misstated § 1786.50. | **Count III**, § 1786.16(b)(1): no box to request a copy. UPS's own screen says "by checking the box beneath your signature," and there is no box. **Count IV**, § 1786.16(a)(2)(B): the disclosure is not standalone, gives no nature-and-scope notice, and gives no privacy-practices notice. ¶19 is deleted. § 1786.50(a)–(b) is quoted verbatim. | Cures Dkt 7 § IV.C.ii and Dkt 14 § II.C. |
| Count II, *Tameny* failure to hire | Dropped | *Williams v. Sacramento River Cats*; conceded in Dkt 10. |
| Count IV, constitutional privacy | Dropped | Public registry data plus signed consent. Both reviews rate it weak. |
| Count V, negligence per se | Dropped | Doctrine, not a cause of action; conceded in Dkt 10. |
| Count VI, UCL | Dropped | No restitution of unearned wages (*Korea Supply*). Thin standing for an injunction. Count II now supplies injunctive relief. |
| ¶5: Delaware corporation | Ohio corporation with its principal place of business in Atlanta | UPS's Notice of Removal and its arbitration agreement say Ohio. |
| ¶22: on information and belief, the report carried a § 290.46 warning | Deleted | Exhibit A shows no such warning. |
| State-court jurisdiction and venue | 28 U.S.C. §§ 1332(a), 1441(a), 1391(b)(2) | Federal posture after removal. |

**Waiver note.** Claims left out of an amended pleading are generally treated as abandoned. If you want to preserve the UCL or privacy count for appeal or for leverage, add it back before filing.

## Deviations from the instructions (read first)

1. **Court header and case number.** The original Complaint's caption reads "SUPERIOR COURT OF THE STATE OF CALIFORNIA, COUNTY OF SAN JOAQUIN," with a blank case number. Since removal, the action exists only in E.D. Cal. A FAC with the state header and no number could not be filed. The draft therefore uses "UNITED STATES DISTRICT COURT / EASTERN DISTRICT OF CALIFORNIA" and **Case No. 2:26-cv-02847-DAD-CKD** (from `matter.json` and every docketed paper).
   - The **party caption** is copied exactly from the original: "BRENDAN NGEHSI NEWANFORBI, Plaintiff, v. UNITED PARCEL SERVICE, INC., and DOES 1 through 10, inclusive, Defendants."
   - The **plaintiff name and address block** is also exact, including "Plaintiff, In Pro Per."
2. **E-mail line: confirm before filing.** The original Complaint reads `bnn.cdla@gmail.com`, and the draft copies it exactly. The rest of the portfolio record (the opposition script, the settlement-demand events, the Claude review) treats **`bnn.cdl@gmail.com`** as correct and `cdla` as UPS's misspelling. If `cdl` is right, change one line (`PLAINTIFF_BLOCK`) and regenerate.
3. **No verification page.** The original was verified. A FAC in federal court does not need to be (Fed. R. Civ. P. 11 signature only), and a verification turns every "on information and belief" allegation into sworn testimony. You can add one if you want it.

## Flagged / unverified items

### Bracketed in the FAC text

| # | Item | Where | Status |
|---|---|---|---|
| 1 | `[E.D. Cal. L.R. 220]`: amended pleading must be complete in itself | ¶3 | Local rule text not fetched this session. |
| 2 | `[E.D. Cal. L.R. 120(d)]`: Sacramento Division assignment | ¶8 | Not fetched. |
| 3 | *Mendoza v. ADP Screening & Selection Services, Inc.* (2010) 182 Cal.App.4th 1644 `[pin cites unverified]` | ¶17 | Both quotations match a law-firm summary (AALRR). The reporter citation comes from a secondary source (Proskauer). Pull the opinion and add pins. No negative treatment found, but none was checked on a citator. |
| 4 | Gov. Code § 12952 `[statute text not verified for this draft]` | ¶53 | Statute not fetched. The FAC does not quote it. |
| 5 | Civ. Code § 1786.2(c) `[definition not verified for this draft]` | ¶71 | Definition of "investigative consumer report" not fetched. ¶71 also rests on UPS's own disclosure, which calls the report an ICRAA "investigative consumer report." |
| 6 | *Gilberg v. California Check Cashing Stores, LLC*, 913 F.3d 1169 (9th Cir. 2019) `[pin cite unverified]` | ¶80(a) | Existence and holding confirmed only through law-firm summaries: a combined disclosure violates both the FCRA and ICRAA standalone rules. Read the opinion before relying on it. |

### Cited without brackets but not fetched this session

These are standard, but they were not independently pulled:

- 28 U.S.C. §§ 1332(a), 1391(b)(2), 1441(a)
- Fed. R. Civ. P. 38(b)
- 15 U.S.C. §§ 1681n, 1681o (cited only to disclaim an FCRA claim)

### Verified this session

**Statutes.** Verbatim from california.public.law reproductions of leginfo, updated through 2022:

- Penal Code § 290.46(a)(1), (j)(1), (j)(2), (j)(3), (j)(4)(A), (j)(4)(B). Note that (j)(3) lists **Family Code § 8808**, not "Civil Code § 226.55."
- Labor Code § 432.7(n)
- Labor Code § 1024.5(a)
- Civil Code § 1786.16(a)(2)(A)–(C) and (b)(1)–(2)
- Civil Code § 1786.40(a)
- Civil Code § 1786.50(a)–(b)
- Civil Code § 1786.52

**DOJ SMART Office, "NSOPW vs NSOR" fact sheet.** Text was extracted from the official PDF at smart.ojp.gov/nsopw-nsor-fact-sheet. All four quotations in ¶¶18–20 match it.

**Record quotations.** Every quoted record phrase was checked against the filed exhibits (ECF No. 7-2, pp. 4–9, 11, 16–18, 23–24) and the briefs (Dkt 7 Part IV; Dkt 14 Part II.A).

### Facts you must confirm before signing (Rule 11)

These are not blanks. The draft pleads them, but they are outside the documents.

1. **¶58 and all of Count II.** That you continue to seek warehouse and package-handling work in the Stockton–Lathrop area and *would apply again* to UPS. Article III standing for an injunction depends on this. If it is not true, delete the last two sentences of ¶58 and Count II, and drop prayer item 2.
2. **¶42.** That in July 2024 your information was displayed on the California Megan's Law website, as opposed to being excluded under § 290.46(e). This is the linchpin of Count I. If you were excluded, NSOPW could not have returned you, and the provenance theory needs rethinking.
3. **¶25.** The position involved in-hub package handling only: no home entry, no residential delivery, no at-risk persons. This is pleaded on information and belief.
4. **¶32.** UPS never sent you a copy of the report itself. The only access was the expiring First Advantage portal link.
5. **¶46.** Reminder e-mails on July 23 and July 27, 2024. This comes from `matter.json` `key_facts`.
6. **¶4.** The name variants in UPS's records all refer to you.

## Procedural posture and deadlines

- **Leave is required.** The Rule 15(a)(1)(B) window closed in September (`clocks.json` `26-deadline-2`, satisfied/retired). The FAC can be filed only:
  - with UPS's written consent;
  - by leave of court under Fed. R. Civ. P. 15(a)(2); or
  - by the deadline set in an order or F&R on the motion to dismiss that grants leave.

  If you move for leave now, attach this draft as the proposed amended pleading `[E.D. Cal. L.R. 137(c), unverified]`.
- **The motion to dismiss is under submission without a hearing** (Sep. 24, 2026 minute order, Dkt 15). If a magistrate judge issues Findings & Recommendations, objections are due **14 days after service** (28 U.S.C. § 636(b)(1); Fed. R. Civ. P. 72(b)(2)), plus 3 days if served by mail (Fed. R. Civ. P. 6(d)). This deadline comes from the Claude review and was not re-verified here. Calendar it from the actual service date.
- **Docket-number mismatch.** `matter.json` says the live motion is Dkt 9, while the repo files label it Dkt 07. The FAC cites the briefs by name and part, not by ECF number. Exhibits cite ECF No. 7-2 as stamped on the filed pages.

## Strategy notes (not in the pleading)

- **Copy-delivery theory not pleaded.** The report was completed Thursday, July 18. The July 22 portal link may fall within three business days (Fri 19, Mon 22, Tue 23). The FAC pleads only the missing-box violation, which does not depend on timing.
- **§ 1786.40 adverse-action content not pleaded.** The notices' contents are unknown because the portal expired. Add this only if you recover the notices.
- **Possible FCRA claim (not pleaded).** UPS cancelled the July 22 "Hired Date" at 3:59 a.m. on July 21, before the pre-adverse notice. That could support a 15 U.S.C. § 1681b(b)(3)(A) claim.
  - It would probably relate back to the July 15, 2026 complaint under Fed. R. Civ. P. 15(c)(1)(B). The limitations period under 15 U.S.C. § 1681p is `[unverified]`.
  - Risks: UPS will argue the cancellation was not "adverse action." Civ. Code § 1786.52 (verified) bars ICRAA suit for the *same act or omission* while an FCRA action is pending. Keep any FCRA claim tied to different acts.
  - ¶83 currently disclaims any FCRA claim. Decide before filing.
- **Arbitration.** The arbitration-agreement pages of UPS's Exhibit B (version dated 11.3.2025) are deliberately **not** attached. The disability-questionnaire page (ECF 7-2 p. 22) is also left out.
- **Limitations exposure** UPS may raise:
  - Code Civ. Proc. § 340(a) one-year period against the § 290.46 civil-penalty component `[unverified]`.
  - The ICRAA limitations period `[unverified]`.
  - Relation back to the July 15, 2026 filing under Rule 15(c)(1)(B) is the answer to both. Every FAC count arises from the conduct pleaded in the original.
- **Apodictic / verification-foundation.** Your standing instruction is to stress-test before filing. Recommended next step: run `verification-foundation:opposing-counsel-attack-en` and `apodictic:audit` on Count I and Counts III–IV.
