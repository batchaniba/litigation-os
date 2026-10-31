# Source register, evidence map and verification limits

Private research reference; exclude from all service copies. Repository sources are pinned to commit `800bb4996fdb8cb934937e1437f637b85a09595b` before this review was added. Paths below are exact, repo-root-relative. All source facts in the package refer to these materials, not a live PACER refresh.

## Citation conventions

`C ¶61` means the complaint's paragraph 61, not a finding. `A p. 38:7–8` means the answer's printed/ECF page38 and pleading lines 7–8. For RFPs the page is the nine-page served packet's PDF page, including two proof-of-service pages. `FD p. 31` means the31st form-feed-delimited page of the202-page disclosure extraction, **unverified against the absent original PDF**. “lines” refers to physical newline-delimited text lines on this pinned commit, as counted by `nl -ba`, not a word processor's display wraps. A form feed starts a new PDF page but does not necessarily start another physical text line. Trailing empty form-feed pages are not substantive pages.

## Core source keys

| Key | Exact repository path | Main pinpoint / evidentiary role |
|---|---|---|
| FOUNDATION | `internal/private/research/matter-29-discovery/00-ANALYSIS.md` | Lines20–38: claims, posture and disclosure thesis; lines 40–61: original RFP ratings; lines 63–76: proposed gaps/next steps. Source of views being tested, not independent proof. |
| README | `internal/private/research/matter-29-discovery/README.md` | Workspace instructions and historical posture; do not treat as operative docket. |
| INDEX | `internal/private/research/matter-29-discovery/INDEX.md` | §§ 3–5 docket/discovery map; § 7 absent preservation letters; § 11 exclusions. |
| RFP | `internal/private/research/matter-29-discovery/sources/RFP_Accurate_Set1.txt` | p. 2 instructions, physical lines 65–109; Nos. 1–5 p. 3,121–167; Nos. 6–10 p. 4,175–227; Nos. 11–15 p. 5,233–281; Nos. 16–20 pp. 6–7,291–351; service form pp. 8–9,422–end. |
| RFP-PDF | `internal/private/research/matter-29-discovery/sources/RFP_Accurate_Set1.pdf` | Original nine-page packet; PDF pages4–6 were rendered/visually checked. No. 8 p. 4:11–16; No. 16 p. 6:1–5; No. 18 p. 6:13–18; No. 19 p. 6:20–23. |
| CL | `internal/private/research/matter-29-discovery/sources/Closing_Letter_1028.txt` | p. 2,lines 17–44: receipt, dispute subjects, completed correction, reported forwarding and procedure-description offer; pp. 15–16,543–580: retained update date, removed alias, result note; pp. 17–18,607–692: Santa Clara reported fields. |
| CL-PDF | `internal/private/research/matter-29-discovery/sources/Closing_Letter_1028.pdf` | Twenty-five-page packet; letter on PDF p. 2 visually checked against extract. It says receipt October 15, removes the AKA, says no NSOR information was reported, and says the revised report was forwarded to the requesting employer. It does not prove delivery/access or state the precise completion timestamp. |
| FD | `internal/private/research/matter-29-discovery/sources/Accurate_File_Disclosure_Oct27.txt` | p. 1,lines 1–46: cover date, request dates, Amazon report date, county vendors; p. 2,49–62:Tauxbe/NSOPW; p. 17,676–717:AKA attribution and summary; pp. 18–19,718–805:county results/dates/status; p. 25,952–1008:NSOR no-hit and conviction-question header; pp. 25–26, 1008–1112:question/answer; pp. 28–30, 1124–1245:three raw San Joaquin entries; p. 31, 1246–1262:Santa Clara raw request/variants; pp. 32–37, 1263–1268:image-only text gaps; pp. 39–42, 1275–1410:federal query receipts/variants; pp. 49–50, 1549–1621:Target report; p. 179, 2450–2497:embedded October 28 letter; pp. 192–193, 2982–3019:corrected report/update date/result note. |
| FD-NOTE | `internal/private/research/matter-29-discovery/sources/README.md` | Original disclosure PDF is not in the branch; identifies extraction as202pages and the original as held outside the repo. Does not authenticate the original or its assembly chronology. |
| O14 | `internal/private/research/matter-29-discovery/extracts/Accurate_Consumer_Report_Oct14.txt` | pp. 1–2,lines 24–43:date and original AKA attribution; p. 4,81–115:county components; pp. 5–6,116–167:disposition/release/parole fields; p. 9,282–290:package review; p. 10,299–326:notification components and NSOR result; pp. 11–14,361 onward:conviction question/answer. |
| C | `internal/private/research/matter-29-discovery/extracts/Dkt_02_Removal_Exhibits.txt` | Exhibit 1 complaint: PDF p. 8/complaint p. 7,lines 353–395,¶¶22–25; PDF pp. 9–10,458–475,¶¶28–29 continuation; PDF p. 18/complaint p. 17,907–945,¶¶61–63; PDF pp. 19–20/complaint pp. 18–19,965–1036,¶¶64–70. The combined extract continues with removal exhibits after the complaint; distinguish original complaint facts from later attachments. |
| D9 | `internal/private/research/matter-29-discovery/extracts/Dkt_09_Order_Setting_Initial_CMC.txt` | p. 1,lines 18–43 assignment/GO71/ADR; p. 2,53–69 deadlines. |
| MTD | `documents/matter-29/Dkt 19 - Amazon Motion to Dismiss Fifth Sixth Seventh Claims with Memorandum (Filed Sep 22 2026).txt` | Notice p. 2,lines 130–153:scope; memorandum pp. 1–2,426–523:theory/summary; pp. 3–7,593–779:UCL,privacy, IIED arguments. Arguments, not findings. |
| MTD19-1 | `documents/matter-29/Dkt 19-1 - Amazon Proposed Order Granting Motion to Dismiss (Filed Sep 22 2026).txt` | Proposed order, not entered adjudication. |
| MTD19-2 | `documents/matter-29/Dkt 19-2 - Amazon Certificate of Service of Motion to Dismiss (Filed Sep 22 2026).txt` | Service evidence for motion; distinguish filing/service/receipt. |
| A | `documents/matter-29/Dkt 21 - Accurate Background Answer and Affirmative and Other Defenses (Filed Sep 22 2026).txt` | p. 38:7–25,physical 2299–2335:Defenses 1–6; p. 39:1–21, 2349–2388:Defenses 7–12; p. 40, 2410 onward:service. The answer reproduces allegations while denying/admitting them; quoted allegation text alone is not an admission. |
| OPP | `internal/public/documents/matter-29/Opposition to Amazon MTD with Proposed Order and POS - Unified (N.D. Cal. 4-26-cv-09249-ASK) (Sep 22 2026).txt` | Lines807–877:qualified concessions as to Amazon;935–943:requested disposition; proposed order later in file is not entered. ECF docket number not verified/ingested. |
| REPLY | `internal/private/research/matter-29-discovery/extracts/Amazon_Reply_ISO_MTD_Served_Oct13.txt` | Cover and memorandum pp. 1–4:Amazon's characterization of opposition/claims; certificate October 13. Served copy; ECF number not verified. |
| CLOCK | `internal/src/data/matters/29/clocks.json` | Entries29-deadline-2,29-deadline-3,29-hearing-mtd and 29-rule26f-meet-confer; last entry physical 189–201 contains conference/invitation pointer. Live repo clock, not an independently accessed invitation. |
| DOCKET | `internal/src/data/matters/29/docket.json` | Dkt19 and 21 rows, physical 538–573; mixed related-case rows are not docket entries in this case. Null docket numbers remain null. |
| DOCS | `internal/src/data/matters/29/documents.json` | File inventory used to locate source records; not proof of document contents. |
| OLD-ROG | `internal/docs/matter-29/discovery-set-one/04_Accurate_Interrogatories_Set_One.md` | Nine-question October 19 draft; revised/expanded here, not assumed served. |
| OLD-RFA | `internal/docs/matter-29/discovery-set-one/06_Accurate_RFA_Set_One.md` | Eight-question October 19 draft; revised here. Its specific October 14 receipt proposition is not silently assumed proved. |
| OLD-ESI | `internal/docs/matter-29/discovery-set-one/07_Rule_26f_ESI_Proposal.md` | Historical draft protocol; not an entered order. |
| DISPUTE | `internal/docs/settlement/fcra-file-requests/Accurate Background - Dispute of Accuracy and Request for Complete File, Ref 496623722 (Sent Oct 14 2026).txt` | Non-settlement consumer dispute/file-request text despite folder name. Contains Plaintiff's assertions/requests, not Accurate's admission or proof of every assertion. |
| PREP | `internal/private/research/matter-29/10-rule26f-prep/00-26F-PREP-SHEET.md` | Historical conference preparation, checked againstD9,CLOCK and new production. |
| PREP-AGENDA | `internal/private/research/matter-29/10-rule26f-prep/01-AGENDA-AND-TALKING-POINTS.md` | Historical agenda, not actual agreements. |

