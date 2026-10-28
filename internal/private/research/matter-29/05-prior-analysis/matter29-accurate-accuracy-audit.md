# Matter 29 — Accurate Background Consumer Report: Accuracy Audit
Subject: Brendan Ngehsi Newanforbi (a/k/a Brendan Ngwa Nforbi) · Accurate ref 496623722 · Requestor "Amazon HVH" (Fremont, Alameda Co., CA) · ordered 07/07/2026, "updated on" 10/14/2026
Prepared 10/14/2026 (PT). Working draft for the user. Nothing has been sent. This is not legal advice; everything here comes from the documents unless marked as inference.

## 1. Sources and dedupe

Citation key: **CR** = Consumer Report (15 pp.). Portal `Consumer Report-1792008058162.pdf`; repo copy `Accurate Background - Consumer Report (... updated Oct 14 2026).pdf`.

| Group | Portal files | Result |
|---|---|---|
| FCRA Summary of Rights | -124675, -162564, -193219 | Same size (171,526 B). The md5 differs only because the embedded IDs/timestamps differ; the **text is identical**. Duplicate of the repo copy. |
| CA ICRA Notice of Rights | -177907, -208387 | Text identical. Duplicate of the repo copy. |
| Notice re Background Checks (CA) | -096536, -208484, -225302, -244265 | Text identical. Duplicate of the repo copy. |
| Subject Notification | -081279, -109321, -149535, -169534 | Text identical. Duplicate of the repo cover letter. |
| **Subject Notification variant** | **-190268** | **Different template** (44,992 B vs 100,345 B). See §1a. NEW. |
| **Notification under FCRA** | **-239478** | 15 U.S.C. 1681k(a)(1) "may be reporting public record information" notice to the consumer. NEW. |
| Consumer Report | -058162 | **Text identical** to the repo copy (22,380 chars). The bytes differ because the PDF is regenerated on every download (CreationDate repo 12:31:17, portal 13:00:58, both stamped "-08'00'", which is the wrong offset for PDT). The content was not edited between those two downloads. |

User attachments:
- `8a5983…pdf`: Gmail print of the email "Your Copy of Your Consumer Report from Accurate Background", from noreply@accurate.com to brendan@ngwanforbi.com, Wed 10/14/2026 11:58 AM PT. Its body matches the variant -190268 word for word. NEW.
- `932f84…pdf`: Gmail print of the email "Important FCRA notice about your Consumer Report", from noreply@accurate.com, 10/14/2026 11:58 AM PT (2 pp.). Its body matches -239478. NEW.
- `5fb68c…pdf`: Safari print of the MyPortal Documents page, 12:30 PM PT. **Byte-identical** (md5 6bd6f0e8…) to the repo "Portal Documents Page Screenshot". Duplicate.

### 1a. Standard vs variant Subject Notification
| | Standard (-081279 etc.) | Variant (-190268 = 11:58 email) |
|---|---|---|
| Describes | "background screening report request" | "consumer report request" |
| Dispute contact | customer_service@accurate.com | disputes@accuratebackground.com |
| "Accurate Background does not make employment decisions … contact Amazon Salesforce" | present | **absent** |
| Signature | "Regards, Accurate Background" | **"Regards, Amazon Salesforce"** |
| Confidentiality / Privacy footer | present | absent |
Both versions have the same portal link, list the same 4 enclosures, and use the same address and phone. The variant is an Accurate-generated letter that is signed in the employer's name. Read alone, it misstates who sent it. Both versions sit on the same 10/14 portal, which points to two templates (one emailed, one stored). Neither version is evidence that the report itself was edited.

## 2. Line-by-line audit of the Consumer Report

Flags: INACC = inaccurate · INCOMP = incomplete · MISL = misleading · UNVER = unverifiable from the documents · INCONS = inconsistent across documents. "Proof needed" names the record that would settle the point.

