# Index — Matter 29 Accurate discovery room

Relative links are from `internal/private/research/matter-29-discovery/`.  
Prefer `.txt` / `.md` over PDFs. PDFs control. Do not open settlement, demand, or ledger files.

Companion: [`README.md`](README.md) (identity and rules) · [`00-ANALYSIS.md`](00-ANALYSIS.md) (foundation analysis).

---

## 1. This room

| File | One-line description |
|---|---|
| [`README.md`](README.md) | Case identity, posture, key dates, working rules, how an outside model should read this folder |
| [`INDEX.md`](INDEX.md) | This file map and the suggested follow-up questions |
| [`00-ANALYSIS.md`](00-ANALYSIS.md) | Oct. 31 foundation analysis, verbatim, plus a short workspace header |
| [`SYNTHESIS-3-MODEL.md`](SYNTHESIS-3-MODEL.md) | **Consolidated plan** after the ChatGPT, Claude, and Grok reviews. Controls where they differ |
| [`review-2026-10-31/00-START-HERE.md`](review-2026-10-31/00-START-HERE.md) | ChatGPT review: re-ratings, redlines, Set Two RFPs 21–44, ROGs, RFAs, Rule 15, subpoenas, 26(f) |
| [`claude-review-2026-10-31/claude-work-response.md`](claude-review-2026-10-31/claude-work-response.md) | Claude review, copied from the Oct. 31 upload, not edited |
| [`grok-review-2026-10-31/00-START-HERE.md`](grok-review-2026-10-31/00-START-HERE.md) | Grok review, written from the sources before the other two reviews were opened |
| [`sources/README.md`](sources/README.md) | What was newly attached on Oct. 31, including the missing 34 MB file-disclosure PDF |
| [`sources/RFP_Accurate_Set1.pdf`](sources/RFP_Accurate_Set1.pdf) | Served Plaintiff's First RFPs to Accurate, Set One (Oct. 19, 2026; 9 pp.) |
| [`sources/RFP_Accurate_Set1.txt`](sources/RFP_Accurate_Set1.txt) | Text of the served Accurate RFP set |
| [`sources/Closing_Letter_1028.pdf`](sources/Closing_Letter_1028.pdf) | Accurate Oct. 28 reinvestigation closing letter + revised report (25 pp.) |
| [`sources/Closing_Letter_1028.txt`](sources/Closing_Letter_1028.txt) | Text of the closing letter |
| [`sources/Accurate_File_Disclosure_Oct27.txt`](sources/Accurate_File_Disclosure_Oct27.txt) | Text of Accurate's Oct. 27 file disclosure (202 pp.). **Original PDF is in Gmail from Seyfarth, Oct. 30, 2026 — not in this repo** |
| [`extracts/README.md`](extracts/README.md) | Helper `pdftotext` extracts of repo PDFs that lacked sidecars |
| [`extracts/Dkt_09_Order_Setting_Initial_CMC.txt`](extracts/Dkt_09_Order_Setting_Initial_CMC.txt) | Dkt. 9 CMC / ADR order |
| [`extracts/Dkt_02_Removal_Exhibits.txt`](extracts/Dkt_02_Removal_Exhibits.txt) | Dkt. 2 Exhibit 1 = as-filed Alameda complaint |
| [`extracts/Amazon_Reply_ISO_MTD_Served_Oct13.txt`](extracts/Amazon_Reply_ISO_MTD_Served_Oct13.txt) | Amazon reply ISO Dkt. 19 (served copy) |
| [`extracts/Accurate_Consumer_Report_Oct14.txt`](extracts/Accurate_Consumer_Report_Oct14.txt) | Oct. 14 Accurate consumer report (pre-reinvestigation) |

---

## 2. Live Matter 29 graph

Canonical split siblings. Do not reconstruct a docket from README or from `status` / `procedural_status`.

