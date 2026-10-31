# Re-rating of Accurate RFP Set One

Served text: `sources/RFP_Accurate_Set1.txt` (proof of service dated October 19, 2026; email and first-class mail; deemed served at the first Rule 26(f) conference under Rule 26(d)(2)). Foundation ratings: `00-ANALYSIS.md` lines 40–60.

Labels: **FACT** is in a cited file. **INFERENCE** is a conclusion from those facts. **UNVERIFIED** is not established by a file in this room.

## What the pleadings actually put in issue

Count 3 against Accurate is 15 U.S.C. § 1681b(b)(1): furnishing a consumer report for employment without the user's certification, plus a willfulness allegation under § 1681n. Complaint ¶¶ 61–63, Dkt. 2 exhibit extract at the complaint's page 17 (removal exhibit header "Page 18 of 28"), `extracts/Dkt_02_Removal_Exhibits.txt` lines 907–945. Sections 1681e(b), 1681i, 1681g, and 1681k are not pleaded.

Count 4 pleads Civil Code §§ 1786.16 and 1786.40 and "without ensuring" user compliance. ¶¶ 64–70, complaint pages 18–20, extract lines 963–1034. Section 1786.20 is not pleaded. No CCRAA count.

Accurate's answer, Dkt. 21, pages 38–39 (`documents/matter-29/Dkt 21 - Accurate Background Answer and Affirmative and Other Defenses (Filed Sep 22 2026).txt` lines 2297–2389):

| Defense | Plea | What the new papers do to it |
|---|---|---|
| 1 | Has not prepared a consumer report or investigative consumer report | Under cut. The file contains Background Report Y94611404, ordered 07/07/2026, updated 10/14/2026. Disclosure extract p. 16, line 632; p. 17, lines 658–660. |
| 2 | Has not reported any information about registry status | Still a live defense on the **registry-status** theory. The sex-offender component says `NO RECORD FOUND`. Extract p. 24, lines 952–960. A court conviction for a sex offense is not, by itself, a registry report. *Lerma* is the caution already in `matter.json`. |
| 5 | Good faith and an objectively reasonable reading of the law, against punitives | Open. The alias and the day-one search of that alias are the willfulness facts. |
| 8 | State-law claims preempted by § 1681h(e) | A defense to privacy, negligence-style, and IIED theories. It is not a defense to the FCRA count. Broader § 1681t preemption of ICRAA is **UNVERIFIED** in this session. Do not concede it and do not ignore it. |
| 10 | Accurate made no hiring decision | Fits the pleaded adverse-action facts, which are Amazon's. It does not answer a CRA accuracy or certification claim. |

Amazon's motion (Dkt. 19) challenges claims 5–7 only. Claims 1–4 are live as to both defendants. `claims.json`; `clocks.json` id `29-hearing-mtd`.

## Common objections, and the cure

Trade secret and confidentiality will be aimed at RFPs 8, 16, and 20. The cure is the Northern District model protective order, with one change: Plaintiff is pro se, so an attorneys'-eyes-only tier that he cannot see cannot be the tier for the agreement, the certification, or the matching rules. Source code and price lists can be staged. That is a conference term, not a served objection.

Native-format burden is already answered by Instruction 5 of the served set (CSV/JSON/native, no screenshot substitute). `RFP_Accurate_Set1.txt` lines 95–101.

"Unpleaded claim" is a weak relevance objection. Rule 26(b)(1) covers facts of the pleaded screening and the pleaded defenses. The alias was used in this order. It is not a different transaction.

## Ratings

Foundation grade, then this review. "Agree" means the grade and the reason both hold.

