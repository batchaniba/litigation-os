#!/usr/bin/env python3
"""Matter 28 -- Plaintiff's Rule 26(a)(1) Initial Disclosures on portfolio
pleading paper (pattern of internal/scripts/pleading-paper-formatter-script.py
and matter28-opposition-mtd-pleading.py). Two renders:
  REVIEW  -- keeps working-draft banner/notes, signature line left blank.
  SERVICE -- banner and internal notes removed, universal signature stamped.
"""
import sys
from pathlib import Path
REPO = Path("/workspace/ilp-repo")
S = REPO / "internal" / "scripts"
sys.path.insert(0, str(S / "lib")); sys.path.insert(0, str(S))
from pleading_paper import PleadingPaper, CONTENT_LEFT  # noqa
from signature_stamp import SIGNATURE_PATH, SIGNATURE_NATIVE_PX  # noqa

COURT1, COURT2 = "UNITED STATES DISTRICT COURT", "NORTHERN DISTRICT OF CALIFORNIA"
ATTY = [("BRENDAN NGEHSI NEWANFORBI", "Times-Bold", 12), ("Plaintiff, Pro Se", "Times-Roman", 12),
        ("1455 Cat Tail Drive", "Times-Roman", 12), ("Stockton, CA 95204", "Times-Roman", 12),
        ("Telephone: (209) 801-4442", "Times-Roman", 12), ("E-mail: bnn.cdl@gmail.com", "Times-Roman", 12)]
LEFT = [("BRENDAN NGEHSI NEWANFORBI,", True, False),
        ("", 0, 0),
        ("                          Plaintiff,", 0, 0), ("", 0, 0), ("       v.", 0, 0), ("", 0, 0),
        ("SHANNON SMITH, LCSW, Chief", True, False), ("Executive Officer and Founder of", True, False),
        ("HOPE Program, an individual; and", True, False), ("HOPE PSYCHOTHERAPY, INC.,", True, False),
        ("d/b/a HOPE PROGRAM, a California", True, False), ("corporation,", True, False), ("", 0, 0),
        ("                          Defendants.", 0, 0)]
RIGHT = [("Case No. 3:26-cv-07504-LJC", 0, 0), ("", 0, 0), ("PLAINTIFF'S INITIAL DISCLOSURES", True, False),
         ("PURSUANT TO FED. R. CIV. P. 26(a)(1)", True, False), ("", 0, 0),
         ("Judge: Hon. Lisa J. Cisneros", 0, 0), ("Initial CMC and MTD Hearing (Dkt. 29):", 0, 0), ("October 27, 2026, 10:30 a.m.", 0, 0), ("Courtroom G, 15th Floor", 0, 0)]

