// Ground-truth lawyer-fee estimate for the entire 24-matter portfolio.
// Real page counts extracted with pdfinfo from every PDF in public/documents/matter-XX/
// (poppler-utils), then classified by document type and priced per the methodology in
// docs/LAWYER_FEES_CALCULATOR.md by five parallel analysis passes, one per case cluster.
// Matters with no uploaded PDFs (4, 11, 13, 17, 18) are estimated from matters.js status text.
export const lawyer_fees = [
  {
    number: 1, caption: "Newanforbi v. CHP et al.", caseNumber: "2:25-cv-01460-DC-CSK",
    court: "USDC E.D. Cal.", type: "Federal - 42 U.S.C. 1983 (4th/14th Amend., Monell)",
    status: "Filed 05/27/2025; MTD fully briefed (MTD, Opposition, Reply); ruling pending",
    documentsCount: 23, totalPagesReal: 108,
    hours: { low: 48.4, high: 85.2, mid: 66.8 },
    cost: { low: 13552, high: 23856, mid: 18704 },
    notes: "Real page counts are far smaller than a naive filename-based guess would suggest (108 total pages, not 1,000+); the MTD briefing cycle is genuinely modest in length. Opposing-party filings (CHP's MTD, AG's Reply) are billed only at a light review rate, not drafting rate."
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
    documentsCount: 33, totalPagesReal: 821,
    hours: { low: 420.1, high: 682.8, mid: 551.45 },
    cost: { low: 117628, high: 191184, mid: 154406 },
    notes: "Largest matter in this batch by real page count (821 pages across 33 files) — driven mainly by heavy bilateral discovery (377 pp) and two large Requests for Judicial Notice (222 pp combined). The prior 712-page 'CASOMB Complaint' estimate in LAWYER_FEES_CALCULATOR.md does not match the actual file (38 real pages); real pdfinfo counts were used throughout. Matters.js notes that 12 underlying discovery-production PDFs (defendants' document production) were removed from the public repository after review and are correctly absent from both the ground-truth JSON and this cost estimate."
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
    documentsCount: 16, totalPagesReal: 181,
    hours: { low: 184.6, high: 287.9, mid: 236.25 },
    cost: { low: 51688, high: 80612, mid: 66150 },
    notes: "Highest-cost matter in the cluster because it contains two real complaint drafts (60p original + 31p FAC) totaling 91 pages of genuine pleading work; this is a defensible, non-inflated result since the original complaint is billed once at full rate and the FAC only at a reduced amendment rate."
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
    status: "Active — Default judgment request submitted 06/15/2026; CMC 08/12/2026",
    documentsCount: 17, totalPagesReal: 131,
    hours: { low: 136, high: 220, mid: 178 },
    cost: { low: 38080, high: 61600, mid: 49840 },
    notes: "Active case with a real 34-page amended complaint and a substantial 58-page default judgment packet already on file, so the fee estimate here is meaningfully higher than a generic 'early-stage/light filing' guess — the underlying documents show genuine substantive drafting work, not just a bare-bones complaint."
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
    documentsCount: 17, totalPagesReal: 445,
    hours: { low: 300, high: 418, mid: 359 },
    cost: { low: 84000, high: 117040, mid: 100520 },
    notes: "Largest matter in this batch (445 real pages, 17 files). Multiple complaint versions reflect genuine post-demurrer recalibration (companion Macomber mandate case, Matter 19/9, received an adverse tentative ruling that forced a damages-only rewrite) rather than pure duplication. The two ~110-page files were billed at evidence-compilation, not complaint, rates specifically to keep the estimate defensible rather than inflated."
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
    documentsCount: 2, totalPagesReal: 69,
    hours: { low: 40.5, high: 72, mid: 56.25 },
    cost: { low: 11340, high: 20160, mid: 15750 },
    notes: "Companion matter to Matters 9, 10, and 11 (same administrative record); targets the parole term itself rather than treatment compulsion. The 67-page petition is unusually dense for a habeas filing (5 causes of action, 6 exhibits, extensive regulatory/case-law analysis re: In re Gadlin, In re Leman, ACSOL v. Macomber), justifying the top of the 40-70 hr specialized-habeas range."
  },
  {
    number: 20, caption: "Newanforbi v. California Highway Patrol, et al.", caseNumber: "26CV191136",
    court: "Alameda Sup. Ct.", type: "State - Writ of Mandate (CCP 1085, PC 679.10 U-Visa Certification)",
    status: "Active - Petition filed 05/29/2026; AG Demurrer filed; Opposition filed 07/11/2026; hearing 08/28/2026",
    documentsCount: 18, totalPagesReal: 390,
    hours: { low: 80.8, high: 137.9, mid: 109.35 },
    cost: { low: 22624, high: 38612, mid: 30618 },
    notes: "390 pages is the largest raw page count in the cluster, but 306 of those pages are two near-duplicate copies of the same 153-page writ petition, so the writ is billed once at the flat specialized rate rather than per-page, keeping the estimate defensible."
  },
  {
    number: 21, caption: "Newanforbi v. Rojo et al.", caseNumber: "2:26-cv-00193-DC-CKD",
    court: "USDC E.D. Cal.", type: "Federal",
    status: "DISMISSED WITH PREJUDICE — Notice of Voluntary Dismissal (FRCP 41(a)(1)(A)(i)) filed June 29, 2026, self-executing; no defendant ever answered or moved",
    documentsCount: 1, totalPagesReal: 9,
    hours: { low: 28, high: 41, mid: 34.5 },
    cost: { low: 7840, high: 11480, mid: 9660 },
    notes: "Only the complaint itself is present in the documents folder. Case was voluntarily dismissed with prejudice before any defendant answered or moved, so no motion practice is billed."
  },
  {
    number: 22, caption: "Newanforbi v. Pilot Travel Centers LLC", caseNumber: "STK-CV-UWT-2026-0007649",
    court: "San Joaquin Sup. Ct.", type: "State — PC §290.46(j) / FCRA / ICRAA / UCL / Wrongful Termination",
    status: "SETTLED July 11, 2026 — resolved in under six weeks, before service completed",
    documentsCount: 7, totalPagesReal: 47,
    hours: { low: 62, high: 102, mid: 82 },
    cost: { low: 17360, high: 28560, mid: 22960 },
    notes: "Light litigation footprint by design: a complaint was drafted and filed, but the matter settled via demand letter and negotiation before service was even completed, so no answer, motion practice, or discovery ever occurred — billed accordingly at pre-litigation/negotiation intensity rather than full federal-style motion practice."
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
    number: 25, caption: "Newanforbi v. Federal Express Corporation", caseNumber: "TBD",
    court: "San Joaquin Sup. Ct.", type: "State — PC §290.46(j) / ICRAA / Wrongful Failure to Hire",
    status: "Complaint drafted and verified July 15, 2026; not yet filed or served",
    documentsCount: 10, totalPagesReal: 27,
    hours: { low: 45, high: 75, mid: 60 },
    cost: { low: 12600, high: 21000, mid: 16800 },
    notes: "Pre-filing stage: the 18-page, six-count complaint is the only substantive drafting product; the remaining 9 pages are single-page First Advantage notice/reminder emails reviewed for the factual record, not drafted. No answer, motion practice, or discovery exists yet because the complaint has not been filed."
  },
  {
    number: 26, caption: "Newanforbi v. United Parcel Service, Inc.", caseNumber: "TBD",
    court: "San Joaquin Sup. Ct.", type: "State — PC §290.46(j) / ICRAA / Wrongful Failure to Hire",
    status: "Complaint drafted and verified July 15, 2026; not yet filed or served — filing is time-sensitive",
    documentsCount: 5, totalPagesReal: 22,
    hours: { low: 40, high: 68, mid: 54 },
    cost: { low: 11200, high: 19040, mid: 15120 },
    notes: "Pre-filing stage, same posture as Matter 25: the 18-page, six-count complaint is the only substantive drafting product; the remaining 4 pages are single-page First Advantage notice/reminder emails. No answer, motion practice, or discovery exists yet because the complaint has not been filed."
  },
  {
    number: 27, caption: "Newanforbi v. Randstad, et al.", caseNumber: "TBD",
    court: "San Joaquin Sup. Ct.", type: "State — PC §290.46(j) / FCRA / ICRAA / Wrongful Termination",
    status: "Pre-adverse notice received Jul. 13, 2026; adverse action imminent; complaint not yet drafted or filed",
    documentsCount: 8, totalPagesReal: 24,
    hours: { low: 32, high: 58, mid: 44 },
    cost: { low: 8960, high: 16240, mid: 12320 },
    notes: "Pre-filing stage. Eight documents analyzed: three onboarding/notice emails (rehire confirmation, MVR request, InfoMart FCRA pre-adverse notice); the 15-page InfoMart background check report (Order No. 15780719) — the evidentiary centerpiece confirming registry as the sole adverse flag; and four corroborating screenshots (Indeed application, RK Logistics auto-SMS, two Randstad recruiter iMessages establishing the inhouse staffing pipeline from June 30 Indeed application through July 2 Watkins referral). Hours reflect case assessment, initial theory development, BGC report analysis, and complaint-drafting preparation based on the Matters 22/25/26 template. Once drafted, the complaint will add a substantial increment tracked in a future update."
  },
  {
    number: 28, caption: "Newanforbi v. Shannon Smith, LCSW, CEO, et al.", caseNumber: "TBD",
    court: "USDC N.D. Cal.", type: "Federal — 42 U.S.C. §1983 (Monell + Individual Capacity); Bane Act §52.1; Fraud/Negligent Misrepresentation; RICO 18 U.S.C. §1962(c)-(d)",
    status: "Complaint (v2) mailed Jul. 16, 2026; anticipated receipt USDC N.D. Cal. Jul. 20, 2026",
    documentsCount: 6, totalPagesReal: 53,
    hours: { low: 90, high: 155, mid: 122.5 },
    cost: { low: 25200, high: 43400, mid: 34300 },
    notes: "Six documents totaling approximately 53 pages: 22-page federal complaint (the dominant cost driver — novel theory development across RICO, §1983 Monell, individual-capacity §1983, Bane Act, and fraud/negligent misrepresentation in a single pleading; hours are elevated accordingly); 4-page Motion for Protective Order; 3-page supporting Declaration; state court Stipulated Protective Order as Exhibit A (~10 pages); 5-page Proposed NDCA Protective Order; 9-page signed state Stipulated PO. Hours reflect drafting a complex multi-theory federal complaint from scratch leveraging 542 pages of discovery already produced in the dismissed state case, plus preparation of the contemporaneous protective-order motion package. Fee-shifting under §1988 and RICO makes attorney fee recovery highly probable if Plaintiff prevails."
  },
];