| File | One-line description |
|---|---|
| [`../../../src/data/index/matters.json`](../../../src/data/index/matters.json) | Portfolio front door; Matter 29 `next_clock` is the Nov. 6 26(f) |
| [`../../../src/data/matters/29/matter.json`](../../../src/data/matters/29/matter.json) | Identity: caption, case no., judge, phase, long `key_facts` (includes the *Lerma* correction) |
| [`../../../src/data/matters/29/clocks.json`](../../../src/data/matters/29/clocks.json) | **Live calendar.** Open: 26(f) Nov. 6; ADR Nov. 10; MTD Nov. 18; disclosures / JCMC Nov. 24; CMC Dec. 1 |
| [`../../../src/data/matters/29/docket.json`](../../../src/data/matters/29/docket.json) | Pleadings inventory (some related-docket rows are mixed in; `dkt: null` means no number ingested) |
| [`../../../src/data/matters/29/documents.json`](../../../src/data/matters/29/documents.json) | File inventory for `documents/matter-29/` |
| [`../../../src/data/matters/29/events.jsonl`](../../../src/data/matters/29/events.jsonl) | Append-only chronology. **Do not rewrite.** Some older rows mention settlement correspondence — skip those |
| [`../../../src/data/matters/29/claims.json`](../../../src/data/matters/29/claims.json) | Seven live counts |
| [`../../../src/data/matters/29/parties.json`](../../../src/data/matters/29/parties.json) | Amazon and Accurate service tracking (both served July 31, 2026) |
| [`../../../src/data/matters/29/counsel.json`](../../../src/data/matters/29/counsel.json) | Stanzick (Seyfarth) and Frederick (Morgan Lewis) |
| [`../../../src/data/matters/29/evidence.json`](../../../src/data/matters/29/evidence.json) | Evidence labels. Skip any opening-demand row |
| [`../../../src/data/matters/29/prose.json`](../../../src/data/matters/29/prose.json) | Narrative status / facts / risk. **Stale in places** (still talks as if defendants have not consented). Skip any demand figure |
| [`../../../src/data/matters/29/damages.json`](../../../src/data/matters/29/damages.json) | Statutory-range narrative and *Lerma* caution. Not a settlement ledger |

---

## 3. Operative pleadings and orders (this case)

Bytes: [`../../../../documents/matter-29/`](../../../../documents/matter-29/). Text first.

