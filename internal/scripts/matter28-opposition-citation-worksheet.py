# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
Matter 28 -- Citation verification RECORD for the MTD opposition.

  python3 internal/scripts/matter28-opposition-citation-worksheet.py

Standalone letter-size PDF: every authority cited in Plaintiff's Opposition to
the Smith/HOPE Motion to Dismiss, with the pin(s) used, the proposition it is
cited for, the section, and the Westlaw KeyCite disposition recorded on
2026-09-21 (flag + verdict + one-line note). A self-documenting record of how
each cite was cleared under Standing Order E.4. NOT a court filing.
"""

from __future__ import annotations

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
OUT_PATHS = [
    REPO_ROOT / "internal" / "public" / "documents" / "matter-28"
    / "Opposition to MTD - Citation Verification Record.pdf",
    Path(
        "/tmp/claude-0/-home-user-interactive-litigation-portfolio/"
        "3fd8a963-2d26-598c-823f-b47c1b152f34/scratchpad/"
        "Opposition-MTD-Citation-Verification-Record.pdf"
    ),
]

# KeyCite flag colors
RED = colors.HexColor("#8a0000")
AMBER = colors.HexColor("#8a4b00")
GREEN = colors.HexColor("#0b6b3a")

# (authority, pin(s), cited-for, section, flag_color, flag_label, verdict + one-line KeyCite note)
CASES = [
    ("Arizona Students' Ass'n v. Arizona Bd. of Regents, 824 F.3d 858 (9th Cir. 2016)", "867",
     "First Amendment retaliation elements.", "C", AMBER, "Yellow",
     "KEEP-WATCH. Pin 867 supports; 5 distinguishing refs, all collateral."),
    ("Ashcroft v. Iqbal, 556 U.S. 662 (2009)", "678",
     "Rule 12(b)(6) plausibility.", "IV", AMBER, "Yellow",
     "KEEP-WATCH. Canonical plausibility rule; negative refs dicta/state-law, collateral."),
    ("Berri v. Superior Court, 43 Cal. 2d 856 (1955)", "860",
     "Demurrer order not appealable / not a judgment.", "A.1", AMBER, "Yellow",
     "KEEP-WATCH. Pin 860 supports; distinguishing refs collateral."),
    ("Boeken v. Philip Morris USA, Inc., 48 Cal. 4th 788 (2010)", "797",
     "Claim-preclusion elements.", "A", AMBER, "Yellow",
     "KEEP-WATCH. Pin 797 supports; treatments concern different facts."),
    ("Caviness v. Horizon Cmty. Learning Ctr., Inc., 590 F.3d 806 (9th Cir. 2010)", "812, 816",
     "State action is conduct-specific.", "B.1-2", AMBER, "Yellow",
     "KEEP-WATCH. Pins 812/816 support; 3 distinguishing (education) refs collateral."),
    ("Cedric Kushner Promotions, Ltd. v. King, 533 U.S. 158 (2001)", "163",
     "RICO person/enterprise distinctness.", "G", AMBER, "Yellow",
     "KEEP-WATCH. Pin 163 distinctness supported; refs collateral."),
    ("DKN Holdings LLC v. Faerber, 61 Cal. 4th 813 (2015)", "824-26",
     "Claim/issue preclusion + privity.", "A", AMBER, "Yellow",
     "KEEP-WATCH. Pins 824-26 support; one declined-extension collateral."),
    ("Drawsand v. F.F. Props., L.L.P., 866 F. Supp. 2d 1110 (N.D. Cal. 2011)", "1127",
     "Privity / course-and-scope.", "A.3", GREEN, "None",
     "KEEP. No negative flag. Pin 1127 confirmed; motion's \"1227\" is wrong."),
    ("Erickson v. Pardus, 551 U.S. 89 (2007)", "94",
     "Pro se liberal construction.", "IV", AMBER, "Yellow",
     "KEEP-WATCH. Pin 94 supports; negative refs state-law/procedural, collateral."),
    ("Florer v. Congregation Pidyon Shevuyim, N.A., 639 F.3d 916 (9th Cir. 2011)", "923-26",
     "Distinguished: chaplain; no joint action.", "B.2", AMBER, "Yellow",
     "KEEP-WATCH. Pins 923-26 support; 4 prison/religion refs collateral."),
    ("Franklin v. Fox, 312 F.3d 423 (9th Cir. 2002)", "445",
     "Willful joint participation (now cited as see also).", "B", AMBER, "Yellow",
     "DEMOTED to see-also (Rawson leads). Overruled in part on OTHER grounds by "
     "Pearson v. Callahan (QI sequencing); joint-action holding at 445 intact."),
    ("Goddard v. Sec. Title Ins. & Guar. Co., 14 Cal. 2d 47 (1939)", "52-53",
     "Demurrer merits vs. curable defect.", "A.2", AMBER, "Yellow",
     "KEEP-WATCH. Pins 52-53 support; 13 refs distinguish on other settings."),
    ("Greenholtz v. Inmates of Neb. Penal & Corr. Complex, 442 U.S. 1 (1979)", "9",
     "Distinguished: discretionary parole release.", "D", AMBER, "Yellow",
     "KEEP-WATCH. Cited to distinguish; pin 9 distinction supported."),
    ("Heath v. Cleary, 708 F.2d 1376 (9th Cir. 1983)", "1380 & n.4",
     "Nonexhaustion disposition doesn't decide federal claims.", "A.2", AMBER, "Yellow",
     "KEEP-WATCH. Pin 1380 & n.4 support; one collateral distinction."),
    ("Hishon v. King & Spalding, 467 U.S. 69 (1984)", "73",
     "Accept allegations as true.", "IV", AMBER, "Yellow",
     "KEEP-WATCH. Pin 73 supports; abrogation refs (Title VII) collateral."),
    ("Kearns v. Ford Motor Co., 567 F.3d 1120 (9th Cir. 2009)", "1124",
     "Rule 9(b) who/what/when.", "F", AMBER, "Yellow",
     "KEEP-WATCH. Pin 1124 supports; negative refs statute-specific."),
    ("Khoja v. Orexigen Therapeutics, Inc., 899 F.3d 988 (9th Cir. 2018)", "999",
     "Scope of judicial notice.", "IV", AMBER, "Yellow",
     "KEEP-WATCH. Pin 999 supports; declined-extension refs collateral."),
    ("Logan v. Zimmerman Brush Co., 455 U.S. 422 (1982)", "436",
     "Established-procedure deprivation -> process due.", "D", AMBER, "Yellow",
     "KEEP-WATCH. Pin 436 supports; treatments collateral, no bite."),
    ("Lopez v. Smith, 203 F.3d 1122 (9th Cir. 2000) (en banc)", "1130-31",
     "Leave to amend for pro se.", "IV, H", RED, "Red",
     "KEEP + co-anchored w/ Fed. R. Civ. P. 15(a)(2). Pin 1130-31 supports; red "
     "flag = later PLRA/pro se leave-to-amend LIMITS, not the core holding."),
    ("Neal v. Shimoda, 131 F.3d 818 (9th Cir. 1997)", "830",
     "Liberty interest: label + mandatory treatment.", "D", AMBER, "Yellow",
     "KEEP (be ready). Pin 830 supports; on-point disagreement (Garcia = burden "
     "of proof, which Neal left open) + distinctions -- holding intact."),
    ("Patsy v. Bd. of Regents, 457 U.S. 496 (1982)", "516",
     "No exhaustion prerequisite for Section 1983.", "A.2, D", AMBER, "Yellow",
     "KEEP-WATCH. Pin 516 supports; abrogation refs context-specific."),
    ("Perez v. City of San Bruno, 27 Cal. 3d 875 (1980)", "882-83",
     "Prematurity is not a merits adjudication.", "A.2", AMBER, "Yellow",
     "KEEP-WATCH. Pins 882-83 support; later treatment small-claims/statutory."),
    ("Rawson v. Recovery Innovations, Inc., 975 F.3d 742 (9th Cir. 2020)", "747-48, 753-54",
     "Integration into state process -> state action (now the lead cite).", "B", AMBER, "Yellow",
     "KEEP (promoted to lead). Pins support; 7 distinguishing refs collateral; "
     "cert. denied Oct. 4, 2021."),
    ("Schreiber Distrib. Co. v. Serv-Well Furniture Co., 806 F.2d 1393 (9th Cir. 1986)", "1400-01",
     "Reversed RICO dismissal; leave to amend.", "G", AMBER, "Yellow",
     "KEEP. 1986 confirmed (motion's \"2004\" wrong); pins 1400-01 support; "
     "disagreement nonbinding."),
    ("Scott v. Kuhlmann, 746 F.2d 1377 (9th Cir. 1984) (per curiam)", "1378",
     "Preclusion-on-pleadings exception + officer privity.", "IV, A.3", AMBER, "Yellow",
     "KEEP (sentence tightened). Pin 1378 supports the narrow no-disputed-facts "
     "exception + gov-officer privity; broad pleading-std claim qualified."),
    ("Valvo v. Univ. of S. Cal., 67 Cal. App. 3d 887 (1977)", "892 n.3",
     "Demurrer not res judicata until judgment.", "A.1", AMBER, "Yellow",
     "KEEP-WATCH. Pin 892 n.3 supports; 4 distinguishing refs collateral."),
    ("West v. Atkins, 487 U.S. 42 (1988)", "54-57",
     "Contractor providing state-obligated care = state actor.", "B.3", AMBER, "Yellow",
     "KEEP-WATCH. Pins 54-57 (core SCOTUS holding) intact; a D. Kan. "
     "\"overruling recognized\" ref cannot reach it."),
    ("Zinermon v. Burch, 494 U.S. 113 (1990)", "132-39",
     "Foreseeable deprivation; predeprivation process.", "D", AMBER, "Yellow",
     "KEEP-WATCH. Pins 132-39 support; 74 refs collateral, no direct history."),
]

STATUTES = [
    ("18 U.S.C. § 1961(1)", "RICO predicate list (§ 1519 not among them).", "G, H"),
    ("18 U.S.C. § 1519", "Obstruction -- NOT a RICO predicate (withdrawn).", "G, H"),
    ("Cal. Civ. Code § 52.1 (incl. § 52.1(b))", "Bane Act; $25k penalty public-enforcement only (not sought).", "E"),
    ("Cal. Code Civ. Proc. § 581d", "Dismissal must be entered as a judgment.", "A.1"),
    ("Cal. Penal Code § 3008(d)(2)", "Duration set by certified professional.", "III, B, D"),
    ("15 Cal. Code Regs. § 3574(f)(1)", "Good cause + signed Form 3043.", "III, B, D"),
    ("Fed. R. Civ. P. 9(b)", "Fraud particularity.", "F, G"),
    ("Fed. R. Civ. P. 12(b)(6)", "Failure to state a claim.", "IV"),
    ("Fed. R. Civ. P. 15(a)(2)", "Leave to amend freely given (added; co-anchor for Lopez).", "IV, H"),
]


def build():
    styles = getSampleStyleSheet()
    cell = ParagraphStyle("cell", parent=styles["Normal"], fontName="Times-Roman",
                          fontSize=8.2, leading=10.0, alignment=TA_LEFT)
    head = ParagraphStyle("head", parent=styles["Normal"], fontName="Times-Bold",
                          fontSize=8.2, leading=10.0, textColor=colors.white)
    title = ParagraphStyle("title", parent=styles["Title"], fontName="Times-Bold", fontSize=14)
    sub = ParagraphStyle("sub", parent=styles["Normal"], fontName="Times-Roman", fontSize=9, leading=12)
    sech = ParagraphStyle("sech", parent=styles["Heading2"], fontName="Times-Bold", fontSize=11)

    def case_rows():
        header = [Paragraph(h, head) for h in
                  ["✓", "Case & pin(s)", "Cited for", "§", "KeyCite disposition (2026-09-21)"]]
        out = [header]
        for auth, pin, prop, sec, fcolor, flabel, note in CASES:
            name = auth.split(",")[0]
            rest = auth[len(name) + 1:]
            auth_p = Paragraph(f"<i>{name}</i>,{rest}  <b>pin {pin}</b>", cell)
            flag_style = ParagraphStyle("kc", parent=cell, fontName="Times-Bold", textColor=fcolor)
            kc = Paragraph(f"<b>[{flabel}]</b> {note}", flag_style)
            out.append([
                Paragraph("&#9745;", cell),  # checked box -- verified
                auth_p,
                Paragraph(prop, cell),
                Paragraph("§ " + sec, cell),
                kc,
            ])
        return out

    def statute_rows():
        header = [Paragraph(h, head) for h in ["Authority", "Cited for", "§", "KeyCite"]]
        out = [header]
        for auth, prop, sec in STATUTES:
            out.append([
                Paragraph(f"<b>{auth}</b>", cell),
                Paragraph(prop, cell),
                Paragraph("§ " + sec, cell),
                Paragraph("N/A (text)", cell),
            ])
        return out

    case_w = [0.22 * inch, 2.15 * inch, 1.5 * inch, 0.42 * inch, 3.06 * inch]
    stat_w = [2.3 * inch, 3.05 * inch, 1.05 * inch, 0.95 * inch]

    def styled(tbl_data, widths):
        t = Table(tbl_data, colWidths=widths, repeatRows=1)
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#333333")),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#999999")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f2f2f2")]),
            ("TOPPADDING", (0, 0), (-1, -1), 2.5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
            ("LEFTPADDING", (0, 0), (-1, -1), 3.5),
            ("RIGHTPADDING", (0, 0), (-1, -1), 3.5),
        ]))
        return t

    story = [
        Paragraph("Citation Verification Record", title),
        Paragraph("Plaintiff's Opposition to Defendants' Motion to Dismiss &mdash; "
                  "<i>Newanforbi v. Smith</i>, N.D. Cal. No. 3:26-cv-07504-LJC.", sub),
        Paragraph("<b>Verified via Westlaw KeyCite on 2026-09-21</b> (San Diego Law Library RPA). "
                  "All 28 cases exist; every pin supports its cited proposition; the <i>Schreiber</i> "
                  "(1986, not 2004) and <i>Drawsand</i> (pin 1127, not 1227) corrections are confirmed. "
                  "No fabrications. ☑ = cleared to file. Flags: <b>[None]</b> no negative treatment; "
                  "<b>[Yellow]</b> some negative treatment (here collateral / distinguishable unless "
                  "noted); <b>[Red]</b> reviewed and co-anchored. Post-verification edits are noted in "
                  "the disposition column.", sub),
        Spacer(1, 8),
        Paragraph("Cases (28) &mdash; all cleared", sech),
        styled(case_rows(), case_w),
        Spacer(1, 10),
        Paragraph("Statutes &amp; Rules (9)", sech),
        styled(statute_rows(), stat_w),
        Spacer(1, 8),
        Paragraph("Post-verification actions taken: (1) <i>Lopez</i> co-anchored with Fed. R. Civ. P. "
                  "15(a)(2) [secs. IV, H]; (2) <i>Rawson</i> promoted to lead the joint-action point, "
                  "<i>Franklin</i> demoted to see-also [sec. B]; (3) <i>Scott v. Kuhlmann</i> sentence "
                  "tightened to the narrow no-disputed-facts exception [sec. IV]. <i>Franklin</i>'s "
                  "partial overruling is on other grounds (<i>Pearson v. Callahan</i>, QI sequencing) "
                  "and does not touch the color-of-law holding at 445. <i>Neal</i> retained; be ready "
                  "for on-point distinguishing authority at argument.", sub),
    ]
    return story


def main():
    for out in OUT_PATHS:
        out.parent.mkdir(parents=True, exist_ok=True)
        SimpleDocTemplate(
            str(out), pagesize=letter,
            leftMargin=0.5 * inch, rightMargin=0.5 * inch,
            topMargin=0.55 * inch, bottomMargin=0.5 * inch,
            title="Matter 28 Opposition -- Citation Verification Record",
        ).build(build())
        print(f"Wrote {out} ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
