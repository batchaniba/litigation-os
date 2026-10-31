# Source register

Page numbers for the three text extracts are form-feed pages: page = 1 + the number of form-feed characters before the quoted line. `sources/README.md` describes the disclosure extract as 202 pages and the closing letter as 25 pages. The disclosure file contains 202 form feeds and the letter file contains 25. The original disclosure PDF is not in the repo. Confirm any page image against that PDF before a filing or a request for admission attaches it.

Line numbers are the text-extract lines (split on newline only; a form feed does not start a new line number).

## Facts used in this review

| Fact | Where |
|---|---|
| Disclosure cover dated October 27, 2026. Accurate says it **received requests** for a report for Amazon on July 7, 2026 and for Target on March 19, 2025. That sentence is the order date, not a furnishing date. The Amazon report is identified as report Y94611404 on October 14, 2026 | `sources/Accurate_File_Disclosure_Oct27.txt` p. 1, lines 1–27 |
| San Joaquin vendor Infinity Court Research & Retrieval, Santa Fe Springs | Same, p. 1, lines 29–33 |
| Santa Clara vendor InformData - SJV & Associates, LLC, Kennesaw; court address on W. Hedding | Same, p. 1, lines 35–46 |
| Sex-offender source Tauxbe Data Inc., Mount Holly, NC; underlying source NSOPW | Same, p. 2, lines 49–61 |
| Report Y94611404, ordered 07/07/2026, updated 10/14/2026 | Same, p. 16, line 632; p. 17, lines 658–660 |
| Alias `NGWA NFORBI, NEWANSORBI`, "Provided by Applicant" | Same, p. 17, lines 675–677. October 14 report extract p. 2, line 42 |
| San Joaquin report face `NO RECORD FOUND`, search 496644200, completed 2026-09-03, names include NEWANSORBI | Disclosure p. 17, line 701; p. 18, lines 718–732 |
| Santa Clara `RECORD FOUND`, search 496644204, completed 2026-10-14, case C1761642 | p. 18, lines 741–755 |
| "CURRENTLY ON PAROLE" twice, date 12/02/2020 | p. 19, lines 777–781 and 803–806. October 14 extract p. 5, lines 140–141 |
| National criminal search 496623727, completed 2026-07-07, names include NEWANSORBI; no raw section elsewhere in the file | Formatted block p. 22, lines 908–916. Revised block p. 198, lines 3229–3236 (three names, no NEWANSORBI). File search for `496623727` hits only those formatted blocks |
| Sex-offender search 496623723, `NO RECORD FOUND`, completed 2026-07-07, no names listed | p. 24, lines 952–960. October 14 extract p. 10, lines 317–325. Revised report p. 199, lines 3280–3284 |
| Previous conviction question answered NO | p. 25, line 1000. Question text mentions current parole at lines 1001–1004 |
| Three San Joaquin cases, all `identified_by_name` false and `identified_by_dob` true, name BRENDAN NGEHSI NEWANFORBI, dob_on_file 09/16/1996, charge description N/A | `STK-CR-FMISC-2020-0002397` p. 28, lines 1131–1134; `STK-CR-FMISC-2020-0004747` p. 28–29, lines 1169–1172; `STK-CR-FMISC-2025-0004687` p. 29, lines 1207–1210 |
| Santa Clara outbound JSON, principal name NEWANSORBI / NGWA | p. 31, line 1248. Further alias tokens lines 1252–1261 |
| July 7, 2026 PACER search of "NGWA NFORBI, NEWANSORBI" | Eastern District p. 39, lines 1292–1296. Same string at lines 1330, 1364, 1398 |
| Last `NEWANSORBI` hit in the extract is line 1398 | Search of the file. The October 28 letter uses the spelling "Newansorbi" at p. 179, line 2461, which is a different capitalization and was a separate search |
| Target 2025 sex-offender entry: no reportable records, March 19, 2025 | p. 50, lines 1607–1616 |
| Target 2025 San Joaquin request uses NFORBI / NGWANFORBI-style aliases, not NEWANSORBI | p. 52, lines 1637–1648 |
| Keurig 2022 AccurateReach arrest hit: matching IDs DOB and APX_NAME, name match BRENDAN N NEWANFORBI, Santa Clara Sheriff, booking 2018-01-22 | p. 64, lines 1822–1830. This is a surname match in an older product, not the 2026 first-name token |
| October 28 letter text begins inside the disclosure extract | p. 178–179, lines 2442–2467, after a run of 92 form feeds on line 2442 (image-only pages). Letter date line 2450 |
| Revised report inside that extract drops the alias and still says updated 10/14/2026 | p. 192, line 2983; alias block p. 193, lines 2999–3000; dispute-initiated stamp p. 193, lines 3017–3019 |
| Standalone closing letter: received disputes October 15; alias removed; no reported sex-offender information; revised report forwarded to the employer; procedure description offered on request | `sources/Closing_Letter_1028.txt` p. 2, lines 17–44 |
| Revised national-criminal names on the standalone letter: Ngwa Nforbi / Brendan; NFORBI / BRENDAN; NEWANFORBI / BRENDAN. No NEWANSORBI. Completion date still 2026-07-07 | Closing letter p. 21, lines 790–797 |
| Served RFP text and October 19 proof of service | `sources/RFP_Accurate_Set1.txt` |
| Accurate defenses 1, 2, 5, 8, 10 | Dkt. 21 text, lines 2297–2377, answer pages 38–39 |
| FCRA and ICRAA paragraphs of the complaint | `extracts/Dkt_02_Removal_Exhibits.txt` lines 907–1034 |
| Live dates | `internal/src/data/matters/29/clocks.json` |
| Operative FCRA theory as summarized in the matter record | `internal/src/data/matters/29/matter.json` `key_facts` (includes the *Lerma* correction). The complaint extract controls over the summary where they differ |