| Item | Dkt | Text / extract | PDF |
|---|---|---|---|
| As-filed complaint (Alameda 26CV201554) | Exhibit 1 to 2 | [`extracts/Dkt_02_Removal_Exhibits.txt`](extracts/Dkt_02_Removal_Exhibits.txt) | [`Dkt 02 - Notice of Removal Exhibits 1-11`](../../../../documents/matter-29/Dkt%2002%20-%20Notice%20of%20Removal%20Exhibits%201-11%20%28Filed%20Aug%2031%202026%29.pdf) |
| Notice of Removal | 1 | — | [`Dkt 01 - Notice of Removal`](../../../../documents/matter-29/Dkt%2001%20-%20Notice%20of%20Removal%20%28Filed%20Aug%2031%202026%29.pdf) |
| Amazon extension stip | 6 | — | [`Dkt 06`](../../../../documents/matter-29/Dkt%2006%20-%20Stipulation%20to%20Extend%20Time%20for%20Amazon%20to%20Respond%20%28Filed%20Sep%201%202026%29.pdf) |
| Accurate extension stip | 7 | — | [`Dkt 07`](../../../../documents/matter-29/Dkt%2007%20-%20Stipulation%20to%20Extend%20Time%20for%20Accurate%20Background%20to%20Respond%20%28Filed%20Sep%202%202026%29.pdf) |
| Accurate corporate disclosure | 8 | — | [`Dkt 08`](../../../../documents/matter-29/Dkt%2008%20-%20Accurate%20Background%20Corporate%20Disclosure%20and%20Certification%20of%20Conflicts%20%28Filed%20Sep%202%202026%29.pdf) |
| **Order setting CMC and ADR** | **9** | [`extracts/Dkt_09_Order_Setting_Initial_CMC.txt`](extracts/Dkt_09_Order_Setting_Initial_CMC.txt) | [`Dkt 09`](../../../../documents/matter-29/Dkt%2009%20-%20Order%20Setting%20Initial%20CMC%20and%20ADR%20Deadlines%20%28Filed%20Sep%203%202026%29.pdf) |
| POS of Krishnan standing orders | 10 | — | [`Dkt 10`](../../../../documents/matter-29/Dkt%2010%20-%20Proof%20of%20Service%20of%20Krishnan%20Standing%20Orders%20%28Filed%20Sep%203%202026%29.pdf) |
| Plaintiff MJ consent | 11 | — | [`Dkt 11`](../../../../documents/matter-29/Dkt%2011%20-%20Plaintiff%27s%20Consent%20to%20Magistrate%20Judge%20Jurisdiction%20%28Filed%20Sep%203%202026%29.pdf) |
| Plaintiff conflicts cert | 13 | — | [`Dkt 13`](../../../../documents/matter-29/Dkt%2013%20-%20Plaintiff%27s%20Certification%20of%20Conflicts%20%28Filed%20Sep%209%202026%29.pdf) |
| Accurate MJ consent | 14 | — | [`Dkt 14`](../../../../documents/matter-29/Dkt%2014%20-%20Accurate%20Background%20Consent%20to%20Magistrate%20Judge%20Jurisdiction%20%28Filed%20Sep%2010%202026%29.pdf) |
| **Amazon MTD (Claims 5–7)** | **19** | [`Dkt 19 … .txt`](../../../../documents/matter-29/Dkt%2019%20-%20Amazon%20Motion%20to%20Dismiss%20Fifth%20Sixth%20Seventh%20Claims%20with%20Memorandum%20%28Filed%20Sep%2022%202026%29.txt) | [PDF](../../../../documents/matter-29/Dkt%2019%20-%20Amazon%20Motion%20to%20Dismiss%20Fifth%20Sixth%20Seventh%20Claims%20with%20Memorandum%20%28Filed%20Sep%2022%202026%29.pdf) |
| Amazon proposed order / COS | 19 | [19-1 txt](../../../../documents/matter-29/Dkt%2019-1%20-%20Amazon%20Proposed%20Order%20Granting%20Motion%20to%20Dismiss%20%28Filed%20Sep%2022%202026%29.txt) · [19-2 txt](../../../../documents/matter-29/Dkt%2019-2%20-%20Amazon%20Certificate%20of%20Service%20of%20Motion%20to%20Dismiss%20%28Filed%20Sep%2022%202026%29.txt) | [19-1](../../../../documents/matter-29/Dkt%2019-1%20-%20Amazon%20Proposed%20Order%20Granting%20Motion%20to%20Dismiss%20%28Filed%20Sep%2022%202026%29.pdf) · [19-2](../../../../documents/matter-29/Dkt%2019-2%20-%20Amazon%20Certificate%20of%20Service%20of%20Motion%20to%20Dismiss%20%28Filed%20Sep%2022%202026%29.pdf) |
| **Accurate Answer (12 defenses)** | **21** | [`Dkt 21 … .txt`](../../../../documents/matter-29/Dkt%2021%20-%20Accurate%20Background%20Answer%20and%20Affirmative%20and%20Other%20Defenses%20%28Filed%20Sep%2022%202026%29.txt) | [PDF](../../../../documents/matter-29/Dkt%2021%20-%20Accurate%20Background%20Answer%20and%20Affirmative%20and%20Other%20Defenses%20%28Filed%20Sep%2022%202026%29.pdf) |
| Opposition to Dkt. 19 | **null** (served Sep. 23; no ECF number ingested) | [`Opposition … .txt`](../../../public/documents/matter-29/Opposition%20to%20Amazon%20MTD%20with%20Proposed%20Order%20and%20POS%20-%20Unified%20%28N.D.%20Cal.%204-26-cv-09249-ASK%29%20%28Sep%2022%202026%29.txt) | PDF listed in `documents.json`; bytes not on this checkout — use the text sidecar |
| Amazon reply ISO MTD | **null** (served Oct. 13; served copy only) | [`extracts/Amazon_Reply_ISO_MTD_Served_Oct13.txt`](extracts/Amazon_Reply_ISO_MTD_Served_Oct13.txt) | [PDF](../../../../documents/matter-29/Amazon%20Reply%20ISO%20Motion%20to%20Dismiss%20%28Dkt%2019%29%20-%20Served%20Copy,%20Not%20File-Stamped%20%28N.D.%20Cal.%204-26-cv-09249-ASK%29%20%28Served%20Oct%2013%202026%29.pdf) |

Krishnan Civil Standing Order (Aug. 20, 2026) is **not** stored as a PDF here. Court file: `https://cand.uscourts.gov/sites/default/files/standing-orders/ASK-CivilStandingOrder_8.20.26.pdf`. Working notes: [`../../../docs/legal-intel/judges/ajay-s-krishnan-2026.md`](../../../docs/legal-intel/judges/ajay-s-krishnan-2026.md). Discovery fights: live meet-and-confer, then a **5-page joint letter** (2.5 per side). Amended pleadings need a redline.

---

## 4. Formal discovery (Rule 34 / 33 / 36)