H, SH, P, L, NOTE = "H", "SH", "P", "L", "NOTE"
X = "the San Joaquin action"
def content(service):
    c = [
     (P, "Plaintiff Brendan Ngehsi Newanforbi, appearing pro se, makes the following initial disclosures based on the information reasonably available to him. See Fed. R. Civ. P. 26(a)(1)(E). The parties held their Rule 26(f) conference on September 29, 2026, and each side stated in the Joint Case Management Statement that it will serve initial disclosures no later than October 15, 2026. (Dkt. No. 28.)"),
     (NOTE, "WORKING DRAFT -- REVIEW COPY. SECTION III COMPUTATION APPROVED OCTOBER 14, 2026; SIGN BEFORE SERVICE."),
     (H, "I. INDIVIDUALS LIKELY TO HAVE DISCOVERABLE INFORMATION"), (SH, "Fed. R. Civ. P. 26(a)(1)(A)(i)"),
     (P, "Plaintiff may use the following individuals to support his claims. A work address is provided where it is known from the record. Individual home addresses and telephone numbers are unknown unless stated."),
     (L, "1. Brendan Ngehsi Newanforbi (Plaintiff) -- 1455 Cat Tail Drive, Stockton, CA 95204; telephone (209) 801-4442; e-mail bnn.cdl@gmail.com. Subjects: his enrollment, treatment, communications, employment history, claimed injuries, and all events pleaded in the operative complaint."),
     (L, "2. Shannon Smith, LCSW -- Chief Executive Officer and Founder of HOPE; individual defendant; c/o HOPE, 1245 B Street, Hayward, CA 94541. Subjects: HOPE policies, practices, manuals, billing and reporting systems, policymaking authority, notice, and her personal role in the events at issue."),
     (L, "3. HOPE Psychotherapy, Inc. d/b/a HOPE Program (appearing as HOPE Program, A Licensed Clinical Social Worker Professional Corporation, sued and served as HOPE Psychotherapy, Inc.) -- entity defendant, 1245 B Street, Hayward, CA 94541, through its officers, managing agents, and one or more Rule 30(b)(6) witnesses. Subjects: corporate policies, clinical operations, reports to CDCR, record systems, revenue and billing, and the Bates production HOPE_000001-HOPE_000542."),
     (L, "4. Katie Palacios -- former Clinical Director or Site Director identified in the record; c/o HOPE; address and telephone otherwise unknown. Subjects: clinical operations, containment-team meetings, treatment-completion recommendations, statements to Plaintiff and parole personnel, and reports concerning Plaintiff."),
     (L, "5. Pamela Akins (pakins@hopeprogram.biz) -- HOPE staff member and contact identified in clinical notes. Subjects: Plaintiff's treatment records, homework, and clinical communications."),
     (L, "6. Carla Marie Boatner (cboatner@hopeprogram.biz) -- HOPE staff member identified in clinical notes. Subjects: Plaintiff's treatment records, homework, and clinical communications."),
     (L, "7. Johana Felix -- HOPE staff member identified in clinical notes. Subjects: the same subjects as Nos. 5-6."),
     (L, "8. Vichra You -- HOPE staff member identified in clinical notes. Subjects: the same subjects as Nos. 5-6."),
     (L, "9. Janelle Harper (jharper@hopeprogram.biz) -- HOPE note author. Subjects: authorship, content, and transmission of notes concerning Plaintiff."),
     (L, "10. Joy Hubbard (jhubbard@hopeprogram.biz) -- HOPE note author. Subjects: the same subjects as No. 9."),
     (L, "11. Marina Serrano (mserrano@almaxconsulting.com) -- note author or system user identified in the produced records. Subjects: authorship, content, data entry, and record-system custody concerning Plaintiff."),
     (L, "12. HOPE note authors identified in the produced records by the account handles jaldana, kkaur, kphaysaleum, thuynh, and adittmer -- full names, current addresses, and telephone numbers presently unknown. Subjects: authorship and content of their notes concerning Plaintiff. Plaintiff will supplement with full identifying information if learned."),
     (L, "13. Mark Delucchi -- HOPE manager identified in a January 6, 2026 escalation note or communication. Subjects: receipt of notice concerning Plaintiff's litigation and subsequent policy, reporting, and corrective decisions."),
     (L, "14. Dr. Carrie Shinske -- HOPE manager or clinical leader identified in discovery responses and a January 6, 2026 escalation. Subjects: HOPE policy, discovery verification, notice, reporting, and corrective decisions."),
     (L, "15. Dr. Cristina Loree -- HOPE clinical-training leader identified in the <<i:Dwyer>> record. Subjects: HOPE's treatment phases, completion and aftercare structure, training, and institutional knowledge."),
     (L, "16. Long Moua (also identified as L. Moua) -- CDCR parole agent; current work address and telephone unknown to Plaintiff. Subjects: communications with HOPE, the March 31, 2026 no-show instruction, Form 3043 or treatment-status material, and the November 14, 2025 CDCR Form 1502-DR."),
     (L, "17. Gary Noguchi -- CDCR supervising agent; current work address and telephone unknown to Plaintiff. Subjects: supervision decisions, treatment reports received from HOPE, and the November 19, 2025 supervisory portion of the Form 1502-DR."),
     (L, "18. Parole agents Magana, Arestad, Acierto, and Urrea -- current work addresses and telephone numbers unknown to Plaintiff. Subjects: receipt of and reliance on HOPE treatment-status reports, participation in containment-team meetings, supervision decisions, and communications with Plaintiff and HOPE."),
     (L, "19. Yvonne Richmond -- The Counseling and Psychotherapy Center Inc., a CASOMB-certified sex offender treatment program; address and telephone presently unknown to Plaintiff. Subjects: sex offender treatment program participation, CASOMB-certified treatment, and Plaintiff's treatment history and compliance relevant to his claims."),
     (L, "20. Scheherazade Glover-Coleman, Ph.D. -- The Counseling and Psychotherapy Center Inc., a CASOMB-certified sex offender treatment program; address and telephone presently unknown to Plaintiff. Subjects: the same subjects as No. 19."),
     (L, "21. Nicole Beasley, Ph.D. -- former employee of HOPE Psychotherapy, Inc.; current address and telephone presently unknown to Plaintiff. Subjects: HOPE's policies, practices, and operations during her employment."),
     (H, "II. DOCUMENTS, ELECTRONICALLY STORED INFORMATION, AND TANGIBLE THINGS"), (SH, "Fed. R. Civ. P. 26(a)(1)(A)(ii)"),
     (P, f"Plaintiff may use the following categories to support his claims. The descriptions identify the categories and locations presently known. Production of material covered by the protective order entered in {X} remains subject to that order and to any protective order entered in this action."),
     (L, f"1. The HOPE Bates production, HOPE_000001-HOPE_000542, produced in {X} and stamped CONFIDENTIAL: professional-liability policy (HOPE_000001-031); D&O/EPL policy (000032-104); Block 1 homework (000105-138); collateral notes and communications (000139-199); homework and preparatory tickets (000200-223); curriculum tracking audit (000224); Clinical Operational Manual (000225-349); Maintenance Curriculum (000350-434); Employee Handbook (000435-485); Proprietary Treatment Manual (000486-537); and Clinical Director Job Description (000538-542)."),
     (L, f"2. Written discovery in {X}, including HOPE's and Palacios's responses to requests for admission, special interrogatories, form interrogatories, and requests for production, together with verifications and any amendments."),
     (L, "3. Plaintiff's HOPE records in his possession, including enrollment and intake material, assigned homework, communications with HOPE personnel, treatment-plan and phase records, attendance and scheduling communications, containment-team meeting material, and discharge or completion communications, if any."),
     (L, "4. CDCR and parole records in Plaintiff's possession, including the November 14/19, 2025 CDCR Form 1502-DR Discharge Review Report and communications involving HOPE treatment status. No completed Form 3043 is presently identified in Plaintiff's possession; Plaintiff describes that category as located in Defendants' and CDCR's possession and will supplement if copies are obtained."),
     (L, "5. Employment and earnings records, including federal Form W-2 statements for 2022-2024, offer letters, pay records, schedules, resignation or separation communications, and records concerning United Road, Keurig Dr Pepper, Tiger Lines LLC, US-1 Shorthaul, Lazer Spot, Inc., Centerline Drivers, and FedEx. These records may bear on actual earnings, mitigation, scheduling conflicts, and claimed wage loss."),
     (L, "6. The state-court file in <<i:Newanforbi v. Palacios, et al.>>, San Joaquin County Superior Court No. STK-CV-UF-2026-0001032 (the \"San Joaquin action\"), including the complaint, discovery, demurrer papers, July 2026 tentative ruling and minute order, July 15, 2026 order sustaining the demurrer without leave to amend, and any later judgment or notice of entry."),
     (L, "7. The docket and served filings in this action, including the operative complaint, orders (including the Order Continuing Case Management Conference, Dkt. 29), proof of service, Defendants' motion to dismiss and attachments (Dkt. Nos. 15, 15-1, 15-2), Plaintiff's opposition, and communications concerning service and the claims."),
     (L, "8. The <<i:In re Dwyer>> court record and regulatory materials concerning sex-offender treatment duration, completion, aftercare, and Cal. Code Regs., tit. 15, section 3574, to the extent admissible or judicially noticeable."),
     (L, "9. Other nonprivileged records responsive to these categories that are located, received in discovery, or created as damages continue to accrue. Plaintiff will supplement under Rule 26(e)."),
     (P, f"Handling of the protected Bates set. The set is described here. Plaintiff will not reproduce or use material in violation of the protective order entered in {X}. Consistent with the parties' statements in the Joint Case Management Statement (Dkt. No. 28), Plaintiff will meet and confer regarding a stipulated protective order and will produce the set promptly after entry of an order or written agreement authorizing its use and production in this action."),
     (H, "III. COMPUTATION OF DAMAGES"), (SH, "Fed. R. Civ. P. 26(a)(1)(A)(iii)"),
     (P, "Plaintiff's present computation is preliminary and is made on the information reasonably available to him. Defendants and third parties control additional inputs, including HOPE attendance and scheduling records and carrier dispatch and payroll records. Plaintiff is compiling his 2025 earnings and his 2026 earnings before his current employment and will supplement or correct this computation under Rule 26(e) when that compilation is complete."),
     (P, "<<b:Factual basis.>> Commercial driving, particularly long-haul and regional routes, requires the ability to travel without geographic restrictions and to work flexible schedules free from mandatory treatment attendance. In or about January 2022, after Plaintiff missed a HOPE group session in connection with a long-haul assignment for United Road, his parole agent threatened to violate his parole for missing the session, and Plaintiff was forced to resign that position. Thereafter Plaintiff was required to decline dispatches that fell on HOPE group-session days. Plaintiff attributes this loss to HOPE's non-completion characterizations and the resulting supervision conditions, including mandatory HOPE attendance. (See Dkt. No. 15-1 at ECF pp. 12-13 (First Amended Complaint, San Joaquin action, paras. G.1-G.2).)"),
     (P, "<<b:But-for rate.>> Plaintiff's but-for weekly pay as a Class A CDL driver is computed from the Centerline Drivers wage notice dated October 31, 2024 ($33.35 per hour regular; $50.03 per hour premium), at 60 hours per week worked as five 12-hour days: 40 regular hours x $33.35 = $1,334.00, plus 20 overtime hours (4 per day beyond 8) x $50.03 = $1,000.60, for $2,334.60 per week ($121,399.20 per year at 52 weeks)."),
     (P, "<<b:1. Accrued lost wages.>> $2,334.60 per week from January 1, 2022 through October 14, 2026, excluding February 20, 2025 through February 19, 2026, the period of Plaintiff's CDL suspension, less interim earnings. By year:"),
     (L, "a. 2022 (365 days): but-for $121,732.71, less W-2 earnings of $39,553.00 = $82,179.71."),
     (L, "b. 2023 (365 days): but-for $121,732.71, less W-2 earnings of $11,145.00 = $110,587.71."),
     (L, "c. 2024 (366 days): but-for $122,066.23, less W-2 earnings of $55,894.00 = $66,172.23."),
     (L, "d. 2025 (January 1-February 19; 50 days): but-for $16,675.71, less interim earnings (being compiled; none presently deducted) = $16,675.71."),
     (L, "e. 2026 (February 20-October 14; 237 days): but-for $79,042.89, less known interim earnings from Plaintiff's current employment of $2,102.86 ($23.00 per hour x 40 hours per week from September 28 through October 14, 2026) = $76,940.03."),
     (L, "f. Total: but-for $461,250.25, less known interim earnings of $108,694.86 (including 2022-2024 W-2 earnings totaling $106,592.00) = $352,555.39 in accrued net wage loss. The amount continues to accrue at $2,334.60 per week gross ($1,414.60 per week net of current earnings), subject to proof, mitigation, and the appropriate legal cutoff."),
     (P, "<<b:2. Front pay.>> Using a provisional two-year period, 104 weeks x ($2,334.60 - $920.00 current weekly earnings) = $147,118.40 (gross before mitigation: $242,798.40). Plaintiff will supplement this period and calculation as the case schedule, discovery, and mitigation record develop."),
     (P, "<<b:3. Lost employment benefits.>> The value of carrier-provided benefits Plaintiff would have received during the compensable period, less corresponding benefits obtained through mitigation. Plan terms and contribution data are controlled by third parties and will be incorporated when obtained."),
     (P, "<<b:4. Statutory remedies.>> (a) Bane Act, Civil Code sections 52 and 52.1: actual damages and any additional amount permitted by law, not less than the $4,000 statutory minimum, plus attorney's fees where recoverable; Plaintiff does not multiply the $4,000 minimum by an unverified number of violations. (b) Civil RICO, 18 U.S.C. section 1964(c): three times the business-or-property injury proven. Applied to the net economic loss above ($352,555.39 + $147,118.40 = $499,673.79), trebled damages would be $1,499,021.37. This figure is an alternative measure, not an additive amount, and is not included in the total below. (c) 42 U.S.C. section 1983: compensatory damages as computed here, or $1 in nominal damages if a violation is proven without compensable injury."),
     (P, "<<b:5. Emotional-distress and other noneconomic damages.>> Plaintiff presently estimates $100,000, subject to supplementation based on discovery and the nature, duration, and effects of the anxiety, depression, mental anguish, and reputational harm established through testimony and other admissible evidence. These damages are not susceptible to a precise mathematical calculation."),
     (P, "<<b:6. Punitive damages.>> Against Defendant Smith individually, an amount sufficient to punish and deter, to be determined by the trier of fact based on evidence of malice, oppression, or reckless disregard and Defendants' financial condition. Plaintiff will provide a more specific computation if and when the necessary financial evidence is obtained."),
     (P, "<<b:7. Costs, interest, and equitable relief.>> Recoverable costs, pre- and post-judgment interest, declaratory and injunctive relief, and any other relief authorized by the operative pleading and governing law, in amounts to be updated as incurred or determined."),
     (P, "<<b:Presently quantifiable total.>> The presently quantifiable damages are approximately $599,673.79 after known mitigation, consisting of $352,555.39 in accrued net wage loss, $147,118.40 in provisional net front pay, and $100,000 in noneconomic damages. Accrued wage loss continues as stated above. RICO trebling, Bane Act enhancements, benefits, punitive damages, costs, interest, and equitable relief are not included and remain additional or subject to later computation."),
     (P, "<<b:Non-duplication.>> Plaintiff seeks these amounts once. To the extent any portion of this wage loss is recovered from any other defendant or in any other action, including claims arising from the 2025-2026 CDL suspension or against CDCR personnel, Plaintiff will credit that recovery and does not seek duplicative compensation. The period February 20, 2025 through February 19, 2026 is excluded from this computation."),
     (P, "<<b:Documents supporting the computation:>> the Centerline Drivers wage notice dated October 31, 2024; Plaintiff's federal W-2 statements for 2022-2024 and 2025 earnings records; pay records from Plaintiff's current employment; dispatch logs and records of declined assignments; DMV records reflecting CDL issuance, suspension, and reinstatement; HOPE collateral notes and communications (HOPE_000139-199); HOPE's Clinical Operational Manual (HOPE_000225-349); Dkt. No. 15-1; and the Joint Case Management Statement (Dkt. No. 28)."),
     (H, "IV. INSURANCE AGREEMENTS"), (SH, "Fed. R. Civ. P. 26(a)(1)(A)(iv)"),
     (P, f"Plaintiff has no insurance agreement under which an insurance business may be liable to satisfy all or part of a judgment entered against Plaintiff in this action. Plaintiff possesses Bates-stamped copies of HOPE's professional-liability and D&O/EPL policies, described in Section II and subject to the protective order entered in {X}. Defendants retain their independent Rule 26(a)(1)(A)(iv) duty to produce any insurance or indemnity agreement applicable to the claims in this action."),
     (H, "V. RESERVATION AND SUPPLEMENTATION"),
     (P, "Plaintiff will supplement or correct these disclosures in a timely manner under Federal Rule of Civil Procedure 26(e), including when full witness contact information, Form 3043 records, a supported damages computation, or additional responsive records become available."),
    ]
    return [x for x in c if not (service and x[0] == NOTE)]

