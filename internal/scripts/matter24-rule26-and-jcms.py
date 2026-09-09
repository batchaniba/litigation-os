#!/usr/bin/env python3
"""Matter 24 — Rule 26(a)(1) disclosures and Plaintiff's JCMS portion.

Li's Sep. 7 fallback: if Dkt. 22 is still unsigned at 2:00 p.m. Pacific
September 8, Plaintiff sends his JCMS portion so the AG can incorporate
the defense portion and file a joint statement by end of day. Plaintiff
also serves Rule 26(a)(1) disclosures. Disclosures are served, not filed.

  python3 internal/scripts/matter24-rule26-and-jcms.py

HOLD: if PACER shows a signed order on Dkt. 22, do not send.
"""
from __future__ import annotations

import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR / "lib"))
sys.path.insert(0, str(SCRIPT_DIR))

from pleading_paper import CONTENT_LEFT, PleadingPaper  # noqa: E402
from proof_of_service import (  # noqa: E402
    DISTRICT_NDCAL,
    ProofOfServiceFields,
    build_proof_of_service,
)
from signature_stamp import SIGNATURE_NATIVE_PX, SIGNATURE_PATH  # noqa: E402

ROOT = SCRIPT_DIR.parent
MATTER24 = ROOT / "public/documents/matter-24"

EXEC_DATE = "September 8, 2026"
CMC_DATE = "September 15, 2026"
MTD_DATE = "September 30, 2026"

OUT_DISCLOSURES = MATTER24 / (
    "Plaintiff's Rule 26(a)(1) Initial Disclosures (Sep 8 2026).pdf"
)
OUT_JCMS = MATTER24 / (
    "Plaintiff's Portion of Joint Case Management Statement (Sep 8 2026).pdf"
)
OUT_POS = MATTER24 / (
    "Proof of Service by Email - Rule 26 Initial Disclosures and JCMS Portion "
    "(Sep 8 2026).pdf"
)

ATTY = [
    ("BRENDAN NGEHSI NEWANFORBI", "Times-Bold", 12),
    ("Plaintiff, In Pro Per", "Times-Roman", 12),
    ("1455 Cat Tail Drive", "Times-Roman", 12),
    ("Stockton, CA 95204", "Times-Roman", 12),
    ("Telephone: (209) 801-4442", "Times-Roman", 12),
    ("E-mail: bnn.cdl@gmail.com", "Times-Roman", 12),
]

CAPTION_LEFT = [
    ("BRENDAN NGEHSI NEWANFORBI,", True, False),
    ("", False, False),
    ("                          Plaintiff,", False, False),
    ("", False, False),
    ("       v.", False, False),
    ("", False, False),
    ("CAPTAIN G. SERRATO, in his", True, False),
    ("individual and official capacities", True, False),
    ("as Commander, Dublin Area,", True, False),
    ("California Highway Patrol,", True, False),
    ("", False, False),
    ("                          Defendant.", False, False),
]

SIG_LINE = "___________________________________"


def _header(d: PleadingPaper) -> None:
    c = d.c
    atty_y = d._line_y(0)
    for i, (txt, fn, sz) in enumerate(ATTY):
        c.setFont(fn, sz)
        c.drawString(CONTENT_LEFT, atty_y - i * 14, txt)
    d.current_line = 4
    d.blank_line()
    d.write_line("UNITED STATES DISTRICT COURT", bold=True, center=True)
    d.write_line("NORTHERN DISTRICT OF CALIFORNIA", bold=True, center=True)
    d.blank_line()


def _sign_block(d: PleadingPaper) -> None:
    d.ensure_space(8)
    d.write_line(f"Dated: {EXEC_DATE}")
    d.blank_line()
    d.write_line("Respectfully submitted,", right=True, right_margin_offset=20)
    d.blank_line()
    d.draw_signature_image(
        SIGNATURE_PATH,
        SIGNATURE_NATIVE_PX[0],
        SIGNATURE_NATIVE_PX[1],
        SIG_LINE,
        width=220,
        x_offset=15,
    )
    d.write_line(SIG_LINE, right=True, right_margin_offset=20)
    d.write_line("BRENDAN NGEHSI NEWANFORBI", right=True, right_margin_offset=20)
    d.write_line("Plaintiff, In Pro Per", right=True, right_margin_offset=20)


def _heading(d: PleadingPaper, text: str) -> None:
    d.ensure_space(3)
    d.write_line(text, bold=True)


def _para(d: PleadingPaper, text: str, first_indent: int = 36) -> None:
    d.write_wrapped(text, first_indent=first_indent)


