import { withMatterIdentity } from "./matterIdentity.js";

// Ground-truth lawyer-fee estimate for the portfolio.
// Real page counts extracted with pdfinfo from every PDF in public/documents/matter-XX/
// (poppler-utils), then classified by document type and priced per the methodology in
// docs/LAWYER_FEES_CALCULATOR.md.
// Matter identity (caption / case_no / court / status) lives on matter JSON — join via
// matterIdentity.js at read time. This module stores number + fee analytics only.
// `type` here is a fee-tab claim shorthand and may differ from matter.type by design.
const lawyer_fees_raw = [
  {
    number: 1,
    type: "Federal - 42 U.S.C. 1983 (4th/14th Amend., Monell)",
    documentsCount: 25,
    totalPagesReal: 116,
    hours: {
      low: 49.4,
      high: 88.2,
      mid: 68.8
    },
    cost: {
      low: 13832,
      high: 24696,
      mid: 19264
    },
    notes: "Real page counts are far smaller than a naive filename-based guess would suggest (116 total pages, not 1,000+); the MTD briefing cycle is genuinely modest in length. Opposing-party filings (CHP's MTD, AG's Reply) are billed only at a light review rate, not drafting rate. True-up increment: Notice of Change of Address and a Notice of Supplemental Authority (Serrato Order) were present on disk but not previously counted; billed at flat administrative rates."
  },
  {
    number: 2,
    type: "State - False Imprisonment, Battery, Bane Act",
    documentsCount: 16,
    totalPagesReal: 111,
    hours: {
      low: 68.4,
      high: 116.6,
      mid: 92.5
    },
    cost: {
      low: 19152,
      high: 32648,
      mid: 25900
    },
    notes: "Parallel state action tied to Matter 1; heaviest real cost driver is the 15-page complaint plus the Ex Parte Application and U-Visa reply briefing, not the shared discovery/evidence set."
  },
  {
    number: 3,
    type: "Federal",
    documentsCount: 26,
    totalPagesReal: 290,
    hours: {
      low: 190.8,
      high: 351.6,
      mid: 271.2
    },
    cost: {
      low: 53424,
      high: 98448,
      mid: 75936
    },
    notes: "Ground-truth PDFs (290 total pages across 26 files) show a much smaller record than the 664-pg complaint/685-pg MTQ referenced in the prior LAWYER_FEES_CALCULATOR.md draft — no such files exist in public/documents/matter-03; that figure appears to be a stale/incorrect prior estimate and was disregarded in favor of actual pdfinfo counts. Two documents listed in matters.js (PalaciosMTD_Doc24.pdf, Opposition_PalaciosMTD.pdf) are referenced but not present in the uploaded folder and were excluded from the page/hour tally; their substance is effectively captured by 'SLB MTD.pdf' and 'SLB Opposition to MTD.pdf', which are counted."
  },
  {
    number: 4,
    type: "State",
    documentsCount: 0,
    totalPagesReal: 0,
    hours: {
      low: 41.5,
      high: 94,
      mid: 67.75
    },
    cost: {
      low: 11620,
      high: 26320,
      mid: 18970
    },
    notes: "No documents folder exists for this matter (empty array in ground-truth extraction) — a complaint was filed (05/29/2026) and the case is confirmed real (Gov. Claim filed Feb. 2026, deemed rejected ~Apr. 2026) but voluntarily dismissed before any filing was uploaded to the portfolio site. Estimated conservatively as a moderate-length state complaint plus a Government Claim, given the matter never proceeded to motion practice or discovery."
  },
  {
    number: 5,
    type: "State",
    documentsCount: 38,
    totalPagesReal: 833,
    hours: {
      low: 422.1,
      high: 687.8,
      mid: 554.95
    },
    cost: {
      low: 118188,
      high: 192584,
      mid: 155386
    },
    notes: "Largest matter in this batch by real page count (833 pages across 38 files) — driven mainly by heavy bilateral discovery (377 pp) and two large Requests for Judicial Notice (222 pp combined). The prior 712-page 'CASOMB Complaint' estimate in LAWYER_FEES_CALCULATOR.md does not match the actual file (38 real pages); real pdfinfo counts were used throughout. Matters.js notes that 12 underlying discovery-production PDFs (defendants' document production) were removed from the public repository after review and are correctly absent from both the ground-truth JSON and this cost estimate. True-up increment: the Order Sustaining Demurrer to FAC (court order, light review only), a duplicate Tentative Ruling text file, and other previously uncounted administrative pages were added at light review/admin rates, not drafting rate."
  },
  {
    number: 6,
    type: "Federal",
    documentsCount: 4,
    totalPagesReal: 101,
    hours: {
      low: 193,
      high: 292,
      mid: 242.5
    },
    cost: {
      low: 54040,
      high: 81760,
      mid: 67900
    },
    notes: "Voluntarily dismissed one day after the sole defense appearance (Notice of Related Cases), before any answer or MSJ — so nearly all billable work is the two complaints themselves (96 pages total), not motion practice. A Minute Order PDF referenced in matters.js is not present in the uploaded folder and was excluded from the tally (immaterial — court orders are not billable attorney drafting time in any event)."
  },
  {
    number: 7,
    type: "Federal - 42 U.S.C. 1983 Procedural Due Process (structural bias, DMV APS)",
    documentsCount: 17,
    totalPagesReal: 185,
    hours: {
      low: 185.1,
      high: 289.4,
      mid: 237.25
    },
    cost: {
      low: 51828,
      high: 81032,
      mid: 66430
    },
    notes: "Highest-cost matter in the cluster because it contains two real complaint drafts (60p original + 31p FAC) totaling 91 pages of genuine pleading work; this is a defensible, non-inflated result since the original complaint is billed once at full rate and the FAC only at a reduced amendment rate. True-up increment: a Notice of Supplemental Authority (Serrato Order) present on disk but not previously counted, billed at a flat administrative rate."
  },
  {
    number: 8,
    type: "State - Writ of Administrative Mandate (CCP 1094.5)",
    documentsCount: 2,
    totalPagesReal: 88,
    hours: {
      low: 50.5,
      high: 81,
      mid: 65.75
    },
    cost: {
      low: 14140,
      high: 22680,
      mid: 18410
    },
    notes: "Single-document matter (writ petition); cost driven entirely by the flat specialized-writ rate, consistent with the 5-count 1094.5 causes of action asserted."
  },
  {
    number: 9,
    type: "Writ of Mandate (CCP §1085)",
    documentsCount: 9,
    totalPagesReal: 179,
    hours: {
      low: 65,
      high: 116,
      mid: 90.5
    },
    cost: {
      low: 18200,
      high: 32480,
      mid: 25340
    },
    notes: "Challenges CDCR's discharge-review denial (Form 1502-DR errors, wrong legal standard). AG's demurrer prompted a petitioner opposition (not present as a separate uploaded file) and an AG reply (present but not billable — opposing counsel's work). Estimate is conservative: it excludes the AG's own filing and treats voluminous notice/administrative bundles as flat per-document tasks rather than per-page briefing."
  },
  {
    number: 10,
    type: "Habeas Corpus (PC §3008(d)(2); 15 CCR §3574) — Treatment Termination",
    documentsCount: 2,
    totalPagesReal: 3,
    hours: {
      low: 40.5,
      high: 72,
      mid: 56.25
    },
    cost: {
      low: 11340,
      high: 20160,
      mid: 15750
    },
    notes: "Only 2 files sit in this matter's public folder (a notice and the court's denial order); the underlying petition PDF was never uploaded to the portfolio site. Because the case record independently establishes the petition was drafted, filed, and adjudicated on exhaustion grounds (PC §3008(d)(2) certification requirement), the estimate credits the standard habeas-drafting range rather than reporting a near-zero cost that would understate real work performed."
  },
  {
    number: 11,
    type: "Federal",
    documentsCount: 0,
    totalPagesReal: 0,
    hours: {
      low: 30.5,
      high: 76,
      mid: 53.25
    },
    cost: {
      low: 8540,
      high: 21280,
      mid: 14910
    },
    notes: "Filed 03/02/2026 and voluntarily dismissed with prejudice 06/29/2026 before any defendant answered or moved — case never reached motion practice or discovery. Estimated conservatively as a single-issue equitable-relief-only complaint (declaratory/injunctive, no damages claim) plus a short dismissal notice; no uploaded documents exist to verify actual length."
  },
  {
    number: 12,
    type: "State — Consumer Fraud / UCL",
    documentsCount: 20,
    totalPagesReal: 188,
    hours: {
      low: 151,
      high: 247,
      mid: 199
    },
    cost: {
      low: 42280,
      high: 69160,
      mid: 55720
    },
    notes: "Active case with a real 34-page amended complaint and a substantial 58-page default judgment packet already on file, so the fee estimate here is meaningfully higher than a generic 'early-stage/light filing' guess — the underlying documents show genuine substantive drafting work, not just a bare-bones complaint. Increment: 6-page CM-110 Case Management Statement (filed Jul. 20, 2026), billed as a flat administrative filing plus a short sworn declaration (Attachment 4b itemizing the $78,671.20 default judgment prove-up), not per-page drafting rate; a 2-page formal POS-010 Proof of Service for Alpine Truck Sales (Levying Officer File No. 2026002577) — a duplicate confirmation of the already-tracked July 1, 2026 service, billed at a nominal administrative rate; and a 49-page Alpine Default Judgment Packet, now a complete self-contained filing record: 3-page CIV-100 Request for Entry of Default/Court Judgment (flat administrative-filing rate), a 7-page supporting Declaration developing the derivative successor-liability/alter-ego theory (motion-brief-adjacent rate given the legal research and case citations required), and 39 pages of exhibits and exhibit covers (Exhibits 1–10) reattached from the Diamond prove-up package — billed at a nominal clerical/compilation rate since this is a duplicate of exhibits already fully priced once under the original Diamond packet, not fresh evidentiary drafting."
  },
  {
    number: 13,
    type: "Federal",
    documentsCount: 0,
    totalPagesReal: 0,
    hours: {
      low: 30.5,
      high: 76,
      mid: 53.25
    },
    cost: {
      low: 8540,
      high: 21280,
      mid: 14910
    },
    notes: "Filed 01/22/2026 and voluntarily dismissed with prejudice 06/29/2026 before any defendant answered or moved — same early-dismissal pattern as Matter 11. Estimated conservatively as a single-issue federal complaint plus a short dismissal notice; no uploaded documents exist to verify actual length."
  },
  {
    number: 14,
    type: "State",
    documentsCount: 1,
    totalPagesReal: 28,
    hours: {
      low: 70,
      high: 95,
      mid: 82.5
    },
    cost: {
      low: 19600,
      high: 26600,
      mid: 23100
    },
    notes: "Single 28-page combined writ/complaint filed June 30, 2026 and voluntarily dismissed shortly after; no motion practice occurred, so the estimate reflects drafting/research/filing only."
  },
  {
    number: 15,
    type: "State",
    documentsCount: 19,
    totalPagesReal: 448,
    hours: {
      low: 300.5,
      high: 419.5,
      mid: 360
    },
    cost: {
      low: 84140,
      high: 117460,
      mid: 100800
    },
    notes: "Largest matter in this batch (448 real pages, 19 files). Multiple complaint versions reflect genuine post-demurrer recalibration (companion Macomber mandate case, Matter 19/9, received an adverse tentative ruling that forced a damages-only rewrite) rather than pure duplication. The two ~110-page files were billed at evidence-compilation, not complaint, rates specifically to keep the estimate defensible rather than inflated. True-up increment: a meet-and-confer calendar invite and a minor administrative filing present on disk but not previously counted, billed at flat administrative rates."
  },
  {
    number: 16,
    type: "State",
    documentsCount: 1,
    totalPagesReal: 32,
    hours: {
      low: 64,
      high: 80,
      mid: 72
    },
    cost: {
      low: 17920,
      high: 22400,
      mid: 20160
    },
    notes: "Single 32-page complaint filed July 7, 2026, voluntarily dismissed; no further filings appear in the record."
  },
  {
    number: 17,
    type: "Federal",
    documentsCount: 0,
    totalPagesReal: 0,
    hours: {
      low: 56,
      high: 80,
      mid: 68
    },
    cost: {
      low: 15680,
      high: 22400,
      mid: 19040
    },
    notes: "No documents folder exists for this matter (empty in source data). Conservative estimate limited to complaint + minimal ancillary filings, since the case was voluntarily dismissed with prejudice before any defendant answered or filed a motion."
  },
  {
    number: 18,
    type: "Federal",
    documentsCount: 0,
    totalPagesReal: 0,
    hours: {
      low: 55,
      high: 75,
      mid: 65
    },
    cost: {
      low: 15400,
      high: 21000,
      mid: 18200
    },
    notes: "No documents folder exists for this matter. Estimate reflects a prisoner civil-rights complaint plus minor PLRA-related procedural filings before an early, self-executing voluntary dismissal with prejudice."
  },
  {
    number: 19,
    type: "Habeas Corpus — Immediate Discharge from Parole (Pen. Code §1473; PC §§3000, 3001, 3008(d)(2); 15 CCR §3574)",
    documentsCount: 4,
    totalPagesReal: 72,
    hours: {
      low: 43,
      high: 77,
      mid: 60
    },
    cost: {
      low: 12040,
      high: 21560,
      mid: 16800
    },
    notes: "Companion matter to Matters 9, 10, and 11 (same administrative record); targets the parole term itself rather than treatment compulsion. The 67-page petition is unusually dense for a habeas filing (5 causes of action, 6 exhibits, extensive regulatory/case-law analysis re: In re Gadlin, In re Leman, ACSOL v. Macomber), justifying the top of the 40-70 hr specialized-habeas range. True-up: Notice of Change of Address (admin) plus HC-004 Notice and Request for Ruling packet prepared Aug. 7, 2026 — only the HC-004 cover pages are new billable work (petition pages inside the packet are the same 67 pp. already counted; billed at flat administrative/form-fill rate, not habeas redraft)."
  },
  {
    number: 20,
    type: "State - Writ of Mandate (CCP 1085, PC 679.10 U-Visa Certification)",
    documentsCount: 18,
    totalPagesReal: 390,
    hours: {
      low: 80.8,
      high: 137.9,
      mid: 109.35
    },
    cost: {
      low: 22624,
      high: 38612,
      mid: 30618
    },
    notes: "390 pages is the largest raw page count in the cluster, but 306 of those pages are two near-duplicate copies of the same 153-page writ petition, so the writ is billed once at the flat specialized rate rather than per-page, keeping the estimate defensible."
  },
  {
    number: 21,
    type: "Federal",
    documentsCount: 2,
    totalPagesReal: 21,
    hours: {
      low: 28.5,
      high: 42.5,
      mid: 35.5
    },
    cost: {
      low: 7980,
      high: 11900,
      mid: 9940
    },
    notes: "Only the complaint itself is billable drafting work; the folder also contains a 12-page CSK order (Barocio-related) present on disk but not previously counted — billed at a light review-only rate since court orders are not billable attorney drafting time. Case was voluntarily dismissed with prejudice before any defendant answered or moved, so no motion practice is billed."
  },
  {
    number: 22,
    type: "State — PC §290.46(j) / FCRA / ICRAA / UCL / Wrongful Termination",
    documentsCount: 8,
    totalPagesReal: 45,
    hours: {
      low: 63,
      high: 103.5,
      mid: 83.25
    },
    cost: {
      low: 17640,
      high: 28980,
      mid: 23310
    },
    notes: "Light litigation footprint by design: a complaint was drafted and filed, but the matter settled via demand letter and negotiation before service was even completed, so no answer, motion practice, or discovery ever occurred — billed accordingly at pre-litigation/negotiation intensity rather than full federal-style motion practice. True-up increment: the process server's Invoice and Signed Proof of Service (POS-010), relocated into this folder during an earlier cleanup, was present on disk but not previously counted — billed at evidence/exhibit rate."
  },
  {
    number: 23,
    type: "State — PC §290.46(j) / FCRA / ICRAA / UCL / Wrongful Termination (contemplated)",
    documentsCount: 2,
    totalPagesReal: 11,
    hours: {
      low: 4,
      high: 8,
      mid: 6
    },
    cost: {
      low: 1120,
      high: 2240,
      mid: 1680
    },
    notes: "Essentially pre-litigation only: no complaint, summons, or any court filing exists in this matter's file set — the two documents present are evidentiary background records reviewed during initial case assessment before the decision was made not to pursue."
  },
  {
    number: 24,
    type: "Federal - 42 U.S.C. 1983 (Due Process, 1st Amend. Retaliation - U-Visa certification denial)",
    documentsCount: 6,
    totalPagesReal: 58,
    hours: {
      low: 46.5,
      high: 72,
      mid: 59.25
    },
    cost: {
      low: 13020,
      high: 20160,
      mid: 16590
    },
    notes: "Newest and lightest matter in the cluster; only a single 21-page complaint plus routine N.D. Cal. intake paperwork (IFP application, proposed summons, ISC/magistrate consent form) have been filed so far."
  },
  {
    number: 25,
    type: "State — PC §290.46(j) / ICRAA / Wrongful Failure to Hire",
    documentsCount: 17,
    totalPagesReal: 53,
    hours: {
      low: 47,
      high: 79,
      mid: 63
    },
    cost: {
      low: 13160,
      high: 22120,
      mid: 17640
    },
    notes: "Filed July 15, 2026. The 18-page, six-count complaint is the only substantive drafting product; most remaining pages are single-page First Advantage notice/reminder emails reviewed for the factual record. Increment since the prior estimate: file-stamped complaint confirmation pages, the FW-003 fee waiver order (GRANTED), a duplicate Notice of Case Assignment/Hearing, and the SUM-100 Summons — all billed at light administrative/evidence-review rates, not drafting rate. No answer, motion practice, or discovery exists yet; service not yet completed."
  },
  {
    number: 26,
    type: "State — PC §290.46(j) / ICRAA / Wrongful Failure to Hire",
    documentsCount: 13,
    totalPagesReal: 48,
    hours: {
      low: 43,
      high: 74,
      mid: 58.5
    },
    cost: {
      low: 12040,
      high: 20720,
      mid: 16380
    },
    notes: "Filed July 15, 2026 — 16 days before the July 31, 2026 two-year limitations cutoff, preserving all time-sensitive claims. The 18-page, six-count complaint is the only substantive drafting product; most remaining pages are single-page First Advantage notice/reminder emails. Increment since the prior estimate: file-stamped complaint confirmation pages, the FW-003 fee waiver order (GRANTED), a duplicate Notice of Case Assignment/Hearing, the SUM-100 Summons, and a 5-page SER-001 Request for Sheriff to Serve Court Papers (Sacramento County, registered-agent service, requested deadline July 31, 2026) — billed as a light administrative/procedural task, not full motion-drafting rate. No answer, motion practice, or discovery exists yet."
  },
  {
    number: 27,
    type: "State — PC §290.46(j) / Wrongful Termination / ICRAA / Negligence Per Se / UCL",
    documentsCount: 25,
    totalPagesReal: 110,
    hours: {
      low: 69.7,
      high: 118.2,
      mid: 93.95
    },
    cost: {
      low: 19516,
      high: 33096,
      mid: 26306
    },
    notes: "Substantial increment now that the complaint has actually been e-filed and RK Logistics has responded, plus service now confirmed. Thirteen new documents since the pre-filing estimate (25 total, 110 real pages, +52 pages): the e-filing confirmation packet (Civil Case Cover Sheet, Fee Waiver, Order on Fee Waiver, Notice of Confirmation of E-Filing, Notice of Case Assignment, Notice of CMC, and two SUM-100 versions plus the blank template) billed as light administrative/procedural tasks (0.5–2 hr/doc, per methodology); a duplicate filed copy of the 19-page Complaint billed only incrementally per the near-duplicate rule; the 12-page Garcia & Gurney response letter, billed above the standard opposing-counsel light-review rate to account for the substantive rebuttal analysis it required (comparing the SambaSafety Class A/Class C license distinction and the Jack Altares email against the letter's employer-status argument), plus its 1-page Gmail transmittal; and the 2-page Sacramento County Sheriff Civil File Status confirming Jul. 30, 2026 dual service, billed as a light administrative/status document. Prior 12-document, 58-page base (19-page Verified Complaint, two 4-page demand letters, 15-page InfoMart report, CA SOS records, Gmail demand transmittals, onboarding emails, and the 5-page SER-001) carries forward unchanged. Randstad's August 2 demand response remains outstanding; responsive pleadings are now due August 31, 2026, and any demurrer/meet-and-confer practice will add a further increment."
  },
  {
    number: 28,
    type: "Federal — 42 U.S.C. §1983 (Monell + Individual Capacity); Bane Act §52.1; Fraud/Negligent Misrepresentation; RICO 18 U.S.C. §1962(c)-(d)",
    documentsCount: 7,
    totalPagesReal: 77,
    hours: {
      low: 102,
      high: 176,
      mid: 139
    },
    cost: {
      low: 28560,
      high: 49280,
      mid: 38920
    },
    notes: "Seven documents totaling 77 real pages (corrected from a 53-page estimate — several documents ran longer than originally guessed): 24-page federal complaint (the dominant cost driver — novel theory development across RICO, §1983 Monell, individual-capacity §1983, Bane Act, and fraud/negligent misrepresentation in a single pleading; hours are elevated accordingly); 10-page Motion for Protective Order; 6-page supporting Declaration (billed per-document, not per-page, per methodology); state court Stipulated Protective Order as Exhibit A (12 pages); 12-page Proposed NDCA Protective Order; 11-page signed state Stipulated PO; 2-page PACER docket sheet confirming case filing and docket activity, billed at a nominal administrative-monitoring rate. Hours reflect drafting a complex multi-theory federal complaint from scratch leveraging 542 pages of discovery already produced in the dismissed state case, plus preparation of the contemporaneous protective-order motion package — now correctly priced against the actual, longer motion and proposed-order page counts. Fee-shifting under §1988 and RICO makes attorney fee recovery highly probable if Plaintiff prevails."
  },
  {
    number: 29,
    type: "State — PC §290.46(j) / FCRA / ICRAA / Failure to Hire",
    documentsCount: 17,
    totalPagesReal: 56,
    hours: {
      low: 76.5,
      high: 128,
      mid: 102.25
    },
    cost: {
      low: 21420,
      high: 35840,
      mid: 28630
    },
    notes: "Substantial increment now that the complaint has actually been e-filed. Five new documents since the pre-filing estimate (16 total, 54 real pages, +35 pages): the 27-page Verified Complaint (7 causes of action) is the dominant new cost driver, billed at the standard 2–3 hr/page major-pleading rate ($54–81 hrs alone); the 3-page CM-010 Civil Case Cover Sheet, 1-page SUM-100 Summons, 2-page FW-001 Request to Waive Court Fees, and 2-page One Legal Order Receipt (eFiling Confirmation #35236062, Filing Order #28857032) are billed as light administrative/procedural tasks (0.5–2 hr/doc), consistent with how the equivalent e-filing packet was priced in Matter 27. Prior 11-document, 19-page pre-filing base (Amazon Simple Hire Checklists, BGC-status emails, Equifax reminder, and application/appointment screenshots) carries forward unchanged. Court acceptance, case number assignment, and service (two defendants — Amazon.com Services, LLC via CSC – Lawyers Incorporating Service in Sacramento County, and Accurate Background LLC via CT Corporation System in Los Angeles County, per the Lerma docket) will each add a further increment; two draft SER-001 Sheriff service request forms have been prepared but not yet executed or filed, so they are not yet counted here. Fee-shifting under PC §290.46(j)(4)(A), FCRA, and ICRAA applies upon prevailing."
  },
  {
    number: 30,
    type: "Federal — 42 U.S.C. §1983 (First Amendment Retaliation + Due Process); Bane Act Cal. Civ. Code §52.1; IIED",
    documentsCount: 12,
    totalPagesReal: 107,
    hours: {
      low: 56,
      high: 132,
      mid: 86.5
    },
    cost: {
      low: 15680,
      high: 36960,
      mid: 24220
    },
    notes: "Complaint filed Sep. 16, 2026. Twelve documents totaling 107 real pages (corrected from a 64-page estimate): 26-page verified complaint (Newanforbi v. Moua, et al.); 25-page Derrick FAC (Case 2:26-cv-00004-DJC-JDP, E.D. Cal. — scanned PDF, confirms triggering protected activity and Noguchi as named co-defendant); 3 CASOMB submission PDFs (~5 pages — Dr. Kirsten Mason inquiry, BNN responses, telehealth accommodation request); 4 screenshots (4 pages — Agent Moua contact card, Agent Brown text exchanges, CountySuite service records); Macy's job offer (~3 pages); Macy's work schedule (~2 pages); and a 42-page 'Newanforbi v. CDCR, et al 3.pdf' — on inspection this is a duplicate copy of the SUM-100 Summons and Complaint for Damages already fully billed under Matter 15 (case STK-CV-UPI-2026-5417), sitting in this folder as cross-reference evidence for the Noguchi/Rojo service history — billed at a nominal flat rate (not per-page) since it is fully duplicative of already-priced Matter 15 work, not new drafting. Hours are substantially elevated because: (1) the complaint requires three independent §1983 retaliation theories each with distinct factual predicates; (2) Bane Act §52.1 adds a state-law coercion theory requiring Shoyoye pleading of independence; (3) Heck v. Humphrey and absolute immunity must be preemptively addressed; (4) Government Claims Act exhaustion (GCA claim Jul. 18, deemed rejected Sep. 1) must be pleaded; (5) supervisory liability for Noguchi (named Derrick FAC co-defendant + 1502-DR co-author) and Rojo. Fee-shifting under 42 U.S.C. §1988 and mandatory Bane Act attorney fees make attorney fee recovery highly probable on prevailing."
  },
  {
    number: 31,
    type: "State — FCRA §1681b(b)/§1681e(b), ICRAA, Negligence Per Se, UCL §17200",
    documentsCount: 0,
    totalPagesReal: 0,
    hours: {
      low: 35,
      high: 78,
      mid: 56.5
    },
    cost: {
      low: 9800,
      high: 21840,
      mid: 15820
    },
    notes: "No new PDFs — the evidentiary basis (First Advantage's pre-adverse/adverse notices for both the UPS and FedEx sequences) is already measured and billed under Matters 26 and 25 respectively; counting those pages again here would double-count real work already priced elsewhere. Estimated instead from matters.js status text as a single-defendant vendor-liability complaint of moderate complexity: five causes of action (two FCRA provisions, ICRAA, negligence per se, UCL) drafted from an existing fact pattern rather than fresh investigation, roughly comparable in scope to Matter 8's single-document writ estimate. No motion practice, discovery, or service costs included since nothing has been filed."
  },
  {
    number: 32,
    type: "Federal — § 1983 (N.D. Cal.) + Nov. 1, 2024 CHP cluster document store",
    documentsCount: 78,
    totalPagesReal: 808,
    hours: {
      low: 48,
      high: 72,
      mid: 60
    },
    cost: {
      low: 13440,
      high: 20160,
      mid: 16800
    },
    notes: "NEW billable work is the Aug. 7, 2026 N.D. Cal. filing set under ndcal/ (77 pages): operative Complaint v3 (20 pp) at major-pleading 2.0–2.5 hr/page, plus revision credit for superseded drafts v1/v2 (not full rebill of 49 draft pages), plus intake packet / wage-exhibit admin (2–4 hrs). Relocated from-01|02|20|24/ PDFs (731 pp) remain attributed to source Matters 1, 2, 20, and 24 at $0 here to avoid double-counting. Nov. 1 / Candelaria APS evidence lives in Matter 33."
  },
  {
    number: 33,
    type: "Federal — § 1983 APS / N.D. Cal. refile + document store",
    documentsCount: 30,
    totalPagesReal: 428,
    hours: {
      low: 50,
      high: 94,
      mid: 72
    },
    cost: {
      low: 14000,
      high: 26320,
      mid: 20160
    },
    notes: "Combines (a) previously transferred Nov. 1 / APS incident evidence-compilation line (18–40 hrs mid 29) with (b) NEW Aug. 7, 2026 N.D. Cal. refile set under ndcal/ (116 pages): operative Complaint v3 (47 pp) billed below full 2–3 hr/page because it substantially reuses Matter 7 theory/work product (adaptation/venue rewrite ~30–50 hrs mid 40) plus intake admin (2–4 hrs). Drafting hours for from-07 / from-08 historical PDFs remain on Matters 7 and 8 — not re-billed here."
  },
  {
    number: 34,
    type: "Federal — 42 U.S.C. §1983 (Monell + Individual); Bane Act Cal. Civ. Code §52.1; Fraud; UCL §17200",
    documentsCount: 0,
    totalPagesReal: 0,
    hours: {
      low: 15,
      high: 40,
      mid: 27.5
    },
    cost: {
      low: 4200,
      high: 11200,
      mid: 7700
    },
    notes: "Pre-filing intake and compliance-audit stage. No documents on disk yet (0 real pages). Estimated work encompasses initial client intake review, CASOMB provider verification and regulatory analysis under 15 CCR §3574, treatment contract analysis, and adaptation of the Matter 28 / Matter 5 pleading framework for Santa Clara County / CPC corporate defendants. Fee-shifting under 42 U.S.C. §1988 and Cal. Civ. Code §52.1(i) applies upon prevailing."
  },
  {
    number: 35,
    type: "State — Unruh / False Imprisonment / Negligent Training (Santa Clara Sup. Ct.)",
    documentsCount: 6,
    totalPagesReal: 37,
    hours: {
      low: 46,
      high: 78,
      mid: 62
    },
    cost: {
      low: 12880,
      high: 21840,
      mid: 17360
    },
    notes: "Aug. 26, 2026 verified complaint v9 (28 pp. pleading paper) billed as a major state pleading: fact investigation and corporate-entity research, Unruh / §490.5(f) / false-imprisonment theory development, and full drafting/revision of the tightened three-cause complaint with universal signature. Filing packet on disk and e-filed same day: CM-010 (3), SUM-100 (1), CV-5012 (1), plus Internal Damages Worksheet (2 — DO NOT FILE) and One Legal Order Receipt (2 — Confirmation #35442871; under clerk review). Packet forms billed at form-completion/admin rates; receipt at nominal monitoring. Fee-shifting under Civ. Code §52(a) and CCP §1021.5 applies upon prevailing."
  }
];