| # | Statement as reported (CR page) | Flag | Analysis | Proof needed |
|---|---|---|---|---|
| 1 | Name "Ngwa Nforbi, Brendan Ngehsi" (p1-2) | OK/INCONS | The notices address him as "Brendan Ngwa Nforbi" with no middle name. The legal name is Newanforbi. Minor. | Name-change order / ID |
| 2 | AKA "NFORBI, BRENDAN" — Provided by Applicant (p2) | UNVER | It may have come from his application. | Application data |
| 3 | **AKA "NGWA NFORBI, NEWANSORBI" — Provided by Applicant (p2)**; used as a searched name in every search (p4, 6-9, 11) | INACC/MISL (user states he never supplied it) | "NEWANSORBI" is a garbled form of the surname placed in the *first-name* field. No real person by that name is evident. Labeling it "Provided by Applicant" assigns the error to him. This is the only AKA that is both garbled and attributed to him. | His actual application/intake record from Amazon/Accurate (not produced); Accurate's data-entry audit trail |
| 4 | AKA "NEWANFORBI, BRENDAN" — Discovered through Address History (p2) | INCOMP | This is his correct legal name, yet it is labeled as "discovered." The address-history results that produced it are not disclosed (p9 says only "COMPLETED"). | Full file disclosure (1681g(a)(1)/(2); Civ. Code 1786.10) |
| 5 | DOB 09/16/xxxx; SSN xxx-xx-1726; phone +12098014442; 1455 Cat Tail Dr, Stockton CA 95204; email (p2) | User to confirm | Partials only. Nothing on the face of the document is wrong. | User confirmation |
| 6 | Requestor "Amazon HVH", REF "ad188d7ed256-40f1-b7f0-e2a7f77aa061", "General Package" (p2) | INCONS | Every notice names "Amazon Salesforce, PO Box 81226, Seattle". The REF has a 12-4-4-12 pattern, so it is not a well-formed UUID (8-4-4-4-12) and looks truncated. Minor. | Accurate's end-user certification / order record |
| 7 | Position location Fremont, Alameda, CA (p2, p14) | OK | Confirms ICRAA (Civ. Code 1786) applies. | — |
| 8 | Santa Clara County Criminal: RECORD FOUND; search 496644204; **completion 2026-10-14** (p3-4) | Timing anomaly | Ordered 07/07, completed 10/14 = **99 days**. Every other search finished 07/07-07/10, except San Joaquin (09/03, 58 days). **Package Review completed 2026-10-13 (p9), one day *before* the Santa Clara result was completed.** | Accurate's search-vendor log / court-runner timestamps |
| 9 | Case C1761642, filing date 10/25/2017 (p4) | UNVER | It may be correct. The report gives no court-record retrieval date, source, or identifiers matched (DOB/SSN/booking no.). Only names are shown as "searched." | Santa Clara Superior Court docket / register of actions |
| 10 | **Count 1 "Sexual penetration – by force…", FELONY, NO CONTEST; Charge Disposition Date 10/25/2017** (p4-5) | **INACC (likely) / MISL** | The disposition date is the **same day as the filing date**. A no-contest plea and conviction on the day the case was filed is facially implausible. The sentence gives "317 days prison credited", which suggests custody of about 10 months before sentencing (inference: disposition around late 2018). No statute section is given (e.g., PC 289(a)(1)). No conviction or sentencing date is given. | Docket, minute order of plea and sentence, abstract of judgment |
| 11 | Count 1 sentence: "6 YEAR(S) PRISON; 317 DAY(S) PRISON CREDITED; TO BE SERVED CONCURRENT"; costs $140; restitution $300 (p5) | UNVER/MISL | "Concurrent" with what is not stated. | Abstract of judgment |
| 12 | **"12/02/2020 – RELEASE DATE – RELEASED FROM PRISON ONTO PAROLE; CURRENTLY ON PAROLE"** (p5, repeated p6 for Count 2) | **INACC if he has been discharged; stale/MISL in any case** | The report states parole status *as of 10/14/2026*, almost 6 years after release. No source or verification date is given for "currently". The data comes from a court index, which normally does not track live parole status. The 7-year ICRAA window (1786.18(a)(7)) runs from release or parole, so this status line determines how the record is weighed. | **CDCR parole discharge certificate / CDCR letter with discharge date** (strongest dispute if he holds one) |
| 13 | Count 2 "Assault with intent to commit felony", FELONY, NO CONTEST; disposition date 10/25/2017 (p5) | Same as #10 | Same disposition date problem as Count 1. | Docket |
| 14 | Count 2 sentence "4 YEAR(S) PRISON; ; TO BE SERVED CONCURRENT"; costs $140; restitution $300 (p5-6) | INCOMP/MISL | The credit field is blank. Listing the same $140/$300 under both counts makes them look like separate assessments (possible double-count). | Abstract of judgment / minute order |
| 15 | Dismissed / non-conviction counts | Nothing reported | No dismissed counts appear. If the case had other counts, leaving them out is correct (1786.18(a)(7) bars reporting non-convictions). Not a dispute item unless the docket shows one of the two listed counts was dismissed or reduced. | Docket |
| 16 | San Joaquin County: NO RECORD; 2026-09-03 (p3) | Timing | 58 days. Completed three days after the Aug 31, 2026 removal of Matter 29 (context only, not evidence of intent). | Vendor log |
| 17 | Sheridan WY (07/10), Fed. E.D./N.D. Cal., S.D.N.Y., D. Wyo., NY statewide, NSOPW, Global Watch, National DB: no record / completed 07/07 (p6-11) | OK | These favor him. Note that the national DB and NSOPW show no record for the same person. | — |
| 18 | SSN trace / address history: "COMPLETED" with no content (p9) | INCOMP | No address results are given, even though they were the basis for item #4 and for picking jurisdictions. | 1681g full file |
| 19 | **"PREVIOUS CONVICTION QUESTION: NO"; "ANSWER: No"** (p11, p14) | UNVER / possibly MISL | The report attributes a "No" answer to him on a 7-year question that, given a 12/02/2020 release, would call for "Yes" (Fremont is not unincorporated L.A. County or Philadelphia). Next to the "CURRENTLY ON PAROLE" line, this reads as an implied falsehood. **This item cuts both ways.** If he in fact answered "No", disputing it is risky. If he did not, or the answer was system-defaulted, it is a strong inaccuracy. | His actual submitted application answers and timestamp (not in the documents) |
| 20 | "ordered on 07/07/2026 / updated on 10/14/2026" (p1) | INCOMP | The report was "updated". Any earlier version furnished to Amazon is not in the file. | All versions furnished, and the dates (1681g(a)(3); 1786.10) |
| 21 | ICRAA notice: "The written notice can be found at **[LINK]**" / "**[ENLACE]**" (p1) | Notice defect | This is an unfilled template placeholder in the 1786.29/1786.26 required notice, so the notice is not actually given. | Face of document |
| 22 | Electronic Subject Notification and "– CRA" completed 2026-10-14 (p10); 1681k notice and emails 10/14 11:58 AM | Timing | The notices went out on the day the Santa Clara record completed. That is consistent with 1681k(a)(1) "at the time", but they came 99 days after the order. The notices are undated on their face. | — |