| File | One-line description |
|---|---|
| [`sources/RFP_Accurate_Set1.txt`](sources/RFP_Accurate_Set1.txt) | **Served** Accurate RFP Set One (1–20). Use this, not only the draft |
| [`../../../docs/matter-29/discovery-set-one/README.md`](../../../docs/matter-29/discovery-set-one/README.md) | Packet index. Drafts dated Oct. 19. The packet README still says that PR did not serve; the Oct. 31 analysis treats the Accurate set as delivered |
| [`../../../docs/matter-29/discovery-set-one/00_README_Deployment_and_Checklist.md`](../../../docs/matter-29/discovery-set-one/00_README_Deployment_and_Checklist.md) | Service / 26(d)(2) checklist |
| [`../../../docs/matter-29/discovery-set-one/01_Amazon_RFP_Set_One.md`](../../../docs/matter-29/discovery-set-one/01_Amazon_RFP_Set_One.md) | Parallel early RFP set to Amazon (18 requests). Analysis did not re-rate it |
| [`../../../docs/matter-29/discovery-set-one/02_Accurate_RFP_Set_One.md`](../../../docs/matter-29/discovery-set-one/02_Accurate_RFP_Set_One.md) | Draft Markdown of Accurate RFPs 1–20 |
| [`../../../docs/matter-29/discovery-set-one/03_Amazon_Interrogatories_Set_One.md`](../../../docs/matter-29/discovery-set-one/03_Amazon_Interrogatories_Set_One.md) | Draft Amazon ROGs — **do not serve before Nov. 6** |
| [`../../../docs/matter-29/discovery-set-one/04_Accurate_Interrogatories_Set_One.md`](../../../docs/matter-29/discovery-set-one/04_Accurate_Interrogatories_Set_One.md) | Draft Accurate ROGs — same |
| [`../../../docs/matter-29/discovery-set-one/05_Amazon_RFA_Set_One.md`](../../../docs/matter-29/discovery-set-one/05_Amazon_RFA_Set_One.md) | Draft Amazon RFAs — same |
| [`../../../docs/matter-29/discovery-set-one/06_Accurate_RFA_Set_One.md`](../../../docs/matter-29/discovery-set-one/06_Accurate_RFA_Set_One.md) | Draft Accurate RFAs — same |
| [`../../../docs/matter-29/discovery-set-one/07_Rule_26f_ESI_Proposal.md`](../../../docs/matter-29/discovery-set-one/07_Rule_26f_ESI_Proposal.md) | ESI / native / privilege discussion draft |
| [`../../../docs/matter-29/discovery-set-one/08_Amazon_30b6_Draft_HOLD.md`](../../../docs/matter-29/discovery-set-one/08_Amazon_30b6_Draft_HOLD.md) | 30(b)(6) outline — hold |
| [`../../../docs/matter-29/discovery-set-one/09_Accurate_30b6_Draft_HOLD.md`](../../../docs/matter-29/discovery-set-one/09_Accurate_30b6_Draft_HOLD.md) | 30(b)(6) outline — hold |
| [`../../../docs/matter-29/discovery-set-one/10_Amazon_Service_Record.md`](../../../docs/matter-29/discovery-set-one/10_Amazon_Service_Record.md) | Amazon service-record template |
| [`../../../docs/matter-29/discovery-set-one/11_Accurate_Service_Record.md`](../../../docs/matter-29/discovery-set-one/11_Accurate_Service_Record.md) | Accurate service-record template |
| [`../../../docs/matter-29/discovery-set-one/12_Cover_Email_Templates_NOT_SENT.txt`](../../../docs/matter-29/discovery-set-one/12_Cover_Email_Templates_NOT_SENT.txt) | Cover-email drafts — not a send instruction |
| [`../../../docs/matter-29/discovery-set-one/generated/`](../../../docs/matter-29/discovery-set-one/generated/) | Rendered DOCX/PDF of the Oct. 19 packet |

No interrogatory responses, RFA responses, subpoenas, or deficiency letters exist.

---

## 5. Consumer-file and dispute papers (not Rule 34)

