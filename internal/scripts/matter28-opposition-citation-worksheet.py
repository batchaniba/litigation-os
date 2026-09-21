# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
Matter 28 -- Citation verification worksheet for the MTD opposition.

  python3 internal/scripts/matter28-opposition-citation-worksheet.py

Standalone letter-size PDF listing every authority cited in Plaintiff's
Opposition to the Smith/HOPE Motion to Dismiss, with the pin(s) actually
used, the proposition it is cited for, the section location, and a
verification flag -- so each can be pulled and confirmed on Westlaw.
NOT a court filing; a work tool.
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
    / "Opposition to MTD - Citation Verification Worksheet.pdf",
    Path(
        "/tmp/claude-0/-home-user-interactive-litigation-portfolio/"
        "3fd8a963-2d26-598c-823f-b47c1b152f34/scratchpad/"
        "Opposition-MTD-Citation-Worksheet.pdf"
    ),
]

# flag -> (label, color)
SAFE = "SAFE"
MOVANT = "MOVANT CITE"
VERIFY = "VERIFY PIN"
NEW = "NEW -- VERIFY"

# (authority, pin(s) used, cited-for, section, flag)
CASES = [
    ("Arizona Students' Ass'n v. Arizona Bd. of Regents, 824 F.3d 858 (9th Cir. 2016)", "867",
     "First Amendment retaliation elements (protected activity; chill; causation).", "C", MOVANT),
    ("Ashcroft v. Iqbal, 556 U.S. 662 (2009)", "678",
     "Rule 12(b)(6) plausibility standard.", "IV", SAFE),
    ("Berri v. Superior Court, 43 Cal. 2d 856 (1955)", "860",
     "Order sustaining a demurrer is not appealable because it is not the final judgment.", "A.1", SAFE),
    ("Boeken v. Philip Morris USA, Inc., 48 Cal. 4th 788 (2010)", "797",
     "Elements of California claim preclusion.", "A", MOVANT),
    ("Caviness v. Horizon Cmty. Learning Ctr., Inc., 590 F.3d 806 (9th Cir. 2010)", "812, 816",
     "State-action inquiry is conduct-specific, not status-based.", "B.1-2", MOVANT),
    ("Cedric Kushner Promotions, Ltd. v. King, 533 U.S. 158 (2001)", "163",
     "RICO person/enterprise distinctness (natural person vs. corporation).", "G", SAFE),
    ("DKN Holdings LLC v. Faerber, 61 Cal. 4th 813 (2015)", "824-26",
     "Claim/issue preclusion elements; privity requires community of interest + adequate representation.", "A", SAFE),
    ("Drawsand v. F.F. Props., L.L.P., 866 F. Supp. 2d 1110 (N.D. Cal. 2011)", "1127",
     "Privity / course-and-scope (motion miscites this as \"1227\").", "A.3", VERIFY),
    ("Erickson v. Pardus, 551 U.S. 89 (2007)", "94",
     "Pro se pleadings liberally construed.", "IV", SAFE),
    ("Florer v. Congregation Pidyon Shevuyim, N.A., 639 F.3d 916 (9th Cir. 2011)", "923-26",
     "Distinguished: chaplain's ecclesiastical decision; no joint action by the State.", "B.2", MOVANT),
    ("Franklin v. Fox, 312 F.3d 423 (9th Cir. 2002)", "445",
     "Willful participant in joint action acts under color of state law.", "B", MOVANT),
    ("Goddard v. Sec. Title Ins. & Guar. Co., 14 Cal. 2d 47 (1939)", "52-53",
     "A general-demurrer judgment is not on the merits where the defect is formal/curable.", "A.2", SAFE),
    ("Greenholtz v. Inmates of Neb. Penal & Corr. Complex, 442 U.S. 1 (1979)", "9",
     "Distinguished: concerns discretionary parole release, not the Neal liberty interest.", "D", MOVANT),
    ("Heath v. Cleary, 708 F.2d 1376 (9th Cir. 1983)", "1380 & n.4",
     "Prior state disposition on nonexhaustion did not decide the federal claims.", "A.2", VERIFY),
    ("Hishon v. King & Spalding, 467 U.S. 69 (1984)", "73",
     "Court accepts well-pleaded allegations as true.", "IV", MOVANT),
    ("Kearns v. Ford Motor Co., 567 F.3d 1120 (9th Cir. 2009)", "1124",
     "Rule 9(b) who/what/when/where/how.", "F", MOVANT),
    ("Khoja v. Orexigen Therapeutics, Inc., 899 F.3d 988 (9th Cir. 2018)", "999",
     "Judicial notice reaches existence/legal effect, not truth of contents.", "IV", SAFE),
    ("Logan v. Zimmerman Brush Co., 455 U.S. 422 (1982)", "436",
     "Deprivation through an established state procedure requires predeprivation process.", "D", NEW),
    ("Lopez v. Smith, 203 F.3d 1122 (9th Cir. 2000) (en banc)", "1130-31",
     "Leave to amend granted unless it is clear defects cannot be cured.", "IV, H", SAFE),
    ("Neal v. Shimoda, 131 F.3d 818 (9th Cir. 1997)", "830",
     "Liberty interest in avoiding sex-offender label + mandatory treatment gating parole.", "D", VERIFY),
    ("Patsy v. Bd. of Regents, 457 U.S. 496 (1982)", "516",
     "Exhaustion of state administrative remedies is not a prerequisite to a Section 1983 action.", "A.2, D", SAFE),
    ("Perez v. City of San Bruno, 27 Cal. 3d 875 (1980)", "882-83",
     "Dismissal on prematurity / unmet precondition is not a merits adjudication.", "A.2", SAFE),
    ("Rawson v. Recovery Innovations, Inc., 975 F.3d 742 (9th Cir. 2020) (cert. denied Oct. 4, 2021)", "747-48, 753-54",
     "Integration into a State process can make private conduct state action; discretion not dispositive.", "B", MOVANT),
    ("Schreiber Distrib. Co. v. Serv-Well Furniture Co., 806 F.2d 1393 (9th Cir. 1986)", "1400-01",
     "Reversed RICO dismissal; leave to amend (motion miscites the year as \"2004\").", "G", SAFE),
    ("Scott v. Kuhlmann, 746 F.2d 1377 (9th Cir. 1984) (per curiam)", "1378",
     "Cited for BOTH the preclusion-on-the-pleadings standard AND privity among gov't officers -- confirm it supports the pleading-standard proposition (it reads as a privity case).", "IV, A.3", VERIFY),
    ("Valvo v. Univ. of S. Cal., 67 Cal. App. 3d 887 (1977)", "892 n.3",
     "Until entry of judgment, a demurrer ruling is not res judicata.", "A.1", VERIFY),
    ("West v. Atkins, 487 U.S. 42 (1988)", "54-57",
     "Private contractor furnishing care the State is obligated to provide acts under color of law.", "B.3", SAFE),
    ("Zinermon v. Burch, 494 U.S. 113 (1990)", "132-39",
     "Postdeprivation remedy insufficient where deprivation is foreseeable and predeprivation safeguards practicable.", "D", NEW),
]