export const lawyer_fees = lawyer_fees_raw.map((row) => withMatterIdentity(row));

export const lawyer_fees_summary = {
  analysisDate: "2026-08-26",
  totalMatters: 35,
  totalDocumentsAnalyzed: 331,
  totalPagesReal: 3942,
  methodology: {
    blendedHourlyRate: 280,
    rateRange: { seniorPartner: [350, 450], midAssociate: [250, 350], paralegal: [150, 200] },
    note: "Every PDF in public/documents/matter-XX/ was measured with pdfinfo for real page counts (poppler-utils), then classified by document type (complaint, motion/opposition/reply, discovery, writ/habeas, declaration, administrative, evidence) and priced using the hours-per-page/per-document conversions in docs/LAWYER_FEES_CALCULATOR.md. Opposing counsel's filings are billed only at a light review rate, never at drafting rate. Matters with no uploaded PDFs are estimated conservatively from matters.js status text. Aug. 26, 2026 true-up: Matter 35 Unruh verified complaint v9 + filing packet e-filed (37 real pages across 6 files) as Cluster 6.",
  },
  totalEstimatedHours: { low: 2917.8, high: 4847.2, mid: 3875.0 },
  totalEstimatedCost: { low: 816984, high: 1357216, mid: 1085000 },
  byCluster: {
    cluster1: { label: "CHP / DUI / DMV", matters: [1, 2, 7, 8, 20, 24, 32, 33], costLow: 162036, costMid: 214172, costHigh: 266308 },
    cluster2: { label: "Parole Retaliation / HOPE", matters: [3, 4, 5, 6, 11, 13, 14, 15, 16, 17, 18, 21, 28, 30, 34], costLow: 463512, costMid: 610092, costHigh: 760872 },
    cluster3: { label: "Consumer Fraud / Employment", matters: [12, 22, 23, 25, 26, 27, 29, 31], costLow: 136976, costMid: 185500, costHigh: 233940 },
    cluster4: { label: "Administrative Writs & Habeas", matters: [9, 10, 19], costLow: 41580, costMid: 57890, costHigh: 74200 },
    cluster6: { label: "Public Accommodation / Unruh", matters: [35], costLow: 12880, costMid: 17360, costHigh: 21840 },
  },
};