def sign(d, service, name_lines):
    sig = "__________________________________"
    if service:
        w, h = SIGNATURE_NATIVE_PX
        d.draw_signature_image(SIGNATURE_PATH, w, h, sig, width=210, right_margin_offset=28)
    else:
        d.blank_line(); d.blank_line()
    d.write_line(sig, right=True, right_margin_offset=28)
    for ln in name_lines:
        d.write_line(ln, right=True, right_margin_offset=28)

def render(out, service):
    foot = "PLAINTIFF'S INITIAL DISCLOSURES -- NEWANFORBI v. SMITH, No. 3:26-cv-07504-LJC (N.D. Cal.)" + ("" if service else " -- WORKING DRAFT")
    d = PleadingPaper(str(out), doc_title_footer=foot)
    y = d._line_y(0)
    for i, (t, f, s) in enumerate(ATTY):
        d.c.setFont(f, s); d.c.drawString(CONTENT_LEFT, y - i * 15, t)
    d.current_line = 4; d.blank_line()
    d.write_line(COURT1, bold=True, center=True); d.write_line(COURT2, bold=True, center=True); d.blank_line()
    d.draw_caption_block(LEFT, RIGHT, caption_size=10, tight_lh=13, boxed=True); d.blank_line()
    for k, t in content(service):
        if k == H: d.ensure_space(5); d.write_wrapped(f"<<b:{t}>>", first_indent=0)
        elif k == SH: d.write_line(t, italic=True); d.blank_line(); continue
        elif k == P: d.write_wrapped(t, first_indent=36)
        elif k == L: d.write_wrapped(t, indent=36, first_indent=0)
        elif k == NOTE: d.write_wrapped(f"<<b:{t}>>", first_indent=0)
        d.blank_line()
    d.ensure_space(10)
    d.write_line("Dated: October 14, 2026"); d.blank_line()
    d.write_respectfully_submitted(right_margin_offset=28)
    sign(d, service, ["Brendan Ngehsi Newanforbi, Plaintiff Pro Se"])
    d.save()
    # Proof of service: repo's designated federal POS (internal/scripts/lib/proof_of_service.py),
    # appended as the last page(s), as in matter25-discovery-set-one.py.
    from proof_of_service import DISTRICT_NDCAL, ProofOfServiceFields, build_proof_of_service
    from pypdf import PdfReader, PdfWriter
    pos = Path("/tmp") / ("pos-" + ("service" if service else "review") + ".pdf")
    build_proof_of_service(pos, ProofOfServiceFields(
        plaintiff_line="BRENDAN NGEHSI NEWANFORBI", plaintiff_role="Plaintiff",
        defendant_lines=["SHANNON SMITH, LCSW;", "HOPE PSYCHOTHERAPY, INC."], defendant_role="Defendants",
        case_number="3:26-cv-07504-LJC", title="PROOF OF SERVICE", service_date="October 14, 2026",
        document_title="PLAINTIFF'S INITIAL DISCLOSURES PURSUANT TO FED. R. CIV. P. 26(a)(1)",
        recipients=[
            "Cynthia G. Lawrence, Esq. \u2014 cynthia@sims-law.net",
            "Blaze Van Dine, Esq. \u2014 blaze@sims-law.net",
            "Eric T. Martinez, Esq. \u2014 emartinez@sims-law.net",
            "Kim Schmitt (Legal Secretary) \u2014 kschmitt@sims-law.net",
            "June Meinecke \u2014 june@sims-law.net",
            "Amber Krausse \u2014 Amber@sims-law.net",
            "Sims, Lawrence & Broghammer (e-service) \u2014 slb-eservice@sims-law.net",
            "",
            "Attorneys for Defendants Shannon Smith, LCSW, and",
            "HOPE Psychotherapy, Inc. (d/b/a HOPE Program)",
            "",
            "Service by electronic means under Fed. R. Civ. P. 5(b)(2)(E), made pursuant to",
            "the written consent of counsel for Defendants.",
        ],
        server_name="Brendan Ngehsi Newanforbi", stamp_signature=service,
        district_line=DISTRICT_NDCAL, by_email=True))
    w = PdfWriter()
    for f in (out, pos):
        for pg in PdfReader(str(f)).pages: w.add_page(pg)
    with open(out, "wb") as fh: w.write(fh)
    print("wrote", out, len(PdfReader(str(out)).pages), "pages")

if __name__ == "__main__":
    o = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/workspace/out")
    render(o / "Plaintiff's Initial Disclosures - Nforbi v Smith 3-26-cv-07504-LJC (SERVICE, signed).pdf", True)
    render(o / "Plaintiff's Initial Disclosures - Nforbi v Smith 3-26-cv-07504-LJC (REVIEW DRAFT, unsigned).pdf", False)