The original PDFs corresponding to O14,C,D9,REPLY are identified in `internal/private/research/matter-29-discovery/extracts/README.md`. Those sidecars were read; the PDFs control if they differ. The materiality-sensitive image gaps in FD cannot be resolved from those sidecars.

## Comparator keys — allegations, denials, orders kept distinct

| Key | Exact repository path | Pinpoint / limitation |
|---|---|---|
| LERMA36 | `documents/matter-29/lerma-v-amazon/Dkt 36 - ORDER GRANTING Motions to Dismiss - Megan's Law, FCRA, UCL Claims Dismissed (May 26, 2023).pdf` | Original PDF retrieved and text-extracted:pp. 7–9 registry claim;pp. 9–10 derivative FCRA dismissal;pp. 11–13 UCL;pp. 13–14 leave. The order—not the file title—controls. |
| RAN-C | `internal/public/documents/matter-29/rangel-v-accurate/Dkt 01 - Complaint (Aug 1, 2025).txt` | ¶¶20–30,physical 200–270:alleged incorrect criminal identity match, dispute and deletion; not findings. |
| RAN-A | `internal/public/documents/matter-29/rangel-v-accurate/Dkt 08 - Defendant's Answer and Affirmative Defenses (Sep 26, 2025).txt` | Responsive denials/defenses; not an admission that the complaint's allegations occurred. |
| VAR-C | `internal/public/documents/matter-29/varela-v-accurate/Dkt 01 - Complaint (Jan 21, 2026).txt` | ¶¶11–12,physical 133–146:criminal-reporting-age allegations. |
| VAR-A | `internal/public/documents/matter-29/varela-v-accurate/Dkt 13 - Defendant's Answer and Affirmative Defenses (Mar 30, 2026).txt` | Denials/defenses; no same-system or willfulness finding assumed. |
| VAR-26F | `internal/public/documents/matter-29/varela-v-accurate/Dkt 15 - Joint Rule 26(f) Report (Apr 23, 2026).txt` | p. 7,physical 315–334:discovery plans/policies and procedures; not a production order for this case. Financial/settlement discussion is not used. |
| SAN-C | `internal/public/documents/matter-29/santee-v-accurate/Dkt 01 - Complaint (Oct 21, 2025).txt` | ¶¶10–14,physical 125–142:alleged license restriction/repeated dispute; different defect from criminal matching. |
| SAN-A | `internal/public/documents/matter-29/santee-v-accurate/Dkt 14 - Defendant's Answer and Affirmative Defenses (Dec 22, 2025).txt` | Denials/defenses. Rule 68 documents were excluded. |