## Unverified, or not for a filing yet

| Item | Status |
|---|---|
| Original 34 MB / 202-page disclosure PDF | Not in the repo. Gmail from Seyfarth, October 30, 2026, per `sources/README.md`. Page images, including Santa Clara returns, are unverified. The extract **text** does contain the October 28 letter. Whether the PDF bytes do is unverified. |
| "Amazon said on October 19 it had no results" | In `00-ANALYSIS.md` only. Not found in the discovery packet or the matter-29 text sidecars searched for this review. |
| Time zone of the `2026-10-19 09:42:29` dispute stamp | Not stated on the report. |
| Whether "CURRENTLY ON PAROLE" was copied from a minute order or added by Accurate | Unverified until the image pages or the Santa Clara court file are read. |
| Whether Plaintiff was on parole on October 14, 2026 | Not a fact in this room. Do not plead it. |
| Meanings of San Joaquin `charge_level` 26 and `charge_disposition` 40 and 31 | Unknown. RFP 20 is how to learn them. |
| October 14 preservation-letter text | PDFs not ingested. Do not reconstruct. |
| General Order 71 applicability | Dkt. 9 raises it. Not decided in this review. |
| House OLRC text of §§ 1681e, 1681i, 1681k | Cornell LII retrieved October 31, 2026. OLRC URLs returned 404. Recheck before filing. |
| Application of TransUnion, Safeco, and § 1681t to these facts | Not briefed in this session. Do not add case citations from memory at filing time. |
| Civil Code §§ 1786.20 and 1786.50 | Verified against leginfo.legislature.ca.gov on October 31, 2026. Recheck the posting on the day of filing in case of an intervening amendment. No amendment was shown on the pages retrieved (1786.20 last amended 2010; 1786.50 last amended 2003). |
| Whether a database-only search is an "investigative consumer report" under § 1786.2 | Legal conclusion, unverified here. The complaint already alleges it. |
| Contents of the October 14 FCRA § 1681k notice PDF | File exists at `documents/matter-29/Accurate Background - FCRA 1681k Public Record Notice to Consumer (Amazon HVH, Ref 496623722, Oct 14 2026).pdf`. Not re-read for this review. Do not plead "no notice." |
| SSN and full vendor identifiers inside the JSON | Present in the extract. Not repeated in this review. A protective order should cover them. |

## Foundation statements this review rejects

| `00-ANALYSIS.md` | Correction |
|---|---|
| "San Joaquin returned two NEWANFORBI cases (2020, 2025)" (line 38) | Three cases: two filed in 2020 and one filed in 2025. All date-of-birth only. |
| RFP 5 Moderate because § 1681e(b) is unpleaded (line 46) | Strong. The alias was used in this order on July 7. |
| RFP 9 largely satisfied (line 51) | The outbound JSON is in hand. The court return is not readable text. |
| RFP 18 Moderate because of privilege (line 59) | The served request already excludes counsel communications. The activity log is still missing. Strong. |
| Gap list treats §§ 1681e(b), 1681i, 1681k, and 1786.20(b) as one package (line 64) | Add § 1681e(b) and § 1786.20(b), and add § 1786.20(a) to the certification count. Hold § 1681i and § 1681k. |
| "Amazon said 10/19 it had no results" (line 44) | Unverified. |
