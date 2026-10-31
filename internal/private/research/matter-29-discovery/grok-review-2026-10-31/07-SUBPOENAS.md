# Rule 45 outlines — not served

Do not serve these before the November 6, 2026 conference. Rule 26(d)(1) bars discovery from any source before the conference, except the early Rule 34 requests already delivered to the parties. A subpoena is discovery.

Rule 45(a)(4) requires notice to the other parties before a document subpoena is served. Give Amazon and Accurate the notice and a copy of the subpoena before it goes to the vendor.

Prefer party discovery first where Accurate has the same documents. Subpoena the vendor for the vendor’s own file: what Accurate sent, what the vendor returned, and the vendor’s transmission log. That is the copy Accurate’s production cannot edit.

Serve after a protective order is in place, or ask the vendor to produce confidential consumer data under the model order. Each subpoena is one consumer, one search, and a short date range. No "all contracts with Accurate."

Places of compliance: the vendor’s stated address below, or a copy service. Confirm the Rule 45 100-mile question before serving a non-party outside California. Tauxbe is in North Carolina. InformData’s letterhead address is in Georgia. Infinity is in Santa Fe Springs, California, and is the cleanest domestic target. For an out-of-district vendor, notice and a place of compliance inside the vendor’s district, or a letter agreement to produce by email to Plaintiff in Stockton, avoids a motion. Do not serve a Northern District subpoena that commands production in Oakland from a North Carolina company.

Time range on all three: June 1, 2026 through October 31, 2026, limited to Plaintiff and the search ID named. The older Target (2025) and Keurig (2022) reports are already in Accurate’s disclosure. Do not subpoena those employers.

## 1. Tauxbe Data Inc. — sex-offender search

**Who.** Tauxbe Data Inc., 106 Main Street, Mount Holly, NC 28120, (704) 951-4333. Named in the October 27 disclosure as the source of the National Sex Offender Database Search for report Y94611404, with the underlying source the National Sex Offender Public Website, U.S. Department of Justice SMART Office. Disclosure extract p. 2, lines 49–61.

**What the disclosure already shows.** Search ID 496623723, type National Sex Offender Database Search, result `NO RECORD FOUND`, completion date 2026-07-07. No names searched are listed. Extract p. 24, lines 952–960. The same blank name block is on the October 14 report extract, p. 10, lines 317–325, and on the revised report, extract p. 199, lines 3280–3284. The 2025 Target sex-offender entry in this file is a different product: "NO REPORTABLE RECORDS," subject name Brendan Ngehsi Ngwa Nforbi, March 19, 2025, and the source line on that older report is Accurate itself / NSOPW, not Tauxbe. Extract p. 50, lines 1607–1616, and cover letter p. 2, lines 82–90.

**Still missing.** The names and identifiers Tauxbe received, the time of the query, the raw NSOPW return, any hit that was scored and dropped, and any re-query after October 14, 2026.

**Documents to ask for.**

1. The request Tauxbe received for search 496623723 or for Accurate order 496623722 / report Y94611404, including every name, date of birth, and identifier.
2. Tauxbe’s response, including no-hit, hit, and error payloads.
3. The transmission log (date, time, sender, recipient) for that search.
4. Any second search for the same consumer between July 7, 2026 and October 31, 2026.

**Do not ask Tauxbe** for a legal opinion on whether Plaintiff is on a registry, or for NSOPW data about anyone else.

## 2. InformData - SJV & Associates, LLC — Santa Clara

**Who.** InformData - SJV & Associates, LLC, 1701 Barrett Lakes Blvd, Suite 380, Kennesaw, GA 30144, (800) 203-0582. Named as the Santa Clara source, and the disclosure also prints the court: Superior Court of California, County of Santa Clara, 190–200 W. Hedding St., San Jose. Extract p. 1, lines 35–46.

**What the disclosure already shows.** Search 496644204, felony/misdemeanor, `RECORD FOUND`, completed 2026-10-14. Names searched on the report face include `NGWA NFORBI` / `NEWANSORBI`. Extract p. 18, lines 741–750. The vendor JSON’s principal name is `first_name` `NEWANSORBI`, `middle_name` `Ngehsi`, `last_name` `NGWA`, with `county` `SANTA CLARA` and a Stockton street address. Extract p. 31, lines 1248–1262. The report then recites case C1761642 and the parole sentence language. Extract pp. 18–19. Pages after the JSON are headers only in the text extract (lines 1263–1268). The court-return images are **UNVERIFIED**.

**Still missing.** The full request as InformData logged it, the court runner’s return, the images behind those blank pages, and why a July 7 order completed on October 14.

**Documents to ask for.**

1. The search order InformData received for search 496644204, including the name fields.
2. InformData’s return to Accurate, including court documents and images for case C1761642.
3. Status messages between July 7, 2026 and October 14, 2026 that state why the search was open.
4. The log line that transmitted `NEWANSORBI` as a first name.

**Separate from the vendor.** A Santa Clara Superior Court record request for case C1761642 is a public-record request, not this subpoena. Use it to test whether the minute order contains the words "CURRENTLY ON PAROLE." Do not treat the vendor subpoena as a substitute for reading the court file.

## 3. Infinity Court Research & Retrieval — San Joaquin

**Who.** Infinity Court Research & Retrieval, 12631 Imperial Highway, Suite B-210, Santa Fe Springs, CA 90670, (844) 657-6905. Named as the San Joaquin source for the Amazon report. Extract p. 1, lines 29–33. California address. This is the subpoena to serve first if only one goes out in November.

**What the disclosure already shows.** Search 496644200, result on the report `NO RECORD FOUND`, completed 2026-09-03, names searched include the NEWANSORBI alias. Extract p. 18, lines 718–732. The raw JSON contains three cases, each `identified_by_name` false and `identified_by_dob` true, name Brendan Ngehsi Newanforbi, `dob_on_file` 09/16/1996:

| Case | File date | Extract |
|---|---|---|
| STK-CR-FMISC-2020-0002397 | 2020-02-27 | p. 28, lines 1131–1134 |
| STK-CR-FMISC-2020-0004747 | 2020-05-13 | p. 28–29, lines 1169–1172 |
| STK-CR-FMISC-2025-0004687 | 2025-04-24 | p. 29, lines 1207–1210 |

Charge descriptions are `N/A`. Do not describe the cases as convictions in the subpoena.

**Still missing.** The parameters Infinity was given (which names), Infinity’s cover transmission, and any instruction from Accurate to return DOB-only matches or to suppress them.

**Documents to ask for.**

1. The search request Infinity received for search 496644200.
2. Infinity’s complete return, including the three case numbers above.
3. The transmission email or portal log to Accurate, with date and time.
4. Any instruction or profile stating how a date-of-birth-only match should be flagged.

## Order of operations

| When (Pacific) | Step |
|---|---|
| Fri. Nov. 6, 1:00 p.m. | Tell both firms subpoenas to these three vendors are coming, limited to this consumer and these search IDs. Do not negotiate the scope down to "whatever Accurate produces." |
| Week of Nov. 9 | Serve Infinity after notice under Rule 45(a)(4). Infinity is in California. |
| After the protective order, or with a confidentiality designation | Serve InformData and Tauxbe at a place of compliance in their own districts, or by agreed email production. |
| Do not wait for Accurate’s December responses to serve Infinity | Accurate’s copy and Infinity’s copy are different documents. Waiting lets a vendor retention window close. Civil Code § 1786.20(b)’s two-year retention binds Accurate, not Infinity. |

If Accurate produces the raw Tauxbe file with Set One, narrow the Tauxbe subpoena to transmission logs only. Do not withdraw it in advance.