| File | One-line description |
|---|---|
| [`../../../docs/settlement/fcra-file-requests/Accurate Background - Consumer File Request (Sep 25 2026).txt`](../../../docs/settlement/fcra-file-requests/Accurate%20Background%20-%20Consumer%20File%20Request%20%28Sep%2025%202026%29.txt) | § 1681g / § 1786.10 file request — **marked DRAFT, no evidence sent** |
| [`../../../docs/settlement/fcra-file-requests/Accurate Background - Dispute of Accuracy and Request for Complete File, Ref 496623722 (Sent Oct 14 2026).txt`](../../../docs/settlement/fcra-file-requests/Accurate%20Background%20-%20Dispute%20of%20Accuracy%20and%20Request%20for%20Complete%20File,%20Ref%20496623722%20%28Sent%20Oct%2014%202026%29.txt) | Sent Oct. 14, 1:58 p.m. PT; disputed NEWANSORBI and NSOR "No Record Found" |
| [`../../../../documents/matter-29/Gmail - Dispute of Accuracy and Request for Complete File to Accurate Background, Ref 496623722 (Sent Oct 14 2026).pdf`](../../../../documents/matter-29/Gmail%20-%20Dispute%20of%20Accuracy%20and%20Request%20for%20Complete%20File%20to%20Accurate%20Background,%20Ref%20496623722%20%28Sent%20Oct%2014%202026%29.pdf) | Gmail of the same dispute |
| [`../../../../documents/matter-29/Gmail - Accurate Background Support Acknowledgment, Service Request 20261014-15421955 (Received Oct 14 2026 203 PM).pdf`](../../../../documents/matter-29/Gmail%20-%20Accurate%20Background%20Support%20Acknowledgment,%20Service%20Request%2020261014-15421955%20%28Received%20Oct%2014%202026%20203%20PM%29.pdf) | Accurate SR ack, 2:03 p.m. |
| [`../../../../documents/matter-29/Gmail - Accurate Acknowledgment Thread with Forward to Seyfarth (Drury, Stanzick), SR 20261014-15421955 (Oct 14 2026 204 PM).pdf`](../../../../documents/matter-29/Gmail%20-%20Accurate%20Acknowledgment%20Thread%20with%20Forward%20to%20Seyfarth%20%28Drury,%20Stanzick%29,%20SR%2020261014-15421955%20%28Oct%2014%202026%20204%20PM%29.pdf) | Forward to Seyfarth |
| [`extracts/Accurate_Consumer_Report_Oct14.txt`](extracts/Accurate_Consumer_Report_Oct14.txt) | Oct. 14 completed report |
| Oct. 14 notice packet (PDFs) | ICRA notice, FCRA 1681k notice, FCRA summary of rights, CA background-check notice, subject-notification covers, portal screenshot — all under [`../../../../documents/matter-29/`](../../../../documents/matter-29/) with prefix `Accurate Background -` |
| [`sources/Closing_Letter_1028.txt`](sources/Closing_Letter_1028.txt) | Oct. 28 reinvestigation close |
| [`sources/Accurate_File_Disclosure_Oct27.txt`](sources/Accurate_File_Disclosure_Oct27.txt) | Oct. 27 complete-file disclosure (text only) |

The First Advantage file request in the same folder is a different vendor. Ignore it for Accurate work.

---

## 6. Hiring / screening evidence (this application)

Useful PDFs under [`../../../../documents/matter-29/`](../../../../documents/matter-29/):

| File | One-line description |
|---|---|
| `Congratulations on Your Amazon Offer Email (Jul 3, 2026).pdf` | Conditional offer; training July 28–29 and Aug. 4–5 |
| `Confirmed Pre-Hire Appointment Email (Jul 3, 2026).pdf` | Pre-hire set for July 7 |
| `Completed Pre-Hire Appointment Email (Jul 7, 2026).pdf` | Appointment completed |
| `Accurate Background - Notification of Electronic Communication (Y94611404).pdf` | Accurate identifies itself as a CRA for "Amazon Salesforce" |
| `Accurate Background - Other Information Needed (Screening ID 496623722).pdf` | Mid-screening identity-verification demand |
| `Amazon Reference Number Confirmation (Y94611404).pdf` | Order number |
| `Amazon Simple Hire Checklist.pdf` (and `2`, `3`) | Drug test / I-9 complete; background check pending; later "no shift selected" |
| `I-9 Form and Audit Log (SSN redacted).pdf` | I-9 completed July 4 |
| `Information regarding your Amazon application.pdf` (and `2`) | Delay emails |
| `Gmail - Information regarding your Amazon application - Amazon Jobs to brendan@ngwanforbi.com (Oct 14 2026 5.06 AM).pdf` | Application still "in progress" the morning of the Oct. 14 report |

Checkr reports in the same folder are **other** applications (Next Chapter / Nuro), not the Amazon/Accurate screen.

---

## 7. Preservation letter to Seyfarth — **MISSING from repo**

