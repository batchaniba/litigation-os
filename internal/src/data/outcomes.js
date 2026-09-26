import { damages_table } from "./damages.js";
import { withMatterIdentity } from "./matterIdentity.js";

// portfolio_exposure is derived from damages_table (the actively-maintained, de-duplicated
// category rollup) rather than hand-maintained separately, so the headline figures can never
// drift out of sync with the category rows behind them again.
const sumColumn = (key) => damages_table.reduce((total, row) => total + row[key], 0);

// Matter identity (caption / case_no / court) is joined from summaries via
// matterIdentity.js. Keep a row-level `caption` only when it differs from the
// matter caption (e.g. defendant-specific demand labels).
const enrichOutcome = (row) => withMatterIdentity(row, { numberKey: "matter" });
const enrichOutcomes = (rows) => (rows ?? []).map(enrichOutcome);

const outcomes_raw = {
  realized: [
    {
      matter: 22,
      type: "settlement",
      status: "SETTLED",
      date: "July 14, 2026",
      // Settlement figures never ship in the public bundle (see settlement memo).
      amount: 0,
      confidential: true,
      speed: "Under 6 weeks from filing",
      served: false,
      claims: "PC §290.46(j)(2)(E) Wrongful Termination; Tameny; ICRAA; UCL §17200",
      notes: "Defendant's own Post-Adverse Action Notice named the registry as the sole basis for termination — no ambiguity on liability. Resolved pro se before service was completed. First portfolio matter to reach a negotiated resolution. CIV-110 Request for Dismissal (entire action with prejudice) filed and entered August 6, 2026 — settled action closed. FLAGGED: this settlement's case number and existence have since been cited by name as persuasive precedent in demand letters to other corporate defendants (Matters 25, 26, 27). Only the signature page of the signed release is in the document repository (see Matter 22) — the confidentiality clause's actual scope (amount only, vs. the fact/existence of settlement) has not been confirmed against the full release text. Worth resolving before this case number is cited again."
    }
  ],
  // Matter 12 default track closed Aug. 12, 2026 when Diamond/Alpine appeared through
  // Gulomjon Azimov and disputed service — no near-term recovery is currently booked.
  anticipated: [],
  // Matter 27 demands removed Sep. 25, 2026: resolved under a confidential agreement.
  // Demand and settlement figures stay internal (internal/docs/settlement/).
  active_demands: [],

  portfolio_exposure: {
    conservative: sumColumn("conservative"),
    moderate: sumColumn("moderate"),
    aggressive: sumColumn("aggressive"),
  },
  judicial_opinions: [
    {
      matter: 20,
      judge: "Hon. Jenna M. Whitman",
      date: "August 29, 2026",
      type: "merits",
      outcome: "mixed",
      title: "ORDER Sustaining Demurrer In Part, with Leave to Amend (CHP Demurrer to Petition for Writ of Mandate)",
      holding: "Entered after the August 28, 2026 hearing. First cause of action (ministerial duty / abuse of discretion under Pen. Code §679.10): OVERRULED. Crediting the petition's allegations that neither Petitioner nor his vehicle smelled of alcohol, that he showed no signs of impairment, and that the arresting officers lied in the report, a finder of fact could reasonably find probable cause for the November 1, 2024 arrest was lacking, which could support a finding that CHP abused its discretion in refusing to certify Form I-918 (People v. Wolterman; Espinoza v. Shiomoto). Second cause of action (reason-giving, §679.10(i)(2)): SUSTAINED WITHOUT LEAVE — specificity is required only for noncooperation denials, and CHP denied for lack of qualifying crime. Third cause of action (helpfulness presumption, §679.10(h)): SUSTAINED WITHOUT LEAVE — the presumption never came into play on a qualifying-crime denial. Fourth cause of action (declaratory relief): SUSTAINED WITH LEAVE TO AMEND — the pleaded declarations were pure questions of law; Petitioner may amend within 20 days of notice of entry to narrow to the concrete controversy. Dutra and Paul dismissed by stipulation; their and Serrato's September 18 demurrer hearings vacated. CMC continued to October 28, 2026, 4:00 p.m., Dept. 25. Clerk served notice of entry August 31, 2026 (CCP §1010.6 e-service on Petitioner and DAG Ing, plus mail to 1455 Cat Tail Drive).",
      significance: "The first entered merits ruling in the CHP U-visa mandate. Count 1 survives for trial on whether the November 1, 2024 stop was qualifying criminal activity because probable cause was lacking — the same factual predicate Magistrate Judge Krishnan found plausible in Serrato (Matter 24) and the same incident Magistrate Judge Kim treated as probable cause as a matter of law in the Matter 1 F&R. Counts 2 and 3 are dead on this petition. Count 4 is optional leave only; default path is proceed on Count 1 alone and await the answer. Live respondents are CHP and Serrato.",
      document_path: "/documents/opinions/Newanforbi v California CHP - Alameda Sup Ct - Order Sustaining Demurrer In Part Aug 29 2026.pdf"
    },
    {
      matter: 28,
      judge: "Magistrate Judge Lisa J. Cisneros",
      date: "August 26, 2026",
      type: "procedural",
      outcome: "mixed",
      title: "Order Regarding Payment of Filing Fee and Application to Proceed In Forma Pauperis (Dkt. 11)",
      holding: "Plaintiff's original IFP application (Dkt. 2) DENIED AS MOOT — he paid the filing fee in lieu of the supplemental IFP form required by the July 23 order (Dkt. 7), and he filed the state-court demurrer decision. No further response to Dkt. 7 is required. Because the fee is paid, the Court will not screen the complaint sua sponte under 28 U.S.C. §1915(e)(2)(B) and will not decide case or issue preclusion from the Matter 5 HOPE demurrer; those defenses are left for Defendants to raise after they are served and appear. The Order 'should not be construed as implying any opinion by the Court as to whether such defenses might apply.' Plaintiff is DIRECTED to serve process under Rule 4.",
      significance: "Closes the July 23 IFP / state-decision to-do list and takes Matter 28 off the §1915 screening track that produced the adverse F&Rs in Matters 1 and 7. Preclusion from Palacios (Matter 5) is not dead — it is just not a sua sponte issue anymore. The live clock is Rule 4 service on Smith and HOPE (4(m) ~October 19, 2026 from the July 21 filing). This is the opposite of a merits win; it is permission to serve and proceed.",
      document_path: "/documents/opinions/Newanforbi v Smith - USDC NDCal - Order Directing Service Aug 26 2026.pdf"
    },
    {
      matter: 24,
      caption: "Newanforbi v. Serrato — related to Nforbi v. Meza-Gonzalez",
      judge: "Magistrate Judge Ajay S. Krishnan",
      date: "August 24, 2026",
      type: "procedural",
      outcome: "favorable",
      title: "Order Granting Administrative Motion to Consider Whether Cases Should Be Related (Civil L.R. 3-12)",
      holding: "Newanforbi v. Serrato (4:26-cv-05953-ASK) and Nforbi v. Meza-Gonzalez et al. (3:26-cv-08271-PHK, Matter 32) are RELATED. Clerk directed to reassign Meza-Gonzalez to Magistrate Judge Krishnan. Meza CMC to be rescheduled. Serrato CMC remains September 15, 2026.",
      significance: "Puts the U-visa certification case and the November 1, 2024 false-arrest case in front of the same judge who already held, at §1915 screening, that the CHP incident allegations plausibly state false imprisonment on fabricated evidence. Relatedness is not a merits ruling, but it is the assignment Plaintiff asked for. Serrato's MTD (hearing reset to Sep. 30) and the Meza service / CMC track now run in one courtroom.",
      document_path: "/documents/opinions/Newanforbi v Serrato - USDC NDCal - Order Relating Meza Aug 24 2026.pdf"
    },
    {
      matter: 19,
      caption: "In re Newanforbi (Habeas Corpus)",
      judge: "Hon. Robert Hawk",
      date: "July 2, 2026",
      type: "procedural",
      outcome: "procedural",
      title: "Order Extending Time to Rule on Petition for Writ of Habeas Corpus",
      holding: "The Court found good cause to extend the time in which to rule on Plaintiff's habeas petition, citing the need to thoroughly review the voluminous papers filed and the court's recent workload. The time to issue an order was extended to August 1, 2026. (Cal. Rules of Court, rule 4.551(i).)",
      significance: "A procedural extension only — not a ruling on the merits. Confirms the petition, filed April 3, 2026 seeking immediate and unconditional discharge from parole, remains under active review by the Court rather than having lapsed or been summarily denied. The extension itself is notable: the Court's own stated reason — the volume of the record — reflects the substantiality of the papers filed in support of discharge. August 1, 2026 is now the operative deadline for the Court to rule.",
      document_path: "/documents/opinions/Newanforbi Habeas - Santa Clara Sup Ct - Order Extending Time Jul 2 2026.pdf"
    },
    {
      matter: 20,
      judge: "Hon. Jenna Whitman",
      date: "July 15, 2026",
      type: "procedural",
      outcome: "procedural",
      title: "Order Initial Case Management Conference — Continued to September 2, 2026",
      holding: "The Court's tentative ruling was not contested at the hearing and was affirmed: because the pleadings are not yet at issue, the Initial Case Management Conference scheduled for July 15, 2026 is continued to September 2, 2026, at 4:00 PM in Department 25, Rene C. Davidson Courthouse. Signed by Judge Whitman July 15, 2026; entered and file-stamped by the Clerk July 21, 2026, with a Certificate of Electronic Service on Petitioner and DAG Vanessa Kelley Ing and a Certificate of Mailing to Petitioner's address of record.",
      significance: "Formalizes, as a signed and entered order, what had previously only been documented in this portfolio as a tentative ruling forwarded by courtesy email from Deputy AG Vanessa Ing on July 12, 2026. Purely calendar-driven — the continuance reflects that the AG's Demurrer to the Petition remains pending (hearing set August 28, 2026) and confirms the CMC will not proceed until after the demurrer is resolved. Not a ruling on the merits.",
      document_path: "/documents/opinions/Newanforbi v California CHP - Alameda Sup Ct - Order Continuing CMC to Sep 2 2026.pdf"
    },
    {
      matter: 5,
      caption: "Newanforbi v. Palacios et al. (HOPE Program)",
      judge: "Hon. George J. Abdallah, Jr.",
      date: "July 15, 2026",
      type: "merits",
      outcome: "adverse",
      title: "Order Sustaining Demurrer to First Amended Complaint Without Leave to Amend",
      holding: "Demurrer to the First Amended Complaint SUSTAINED without leave to amend. Court affirmed the July 10, 2026 tentative ruling. Ground: failure to exhaust administrative remedies — exhaustion is a jurisdictional prerequisite and plaintiff failed to satisfy it. Demurrer brought by defendants HOPE Program / Blaze Van Dine, Esq. (Sims, Lawrence & Broghammer). Plaintiff appeared pro se and argued the tentative. Case status updated to Disposed at 1:38 PM; CMC vacated.",
      significance: "Notable as the matter in which defense counsel Blaze Van Dine (Sims, Lawrence & Broghammer) cited plaintiff's Westlaw-indexed federal opinions (2026 WL 1067541; 2026 WL 1389969) in the demurrer brief — the source of the Westlaw accolade featured in this portfolio. Case fully disposed July 15, 2026 (FullCourt: CASESTAT → Disposed; CMC October 13 vacated). The exhaustion defect is procedural and jurisdictional, not a merits adjudication — the discovery record (Clinical Operational Manual, treatment manuals, collateral notes, homework/audit records) and a rejected pre-suit settlement offer (May 23, 2026) establish the factual predicate for the N.D. Cal. complaint against HOPE (Matter 28). Note: Minute Order states exhaustion as the ruling ground; defense's proposed order (signed same date) states broader 'failure to state any cause of action' — the Minute Order controls.",
      document_path: "/documents/opinions/Newanforbi v Palacios - San Joaquin Sup Ct - Demurrer Sustained WOLA Jul 15 2026.pdf"
    },
    {
      matter: 18,
      caption: "Newanforbi v. K. Barocio et al.",
      judge: "Magistrate Judge Chi Soo Kim",
      date: "May 18, 2026",
      type: "merits",
      outcome: "adverse",
      title: "§ 1915A Screening Order: Complaint Dismissed With Leave to Amend",
      holding: "IFP GRANTED. Complaint DISMISSED with leave to amend within 30 days. (1) First Amendment retaliation — Barocio: animus traced to technology embarrassment during BPH hearing, not to plaintiff's protected grievance activity; insufficient nexus between protected conduct and retaliatory act. Hernandez: no facts showing intentional omission or retaliatory motive. John Doe: denial of a grievance is not an adverse action cognizable under the First Amendment. (2) Equal Protection (class of one): 'refused or failed to apply' the PPC is too vague to allege intentional disparate treatment — no facts demonstrating intentional denial. (3) Procedural Due Process: no standalone due process claim for the prison grievance process itself. Complaint dismissed as too vague and conclusory to satisfy Rule 8(a)(2). Plaintiff not granted leave to add new claims or new defendants.",
      significance: "Adverse at §1915A screening but curable — dismissed without prejudice with leave to amend. The court identified specific, fixable pleading gaps: the temporal nexus between the grievance filing and Barocio's animus was traceable to the BPH technology incident rather than the grievance itself, and no facts tied Hernandez to Barocio's conduct. The core factual injury — Barocio's refusal to apply the July 9, 2020 One-Time Positive Programming Credit (PPC) caused 84 days of extended custody and an inflated parole end date of December 2, 2030, confirmed by the disparate treatment of plaintiff's cellmate who received the same credit — was not contested and remains the live factual predicate. This is the source of Westlaw citation 2026 WL 1389969.",
      document_path: "/documents/opinions/Newanforbi v Barocio - USDC EDCal - Screening Order Dismissed WLA May 18 2026.pdf"
    },
    {
      matter: 9,
      judge: "Hon. James P. Arguelles",
      date: "March 10, 2026",
      type: "procedural",
      outcome: "adverse",
      title: "Court Order Vacating Hearing Scheduled on March 27, 2026",
      holding: "Petition must be served in the same manner as a summons (CCP §1096, §§413.10–417.40); mail service is insufficient to establish the Court's jurisdiction over Respondent. Hearing on the merits vacated pending proper service and proof of service filed with the Court.",
      significance: "Procedural ruling only — not on the merits of the writ. Court applied CCP §1088.5 (no action until respondent served). Cure: personal service on Macomber and filing of POS-010 reinstates the right to a merits hearing. Underlying petition remains live.",
      document_path: "/documents/opinions/Newanforbi v Macomber - Sacramento Sup Ct - Minute Order Mar 10 2026.pdf"
    },
    {
      matter: 9,
      judge: "Hon. James P. Arguelles",
      date: "May 29, 2026",
      type: "merits",
      outcome: "adverse",
      title: "Demurrer of Respondent Macomber (CDCR) Sustained Without Leave to Amend",
      holding: "CDCR has no duty under Pen. Code §3008 to conduct an individualized parole discharge assessment for Petitioner because Pen. Code §3000(b)(2)(B) mandates a 10-year parole term for Petitioner's offenses (§§220(a)(1), 289(a)(1)(A)). Reading §3000 and §3008 together, imposing §3008 procedures while §3000 mandates the 10-year term would produce an absurd result. Wrong vehicle — challenge to parole retention should be brought in habeas corpus, not mandate — but Court exercised discretion to treat petition as one for mandate; result the same. Demurrer sustained; Respondent to prepare formal order and judgment of dismissal.",
      significance: "Adverse on the merits as to the Earned Discharge Criteria (EDC) writ theory. Correct vehicle is habeas corpus — Matter 19 (pending Santa Clara Superior Court, habeas petition, Order Extending Time issued July 2, 2026) remains the live avenue for the same underlying claim. CRITICAL FOR MATTER 30: Court explicitly found 'it is not clear why CDCR undertook the early parole review process in the first place, and/or why CDCR refuses to provide any explanation for this course of conduct' regarding the 1502-DR — a Sacramento Superior Court judge, on the record, characterizing CDCR's 1502-DR conduct as inexplicable and unexplained. This judicial finding directly supports the fabrication/pretext narrative in Newanforbi v. Moua (Matter 30). Note: opinion dates the 1502-DR as 'on or about December 11, 2025' per FAP Exh. A; Matter 30 complaint uses November 14, 2025 as the authorship date — possible discrepancy between document date and issuance/transmittal date.",
      document_path: "/documents/opinions/Newanforbi v Macomber - Sacramento Sup Ct - Demurrer Sustained WOLA May 29 2026.pdf"
    },
    {
      matter: 1,
      caption: "Newanforbi v. State of California et al. (CHP / Meza-Gonzalez / Melano)",
      judge: "Magistrate Judge Chi Soo Kim (Findings & Recommendations — District Judge Dena Coggins to adopt/modify)",
      date: "April 20, 2026",
      type: "merits",
      outcome: "adverse",
      title: "Findings and Recommendations: Granting Defendants' Motion to Dismiss Without Leave to Amend",
      holding: "Motion to dismiss GRANTED. Plaintiff consented to dismiss State of California, Monell claims against CHP, and official-capacity claims against officers, leaving only individual-capacity 4th and 14th Amendment claims against Meza-Gonzalez and Melano. (1) 4th Amendment: Dismissed — totality of circumstances (officer observed cup, 'I think it's booze,' report notes odor of alcohol, red/watery eyes, slurred speech, field sobriety test failure) sufficient for probable cause; court credited Meza-Gonzalez's investigative report. (2) Qualified immunity: Applies alternatively — officers could have reasonably believed probable cause existed even if none. (3) 14th Amendment: Dismissed — no specific facts establishing constitutional due process violation. Leave to amend denied — futile; no non-frivolous claim presented. NOTE: This is a Magistrate's F&R, not a final order. 14-day objection period began April 20, 2026; District Judge adoption/modification/rejection pending.",
      significance: "Adverse F&R at pleading stage — court accepted Meza-Gonzalez's report at face value under Twombly/Iqbal (motion to dismiss standard), without considering the 62-minute dashcam recording that directly contradicts the report's fabricated observations (no officer verbalized alcohol odor on camera; cup was identified as urine; blood draw warrant contradicts 'chemical test refusal' designation). The dashcam evidence is not available at the 12(b)(6) stage. If the F&R is adopted and not reversed on objection, the parallel state court action (Matter 2, Alameda Superior Court — stayed pending this federal ruling per Apr. 14, 2026 stipulation) becomes the primary litigation vehicle. The F&R was cross-referenced in the June 15, 2026 Candelaria F&R (Case 2:26-cv-00983) as an example of plaintiff's complaints 'pending dismissal for failure to state a claim.' COUNTER-MOVE: Notice of Supplemental Authority filed July 7, 2026 (ECF No. 24 objections pending) citing Newanforbi v. Serrato (N.D. Cal. June 29, 2026), in which Magistrate Judge Krishnan found the same November 2024 CHP incident allegations sufficient under §1915 — directly undermining the F&R's frivolousness characterization and the qualified-immunity ruling. Pending de novo review by District Judge Dena Coggins.",
      document_path: "/documents/opinions/Newanforbi v California CHP - USDC EDCal - FR Recommending Dismissal Apr 20 2026.pdf",
      objections_path: "/documents/matter-32/from-01/Objections to FR - April 21 2026.pdf",
      nsa_path: "/documents/matter-32/from-01/Notice of Supplemental Authority - Serrato Order - July 7 2026.pdf"
    },
    {
      matter: 7,
      caption: "Newanforbi v. Candelaria et al. (DMV APS Hearing)",
      judge: "Magistrate Judge Chi Soo Kim (Findings & Recommendations — District Judge Dena Coggins to adopt/modify)",
      date: "June 15, 2026",
      type: "merits",
      outcome: "adverse",
      title: "Findings and Recommendations: IFP Denied; FAC Dismissed Without Leave to Amend",
      holding: "IFP application DENIED (action facially frivolous). FAC DISMISSED without leave to amend. (1) §1983 against Candelaria (individual): Quasi-judicial immunity bars claim — DMV APS hearing officer performing adjudicative functions is absolutely immune from §1983 damages. Two immunity-piercing arguments fail: (a) CVC §40300.5 authorized warrantless arrest without observed volitional movement, defeating Mercer argument; (b) 'disappearing arrest' under Pen. Code §849(b) is foreclosed by Armondo v. DMV (1993); conclusory allegations of dual-role/prosecutorial conduct are insufficient without specific facts. (2) Claims against Gordon (official capacity/DMV): Barred by Eleventh Amendment; Ex Parte Young exception fails — no standing for prospective relief because CDL suspension expired Feb. 19, 2026 and no likelihood of future APS hearing. Leave to amend denied — futile. NOTE: F&R only; 14-day objection period began June 15, 2026.",
      significance: "Adverse F&R on quasi-judicial immunity — the most significant structural obstacle in this matter. The court applied absolute immunity to Candelaria's adjudicative role without addressing: (1) the structural bias evidence (three appellate decisions condemning the dual-role framework issued months before the hearing); (2) Candelaria's specific failure to mention the CHP Detention Certificate — affirmative conduct evidence of prosecutorial, not judicial, role; (3) the blood-draw warrant contradicting the 'chemical test refusal' designation. The court's treatment of the Armondo 'disappearing arrest' argument also ignored the PC §849(b)(1) statutory text's mandatory reclassification language. Standing failure on the Gordon official-capacity claims is real — the suspension expired Feb. 19, 2026 — but leaves the structural due process argument live for any future hearing. The F&R cross-referenced Matter 1 F&R as evidence of plaintiff's other cases 'pending dismissal for failure to state a claim.' COUNTER-MOVE: Notice of Supplemental Authority electronically filed July 9, 2026 (Document 9; objections pending) citing Newanforbi v. Serrato (N.D. Cal. June 29, 2026) — directly attacking the cross-reference by showing a coordinate federal court found the same underlying factual record sufficient. The argument: 'The inference that Plaintiff's litigation pattern reflects frivolousness rather than legitimate pursuit of distinct legal theories is no longer sustainable.' Pending de novo review by District Judge Dena Coggins.",
      document_path: "/documents/matter-33/opinions/Newanforbi v Candelaria - USDC EDCal - FR Recommending Dismissal Jun 15 2026.pdf",
      objections_path: "/documents/matter-33/from-07/Objections to FR Newanforbi v Candelaria BOLSTERED 3.pdf",
      nsa_path: "/documents/matter-33/from-07/Notice of Supplemental Authority - Serrato Order - ELECTRONICALLY FILED Jul 9 2026.pdf"
    },
    {
      matter: 24,
      caption: "Newanforbi v. Serrato (U Visa Certification — CHP)",
      judge: "Magistrate Judge Ajay S. Krishnan",
      date: "June 29, 2026",
      type: "merits",
      outcome: "favorable",
      title: "Order re Motion to Proceed In Forma Pauperis: IFP Granted; Complaint Sufficient Under § 1915",
      holding: "IFP GRANTED. Complaint found SUFFICIENT under 28 U.S.C. §1915(e)(2) — case proceeds. Court accepts as plausible: (1) CHP officers falsely imprisoned Plaintiff in November 2024 based on fabricated evidence; (2) Defendant Serrato retaliated against Plaintiff by wrongfully denying his U Nonimmigrant Status (U visa) certification request despite Plaintiff's status as a victim of qualifying criminal activity (false imprisonment, unlawful criminal restraint, felonious assault, obstruction of justice). Court finds: 'Accepting Mr. Newanforbi's alleged facts as true, his complaint supports the plausible inferences that CHP officers falsely imprisoned him in November 2024 based on fabricated evidence. It also supports the plausible inference that, despite his status as a victim of the qualifying crime of false imprisonment, Defendant Serrato retaliated against him by wrongfully denying his certification request. While Defendant Serrato had discretion to certify the request, he did not have discretion to retaliate against Mr. Newanforbi.' Clerk directed to issue summons; U.S. Marshal directed to serve Defendant Serrato without prepayment of fees.",
      significance: "The only favorable §1915 screening ruling in the portfolio — and the most strategically significant. Magistrate Judge Krishnan (N.D. Cal.) applied the identical §1915 standard CSK applied in Matter 7 (June 15, 2026) and reached the opposite conclusion on the same November 2024 CHP incident allegations, 14 days later. Krishnan explicitly found those allegations plausibly state claims of false arrest based on fabricated evidence — the same core factual predicate at issue in Matter 1 (CHP, E.D. Cal.) and Matter 7 (Candelaria, E.D. Cal.). This ruling was cited as the basis for Notices of Supplemental Authority filed July 7, 2026, in both Matter 1 and Matter 7, now before District Judge Dena Coggins on de novo review. The argument: a coordinate court in the same circuit found the identical factual record sufficient under the identical screening standard 14 days after CSK called the Candelaria complaint 'facially frivolous.' The doctrinal split is now in the record and cannot be ignored on de novo review. Also note: Krishnan's finding that Serrato 'did not have discretion to retaliate' — the first federal judicial ruling expressly vindicating the 1st Amendment retaliation theory underlying Plaintiff's U visa denial claim.",
      document_path: "/documents/opinions/Newanforbi v Serrato - USDC NDCal - IFP Granted Complaint Sufficient Jun 29 2026.pdf"
    },
    {
      matter: 28,
      judge: "Magistrate Judge Lisa J. Cisneros",
      date: "July 23, 2026",
      type: "procedural",
      outcome: "adverse",
      title: "Order Addressing IFP Application, Denying Motion for Protective Order, and Requiring Filing of State Court Decision",
      holding: "IFP application not yet resolved — Plaintiff used a generic AO-published form rather than this district's specific form, and his answers (all 'No'/'N/A'/'None' except a $105.45 bank balance) lack sufficient context for the Court to assess credibility. Clerk directed to attach the district's own IFP form; Plaintiff ORDERED to complete and file it by August 13, 2026, with a separate statement explaining how he meets basic needs if it shows no income or expenses. Plaintiff also ORDERED to file a copy of the state court's demurrer decision by August 13, 2026, so the Court can assess potential claim/issue preclusion. Motion for Protective Order DENIED WITHOUT PREJUDICE: the Court found it not obvious that it has authority to alter the state court's requirement to return or destroy documents, and took judicial notice that the Eastern District action (Matter 3) had a motion to dismiss under submission but not yet resolved — meaning the state protective order's 'whichever is later' return-or-destroy clock had not yet started to run, so no urgency required denying without prejudice. Denial preserves Plaintiff's ability to seek relief from the state court directly, or to renew the request in this action once Defendants are served and appear.",
      significance: "CORRECTED (per full text of the underlying Stipulated Protective Order, Sec. VIII — see matter-05 document store): the return-or-destroy clock is not, in fact, close to triggering, and the July 24, 2026 Peterson ruling does not start it. Section VIII defines 'conclusion of an action' as thirty (30) days after the expiration of the time to appeal or challenge any FINAL JUDGMENT, settlement, or consent decree, and ties the 60-day return/destroy obligation to the conclusion of Matter 5 or the named related action Matter 3, whichever is LATER. Neither has reached that point: (1) Matter 5's own July 15, 2026 dismissal without leave to amend is appealable, but the CRC 8.104 appeal window (60 days from notice of entry, or 180 days if none was served) plus the PO's additional 30 days has not run — only 10 days had elapsed as of this writing; (2) the July 24, 2026 Peterson order in Matter 3 is an interlocutory ruling on a motion to dismiss that expressly grants leave to amend and keeps the action alive either way (amended pleading, or the case proceeding on the Equal Protection claim against Derrick) — it is not a final judgment, settlement, or consent decree, so it does not satisfy the PO's 'conclusion' trigger for Matter 3 either. Net effect: the document return/destroy clock remains dormant on both tracks; Cisneros's practical no-urgency conclusion was correct, for this more precise reason rather than narrowly because the MTD was 'under submission.' The live issue is different and still open: the PO's use-authorization carve-out (Secs. IV.A, VI) permits use of Matter 5's 'Confidential'-designated discovery ONLY in Matter 5 itself and the named Matter 3 action — it does not extend to Matter 28 (N.D. Cal.). Until the protective-order motion is renewed and granted there, Confidential-designated HOPE discovery (Clinical Operational Manual, Maintenance Curriculum, homework audit, collateral/contact notes, insurance policies) should not be filed or disclosed in Matter 28 without separate authorization; publicly available facts, including the state court's own published ruling, remain safe to use in the interim. CORROBORATED July 27, 2026: Plaintiff's own Notice of Payment of Filing Fee and Filing of State Court Decision (filed in Matter 28) states in writing that 'no final judgment of dismissal has been entered in the state action as of the date of this filing' — independently confirming, from the Matter 5 side, that the PO's finality-dependent clock has not started. The IFP deadline was mooted by the Jul. 24, 2026 fee payment, and the state-court-decision deadline was satisfied by that same Jul. 27, 2026 Notice, 17 days ahead of the August 13, 2026 due date — both items are now closed rather than open.",
      document_path: "/documents/opinions/Newanforbi v Smith - USDC NDCal - IFP PO Order Jul 23 2026.pdf"
    },
    {
      matter: 3,
      judge: "Magistrate Judge Jeremy D. Peterson",
      date: "July 24, 2026",
      type: "merits",
      outcome: "adverse",
      title: "Order Granting Palacios's Motion to Dismiss; Granting in Part Derrick/Noguchi's Motion; Dismissing FAC With Leave to Amend",
      holding: "Palacios's MTD (Doc 24) GRANTED — the Court walked through all four Ninth Circuit state-actor tests (public function, joint action, governmental nexus, compulsion) and found Plaintiff's allegations insufficient under each; Palacios is not a state actor and all claims against her are dismissed. The Court separately noted that a Rawson v. Recovery Innovations, Inc. quotation in Plaintiff's opposition 'does not appear in Rawson' and that the case does not stand for the cited proposition, reminding Plaintiff of his Rule 11(b)(2) certification obligations. Derrick and Noguchi's motion to quash/dismiss (Doc 9) GRANTED IN PART, DENIED IN PART: quash denied as moot (they waived service in their reply brief), but dismissal granted — the First Amendment retaliation claim fails for lack of plausible allegations tying specific protected speech to a specific adverse action by a specific defendant, and independently fails against Noguchi for lack of supervisory-liability allegations. The substantive due process claim is dismissed as duplicative of the First Amendment claim, per Plaintiff's own non-opposition. Also denied: Plaintiff's request for email case-activity notifications, his motion for evidence preservation/expedited discovery (no good-cause showing), and two motions for leave to file supplemental opposition. The FAC is DISMISSED WITH LEAVE TO AMEND within 14 days (by August 7, 2026); if no amended complaint is filed, the action proceeds solely on the Equal Protection claim against Derrick.",
      significance: "A substantial adverse ruling, though not necessarily final — leave to amend remains open through August 7, 2026. Notably, the order treats Derrick and Noguchi as active parties throughout and structures the case's future around Derrick remaining a defendant — in apparent tension with Plaintiff's July 22, 2026 Notice of Voluntary Dismissal, which purported to self-execute the dismissal of both Derrick and Noguchi under Fed. R. Civ. P. 41(a)(1)(A)(i) two days before this order issued. The order does not reference that filing. This ruling also has a direct downstream effect on Matter 28 (Newanforbi v. Smith/HOPE): the NDCA court's July 23, 2026 denial of the protective order motion there was expressly premised on this MTD still being 'under submission' — a premise this order overtakes.",
      document_path: "/documents/opinions/Newanforbi v Derrick - USDC EDCal - MTD Order Jul 24 2026.pdf"
    }
  ],
  notable_quotes: [
    {
      quote: "If, at the trial on the merits, the Court were to credit Plaintiff's allegations that neither he nor his vehicle smelled of alcohol, that he showed no signs of impairment in talking with the officers or in performing the physical field sobriety tests he agreed to perform, and that the arresting officers lied about it in their police report, it could reasonably find probable cause for arrest was lacking, which could support a finding that the CHP abused its discretion in refusing to certify Petitioners Form I-918.",
      speaker: "Hon. Jenna M. Whitman",
      role: "Judge of the Superior Court, Alameda Sup. Ct., Dept. 25",
      source: "ORDER Sustaining Demurrer In Part, with Leave to Amend, pp. 3–4",
      case_no: "26CV191136",
      date: "August 29, 2026",
      matter: 20,
      category: "vindication",
      note: "Entered demurrer order — Count 1 overruled. The dashcam-versus-report conflict is a fact question for trial, not a demurrer kill. Same November 1, 2024 incident Magistrate Judge Kim treated as probable cause as a matter of law in the Matter 1 F&R."
    },
    {
      quote: "Because Plaintiff has now effectively withdrawn his IFP application by paying the filing fee, however, the Court leaves any such argument for Defendants to raise if they see fit after they are served and appear. This Order should not be construed as implying any opinion by the Court as to whether such defenses might apply.",
      speaker: "Magistrate Judge Lisa J. Cisneros",
      role: "U.S. Magistrate Judge, USDC N.D. Cal.",
      source: "Order Regarding Payment of Filing Fee and Application to Proceed In Forma Pauperis (Dkt. 11), p. 1",
      case_no: "3:26-cv-07504-LJC",
      date: "August 26, 2026",
      matter: 28,
      category: "procedural",
      note: "Fee paid = no §1915 screening and no sua sponte preclusion ruling from the Matter 5 HOPE demurrer. Serve under Rule 4; HOPE can still plead preclusion after appearance."
    },
    {
      quote: "Plaintiff then made the 'strategic decision' to intentionally ignore half of Defendants' motion. Plaintiff regrets this decision, but the Court's local rules do not allow a non-moving party to bifurcate a moving party's motion, respond to the portion it prefers, and then request a second round of briefing on the remainder under the guise that it conserves judicial resources.",
      speaker: "Erick J. Rhoan, Deputy Attorney General",
      role: "California Attorney General's Office — counsel for Defendants Derrick & Noguchi",
      source: "Opposition to Plaintiff's Motion for Leave to File Supplemental Opposition, p.4",
      case_no: "2:26-cv-00004-DJC-JDP",
      date: "February 26, 2026",
      matter: 3,
      category: "dismissive",
      note: "Accuses Plaintiff of manipulating the briefing schedule under a false pretext, after Defendants' own reply first raised the waiver argument that Plaintiff's supplemental opposition sought to address."
    },
    {
      quote: "The Court finds the allegations in plaintiff's complaint so vague and conclusory that it is unable to determine whether the current action is frivolous or fails to state a claim for relief.",
      speaker: "Magistrate Judge Chi Soo Kim",
      role: "U.S. Magistrate Judge, USDC E.D. Cal.",
      source: "Screening Order, p.8:21-22",
      case_no: "2:26-cv-00191-DJC-CSK",
      date: "May 18, 2026",
      matter: 21,
      category: "sharp",
      note: "Issued in the same Barocio screening order in which the Court granted leave to amend — a materially different outcome than the Matter 1 and Matter 7 F&Rs, where CSK denied leave to amend outright."
    },
    {
      quote: "On May 22, 2026, at 9:31 am, Defendants served Plaintiff with the demurrer and related documents. At 4:16 pm that same day, Plaintiff served Defendants with his opposition to the demurrer, evidentiary objections, declaration, and opposition to request for judicial notice.",
      speaker: "Blaze Van Dine, Esq.",
      role: "Sims, Lawrence & Broghammer — counsel for HOPE Program & Katie Palacios",
      source: "Reply in Support of Demurrer to FAC, p.1 (§A, \"Generative AI\")",
      case_no: "STK-CV-UF-2026-0001032",
      date: "July 7, 2026",
      matter: 5,
      category: "backhanded",
      note: "Filed under a section literally titled 'Generative AI' — implicitly casting suspicion on a same-day, roughly 7-hour turnaround that included a full opposition, evidentiary objections, a declaration, and an RJN opposition. Read plainly, the timeline is a demonstration of competence, not an admission of anything improper."
    },
    {
      quote: "It appears from a search of Westlaw that Plaintiff filed two other lawsuits in federal court that have resulted in opinions available on Westlaw.",
      speaker: "Blaze Van Dine, Esq.",
      role: "Sims, Lawrence & Broghammer — counsel for HOPE Program & Katie Palacios",
      source: "Demurrer to First Amended Complaint",
      case_no: "STK-CV-UF-2026-0001032",
      date: "May 22, 2026",
      matter: 5,
      category: "backhanded",
      note: "Cited to portray Plaintiff as litigious — instead became a Westlaw-indexed accolade (2026 WL 1067541 · 2026 WL 1389969), preserved on the Notable Quotes tab.",
    },
    {
      quote: "The Court must extend the time in which to rule on Petitioner's habeas petition. Good cause for the extension is established by the need to thoroughly review the voluminous papers and the court's recent workload.",
      speaker: "Hon. Robert Hawk",
      role: "Judge of the Superior Court, Santa Clara Sup. Ct.",
      source: "Order Extending Time",
      case_no: "C2604791",
      date: "July 2, 2026",
      matter: 19,
      category: "procedural",
      note: "Framed as a scheduling matter, but the stated reason is the volume of Plaintiff's filed papers — a court, not opposing counsel, on the record describing the habeas petition as substantial enough to require additional time beyond the standard 60-day review period."
    },
    {
      quote: "Newanforbi has not administratively challenged CDCR's actions and he cannot pretend to know how CDCR would address a meritorious grievance.",
      speaker: "Kathleen R. Walton, Deputy Attorney General",
      role: "California Attorney General's Office — counsel for Respondent Jeffrey Macomber (CDCR)",
      source: "Reply to Opposition to Respondent's Demurrer, p.3",
      case_no: "26WM000028",
      date: "May 15, 2026",
      matter: 9,
      category: "dismissive",
      note: "Casts Plaintiff's exhaustion argument as presumptuous rather than substantive — yet the same court's May 29, 2026 order later found CDCR itself 'refuses to provide any explanation' for why it undertook the discharge review process in the first place."
    },
    {
      quote: "While Defendant Serrato had discretion to certify the request, he did not have discretion to retaliate against Mr. Newanforbi.",
      speaker: "Magistrate Judge Ajay S. Krishnan",
      role: "U.S. Magistrate Judge, USDC N.D. Cal.",
      source: "Order re Motion to Proceed In Forma Pauperis",
      case_no: "4:26-cv-05953-ASK",
      date: "June 29, 2026",
      matter: 24,
      category: "vindication",
      note: "The only favorable §1915 screening ruling in the portfolio — applying the identical standard CSK applied 14 days earlier in the Candelaria F&R, and reaching the opposite conclusion on the same core facts."
    },
    {
      quote: "Summons (filed/stamped) → stamped Complaint page 1 → plain pages 2–16 → signed pages 17–18 → Notice of Case Assignment and Notice of Hearing. The uploaded Summons checked out as complete and properly filed, so I used it as-is rather than the blank fallback template. The SER-001 is filled out and e-signed — directs the Los Angeles County Sheriff to serve FedEx's registered agent. The signature is your actual pen signature lifted from the Complaint's verification page, not a synthetic script font.",
      speaker: "Claude, AI Case Assistant",
      role: "Document assembly — this portfolio",
      source: "Chat summary, Matter 25 FedEx filing packet + SER-001 assembly",
      case_no: "STK-CV-UWT-2026-0009118",
      date: "July 21, 2026",
      matter: 25,
      category: "meta",
      note: "The one entry in this tab not extracted from an actual filing — added at the user's request as a nod to the AI doing the extracting. Earned, allegedly, by getting a malformed XFA field name to behave."
    },
    {
      quote: "However, this quotation does not appear in Rawson. What is more, Rawson does not stand for this proposition since it did not concern the operation of a re-entry program or even include the word \"parole.\"",
      speaker: "Magistrate Judge Jeremy D. Peterson",
      role: "U.S. Magistrate Judge, USDC E.D. Cal.",
      source: "Order Granting Palacios's Motion to Dismiss, p.6 n.5",
      case_no: "2:26-cv-00004-DJC-JDP",
      date: "July 24, 2026",
      matter: 3,
      category: "sharp",
      note: "On the misquoted Rawson v. Recovery Innovations, Inc. citation in Plaintiff's opposition — followed immediately by a reminder of the Rule 11(b)(2) certification obligation that legal contentions be 'warranted by existing law.'"
    },
    {
      quote: "It is not obvious that this Court has authority to alter the state court's requirement to return or destroy documents, even if this Court were to impose equivalent protections in its own protective order.",
      speaker: "Magistrate Judge Lisa J. Cisneros",
      role: "U.S. Magistrate Judge, USDC N.D. Cal.",
      source: "Order Addressing IFP Application, Denying Motion for Protective Order, and Requiring Filing of State Court Decision, p.2",
      case_no: "3:26-cv-07504-LJC",
      date: "July 23, 2026",
      matter: 28,
      category: "procedural",
      note: "The core holding denying the protective order without prejudice — premised on the Matter 3 MTD still being under submission, a premise Peterson's ruling overtook the very next day."
    }
  ],
};

export const outcomes = {
  ...outcomes_raw,
  realized: enrichOutcomes(outcomes_raw.realized),
  anticipated: enrichOutcomes(outcomes_raw.anticipated),
  active_demands: enrichOutcomes(outcomes_raw.active_demands),
  judicial_opinions: enrichOutcomes(outcomes_raw.judicial_opinions),
};