No settlement amount, negotiation ledger, demand letter, or comparator settlement agreement supports this package. Prior suits can establish notice of an allegation once receipt is proved; they do not establish that the alleged violation happened, the same platform was used, or that this Plaintiff suffered it.

## Other linked docket materials inspected

The following repo PDFs were retrieved through GitHub and text-extracted, without treating routine procedural records as merits findings:

- `documents/matter-29/Dkt 01 - Notice of Removal (Filed Aug 31 2026).pdf`:pp. 1–3,case identity/removal allegations.
- `documents/matter-29/Dkt 06 - Stipulation to Extend Time for Amazon to Respond (Filed Sep 1 2026).pdf`:pp. 1–2,response-extension terms.
- `documents/matter-29/Dkt 07 - Stipulation to Extend Time for Accurate Background to Respond (Filed Sep 2 2026).pdf`:pp. 1–2,response-extension terms.
- `documents/matter-29/Dkt 08 - Accurate Background Corporate Disclosure and Certification of Conflicts (Filed Sep 2 2026).pdf`:p. 2,corporate disclosure. It does not supply entity net worth or insurance.
- `documents/matter-29/Dkt 10 - Proof of Service of Krishnan Standing Orders (Filed Sep 3 2026).pdf`:p. 2,service list; it is not the standing order itself.
- `documents/matter-29/Dkt 11 - Plaintiff's Consent to Magistrate Judge Jurisdiction (Filed Sep 3 2026).pdf`:p. 1,consent form; a duplicate-titled Dkt11 file was also inspected.
- `documents/matter-29/Dkt 13 - Plaintiff's Certification of Conflicts (Filed Sep 9 2026).pdf`:p. 1,party certification.
- `documents/matter-29/Dkt 14 - Accurate Background Consent to Magistrate Judge Jurisdiction (Filed Sep 10 2026).pdf`:p. 1,consent form. Extraction of checkbox marks alone is not substituted for a judicial jurisdiction determination.

