#!/usr/bin/env python3
"""Matter 27 — Declaration ISO default judgment by court as to Randstad US, LLC.

Alameda Super. Ct. No. 26CV199902, Dept. 20 (Hon. Thomas Weathers).

Amounts are a Kim v. Westmoore prove-up the Court can walk on one page:
ICRAA $10,000 + Penal Code additional $10,000 (1x the ICRAA figure as the
actuals stand-in) + $25,000 civil penalty + $543.70 interest = $45,543.70.
The served CCP section 425.115 notice ($500,000) is the preserved cap;
$0 punitive is requested on this packet. No CCP section 425.11; general/
emotional-distress and lost-wage "according to proof" sums are omitted.

  python3 internal/scripts/matter27-randstad-prove-up-declaration.py
"""
from __future__ import annotations

import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, "lib"))
from pleading_paper import (  # noqa: E402
    CONTENT_LEFT,
    COURT_LINE1,
    PleadingPaper,
)

sys.path.insert(0, SCRIPT_DIR)
from signature_stamp import (  # noqa: E402
    SIGNATURE_NATIVE_PX,
    SIGNATURE_PATH,
)

SIGNATURE_IMG = SIGNATURE_PATH
SIG_IMG_W_PX, SIG_IMG_H_PX = SIGNATURE_NATIVE_PX
SIG_WIDTH = 140

NO_SIGNATURE = os.environ.get("MATTER27_NO_SIGNATURE", "") == "1"
OUT_DIR = os.environ.get("MATTER27_DECL_OUT_DIR", "/tmp/m27build")
COURT_LINE2 = "COUNTY OF ALAMEDA"
CASE_NO = "26CV199902"
EXEC_DATE = os.environ.get("MATTER27_EXEC_DATE", "September 16, 2026")
DECL_TAG = os.environ.get("MATTER27_DECL_TAG", "Sep16_2026")

ICRAA = "10,000.00"
PC_ADD = "10,000.00"
PC_PENALTY = "25,000.00"
DAMAGES = "45,000.00"
PUNITIVE = "0.00"
INTEREST = "543.70"
TOTAL = "45,543.70"
RATE = "7"
DAYS = "63"
CAP_NOTICED = "500,000.00"


def party_block(d: PleadingPaper) -> None:
    c = d.c
    atty_y = d._line_y(0)
    atty_lh = 15
    lines = [
        ("BRENDAN NGEHSI NEWANFORBI", "Times-Bold", 12),
        ("Plaintiff, In Pro Per", "Times-Roman", 12),
        ("1455 Cat Tail Drive", "Times-Roman", 12),
        ("Stockton, CA 95204", "Times-Roman", 12),
        ("Telephone: (209) 801-4442", "Times-Roman", 12),
        ("E-mail: bnn.cdl@gmail.com", "Times-Roman", 12),
    ]
    for i, (txt, fn, sz) in enumerate(lines):
        c.setFont(fn, sz)
        c.drawString(CONTENT_LEFT, atty_y - i * atty_lh, txt)
    d.current_line = 4
    d.blank_line()
    d.write_line(COURT_LINE1, bold=True, center=True)
    d.write_line(COURT_LINE2, bold=True, center=True)
    d.blank_line()


def caption_left() -> list[tuple[str, bool, bool]]:
    return [
        ("BRENDAN NGEHSI NEWANFORBI,", True, False),
        ("", False, False),
        ("                          Plaintiff,", False, False),
        ("", False, False),
        ("       v.", False, False),
        ("", False, False),
        ("RANDSTAD US, LLC, a Delaware", True, False),
        ("limited liability company;", True, False),
        ("THE RK LOGISTICS GROUP, INC.,", True, False),
        ("a California corporation; and", True, False),
        ("DOES 1 through 20, inclusive,", True, False),
        ("", False, False),
        ("                          Defendants.", False, False),
    ]