STATUTES = [
    ("18 U.S.C. § 1961(1)", "--", "RICO predicate-offense list (§ 1519 is not among them).", "G, H", SAFE),
    ("18 U.S.C. § 1519", "--", "Obstruction -- NOT a listed RICO predicate (reliance withdrawn).", "G, H", SAFE),
    ("Cal. Civ. Code § 52.1 (incl. § 52.1(b))", "--", "Bane Act; the $25,000 penalty is reserved to public enforcement (not sought).", "E", SAFE),
    ("Cal. Code Civ. Proc. § 581d", "--", "A dismissal must be entered in writing as a judgment.", "A.1", SAFE),
    ("Cal. Penal Code § 3008(d)(2)", "--", "Treatment duration determined by the certified professional in consultation with the parole officer.", "III, B, D", SAFE),
    ("15 Cal. Code Regs. § 3574(f)(1)", "--", "Retention requires good cause + a Form 3043 signed by provider and parole agent.", "III, B, D", SAFE),
    ("Fed. R. Civ. P. 9(b)", "--", "Particularity for fraud.", "F, G", SAFE),
    ("Fed. R. Civ. P. 12(b)(6)", "--", "Failure to state a claim.", "IV", SAFE),
]


def build():
    styles = getSampleStyleSheet()
    cell = ParagraphStyle("cell", parent=styles["Normal"], fontName="Times-Roman",
                          fontSize=8.5, leading=10.5, alignment=TA_LEFT)
    cell_i = ParagraphStyle("celli", parent=cell, fontName="Times-Italic")
    head = ParagraphStyle("head", parent=styles["Normal"], fontName="Times-Bold",
                          fontSize=8.5, leading=10.5, textColor=colors.white)
    title = ParagraphStyle("title", parent=styles["Title"], fontName="Times-Bold", fontSize=14)
    sub = ParagraphStyle("sub", parent=styles["Normal"], fontName="Times-Roman", fontSize=9, leading=12)
    sech = ParagraphStyle("sech", parent=styles["Heading2"], fontName="Times-Bold", fontSize=11)

    def flag_para(f):
        color = {SAFE: colors.HexColor("#0b6b3a"), MOVANT: colors.HexColor("#1f4e79"),
                 VERIFY: colors.HexColor("#8a4b00"), NEW: colors.HexColor("#8a0000")}[f]
        st = ParagraphStyle("flag", parent=cell, fontName="Times-Bold", textColor=color)
        return Paragraph(f, st)

    def rows(data, kind):
        header = [Paragraph(h, head) for h in
                  ["#", f"{kind} & pin(s) used", "Cited for (proposition)", "§", "Status", "Ver."]]
        out = [header]
        for i, (auth, pin, prop, sec, flag) in enumerate(data, 1):
            # italicize the case name up to the first comma-reporter for cases
            auth_p = Paragraph(
                f"<i>{auth.split(',')[0]}</i>," + auth[len(auth.split(',')[0]) + 1:]
                + (f"  <b>pin {pin}</b>" if pin != "--" else ""),
                cell,
            ) if kind == "Case" else Paragraph(f"<b>{auth}</b>", cell)
            out.append([
                Paragraph(str(i), cell),
                auth_p,
                Paragraph(prop, cell),
                Paragraph("§ " + sec, cell),
                flag_para(flag),
                Paragraph("&#9633;", cell),
            ])
        return out

    col_w = [0.28 * inch, 2.75 * inch, 2.35 * inch, 0.55 * inch, 0.95 * inch, 0.32 * inch]

    def styled(tbl_data):
        t = Table(tbl_data, colWidths=col_w, repeatRows=1)
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#333333")),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#999999")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f2f2f2")]),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ("LEFTPADDING", (0, 0), (-1, -1), 4),
            ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ]))
        return t

    story = [
        Paragraph("Citation Verification Worksheet", title),
        Paragraph("Plaintiff's Opposition to Defendants' Motion to Dismiss &mdash; "
                  "<i>Newanforbi v. Smith</i>, N.D. Cal. No. 3:26-cv-07504-LJC "
                  "(opposition dated Sept. 21, 2026).", sub),
        Spacer(1, 4),
        Paragraph("Pull each authority on Westlaw, confirm the case exists and the caption/reporter "
                  "match, read the cited pin, and check the \"Ver.\" box. Status legend: "
                  "<b>SAFE</b> = verified in the portfolio corpus; <b>MOVANT CITE</b> = defendants' own "
                  "authority, turned (confirm we characterize it fairly); <b>VERIFY PIN</b> = pin/attribution "
                  "flagged, confirm before filing; <b>NEW -- VERIFY</b> = not previously vetted, confirm "
                  "existence + pin + proposition. Standing Order &sect; E.4 makes unverified citations "
                  "sanctionable.", sub),
        Spacer(1, 8),
        Paragraph("Cases (28)", sech),
        styled(rows(CASES, "Case")),
        Spacer(1, 10),
        Paragraph("Statutes &amp; Rules (8)", sech),
        styled(rows(STATUTES, "Authority")),
        Spacer(1, 8),
        Paragraph("Priority to verify first: <i>Zinermon</i> 132&ndash;39, <i>Logan</i> 436 (new); "
                  "<i>Scott v. Kuhlmann</i> pleading-standard attribution; <i>Caviness</i> 812, "
                  "<i>Drawsand</i> 1127, <i>Rawson</i> 753&ndash;54, <i>Florer</i> 923&ndash;26, "
                  "<i>Heath</i> n.4, <i>Neal</i> 830, <i>Valvo</i> 892 n.3.", sub),
    ]
    return story


def main():
    story = build()
    for out in OUT_PATHS:
        out.parent.mkdir(parents=True, exist_ok=True)
        doc = SimpleDocTemplate(
            str(out), pagesize=letter,
            leftMargin=0.5 * inch, rightMargin=0.5 * inch,
            topMargin=0.55 * inch, bottomMargin=0.5 * inch,
            title="Matter 28 Opposition -- Citation Verification Worksheet",
        )
        doc.build(build())
        print(f"Wrote {out} ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