The matter index, identity, claims, docket, documents and clocks were read for navigation/consistency. The reviewed repository is not a complete PACER docket or proof that no later order exists.

## Primary legal authorities checked

Legal propositions are conclusions about these authorities, not “facts from the repo.” Check for a later case-specific order before actual service/filing.

| Key | Primary source / pinpoint |
|---|---|
| FRCP | [Official Federal Rules of Civil Procedure, Dec. 1, 2025](https://www.uscourts.gov/sites/default/files/document/federal-rules-of-civil-procedure.pdf):Rules 5(b)(2)(E),6(a),(d),15(a),(c),(d),16(b)(4),26(b)(1),(3),(5),(c),(d),(e),(f),33–36,37(c)(2),45(a),(c)–(f). Rules 16/26's2025 privilege-protocol amendments are included. |
| ASK | [Krishnan Civil Standing Order, Aug. 20, 2026](https://cand.uscourts.gov/sites/default/files/standing-orders/ASK-Civil-Standing-8.20.26.pdf):§ 4,p. 2 amended pleading redline;§ 5,pp. 2–4 live conference/joint statement, model protective order, editable courtesy copies, logs, search process and sanctions procedure. Correct court URL differs from the stale URL in the workspace README. |
| CLR | [N.D. Cal.Civil Local Rules](https://cand.uscourts.gov/rules-forms-fees/local-rules/civil-local-rules):15-1(a)–(d),16-9,37-3,37-4.15-1 requires complete pleading plus redline/highlight exhibits to a leave motion;37-3 defines cutoff and related motion deadline. |
| GO71 | [Official General Order71](https://cand.uscourts.gov/media-library/uploads/general-order/go-71-initial-discovery-protocols-employment-cases-alleging):p. 1 scope/exclusions/thirty-day exchange;pp. 2–5 protocols. Hiring-only exception is stated; no blanket pro se exclusion is stated. Applicability to this mixed case remains unresolved. |
| FCRA-b | [15 U.S.C. § 1681b, OLRC text](https://uscode.house.gov/us/usc/119-121/t15/s1681b/):particularly(b)(1)(A)(i)–(ii),(B),(b)(2),(b)(3). Also verified against the [GPO FCRA compilation](https://www.govinfo.gov/content/pkg/USCODE-2023-title15/html/USCODE-2023-title15-chap41-subchapIII.htm),§ 1681b(b)(1). |
| FCRA-e | [15 U.S.C. § 1681e, OLRC text throughOct.15, 2026](https://uscode.house.gov/us/usc/119-124/t15/s1681e/):(a),(b). |
| FCRA-i | [15 U.S.C. § 1681i, OLRC text](https://uscode.house.gov/us/usc/119-124/t15/s1681i/):(a)(1)thirty-day reinvestigation;(a)(2)furnisher notice;(a)(4)relevant information;(a)(5)correction/reinsertion;(a)(6)notice;(a)(7)fifteen-day procedure description after request. |
| FCRA-k | [GPO FCRA compilation](https://www.govinfo.gov/content/pkg/USCODE-2023-title15/html/USCODE-2023-title15-chap41-subchapIII.htm),§ 1681k(a)(1)–(2):contemporaneous public-record reporting notice **or** strict completeness/currentness procedures. |
| FCRA-g/h/n/o/p | Same GPO compilation,§§ 1681g(a),1681h(e),1681n,1681o,1681p. Used to distinguish file disclosure, preemption, remedies and limitations. Do not treat the2023 compilation's date as a new2026 statutory amendment. |
| FCRA-t | [15 U.S.C. § 1681t, OLRC text throughOct.15, 2026](https://uscode.house.gov/us/usc/119-124/t15/s1681t/):(a),(b)(1)(B),(C),(E),including express grandfather provisions. |
| CA16/CA20 | [Official chaptered SB909,Stats.2010,ch.481](https://www.leginfo.ca.gov/pub/09-10/bill/sen/sb_0901-0950/sb_909_bill_20100929_chaptered.html):§ 1 enacts§ 1786.16 wording, including(a)(2),(a)(4),(b);§ 2 enacts§ 1786.20,including(a),(b). Current codified-section endpoints returned403 during this review; the official chaptered text was reviewed. Current-date codification/case application should be rechecked before filing. |
| CA40 | [Official chaptered AB1068,Stats.2002,ch.1030](https://www.leginfo.ca.gov/pub/01-02/bill/asm/ab_1051-1100/ab_1068_bill_20020928_chaptered.html):§ 6 adds§ 1786.40,including(a)'s adverse-action advice and agency identification. Current codified-section endpoint was unavailable; chaptered text reviewed. |
| CA50 | Civil Code § 1786.50(a)individual damages;(b)grossly negligent/willful punitives;(c)more-favorable-report exception. **Primary codified text could not be retrieved**:official [section endpoint](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1786.50.) returned403; the official 2003 statutes volume exceeded retrieval size. Readable current reproductions corroborated the text, but this remains a primary-source/currency verification item before filing. Do not claim complete primary verification for this section. |
| SAFECO | [Official *Safeco Insurance Co.of America v. Burr*,551 U.S.47(2007)](https://www.govinfo.gov/content/pkg/USREPORTS-551/pdf/USREPORTS-551-47.pdf),pp. 68–70 & n.20:knowing/reckless liability and objectively reasonable statutory interpretation. |
| TRANSUNION | [Official *TransUnion LLC v. Ramirez*,594 U.S.413(2021)](https://www.supremecourt.gov/opinions/20pdf/20-297_4g25.pdf):slipop.pp. 15–27,especially dissemination, internal files and informational injury; reporter pp. 432–42. Concrete injury must be assessed claim by claim. |

No reliance is placed on the initially retrieved2007 *Dennis* opinion; it was amended later and was not necessary to this analysis. Do not cite an outdated version from preliminary search results.

## Evidence-to-draft map

These are research annotations. A discovery request asks the opposing party to supply or admit a fact; it is not Plaintiff certifying that a disputed premise is already true. Keep this map out of the service body.

| Draft items | Source predicate and gap |
|---|---|
| RFP 21/29;ROG 3–4;RFA 7–8,25–26 | O14 p. 2;FD p. 31;CL p. 2:alias/attribution, principal fields and other correct variants;original source remains unknown. |
| RFP 22/25–28;ROG 15–17;RFA 32–36 | C ¶61;A Defenses 5,10–11;RFP 16–17;O14 p. 10:certification, authorization, notice and adjudication issues;actual agreement/forms/notice delivery remain unverified. |
| RFP 23/35;ROG 12–14,21–22;RFA 17–20,27–29 | CL p. 2,pp. 15–16;FD pp. 179,192–193:correction, receipt/initiation dates, report version and employer-forwarding statement;actual investigation and delivery events missing. |
| RFP 24/35/42;ROG 1–2,18–19;RFA 1–2,9,30–31 | C ¶¶22–25;A Defenses 1,3–4,10;FD p. 1;O14 p. 1:chronology, communication, causation;no verified July employer-report content. |
| RFP 30/33;ROG 5–6;RFA 3,10–13 | FD p. 2,p. 25;A Defense 2:vendor/source labels and negative result;query/California source path/result handling not proved. |
| RFP 31/34;ROG 7,9,11;RFA 14–16 | FD pp. 18–19,31–37;O14 pp. 4–6,9:county raw data, dates/currentness, review event;source images and current verification missing. |
| RFP 32;ROG 8;RFA 21–24 | FD pp. 18,28–30:three entries/boolean values versus final no-record result;identity/flag semantics/exclusion rationale not proved. |
| RFP 36–40/43;ROG 20 | C ¶62;A Defenses 5,7;comparator allegations and Lerma order:knowledge/reasonableness/financial condition are subjects to discover, not existing findings of liability or financial facts. |
| RFP 41 | RFP 1–3,6–13,18–20 identify relevant records;retention/loss is a proposed inquiry.No spoliation fact is asserted. |
| RFP 44 | Rule 26(a)(1)(A)(iv);no policy or insurer identity verified.D9's timing/GO71 issue must be resolved. |

## Verification limits and items not to turn into allegations

1. The original 202-page disclosure PDF is absent. Its extraction has image-only pages, including Santa Clara source material, and many empty pages after the older reports. Missing text does not mean missing records. The October 28 packet embedded in an October 27-cover compilation requires assembly provenance.
2. No original Amazon-to-Accurate intake payload, complete applicable agreement, certification, authorization/disclosure acceptance record, July furnishing/access log, full2026 NSOR raw query, or underlying reinvestigation workfile is verified. Absence from this extraction is not proof the item never existed.
3. No competent source in the reviewed text establishes that the current-parole statement was false, that the charge-disposition date is wrong, that a reported conviction was someone else's, or that the San Joaquin entries were reportable criminal convictions.
4. No verified evidence establishes a suppressed California registry hit, or use of California website-derived information in Amazon's employment decision. The existence of a vendor search does not establish either.
5. The source closing letter says receipt October 15;the supplied dispute text is datedOctober14;the revised report notes initiationOctober19. These are distinct events. The2:03 p.m.October 14 acknowledgment is described elsewhere in the workspace, but its original message was not independently rendered in this review. RFA 27 therefore uses “no later thanOctober15.”
6. Set One's packet includes a proof-of-service form, not independently verified delivery/receipt evidence. Confirm actual conference and delivery;do not convert an anticipatedNovember6 date into a completed event. No new discovery from this review has been served.
7. No amended complaint, scheduling order, protective order, or later dispositive ruling was independently verified from a current full docket. The branch inventory/live clocks are the scope of this review. The Rule 15 proposal is not operative.
8. Vendor addresses are addresses disclosed in the consumer file, not verified current service addresses or legal-entity identities.
9. The originalOctober14 preservation letters and a fresh§ 1681i(a)(7)request are not present. Do not reconstruct their content, receipt, or deadlines.
10. Primary§ 1786.50/current California codification verification is incomplete as described above.GeneralOrder71's application to this mixed hiring/consumer-reporting action is unresolved;do not assume either exemption or an already-entered extension.

## Deployment and review checks

This is legal-text work only. The package was checked for numbering, complete request bodies, link targets within the package, source pinpoints, count consistency, PII leakage, and separation of private research from service bodies. No application-code tests or portfolio gate were run; no public registry, deadline graph, event log, Worker, D1,R2,main branch, or existing pleading is changed by this package. No PR was merged or marked ready.