## 3. What the documents prove vs what needs outside records
**Proven on the face of the documents:** the [LINK]/[ENLACE] placeholder; the disposition date equals the filing date; "currently on parole" is asserted in 2026 with no source or verification date; "NEWANSORBI" is labeled "Provided by Applicant"; address-history results are absent; the 99-day Santa Clara delay; package review dated 10/13, before the record completed on 10/14; the requestor name is inconsistent (HVH vs Salesforce); two Subject Notification templates exist, one signed "Amazon Salesforce"; the Consumer Report text did not change between the two 10/14 downloads.
**Requires outside records:** whether parole was discharged (CDCR); the true plea/conviction/sentencing dates and statutes (Santa Clara docket, abstract of judgment); whether he ever supplied "NEWANSORBI" or answered "No" (application record); the earlier report version(s).
**Intent:** the documents do not prove intent. At most they show a pattern consistent with lack of reasonable procedures (1681e(b)/1786.20(b)): unfilled templates, an unsourced live-status claim, a garbled alias attributed to the applicant, and review completed before the record was. A willfulness theory would need the outside records plus Accurate's audit log.

## 4. Missing documents to request (1681g / Civ. Code 1786.10-1786.11)
1. Signed stand-alone FCRA disclosure and authorization (1681b(b)(2)) and the ICRAA disclosure and the box to request a copy (1786.16).
2. His actual application/intake data: names entered, AKAs, and the conviction-question answer with timestamp.
3. Full address-history / SSN-trace results.
4. Source, retrieval date, researcher, and identifiers matched for C1761642, and the source/date of "currently on parole".
5. Every version of the report and the date each was furnished to Amazon (recipients list, 1681g(a)(3)).
6. Package-review notes from 10/13/2026.
7. The 1786.29 notice that [LINK] should have pointed to.

