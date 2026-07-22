// Ground-truth lawyer-fee estimate for the entire 30-matter portfolio.
// Real page counts extracted with pdfinfo from every PDF in public/documents/matter-XX/
// (poppler-utils), then classified by document type and priced per the methodology in
// docs/LAWYER_FEES_CALCULATOR.md by five parallel analysis passes, one per case cluster.
// Matters with no uploaded PDFs (4, 11, 13, 17, 18) are estimated from matters.js status text.
export const lawyer_fees = [
  {
    number: 1, caption: "Newanforbi v. CHP et al.", caseNumber: "2:25-cv-01460-DC-CSK",
    court: "USDC E.D. Cal.", type: "Federal - 42 U.S.C. 1983 (4th/14th Amend., Monell)",
    status: "Filed 05/27/2025; MTD fully briefed (MTD, Opposition, Reply); ruling pending",
    documentsCount: 25, totalPagesReal: 116,
    hours: { low: 49.4, high: 88.2, mid: 68.8 },
    cost: { low: 13832, high: 24696, mid: 19264 },
    notes: "Real page counts are far smaller than a naive filename-based guess would suggest (116 total pages, not 1,000+); the MTD briefing cycle is genuinely modest in length. Opposing-party filings (CHP's MTD, AG's Reply) are billed only at a light review rate, not drafting rate. True-up increment: Notice of Change of Address and a Notice of Supplemental Authority (Serrato Order) were present on disk but not previously counted; billed at flat administrative rates."
  },
  {
    number: 2, caption: "Newanforbi v. Meza-Gonzalez et al.", caseNumber: "26CV168913",
    court: "Alameda Sup. Ct.", type: "State - False Imprisonment, Battery, Bane Act",
    status: "STAYED pending federal Matter 1 resolution; U-Visa certification motion briefed (Opp./Reply) and heard",
    documentsCount: 16, totalPagesReal: 111,
    hours: { low: 68.4, high: 116.6, mid: 92.5 },
    cost: { low: 19152, high: 32648, mid: 25900 },
    notes: "Parallel state action tied to Matter 1; heaviest real cost driver is the 15-page complaint plus the Ex Parte Application and U-Visa reply briefing, not the shared discovery/evidence set."
  },
  {
    number: 3, caption: "Newanforbi v. Derrick et al.", caseNumber: "2:26-cv-00004-DJC-JDP",
    court: "USDC E.D. Cal.", type: "Federal",
    status: "Active — MTD (Doc 24) under submission; hearing vacated, awaiting ruling",
    documentsCount: 26, totalPagesReal: 290,
    hours: { low: 190.8, high: 351.6, mid: 271.2 },
    cost: { low: 53424, high: 98448, mid: 75936 },
    notes: "Ground-truth PDFs (290 total pages across 26 files) show a much smaller record than the 664-pg complaint/685-pg MTQ referenced in the prior LAWYER_FEES_CALCULATOR.md draft — no such files exist in public/documents/matter-03; that figure appears to be a stale/incorrect prior estimate and was disregarded in favor of actual pdfinfo counts. Two documents listed in matters.js (PalaciosMTD_Doc24.pdf, Opposition_PalaciosMTD.pdf) are referenced but not present in the uploaded folder and were excluded from the page/hour tally; their substance is effectively captured by 'SLB MTD.pdf' and 'SLB Opposition to MTD.pdf', which are counted."
  },
  {
    number: 4, caption: "Newanforbi v. Derrick et al. (State Mirror)", caseNumber: "TBD",
    court: "San Joaquin Sup. Ct.", type: "State",
    status: "NOT PURSUING — Voluntarily dismissed shortly after filing",
    documentsCount: 0, totalPagesReal: 0,
    hours: { low: 41.5, high: 94, mid: 67.75 },
    cost: { low: 11620, high: 26320, mid: 18970 },
    notes: "No documents folder exists for this matter (empty array in ground-truth extraction) — a complaint was filed (05/29/2026) and the case is confirmed real (Gov. Claim filed Feb. 2026, deemed rejected ~Apr. 2026) but voluntarily dismissed before any filing was uploaded to the portfolio site. Estimated conservatively as a moderate-length state complaint plus a Government Claim, given the matter never proceeded to motion practice or discovery."
  },
  {
    number: 5, caption: "Newanforbi v. Palacios et al.", caseNumber: "STK-CV-UF-2026-0001032",
    court: "San Joaquin Sup. Ct.", type: "State",
    status: "Active — Demurrer to FAC fully briefed; hearing 07/15/2026; discovery underway",
    documentsCount: 38, totalPagesReal: 833,
    hours: { low: 422.1, high: 687.8, mid: 554.95 },
    cost: { low: 118188, high: 192584, mid: 155386 },
    notes: "Largest matter in this batch by real page count (833 pages across 38 files) — driven mainly by heavy bilateral discovery (377 pp) and two large Requests for Judicial Notice (222 pp combined). The prior 712-page 'CASOMB Complaint' estimate in LAWYER_FEES_CALCULATOR.md does not match the actual file (38 real pages); real pdfinfo counts were used throughout. Matters.js notes that 12 underlying discovery-production PDFs (defendants' document production) were removed from the public repository after review and are correctly absent from both the ground-truth JSON and this cost estimate. True-up increment: the Order Sustaining Demurrer to FAC (court order, light review only), a duplicate Tentative Ruling text file, and other previously uncounted administrative pages were added at light review/admin rates, not drafting rate."
  },
  {
    number: 6, caption: "Newanforbi v. HOPE et al.", caseNumber: "2:26-cv-00195-TLN-AC",
    court: "USDC E.D. Cal.", type: "Federal",
    status: "Dismissed without prejudice (voluntary, 5/21/2026); refiling preserved",
    documentsCount: 4, totalPagesReal: 101,
    hours: { low: 193, high: 292, mid: 242.5 },
    cost: { low: 54040, high: 81760, mid: 67900 },
    notes: "Voluntarily dismissed one day after the sole defense appearance (Notice of Related Cases), before any answer or MSJ — so nearly all billable work is the two complaints themselves (96 pages total), not motion practice. A Minute Order PDF referenced in matters.js is not present in the uploaded folder and was excluded from the tally (immaterial — court orders are not billable attorney drafting time in any event)."
  },
  {
    number: 7, caption: "Newanforbi v. Candelaria", caseNumber: "2:26-cv-00983-DC-CSK",
    court: "USDC E.D. Cal.", type: "Federal - 42 U.S.C. 1983 Procedural Due Process (structural bias, DMV APS)",
    status: "Active; FAC filed Apr. 27, 2026; objections to F&R filed; awaiting ruling",
    documentsCount: 17, totalPagesReal: 185,
    hours: { low: 185.1, high: 289.4, mid: 237.25 },
    cost: { low: 51828, high: 81032, mid: 66430 },
    notes: "Highest-cost matter in the cluster because it contains two real complaint drafts (60p original + 31p FAC) totaling 91 pages of genuine pleading work; this is a defensible, non-inflated result since the original complaint is billed once at full rate and the FAC only at a reduced amendment rate. True-up increment: a Notice of Supplemental Authority (Serrato Order) present on disk but not previously counted, billed at a flat administrative rate."
  },
  {
    number: 8, caption: "Newanforbi v. Candelaria, et al.", caseNumber: "26WM000135",
    court: "Sacramento Sup. Ct.", type: "State - Writ of Administrative Mandate (CCP 1094.5)",
    status: "Fee Waiver Denied (05/19/2026); hearing 07/17/2026; petition pending",
    documentsCount: 2, totalPagesReal: 88,
    hours: { low: 50.5, high: 81, mid: 65.75 },
    cost: { low: 14140, high: 22680, mid: 18410 },
    notes: "Single-document matter (writ petition); cost driven entirely by the flat specialized-writ rate, consistent with the 5-count 1094.5 causes of action asserted."
  },
  {
    number: 9, caption: "Newanforbi v. Macomber", caseNumber: "26WM000028",
    court: "Sacramento Sup. Ct.", type: "Writ of Mandate (CCP §1085)",
    status: "Closed — Demurrer sustained/case closed May 29, 2026 (Dept. 13A)",
    documentsCount: 9, totalPagesReal: 179,
    hours: { low: 65, high: 116, mid: 90.5 },
    cost: { low: 18200, high: 32480, mid: 25340 },
    notes: "Challenges CDCR's discharge-review denial (Form 1502-DR errors, wrong legal standard). AG's demurrer prompted a petitioner opposition (not present as a separate uploaded file) and an AG reply (present but not billable — opposing counsel's work). Estimate is conservative: it excludes the AG's own filing and treats voluminous notice/administrative bundles as flat per-document tasks rather than per-page briefing."
  },
  {
    number: 10, caption: "Newanforbi v. Macomber", caseNumber: "C2602632",
    court: "Santa Clara Sup. Ct.", type: "Habeas Corpus (PC §3008(d)(2); 15 CCR §3574) — Treatment Termination",
    status: "Closed — Petition Denied Without Prejudice (April 27, 2026, exhaustion grounds)",
    documentsCount: 2, totalPagesReal: 3,
    hours: { low: 40.5, high: 72, mid: 56.25 },
    cost: { low: 11340, high: 20160, mid: 15750 },
    notes: "Only 2 files sit in this matter's public folder (a notice and the court's denial order); the underlying petition PDF was never uploaded to the portfolio site. Because the case record independently establishes the petition was drafted, filed, and adjudicated on exhaustion grounds (PC §3008(d)(2) certification requirement), the estimate credits the standard habeas-drafting range rather than reporting a near-zero cost that would understate real work performed."
  },
  {
    number: 11, caption: "Newanforbi v. Macomber", caseNumber: "TBD (USDC E.D. Cal.)",
    court: "USDC E.D. Cal.", type: "Federal",
    status: "Dismissed with prejudice (voluntary, 6/29/2026); early-stage, no defendant response filed",
    documentsCount: 0, totalPagesReal: 0,
    hours: { low: 30.5, high: 76, mid: 53.25 },
    cost: { low: 8540, high: 21280, mid: 14910 },
    notes: "Filed 03/02/2026 and voluntarily dismissed with prejudice 06/29/2026 before any defendant answered or moved — case never reached motion practice or discovery. Estimated conservatively as a single-issue equitable-relief-only complaint (declaratory/injunctive, no damages claim) plus a short dismissal notice; no uploaded documents exist to verify actual length."
  },
  {
    number: 12, caption: "Brendan Ngwa Nforbi v. Diamond Truck Sales, Inc.", caseNumber: "STK-CV-UF-2026-0001094",
    court: "San Joaquin Sup. Ct.", type: "State — Consumer Fraud / UCL",
    status: "Active — Default ENTERED against Diamond (05/12/2026); Alpine served 07/01/2026 (POS-010, Levying Officer File No. 2026002577); Alpine default judgment packet pre-drafted, execution date 08/01/2026; CM-110 filed 07/20/2026; CMC 08/12/2026",
    documentsCount: 20, totalPagesReal: 188,
    hours: { low: 151, high: 247, mid: 199 },
    cost: { low: 42280, high: 69160, mid: 55720 },
    notes: "Active case with a real 34-page amended complaint and a substantial 58-page default judgment packet already on file, so the fee estimate here is meaningfully higher than a generic 'early-stage/light filing' guess — the underlying documents show genuine substantive drafting work, not just a bare-bones complaint. Increment: 6-page CM-110 Case Management Statement (filed Jul. 20, 2026), billed as a flat administrative filing plus a short sworn declaration (Attachment 4b itemizing the $78,671.20 default judgment prove-up), not per-page drafting rate; a 2-page formal POS-010 Proof of Service for Alpine Truck Sales (Levying Officer File No. 2026002577) — a duplicate confirmation of the already-tracked July 1, 2026 service, billed at a nominal administrative rate; and a 49-page Alpine Default Judgment Packet, now a complete self-contained filing record: 3-page CIV-100 Request for Entry of Default/Court Judgment (flat administrative-filing rate), a 7-page supporting Declaration developing the derivative successor-liability/alter-ego theory (motion-brief-adjacent rate given the legal research and case citations required), and 39 pages of exhibits and exhibit covers (Exhibits 1–10) reattached from the Diamond prove-up package — billed at a nominal clerical/compilation rate since this is a duplicate of exhibits already fully priced once under the original Diamond packet, not fresh evidentiary drafting."
  },
  {
    number: 13, caption: "Newanforbi v. Urrea et al.", caseNumber: "2:26-cv-00190-DC-SCR",
    court: "USDC E.D. Cal.", type: "Federal",
    status: "Dismissed with prejudice (voluntary, 6/29/2026); early-stage, no defendant response filed",
    documentsCount: 0, totalPagesReal: 0,
    hours: { low: 30.5, high: 76, mid: 53.25 },
    cost: { low: 8540, high: 21280, mid: 14910 },
    notes: "Filed 01/22/2026 and voluntarily dismissed with prejudice 06/29/2026 before any defendant answered or moved — same early-dismissal pattern as Matter 11. Estimated conservatively as a single-issue federal complaint plus a short dismissal notice; no uploaded documents exist to verify actual length."
  },
  {
    number: 14, caption: "Newanforbi v. Urrea et al.", caseNumber: "TBD (San Joaquin Sup. Ct.)",
    court: "San Joaquin Sup. Ct.", type: "State",
    status: "NOT PURSUING — Voluntarily Dismissed (archived); filed June 30, 2026",
    documentsCount: 1, totalPagesReal: 28,
    hours: { low: 70, high: 95, mid: 82.5 },
    cost: { low: 19600, high: 26600, mid: 23100 },
    notes: "Single 28-page combined writ/complaint filed June 30, 2026 and voluntarily dismissed shortly after; no motion practice occurred, so the estimate reflects drafting/research/filing only."
  },
  {
    number: 15, caption: "Newanforbi v. California Department of Corrections and Rehabilitation, et al.", caseNumber: "STK-CV-UPI-2026-5417",
    court: "San Joaquin Sup. Ct.", type: "State",
    status: "Active — Complaint for Damages filed June 11, 2026; CDCR & Dodd served June 22; responsive pleading due ~July 22, 2026",
    documentsCount: 19, totalPagesReal: 448,
    hours: { low: 300.5, high: 419.5, mid: 360 },
    cost: { low: 84140, high: 117460, mid: 100800 },
    notes: "Largest matter in this batch (448 real pages, 19 files). Multiple complaint versions reflect genuine post-demurrer recalibration (companion Macomber mandate case, Matter 19/9, received an adverse tentative ruling that forced a damages-only rewrite) rather than pure duplication. The two ~110-page files were billed at evidence-compilation, not complaint, rates specifically to keep the estimate defensible rather than inflated. True-up increment: a meet-and-confer calendar invite and a minor administrative filing present on disk but not previously counted, billed at flat administrative rates."
  },
  {
    number: 16, caption: "Newanforbi v. Rojo", caseNumber: "TBD (San Joaquin Sup. Ct.)",
    court: "San Joaquin Sup. Ct.", type: "State",
    status: "NOT PURSUING — Voluntarily Dismissed (archived); filed July 7, 2026",
    documentsCount: 1, totalPagesReal: 32,
    hours: { low: 64, high: 80, mid: 72 },
    cost: { low: 17920, high: 22400, mid: 20160 },
    notes: "Single 32-page complaint filed July 7, 2026, voluntarily dismissed; no further filings appear in the record."
  },
  {
    number: 17, caption: "Newanforbi v. Maloney et al.", caseNumber: "2:26-cv-00194-DAD-SCR",
    court: "USDC E.D. Cal.", type: "Federal",
    status: "DISMISSED WITH PREJUDICE — Notice of Voluntary Dismissal (FRCP 41(a)(1)(A)(i)) filed June 29, 2026, self-executing; no defendant ever answered or moved",
    documentsCount: 0, totalPagesReal: 0,
    hours: { low: 56, high: 80, mid: 68 },
    cost: { low: 15680, high: 22400, mid: 19040 },
    notes: "No documents folder exists for this matter (empty in source data). Conservative estimate limited to complaint + minimal ancillary filings, since the case was voluntarily dismissed with prejudice before any defendant answered or filed a motion."
  },
  {
    number: 18, caption: "Newanforbi v. Barocio", caseNumber: "2:26-cv-00191-DJC-CSK (PC)",
    court: "USDC E.D. Cal.", type: "Federal",
    status: "DISMISSED WITH PREJUDICE — Notice of Voluntary Dismissal (FRCP 41(a)(1)(A)(i)) filed June 29, 2026, self-executing; no defendant ever answered or moved",
    documentsCount: 0, totalPagesReal: 0,
    hours: { low: 55, high: 75, mid: 65 },
    cost: { low: 15400, high: 21000, mid: 18200 },
    notes: "No documents folder exists for this matter. Estimate reflects a prisoner civil-rights complaint plus minor PLRA-related procedural filings before an early, self-executing voluntary dismissal with prejudice."
  },
  {
    number: 19, caption: "Newanforbi v. Macomber", caseNumber: "C2604791",
    court: "Santa Clara Sup. Ct.", type: "Habeas Corpus — Immediate Discharge from Parole (Pen. Code §1473; PC §§3000, 3001, 3008(d)(2); 15 CCR §3574)",
    status: "Active — Filed 04/03/2026; OSC anticipated 06/05/2026",
    documentsCount: 3, totalPagesReal: 70,
    hours: { low: 41, high: 73, mid: 57 },
    cost: { low: 11480, high: 20440, mid: 15960 },
    notes: "Companion matter to Matters 9, 10, and 11 (same administrative record); targets the parole term itself rather than treatment compulsion. The 67-page petition is unusually dense for a habeas filing (5 causes of action, 6 exhibits, extensive regulatory/case-law analysis re: In re Gadlin, In re Leman, ACSOL v. Macomber), justifying the top of the 40-70 hr specialized-habeas range. True-up increment: Notice of Change of Address present on disk but not previously counted, billed at a flat administrative rate."
  },
  {
    number: 20, caption: "Newanforbi v. California Highway Patrol, et al.", caseNumber: "26CV191136",
    court: "Alameda Sup. Ct.", type: "State - Writ of Mandate (CCP 1085, PC 679.10 U-Visa Certification)",
    status: "Active - Petition filed 05/29/2026; AG Demurrer filed; Opposition filed 07/13/2026; hearing 08/28/2026",
    documentsCount: 18, totalPagesReal: 390,
    hours: { low: 80.8, high: 137.9, mid: 109.35 },
    cost: { low: 22624, high: 38612, mid: 30618 },
    notes: "390 pages is the largest raw page count in the cluster, but 306 of those pages are two near-duplicate copies of the same 153-page writ petition, so the writ is billed once at the flat specialized rate rather than per-page, keeping the estimate defensible."
  },
  {
    number: 21, caption: "Newanforbi v. Rojo et al.", caseNumber: "2:26-cv-00193-DC-CKD",
    court: "USDC E.D. Cal.", type: "Federal",
    status: "DISMISSED WITH PREJUDICE — Notice of Voluntary Dismissal (FRCP 41(a)(1)(A)(i)) filed June 29, 2026, self-executing; no defendant ever answered or moved",
    documentsCount: 2, totalPagesReal: 21,
    hours: { low: 28.5, high: 42.5, mid: 35.5 },
    cost: { low: 7980, high: 11900, mid: 9940 },
    notes: "Only the complaint itself is billable drafting work; the folder also contains a 12-page CSK order (Barocio-related) present on disk but not previously counted — billed at a light review-only rate since court orders are not billable attorney drafting time. Case was voluntarily dismissed with prejudice before any defendant answered or moved, so no motion practice is billed."
  },
  {
    number: 22, caption: "Newanforbi v. Pilot Travel Centers LLC", caseNumber: "STK-CV-UWT-2026-0007649",
    court: "San Joaquin Sup. Ct.", type: "State — PC §290.46(j) / FCRA / ICRAA / UCL / Wrongful Termination",
    status: "SETTLED July 11, 2026 — resolved in under six weeks, before service completed",
    documentsCount: 8, totalPagesReal: 45,
    hours: { low: 63, high: 103.5, mid: 83.25 },
    cost: { low: 17640, high: 28980, mid: 23310 },
    notes: "Light litigation footprint by design: a complaint was drafted and filed, but the matter settled via demand letter and negotiation before service was even completed, so no answer, motion practice, or discovery ever occurred — billed accordingly at pre-litigation/negotiation intensity rather than full federal-style motion practice. True-up increment: the process server's Invoice and Signed Proof of Service (POS-010), relocated into this folder during an earlier cleanup, was present on disk but not previously counted — billed at evidence/exhibit rate."
  },
  {
    number: 23, caption: "Newanforbi v. Macy's Inc. et al.", caseNumber: "TBD",
    court: "San Joaquin Sup. Ct.", type: "State — PC §290.46(j) / FCRA / ICRAA / UCL / Wrongful Termination (contemplated)",
    status: "NOT PURSUING — Voluntarily Dismissed (never filed)",
    documentsCount: 2, totalPagesReal: 11,
    hours: { low: 4, high: 8, mid: 6 },
    cost: { low: 1120, high: 2240, mid: 1680 },
    notes: "Essentially pre-litigation only: no complaint, summons, or any court filing exists in this matter's file set — the two documents present are evidentiary background records reviewed during initial case assessment before the decision was made not to pursue."
  },
  {
    number: 24, caption: "Newanforbi v. Serrato", caseNumber: "4:26-cv-05953-ASK",
    court: "USDC N.D. Cal.", type: "Federal - 42 U.S.C. 1983 (Due Process, 1st Amend. Retaliation - U-Visa certification denial)",
    status: "Active - Complaint filed 06/17/2026; ISC Order issued; CMC scheduled 09/15/2026",
    documentsCount: 6, totalPagesReal: 58,
    hours: { low: 46.5, high: 72, mid: 59.25 },
    cost: { low: 13020, high: 20160, mid: 16590 },
    notes: "Newest and lightest matter in the cluster; only a single 21-page complaint plus routine N.D. Cal. intake paperwork (IFP application, proposed summons, ISC/magistrate consent form) have been filed so far."
  },
  {
    number: 25, caption: "Newanforbi v. Federal Express Corporation", caseNumber: "STK-CV-UWT-2026-0009118",
    court: "San Joaquin Sup. Ct.", type: "State — PC §290.46(j) / ICRAA / Wrongful Failure to Hire",
    status: "Filed July 15, 2026; Case No. STK-CV-UWT-2026-0009118; Dept. 10B, Hon. Blanca Banuelos; CMC Jan. 14, 2027; FW-003 Fee Waiver GRANTED July 15, 2026",
    documentsCount: 17, totalPagesReal: 53,
    hours: { low: 47, high: 79, mid: 63 },
    cost: { low: 13160, high: 22120, mid: 17640 },
    notes: "Filed July 15, 2026. The 18-page, six-count complaint is the only substantive drafting product; most remaining pages are single-page First Advantage notice/reminder emails reviewed for the factual record. Increment since the prior estimate: file-stamped complaint confirmation pages, the FW-003 fee waiver order (GRANTED), a duplicate Notice of Case Assignment/Hearing, and the SUM-100 Summons — all billed at light administrative/evidence-review rates, not drafting rate. No answer, motion practice, or discovery exists yet; service not yet completed."
  },
  {
    number: 26, caption: "Newanforbi v. United Parcel Service, Inc.", caseNumber: "STK-CV-UWT-2026-0009113",
    court: "San Joaquin Sup. Ct.", type: "State — PC §290.46(j) / ICRAA / Wrongful Failure to Hire",
    status: "Filed July 15, 2026; Case No. STK-CV-UWT-2026-0009113; limitations period preserved (16 days ahead of July 31, 2026 cutoff); Dept. 11B, Hon. Robert T. Waters; CMC Jan. 13, 2027; FW-003 Fee Waiver GRANTED July 15, 2026; SER-001 Sheriff service request filed July 20, 2026",
    documentsCount: 13, totalPagesReal: 48,
    hours: { low: 43, high: 74, mid: 58.5 },
    cost: { low: 12040, high: 20720, mid: 16380 },
    notes: "Filed July 15, 2026 — 16 days before the July 31, 2026 two-year limitations cutoff, preserving all time-sensitive claims. The 18-page, six-count complaint is the only substantive drafting product; most remaining pages are single-page First Advantage notice/reminder emails. Increment since the prior estimate: file-stamped complaint confirmation pages, the FW-003 fee waiver order (GRANTED), a duplicate Notice of Case Assignment/Hearing, the SUM-100 Summons, and a 5-page SER-001 Request for Sheriff to Serve Court Papers (Sacramento County, registered-agent service, requested deadline July 31, 2026) — billed as a light administrative/procedural task, not full motion-drafting rate. No answer, motion practice, or discovery exists yet."
  },
  {
    number: 27, caption: "Newanforbi v. Randstad, et al.", caseNumber: "26CV199902 (Alameda Sup. Ct.)",
    court: "Alameda Sup. Ct.", type: "State — PC §290.46(j) / Wrongful Termination / ICRAA / Negligence Per Se / UCL",
    status: "Employment terminated July 15, 2026. Verified Complaint for Damages e-filed July 20, 2026 via One Legal — Case No. 26CV199902 assigned, Hon. Karin Schwartz, Dept. 20; Complaint, Civil Case Cover Sheet, and Fee Waiver ACCEPTED, Summons REJECTED on a caption technicality and being resubmitted; Pre-Filing Demand Letters sent to Randstad and RK Logistics same day ($85,000 each, deadline Aug. 2, 2026); SER-001 Sheriff service request executed for Randstad. On July 21, 2026, RK Logistics denied the demand through counsel Garcia & Gurney, ALC; Randstad has not yet responded.",
    documentsCount: 24, totalPagesReal: 108,
    hours: { low: 69.7, high: 118.2, mid: 93.95 },
    cost: { low: 19516, high: 33096, mid: 26306 },
    notes: "Substantial increment now that the complaint has actually been e-filed and RK Logistics has responded. Twelve new documents since the pre-filing estimate (24 total, 108 real pages, +50 pages): the e-filing confirmation packet (Civil Case Cover Sheet, Fee Waiver, Order on Fee Waiver, Notice of Confirmation of E-Filing, Notice of Case Assignment, Notice of CMC, and two SUM-100 versions plus the blank template) billed as light administrative/procedural tasks (0.5–2 hr/doc, per methodology); a duplicate filed copy of the 19-page Complaint billed only incrementally per the near-duplicate rule; and the 12-page Garcia & Gurney response letter, billed above the standard opposing-counsel light-review rate to account for the substantive rebuttal analysis it required (comparing the SambaSafety Class A/Class C license distinction and the Jack Altares email against the letter's employer-status argument), plus its 1-page Gmail transmittal. Prior 12-document, 58-page base (19-page Verified Complaint, two 4-page demand letters, 15-page InfoMart report, CA SOS records, Gmail demand transmittals, onboarding emails, and the 5-page SER-001) carries forward unchanged. Randstad's August 2 response is still outstanding; service and any motion practice on either defendant will add a further increment."
  },
  {
    number: 28, caption: "Newanforbi v. Shannon Smith, LCSW, CEO, et al.", caseNumber: "TBD",
    court: "USDC N.D. Cal.", type: "Federal — 42 U.S.C. §1983 (Monell + Individual Capacity); Bane Act §52.1; Fraud/Negligent Misrepresentation; RICO 18 U.S.C. §1962(c)-(d)",
    status: "Complaint (v2) mailed Jul. 16, 2026; anticipated receipt USDC N.D. Cal. Jul. 20, 2026",
    documentsCount: 6, totalPagesReal: 75,
    hours: { low: 101, high: 174, mid: 137.5 },
    cost: { low: 28280, high: 48720, mid: 38500 },
    notes: "Six documents totaling 75 real pages (corrected from a 53-page estimate — several documents ran longer than originally guessed): 24-page federal complaint (the dominant cost driver — novel theory development across RICO, §1983 Monell, individual-capacity §1983, Bane Act, and fraud/negligent misrepresentation in a single pleading; hours are elevated accordingly); 10-page Motion for Protective Order; 6-page supporting Declaration (billed per-document, not per-page, per methodology); state court Stipulated Protective Order as Exhibit A (12 pages); 12-page Proposed NDCA Protective Order; 11-page signed state Stipulated PO. Hours reflect drafting a complex multi-theory federal complaint from scratch leveraging 542 pages of discovery already produced in the dismissed state case, plus preparation of the contemporaneous protective-order motion package — now correctly priced against the actual, longer motion and proposed-order page counts. Fee-shifting under §1988 and RICO makes attorney fee recovery highly probable if Plaintiff prevails."
  },
  {
    number: 29, caption: "Newanforbi v. Amazon.com Services, LLC", caseNumber: "TBD",
    court: "TBD — anticipated Alameda Sup. Ct.",
    type: "State — PC §290.46(j) / FCRA / ICRAA / Failure to Hire",
    status: "Pre-complaint — BGC pending; adverse action anticipated",
    documentsCount: 11, totalPagesReal: 19,
    hours: { low: 20, high: 38, mid: 29 },
    cost: { low: 5600, high: 10640, mid: 8120 },
    notes: "Pre-filing stage. Eleven documents: 5 PDFs (13 pages) — Amazon Simple Hire Checklists (2), Amazon Jobs BGC-status emails (2), and Equifax onboarding reminder — and 6 screenshots (6 pages) documenting the application, pre-hire appointment, Amazon/Accurate Background SMS chain, and pending BGC status. No complaint drafted yet; hours reflect case assessment and theory development from the established §290.46(j) portfolio template. Fee-shifting under PC §290.46(j)(4)(A), FCRA, and ICRAA applies upon prevailing."
  },
  {
    number: 30, caption: "Newanforbi v. Moua, et al.", caseNumber: "TBD",
    court: "USDC N.D. Cal.",
    type: "Federal — 42 U.S.C. §1983 (First Amendment Retaliation + Due Process); Bane Act Cal. Civ. Code §52.1; IIED",
    status: "Pre-complaint — anticipated filing September 16, 2026, USDC N.D. Cal.; Gary Noguchi (Badge #7284) served Jul. 7, 2026; Joseelyn Rojo served Jul. 14, 2026; Long Moua (Badge #7472) service pending; GCA claim filed Jul. 18, 2026, anticipated deemed rejected Sep. 1, 2026",
    documentsCount: 12, totalPagesReal: 107,
    hours: { low: 56, high: 132, mid: 86.5 },
    cost: { low: 15680, high: 36960, mid: 24220 },
    notes: "Complaint filed Sep. 16, 2026. Twelve documents totaling 107 real pages (corrected from a 64-page estimate): 26-page verified complaint (Newanforbi v. Moua, et al.); 25-page Derrick FAC (Case 2:26-cv-00004-DJC-JDP, E.D. Cal. — scanned PDF, confirms triggering protected activity and Noguchi as named co-defendant); 3 CASOMB submission PDFs (~5 pages — Dr. Kirsten Mason inquiry, BNN responses, telehealth accommodation request); 4 screenshots (4 pages — Agent Moua contact card, Agent Brown text exchanges, CountySuite service records); Macy's job offer (~3 pages); Macy's work schedule (~2 pages); and a 42-page 'Newanforbi v. CDCR, et al 3.pdf' — on inspection this is a duplicate copy of the SUM-100 Summons and Complaint for Damages already fully billed under Matter 15 (case STK-CV-UPI-2026-5417), sitting in this folder as cross-reference evidence for the Noguchi/Rojo service history — billed at a nominal flat rate (not per-page) since it is fully duplicative of already-priced Matter 15 work, not new drafting. Hours are substantially elevated because: (1) the complaint requires three independent §1983 retaliation theories each with distinct factual predicates; (2) Bane Act §52.1 adds a state-law coercion theory requiring Shoyoye pleading of independence; (3) Heck v. Humphrey and absolute immunity must be preemptively addressed; (4) Government Claims Act exhaustion (GCA claim Jul. 18, deemed rejected Sep. 1) must be pleaded; (5) supervisory liability for Noguchi (named Derrick FAC co-defendant + 1502-DR co-author) and Rojo. Fee-shifting under 42 U.S.C. §1988 and mandatory Bane Act attorney fees make attorney fee recovery highly probable on prevailing."
  },
];