export const lawyer_fees_summary = {
  analysisDate: "2026-07-17",
  totalMatters: 28,
  totalDocumentsAnalyzed: 232,
  totalPagesReal: 3228,
  methodology: {
    blendedHourlyRate: 280,
    rateRange: { seniorPartner: [350, 450], midAssociate: [250, 350], paralegal: [150, 200] },
    note: "Every PDF in public/documents/matter-XX/ was measured with pdfinfo for real page counts (poppler-utils), then classified by document type (complaint, motion/opposition/reply, discovery, writ/habeas, declaration, administrative, evidence) and priced using the hours-per-page/per-document conversions in docs/LAWYER_FEES_CALCULATOR.md. Opposing counsel's filings are billed only at a light review rate, never at drafting rate. Matters with no uploaded PDFs are estimated conservatively from matters.js status text.",
  },
  totalEstimatedHours: { low: 2513.6, high: 4088.0, mid: 3299.8 },
  totalEstimatedCost: { low: 703808, high: 1144640, mid: 923944 },
  byCluster: {
    cluster1: { label: "CHP / DUI / DMV", matters: [1, 2, 7, 8, 20, 24], costLow: 134176, costMid: 176372, costHigh: 218568 },
    cluster2: { label: "Parole Retaliation / HOPE", matters: [3, 4, 5, 6, 11, 13, 14, 15, 16, 17, 18, 21, 28], costLow: 439432, costMid: 572012, costHigh: 704592 },
    cluster3: { label: "Consumer Fraud / Employment", matters: [12, 22, 23, 25, 26, 27], costLow: 89320, costMid: 118720, costHigh: 148680 },
    cluster4: { label: "Administrative Writs & Habeas", matters: [9, 10, 19], costLow: 40880, costMid: 56840, costHigh: 72800 },
  },
};