def build_disclosures(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    d = PleadingPaper(
        str(path),
        doc_title_footer=(
            "PLAINTIFF'S RULE 26(a)(1) INITIAL DISCLOSURES -- "
            "NEWANFORBI v. SERRATO"
        ),
    )
    _header(d)
    right = [
        ("Case No. 4:26-cv-05953-ASK", False, False),
        ("", False, False),
        ("PLAINTIFF'S INITIAL", True, False),
        ("DISCLOSURES", True, False),
        ("(Fed. R. Civ. P. 26(a)(1))", False, False),
        ("", False, False),
        (f"CMC: {CMC_DATE}", False, False),
        ("Time: 1:30 p.m. via Zoom", False, False),
        ("Judge: Hon. Ajay S. Krishnan", False, False),
    ]
    d.draw_caption_block(CAPTION_LEFT, right, caption_size=10, tight_lh=13, boxed=True)
    d.blank_line()
    d.write_line("PLAINTIFF'S INITIAL DISCLOSURES", bold=True, center=True)
    d.write_line("(Fed. R. Civ. P. 26(a)(1))", center=True)
    d.blank_line()
    _para(
        d,
        "TO DEFENDANT AND HIS ATTORNEY OF RECORD:",
        first_indent=0,
    )
    d.blank_line()
    _para(
        d,
        "Plaintiff Brendan Ngehsi Newanforbi, appearing in propria persona, "
        "serves these Initial Disclosures under Federal Rule of Civil Procedure "
        f"26(a)(1). They are dated {EXEC_DATE}, the date set by the Court's "
        "June 17, 2026 Order Setting Initial Case Management Conference and ADR "
        "Deadlines (Dkt. 4). They are served on counsel; they are not filed with "
        "the Clerk except as the Court may later order. Plaintiff reserves the "
        "right to supplement under Rule 26(e).",
    )
    d.blank_line()
    _para(
        d,
        "The parties stipulated on September 3, 2026 to continue the initial "
        "case management conference until after a ruling on Defendant's pending "
        "motion to dismiss and to vacate this disclosure deadline (Dkt. 22). No "
        "signed order appears on PACER as of the date of these disclosures. "
        "Plaintiff therefore makes them now. If the Court later enters the "
        "Dkt. 22 proposed order, Plaintiff will treat this service as having "
        "been made without prejudice to the reset schedule.",
    )

    _heading(d, "A.  Individuals Likely to Have Discoverable Information")
    _para(
        d,
        "Fed. R. Civ. P. 26(a)(1)(A)(i). Addresses and telephone numbers are "
        "given as known. CHP personnel may be contacted through counsel of "
        "record for Defendant unless they agree otherwise.",
        first_indent=0,
    )
    d.blank_line()
    _para(
        d,
        "<<b:1. Brendan Ngehsi Newanforbi (Plaintiff).>> 1455 Cat Tail Drive, "
        "Stockton, CA 95204; telephone (209) 801-4442; e-mail "
        "bnn.cdl@gmail.com. Subjects: the November 1, 2024 stop and arrest; "
        "the Penal Code section 851.6 detention certificate; Plaintiff's "
        "complaints to CHP and POST; the April 9, 2026 U-visa certification "
        "request; receipt of Lieutenant Paul's April 10, 2026 e-mail; receipt "
        "of Captain Serrato's April 20, 2026 denial; protected petitioning; "
        "and the injuries alleged in the First Amended Complaint.",
        first_indent=0,
    )
    d.blank_line()
    _para(
        d,
        "<<b:2. Captain G. Serrato,>> Commander, CHP Dublin Area, in his "
        "individual and official capacities. CHP Dublin Area, 4999 Gleason "
        "Drive, Dublin, CA 94568; c/o Haiyang A. Li, Deputy Attorney General, "
        "300 South Spring Street, Suite 1702, Los Angeles, CA 90013-1230; "
        "telephone (213) 269-6404; e-mail Haiyang.Li@doj.ca.gov. Subjects: "
        "the March 26, 2026 complaint-assignment letter; the April 20, 2026 "
        "denial; review of the April 9 packet; application of Penal Code "
        "section 679.10 and Attorney General Bulletin DLE-2024-05; knowledge "
        "of Plaintiff's complaints and related litigation; and any internal "
        "review or investigation of the November 1, 2024 incident.",
        first_indent=0,
    )
    d.blank_line()
    _para(
        d,
        "<<b:3. Lieutenant Gary Paul,>> CHP Dublin Area, 4999 Gleason Drive, "
        "Dublin, CA 94568; telephone unknown; c/o counsel for Defendant. "
        "Subjects: the April 10, 2026 e-mail confirming receipt of the "
        "certification request (\"Your email has been received and your "
        "request is under review\") and routing of that request.",
        first_indent=0,
    )
    d.blank_line()
    _para(
        d,
        "<<b:4. Sergeant Eric Dutra,>> CHP Dublin Area, 4999 Gleason Drive, "
        "Dublin, CA 94568; telephone unknown; c/o counsel for Defendant. "
        "Subjects: the investigation assigned by Captain Serrato's March 26, "
        "2026 letter, and any findings bearing on the certification request "
        "or the November 1, 2024 incident.",
        first_indent=0,
    )
    d.blank_line()
    _para(
        d,
        "<<b:5. Officer Santiago Meza-Gonzalez, CHP #023295.>> California "
        "Highway Patrol, Modesto Area, 4030 Kiernan Avenue, Modesto, CA 95356; "
        "telephone unknown. Subjects: the November 1, 2024 stop, arrest, and "
        "Arrest-Investigation Report (CHP Case No. RJ68845), which were the "
        "subject of Plaintiff's certification request. He is a defendant in "
        "the related action <<i:Nforbi v. Meza-Gonzalez et al.>>, No. "
        "4:26-cv-08271-ASK.",
        first_indent=0,
    )
    d.blank_line()
    _para(
        d,
        "<<b:6. Officer Jose Melano, CHP #023054.>> California Highway Patrol, "
        "South Sacramento Area, 6 Massie Court, Sacramento, CA 95823; "
        "telephone unknown. Subjects: the same November 1, 2024 stop, arrest, "
        "and report. He is a defendant in No. 4:26-cv-08271-ASK.",
        first_indent=0,
    )
    d.blank_line()
    _para(
        d,
        "<<b:7. Custodian of Records, CHP Dublin Area,>> 4999 Gleason Drive, "
        "Dublin, CA 94568; and <<b:Custodian of Records, California Highway "
        "Patrol>> (dashcam, CAD, and arrest-report systems statewide). "
        "Subjects: the original dashcam recording of the November 1, 2024 "
        "I-580 East Livermore encounter (approximately 00:54:36 to 01:57:10); "
        "Arrest-Investigation Report RJ68845; the November 5, 2024 Penal Code "
        "section 851.6 Detention Certificate; the April 9, 2026 certification "
        "packet as received; internal-affairs or complaint files; and e-mail "
        "concerning the request and the April 20 denial.",
        first_indent=0,
    )
    d.blank_line()
    _para(
        d,
        "<<b:8. Custodian of Records, Commission on Peace Officer Standards "
        "and Training (POST),>> regarding Case No. PUBLIC-26-000371. Subjects: "
        "Plaintiff's complaint forwarded to CHP on or about March 23, 2026, "
        "and POST's handling of that complaint.",
        first_indent=0,
    )

    _heading(d, "B.  Documents and Electronically Stored Information")
    _para(
        d,
        "Fed. R. Civ. P. 26(a)(1)(A)(ii). Plaintiff describes categories and "
        "location rather than attaching copies. Unless noted, copies in "
        "Plaintiff's possession are at 1455 Cat Tail Drive, Stockton, CA 95204, "
        "and in Plaintiff's e-mail account bnn.cdl@gmail.com. Originals of CHP "
        "and POST records are in those agencies' possession.",
        first_indent=0,
    )
    d.blank_line()
    for item in (
        "1. Pleadings, orders, and papers on the PACER docket of this action, "
        "including the First Amended Complaint (Dkt. 10), Notice of Errata "
        "(Dkt. 12), USM-285 return (Dkt. 15), Defendant's motion to dismiss "
        "(Dkt. 18), Plaintiff's opposition (Dkt. 20), Clerk's Notice (Dkt. 21), "
        "and the unsigned stipulation (Dkt. 22).",
        "2. CHP dashcam video transcript of the November 1, 2024 I-580 East "
        "Livermore encounter (approximately 00:54:36 to 01:57:10), and the "
        "underlying recording (original with CHP).",
        "3. CHP Arrest-Investigation Report, Case No. RJ68845.",
        "4. Penal Code section 851.6 Detention Certificate issued by Dublin "
        "CHP on November 5, 2024.",
        "5. Plaintiff's April 9, 2026 U-visa certification packet to CHP "
        "Dublin Area: completed Form I-918, Supplement B; legal memorandum "
        "identifying qualifying criminal activity under 8 U.S.C. "
        "§ 1101(a)(15)(U)(iii); dashcam transcript with timestamped citations; "
        "and supporting exhibits (report, detention certificate, POST "
        "acknowledgment).",
        "6. POST Case No. PUBLIC-26-000371 materials, including the complaint "
        "forwarded to CHP on or about March 23, 2026.",
        "7. Captain Serrato's March 26, 2026 complaint-assignment letter "
        "assigning Sergeant Eric Dutra as investigator.",
        "8. Lieutenant Gary Paul's April 10, 2026 e-mail confirming receipt.",
        "9. Captain Serrato's April 20, 2026 denial letter.",
        "10. California Attorney General Information Bulletin No. DLE-2024-05 "
        "(April 3, 2024).",
        "11. Papers in the related federal action Nforbi v. Meza-Gonzalez et "
        "al., No. 4:26-cv-08271-ASK, and in Newanforbi v. California Highway "
        "Patrol et al., Alameda Superior Court No. 26CV191136, including Hon. "
        "Jenna M. Whitman's August 29, 2026 order (notice of entry August 31).",
        "12. Correspondence with the Office of the Attorney General concerning "
        "this action, including service and case-management e-mails.",
        "13. ESI: e-mails, PDFs, and drafts in Plaintiff's possession relating "
        "to the certification request, the denial, and this lawsuit.",
    ):
        _para(d, item, first_indent=18)
        d.blank_line()

    _heading(d, "C.  Computation of Damages")
    _para(
        d,
        "Fed. R. Civ. P. 26(a)(1)(A)(iii). The First Amended Complaint does "
        "not plead a specific dollar figure. Plaintiff presently computes "
        "claimed damages as follows, subject to supplementation. These "
        "computations are for this action's April 20, 2026 certification "
        "denial. They do not import a wage figure pleaded in any related "
        "action concerning the November 1, 2024 arrest.",
        first_indent=0,
    )
    d.blank_line()
    _para(
        d,
        "<<b:1. Compensatory / noneconomic.>> Deprivation of meaningful access "
        "to the U-visa process; ongoing immigration uncertainty; inability to "
        "obtain employment authorization and removal protections that a "
        "lawful certification decision would have allowed Plaintiff to pursue; "
        "severe emotional distress and anxiety; and deprivation of the "
        "dignitary interest in having a state actor acknowledge documented "
        "criminal misconduct by subordinate officers. These harms began on "
        "April 20, 2026, and are continuing. They are not presently reducible "
        "to a precise dollar figure. Plaintiff will prove them according to "
        "the evidence at trial.",
        first_indent=0,
    )
    d.blank_line()
    _para(
        d,
        "<<b:2. Compensatory / economic.>> Lost opportunity to obtain "
        "employment authorization through the U-visa process as a consequence "
        "of the denial. Plaintiff has not yet quantified a wage-loss or "
        "earnings figure attributable to this action and will supplement "
        "under Rule 26(e) if a figure is developed. Documents that may bear "
        "on that category include the April 9 packet, the April 20 denial, "
        "and any later certification decision.",
        first_indent=0,
    )
    d.blank_line()
    _para(
        d,
        "<<b:3. Punitive damages>> against Defendant in his individual "
        "capacity, for the conduct alleged in the First Amended Complaint, "
        "including a claimed \"thorough review\" unsupported by the record and "
        "willful refusal to engage with evidence in CHP's possession. Amount "
        "according to proof; a jury determination. No insurance or indemnity "
        "document in Plaintiff's possession computes this category.",
        first_indent=0,
    )
    d.blank_line()
    _para(
        d,
        "<<b:4. Prospective relief>> (non-monetary): vacatur of the April 20, "
        "2026 denial and a remand for a new certification decision that "
        "applies the correct statutory standards, engages with the evidence, "
        "and is free of retaliatory motive. Plaintiff does not seek in this "
        "action an order compelling Defendant to sign Form I-918, Supplement "
        "B. See Dkt. 20.",
        first_indent=0,
    )
    d.blank_line()
    _para(
        d,
        "<<b:5. Costs, pre-judgment and post-judgment interest,>> and "
        "attorney's fees under 42 U.S.C. § 1988(b) and California Code of "
        "Civil Procedure section 1021.5 as prayed. Plaintiff is presently "
        "appearing in propria persona. Fee amounts, if any, will be "
        "supplemented if counsel is retained.",
        first_indent=0,
    )

    _heading(d, "D.  Insurance Agreements")
    _para(
        d,
        "Fed. R. Civ. P. 26(a)(1)(A)(iv). Plaintiff is not aware of any "
        "insurance agreement under which an insurance business may be liable "
        "to satisfy all or part of a possible judgment against Plaintiff, or "
        "to indemnify or reimburse for payments made to satisfy such a "
        "judgment. Any indemnity, self-insurance, or coverage applicable to "
        "Defendant is uniquely within Defendant's knowledge and is "
        "Defendant's disclosure obligation.",
        first_indent=0,
    )
    d.blank_line()
    _para(
        d,
        "Plaintiff reserves the right to supplement these disclosures as "
        "investigation and discovery continue, including after a ruling on "
        "Defendant's pending motion to dismiss.",
    )
    _sign_block(d)
    d.save()
    print(f"Wrote {path} ({path.stat().st_size} bytes, {d.page_num} pp.)")


def build_jcms(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    d = PleadingPaper(
        str(path),
        doc_title_footer=(
            "PLAINTIFF'S PORTION OF JCMS -- NEWANFORBI v. SERRATO (N.D. Cal.)"
        ),
    )
    _header(d)
    right = [
        ("Case No. 4:26-cv-05953-ASK", False, False),
        ("", False, False),
        ("PLAINTIFF'S PORTION OF", True, False),
        ("JOINT CASE MANAGEMENT", True, False),
        ("STATEMENT", True, False),
        ("", False, False),
        ("(Civil L.R. 16-9;", False, False),
        ("Standing Order for All", False, False),
        ("Judges, N.D. Cal.)", False, False),
        ("", False, False),
        (f"CMC: {CMC_DATE}", False, False),
        ("Time: 1:30 p.m. via Zoom", False, False),
        ("Judge: Hon. Ajay S. Krishnan", False, False),
    ]
    d.draw_caption_block(CAPTION_LEFT, right, caption_size=10, tight_lh=13, boxed=True)
    d.blank_line()
    d.write_line("PLAINTIFF'S PORTION OF", bold=True, center=True)
    d.write_line("JOINT CASE MANAGEMENT STATEMENT", bold=True, center=True)
    d.blank_line()
    _para(
        d,
        "This is Plaintiff's portion of the joint statement required by Civil "
        "Local Rule 16-9 and the Standing Order for All Judges of the Northern "
        "District of California. It is transmitted to counsel for Defendant "
        "for incorporation of the defense portion and a joint filing. "
        "Plaintiff does not file this document separately. Defense responses "
        "belong under each heading. The joint statement should not exceed ten "
        "pages except in unusually complex cases.",
        first_indent=0,
    )
    d.blank_line()
    _para(
        d,
        f"The initial case management conference is set for {CMC_DATE}, "
        "1:30 p.m., by Zoom (cand.uscourts.gov/ask). On September 3, 2026, "
        "the parties stipulated to continue that conference until fourteen "
        "days after a final order on Defendant's motion to dismiss and to "
        "vacate the September 8 disclosure, joint-statement, and ADR-"
        "certification dates (Dkt. 22). No signed order appears on PACER as "
        "of this writing. Plaintiff therefore submits this portion so that a "
        "joint statement can be filed today if the September 8 deadline "
        "remains live. Plaintiff still prefers the Dkt. 22 continuance. If "
        "the Court has entered that order, this portion should not be filed.",
    )

    _heading(d, "1.  Jurisdiction and Service")
    _para(
        d,
        "Subject-matter jurisdiction is federal question, 28 U.S.C. §§ 1331 "
        "and 1343, on claims under 42 U.S.C. § 1983 and 28 U.S.C. §§ 2201-"
        "2202. Jurisdiction is not based on 28 U.S.C. § 1332(a). Plaintiff "
        "is not aware of a personal-jurisdiction or venue dispute. Venue is "
        "proper in this District and Division because the events occurred in "
        "Alameda County (CHP Dublin Area; I-580 East Livermore). No "
        "counterclaims have been filed. Defendant Captain G. Serrato was "
        "served August 5, 2026, by the United States Marshals Service on Kim "
        "Schoonmaker, Office Assistant, at CHP Dublin Area, 4999 Gleason "
        "Drive, Dublin, CA 94568 (Dkt. 15, filed August 6). DOES 1-10 remain "
        "unnamed. Plaintiff does not presently propose a service deadline for "
        "additional defendants in advance of a ruling on the pending motion "
        "to dismiss.",
        first_indent=0,
    )

    _heading(d, "2.  Facts")
    _para(
        d,
        "Chronology (Plaintiff's account). On November 1, 2024, CHP Officers "
        "Santiago Meza-Gonzalez (#023295) and Jose Melano (#023054) arrested "
        "Plaintiff on I-580 East Livermore (CHP Case No. RJ68845). Plaintiff "
        "contends the sworn report fabricated four material facts that the "
        "dashcam recording disproves: an alcohol odor never verbalized during "
        "a 62-minute encounter; \"slurred\" speech; that Plaintiff \"seemed "
        "very confused and disoriented\"; and \"BEVERAGE PRESENT: YES\" when "
        "the only liquid found was urine in a cup. On November 5, 2024, CHP "
        "issued a Penal Code section 851.6 Detention Certificate, "
        "reclassifying the incident as a detention only, not an arrest, for "
        "insufficient grounds for a criminal complaint. The district attorney "
        "declined to file charges.",
        first_indent=0,
    )
    d.blank_line()
    _para(
        d,
        "On April 9, 2026, Plaintiff submitted a U-visa certification request "
        "to CHP Dublin Area (completed Form I-918, Supplement B; legal "
        "memorandum; POST acknowledgment; timestamped dashcam transcript; "
        "supporting exhibits). Lieutenant Gary Paul e-mailed on April 10 that "
        "the request had been received and was under review. Penal Code "
        "section 679.10(j) required processing within 30 days. On April 20, "
        "2026, Captain Serrato issued a five-sentence denial claiming a "
        "\"thorough review,\" without addressing the dashcam, the section "
        "851.6 certificate, the fabrications, the statutory elements, the "
        "section 679.10(h) presumption, or the section 679.10(g) specific-"
        "reasons requirement. Plaintiff contends the denial was arbitrary, "
        "process-deficient, structurally biased (Serrato as supervisor of the "
        "accused officers), and retaliatory for protected complaints to CHP, "
        "POST, and the courts. Serrato's March 26, 2026 letter had assigned "
        "Sergeant Eric Dutra to investigate the POST complaint "
        "(PUBLIC-26-000371, forwarded on or about March 23).",
        first_indent=0,
    )
    d.blank_line()
    _para(
        d,
        "Principal factual issues in dispute (as Plaintiff understands them): "
        "what review, if any, preceded the April 20 denial; whether Serrato "
        "engaged with the packet and the evidence in CHP's possession; "
        "Serrato's knowledge of Plaintiff's protected activity; the reason "
        "for the denial; and the injuries that followed. Defendant's account "
        "belongs here.",
        first_indent=0,
    )

    _heading(d, "3.  Legal Issues")
    _para(
        d,
        "Without extended argument, Plaintiff identifies these disputed "
        "points of law: (a) whether the April 20 denial violated the "
        "Fourteenth Amendment's guarantee of non-arbitrary decision-making "
        "in the exercise of the certification function, see <<i:Shanks v. "
        "Dressel>>, 540 F.3d 1082 (9th Cir. 2008); (b) whether Plaintiff was "
        "denied constitutionally adequate process, see <<i:Mathews v. "
        "Eldridge>>, 424 U.S. 319 (1976), Penal Code § 679.10(g), (h), (j), "
        "and <<i:Withrow v. Larkin>>, 421 U.S. 35 (1975); (c) whether the "
        "denial was First Amendment retaliation for protected petitioning, "
        "see <<i:Hartman v. Moore>>, 547 U.S. 250 (2006), and <<i:Borough of "
        "Duryea v. Guarnieri>>, 564 U.S. 379 (2011); (d) qualified immunity; "
        "(e) the proper scope of prospective relief under <<i:Ex parte "
        "Young>>, 209 U.S. 123 (1908) (Plaintiff seeks vacatur and a new "
        "decision, not a directed Form B signature); and (f) whether "
        "punitive damages and fee claims may be stricken under Rule 12(f). "
        "Those issues are briefed on Dkt. 18 and Dkt. 20, set for hearing "
        f"{MTD_DATE}.",
        first_indent=0,
    )

    _heading(d, "4.  Motions")
    _para(
        d,
        "Prior: IFP granted and complaint found sufficient under 28 U.S.C. "
        "§ 1915 (Dkt. 5, June 29, 2026); related-case motion granted as to "
        "Nforbi v. Meza-Gonzalez, then 3:26-cv-08271-PHK, now "
        "4:26-cv-08271-ASK (Dkt. 16, 17). Pending: Defendant's motion to "
        "dismiss the FAC and/or strike (Dkt. 18), opposition Dkt. 20, hearing "
        f"reset by Dkt. 21 to {MTD_DATE}, 1:30 p.m., Oakland Courtroom 4 "
        "(Dkt. 21's 2025 briefing years are wrong on the face of the notice). "
        "Dkt. 22 (stipulation to continue the CMC) is filed; no order. "
        "Plaintiff's Civil L.R. 3-15 certification was executed September 4, "
        "2026, and has not yet been filed. Plaintiff's August 25 "
        "administrative motion concerning Candelaria, 3:26-cv-08272-LJC "
        "(docketed as Dkt. 19) had no order on the September 4 PACER report. "
        "Anticipated: Defendant's reply on Dkt. 18; possibly an answer if "
        "the motion is denied in whole or in part; possibly amendment if "
        "leave is granted. Plaintiff does not presently anticipate a "
        "separate Rule 12 motion.",
        first_indent=0,
    )

    _heading(d, "5.  Amendment of Pleadings")
    _para(
        d,
        "The operative pleading is the First Amended Complaint (Dkt. 10), "
        "with Notice of Errata (Dkt. 12) correcting related-action "
        "disclosure. Plaintiff does not presently intend to add parties or "
        "claims before a ruling on Dkt. 18, except as that ruling may "
        "require. Plaintiff proposes any amendment deadline of 30 days after "
        "the Court's order on Dkt. 18.",
        first_indent=0,
    )

    _heading(d, "6.  Evidence Preservation")
    _para(
        d,
        "Plaintiff has reviewed the Northern District's Guidelines Relating "
        "to the Discovery of Electronically Stored Information. Plaintiff "
        "has preserved e-mails, PDFs, and files in his possession relating to "
        "the certification request, the denial, and this case, and has not "
        "operated a document-destruction program. The parties spoke by "
        "telephone on September 3, 2026 (Dkt. 22 ¶ 7). Plaintiff asks "
        "Defendant to confirm preservation of the dashcam original, CAD and "
        "arrest-report files for RJ68845, the April 9 packet as received, "
        "internal-affairs and complaint files, and e-mail concerning the "
        "request and the April 20 denial. Plaintiff is prepared to complete "
        "an ESI meet-and-confer under Guidelines 2.01 and 2.02.",
        first_indent=0,
    )

    _heading(d, "7.  Disclosures")
    _para(
        d,
        "Plaintiff is serving Rule 26(a)(1) initial disclosures with this "
        f"portion, dated {EXEC_DATE}: witnesses, document categories and "
        "locations, a damages computation (the FAC pleads no dollar figure; "
        "noneconomic damages according to proof; no imported wage number "
        "from a related arrest case), and insurance (none known as to "
        "Plaintiff). Defendant's compliance should be stated here.",
        first_indent=0,
    )

    _heading(d, "8.  Discovery")
    _para(
        d,
        "No formal discovery has been taken. The parties' September 3 "
        "telephone conference is the Rule 26(f) conference of record in "
        "Dkt. 22. Plaintiff proposes: written discovery (interrogatories, "
        "requests for production, requests for admission) to Defendant; "
        "third-party process to CHP and POST custodians for the categories "
        "in Plaintiff's disclosures; and depositions of Captain Serrato, "
        "Lieutenant Paul, Sergeant Dutra, and, as needed, Officers Meza-"
        "Gonzalez and Melano. Plaintiff has considered a stipulated e-"
        "discovery order and is willing to use the District's model. "
        "Plaintiff does not agree that a discovery stay follows automatically "
        "from the pending Rule 12 motion; Plaintiff is willing to discuss "
        "deferring depositions until after a ruling if document discovery "
        "may proceed. No discovery dispute is pending. Defendant's plan "
        "belongs here.",
        first_indent=0,
    )

    _heading(d, "9.  Class Actions")
    _para(d, "This is not a class action.", first_indent=0)

    _heading(d, "10.  Related Cases")
    _para(
        d,
        "(a) <<i:Nforbi v. Meza-Gonzalez et al.>>, No. 4:26-cv-08271-ASK, "
        "this Court (related by Dkt. 17, August 24, 2026); claims against "
        "the stopping officers arising from November 1, 2024. (b) "
        "<<i:Newanforbi v. California Highway Patrol et al.>>, Alameda "
        "Superior Court No. 26CV191136 (writ of mandate concerning Penal "
        "Code section 679.10); Hon. Jenna M. Whitman, August 29, 2026, "
        "overruled the demurrer as to Count 1, sustained Counts 2-3 without "
        "leave, and sustained Count 4 with leave; Dutra and Paul were "
        "dismissed by stipulation. (c) POST Case No. PUBLIC-26-000371. (d) "
        "Plaintiff's August 25 administrative motion (Dkt. 19) asking "
        "whether <<i:Nforbi v. Candelaria et al.>>, No. 3:26-cv-08272-LJC, "
        "should also be related; no order on the September 4 PACER report. "
        "Terminated proceedings recited in the motion-to-dismiss papers "
        "include Alameda No. 26CV168913 and E.D. Cal. No. "
        "2:25-cv-01460-DC-CSK (dismissed without prejudice).",
        first_indent=0,
    )

    _heading(d, "11.  Relief")
    _para(
        d,
        "As pleaded: compensatory damages for deprivation of meaningful "
        "access to the U-visa process, immigration uncertainty, inability to "
        "obtain employment authorization and removal protections, emotional "
        "distress, anxiety, and dignitary injury; punitive damages against "
        "Defendant individually; costs, interest, and fees under 42 U.S.C. "
        "§ 1988(b) and Code of Civil Procedure section 1021.5; and "
        "declaratory and injunctive process-correction relief — vacatur of "
        "the April 20, 2026 denial and a new decision applying the correct "
        "standards to the evidence, not a directed Form B signature (Dkt. "
        "20). The FAC does not plead a specific compensatory figure. "
        "Noneconomic damages will be proved according to the evidence. "
        "Plaintiff has not quantified a wage-loss figure in this action and "
        "will supplement if one is developed. Punitive damages according to "
        "proof. Defendant should state any competing method of calculation.",
        first_indent=0,
    )

    _heading(d, "12.  Settlement and ADR")
    _para(
        d,
        "Prospects: Plaintiff is willing to settle on vacatur of the denial, "
        "a constitutionally adequate new certification decision, and "
        "reasonable compensatory relief. The pending motion to dismiss is "
        "the principal obstacle to a meaningful negotiation. ADR efforts to "
        "date: the September 3 telephone conference; no mediation. Plan: "
        "court-sponsored mediation after a ruling on Dkt. 18, consistent "
        "with ADR L.R. 3-5. The ADR certification was due August 25, 2026 "
        "(Dkt. 4). Service was completed August 5, so that date ran before "
        "a complete Rule 26(f) conference; no ADR certification appears on "
        "the September 4 PACER report. Plaintiff will file the ADR "
        "certification promptly unless Dkt. 22 vacates that deadline. "
        "Defendant's ADR position belongs here.",
        first_indent=0,
    )

    _heading(d, "13.  Other References")
    _para(
        d,
        "This case is not suitable for binding arbitration, a special "
        "master, or the Judicial Panel on Multidistrict Litigation.",
        first_indent=0,
    )

    _heading(d, "14.  Narrowing of Issues")
    _para(
        d,
        "The Rule 12 motion may narrow or end claims. If claims proceed, "
        "the parties may be able to stipulate to authenticity of the April "
        "9 packet, the April 10 e-mail, the April 20 denial, the dashcam "
        "recording, Report RJ68845, and the section 851.6 certificate. "
        "Plaintiff does not request bifurcation. Plaintiff proposes the "
        "following as the most consequential issues (Defendant to confirm "
        "or substitute):",
        first_indent=0,
    )
    d.blank_line()
    d.write_wrapped(
        "<<b:Whether the April 20, 2026 denial violated the Fourteenth "
        "Amendment (substantive and/or procedural due process).>>",
        first_indent=18,
    )
    d.write_wrapped(
        "<<b:Whether the denial was First Amendment retaliation for "
        "protected petitioning.>>",
        first_indent=18,
    )
    d.write_wrapped(
        "<<b:Whether qualified immunity bars damages against Defendant in "
        "his individual capacity.>>",
        first_indent=18,
    )
    d.blank_line()
    _para(
        d,
        "Resolution of the first two issues on a correct legal standard, "
        "including on Dkt. 18, will determine whether discovery and trial "
        "are required and the scope of any prospective remedy.",
        first_indent=0,
    )

    _heading(d, "15.  Scheduling")
    _para(
        d,
        "Plaintiff prefers the Dkt. 22 schedule: continue the initial CMC "
        "until fourteen days after a final order on Dkt. 18, and reset "
        "disclosure, JCMS, and ADR dates from that conference. If this "
        "conference proceeds on September 15, Plaintiff proposes the "
        "following, subject to adjustment after the motion-to-dismiss "
        "ruling:",
        first_indent=0,
    )
    d.blank_line()
    for row in (
        "Close of fact discovery: April 16, 2027",
        "Opening expert disclosures: May 14, 2027",
        "Rebuttal expert disclosures: June 11, 2027",
        "Close of expert discovery: June 25, 2027",
        "Last day to hear dispositive motions: August 12, 2027",
        "Pretrial conference: September 15, 2027",
        "Jury trial: October 5, 2027, or the first available date thereafter",
    ):
        d.write_line(row, indent=18)
    d.blank_line()
    _para(
        d,
        "If the Court grants leave to amend, Plaintiff proposes that these "
        "dates run from the amended pleading rather than from September 15. "
        "Defendant's dates belong here.",
        first_indent=0,
    )

    _heading(d, "16.  Trial")
    _para(
        d,
        "Plaintiff demanded a jury (PACER: Jury Demand: Plaintiff) and "
        "expects a jury trial of approximately four to five court days. "
        "Official-capacity prospective relief, if tried, would be to the "
        "Court.",
        first_indent=0,
    )

    _heading(d, "17.  Disclosure of Non-party Interested Entities or Persons")
    _para(
        d,
        "Plaintiff executed a Civil L.R. 3-15 Certification of Conflicts, "
        "Interested Entities and Persons, and Citizenship on September 4, "
        "2026. It has not yet been filed; Plaintiff will file it promptly. "
        "Restated: Plaintiff is a natural person with no parent corporation "
        "and no litigation funder. As of September 4, 2026, there is no "
        "conflict or interest (other than the named parties) to report. "
        "Plaintiff is not aware of any conflict the presiding Judge may have "
        "with the parties. This Court's jurisdiction is not based on 28 "
        "U.S.C. § 1332(a). Defendant's certification belongs here.",
        first_indent=0,
    )

    _heading(d, "18.  Professional Conduct")
    _para(
        d,
        "Plaintiff, appearing in propria persona, has reviewed the "
        "Guidelines for Professional Conduct for the Northern District of "
        "California. Counsel of record should confirm their review.",
        first_indent=0,
    )

    _heading(d, "19.  Other Matters")
    _para(
        d,
        "Plaintiff consented to magistrate-judge jurisdiction (Dkt. 8). "
        "Plaintiff does not know whether Defendant has filed a consent or "
        "declination. The initial CMC remains by Zoom at "
        "cand.uscourts.gov/ask. Please do not treat Dkt. 22 as an order "
        "until it is signed and on PACER.",
        first_indent=0,
    )
    _sign_block(d)
    d.save()
    print(f"Wrote {path} ({path.stat().st_size} bytes, {d.page_num} pp.)")


def pos_fields() -> ProofOfServiceFields:
    return ProofOfServiceFields(
        plaintiff_line="BRENDAN NGEHSI NEWANFORBI",
        plaintiff_role="Plaintiff",
        defendant_lines=[
            "CAPTAIN G. SERRATO; and",
            "DOES 1-10, inclusive",
        ],
        defendant_role="Defendants",
        case_number="4:26-cv-05953-ASK",
        title="PROOF OF SERVICE",
        service_date=EXEC_DATE,
        document_title=(
            "Plaintiff's Rule 26(a)(1) Initial Disclosures and Plaintiff's "
            "Portion of Joint Case Management Statement"
        ),
        recipients=[
            "Haiyang A. Li, Deputy Attorney General — Haiyang.Li@doj.ca.gov",
            "Office of the Attorney General, 300 South Spring Street, Suite 1702",
            "Los Angeles, CA 90013-1230",
            "Attorney for Defendant Captain G. Serrato",
        ],
        server_name="Brendan Ngehsi Newanforbi",
        stamp_signature=True,
        district_line=DISTRICT_NDCAL,
        by_email=True,
    )


def build_pos(path: Path) -> Path:
    out = build_proof_of_service(path, pos_fields())
    print(f"Wrote {out} ({out.stat().st_size} bytes)")
    return out


def main() -> None:
    if not Path(SIGNATURE_PATH).is_file():
        raise SystemExit(f"Missing signature: {SIGNATURE_PATH}")
    build_disclosures(OUT_DISCLOSURES)
    build_jcms(OUT_JCMS)
    build_pos(OUT_POS)
    artifact_dir = Path("/opt/cursor/artifacts")
    if artifact_dir.is_dir():
        import shutil

        for src in (OUT_DISCLOSURES, OUT_JCMS, OUT_POS):
            shutil.copy2(src, artifact_dir / src.name)
            print(f"Copied {src.name} to {artifact_dir}")


if __name__ == "__main__":
    main()
