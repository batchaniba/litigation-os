# Claude review — as attached October 31, 2026

Copied into this folder from the uploaded work product. Not edited. Nothing here has been served or filed. The comparison across the three reviews is `../SYNTHESIS-3-MODEL.md`.

---

Reading the source files now (closing letter, then the 202-page disclosure); analysis to follow.

Still gathering record: complaint read; now the Answer (Dkt 21), Oct 14 report, and the file disclosure.

Now searching the 202-page file disclosure for Tauxbe, vendors, name inputs, and DOB-only matches.

I've read everything you listed: the README, 00-ANALYSIS, INDEX, all of `sources/` and `extracts/`, the Dkt. 21 Answer, the Oct. 14 dispute email, and the earlier draft ROG and RFA sets. I didn't edit, commit or push anything.

# Matter 29: critical review of Accurate RFP Set One, plus Set Two, ROGs, RFAs, Rule 15, Rule 45 and the 26(f) agenda

## Bottom line

1. **Set One is sound but aimed at the wrong channel for § 290.46.** The analysis treats the sex-offender search (#496623723) as the key evidence. The search more likely to have carried registry data is the **National Criminal Database Search #496623727**. It shows only "COMPLETED," with no result. Its raw output is missing from the 202-page disclosure, and Set One never asks for it by ID. That is the largest gap.
2. **Four ratings are wrong on the facts.**
   - **RFP 15** (the "Previous conviction question: No" answer) is a serious risk to you, not a "Good" request.
   - **RFP 11** (San Joaquin) should be low priority. Pressing it could surface records Accurate correctly left out.
   - **RFP 10** (the 99-day Santa Clara delay) is tied to the pleaded delay theory, so it is stronger than "Moderate."
   - **RFP 16** will most likely produce a certification that *defeats* the pleaded § 1681b(b)(1) theory. Its real value is the contract and the adjudication criteria.
3. **The analysis has three factual errors:**
   - San Joaquin returned **three** DOB-only cases, not two.
   - The "Oct. 27" disclosure **contains the Oct. 28 closing letter**.
   - The revised report **removed NEWANSORBI from the "names searched" lists without re-running the searches**. This is new, and it is the best accuracy and audit-trail fact in the file.
4. **Rule 15:**
   - § 1681e(b) and ICRAA § 1786.20(b) are worth adding, but they are light on damages.
   - § 1681i is weak, because Accurate fixed the alias within 14 days.
   - § 1681k depends on whether Amazon saw any results before Oct. 14. Don't plead it until the furnishing logs come in.
   - Do **not** build an accuracy claim on the sex-offender "NO RECORD FOUND." It is an omission that helps you, and it supports Accurate's Second Defense and the *Lerma* pattern.
5. **Don't rewrite the served requests.** Withdrawing or amending Set One gives Accurate a fresh 30 days. Serve the rewrites as Set Two Nos. 21–24 (supplementing 8, 16, 18 and 19) right after the Nov. 6 conference.

**Path key used below**

| Key | Path (relative to `internal/private/research/matter-29-discovery/` unless it starts with `documents/`) |
|---|---|
| RFP | `sources/RFP_Accurate_Set1.txt` |
| CL | `sources/Closing_Letter_1028.txt` |
| FD | `sources/Accurate_File_Disclosure_Oct27.txt`. "p." means the form-feed page in the text extract, which is **not** the PDF page. The 202-page PDF isn't in the repo. |
| R14 | `extracts/Accurate_Consumer_Report_Oct14.txt` |
| CMP | `extracts/Dkt_02_Removal_Exhibits.txt` (Complaint = Ex. 1; cited by complaint page:line) |
| ANS | `documents/matter-29/Dkt 21 - Accurate Background Answer and Affirmative and Other Defenses (Filed Sep 22 2026).txt` (cited by Dkt. 21 page:line) |
| DISP | `internal/docs/settlement/fcra-file-requests/Accurate Background - Dispute of Accuracy and Request for Complete File, Ref 496623722 (Sent Oct 14 2026).txt` |

---

## 0. Record facts that change the analysis

| # | Fact | Source | Effect |
|---|---|---|---|
| F1 | San Joaquin vendor (Infinity) returned **3** cases on Brendan Ngehsi Newanforbi, all `identified_by_dob: true`, `identified_by_name: false`, `identified_by_ssn: false`. Case numbers: STK-CR-FMISC-2020-0002397, -2020-0004747, -2025-0004687. Reported "NO RECORD FOUND." | FD:1124–1244 (p.28–30); R14:83–87 | Corrects 00-ANALYSIS:137 ("two"). The name fields match exactly, yet the name flag is false. That is an anomaly, but it is also an exclusion that **helps** you. |
| F2 | The Santa Clara request to InformData-SJV used first name **NEWANSORBI**, last name **NGWA**, county "SANTA CLARA," `years_searched: 0`, plus ten AKAs, five of which use NEWANSORBI. | FD:1246–1262 (p.31) | NEWANSORBI was the **primary subject name** sent to the vendor, not just an alias on the report. |
| F3 | The 2025 Target order's subject profile has **no** NEWANSORBI variant (Brendan Ngehsi Nforbi, Ngwanforbi, Ngwa, Ngwa-Nforbi). | FD:1637–1650 (p.50) | INFERENCE: NEWANSORBI first appears in 2026, so it came from Amazon's intake or Accurate's processing of it. It is not a legacy file value. |
| F4 | The revised report keeps the same completion dates (San Joaquin 2026-09-03; Santa Clara 2026-10-14) but lists only three names searched. The Oct. 14 version listed NGWA NFORBI / NEWANSORBI. | CL:612–637 vs. R14:83–110 | The reinvestigation **rewrote the search record without re-running it**. This matters for audit trail, accuracy and reinvestigation integrity. |
| F5 | The revised report still says "updated on 10/14/2026" and shows "2026-10-19 09:42:29: Dispute has been initiated." | CL:544, 579–580; FD:660, 3019 | Version-control problem. Dispute received Oct. 15 (CL:17) and initiated Oct. 19 (four days later). |
| F6 | The "Oct. 27" disclosure includes the **Oct. 28** closing letter. | FD:2440–2475 (p.179) | Ask when and how the file was assembled. The date is inconsistent. |
| F7 | No raw data in the disclosure for **#496623727 National Criminal Database**, **#496623723 sex-offender search**, #496623725 Global Watch, or #496639945 SSN/Address Mover. Raw sections exist only for San Joaquin, Santa Clara, Sheridan, four federal districts and NY statewide. | FD:1124–1411 (headers at 1124, 1246, 1269, 1275, 1309, 1343, 1377, 1411) | The two database searches most likely to carry registry data are exactly the ones withheld. |
| F8 | #496623727 lists names searched and shows "COMPLETED," with no result line, on 7/7/2026. The sex-offender search lists **no** names searched. | FD:903–915, 952–960; R14:265–277, 317–325 | Ties into DISP (the dispute complained the sex-offender search hid its inputs). |
| F9 | Most components finished July 7. San Joaquin finished Sept. 3. The package review was Oct. 13; Santa Clara finished Oct. 14. | R14:87, 105, 181–352; CL:616, 633, 806–808 | The July 27 shift loss (Compl. ¶22, 7:1–6) came **before** the report was complete. Causation depends on what Amazon saw before July 27. |
| F10 | "CURRENTLY ON PAROLE" (release 12/02/2020) **survived** the reinvestigation. You did not dispute it on Oct. 14. | R14:140, 166; CL:667, 692; DISP (items 1–2 only) | It can't support § 1681i until it is disputed. Whether it is inaccurate depends on your actual discharge status (**UNVERIFIED**; no CDCR record in this room). |
| F11 | "PREVIOUS CONVICTION QUESTION: NO" / "ANSWER: No." The question covers release from prison within 7 years and warns that failure to answer honestly "may impact your eligibility." | R14:361; CL:879–901, 978; FD:1000, 1097 | See RFP 15 below. |
| F12 | The California notices contain unfilled "[LINK]" and "[ENLACE]" placeholders, still present in the revised report. | R14:11, 23; CL:529, 540; FD:644, 656, 2967 | Possible ICRAA notice defect (§ 1786.29, subdivision **UNVERIFIED**). |
| F13 | Accurate's report legend: "Client agrees and certifies that its ordering of and use of this report is in strict compliance…" | FD:1418, 1660, 2262 | A certification almost certainly exists. That undercuts pleaded ¶61 (§ 1681b(b)(1)). |
| F14 | Recipients: Amazon (7/7/2026) and Target (3/19/2025). Sources letter is captioned "Report #Y94611404 for Amazon on October 14, 2026." Vendors: Tauxbe (sex-offender, source NSOPW), InformData-SJV (Santa Clara), Infinity (San Joaquin), RDK (Sheridan), Vital4 (Global Watch). | FD:21–76 (p.1–2) | Rule 45 targets, and some evidence that the report was furnished on Oct. 14. |

**Pleadings anchor.**

- Complaint ¶26 says you are a registrant (CMP 8:2–3). Accurate answered "lacks knowledge" (ANS 11:1–6).
- Count 3's only Accurate-specific theory is ¶61, § 1681b(b)(1) (CMP 17:1–8), plus willfulness at ¶62 (17:10–14).
- Count 4 against Accurate is "prepared and furnished the report without ensuring that the user complied" (CMP 19:1–4).
- Accurate's Answer: First Defense "has not prepared" a report; Second Defense "has not reported" registry status (ANS 38:6–11); Answer ¶23 admits the report is "pending" (ANS 10:1–5).
- **The Second Defense is consistent with the Oct. 14 report on its face.** Only the First Defense is undercut.

---

## 1. Testing the RFP ratings (Set One)

| RFP | Analysis | Mine | Why |
|---|---|---|---|
| 1 Order record / audit history | Strong | **Strong** | Agree. It now also covers F4 and F5 (the version rewrite and the "updated 10/14" header). Cite those in the meet-and-confer. |
| 2 Every report version | Strong | **Strong** | Agree. F4 shows at least two materially different versions sharing one date stamp. |
| 3 Furnishing / access logs | Strong | **Strongest in the set** | Causation (F9), § 1681k timing, *TransUnion* standing (who received the NEWANSORBI version) and the First Defense all depend on it. The "Amazon said 10/19 it had no results" support in 00-ANALYSIS:144 has **no source in this room** (UNVERIFIED). |
| 4 Amazon intake data | Strong | **Strong, two-edged** | It will settle where NEWANSORBI came from (F3). It will also show the conviction-question answer in its original form (F11). |
| 5 NEWANSORBI audit trail | Moderate | **Strong** | F2 and F3 make this central to procedures and willfulness under the *pleaded* counts too (the Fifth Defense on good faith, and the delay). It is more than an unpleaded § 1681e(b) point. |
| 6 Names per search | Strong | **Strong** | Agree. |
| 7 Sex-offender search #496623723 | Strong | **Strong but under-inclusive** | It omits #496623727 (F7, F8). After *Lerma*, the registry-sourcing question is whether a database hit caused Accurate to choose and search Santa Clara (a county you didn't live in, FD:1248–1251). Cover this in Set Two. |
| 8 Matching / normalization "limited to those applied" | Moderate | **Weak as drafted** | "Limited to those applied to Plaintiff's order" invites the answer "no written policy was specifically applied." There is no willfulness period and it doesn't cover the database or alias logic. Rewrite below. |
| 9 Santa Clara court records | Moderate ("largely satisfied") | **Moderate** | Not satisfied in the text. Six consecutive Santa Clara headers carry no extracted text (FD:1263–1268), probably image-only court papers (check the PDF). More important: nothing says **why** Santa Clara was searched. |
| 10 Reasons for 99 days | Moderate (unpleaded) | **Good to Strong** | The delay is pleaded (Compl. ¶¶17–25, 6:8–7:28) and is the mechanism of the alleged constructive adverse action. |
| 11 San Joaquin | Moderate | **Low; handle with care** | F1: Accurate excluded three exact-name, DOB-matched cases. Pressing "matching or exclusion decisions" invites Accurate (and Amazon in discovery) to re-examine records the report correctly left out. It is already served; don't escalate it in a deficiency letter. |
| 12 Oct. 13 package review | Good | **Good** | Agree. The package review closed the day **before** Santa Clara completed. |
| 13 Case notes / holds | Strong | **Strong** | Agree. Insist on a Rule 26(b)(5) log. |
| 14 "Currently on parole" source | Good | **Good if you were discharged; risky otherwise** | Depends on facts this room doesn't contain (F10). Confirm your CDCR discharge date before relying on it. |
| 15 Conviction-question provenance | Good | **High risk** | If the "No" is your own answer, given the 12/02/2020 release (CL:663–667) and the 7-year wording (CL:885–886), the production gives Amazon a ready non-discriminatory or honesty reason, and possibly an after-acquired-evidence argument on the Fair Chance Act claim. It helps only if the "No" was system-defaulted or mis-mapped. It is already served and Amazon holds the same data, so withdrawing it gains little and draws attention. Don't build ROGs or RFAs on it. |
| 16 Certifications / "parts of" agreement | Strong | **Strong for discovery; weak for the pleaded claim** | F13: the certification probably exists and disposes of ¶61 as pleaded. The value is the full contract, adjudication criteria and allocation of compliance duties (the Tenth Defense). |
| 17 Notices incl. [LINK] | Good | **Good** | Ties to F12, and to § 1681k timing if anything was reported before Oct. 14. |
| 18 Dispute file | Moderate | **Moderate** | It carves out privilege, but your Oct. 14 email cc'd Seyfarth and Accurate forwarded it to Seyfarth (INDEX:111; DISP header). Expect over-withholding. Rewrite below. |
| 19 Accurate–Amazon communications | Strong but narrow | **Moderate as drafted** | It misses status / "pending" / ETA / expedite or cancel messages, shift-related contact, and machine-to-machine status pushes. Rewrite below. |
| 20 Data dictionaries | Good | **Good** | Add adjudication and eligibility codes and the "F" / "N" search_status codes (FD:1128, 1271). |

**Problems across the whole set:**

- No definition of "Amazon": the record uses "Amazon HVH" (R14:48), "Amazon Salesforce" (Compl. ¶15b, 5:12–17) and Ref. ad188d7e… (CL:568).
- The default period (RFP:87–91, July 1–Nov. 15, 2026) shuts out willfulness: post-*Lerma* 2023 knowledge and the 2025 Target report.
- No request reaches the National Criminal Database search, vendor contracts or raw vendor returns.
- **Signature:** the PDF does carry an image on pp. 7 and 9 (`pdfimages`), so Rule 26(g) is satisfied.

---

## 2. Redlined rewrites, served as Set Two Nos. 21–24

Format: ~~deleted~~ / **added**. Each supplements and does not replace the Set One request. State that in the preamble ("Requests 21–24 supplement, and do not withdraw or narrow, Requests 8, 16, 18 and 19").

**Add a definition: "Amazon"** means Amazon.com Services, LLC and any affiliate, account or portal identity through which it ordered, viewed or received Screening Order 496623722, including "Amazon HVH," "Amazon Salesforce," and account or reference ad188d7ed256-40f1-b7f0-e2a7f77aa061.

### RFP 21 (supplementing 8): matching, alias and search-selection procedures
> Produce the policies, procedures, matching criteria, field-mapping specifications, name-normalization **and alias-generation** rules, **county-selection rules,** and vendor specifications in effect at any time from ~~July 1, 2026~~ **January 1, 2023** through ~~October 31~~ **November 15**, 2026, ~~limited to those applied to Plaintiff's Screening Order 496623722 and the National Sex Offender Database Search performed for Plaintiff under Search ID 496623723~~ **that governed orders placed by Amazon in California, concerning: (a) how name variants and AKAs are created, parsed, ordered and attributed (including "Provided by Applicant" and "Discovered through Address History"); (b) how identity matches are confirmed or excluded in county criminal searches, including the use of name, date of birth and SSN identifiers; (c) how counties and jurisdictions are selected for search, including any search triggered by a database result; (d) how results of the National Criminal Database Search and the National Sex Offender Database Search are used, filtered, suppressed, verified, or reported as "COMPLETED" or "NO RECORD FOUND"; and (e) how parole or supervision status is sourced and verified before reporting.**

- Trade secret: expect the objection. The cure is the N.D. Cal. model protective order with an AEO tier. Don't concede redaction of the rules themselves.
- Fallback: limit to the Amazon account and 2025–2026.

### RFP 22 (supplementing 16): full agreement, certifications and adjudication criteria
> Produce ~~Amazon's permissible-purpose and employment-law certifications applicable to order 496623722 and the parts of the account configuration, order instructions, or screening service agreement showing the scope of the package ordered and the respective compliance responsibilities~~ **(a) every agreement between Accurate and Amazon in effect at any time from January 1, 2023 through November 15, 2026 governing employment screening in California, including master agreements, statements of work, order forms, amendments, addenda, schedules and exhibits (pricing may be redacted); (b) every end-user certification Amazon gave under 15 U.S.C. § 1681b(b)(1) or Cal. Civ. Code § 1786 et seq. that applied to order 496623722, with its execution date and version; (c) the account and package configuration for "Amazon HVH" / "General Package," including component list, search triggers and any California- or Fremont-specific settings; and (d) any adjudication matrix, eligibility criteria, scoring, flagging or "review"/"pending" rules that Accurate applied, or configured or hosted for Amazon, for that account.**

- 26(b)(5): none expected.
- Seyfarth will argue (d) is Amazon's. It is in Accurate's "possession, custody, or control" if Accurate hosts it.

### RFP 23 (supplementing 18): reinvestigation file
> Produce the ordinary-course dispute-case file, intake logs, investigation activity logs, communications, findings, corrections, and status records concerning Plaintiff's October 14, 2026 dispute, reference 496623722, and service request 20261014-15421955, through the date of production, **including: (a) every notice to and communication with any vendor or furnisher (including Tauxbe Data Inc., InformData - SJV & Associates, LLC, and Infinity Court Research & Retrieval); (b) records of any search re-run, re-verification or decision not to re-run; (c) records showing who decided to remove the "NGWA NFORBI, NEWANSORBI" entry and to change the "NAME(S) SEARCHED" lists, and why; (d) the date, channel and content of each revised report sent to Amazon; (e) records of the October 15 receipt and October 19 initiation dates; and (f) records showing how and when the file disclosure dated October 27, 2026 was assembled, including why it contains a letter dated October 28, 2026,** excluding communications between Accurate and its counsel protected by the attorney-client privilege and attorney work product. **The copying of counsel on a communication does not exempt ordinary-course dispute-processing records. Log any withheld document under Fed. R. Civ. P. 26(b)(5).**

### RFP 24 (supplementing 19): all Accurate–Amazon communications about Plaintiff
> Produce ~~nonprivileged business communications~~ **all communications, in any form (including email, portal messages, tickets, chat, API or webhook status transmissions, and system notes),** between Accurate and Amazon **from July 1, 2026 through the date of production** about Plaintiff's **Application,** screening status, identity inputs, search results, exceptions or delivery, **including communications about eligibility, adjudication, "pending," hold, delay or ETA status, requests to expedite, cancel or close the order, Plaintiff's start date or training shift, Plaintiff's dispute, and the revised report,** excluding post-litigation attorney-client communications and attorney work product. **For any communication withheld under a common-interest or joint-defense claim, provide a Rule 26(b)(5) log.**

---

## 2b. Accurate RFP Set Two, Nos. 25–40 (filling the gaps)

Period: Jan. 1, 2023 – Nov. 15, 2026 unless stated otherwise. All of these are post-Nov. 6 Rule 34 requests.

**Database channels and vendor raw data**
- **25.** The complete request and response payloads, raw vendor returns, possible-match lists, and filtering or suppression records for **National Criminal Database Search 496623727**, including any record from a sex-offender registry source and any record that triggered a county search. (F7, F8)
- **26.** The complete request and response payloads exchanged with Tauxbe Data Inc. for search 496623723: names, name order, DOB/SSN/address sent, the timestamp, every candidate returned, and any match or exclusion decision. (FD:50–61; F8)
- **27.** The raw request and response payloads and retrieval records for Global Watch 496623725 and SSN Trace / Address Mover 496639945, including the address history that produced "Discovered through Address History" (R14:43). These are the same categories, missing from FD.
- **28.** Records showing why Santa Clara County (Search 496644204) and Sheridan County, WY (496644207) were selected for search. (FD:1246–1251, 1269–1272)
- **29.** InformData-SJV's full response, the court-runner and retrieval notes, and the image files for 496644204, in native format with metadata. (FD:1263–1268)

**Vendor relationships**
- **30.** Agreements, specifications and service-level terms with Tauxbe, InformData-SJV and Infinity that were in effect in 2026, limited to matching, identifiers, turnaround and accuracy obligations. (Pricing may be redacted.)

**Disclosure and authorization**
- **31.** Every FCRA § 1681b(b)(2) disclosure, authorization, ICRAA § 1786.16 notice or consent, and e-sign audit trail (IP, timestamps, document version, click path) for Plaintiff's 2026 Application, whether hosted by Accurate or received from Amazon. (Missing: 00-ANALYSIS:137)
- **32.** The template versions of the documents in No. 31 that Accurate supplied, hosted or approved for Amazon California hires in 2026.

**Willfulness and punitive damages (§ 1681n; Civ. Code § 1786.50)**
- **33.** Policies, training materials and audits from 2023–2026 concerning alias attribution, identity matching, sex-offender registry searches and California Penal Code § 290.46.
- **34.** Documents sufficient to show the changes, if any, Accurate made to its sex-offender, database or registry-related search practices for California employment orders after the May 2023 dismissal order in *Lerma*, C.D. Cal. 8:22-cv-01727 (INDEX:168–174).
  - Notice only. Don't characterize *Lerma* as a liability finding, and never as Amazon having settled a § 290.46 claim (README:78).
- **35.** Complaints, CFPB and AG inquiries, and lawsuit pleadings from 2023–2026 alleging (a) an alias or name attributed to a consumer that the consumer did not provide, or (b) registry-derived information in an employment report.
  - Expect a proportionality fight. Fallback: documents sufficient to identify such matters, plus the pleadings in *Varela*, *Santee* and *Rangel*.
- **36.** Documents sufficient to show Accurate's net worth and annual revenue for 2024–2025.
  - Courts split on timing of financial-condition discovery when punitive damages are claimed. Offer AEO treatment and agree to defer production until after the summary-judgment ruling if Accurate insists, but not further. **UNVERIFIED:** no N.D. Cal. authority checked in this room.

**Insurance and indemnity**
- **37.** Any insurance agreement under Rule 26(a)(1)(A)(iv), and any indemnity or defense agreement with Amazon covering this action.

**Versions and file assembly**
- **38.** Native version history or diff records for every version of the report for order 496623722, with the date stamp each version displayed. (F4, F5)
- **39.** Documents showing every person or entity to whom any version was furnished, including any re-furnishing after Oct. 28. (CL:28)
- **40.** The 2025 Target order 27257525 subject profile and the sex-offender search payload, limited to identity inputs and match results. This is the comparator for the NEWANSORBI origin (FD:1590–1650).

---

## 3. Interrogatories (22 drafted; 3 held in reserve under Rule 33(a)(1)) and RFAs

**Service timing.** Serve after the conference ends Nov. 6 (Rule 26(d)(1)).
- By email with written Rule 5(b)(2)(E) consent: due 30 days → Dec. 6 (Sun.) → **Mon. Dec. 7** (Rule 6(a)(1)(C)).
- By mail: +3 under Rule 6(d) → **Thu. Dec. 10**.

The Oct. 19 draft (`internal/docs/matter-29/discovery-set-one/04_Accurate_Interrogatories_Set_One.md` ROGs 1–9) is folded in below. Each is drafted as a single subject to avoid "discrete subpart" counting.

1. State all facts supporting your First Defense (ANS 38:6–8) and your denials at Answer ¶¶29, 56, 57 (ANS 12:14–16; 23:18–21; 24:1–4), including what "prepared" and "completed" mean as you use them, and whether your position changed after Oct. 14, 2026.
2. State all facts supporting your Second Defense (ANS 38:9–11), including every source of sex-offender registry data accessed for order 496623722 by any component, including #496623727.
3. Identify each date on which any component result, status or version from order 496623722 was furnished or made viewable to Amazon, with the channel and the version.
4. Identify the original source of "NEWANSORBI," the system or person that first recorded it, and the basis for labeling it "Provided by Applicant" (R14:42).
5. Explain why the Santa Clara request transmitted NEWANSORBI as the subject's first name and NGWA as the last name (FD:1248–1249).
6. Identify the vendor, database and identifiers used for National Criminal Database Search 496623727, and describe every result it returned, including any registry-sourced record.
7. Identify the names, name order and identifiers sent to Tauxbe for search 496623723, and describe every candidate record returned.
8. State why Santa Clara County was selected for search for a consumer with a Stockton address.
9. State the reason reflected in your records for the 99-day Santa Clara turnaround (July 7 – Oct. 14).
10. Identify the person or automated process that performed the Oct. 13 package review (500363362), and what results were then available.
11. Identify every person who worked on order 496623722 or the dispute, with role and dates.
12. Describe the reinvestigation step by step: who did it, what sources were contacted, whether any search was re-run, and why the "NAME(S) SEARCHED" lists changed while the completion dates did not (CL:612–637).
13. State why the revised report bears "updated on 10/14/2026" (CL:544).
14. Identify each version of the report and the date each was furnished to anyone.
15. State whether you provided a § 1681k(a)(1) notice for each public-record item reported, and the date of each notice relative to the date Amazon could first view that item.
16. Identify who authored or controlled the California notices containing "[LINK]/[ENLACE]," and the date the placeholder was first noticed (R14:11, 23).
17. Identify every certification Amazon gave you that applied to this order (date, version, signatory).
18. Describe the division of adjudication and compliance responsibilities between you and Amazon for California hires in 2026, including whether you assign any eligibility or "review" status.
19. State the facts supporting your Fifth Defense (good faith / objectively reasonable interpretation), identifying each FCRA or ICRAA provision interpreted and the interpretation (ANS 38:20–23).
20. State the facts supporting your Fourth Defense (failure to mitigate or use FCRA/ICRAA procedures) (ANS 38:15–19).
21. State the facts supporting your Tenth Defense (no hiring decision) (ANS 39:12–15), including every communication to Amazon that could affect start date or shift.
22. Identify every lawsuit, CFPB complaint or regulatory inquiry from 2023–2026 alleging alias misattribution or registry-derived reporting in employment screening.

Reserved: 23–25, for follow-up after the Dec. 7 production.

**Deliberately omitted:** anything on the conviction-question answer, the San Joaquin DOB-only cases, or the underlying conviction.

### Requests for Admission

Attach exhibits for the genuineness RFAs (Rule 36(a)(1)(B), (a)(2)). The Oct. 19 drafts (`06_Accurate_RFA_Set_One.md` Nos. 1–8) are kept in substance; Nos. 1, 3–6 and 8 are restated or folded in below.

*Genuineness*
- **1.** Ex. A (the Oct. 14 report, documents/matter-29/…updated Oct 14 2026.pdf) is a genuine copy of a report Accurate prepared.
- **2.** Ex. B (the Oct. 28 letter and revised report) is genuine.
- **3.** Ex. C (the file disclosure) is a genuine copy of what Accurate provided.

*First Defense (preparation and furnishing)*
- **4.** On or before Oct. 14, 2026, Accurate prepared a consumer report about Plaintiff for Amazon.
- **5.** Accurate furnished the Oct. 14 report to Amazon. (FD:27)
- **6.** Accurate furnished a revised report to Amazon on or after Oct. 28, 2026. (CL:28)
- **7.** The report was prepared for employment purposes.
- **8.** Accurate is an investigative consumer reporting agency as to order 496623722. (Supported by *Connor v. First Student, Inc.*, 5 Cal. 5th 1026 (2018), on ICRAA's application to criminal-record reports.)

*Alias*
- **9.** The Oct. 14 report listed "NGWA NFORBI, NEWANSORBI" as an AKA. (R14:42)
- **10.** It labeled that AKA "Provided by Applicant."
- **11.** Plaintiff did not provide "NEWANSORBI" to Accurate.
- **12.** Accurate transmitted NEWANSORBI as the subject's first name in the Santa Clara request. (FD:1248)
- **13.** The 2025 Target subject profile did not contain NEWANSORBI. (FD:1637–1650)
- **14.** Accurate removed the AKA on reinvestigation. (CL:23–26)

*Search records*
- **15.** Accurate did not re-run the San Joaquin or Santa Clara searches during the reinvestigation.
- **16.** The revised report's "NAME(S) SEARCHED" for 496644204 omits a name that was actually searched. (CL:633–637 vs. FD:1248–1260)
- **17.** The revised report displays "updated on 10/14/2026." (CL:544)
- **18.** Search 496623723 was performed through Tauxbe Data Inc. using NSOPW. (FD:50–61)
- **19.** Search 496623723 was completed July 7, 2026. (R14:325)
- **20.** The report lists no names searched for 496623723. (R14:317–325)
- **21.** Search 496623727 was completed July 7, 2026, and the report states no result other than "COMPLETED." (R14:265–273)
- **22.** The file disclosure contains no raw result data for 496623727 or 496623723.

*Timing and delay*
- **23.** As of July 27, 2026, order 496623722 was not complete. (ANS 10:3–4 admits "pending" as of Sept. 22)
- **24.** The Santa Clara component was ordered on or about July 7 and completed Oct. 14, 2026.
- **25.** The package review (500363362) was completed Oct. 13, before the Santa Clara completion.

*Notices and dispute*
- **26.** The California ICRAA notice in the report displayed "[LINK]" and "[ENLACE]" in place of a link. (R14:11, 23; CL:529, 540)
- **27.** Accurate received Plaintiff's dispute on Oct. 14, 2026 (SR 20261014-15421955 at 2:03 p.m.; INDEX:110).
- **28.** Accurate recorded the dispute as initiated Oct. 19, 2026. (CL:580)
- **29.** The file disclosure dated Oct. 27, 2026 contains a letter dated Oct. 28, 2026. (FD:2440–2450)

*Certification*
- **30.** Amazon provided Accurate a written certification under § 1681b(b)(1) before the report was furnished.

  This is a deliberate risk. An admission ends the ¶61 theory, but it tells you before you amend that ¶61 should be replaced, not defended.

**Don't serve RFAs on** parole status, the conviction-question answer, the San Joaquin cases, or whether you are a registrant.

---

## 4. Rule 15 amendment assessment

**Procedure.**
- The as-of-right window closed Oct. 13 (README:60). Proceed under Rule 15(a)(2): written consent, or leave "freely given" under *Foman v. Davis*, 371 U.S. 178, 182 (1962).
- Ask Accurate to stipulate at the Nov. 6 conference.
- If they refuse, file a noticed motion: Civil L.R. 7-2 (35 days' notice), with the full proposed pleading (Civil L.R. 10-1) and a redline against the last pleading (Krishnan requirement per README:60; the standing order PDF isn't in the repo, so **UNVERIFIED** against its text).
- File before any scheduling-order amendment deadline. After that deadline, Rule 16(b)(4) good cause applies (*Johnson v. Mammoth Recreations*, 975 F.2d 604, 607–09 (9th Cir. 1992)).

**Timing recommendation.** File after the Nov. 18 ruling on Dkt. 19, so one amended complaint answers the ruling on Claims 5–7. Target early-to-mid December. Disclose the anticipated amendment in the Nov. 24 Joint CMC Statement.

**Why leave is needed.** Count 3 is captioned generally (CMP 15:14–16), but its Accurate-specific allegation is only ¶61 (§ 1681b(b)(1)). In the Ninth Circuit, new theories raised first at summary judgment are generally barred when the complaint gave no notice (*Pickern v. Pier 1 Imports (U.S.), Inc.*, 457 F.3d 963, 968–69 (9th Cir. 2006)). If leave is denied, the facts below still go to willfulness under ¶62, to ICRAA Count 4, and to rebutting the First, Fourth, Fifth and Tenth Defenses. They do not support a free-standing accuracy claim.

### Claim-by-claim

**A. § 1681e(b) against Accurate: plead it. Moderate liability case, thin damages.**

Elements: inaccurate information, unreasonable procedures, damages and causation (*Guimond v. Trans Union Credit Info. Co.*, 45 F.3d 1329, 1333 (9th Cir. 1995)). "Inaccurate" includes "patently incorrect or materially misleading" (*Carvalho v. Equifax Info. Servs.*, 629 F.3d 876, 890 (9th Cir. 2010)).

Facts:
1. A name you never provided, attributed to you as "Provided by Applicant" (R14:42; DISP item 1).
2. It was used as the primary search name sent to vendors (FD:1248).
3. It does not appear in the 2025 profile, which shows a 2026 processing origin (F3).
4. "Currently on parole," only if you can prove discharge (F10; **UNVERIFIED**).
5. The revised report misstates the names actually searched (F4). This is a post-dispute inaccuracy furnished again to Amazon (CL:28).

Standing: *TransUnion LLC v. Ramirez*, 594 U.S. 413 (2021) requires dissemination. Plead the Oct. 14 furnishing (FD:27) and the Oct. 28 re-furnishing (CL:28).

Weak spots:
- The shift was lost July 27, before either version existed (F9). Damages from the alias are mostly dignitary or emotional unless Amazon saw it earlier, which turns on RFP 3.
- Statutory damages require willfulness (§ 1681n).

**Do not** plead the sex-offender "NO RECORD FOUND" as inaccurate (see Bottom line 4). It reinforces ANS 38:9–11 and the *Lerma* pattern the complaint itself describes (Compl. ¶32, 9:21–10:1).

**B. § 1681i: hold. Weak now.**

The dispute was emailed Oct. 14 (DISP), received per Accurate Oct. 15 (CL:17), initiated Oct. 19 (CL:580) and closed Oct. 28 (CL:10–26), inside 30 days. The alias was removed. The only colorable defects:
- The non-responsive treatment of the sex-offender search item. Pleading it hurts you, for the same reason as above.
- The names-searched rewrite without a re-run (F4), which is an "unreasonable reinvestigation" theory.

Plead it only if Set Two shows no vendor contact or no real review. Separately, decide whether to dispute the parole line as a consumer step (not a court paper) once you have discharge proof. That would create a clean § 1681i record.

**C. § 1681k: conditional. Don't plead yet.**

Accurate sent a § 1681k notice on Oct. 14 (documents/matter-29/"…FCRA 1681k Public Record Notice…Oct 14 2026.pdf"; INDEX:113). That looks compliant for the Santa Clara item. A violation exists only if public-record results were viewable to Amazon earlier (federal and NY components July 7; San Joaquin Sept. 3) without a contemporaneous notice. That turns entirely on RFP 3 and ROG 15.

**D. ICRAA § 1786.20(b) (reasonable procedures for maximum possible accuracy): plead it. Same facts as A.**

- Pairs with Count 4.
- *Connor* forecloses the argument that ICRAA does not reach criminal-record reports.
- The Eighth Defense (§ 1681h(e)) targets common-law-type claims "based on" FCRA disclosures. It is not a strong preemption argument against an ICRAA statutory accuracy claim. **UNVERIFIED:** no case pulled in this room.
- Damages under Civ. Code § 1786.50(a): the complaint pleads $10,000 "if knowing" (CMP 19:5–11). **Verify the statute's text** before re-pleading; I could not confirm whether the $10,000 floor requires a knowing violation.
- Optional add-on: § 1786.29 for the [LINK]/[ENLACE] placeholders (F12). Subdivision and private right **UNVERIFIED**.

**Fix ¶61.** F13 shows a certification will probably appear. Re-plead § 1681b(b)(1) only if discovery shows the certification was missing, stale, or post-dated. Otherwise drop it and let §§ 1681e(b) and 1786.20(b) carry Count 3 and 4 against Accurate.

**Proposed count outline (against Accurate):**
- Count 3-A § 1681e(b), willful and negligent (§§ 1681n, 1681o)
- Count 3-B § 1681i (only if supported)
- Count 3-C § 1681k (only if RFP 3 supports it)
- Count 4-A Civ. Code § 1786.20(b)
- Count 4-B § 1786.29 (if verified)

Willfulness allegations: *Safeco Ins. Co. of Am. v. Burr*, 551 U.S. 47, 57, 69 (2007) (reckless disregard; objectively unreasonable reading). Plead *Lerma* as notice only (README:78).

**Limitations.** § 1681p: 2 years from discovery (Oct. 14, 2026), so no urgency. ICRAA § 1786.52 period **UNVERIFIED**; check it.

---

## 5. Rule 45 subpoenas: topic lists, not papers

**Common mechanics:**
- No discovery from any source before Nov. 6 (Rule 26(d)(1)).
- Get a protective order first, so vendors can't hide behind confidentiality.
- Ask Accurate first: vendor data Accurate can demand under contract is within its Rule 34 "control" (Set Two Nos. 25–30). Subpoena only if Accurate says it lacks control.
- The clerk issues a signed blank subpoena to a pro se party (Rule 45(a)(3)).
- Give the parties notice and a copy **before** service (Rule 45(a)(4)).
- Service must be by a non-party adult (Rule 45(b)(1)).
- Documents only, electronic production. Place of compliance within 100 miles of the recipient (Rule 45(c)(2)(A)). Disputes go to the compliance district (Rule 45(d)(3)), with possible transfer under 45(f).
- Target serving within ~2 weeks after Accurate's Dec. 7 responses.

| | **Tauxbe Data Inc.** (Mount Holly, NC; FD:50–61) | **InformData – SJV & Associates** (Kennesaw, GA; FD:36–46) | **Infinity Court Research & Retrieval** (Santa Fe Springs, CA; FD:30–34) |
|---|---|---|---|
| Already shown | Vendor for #496623723; source NSOPW; "NO RECORD FOUND"; completed 7/7; no names shown (FD:952–960; R14:317–325) | Request payload: NEWANSORBI/NGWA, county Santa Clara, `years_searched: 0`, AKAs (FD:1246–1262); result C1761642 reported Oct. 14 | Response JSON: 3 DOB-only cases, not reported (FD:1124–1244) |
| Missing | Request and response payloads; candidate list; match logic; timestamps; any "possible match" withheld; any re-query during the dispute | Response payload; court-runner notes; retrieval dates; reasons for the 99 days; source of "currently on parole"; images | Request payload (names sent); why `identified_by_name: false` |
| Narrowest topics | (1) All data received from or sent to Accurate for order 496623722 / search 496623723; (2) all records returned, including non-matches; (3) the match or confidence logic applied to that query; (4) any later query on the same subject in Oct. 2026 | (1) All data received from or sent to Accurate for 496644204 / C1761642; (2) retrieval and court-runner logs, July 7 – Oct. 14; (3) source documents for disposition, release and parole fields; (4) any communication about delay | (1) The request payload Accurate sent for 496644200; (2) documents sufficient to show the identifier-matching method. **Do not request case contents or dispositions.** |
| Priority / risk | **Highest.** This is the § 290.46 sourcing question. | **High.** Delay and parole. | **Low.** It could confirm records adverse to you. Consider skipping. |

Add a #496623727 database-vendor subpoena once Accurate identifies that vendor (ROG 6). It may matter more than all three of the above.

---

## 6. Nov. 6 Rule 26(f) agenda (30 minutes, Teams, 1:00–1:30 p.m. PT)

| Min. | Item | Say | Don't volunteer |
|---|---|---|---|
| 0–2 | Roll call; record the start time | "This is our Rule 26(f) conference. Under 26(d)(2)(B) the Oct. 19 Accurate requests are deemed served today. I calendar responses for Dec. 7." | Any offer of more time. Answer any extension request with "send it in writing and I'll consider it." |
| 2–5 | Service | Ask for **written** Rule 5(b)(2)(E) email-service consent both ways, confirmed by email today | — |
| 5–9 | Protective order | Propose the N.D. Cal. model stipulated PO (standard, with an AEO tier) and a FRE 502(d) order. Ask that it be filed within 14 days. | That the PO is meant for vendor subpoenas in particular |
| 9–13 | ESI | Native/CSV/JSON with data dictionaries (RFP:95–101); no screenshots in place of data; preserve audit and version logs and vendor payloads; custodians include dispute staff and the account team | The F4 version-rewrite theory in detail |
| 13–16 | Privilege log | Counsel communications after the **July 28, 2026** filing don't need logging. Ordinary-course dispute and screening records are not privileged because counsel was copied (Oct. 14 email cc'd Seyfarth). Everything else gets a Rule 26(b)(5) log. | — |
| 16–19 | Amendment | "I expect to seek leave to add FCRA and ICRAA accuracy claims based on the Oct. 14, 27 and 28 documents. Will Accurate stipulate under 15(a)(2)? I propose an amendment deadline in the scheduling order no earlier than [~90 days after the CMC]." | The parole, conviction-question and San Joaquin facts |
| 19–21 | No stay or phasing | Discovery proceeds despite the Nov. 18 partial MTD (Claims 1–4 are unchallenged as to both defendants). No bifurcation of willfulness discovery. | — |
| 21–24 | Discovery plan (Rule 26(f)(3)) | ROGs and RFAs served today; third-party document subpoenas to vendors identified in Accurate's file; no change to Rule 30/33 limits; 30(b)(6) later | Which vendors, or the order you will subpoena them in |
| 24–27 | Initial disclosures / ADR | Nov. 24 disclosures including insurance (26(a)(1)(A)(iv)); ADR certification Nov. 10 (Dkt. 9); state an ADR process preference only | **No settlement figures or terms** |
| 27–30 | Joint CMC Statement | Who drafts; exchange of drafts by Nov. 20; include the amendment notice and discovery plan | Agreeing to sign counsel's draft without review |

After the call: send a same-day confirming email summarizing the agreements, the email-service consent, and the Dec. 7 response date. Draft it; don't send it until you've reviewed it.

---

## Flags and items I couldn't verify

1. **Full SSN and DOB are unredacted** in FD:1248–1250 and FD:1637–1640, inside a room the README says is meant for outside LLMs (README:7). I didn't repeat them here. You may want to redact the extract.
2. FD page references are form-feed pages in the text extract (110 breaks), **not** the 202-page PDF. Confirm against the Gmail original before citing anything in a filing.
3. **Krishnan standing order** (joint-letter page limit, redline requirement) comes only from README:60 and INDEX:74. The PDF isn't in the repo.
4. "Amazon said 10/19 it had no results" (00-ANALYSIS:144): no source in the room.
5. **Your parole discharge status and how you answered the conviction question** aren't in the room. Both decide RFP 14 and 15 strategy.
6. **Why the registry search missed you**, given that other CRAs returned a CA registry record (DISP item 2), is unexplained. Possibilities include a name-input error or a Megan's Law posting category. That is exactly what the Tauxbe and #496623727 discovery should answer; don't plead a cause yet.
7. Dkt. 2 headers read "3:26-cv-09249-ASK" (CMP:1, 7); later papers read "4:26." Probably a division assignment change. Use 4:26.
8. Statutory points marked UNVERIFIED (§ 1786.29 subdivision, § 1786.50(a) "knowing" floor, § 1786.52 period, § 1786.16(a)(4) certification) should go through the citation-verify skill before anything is filed. The cases I cite are real and in my knowledge: *Foman*, *Johnson v. Mammoth*, *Pickern*, *Guimond*, *Carvalho*, *Safeco*, *TransUnion v. Ramirez*, *Connor*. I didn't pull pin cites from a database in this session; CourtListener isn't authorized here.

Nothing here has been filed, served or sent. All drafts need your review first.