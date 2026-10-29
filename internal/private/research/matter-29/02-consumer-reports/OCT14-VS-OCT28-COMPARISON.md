# Oct. 14 report vs. Oct. 28 revised report

Sources: CR-2026-10-14 (portfolio PDF; line-level from the Oct. 14 accuracy audit) and CR-2026-10-28 (this room's 25-page PDF, pages 15–25 of the packet are the enclosed report). The original PDF controls. Extraction is an aid, not a certification.

Labels: **CHANGED** / **UNCHANGED** / **NEW ON FACE** / **UNVERIFIED** (needs the Oct. 14 PDF open next to this packet).

## Cover / letter (Oct. 28 packet pp. 1–2 only)

| Point | Oct. 14 | Oct. 28 letter | Flag |
|---|---|---|---|
| Document type | Subject notification + report | Consumer Dispute Department letter + enclosed report | NEW ON FACE |
| Date | Notices/emails 10/14/2026 11:58 a.m. PT | Letter dated **October 28, 2026** | NEW ON FACE |
| Dispute receipt date | Dispute **sent** 10/14 1:58 p.m.; SR ack 2:03 p.m. | "We received your disputes on **October 15, 2026**" | NEW ON FACE; conflicts with send/ack dates |
| Items Accurate says were disputed | n/a | (1) AKA 'Ngwa Nforbi, Newansorbi'; (2) National Sex Offender Database Search | Matches the two items in the sent dispute (events.jsonl 2026-10-14) |
| AKA disposition | Present on CR p.2 as "NGWA NFORBI, NEWANSORBI — Provided by Applicant" | "the updated report **removes the AKA above**" | CHANGED |
| NSOR disposition | NO RECORD FOUND (CR p.10) | "There was **no reported information** in the National Sex Offender Database Search on your background check report" | UNCHANGED result; NEW ON FACE as reinvestigation conclusion |
| Employer copy | Oct. 14 notices identify Amazon Salesforce / Amazon HVH | "we have **forwarded a copy of the revised report to the employer** who requested your report" | NEW ON FACE (Amazon receipt UNVERIFIED) |
| Complete file | Requested 10/14 under § 1681g / § 1786.10 | Letter recites rights to inspect / append a statement / get procedure description; enclosures are report + form notices | UNVERIFIED whether this packet is meant as the complete file; on its face it is a reinvestigation result letter plus a report |

## Enclosed report (packet pp. 15–25) vs. Oct. 14 CR

| Field | Oct. 14 (audit) | Oct. 28 enclosed report | Flag |
|---|---|---|---|
| Header screening | Y94611404 | Y94611404 | UNCHANGED |
| Ordered / updated | ordered 07/07/2026 / updated 10/14/2026 | **same** "ordered on 07/07/2026 / updated on 10/14/2026" | UNCHANGED header date (stale relative to the 10/28 letter) |
| Name | Ngwa Nforbi, Brendan Ngehsi | same | UNCHANGED |
| AKA NFORBI, BRENDAN | Provided by Applicant | Provided by Applicant | UNCHANGED |
| AKA NEWANFORBI, BRENDAN | Discovered through Address History | Discovered through Address History | UNCHANGED |
| **AKA NGWA NFORBI, NEWANSORBI** | Provided by Applicant; searched in county/federal/NSOR-adjacent name blocks | **Absent** from AKA table and from NAME(S) SEARCHED blocks in this packet | **CHANGED — deleted** |
| Requestor / REF / package | Amazon HVH; REF ad188d7ed256-40f1-b7f0-e2a7f77aa061; General Package; Fremont, ALAMEDA, CA | same | UNCHANGED |
| RESULT NOTE | (audit does not quote this string) | `***DISPUTE COMPLETED***` / `2026-10-19 09:42:29: Dispute has been initiated` | NEW ON FACE; date is 10/19, not 10/15 or 10/14 |
| Santa Clara | RECORD FOUND; C1761642; completion 2026-10-14; search 496644204 | same | UNCHANGED |
| Charge disp. dates | 10/25/2017 = filing date for counts 1–2 | same | UNCHANGED |
| "CURRENTLY ON PAROLE" / release 12/02/2020 | present | present | UNCHANGED |
| Count 2 blank credit / duplicated $140/$300 | present | present | UNCHANGED |
| San Joaquin | NO RECORD; 2026-09-03 | same | UNCHANGED |
| NSOR | NO RECORD FOUND; ID 496623723; completed 2026-07-07; **no names searched listed** | NO RECORD FOUND; ID 496623723; completed 2026-07-07; still no names-searched block in this extract | UNCHANGED result and completion date |
| Package review | COMPLETED 2026-10-13 | COMPLETED 2026-10-13 | UNCHANGED |
| SSN trace / address history | COMPLETED, no content shown | COMPLETED, no content shown | UNCHANGED |
| Previous conviction question | ANSWER: No | ANSWER: No | UNCHANGED |
| ICRAA [LINK] / [ENLACE] placeholders | present p.1 | present p.15 of packet | UNCHANGED |
| Names searched (post-deletion) | included NEWANSORBI in every search (audit §2 #3) | Last/First: NEWANFORBI/BRENDAN; NFORBI/BRENDAN; Ngwa Nforbi / Brendan / Ngehsi | CHANGED (garbled AKA no longer a search term on this face) |

## What the comparison does **not** show

- Whether Amazon received the revised report, when, who opened it, or whether any hiring decision followed. **UNVERIFIED.**
- Whether any **pre-Oct. 14** version was furnished to Amazon while the BGC was "Pending" (July–October). **MISSING.**
- The source of "NEWANSORBI" or which searches ran under it historically. Deletion is not a source disclosure. The Oct. 14 dispute asked for (c) source and (d) every search run under it.
- Names, identifiers, source database, or run-time for the NSOR component, which the dispute also asked for.
- A complete 15 U.S.C. § 1681g / Civ. Code § 1786.10 file.
- Correction of parole status, disposition dates, address-history content, or the conviction-question answer. Those items were **not** in the two-item Oct. 14 dispute (events.jsonl).