| RFP | Foundation | This review | Why |
|---|---|---|---|
| 1 | Strong | **Agree. Strong.** | Order audit history is not in the disclosure. The two report faces (alias in, alias out) make the version IDs necessary. |
| 2 | Strong | **Agree. Strong.** | RFP 2 is the request that captures the post-October 28 face. Both faces still say `updated on 10/14/2026`. Extract p. 17, line 660; revised face, extract p. 192, line 2983, and `Closing_Letter_1028.txt` p. 15, line 544. |
| 3 | Strong | **Agree. Strong.** | No furnishing or access log is in the disclosure. The October 28 letter says a revised copy was forwarded to the employer. `Closing_Letter_1028.txt` p. 2, lines 28–29. The foundation sentence "Amazon said 10/19 it had no results" is **UNVERIFIED**. It is not in the discovery packet, the extracts, or the matter-29 text sidecars searched for this review. |
| 4 | Strong | **Agree. Strong.** | Amazon intake is missing. "Provided by Applicant" is a label on the report, not the intake file. Extract p. 17, lines 675–677. |
| 5 | Moderate | **Disagree. Strong.** | The foundation discounted it because § 1681e(b) is unpleaded. The string was on the July 7 federal searches: PACER receipts for "NGWA NFORBI, NEWANSORBI," transaction date 2026-07-07. Extract p. 39, lines 1292–1296 (Eastern District; the same pattern is in Northern, Southern, and Wyoming). It is the principal `first_name` / `last_name` on the Santa Clara vendor request. Extract p. 31, line 1248. Provenance is relevant to Defense 1, Defense 5, the pleaded certification count (who supplied the name Amazon certified), and Penal Code § 290.46 (what was queried). Amend so the count matches the proof. Do not wait on the amendment to ask for the audit trail. |
| 6 | Strong | **Agree. Strong.** | The sex-offender component lists no names. Extract p. 24, lines 952–960. Neighboring components do. The Santa Clara JSON also contains alias splits that the report face does not list (`NGWANFORBI`, `NGWA`, `NFORBI`, `NGWA-NFORBI`). Extract p. 31, lines 1252–1261. |
| 7 | Strong | **Agree. Strong.** | Search 496623723 is a status line: `NO RECORD FOUND`, completed 2026-07-07, no parameters, no vendor return. The disclosure cover names Tauxbe Data Inc. and NSOPW as the source. Extract p. 2, lines 49–61. That is the identity of the vendor, not the search. |
| 8 | Moderate, too narrow | **Agree.** | "limited to those applied to" this order is an objection in the request. Matching, normalization, alias-generation, and the rule that prints "Provided by Applicant" are the policies. Trade secret is cured by the protective order, not by narrowing the request in advance. Redline in `02-REDLINES.md`. |
| 9 | Moderate, largely satisfied | **Disagree. Still live.** | Satisfied only as to the outbound subject JSON. The following Santa Clara pages are headers with no extracted body. Extract lines 1263–1268. The court return, runner log, and the minute order that may or may not contain "CURRENTLY ON PAROLE" are **UNVERIFIED** until the image pages of the 34 MB PDF are read. |
| 10 | Moderate; delay "unpleaded" | **Agree on Moderate. Disagree that the delay is unpleaded.** | Ordered July 7, completed October 14. Extract p. 18, lines 741–745. That span is the screening the complaint already describes as the hold that preceded the July 27 shift loss. `matter.json` `key_facts`. The request asks for the stated reasons. It does not need a new count. |
| 11 | Moderate; "two" DOB-only cases | **Agree the request stays. The count is three.** | Raw JSON for search 496644200, extract pp. 28–29: `STK-CR-FMISC-2020-0002397` (lines 1131–1134), `STK-CR-FMISC-2020-0004747` (lines 1169–1172), `STK-CR-FMISC-2025-0004687` (lines 1207–1210). Each is `identified_by_name: false`, `identified_by_dob: true`, `identified_by_ssn: false`, name `BRENDAN` / `NGEHSI` / `NEWANFORBI`, `dob_on_file` `09/16/1996`. Charge `description` is `N/A`. The report face says `NO RECORD FOUND`, completed 2026-09-03. Extract p. 18, lines 718–732. The case list is partly produced. The exclusion decision and Infinity's transmission are not. Do not describe these as hidden convictions. The charge text is `N/A`. |
| 12 | Good | **Agree. Good.** | Package review 500363362 is a completed status dated 2026-10-13. Extract p. 22, lines 917–925. No reviewer, no notes, no statement of what was in the file the day before Santa Clara completed. |
| 13 | Strong | **Agree. Strong.** | No ordinary-course notes, holds, or identity-exception tickets are in the extract. The July 7 "Other Information Needed" email is a separate consumer-facing document, not the internal ticket. |
| 14 | Good | **Agree. Good.** | The words `RELEASED FROM PRISON ONTO PAROLE; CURRENTLY ON PAROLE` appear twice in the Santa Clara sentencing block, tied to date `12/02/2020`. Extract p. 19, lines 777–781 and 803–806. Same text on the October 14 report extract, p. 5, lines 140–141. No "date last verified" field is in the extract. Whether Accurate typed the phrase or copied a court minute is **UNVERIFIED** until the Santa Clara image pages are read. Do not plead the phrase as false until parole status in October 2026 is checked. |
| 15 | Good | **Agree. Good.** | `PREVIOUS CONVICTION QUESTION` / `NO` is on the report. Extract p. 25, line 1000. The question text itself asks about convictions, release, and current parole. Lines 1001–1004. Provenance of the answer "No" is not in the disclosure. This is Fair Chance and the pleaded individualized-assessment theory, not only an accuracy theory. |
| 16 | Strong; broaden | **Agree.** | This is the request that matches pleaded § 1681b(b)(1). "parts of" the agreement invites a snippet. The full agreement, the certification, and the adjudication criteria are one subject. Civil Code § 1786.20(a), confirmed on leginfo October 31, 2026, also requires a written agreement and a user certification before an investigative consumer report is furnished. Redline in `02-REDLINES.md`. |
| 17 | Good | **Agree. Good.** | `[LINK]` and `[ENLACE]` appear in the report boilerplate. Extract pp. 15–16, lines 639–656. A placeholder in an extracted PDF does not prove the delivered notice had a dead link. Separate notice PDFs exist under `documents/matter-29/` (FCRA 1681k notice, subject-notification covers, dated Oct. 14, 2026). Compare dispatch time to furnishing time. Do not serve a request that assumes the link failed. |
| 18 | Moderate, because of Seyfarth | **Disagree. Strong for the non-privileged file.** | The served request already excludes attorney-client communications and work product. `RFP_Accurate_Set1.txt` lines 313–317. Privilege is a log, not a reason to grade the request down. The October 28 letter reports a result. It does not include the activity log, the furnisher contacted, or whether 496623723 was run again. The revised report's note says `2026-10-19 09:42:29: Dispute has been initiated`. Extract p. 193, lines 3017–3019; `Closing_Letter_1028.txt` p. 16, lines 578–580. Time zone of that stamp is **UNVERIFIED**. |
| 19 | Strong but narrow | **Agree.** | "screening status, identity inputs, search results, exceptions or delivery" misses eligibility, adjudication, pending, and the forwarding of the revised report. Redline in `02-REDLINES.md`. |
| 20 | Good | **Agree. Good.** | The San Joaquin JSON uses `charge_level` 26 and `charge_disposition` 40 and 31. Extract p. 28, lines 1149–1151, and p. 29. Those codes are unexplained. RFP 20 is how they get read. Do not invent meanings. |

## What Set One already covers, so Set Two should not repeat it

RFPs 1–7, 9–15, and 17 should be left as served. Meet and confer if the responses are thin. Set Two carries the gaps: policies not "limited to those applied," the whole agreement, the dispute activity log in fuller form, Amazon communications about adjudication, the missing raw outputs, and willfulness material outside the July 1–November 15, 2026 window.