The Oct. 14 calendar ([`../../../docs/matter-29/matter29-60-day-calendar.md`](../../../docs/matter-29/matter29-60-day-calendar.md); sibling snapshot [`../matter-29/05-prior-analysis/matter29-60-day-calendar.md`](../matter-29/05-prior-analysis/matter29-60-day-calendar.md)) records preservation letters to Amazon and Accurate, plus a CCPA request to Amazon via Morgan Lewis, emailed 2:47–2:48 p.m. PT on Oct. 14. Clock `29-ccpa-amazon` watches the CCPA response.

**The letter PDFs are not ingested.** Do not reconstruct their text. The only Seyfarth letter PDF in `documents/matter-29/` is the Sept. 1 signature-authority letter (`Letter - Seyfarth May Not Affix Plaintiff's Signature (Accurate Stipulation) (Sep 1 2026).pdf`) — that is **not** the preservation letter.

ESI / hold talking points for Nov. 6 (draft, not a sent letter): [`../matter-29/10-rule26f-prep/02-ESI-PRESERVATION-AND-PO.md`](../matter-29/10-rule26f-prep/02-ESI-PRESERVATION-AND-PO.md).

---

## 8. Counsel research and Krishnan

| File | One-line description |
|---|---|
| [`../../../docs/counsel/frederick-stanzick/README.md`](../../../docs/counsel/frederick-stanzick/README.md) | Two-desk playbook index. **Do not email counsel about this research** |
| [`../../../docs/counsel/frederick-stanzick/PLAYBOOK.md`](../../../docs/counsel/frederick-stanzick/PLAYBOOK.md) | Frederick (*Lerma*) / Stanzick (*Carrillo*, *Varela*, *Santee*, *Rangel*) patterns. **Skip any settlement-band or pricing paragraphs** |
| [`../../../docs/counsel/frederick-stanzick/cases.json`](../../../docs/counsel/frederick-stanzick/cases.json) | Machine cards for those dockets |
| [`../../../docs/legal-intel/judges/ajay-s-krishnan-2026.md`](../../../docs/legal-intel/judges/ajay-s-krishnan-2026.md) | Standing-order and discovery-letter notes |
| [`../../../../documents/matter-29/stanzick-searches/`](../../../../documents/matter-29/stanzick-searches/) | S.D. Cal. attorney-search print |

---

## 9. Comparator dockets (not Civil L.R. 3-12 related cases)

Use for willfulness / knowledge / pleading-pattern research. **Do not quote settlement amounts. Do not treat as related-case disclosure.**

### *Lerma v. Amazon.com Services, LLC et al.*, C.D. Cal. 8:22-cv-01727 (Slaughter, J.)

PDFs: [`../../../../documents/matter-29/lerma-v-amazon/`](../../../../documents/matter-29/lerma-v-amazon/).

Read first: Dkt. 20 FAC; Dkt. 23 / 23-1 Accurate MTD; Dkt. 23-2 Accurate report on Lerma (NSOR "NO RECORD FOUND"); Dkt. 24 / 24-1 Amazon MTD; Dkt. 36 order dismissing Megan's Law, FCRA, and UCL; Dkt. 45 Amazon answer on the surviving Fair Chance claim. Dkt. 46/47 are a notice of settlement and dismissal — open only if needed for procedural history; do not extract terms (none are public).

Takeaway already in `matter.json`: the § 290.46 theory was **dismissed**, not settled. Matter 29 must show a different sourcing record than Lerma's court-record-only report.

### *Varela v. Accurate Background*, C.D. Cal. 5:26-cv-00258

PDFs: [`../../../../documents/matter-29/varela-v-accurate/`](../../../../documents/matter-29/varela-v-accurate/) and [`../../../../documents/matter-29/varela-v-accurate-background/`](../../../../documents/matter-29/varela-v-accurate-background/).  
Text: [`../../../public/documents/matter-29/varela-v-accurate/`](../../../public/documents/matter-29/varela-v-accurate/).

Stanzick-signed answer (Dkt. 13) and Joint Rule 26(f) (Dkt. 15) are the useful discovery-posture comps. Skip Dkt. 23 if it attaches a settlement agreement.

### *Santee v. Accurate Background*, C.D. Cal. 8:25-cv-02447

PDFs: [`../../../../documents/matter-29/santee-v-accurate/`](../../../../documents/matter-29/santee-v-accurate/).  
Text: [`../../../public/documents/matter-29/santee-v-accurate/`](../../../public/documents/matter-29/santee-v-accurate/).

Stanzick-signed answer (Dkt. 14). **Do not open the Rule 68 papers for numbers.**