def render_content(d: PleadingPaper, content: list[tuple[str, str]]) -> None:
    for c_type, text in content:
        if c_type == "HEADER":
            d.ensure_space(3)
            d.write_line(text, bold=True, center=True)
            d.blank_line()
        elif c_type == "SUBHEAD":
            d.ensure_space(3)
            for line in text.split("\n"):
                d.write_line(line, bold=True, center=False)
            d.blank_line()
        elif c_type == "PARA":
            d.write_wrapped(text, first_indent=36)
            d.blank_line()
        elif c_type == "LIST_ITEM":
            d.write_wrapped(text, indent=36, first_indent=36)
            d.blank_line()
        elif c_type == "SIGNATURE":
            d.ensure_space(8)
            for line in text.split("\n"):
                if line.startswith("_") and not NO_SIGNATURE and os.path.isfile(SIGNATURE_IMG):
                    d.draw_signature_image(
                        SIGNATURE_IMG,
                        SIG_IMG_W_PX,
                        SIG_IMG_H_PX,
                        line,
                        width=SIG_WIDTH,
                        right_margin_offset=20,
                    )
                    d.write_line(line, right=True, right_margin_offset=20)
                else:
                    d.write_line(line, right=True, right_margin_offset=20)
            d.blank_line()
        elif c_type == "PAGEBREAK":
            d.start_new_page()


def signature_block_text() -> str:
    return (
        f"\nExecuted on {EXEC_DATE},\n"
        "at Stockton, California.\n"
        "\n"
        "___________________________________\n"
        "BRENDAN NGEHSI NEWANFORBI\n"
        "Plaintiff, In Pro Per"
    )


EXHIBITS = [
    "Exhibit A. Verified Complaint for Damages (filed July 20, 2026), including the Prayer for Relief.",
    "Exhibit B. POS-010 Proof of Service of Summons on Randstad US, LLC (personally served July 30, 2026, Levying Officer File No. 2026026857).",
    "Exhibit C. CIV-100 Request for Entry of Default as to Randstad US, LLC, FILE-stamped September 16, 2026 (Deputy S. Pesko); default ENTERED the same day.",
    "Exhibit D. Amended Notice of Amount of Punitive Damages Sought (CCP section 425.115) as to Randstad US, LLC ($500,000.00; executed August 7, 2026).",
    "Exhibit E. POS-040 Proof of Service of the Amended CCP section 425.115 Notice on Randstad US, LLC (personally served August 21, 2026; filed September 9, 2026; Levying Officer File No. 2026028894).",
    "Exhibit F. InfoMart background-check report, Order No. 15780719 (Billing Code RK LOGISTICS; sole adverse item the California sex-offender registry).",
    "Exhibit G. InfoMart Notice to Consumer for Employment Purposes (July 13, 2026).",
    "Exhibit H. Randstad notification that Plaintiff's employee status changed to Rehired (July 7, 2026).",
    "Exhibit I. FW-003 Order on Court Fee Waiver, granted July 20, 2026.",
]


