# Hertz / HireRight — merged timeline

**Timezone:** America/Los_Angeles (PDT in 2026). HireRight footer: “All times listed in US/Pacific timezone” (`ocr/p-16.txt`).  
**Sources merged:** (1) 28 `.eml` Date headers in `evidence/messages/`; (2) the October 31 report via `evidence/ocr/p-NN.txt` and `evidence/HireRight_Report_Forensic_Review.md`; (3) live Matter 43 `events.jsonl` / workshop for items that exist only as screenshots (iMessages) and are not in the email dump.

**Method:** email times are the RFC Date header converted to PT. Report times are the strings printed on the page. Where INDEX.md, the forensic review, and the OCR disagree, the PDF / Date header wins and the conflict is noted.

This is a chronology, not a claim chart. Hertz has not issued a hiring decision.

---

## Key-fact verification (the eight points requested)

| # | Requested fact | Result | Grounding |
|---|---|---|---|
| 1 | Offer Oct 22, 2026 **3:38 PM PT** | **VERIFIED** | `messages/2026-10-22_1538_bnn.cdl_Following-Up-On-Your-Application-with-Hertz_2e133c.eml` — From Gloria Williams `<careers@hertz.com>`; Date `Thu, 22 Oct 2026 22:38:34 +0000` = **15:38:34 PDT**. Body: “the Manager Trainee role you recently interviewed for in Palo Alto… The team would like to extend an offer.” Formal Hertz Careers offer-extended mail is one minute later (15:39:03 PDT). |
| 2 | Acceptance **4:49 PM** | **VERIFIED** | `messages/2026-10-22_1649_bnn.cdl_Re-Following-Up-On-Your-Application-with-Hertz_6813d5.eml` — From Brendan Ngwa Nforbi; Date `Thu, 22 Oct 2026 16:49:01 -0700`. Body: “I happily accept the offer for the Manager Trainee position.” Portal confirmation email is **17:00:15 PDT**, not 4:49. Both are real; 4:49 is the applicant’s acceptance to Gloria. |
| 3 | HireRight request **Oct 23** | **VERIFIED** | Gloria Williams pre-boarding `…43711-Manager-Trainee_dfd6dd.eml` Date `Fri, 23 Oct 2026 19:37:24 +0000` = **12:37:24 PDT**. HireRight request `…Background-Verification-Request-for-Br_ae64b4.eml` Date `Fri, 23 Oct 2026 12:37:48 -0700`. Report p. 3: “Date Request Submitted: Oct 23, 2026 **3:04 PM PDT**” (consent/order submit, not the noon invitation). Request #: **OR-102326-NH87V**. |
| 4 | “Brendan Ngwa” **not in registry Oct 25** | **VERIFIED** | `ocr/p-08.txt` NSOR subrequest 2: Result **Not in Registry**; “Time Completed: Oct 25, 2026 4:16 PM PDT”; name line **Brendan Ngwa**; comment Oct 25 1:04 PM “search performed through the United States Department of Justice.” |
| 5 | Santa Clara **Court Record Found C1761642 Oct 30 9:10 AM** | **VERIFIED** | `ocr/p-11.txt` item 5: “Newanforbi, Brendan Ngehsi” / “Complete - Court Record Found”; “Time Completed: Oct 30, 2026 9:10 AM PDT”; “Case Nbr.: C1761642”; “Confirmation: Name, Date Of Birth. NAME ON FILE (Newanforbi, Brendan Ngehsi).” |
| 6 | “APPLICANT IS LISTED ON THE SEX OFFENDER REGISTRY IN THE STATE OF CA” **Oct 30 9:17 AM and 12:45 PM** | **VERIFIED** | `ocr/p-08.txt`: “Oct 30, 2026 9:17 AM PDT - Satish Kumar R - Note: APPLICANT IS LISTED ON THE SEX OFFENDER REGISTRY IN THE STATE OF CA.” Same page: “Oct 30, 2026 12:45 PM PDT - Kumar Dilip - Note: APPLICANT IS LISTED…” Both sit next to a § 290.46 employment-use warning (9:17 AM on p. 8; 12:46 PM on `ocr/p-09.txt`). |
| 7 | **In Registry** Oct 30 **11:25 AM** and **12:48 PM** | **VERIFIED** | `ocr/p-08.txt` subrequest 1: “In Registry” / “Time Completed: Oct 30, 2026 11:25 AM PDT.” Subrequest 3: “In Registry” / “Time Completed: Oct 30, 2026 12:48 PM PDT” / “Brendan Ngehsi Newanforbi.” Product table p. 4 shows two “In Registry” rows and one “Not in Registry.” |
| 8 | Adjudication still **Undefined**, ETA **Nov 4** | **VERIFIED, two separate printed facts** | **Undefined / Pending (still open):** `ocr/p-03.txt` Managed Adjudication 3.0 **Pending**; “Request Completion Date:” blank; footer “Completed:” blank every page. `ocr/p-05.txt` MVR **Undefined**; one Court Records row **Undefined**. `ocr/p-06.txt` two National Sex Offender Registry rows **Undefined**; Widescreen row **Client Review Required**. `ocr/p-15.txt` Adjudication 3.0 Result **Pending**. **ETA Nov 4:** `ocr/p-08.txt` Satish Kumar R delays Oct 30 **10:24 AM** (NSOR #3) and **10:31 AM** (NSOR #1): “Estimated Completion Date:04-Nov-2026.” Those two NSOR subrequests then **completed the same day** (11:25 AM and 12:48 PM). Nov. 4 is therefore a **superseded search-delay ETA**, not a printed Hertz decision date and not a court clock. Overall adjudication remains open as of the Oct. 31 print. |

---

## September 2026 — applications and interview scheduling

*Source: email dump only. Not in live `events.jsonl`.*

| PT time | Event | Evidence |
|---|---|---|
| Sep 9, 17:12:43 | Hertz Careers one-time passcode (“Confirm your identity”) | `…1712…4c5b40.eml` |
| Sep 9, 17:15:46 | Application receipt: **Part Time Driver - 42215** | `…1715…674f76.eml` |
| Sep 9, 17:20:52 | Application receipt: **Manager Trainee - 42537** | `…1720…2ef30d.eml` |
| Sep 9, 17:22:47 | Application receipt: **Manager Trainee - 42544** | `…1722…bf508d.eml` |
| Sep 15, 09:18:15 | “Schedule your interview for the job Manager Trainee” | `…0918…2b41e0.eml` |
| Sep 15, 10:35:15 | Confirm your identity | `…1035…d93046.eml` |
| Sep 15, 10:36:23 | Interview scheduled **9/16/26 11:00 AM PDT**, web conference; interviewer Ankit Joshi; recruiter Ninibeth Lopez; links job **42537** (INDEX.md summary; confirm in that `.eml` if quoting) | `…1036…c48e9f.eml` |
| Sep 15, 10:42:54 | Confirm your identity | `…1042…c254f8.eml` |
| Sep 15, 11:41:18 | Another schedule-interview invitation | `…1141…6f16d6.eml` |
| Sep 16, 07:20:52 | Schedule-interview invitation | `…0720…86054c.eml` |
| Sep 24, 08:34:50 | Schedule-interview invitation | `…0834…bc67d3.eml` |
| Sep 29, 12:32:04 | Schedule-interview invitation | `…0a596f.eml` |

The later offer is requisition **43711**, not 42537/42544. The September series is prior application traffic, not the accepted offer.

---

## October 21–22, 2026 — interview and accepted offer

| PT time | Event | Evidence | In live graph? |
|---|---|---|---|
| Oct 21 ~12:27 p.m. (screenshot “Yesterday”) | Kathleen HERTZ iMessage: interview at Hertz Ridder Park, 725 Ridder Park Dr., San Jose. Text says “Thursday 10/21 at 1pm” — **weekday/date conflict in 2026; do not silently correct.** | Matter 43 e01 / `events.jsonl` first row. **Not in the email dump.** | Yes |
| Oct 22, 10:14:44 | Applicant emails the Hertz Generalist resume to a print shop (no subject). Not a Hertz decision. | `…1014…ec398b.eml` + `attachments/…/Brendan_Nforbi_Hertz_Generalist_Resume.pdf` | No |
| Oct 22, 13:03 | Applicant iMessage: rain/traffic delay. | e01 / events.jsonl | Yes |
| **Oct 22, 15:38:34** | **Gloria Williams offer forecast** (key fact 1). | `…1538…2e133c.eml` | Yes (15:38) |
| Oct 22, 15:39:03 | Hertz Careers: “the job offer Manager Trainee is extended to you!” | `…1539…57d832.eml` | Yes |
| Oct 22, 15:40 | Kathleen iMessage: offer for Palo Alto Manager Trainee should arrive. | e02 / events.jsonl. **Not in the email dump.** | Yes |
| **Oct 22, 16:49:01** | **Applicant accepts to Gloria** (key fact 2). | `…1649…6813d5.eml` | Yes |
| Oct 22, 16:58:02 | Confirm your identity (portal OTP) | `…1658…e51963.eml` | No |
| Oct 22, 17:00:07 | Additional information required (Oracle / application fields) | `…1700…f2820d.eml` | Yes |
| Oct 22, 17:00:14 | ADP WOTC questionnaire — **Hertz Global Holdings, Inc.** | `…1700…103c42.eml` | Yes |
| Oct 22, 17:00:15 | Hertz Careers: “you accepted the job offer Manager Trainee!” | `…1700…ef8932.eml` | Yes |
| Oct 22 (portal snapshot) | Requisition **43711** status Offer Accepted | workshop E07; registered path in documents.json. Bytes not on this tree. | Yes |
| Oct 22, 17:25:44 | Confirm your identity | `…1725…db634e.eml` | No |
| Oct 22, 17:44 (capture) | ADP WOTC confirmation screenshot | events.jsonl; EVIDENCE_INTAKE #09. Not in this email dump. | Yes |

Offer terms (workshop E05 / matter.json; confirm against the registered offer-letter PDF if quoting dollar figures or address): The Hertz Corporation; full-time Manager Trainee; **$23/hour**; 816 San Antonio Rd., Palo Alto; supervisor Kathleen Williams; background / MVR contingency; at-will.

---

## October 23, 2026 — HireRight order, consents, MVR

| PT time | Event | Evidence |
|---|---|---|
| **12:37:24** | Gloria Williams: “Pre-Boarding for Brendan Ngwa Nforbi - **43711** Manager Trainee” — Oracle additional info + HireRight background request. | `…dfd6dd.eml` |
| **12:37:48** | HireRight: “The Hertz Corporation Background Verification Request for Brendan Ngwa Nforbi.” Consent required before processing. | `…ae64b4.eml` |
| 15:03:07 | HireRight sends signed **Screening Disclosure and Authorization**. | `…833463.eml` + matching PDF (hash = intake #17) |
| 15:04:16 | HireRight sends **Other Disclosures and Authorizations** (Gmail RAW truncated; full headers/body in sibling `.md`; attachment complete). | `…74fb6e.RAW-TRUNCATED.eml` + `…74fb6e.md` + PDF (hash = intake #15) |
| 15:04:46 | HireRight sends **Acknowledgement and Authorization**. | `…4d1cb5.eml` + PDF (hash = intake #12) |
| 15:04:46 | “We’ve received your information – further steps may be required.” Request ID **OR-102326-NH87V**. | `…42ee94.eml` |
| **15:04:58** | “MVR Express report provided to The Hertz Corporation” — public-record report provided to **Gloria Williams**, The Hertz Corporation, Estero FL, OR-102326-NH87V. This is the **notice**, not the MVR data. | `…78f635.eml` |

**Report-side timestamps the same afternoon** (`ocr/p-03.txt`, `p-06.txt`, `p-09.txt`, `p-15.txt`; forensic review §2):

| Printed time | Product / log |
|---|---|
| Oct 23 3:04 PM | Report submitted by “Hertz - Pre Employment (Field)”; Date Request Submitted; MVR submitted **and** completed “MVR Record Found”; SSN Trace complete (Experian FileOne; subject **BRENDAN NGWA NFORBI**); Prohibited Parties “Not in Database”; NSOR #1 opened (DOJ); San Joaquin / Sheridan / Federal delay notes |
| Oct 23 3:05 PM | Widescreen #4 **Brendan Ngwa Nforbi** “Completed - no records to report”; Federal #18 (Ngwa, Brendan, D. Wyo.) no record |
| Oct 23 3:06 PM | Remaining federal searches no record |
| Oct 23 3:07 PM | Activity Log: Applicant “Document opened” / result “MVR Express report provided to The Hertz Corporation” |
| Oct 23 3:14–5:21 PM | San Joaquin court #1–4 complete, no record ( #4 after a 4:04 PM delay ETA Oct 27) |
| Oct 23 4:04 PM | Sheridan delay notices (ETA Oct 26) |

**MVR contents (first time in the repo)** — `ocr/p-06.txt` / `p-07.txt`: name returned **NGWANFORBI, BRENDAN NGEHSI**; CA Class C, issued Jul 21, 2026, expires May 12, 2027, **VALID**, LICTYPE PERSONAL, Non-CDL. Driving record includes SUSP (chemical-test refusal, reinstated May 19, 2026), DISQ labeled “REFUSED TO SUBMIT TO TEST - CMV” (ClearDate Nov 30, 2025; note “MAILED, NOT RETURNED UNCLAIMED”), and a Jul 3, 2024 registration VIOL. Adjudication ruleset name includes **“Excl. MVR”**; MVR row is **Undefined**.

Live `events.jsonl` stored the MVR notice as **15:05**. The `.eml` Date is **15:04:58**. Treat 3:05 p.m. in older Matter 43 prose as a one-second rounding, not a second event.

---

## October 25–29, 2026 — Santa Clara / NSOR subrequests added; “Brendan Ngwa” clear

*Report only. No emails in the dump for these days. INDEX.md: no Hertz-tied “registry” or pre-adverse mail in bnn.cdl@gmail.com.*

| Printed time | Event | Page |
|---|---|---|
| Oct 25 1:01 PM | Santa Clara court #7 (Ngwanforbi) opened; county delay note (ETAs can exceed 7 days) | p. 12 |
| Oct 25 1:04 PM | Santa Clara court #6 (Ngwa, Brendan) opened; **NSOR #2 (Brendan Ngwa)** opened via US DOJ | pp. 8, 12 |
| Oct 25 1:07 PM | Santa Clara court #5 (**Newanforbi**) opened; **NSOR #3 (Brendan Ngehsi Newanforbi)** opened via US DOJ | pp. 8, 11 |
| Oct 25 1:14 PM | Santa Clara #6 and #7 complete — **No Court Record Found** | p. 12 |
| Oct 25 1:46 PM | Court #5 delay; email to requestor; ETA Oct 26 | p. 11 |
| Oct 25 1:53 PM | Widescreen #1 (no name printed) — no records | p. 9 |
| **Oct 25 4:16 PM** | **NSOR #2 Brendan Ngwa — Not in Registry** (key fact 4) | p. 8 |
| Oct 26 5:37 AM | Widescreen #3 Brendan Ngwa — no records | p. 9 |
| Oct 26 6:53 AM | NSOR #3 delay, **S Arun**, ETA Oct 29 | p. 8 |
| Oct 26 7:06 AM | Sheridan court delay, ETA Oct 29 | pp. 12–13 |
| Oct 26 7:14 AM | NSOR #1 delay, **MudduKrishna S**, ETA Oct 29 | p. 8 |
| Oct 26 8:07 AM | Court #5 delay, ETA **Nov 2** | p. 11 |
| Oct 26 2:26 PM | Sheridan #8–11 complete — no record | pp. 12–13 |
| Oct 27 6:39 PM | Activity Log: Applicant opened Background Report | p. 15 |
| Oct 29 8:17 PM | Activity Log: Applicant opened Background Report | p. 15 |

No Hertz “Recipient” or “Background Report opened” row for a company user appears in the Activity Log (`ocr/p-15.txt`, `p-16.txt`). Comments still say “Email notification sent to requestor” on several court delays.

---

## October 30, 2026 — court hit and registry hits

| Printed time | Event | Page |
|---|---|---|
| **9:10 AM** | Santa Clara #5 **Complete - Court Record Found**, case **C1761642** (key fact 5). Count 1: Sexual Penetration By Force/…; Count 2: Assault With Intent To Commit Rape; offense Feb 26, 2017; file Oct 25, 2017; disposition Jan 12, 2018 no contest; sentence 6 years / 317 days credit; parole/release Dec 2, 2020; protective order through 1/12/2028. Labeled “(Past 7 Years Search).” | p. 11 |
| **9:17 AM** | Satish Kumar R: § 290.46 warning **and** “APPLICANT IS LISTED ON THE SEX OFFENDER REGISTRY IN THE STATE OF CA” (key fact 6, first) | p. 8 |
| 9:18 AM | Satish Kumar R: “Verified by Name and DOB.” **No DOB value is printed** (header DOB masked; subrequest 3 “Date of Birth:” blank). | p. 8 |
| 10:24 AM | Satish Kumar R, NSOR #3 delay, **ETA 04-Nov-2026** | p. 8 |
| 10:31 AM | Satish Kumar R, NSOR #1 delay, **ETA 04-Nov-2026** | p. 8 |
| **11:25 AM** | NSOR #1 **In Registry** complete (key fact 7). Printed name BRENDAN / NGEHSI / NEWANFORBI. OCR of aliases on this subrequest is thin (“NFORBI, BRENDAN”); forensic review §3.1 lists additional aliases from the page image — prefer the PDF if quoting the alias list. | p. 8 |
| **12:45 PM** | Kumar Dilip: “APPLICANT IS LISTED…” (key fact 6, second) | p. 8 |
| 12:46 PM | Kumar Dilip: “Verified by Name and DOB.” and the § 290.46 warning | p. 9 |
| **12:48 PM** | NSOR #3 **In Registry** complete (key fact 7). Search name Brendan Ngehsi Newanforbi. Aliases include NEWANFORBI, NGWANFORBI, NGWA-NFORBI. | p. 8 |
| 1:35 PM | Widescreen #2 **Brendan Ngehsi Newanforbi** — “Data found - Please see criminal services, Prohibited Parties or Sex Offender for more details.” Adjudication: **Client Review Required** (yellow). | pp. 6, 9 |

No email in the October 31 Gmail export announces these results to the applicant. INDEX.md: no pre-adverse or adverse-action message, and no Hertz-tied use of the word “registry,” was found in bnn.cdl@gmail.com.

---

## October 31, 2026 — applicant print; adjudication still open

| Time | Event | Evidence |
|---|---|---|
| 2:36 PM PDT | Activity Log: Applicant opened Background Report | `ocr/p-16.txt` |
| 2:38 PM | Browser print header on every page: “10/31/26, 2:38 PM” | all `ocr/p-*.txt` |
| 2:40:59 PM PDT | PDF Created/Modified (Microsoft Print To PDF; Author “Brendan Ngwa Nforbi”); 16 pages; SHA-256 `39482675c88672946eba5d574f1d98839bb0d2a0628f2e800d7ab4e54c2d5142` | forensic review §0; INDEX.md |
| (none printed) | Request Completion Date blank; Managed Adjudication 3.0 **Pending**; several rows **Undefined** (key fact 8) | pp. 3, 5–6, 15 |

The file is an applicant-side web print, not a HireRight-native export. Get a native/certified copy before relying on it in any later filing. Page images from the original forensic pass are **not** in this bundle (only OCR text + the PDF).

---

## Still open after this timeline

| Item | Status |
|---|---|
| Hertz hiring / start / rescission | **No document** |
| Pre-adverse or final adverse notice | **None** in Gmail export or Activity Log |
| Hertz user opening the report | **Not shown** (Recipient blank) |
| Native HireRight file / consumer file under the California copy election | **Not in this packet** (election was checked Oct 23) |
| Oracle additional-information task completion | **Unconfirmed** in emails |
| Live Matter 43 graph | Still ends Oct 23 3:05 p.m. MVR **notice** |
| Court / agency deadline of Nov 4 | **None.** Nov 4 is a HireRight NSOR delay ETA that those subrequests outran on Oct 30 |

Do not treat any row above as a reason to draft or file. The next fact that changes posture is Hertz’s decision, a HireRight final adjudication, or a notice to the applicant.