### *Rangel v. Accurate Background*, S.D. Cal. 3:25-cv-01983

PDFs are not on this checkout. Text sidecars: [`../../../public/documents/matter-29/rangel-v-accurate/`](../../../public/documents/matter-29/rangel-v-accurate/).

Complaint + Stanzick answer (twelve defenses — the analysis treats this as the closest Accurate-answer preview). Docket sheet through Sept. 18, 2026. Skip the notice of settlement except to note that the case later resolved.

### Other lodged comps (secondary)

| Folder | Why it is here |
|---|---|
| [`../../../../documents/matter-29/carrillo-v-vons/`](../../../../documents/matter-29/carrillo-v-vons/) | Stanzick on Asurint; § 290.46 / Fair Chance / FCRA class papers |
| [`../../../../documents/matter-29/walker-v-ronin-staffing/`](../../../../documents/matter-29/walker-v-ronin-staffing/) | Stanzick on a different CRA (Sterling) |
| [`../../../public/documents/matter-29/martin-v-assurehire/`](../../../public/documents/matter-29/martin-v-assurehire/) | Counsel-research sidecar only |
| [`../../../public/documents/matter-29/rosenberg-v-first-advantage/`](../../../public/documents/matter-29/rosenberg-v-first-advantage/) | Counsel-research sidecar only |

---

## 10. Existing Matter 29 research and calendars

Broader Oct. 28 room: [`../matter-29/README.md`](../matter-29/README.md). Useful after this folder, not instead of it.

| File | One-line description |
|---|---|
| [`../matter-29/03-discovery-production/DISCOVERY-PLAN.md`](../matter-29/03-discovery-production/DISCOVERY-PLAN.md) | First-wave discovery plan (pre-file-disclosure) |
| [`../matter-29/09-merits-analysis/REINVESTIGATION-ANALYSIS.md`](../matter-29/09-merits-analysis/REINVESTIGATION-ANALYSIS.md) | Oct. 28 letter vs. Oct. 14 report |
| [`../matter-29/09-merits-analysis/CLAIMS-MATRIX.md`](../matter-29/09-merits-analysis/CLAIMS-MATRIX.md) | Claim-by-claim matrix |
| [`../matter-29/09-merits-analysis/DEFENSE-STRATEGY-ASSESSMENT.md`](../matter-29/09-merits-analysis/DEFENSE-STRATEGY-ASSESSMENT.md) | Two-desk defense read |
| [`../matter-29/10-rule26f-prep/00-26F-PREP-SHEET.md`](../matter-29/10-rule26f-prep/00-26F-PREP-SHEET.md) | Nov. 6 conference sheet |
| [`../matter-29/10-rule26f-prep/01-AGENDA-AND-TALKING-POINTS.md`](../matter-29/10-rule26f-prep/01-AGENDA-AND-TALKING-POINTS.md) | Agenda |
| [`../matter-29/10-rule26f-prep/05-26F-TACTICAL-SHEET.md`](../matter-29/10-rule26f-prep/05-26F-TACTICAL-SHEET.md) | What to push / avoid |
| [`../matter-29/11-deadlines/DEADLINE-LIST.md`](../matter-29/11-deadlines/DEADLINE-LIST.md) | Deadline list — verify against live `clocks.json` |
| [`../matter-29/12-open-questions/OPEN-QUESTIONS.md`](../matter-29/12-open-questions/OPEN-QUESTIONS.md) | Open questions as of Oct. 28 (Q2 on RFP service is superseded if the Oct. 31 analysis is adopted) |
| [`../../../docs/matter-29/matter29-accurate-accuracy-audit.md`](../../../docs/matter-29/matter29-accurate-accuracy-audit.md) | Oct. 14 accuracy audit |
| [`../../../docs/matter-29/matter29-60-day-calendar.md`](../../../docs/matter-29/matter29-60-day-calendar.md) | Oct. 14 sixty-day calendar (some dates stale; skip the settlement-demand aside) |
| [`../../../docs/matter-29/matter29-accurate-dispute-email (pre-send draft text).txt`](../../../docs/matter-29/matter29-accurate-dispute-email%20%28pre-send%20draft%20text%29.txt) | Pre-send dispute draft |

---

## 11. Do not open for this analysis

Leave these alone unless Plaintiff separately asks. They are in the repo; they are not part of this discovery room.