## 5. Draft dispute items (ranked)
1. **Parole status "CURRENTLY ON PAROLE"** (CR p5, p6). *Why:* it is stale or inaccurate as of 10/14/2026, with no source or verification date (if he was discharged). *Correction:* delete it, or replace it with the verified discharge date. *Proof:* CDCR discharge certificate or letter.
2. **Charge disposition date 10/25/2017 for Counts 1-2** (CR p4-5). *Why:* it equals the filing date and is inconsistent with 317 days of credit. *Correction:* report the actual plea/conviction and sentencing dates from the court record, or remove the date. *Proof:* certified docket / minute orders / abstract of judgment.
3. **AKA "NGWA NFORBI, NEWANSORBI — Provided by Applicant"** (CR p2; searched p4-11). *Why:* not a name he uses or provided, and it is garbled. *Correction:* delete it and remove the "Provided by Applicant" attribution. Produce the intake record. *Proof:* his application submission; his sworn statement.
4. **Conviction-question answer "No"** (CR p11, p14). Dispute **only if** he did not give that answer. *Correction:* report his actual answer or remove the item. *Proof:* application record / screenshots.
5. **Sentencing detail for Count 2 and the duplicated costs/restitution** (CR p5-6). *Why:* blank credit field; the $140/$300 may be one assessment shown twice. *Correction:* conform to the abstract of judgment. *Proof:* abstract of judgment.
6. **Incomplete file: address-history results, sources, prior versions, recipients** (CR p1, p2, p9). *Correction:* a complete 1681g/1786.10 disclosure. *Proof:* none needed; this is a request.
7. **ICRAA notice placeholder [LINK]/[ENLACE]** (CR p1) and the variant cover letter signed "Amazon Salesforce" (Subject Notification -190268; 11:58 email). *Correction:* issue a compliant notice and clarify who sent the letter. *Proof:* the face of the documents.
8. **Requestor identity HVH vs Salesforce / malformed REF** (CR p2 vs notices). *Correction:* identify the actual end user. Low priority.
9. **Matching identifiers for C1761642** (CR p4). Ask which identifiers matched (only names are shown as searched). Include this only if he disputes that the record is his. Otherwise omit it.

---
## 6. Cross-CRA comparison (added 10/14/2026, 1:40 PM PT)