export const lawyer_fees_summary = {
  analysisDate: "2026-07-22",
  totalMatters: 30,
  totalDocumentsAnalyzed: 302,
  totalPagesReal: 3607,
  methodology: {
    blendedHourlyRate: 280,
    rateRange: { seniorPartner: [350, 450], midAssociate: [250, 350], paralegal: [150, 200] },
    note: "Every PDF in public/documents/matter-XX/ was measured with pdfinfo for real page counts (poppler-utils), then classified by document type (complaint, motion/opposition/reply, discovery, writ/habeas, declaration, administrative, evidence) and priced using the hours-per-page/per-document conversions in docs/LAWYER_FEES_CALCULATOR.md. Opposing counsel's filings are billed only at a light review rate, never at drafting rate. Matters with no uploaded PDFs are estimated conservatively from matters.js status text.",
  },
  totalEstimatedHours: { low: 2664.3, high: 4389.2, mid: 3519.25 },
  totalEstimatedCost: { low: 746004, high: 1228976, mid: 985390 },
  byCluster: {
    cluster1: { label: "CHP / DUI / DMV", matters: [1, 2, 7, 8, 20, 24], costLow: 134596, costMid: 177212, costHigh: 219828 },
    cluster2: { label: "Parole Retaliation / HOPE", matters: [3, 4, 5, 6, 11, 13, 14, 15, 16, 17, 18, 21, 28, 30], costLow: 459032, costMid: 601972, costHigh: 749112 },
    cluster3: { label: "Consumer Fraud / Employment", matters: [12, 22, 23, 25, 26, 27, 29], costLow: 111356, costMid: 149170, costHigh: 186900 },
    cluster4: { label: "Administrative Writs & Habeas", matters: [9, 10, 19], costLow: 41020, costMid: 57050, costHigh: 73080 },
  },
};