def declaration_content() -> list[tuple[str, str]]:
    return [
        ("HEADER", "DECLARATION OF BRENDAN NGEHSI NEWANFORBI"),
        ("HEADER", "IN SUPPORT OF REQUEST FOR DEFAULT JUDGMENT BY COURT"),
        (
            "SUBHEAD",
            "(Cal. Rules of Court, rule 3.1800; Code Civ. Proc. sections 579, 585(b), 585(d))",
        ),
        ("PARA", "I, <<b:BRENDAN NGEHSI NEWANFORBI>>, declare:"),
        ("HEADER", "I.  PRELIMINARY STATEMENT"),
        (
            "PARA",
            "1. I am the Plaintiff in the above-entitled action and am over eighteen "
            "years of age. The matters set forth herein are within my personal knowledge "
            "unless stated on information and belief, and if called as a witness I could "
            "and would competently testify to them. I submit this Declaration in support "
            "of my Request for Default Judgment by the Court (Judicial Council Form "
            "CIV-100) against Defendant <<b:RANDSTAD US, LLC>>, a Delaware limited "
            "liability company (\"Randstad\"), pursuant to Code of Civil Procedure "
            "section 585, subdivisions (b) and (d), and California Rules of Court, "
            "rule 3.1800.",
        ),
        (
            "PARA",
            "2. This Declaration is submitted with: (a) Plaintiff's Request for Court "
            "Judgment (Form CIV-100), including the declaration of nonmilitary status at "
            "item 8; (b) Plaintiff's [Proposed] Judgment (Form JUD-100); (c) Plaintiff's "
            "Request for Dismissal of Does 1 through 20 without prejudice (Form CIV-110); "
            "and (d) the exhibits listed in the Index below. Default as to Randstad was "
            "already entered on September 16, 2026. This paper asks for a court judgment "
            "on that default. It does not ask the clerk to enter default again, and it "
            "does not seek judgment against The RK Logistics Group, Inc. (\"RK Logistics\").",
        ),
        (
            "PARA",
            "3. The amounts requested are the conservative statutory figures this "
            "record can support on a default prove-up, not the Greenup / section "
            f"425.115 ceiling. They total ${TOTAL}, computed as follows: Civil Code "
            f"section 1786.50 statutory damages of ${ICRAA}; Penal Code section 290.46 "
            f"additional amount of ${PC_ADD} (one times the ICRAA figure, treated as "
            f"the actual-damages stand-in); subdivision civil penalty of ${PC_PENALTY}; "
            f"and prejudgment interest of ${INTEREST} at {RATE} percent. Punitive "
            f"damages noticed under section 425.115 at ${CAP_NOTICED} are recited so "
            "the cap is preserved; I request $0.00 in punitive damages on this packet. "
            "Costs are waived. Attorney's fees are not requested. General damages and "
            "lost wages pleaded \"according to proof\" are not requested.",
        ),
        ("HEADER", "II.  PROCEDURAL POSTURE"),
        (
            "PARA",
            "4. The operative pleading is the Verified Complaint for Damages filed "
            "July 20, 2026 (Exhibit A). It asserts six causes of action against Randstad "
            "and RK Logistics: (1) violation of Penal Code section 290.46, subdivision "
            "(j)(2)(E); (2) wrongful termination in violation of public policy; "
            "(3) violation of the Investigative Consumer Reporting Agencies Act "
            "(Civ. Code section 1786 et seq.); (4) invasion of privacy; (5) negligence "
            "per se; and (6) unlawful business practices (Bus. & Prof. Code section "
            "17200 et seq.).",
        ),
        (
            "PARA",
            "5. The summons and complaint were personally served on Randstad on "
            "July 30, 2026, at its registered agent CSC - Lawyers Incorporating Service, "
            "by Sacramento County Sheriff / Josh Swindell (Levying Officer File No. "
            "2026026857). The POS-010 was accepted for filing August 7, 2026. A true "
            "copy is Exhibit B.",
        ),
        (
            "PARA",
            "6. On August 7, 2026, I executed an Amended Notice of Amount of Punitive "
            "Damages Sought under Code of Civil Procedure section 425.115, stating that "
            f"I reserve the right to seek ${CAP_NOTICED} in punitive damages against "
            "Randstad. That notice was personally served on Randstad on August 21, 2026, "
            "at CSC, by Sacramento County Sheriff / F. Conley (Levying Officer File No. "
            "2026028894). The POS-040 was filed September 9, 2026. True copies are "
            "Exhibits D and E. Default had not been entered when that notice was served. "
            "Code of Civil Procedure section 425.115 therefore supplies the noticed "
            "punitive ceiling on this default. I recite that ceiling so it is preserved. "
            "I do not ask the Court to write that figure on the judgment. No Code of "
            "Civil Procedure section 425.11 statement of damages was served, and I do "
            "not request personal-injury general damages on this prove-up.",
        ),
        (
            "PARA",
            "7. Randstad's time to respond was extended by party agreement through "
            "and including September 15, 2026. That was the one 15-day extension under "
            "California Rules of Court, rule 3.110(d), without a court order. Randstad "
            "did not answer, demur, move to strike, or otherwise appear. On September 16, "
            "2026, I filed a CIV-100 requesting entry of default only (item 1c). The "
            "clerk, Deputy S. Pesko, ENTERED default as to Randstad the same day. A "
            "true copy of the FILE-stamped CIV-100 is Exhibit C. No clerk's judgment "
            "and no court judgment has been entered. This Request asks for a court "
            "judgment for default previously entered on September 16, 2026.",
        ),
        (
            "PARA",
            "8. I apply for a several judgment against Randstad alone under Code of "
            "Civil Procedure section 579. RK Logistics remains a named defendant. A "
            "CIV-141 was served on September 14, 2026, on behalf of RK Logistics; I "
            "have not treated that paper as entered without a clerk stamp, and I am "
            "not requesting default or judgment against RK Logistics in this packet. "
            "A several judgment is proper because Randstad is the employer of record "
            "that ordered the background check and delivered the July 15, 2026 "
            "termination, the default is as to Randstad only, and the action can "
            "proceed against RK Logistics. Does 1 through 20 are dismissed without "
            "prejudice by the accompanying CIV-110. California Rules of Court, "
            "rule 3.1800(a)(7), is therefore satisfied.",
        ),
        (
            "PARA",
            "9. Concurrently with this filing I am mailing copies of the CIV-100 "
            "application for judgment, first-class, postage prepaid, to Randstad's "
            "attorney of record, Chadwick L. Williams, Esq., Kabat Chapman & Ozmer LLP, "
            "1150 Spring Street NW, Suite 800, Atlanta, GA 30309, and to Randstad US, "
            "LLC, c/o CSC - Lawyers Incorporating Service, 2710 Gateway Oaks Drive, "
            "Suite 150N, Sacramento, CA 95833, as declared on CIV-100 item 6 and "
            "required by Code of Civil Procedure section 587.",
        ),
        ("HEADER", "III.  BRIEF SUMMARY OF THE CASE"),
        (
            "SUBHEAD",
            "(Cal. Rules of Court, rule 3.1800(a)(2))",
        ),
        (
            "PARA",
            "10. I applied on June 30, 2026, through Indeed, for a Class C Driver - "
            "Bobtail position listed by RK Logistics at its Newark, California facility. "
            "I held a valid California Class C license. On July 7, 2026, Randstad "
            "notified me that my employee status had changed to Rehired (Exhibit H). "
            "That same day Randstad caused InfoMart LLC to run a background investigation "
            "(Order No. 15780719) billed to \"RK LOGISTICS.\"",
        ),
        (
            "PARA",
            "11. On July 13, 2026, InfoMart completed the report. Every criminal-court "
            "search returned No Record. The sole adverse item was the National Sex "
            "Offender Search result: \"Subject is a registered Sex Offender in "
            "California.\" The overall status was \"NEEDS APPROVAL, PER CLIENT "
            "CRITERIA.\" A true copy of the report is Exhibit F. InfoMart's Notice to "
            "Consumer for Employment Purposes of the same date is Exhibit G.",
        ),
        (
            "PARA",
            "12. Penal Code section 290.46, subdivision (j)(2)(E), prohibits using "
            "information disclosed on the Megan's Law Internet website for purposes "
            "relating to employment. On July 15, 2026, Randstad terminated my employment. "
            "I had been rehired but had not commenced active paid shifts. By default, "
            "the well-pleaded allegations of the verified Complaint are admitted.",
        ),
        ("HEADER", "IV.  DAMAGES REQUESTED — WHAT THIS RECORD SUPPORTS"),
        (
            "PARA",
            "13. Code of Civil Procedure section 580 and Greenup v. Rodman (1986) "
            "42 Cal.3d 822 limit a default judgment to the amount demanded in the "
            "complaint, and, for punitive damages, to the amount noticed under section "
            f"425.115 before default. That ceiling here is the numbered prayer plus "
            f"${CAP_NOTICED}. Kim v. Westmoore Partners, Inc. (2011) 201 Cal.App.4th "
            "267 requires that a default prove-up still prove the dollars. I therefore "
            "ask only for the itemized statutory sums this file can walk the Court "
            "through on one page, and I do not ask the Court to enter the noticed "
            "punitive ceiling.",
        ),
        (
            "PARA",
            "14. Prayer item 6 (third cause of action) seeks statutory damages of "
            "$10,000 per violation, or actual damages, whichever is greater, under "
            "Civil Code section 1786.50. I worked no paid shift between the July 7 "
            "rehire and the July 15 termination, so actual wage loss on this prove-up "
            f"is $0.00. The greater figure is ${ICRAA}. I request ${ICRAA} on the "
            "ICRAA count for one qualifying use of the InfoMart investigative consumer "
            "report ordered July 7, 2026 (Order No. 15780719) and used in the July 15 "
            "termination. Randstad is the user that ordered the report.",
        ),
        (
            "PARA",
            "15. Prayer item 3 (first cause of action) seeks an additional amount "
            "under Penal Code section 290.46, pleaded as subdivision (j)(5). The "
            "current code places that civil remedy at subdivision (j)(4)(A): actual "
            "damages, plus an additional amount of at least $250 and at most three "
            "times actual damages, plus fees, plus either exemplary damages or a civil "
            "penalty not exceeding $25,000. It is not \"actuals or $25,000, whichever "
            f"is greater.\" I treat the ICRAA ${ICRAA} as the actual-damages stand-in "
            f"and request one times that figure, ${PC_ADD}, as the additional amount "
            "— not three times, and not the $250 floor. If the Court declines to treat "
            "the ICRAA statutory sum as Penal Code actuals, the additional amount is "
            "$250.00 and the rest of this Request is unchanged.",
        ),
        (
            "PARA",
            "16. Prayer item 4 seeks exemplary damages or a civil penalty not "
            "exceeding $25,000 per violation under the same subdivision. I request "
            f"the civil penalty of ${PC_PENALTY} as a statutory penalty. I do not also "
            "ask for open-ended Civil Code section 3294 punitive damages, and I do "
            "not stack a Penal Code exemplary award, on the same count.",
        ),
        (
            "PARA",
            "17. Prayer items 1, 2, and 8 seek compensatory damages, general damages "
            "for emotional distress, and UCL restitution, each according to proof. I "
            "do not request those sums on this default. No section 425.11 statement was "
            "served (Schwab v. Rondel Homes, Inc. (1991) 53 Cal.3d 428). I earned no "
            "wages during the July 7-15 window. I do not load homelessness, parole "
            "transfer, or any other portfolio fact onto this eight-day rehire. Omitting "
            "those items keeps this Request inside numbered, documentable dollars.",
        ),
        (
            "PARA",
            "18. Prayer items 5 and 7 seek punitive damages under Civil Code sections "
            "3294 and 1786.50. Exhibit D noticed "
            f"${CAP_NOTICED}. Default admits the well-pleaded facts, not the amount of "
            "damages. Asking that ceiling on an eight-day staffing rehire, with no paid "
            "shifts and no medical file tied to Randstad, would not survive Kim "
            f"scrutiny. I request punitive damages of ${PUNITIVE} on this packet.",
        ),
        (
            "PARA",
            f"19. Itemized principal therefore totals ${DAMAGES} "
            f"(${ICRAA} + ${PC_ADD} + ${PC_PENALTY}). Punitive damages requested are "
            f"${PUNITIVE}. The demand of the complaint on CIV-100 item 2a is ${DAMAGES}.",
        ),
        ("HEADER", "V.  PREJUDGMENT INTEREST"),
        (
            "PARA",
            "20. Prayer item 11 seeks prejudgment interest. The statutory sums in "
            "paragraph 19 are certain within Civil Code section 3287, subdivision (a). "
            "No contract rate applies. The constitutional rate of seven percent per "
            "annum therefore governs. Cal. Const., art. XV, section 1. Interest runs "
            f"from July 15, 2026 (the termination) through {EXEC_DATE}. That is {DAYS} "
            f"days. Computation: ${DAMAGES} x 0.07 x {DAYS}/365 = ${INTEREST}. "
            "Interest is not requested on any punitive sum.",
        ),
        ("HEADER", "VI.  COSTS AND ATTORNEY'S FEES"),
        (
            "PARA",
            "21. Court fees were waived by FW-003 granted July 20, 2026 (Exhibit I). "
            "I waive recoverable costs of suit against Randstad on CIV-100 item 7f. "
            "No Memorandum of Costs is filed. I am informed that Government Code "
            "section 68637 may impose a lien or repayment of waived fees if I recover "
            "$10,000 or more; the accompanying CIV-110 so declares. That is an "
            "obligation to the court, not a cost taxed against Randstad in this judgment.",
        ),
        (
            "PARA",
            "22. I appear in propria persona. I do not request attorney's fees on "
            "this prove-up.",
        ),
        ("HEADER", "VII.  INJUNCTIVE RELIEF"),
        (
            "PARA",
            "23. Prayer item 9 seeks injunctive relief. To permit judgment on "
            "declaration under Code of Civil Procedure section 585, subdivision (d), "
            "I do not request injunctive relief in this packet.",
        ),
        ("HEADER", "VIII.  NONMILITARY STATUS"),
        (
            "PARA",
            "24. Randstad US, LLC is a Delaware limited liability company and a "
            "business entity. It is not eligible to serve in the United States military. "
            "The declaration at CIV-100 item 8 so states.",
        ),
        ("HEADER", "IX.  REQUESTED JUDGMENT"),
        (
            "PARA",
            "25. I respectfully request that the Court enter default judgment on "
            "declaration in favor of Plaintiff Brendan Ngehsi Newanforbi and against "
            "Defendant Randstad US, LLC, a Delaware limited liability company, as follows:",
        ),
        (
            "LIST_ITEM",
            f"a. Damages (itemized statutory): ${DAMAGES};",
        ),
        (
            "LIST_ITEM",
            f"b. Prejudgment interest at {RATE} percent from July 15, 2026: ${INTEREST};",
        ),
        (
            "LIST_ITEM",
            "c. Costs: $0.00 (waived);",
        ),
        (
            "LIST_ITEM",
            "d. Attorney's fees: $0.00 (not requested);",
        ),
        (
            "LIST_ITEM",
            f"e. Punitive damages: ${PUNITIVE} (section 425.115 cap of ${CAP_NOTICED} "
            "noticed and preserved; not requested on this judgment);",
        ),
        (
            "LIST_ITEM",
            f"f. TOTAL: ${TOTAL}.",
        ),
        (
            "PARA",
            "26. The judgment should be several as to Randstad only, leaving the "
            "action pending against RK Logistics, with Does 1 through 20 dismissed "
            "without prejudice.",
        ),
        ("HEADER", "X.  INDEX OF EXHIBITS"),
        *[("LIST_ITEM", item) for item in EXHIBITS],
        (
            "PARA",
            "I declare under penalty of perjury under the laws of the State of "
            "California that the foregoing is true and correct.",
        ),
        ("SIGNATURE", signature_block_text()),
    ]