### 6a. Inventory of non-Accurate background reports
| # | CRA / user | Date | Location | Status |
|---|---|---|---|---|
| R1 | Checkr / Pilot Travel Centers (Report 43f3d4df…) | completed 12/23/2025 | `documents/matter-22/Checkr Consumer Report - Pilot Travel Centers (Dec 23 2025).pdf` (R2/D1; Worker returns 404, so it is not public) | in corpus; **byte-identical to attachment 76d27191…** |
| R2 | HireRight / Macy's (OR-052826-TD9W3) | portal print 5/30/2026; incomplete ("Pending"/"Waiting for reply") | `documents/matter-23/HireRight Report to Macy's … Subject- C 2.pdf` (R2 only, not public) | in corpus |
| R3 | First Advantage / UPS | ordered 7/17/2024, completed 7/18/2024 (printed 8/5/2026) | `documents/matter-26/Dkt 07 Exhibit A - First Advantage Background Report (Filed Aug 26 2026).pdf` (public) | in corpus |
| R4 | InfoMart / Randstad–RK Logistics (Order 15780719) | **ordered 7/7/2026** (the same day as Accurate), reported/decided 7/13/2026 | `documents/matter-27/15780719Final_Profile.PDF` (R2) | in corpus |
| R5 | First Advantage / TaskUs (WPS-361214148) | 9/27/2026 | manifest path `documents/matter-40/First Advantage Consumer Report - TaskUs Background Screening (Sep 27 2026).pdf` | **The bytes are missing from R2, from every git branch, and from D1 FTS. It could not be reviewed.** Matter-40 events describe it as a CA-registry-sourced report. |
| R6 | **Checkr / Next Chapter Project (2998b72e…)** | completed 3/27/2026 | attachment bebf538d… → **newly saved** to matter-29 | **not previously in corpus** |
| R7 | **Checkr / Next Chapter Project (d1eb77b8…)** | completed 8/7/2026 | attachment 6472486f… → **newly saved** | **not previously in corpus** |
| R8 | **Checkr / Nuro (fdd27d50…)** | created 9/22, completed 10/6/2026 | attachment 49fd1b2e… → **newly saved** | **not previously in corpus** |
The user's list of five is therefore correct as far as it goes, but there are **three more Checkr reports** (R6-R8). FedEx (Matter 25) has only pre-adverse/adverse notices and pleadings about a First Advantage report, not the report itself. No Staples report was found in the corpus. None of the four attachments is a duplicate of another attachment. All have different hashes; only 76d2… duplicates an existing corpus file.

### 6b. Comparison table: identity and Santa Clara / C1761642
| Field | Accurate (CR) | Checkr R1/R6/R7/R8 | HireRight R2 | FADV/UPS R3 | InfoMart R4 |
|---|---|---|---|---|---|
| Name searched | Ngwa Nforbi, Brendan Ngehsi; NFORBI; NEWANFORBI; **NGWA NFORBI, NEWANSORBI** (p2, p4-11) | "Brendan (Ngehsi) Ngwa Nforbi" (R1/R6/R7 p2); "Ngwanforbi" (R8 p2) | Nforbi, Brendan Ngwa; Ngwa Nforbi, Brendan; Ngwa, Brendan (p6-7) | BRENDAN NGWANFORBI; developed NGWA-NFORBI, BRENDAN NGEHSI / NFORBI BRENDAN NGWA (p5-6) | Brendan N Ngwa Nforbi; **Alias: "-"** (p12) |
| NEWANSORBI anywhere? | **Yes, "Provided by Applicant"** | No | No | No | No |
| DOB | 09/16/xxxx | Sep 16 (1996 on registry hit) | masked | not shown | 09/16/XXXX |
| SSN | -1726 | -1726 | -1726 (issued NV 2010-11, p7) | not shown | -1726 |
| Addresses | 1455 Cat Tail Dr, Stockton (only one shown) | ZIP 95204 | Cat Tail (11/24/25); Tracy; 30 N Gould St Sheridan WY (6/17/21); **2535 Gimelli Ct San Jose (4/11/17)**; Reno; Las Vegas (p5-6) | Las Vegas 2015; Reno 2016; **San Jose 12/2014-04/2017**; Sheridan WY Ste 1916 10/2020-06/2021 (p5) | 1455 Cat Tail Dr (p1) |
| **Santa Clara County criminal** | **RECORD FOUND, C1761642**; ordered 7/7, completed **10/14/2026** (99 days) (p3-6) | **Clear** on all four: 12/23/2025 (R1 p3), 3/27/2026 (R6 p3), 8/7/2026 (R7 p3), ~9/24-10/6/2026 (R8 p3) | not searched | not searched (national DB: no record, p5) | **No Record**, 7-year search, ordered 7/7, done by 7/13/2026 (p12-13) |
| Charges / filing / disposition / sentence / credits / fines | Counts 1-2, filed 10/25/2017, disp. 10/25/2017, 6 yr/4 yr, 317 days, $140/$300 ×2 | none reported | none | none | none |
| Parole status / discharge date | "Released 12/02/2020 … CURRENTLY ON PAROLE" (p5-6) | none | none | none | none |
| Sex-offender registry | **NSOPW: NO RECORD FOUND** (p10) | CA registry **Consider**: "BRENDAN NGEHSI NEWANFORBI, DOB 9/16/1996" (all four, p2) | "APPLICANT IS LISTED ON THE SEX OFFENDER REGISTRY IN THE STATE OF CA", verified by AKA/DOB/address (p5) | NSOR Record Found; source CA registry (p6) | "Subject is a registered Sex Offender in California" (p13) |
| Other adverse | none | R6: SJ traffic petty offenses pending; **R8: same, disposed "CONVICTION - BAIL FORFEITURE" 8/12/2026; MVR suspensions 12/1/2024-11/30/2025 and refused chemical test 2/20/2025-5/19/2026** (R8 p3-4) | — | — | — (RK says the MVR was the basis, GG letter 7/21/2026) |

### 6c. Contradictions with Accurate (supporting evidence)
1. **Santa Clara County result.** Five independent Santa Clara searches by two other CRAs, from 12/2025 through 10/2026, came back Clear/No Record (R1, R6, R7, R8 p3; R4 p13). Accurate alone reports a Santa Clara record. The most important one is InfoMart (R4), ordered **the same day** (7/7/2026) and finished in 6 days under an expressly **7-year** search. *What this shows:* other CRAs either treated C1761642 as outside the reportable 7-year window or did not match it. Either way, Accurate's reportability depends entirely on its own "released 12/02/2020" / "currently on parole" lines (Civ. Code 1786.18(a)(7) runs from disposition, release, or parole). *What it does not show:* that the conviction is not his. The registry hits imply an underlying qualifying conviction exists.
2. **Turnaround.** Others finished Santa Clara in 2-7 days (R1, R4, R6, R7). Accurate took 99 days, and its package review is dated before the result (CR p9 vs p4). This supports a lack of reasonable procedures and the timing anomaly in §2 #8.
3. **Alias.** No other CRA, across eight reports and three SSN-trace/developed-name lists (R2 p5, R3 p5-6, R4 p12), produced or recorded "NEWANSORBI". InfoMart shows **no alias at all**. This strongly supports dispute #3 that the alias did not come from public data or from the trace, which leaves Accurate's own intake as the source.
4. **Disposition date.** No other report gives a disposition date. Indirect point: InfoMart's 7-year conviction search (window about 7/2019-7/2026) returned No Record. That is consistent with a disposition before 7/2019, and with Accurate's report staying reportable only through its release/parole data rather than the disposition. This is inference only; the docket controls.
5. **Parole status / count 2 amounts.** **No other report has any parole, discharge, sentence, or cost data.** Nothing contradicts Accurate here directly. Proof still has to come from CDCR and the court docket.
6. **Internal inconsistency.** Accurate's own NSOPW search is "No Record Found" (CR p10), while every other CRA got a CA-registry hit on the same identifiers. This shows that Accurate's search matching is inconsistent. **Do not dispute it**, because it is favorable to him and correcting it would add a registry hit.

### 6d. What hurts his position
- Every other CRA confirms CA sex-offender registration (R1-R4, R6-R8). Disputing that C1761642 belongs to him is not supportable. Limit the disputes to *accuracy and completeness of the details* and *reportability* (parole/release dates).
- The 12/02/2020 release date (if true) keeps the case inside the ICRAA 7-year window until about 12/2027, regardless of parole discharge. Correcting "currently on parole" removes a misleading statement but may not remove the record.
- The FADV and HireRight address histories show a 30 N Gould St **Ste 1916**, Sheridan WY address from 10/2020-06/2021. Its start date is before the reported 12/02/2020 release. It looks like a mail-drop suite, which neither proves nor disproves custody dates, but Accurate may cite it. Be ready to explain it.
- The R8 Checkr MVR (suspensions, chemical-test refusal) and the 8/12/2026 bail-forfeiture traffic convictions are true adverse items, available to any employer through other channels (RK Logistics already cited the MVR).
- The conviction-question "No" (CR p11/p14): the other reports do not settle it either way. FADV shows "Self-Disclosed Criminal History: None" (R3 p3), so there is a prior instance of a "none" self-disclosure on file.

## 7. Updated ranked dispute items (supersedes §5 ranking)
1. **"CURRENTLY ON PAROLE" / release 12/02/2020** (CR p5-6). This now matters most, because Accurate's reportability turns on it and on the release date, and five other Santa Clara searches did not report the case (R1/R6/R7/R8 p3; R4 p13). Request: delete "currently on parole"; verify the release and parole-discharge dates with CDCR; re-evaluate reportability under 1786.18(a)(7). Proof: CDCR discharge certificate and release record, plus the other CRAs' Clear results as corroboration that accurate data led others to non-reporting.
2. **Disposition date 10/25/2017 = filing date** (CR p4-5). Request: the actual plea and sentencing dates, with the source. Proof: Santa Clara docket and abstract of judgment. Corroboration: InfoMart's 7-year no-record result (R4 p13), which is inferential.
3. **Alias "NGWA NFORBI, NEWANSORBI — Provided by Applicant"** (CR p2). Request: delete it and produce the intake record. Corroboration: it is absent from all eight other reports and all trace data (R2 p5, R3 p5-6, R4 p12 "Alias: -").
4. **Santa Clara 99-day search, package review before result** (CR p4, p9). Request: the vendor and court-runner log, the retrieval date and source, and the identifiers matched. Corroboration: the same-day InfoMart order finished 7/13 (R4 p12); Checkr took 2-7 days.
5. **Conviction-question "No"** (CR p11, p14). Dispute only if he did not give that answer. Caution: R3 p3 shows "Self-Disclosed Criminal History: None".
6. **Count 2 credits blank; $140/$300 duplicated** (CR p5-6). Proof: abstract of judgment only. No other CRA has this data.
7. **Incomplete file / address history / prior versions** (CR p2, p9). The other CRAs' traces (R2 p5, R3 p5) show the multi-state address history that Accurate withheld.
8. **[LINK]/[ENLACE] placeholder; cover letter signed "Amazon Salesforce"** (CR p1; -190268).
9. **Requestor HVH vs Salesforce / malformed REF** (CR p2). Low priority.
Do **not** dispute: the NSOPW "No Record" (favorable), the identity/ownership of C1761642 (contradicted by the registry hits), or the San Joaquin "No Record".

---
## 8. Focus: why Accurate's sex-offender search returned "No Record Found" (added 10/14/2026, 1:35 PM PT)

### 8a. Side-by-side of each vendor's sex-offender search
| Vendor / report | Product (as labeled) | Names / identifiers shown as searched | Coverage / source | Date run | Result and how the hit is displayed | Cite |
|---|---|---|---|---|---|---|
| **Accurate / Amazon** | "NATIONAL SEX OFFENDER DATABASE SEARCH", ID 496623723 | **None listed.** This is the only Accurate search, apart from address/SSN/package review, with no "NAME(S) SEARCHED" block. No DOB or jurisdiction is shown. | Not stated. Accurate's published product definition says its "National Sex Offender Search" is a **proprietary database** "sourced from state sexual offender registries", with confirmation at the state source. That is distinct from its NSOPW product and is not a direct CA Megan's Law search. | 2026-07-07 (order day) | **NO RECORD FOUND** | CR p10; accurate.com Exhibit C Product Definitions |
| Accurate (comparison) | County Santa Clara (found C1761642); National Criminal DB | Ngwa Nforbi/Brendan/Ngehsi; NFORBI/BRENDAN; NGWA NFORBI/NEWANSORBI; **NEWANFORBI/BRENDAN** | county court; proprietary DB | 10/14 (county); 7/7 (national DB) | The county search found the record. The national DB was "COMPLETED" with no content shown. The matched name is not displayed. | CR p4, p9 |
| Checkr / Pilot | Sex Offender Search | Brendan / Ngwa Nforbi; DOB 9/16; SSN -1726 (p2) | "CA SEX OFFENDER REGISTRY" | 12/16/2025 | Consider. Entry: **BRENDAN NGEHSI NEWANFORBI, DOB Sep 16 1996**, CA | R1 p1-2 |
| Checkr / Next Chapter | same | Brendan Ngehsi Ngwa Nforbi; DOB; SSN | CA registry | 3/26/2026 | same entry | R6 p1-2 |
| Checkr / Next Chapter | same | same | CA registry | 8/5/2026 | same entry | R7 p1-2 |
| Checkr / Nuro | same | Brendan Ngehsi **Ngwanforbi**; DOB; SSN; DL | CA registry | 9/23/2026 | same entry (NEWANFORBI) | R8 p1-2 |
| HireRight / Macy's | "National Sex Offender Registry", performed **through U.S. DOJ** (NSOPW) | Brendan Ngwa Nforbi, SSN -1726 | NSOPW national, then a manual analyst check | 5/29/2026 | The NSOPW run did not resolve; the status stayed **"Pending"**. Analyst note: "APPLICANT IS LISTED ON THE SEX OFFENDER REGISTRY IN THE STATE OF CA … Verified by Aka Name, DOB and Address" | R2 p4-5 |
| First Advantage / UPS | "NSOR Search – Department of Justice Web Site" | Given: BRENDAN NGWANFORBI; developed: NFORBI BRENDAN NGWA, BRENDAN NGEHSI NGWA-NFORBI | source of record: CALIFORNIA SEX OFFENDER REGISTRY; period 7/3/2017-7/3/2024 | 7/17-18/2024 | Record Found. Name on file **BRENDAN NGEHSI NGWANFORBI** | R3 p4, p6 |
| InfoMart / RK | NSO search inside "National Criminal Search" | Brendan N Ngwa Nforbi; DOB 09/16; SSN -1726; Alias "-" | jurisdiction "Sex Offender / California" | 7/7-13/2026 (same order day as Accurate) | Record. Name on file **Newanforbi, Brendan Ngehsi**, DOB 09/16; case # Unknown | R4 p12-13 |

### 8b. What the documents establish
- The CA registry entry exists and is publicly listed under **"Brendan Ngehsi Newanforbi" (or "Ngwanforbi"), DOB 9/16/1996**. Seven hits from four vendors between 7/2024 and 9/2026 confirm this, including one from the same week as Accurate's search (InfoMart, 7/7-13/2026). HireRight verified it by name, DOB **and address**, which means the public listing includes an address.
- Accurate *had* the matching name. "NEWANFORBI, BRENDAN" is on its AKA list (p2) and in every county/federal/national-DB search (p4-11). The DOB on file (09/16) matches.
- Accurate's sex-offender row is the **only** search that does not disclose the names searched, so it cannot be determined from the report which names or identifiers it ran.
- It finished on 7/7/2026, the order day, which is the same day as the SSN/address trace that "discovered" NEWANFORBI (p2, p9).

### 8c. Candidate explanations, ranked by documentary support
1. **Accurate's proprietary database missed or lacked the CA entry. Best supported, but an inference.** The product label ("National Sex Offender *Database* Search") matches Accurate's proprietary-DB product, not a CA DOJ search. Vendors that went to the CA registry (Checkr, InfoMart) or verified at CA (HireRight's analyst, FADV) all hit. HireRight's own DOJ/NSOPW national run stayed "Pending" until a human checked CA (R2 p5), which shows that national aggregators can fail on California. A publicly reported May 2024 outage of California's feed to NSOPW (AmeriCorps notice) makes this plausible, though its status in 2026 is unknown.
2. **The search ran before the matching name was developed, or only on the applicant-entered names. Plausible inference.** The CA listing is under NEWANFORBI, and Accurate says it found that name "through Address History", on the same day the sex-offender search completed (7/7). If the search ran only on the intake names (Ngwa Nforbi / NFORBI / the garbled "NEWANSORBI"), a strict-match search would miss "Newanforbi". This cannot be confirmed because the names searched are not shown.
3. **Garbled "NEWANSORBI" alias or first/last field transposition.** This is only a contributing factor. A garbled alias adds a useless search but would not cause the correct-name searches to miss. Transposition (surname "NGWA NFORBI" in the last-name field and "NEWANSORBI" in the first-name field) is visible for that alias only (p2).
4. **DOB mismatch.** Not supported. Every vendor has 9/16, and the registry shows 1996.
5. **CA §290.46 exclusion from the public site.** Contradicted. Seven public-source hits, including address verification (R2 p5), show he is listed.
6. **Timing.** Weak. The hits run from 7/2024 to 9/2026 continuously, and InfoMart hit in the same week.
7. **Deliberate suppression, for example a CA-employer filter honoring §290.46(j).** No document evidence either way. Note that a compliance filter would normally show "not reported" or "suppressed", not "NO RECORD FOUND". Ask Accurate how the search was run instead of alleging this.

### 8d. Legal significance (brief)
- **§1681e(b) / Civ. Code 1786.20(b):** "NO RECORD FOUND" is a factually incomplete statement. However, it is *favorable* to him, so it caused no harm, and disputing it would invite Accurate to add a registry hit. Its main use is as **procedure evidence**. Accurate's matching was inconsistent: the name it had for him found a county record in Santa Clara but missed a public registry entry under that same name. That supports an unreasonable-procedures theory for the adverse items, particularly the unsourced "currently on parole" line and the intake-attributed garbled alias.
- **§290.46(j) theory:** in Accurate's report, the registry status was **not reported**. That cuts against any claim that Amazon used registry information *from Accurate's report*. Amazon could still have used other sources, and the conviction plus "currently on parole" lines (CR p5-6) are effectively a proxy for registrant status. The §290.46 theory against Amazon would need evidence outside this report, such as Amazon's adjudication notes or another vendor's data.
- **Next step:** request, under 1681g/1786.10, the sex-offender search's names searched, identifiers, source database, and run time. Do not dispute the result.