- `internal/private/negotiation/29.jsonl`
- `documents/matter-29/Opening Settlement Demand - Amazon.com Services LLC (Aug 31 2026).pdf` and the matching email draft
- Comparator Rule 68 papers and any settlement-agreement exhibits
- CCP § 425.115 punitive-amount notices (state device; dead letter after removal)

---

## Questions for further analysis

Paste one of these into ChatGPT (Work / agent mode) pointed at this branch. Stay inside the record in this folder. Do not invent docket numbers. Do not include settlement figures.

1. **Strengthen RFPs 8, 16, and 19.** Using `00-ANALYSIS.md` and `sources/RFP_Accurate_Set1.txt`, rewrite those three requests so they are broader where the analysis says they are too narrow (matching/normalization policies; the full Amazon–Accurate agreement / end-user certification / adjudication criteria; Accurate–Amazon communications including eligibility, adjudication, and "pending"), without volunteering extra time or waiving objections. Show a redline in prose (old → new) and flag any trade-secret / 26(b)(5) issues.

2. **Draft Accurate RFP Set Two.** After the Nov. 6 conference, what should Set Two cover that Set One missed, now that the Oct. 27 file disclosure and Oct. 28 closing letter exist? Include the reinvestigation file, 2026 SO search #496623723 inputs, furnishing/access logs, disclosure and authorization forms, and anything else the file disclosure proves is missing. Number the requests. Do not restate Set One language unless you are narrowing it.

3. **Interrogatories and RFAs (post–Nov. 6).** Starting from the draft sets in `internal/docs/matter-29/discovery-set-one/04_Accurate_Interrogatories_Set_One.md` and `06_Accurate_RFA_Set_One.md`, revise them against Dkt. 21's twelve defenses and the Oct. 14 / Oct. 27 / Oct. 28 papers. Stay inside Rule 33's 25-interrogatory cap. Pin RFAs to documents in this room (genuineness and discrete facts).

4. **Rule 15 amendment theories.** The as-of-right window closed Oct. 13. Map which facts in the file disclosure and closing letter support adding §§ 1681e(b), 1681i, 1681k, and/or ICRAA § 1786.20(b), and which existing counts they would sit under if leave is denied. Include a proposed count outline and the Krishnan redline requirement. Do not draft a full amended complaint unless asked.

5. **Rule 45 vendor subpoenas.** Draft topic lists (not served papers) for Tauxbe Data Inc. (NSOPW / search 496623723), InformData-SJV (Santa Clara / search 496644204), and Infinity Court Research (San Joaquin). For each: what the file disclosure already shows, what is still missing, the narrowest document requests, and timing relative to Nov. 6 and any protective order.

6. **Nov. 6 Rule 26(f) agenda.** Produce a 30-minute agenda Plaintiff can actually use: protective order (N.D. Cal. model), ESI/native, privilege-log protocol with a post-suit cutoff, written Rule 5(b)(2)(E) email-service consent, amendment deadline, no stay pending the Nov. 18 partial MTD, and confirmation that the Oct. 19 Accurate RFPs are deemed served today. Mark what to say vs. what not to volunteer. Use `../matter-29/10-rule26f-prep/` as a check, not as a script to copy.

7. **Willfulness / punitive discovery.** What written discovery (RFPs, ROGs, 30(b)(6) topics) is needed for § 1681n / ICRAA punitives against Accurate: prior complaints and lawsuits (*Varela*, *Santee*, *Rangel*, *Lerma* as notice — not as settled liability), audits, training, general matching procedures, post-*Lerma* knowledge, and net worth. Distinguish notice from admission. Do not use *Lerma* as proof that Amazon settled a § 290.46 claim. Do not recite any settlement number.

8. **First and Second Defenses vs. the Oct. 14 / Oct. 28 papers.** Line up Dkt. 21 Defense 1 ("has not prepared" a consumer report) and Defense 2 (reported nothing on registry status) against the Oct. 14 report, the Oct. 28 closing letter, and the file disclosure. What is now an admission candidate for RFAs, and what still needs a document?

9. **§ 1681i(a)(7) and leftover § 1681g / § 1786.10 asks.** The closing letter offers a procedure description. Draft the consumer-side request (not a court paper) for that description plus the still-missing 2026 SO search inputs and Amazon intake data. Keep it non-settlement and counsel-copied.

10. **Privilege-log and protective-order protocol.** Using Krishnan's standing-order notes and RFP 13 / 18 / 19, propose a privilege-log date cutoff, what "ordinary-course case notes" means, and how the N.D. Cal. model protective order cures the expected trade-secret objections to RFPs 8, 16, and 20.