def build_declaration() -> str:
    os.makedirs(OUT_DIR, exist_ok=True)
    out_path = os.path.join(
        OUT_DIR,
        f"_build_Randstad_Declaration_ISO_Default_Judgment_{DECL_TAG}.pdf",
    )
    d = PleadingPaper(
        out_path,
        doc_title_footer=(
            "DECLARATION ISO DEFAULT JUDGMENT -- "
            "NEWANFORBI v. RANDSTAD US, LLC, ET AL."
        ),
    )
    party_block(d)
    right = [
        (f"Case No. {CASE_NO}", False, False),
        ("", False, False),
        ("DECLARATION OF BRENDAN NGEHSI", True, False),
        ("NEWANFORBI IN SUPPORT OF", True, False),
        ("REQUEST FOR DEFAULT JUDGMENT", True, False),
        ("BY COURT AS TO RANDSTAD US, LLC", True, False),
        ("(Cal. Rules of Court, rule 3.1800;", False, False),
        ("Code Civ. Proc. sections 579,", False, False),
        ("585(b), 585(d))", False, False),
        ("", False, False),
        ("Assigned: Hon. Thomas Weathers,", False, False),
        ("Dept. 20", False, False),
        ("CMC: December 17, 2026", False, False),
        (f"[Date Executed: {EXEC_DATE}]", False, False),
    ]
    d.draw_caption_block(caption_left(), right, caption_size=9, tight_lh=12, boxed=True)
    d.blank_line()
    render_content(d, declaration_content())
    d.save()
    print(f"Generated: {out_path}")
    return out_path


def main() -> None:
    if not os.path.isfile(SIGNATURE_IMG) and not NO_SIGNATURE:
        raise SystemExit(f"Missing signature image: {SIGNATURE_IMG}")
    build_declaration()


if __name__ == "__main__":
    main()
