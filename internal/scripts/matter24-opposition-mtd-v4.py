# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
Matter 24 - Plaintiff's Opposition to Serrato MTD / Motion to Strike (v4).

Retaliation-first revision:
  - Accept Krishnan Dkt. 5 + Fickes posture: Serrato retains certification discretion
  - Lead merits with First Amendment retaliation (Ford / Perry / Umbehr)
  - Keep PDP/SDP as secondary; no compel-certification ask in the Opp
  - Whittlestone; Fickes distinguish; QI; leave-to-amend hedges

  python3 internal/scripts/matter24-opposition-mtd-v4.py
"""

from __future__ import annotations

from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml.ns import qn
from docx.shared import Inches, Pt

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent.parent
OUT_DOCX = REPO_ROOT / "Opposition to MTD v4.docx"
OUT_MATTER24 = (
    REPO_ROOT
    / "internal"
    / "public"
    / "documents"
    / "matter-24"
    / "Opposition to Serrato MTD FAC and Strike v4 (Sep 2 2026).docx"
)
SIG_IMG = SCRIPT_DIR / "assets" / "newanforbi-pen-signature.png"

FONT = "Times New Roman"
SIZE = Pt(12)


def set_run(run, *, bold=False, italic=False, size=SIZE):
    run.font.name = FONT
    run._element.rPr.rFonts.set(qn("w:eastAsia"), FONT)
    run.font.size = size
    run.bold = bold
    run.italic = italic


def add_para(
    doc,
    text="",
    *,
    bold=False,
    italic=False,
    center=False,
    double=True,
    space_after=0,
    first_indent=None,
    left_indent=None,
):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(0)
    pf.space_after = Pt(space_after)
    if double:
        pf.line_spacing_rule = WD_LINE_SPACING.DOUBLE
    else:
        pf.line_spacing = 1.0
        pf.line_spacing_rule = WD_LINE_SPACING.SINGLE
    if center:
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    if first_indent is not None:
        pf.first_line_indent = first_indent
    if left_indent is not None:
        pf.left_indent = left_indent
    if text:
        run = p.add_run(text)
        set_run(run, bold=bold, italic=italic)
    return p


def add_mixed(doc, parts, *, double=True, first_indent=None, left_indent=None, center=False):
    """parts: list of (text, bold, italic)"""
    p = add_para(
        doc,
        "",
        double=double,
        first_indent=first_indent,
        left_indent=left_indent,
        center=center,
    )
    for text, bold, italic in parts:
        run = p.add_run(text)
        set_run(run, bold=bold, italic=italic)
    return p


def add_footnote_para(doc, marker: str, text: str):
    p = add_para(doc, "", double=True, first_indent=Inches(0.5))
    run = p.add_run(marker)
    set_run(run, bold=True, size=Pt(10))
    run = p.add_run(" " + text)
    set_run(run, size=Pt(10))
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    return p


def heading(doc, text):
    return add_para(doc, text, bold=True, center=False, double=True)


def subhead(doc, text):
    return add_para(doc, text, bold=True, double=True)


def body(doc, text, *, indent=True):
    return add_para(
        doc,
        text,
        double=True,
        first_indent=Inches(0.5) if indent else None,
    )


def cite_body(doc, lead, case_italic, rest):
    """lead + italicized case + rest, first-line indented."""
    return add_mixed(
        doc,
        [(lead, False, False), (case_italic, False, True), (rest, False, False)],
        first_indent=Inches(0.5),
    )


def build():
    doc = Document()
    section = doc.sections[0]
    section.page_width = Inches(8.5)
    section.page_height = Inches(11)
    for edge in ("left_margin", "right_margin", "top_margin", "bottom_margin"):
        setattr(section, edge, Inches(1.0))

    # ---- Caption block (single spaced) ----
    for line, bold in [
        ("BRENDAN NGEHSI NEWANFORBI", True),
        ("Plaintiff, In Pro Per", False),
        ("1455 Cat Tail Drive", False),
        ("Stockton, CA 95204", False),
        ("Telephone: (209) 801-4442", False),
        ("E-mail: bnn.cdl@gmail.com", False),
    ]:
        add_para(doc, line, bold=bold, double=False)

    add_para(doc, "", double=True)
    add_para(doc, "UNITED STATES DISTRICT COURT", bold=True, center=True, double=True)
    add_para(doc, "NORTHERN DISTRICT OF CALIFORNIA", bold=True, center=True, double=True)
    add_para(doc, "", double=True)

    for line, bold in [
        ("BRENDAN NGEHSI NEWANFORBI,", True),
        ("\t\tPlaintiff,", False),
        ("v.", False),
        ("CAPTAIN G. SERRATO, in his individual", False),
        ("and official capacities as Commander,", False),
        ("Dublin Area, California Highway Patrol,", False),
        ("\t\tDefendant.", False),
    ]:
        add_para(doc, line, bold=bold, double=False)

    add_para(doc, "", double=True)
    add_para(doc, "Case No. 4:26-cv-05953-ASK", bold=True, double=False)
    add_para(doc, "", double=True)
    add_para(
        doc,
        "PLAINTIFF'S OPPOSITION TO DEFENDANT'S MOTION TO DISMISS FIRST AMENDED "
        "COMPLAINT AND/OR MOTION TO STRIKE PORTIONS OF THE FIRST AMENDED COMPLAINT",
        bold=True,
        center=True,
        double=False,
    )
    add_para(doc, "", double=True)
    for line in [
        "Date: September 16, 2026",
        "Time: 1:30 p.m.",
        "Judge: Magistrate Judge Honorable Ajay S. Krishnan",
    ]:
        add_para(doc, line, double=False)
    add_para(doc, "", double=True)

    # ---- TOC ----
    add_para(doc, "TABLE OF CONTENTS", bold=True, center=True, double=True)
    add_para(doc, "", double=True)
    toc = [
        "I.\tINTRODUCTION",
        "II.\tSTANDARD OF REVIEW",
        "III.\tARGUMENT",
        "\tA.\tDefendant's Rule 12(f) Motions to Strike Are Improper Under Whittlestone",
        "\tB.\tThe First Amendment Retaliation Claim Is Well-Pleaded",
        "\tC.\tThe Procedural Due Process Claim Is Well-Pleaded",
        "\tD.\tThe Substantive Due Process Claim Is Well-Pleaded",
        "\tE.\tDeclaratory and Injunctive Relief Are Proper",
        "\tF.\tThe Related-Case Narrative Does Not Defeat the FAC",
        "\tG.\tQualified Immunity Does Not Apply",
        "\tH.\tLeave to Amend Must Be Granted",
        "IV.\tCONCLUSION",
    ]
    for line in toc:
        add_para(doc, line, double=False)
    add_para(doc, "", double=True)

    # ---- TOA ----
    add_para(doc, "TABLE OF AUTHORITIES", bold=True, center=True, double=True)
    add_para(doc, "", double=True)
    add_para(doc, "Cases", bold=True, italic=True, double=False)
    cases = [
        "Ashcroft v. Iqbal, 556 U.S. 662 (2009)",
        "Bd. of Cnty. Comm'rs v. Umbehr, 518 U.S. 668 (1996)",
        "Bd. of Regents v. Roth, 408 U.S. 564 (1972)",
        "Bell Atl. Corp. v. Twombly, 550 U.S. 544 (2007)",
        "Borough of Duryea v. Guarnieri, 564 U.S. 379 (2011)",
        "Bureerong v. Uvawas, 922 F. Supp. 1450 (C.D. Cal. 1996)",
        "Capp v. Cnty. of San Diego, 940 F.3d 1046 (9th Cir. 2019)",
        "Catholic Charities CYO v. Chertoff, 622 F. Supp. 2d 865 (N.D. Cal. 2008)",
        "District of Columbia v. Wesby, 583 U.S. 48 (2018)",
        "Erickson v. Pardus, 551 U.S. 89 (2007)",
        "Ex parte Young, 209 U.S. 123 (1908)",
        "Ford v. City of Yakima, 706 F.3d 1188 (9th Cir. 2013)",
        "Goldberg v. Kelly, 397 U.S. 254 (1970)",
        "Hartman v. Moore, 547 U.S. 250 (2006)",
        "Hebbe v. Pliler, 627 F.3d 338 (9th Cir. 2010)",
        "Hope v. Pelzer, 536 U.S. 730 (2002)",
        "Kay v. Ehrler, 499 U.S. 432 (1991)",
        "Keates v. Koile, 883 F.3d 1228 (9th Cir. 2018)",
        "Khoja v. Orexigen Therapeutics, Inc., 899 F.3d 988 (9th Cir. 2018)",
        "Knievel v. ESPN, 393 F.3d 1068 (9th Cir. 2005)",
        "Lee v. City of Los Angeles, 250 F.3d 668 (9th Cir. 2001)",
        "Lopez v. Smith, 203 F.3d 1122 (9th Cir. 2000) (en banc)",
        "Mathews v. Eldridge, 424 U.S. 319 (1976)",
        "Mt. Healthy City Sch. Dist. Bd. of Educ. v. Doyle, 429 U.S. 274 (1977)",
        "Navarro v. Block, 250 F.3d 729 (9th Cir. 2001)",
        "Nieves v. Bartlett, 587 U.S. 391 (2019)",
        "Noll v. Carlson, 809 F.2d 1446 (9th Cir. 1987)",
        "Pearson v. Callahan, 555 U.S. 223 (2009)",
        "Perez Perez v. Wolf, 943 F.3d 853 (9th Cir. 2019)",
        "Perry v. Sindermann, 408 U.S. 593 (1972)",
        "Pratt v. Rowland, 65 F.3d 802 (9th Cir. 1995)",
        "Smith v. Wade, 461 U.S. 30 (1983)",
        "Whittlestone, Inc. v. Handi-Craft Co., 618 F.3d 970 (9th Cir. 2010)",
        "Wilkerson v. Butler, 229 F.R.D. 166 (E.D. Cal. 2005)",
        "Winter v. Nat. Res. Def. Council, Inc., 555 U.S. 7 (2008)",
        "Withrow v. Larkin, 421 U.S. 35 (1975)",
    ]
    for c in cases:
        add_para(doc, c, double=False)
    add_para(doc, "", double=False)
    add_para(doc, "Statutes and Rules", bold=True, italic=True, double=False)
    for s in [
        "8 U.S.C. § 1101(a)(15)(U)(iii)",
        "28 U.S.C. §§ 2201-2202",
        "42 U.S.C. § 1983",
        "42 U.S.C. § 1988",
        "Cal. Penal Code § 679.10",
        "Fed. R. Civ. P. 12(b)(6), 12(f)",
        "N.D. Cal. Civil L.R. 7-2(a), 7-3(a)",
    ]:
        add_para(doc, s, double=False)
    add_para(doc, "", double=True)

    # ---- I. INTRODUCTION ----
    heading(doc, "I. INTRODUCTION")
    body(
        doc,
        "This Court has already screened Plaintiff's complaint under 28 U.S.C. § 1915 and "
        "held it sufficient. Accepting the pleaded facts as true, the Court found "
        "\"plausible inferences that CHP officers falsely imprisoned [Plaintiff] in "
        "November 2024 based on fabricated evidence\" and that \"Defendant Serrato "
        "retaliated against him by wrongfully denying his certification request.\" "
        "(Dkt. No. 5 at 4.) Critically, the Court also held: \"While Defendant Serrato "
        "had discretion to certify the request, he did not have discretion to retaliate "
        "against Mr. Newanforbi.\" (Id.) Plaintiff accepts that holding. He does not ask "
        "this Court to compel a Form I-918 Supplement B signature. He asks the Court "
        "to deny dismissal of claims that Serrato's April 20, 2026 denial was retaliatory "
        "and that the denial process failed constitutional and statutory minima.",
    )
    body(
        doc,
        "Two judicial determinations already confirm that Plaintiff is not entitled, in "
        "this Section 1983 action, to an order compelling a Form B signature. First, "
        "this Court expressly recognized Serrato's discretion to certify. (Dkt. No. 5 "
        "at 4.) Second, Judge Fickes denied Plaintiff's motion for judicial U-visa "
        "certification in Alameda Superior Court Case No. 26CV168913. Plaintiff "
        "accepts both determinations for purposes of the relief sought here: he does "
        "not ask this Court to force a Supplement B signature. That acceptance is "
        "limited to this federal pleading posture. It does not waive, and is not "
        "intended to waive, Petitioner's position in the pending Alameda writ "
        "proceeding (Case No. 26CV191136) that Penal Code section 679.10 imposes "
        "enforceable state-law duties-including mandatory processing, explanation, and "
        "related ministerial obligations-reviewable by mandate, with vacatur and "
        "remand for a new decision under the correct standards as the principal "
        "remedy. Defendant's motion, however, treats discretion as a license to "
        "retaliate and as a free pass for a boilerplate denial. The Court's prior "
        "screening determination is highly persuasive here: Defendant now attacks "
        "essentially the same factual theory under the same Rule 12(b)(6) plausibility "
        "standard, and the Court has already identified a plausible retaliation "
        "inference on that theory. (Dkt. No. 5 at 3-4.)",
    )
    body(
        doc,
        "Accordingly, this opposition leads with the First Amendment retaliation claim-"
        "the claim this Court already found plausible and the claim least affected by "
        "certification discretion. Perry v. Sindermann, 408 U.S. 593, 597 (1972); "
        "Bd. of Cnty. Comm'rs v. Umbehr, 518 U.S. 668, 674 (1996); Ford v. City of "
        "Yakima, 706 F.3d 1188, 1193 (9th Cir. 2013). The due-process claims are "
        "preserved as secondary theories: not as a demand that Serrato must certify, "
        "but as claims that California Penal Code section 679.10 constrains how a "
        "denial may be reached and explained. Under federal law, the decision whether "
        "to sign remains discretionary. Perez Perez v. Wolf, 943 F.3d 853, 863 (9th "
        "Cir. 2019). Section 679.10 nonetheless uses mandatory language, creates a "
        "rebuttable presumption of helpfulness, requires a written explanation for "
        "denial, mandates timely processing, and prohibits treating the absence of "
        "charges or prosecution as dispositive. Those process constraints-not a right "
        "to a compelled yes-are what the due-process claims put at issue.",
    )
    body(
        doc,
        "Defendant also moves under Rule 12(f) to strike Plaintiff's prayers for "
        "declaratory relief, injunctive relief, attorney fees, and punitive damages. "
        "The Ninth Circuit has held that Rule 12(f) does not authorize striking a claim "
        "for damages on the ground that it is not recoverable as a matter of law. "
        "Whittlestone, Inc. v. Handi-Craft Co., 618 F.3d 970, 974-75 (9th Cir. 2010). "
        "Several of Defendant's grounds fail on that threshold alone.",
    )
    body(
        doc,
        "Finally, Defendant leans on related-case history-including Judge Fickes's "
        "denial, Plaintiff's voluntary dismissals, and an Eastern District report and "
        "recommendation-to argue retaliation is implausible and leave to amend futile. "
        "Even accepting those facts as true, they do not defeat this FAC. A different "
        "certifying official's decision on a different request does not determine "
        "whether Captain Serrato's April 20, 2026 denial-issued while supervising the "
        "accused officers and while those officers were defendants in pending civil "
        "suits-was free of retaliatory motive. This is the only action asserting "
        "Section 1983 claims against Defendant Serrato in his individual capacity for "
        "that denial. And this Court has already held those claims plausible.",
    )
    # footnote on notice
    add_footnote_para(
        doc,
        "1",
        "Plaintiff also notes that the motion was served on August 26, 2026 and noticed "
        "for hearing on September 16, 2026-21 days' notice. Civil L.R. 7-2(a) requires "
        "35 days. Plaintiff opposes on the merits without waiving any objection to the "
        "deficient notice period. The opposition deadline under Civil L.R. 7-3(a) is "
        "September 2, 2026.",
    )

    # ---- II. STANDARD ----
    heading(doc, "II. STANDARD OF REVIEW")
    cite_body(
        doc,
        "A motion to dismiss under Rule 12(b)(6) tests the legal sufficiency of the "
        "complaint. ",
        "Navarro v. Block",
        ", 250 F.3d 729, 732 (9th Cir. 2001). To survive, a complaint must contain "
        "\"sufficient factual matter, accepted as true, to 'state a claim to relief "
        "that is plausible on its face.'\" Ashcroft v. Iqbal, 556 U.S. 662, 678 (2009). "
        "The court must \"accept all factual allegations in the complaint as true and "
        "construe the pleadings in the light most favorable to the nonmoving party.\" "
        "Knievel v. ESPN, 393 F.3d 1068, 1072 (9th Cir. 2005). Where competing "
        "inferences may be drawn from the same set of facts, the complaint survives-"
        "\"even if it strikes a savvy judge that actual proof of the facts alleged is "
        "improbable.\" Bell Atl. Corp. v. Twombly, 550 U.S. 544, 556 (2007).",
    )
    cite_body(
        doc,
        "Pro se pleadings are held \"to less stringent standards than formal pleadings "
        "drafted by lawyers\" and must be construed liberally. ",
        "Erickson v. Pardus",
        ", 551 U.S. 89, 94 (2007); Hebbe v. Pliler, 627 F.3d 338, 342 (9th Cir. 2010). "
        "Dismissal with prejudice is warranted only when it is \"absolutely clear that "
        "the deficiencies of the complaint could not be cured by amendment.\" Lopez v. "
        "Smith, 203 F.3d 1122, 1137 (9th Cir. 2000) (en banc) (quoting Noll v. Carlson, "
        "809 F.2d 1446, 1448 (9th Cir. 1987)). \"[T]he rule favoring liberality in "
        "amendments to pleadings is particularly important for the pro se litigant.\" "
        "Id. at 1131 (quoting Noll, 809 F.2d at 1448).",
    )

    # ---- III. ARGUMENT ----
    heading(doc, "III. ARGUMENT")

    # A. 12(f)
    subhead(
        doc,
        "A. Defendant's Rule 12(f) Motions to Strike Are Improper Under Whittlestone.",
    )
    body(
        doc,
        "Defendant moves under Rule 12(f) to strike Plaintiff's fourth cause of action "
        "and prayers for declaratory relief, injunctive relief, attorney fees, and "
        "punitive damages. (MTD at 12-14.) Each motion fails at the threshold.",
    )
    cite_body(
        doc,
        "In ",
        "Whittlestone, Inc. v. Handi-Craft Co.",
        ", 618 F.3d 970 (9th Cir. 2010), the Ninth Circuit held that Rule 12(f) "
        "\"does not authorize a district court to strike a claim for damages on the "
        "ground that such damages are precluded as a matter of law.\" Id. at 971, "
        "974-75. Rule 12(f) authorizes striking only \"redundant, immaterial, "
        "impertinent, or scandalous\" matter. Id. at 973 (quoting Fed. R. Civ. P. "
        "12(f)). Challenges that test the legal sufficiency of a damages prayer "
        "\"are better suited for a Rule 12(b)(6) motion or a Rule 56 motion, not a "
        "Rule 12(f) motion.\" Id. at 974. Defendant's reliance on Bureerong v. "
        "Uvawas, 922 F. Supp. 1450 (C.D. Cal. 1996), and Wilkerson v. Butler, 229 "
        "F.R.D. 166 (E.D. Cal. 2005), is misplaced. Both predate Whittlestone and "
        "are no longer good law on this point in the Ninth Circuit.",
    )
    body(
        doc,
        "To the extent the Court construes these arguments as part of the Rule 12(b)(6) "
        "motion, they fail on the merits as well.",
    )
    body(
        doc,
        "Punitive damages. The FAC alleges Defendant (a) denied certification despite "
        "possessing the dashcam recording and Detention Certificate proving fabricated "
        "evidence, (b) issued a boilerplate denial engaging with no evidence, and (c) "
        "did so amid a concrete institutional incentive to deny while supervising the "
        "accused officers. (FAC ¶¶ 37, 49.) These allegations plausibly state \"reckless "
        "or callous indifference to the federally protected rights of others.\" Smith v. "
        "Wade, 461 U.S. 30, 56 (1983). That the FAC disclaims relitigating the officers' "
        "underlying tort liability does not erase Serrato's own conduct: refusing to "
        "engage with evidence in his own custody when deciding a certification request "
        "under section 679.10.",
    )
    body(
        doc,
        "Injunctive relief. The FAC alleges an ongoing deprivation of access to the "
        "U-visa process, continuing immigration uncertainty, inability to obtain "
        "employment authorization and removal protections, and dignitary injury from "
        "the unresolved denial. (FAC ¶¶ 39, 44, 51, Prayer ¶¶ E-F.) Those allegations "
        "speak directly to Winter's irreparable-harm and balance-of-equities inquiries. "
        "Winter v. Nat. Res. Def. Council, Inc., 555 U.S. 7, 20 (2008). Whether "
        "Plaintiff ultimately obtains an injunction is a merits question; it is not a "
        "basis to strike the prayer at the pleading stage.",
    )
    body(
        doc,
        "Attorney fees. Plaintiff does not contend he may recover fees for his own "
        "pro se work under Kay v. Ehrler, 499 U.S. 432, 438 (1991). To the extent "
        "counsel is later retained or appointed-including through the Federal Pro Bono "
        "Project referral (Dkt. No. 5 at 5)-the prayer may matter. Either way, Rule "
        "12(f) is not the vehicle to resolve that contingency now.",
    )

    # B. Retaliation (lead merits claim)
    subhead(
        doc,
        "B. The First Amendment Retaliation Claim Is Well-Pleaded.",
    )
    body(
        doc,
        "Defendant's second ground in the Notice is that retaliation fails \"because "
        "Plaintiff was not entitled to U-visa certification as a matter of law.\" "
        "(MTD at 2.) That gets the doctrine backwards-and ignores this Court's "
        "screening holding that Serrato's certification discretion does not include "
        "discretion to retaliate. (Dkt. No. 5 at 4.) \"[E]ven though a person has no "
        "'right' to a valuable governmental benefit and even though the government "
        "may deny him the benefit for any number of reasons, there are some reasons "
        "upon which the government may not rely. It may not deny a benefit to a "
        "person on a basis that infringes his constitutionally protected "
        "interests-especially, his interest in freedom of speech.\" Perry v. "
        "Sindermann, 408 U.S. 593, 597 (1972); see also Bd. of Cnty. Comm'rs v. "
        "Umbehr, 518 U.S. 668, 674 (1996). Discretionary benefits are precisely "
        "where retaliation doctrine operates. Whether Plaintiff had a freestanding "
        "\"right\" to certification is irrelevant to whether Defendant denied it in "
        "retaliation for protected activity.",
    )
    cite_body(
        doc,
        "To state a First Amendment retaliation claim, Plaintiff must allege that he "
        "engaged in protected activity, that Defendant took adverse action that would "
        "chill a person of ordinary firmness, and that Defendant's desire to chill "
        "that speech was a but-for cause of the adverse action. ",
        "Ford v. City of Yakima",
        ", 706 F.3d 1188, 1193 (9th Cir. 2013). At the pleading stage, Plaintiff need "
        "only allege facts making retaliatory but-for causation plausible-not prove "
        "it, and not disprove every innocent explanation. Ashcroft v. Iqbal, 556 U.S. "
        "662, 678 (2009); Capp v. Cnty. of San Diego, 940 F.3d 1046, 1055 (9th Cir. "
        "2019). The Mt. Healthy burden-shift-under which the defendant may show it "
        "would have taken the same action anyway-is an affirmative defense for summary "
        "judgment or trial, not a pleading barrier. Mt. Healthy City Sch. Dist. Bd. of "
        "Educ. v. Doyle, 429 U.S. 274, 287 (1977).",
    )
    body(
        doc,
        "The FAC more than satisfies Ford's but-for standard through five mutually "
        "reinforcing allegations:",
    )
    body(
        doc,
        "Documented knowledge. Defendant's own March 26, 2026 letter expressly "
        "acknowledges Plaintiff's citizen complaint and assigns an investigator. "
        "(FAC ¶ 48.) This is a contemporaneous written admission-not an inference. "
        "Defendant's response-that assigning an investigator is proper-misses the "
        "point. The letter proves knowledge of protected activity before the denial. "
        "Knowledge plus adverse action in close proximity is classic retaliation "
        "circumstantial evidence.",
    )
    body(
        doc,
        "Tight temporal proximity. POST forwarded the complaint on March 23. Serrato "
        "assigned an investigator on March 26. Plaintiff submitted the certification "
        "request on April 9. Serrato denied it on April 20-eleven days later-without "
        "substantive analysis. (FAC ¶ 49(b).) Pratt v. Rowland, 65 F.3d 802, 808 (9th "
        "Cir. 1995). Defendant's \"prompt action reflects responsiveness\" theory is a "
        "competing inference. Competing inferences must be resolved in Plaintiff's "
        "favor at this stage. Twombly, 550 U.S. at 556.",
    )
    body(
        doc,
        "Concrete institutional incentive. Certifying the Supplement B would have "
        "required Serrato to attest under penalty of perjury that his subordinate "
        "officers committed qualifying criminal activity-while CHP was defending those "
        "same officers in two pending civil lawsuits. (FAC ¶ 49(c).) That incentive is "
        "not \"Plaintiff's decision to sue\"; it is Serrato's institutional interest in "
        "avoiding an official admission that would undermine those defenses.",
    )
    body(
        doc,
        "Pretextual reasoning. The denial offered no engagement with any evidence, "
        "identified no deficient statutory element, and applied no statutory standard. "
        "That absence of any evidence-based justification supports a plausible "
        "inference that the denial would not have occurred but for retaliatory animus: "
        "on this pleaded record, no legitimate, non-retaliatory ground for the "
        "boilerplate refusal appears. Capp, 940 F.3d at 1055; Nieves v. Bartlett, "
        "587 U.S. 391, 406 (2019). (FAC ¶ 49(d).)",
    )
    body(
        doc,
        "Structural conflict. Defendant simultaneously occupied two incompatible "
        "roles: supervisor of the accused officers and certifier of whether they "
        "committed qualifying crimes. (FAC ¶ 49(e).) Withrow v. Larkin, 421 U.S. 35, "
        "47 (1975). Defendant's observation that Plaintiff \"could have\" sought "
        "certification from another entity (MTD at 11) does not erase that conflict: "
        "CHP was the detecting agency possessing the dashcam recording, the Detention "
        "Certificate, and the underlying records, and that agency's commander was "
        "structurally compromised as circumstantial evidence of retaliatory motive.",
    )
    body(
        doc,
        "This Court found these allegations plausible at screening: \"While Defendant "
        "Serrato had discretion to certify the request, he did not have discretion to "
        "retaliate against Mr. Newanforbi.\" (Dkt. No. 5 at 4.) Defendant's motion "
        "simply asserts that each factor in isolation has an innocent explanation. "
        "That is a summary-judgment argument, not a Rule 12(b)(6) dismissal ground.",
    )

    # C. PDP
    subhead(
        doc,
        "C. The Procedural Due Process Claim Is Well-Pleaded.",
    )
    body(
        doc,
        "Even accepting Serrato's substantive discretion to deny certification, the "
        "manner of denial must still satisfy the process section 679.10 requires. "
        "Defendant argues the denial letter \"lays out the reason behind the denial\" "
        "and that \"is all the procedural due process the law requires.\" (MTD at 9.) "
        "The FAC alleges otherwise. Procedural due process first requires a protected "
        "liberty or property interest. Bd. of Regents v. Roth, 408 U.S. 564, 577 "
        "(1972). Plaintiff does not claim a protected interest in the ultimate "
        "certification result. The interest alleged is narrower: section 679.10's "
        "mandatory criteria and denial procedures materially constrain official "
        "discretion and create a legitimate entitlement to a non-retaliatory, "
        "statutorily compliant decisional process-including a meaningful written "
        "explanation-even if not to a compelled Form B signature. (FAC ¶¶ 40-44.)",
    )
    body(
        doc,
        "Section 679.10, subdivision (i)(2), requires \"a written explanation for the "
        "denial.\" Where the denial rests on non-cooperation, the explanation must "
        "include \"specific details of any reasonable requests for cooperation and a "
        "detailed description of how the victim refused to cooperate.\" The first "
        "sentence is a stand-alone command applicable to every denial; the second "
        "supplements it for cooperation-based denials. To read the second as the only "
        "requirement would mean an agency could deny certification on the most common "
        "ground-a finding the applicant was not a crime victim-with no meaningful "
        "explanation at all. That is what AB 1261 was enacted to prevent. The "
        "Legislative Counsel's Digest describes the written-explanation duty without "
        "qualification: a certifying entity that does not certify \"shall provide a "
        "written explanation for the denial of the certification.\" (Stats. 2023, ch. "
        "679.)",
    )
    body(
        doc,
        "The FAC specifically alleges the five-sentence boilerplate was legally "
        "deficient because it: (a) did not address the dashcam evidence; (b) did not "
        "address the section 851.6 Detention Certificate; (c) did not identify which "
        "statutory element was unsatisfied; (d) did not acknowledge the rebuttable "
        "presumption of helpfulness; and (e) did not provide specific reasons as "
        "required by statute. (FAC ¶¶ 31, 37, 43.) A conclusory assertion that the "
        "incident \"does not meet the standard\"-without identifying the standard "
        "applied, the element found wanting, or any engagement with the agency's own "
        "exculpatory records-is not a \"written explanation\" in any meaningful sense. "
        "It is the form of denial AB 1261 was written to abolish.",
    )
    cite_body(
        doc,
        "If that interest is protected, ",
        "Mathews v. Eldridge",
        ", 424 U.S. 319, 335 (1976), confirms the process alleged here was inadequate: "
        "the private interest in access to the U-visa gateway is substantial; the risk "
        "of erroneous deprivation from a five-sentence boilerplate engaging with no "
        "evidence is extreme; and the governmental interest in withholding a reasoned "
        "explanation is minimal because the Supplement B is a factual certification, "
        "not a visa approval. (FAC ¶ 38.) Goldberg v. Kelly, 397 U.S. 254, 262 (1970). "
        "These allegations state a plausible procedural due process claim.",
    )

    # D. SDP (secondary; no compel-certification overclaim)
    subhead(
        doc,
        "D. The Substantive Due Process Claim Is Well-Pleaded.",
    )
    body(
        doc,
        "Plaintiff does not assert a federal right to U-visa certification. Nor does he "
        "argue that section 679.10 eliminates all discretion. To the extent FAC "
        "paragraph 35 can be read as alleging that section 679.10 eliminates all "
        "substantive certification discretion or that the official \"must sign\" whenever "
        "statutory elements are met, Plaintiff does not rely on that proposition here. "
        "The surviving constitutional theory concerns retaliatory motive and mandatory "
        "procedural constraints. He accepts this Court's holding that Serrato had "
        "discretion to certify for purposes of the compel-signature theory Defendant "
        "attributes to the FAC. (Dkt. No. 5 at 4.) That acceptance does not waive "
        "Plaintiff's separate state-mandate arguments under section 679.10. The claim "
        "here is narrower: where California has enacted a statute that (a) uses "
        "mandatory language (\"shall\"), (b) creates a rebuttable presumption of "
        "helpfulness, (c) requires specific written reasons for denial, (d) mandates "
        "processing within 30 days, and (e) expressly provides that investigation, "
        "charges, prosecution, or conviction are not required for certification, a "
        "certifying official who ignores those constraints and issues a boilerplate "
        "denial without engaging with the evidence in his own custody has acted "
        "arbitrarily.",
    )
    cite_body(
        doc,
        "Under federal law, the decision to sign a certification is discretionary. ",
        "Perez Perez v. Wolf",
        ", 943 F.3d 853, 863 (9th Cir. 2019). This Court quoted that principle at "
        "screening and still held the complaint sufficient. (Dkt. No. 5 at 3-4.) "
        "Federal discretion does not erase California's subsequent statutory "
        "constraints. Defendant's reliance on Catholic Charities CYO v. Chertoff, "
        "622 F. Supp. 2d 865 (N.D. Cal. 2008), is misplaced: that case addressed the "
        "federal statute-which lacked mandatory language-and was decided seven years "
        "before section 679.10 and sixteen years before AB 1261. The secondary "
        "substantive due process theory is preserved, but it is not the lead claim and "
        "does not depend on forcing a certification signature.",
    )
    body(
        doc,
        "Defendant's \"civil tort\" label rests on the absence of criminal charges. "
        "Section 679.10, subdivision (k)(1), expressly provides that investigation, "
        "charges, prosecution, or conviction \"are not required\" for certification. "
        "The FAC identifies enumerated qualifying criminal activity under 8 U.S.C. "
        "§ 1101(a)(15)(U)(iii) and section 679.10(c)-false imprisonment, unlawful "
        "criminal restraint, felonious assault, perjury, and obstruction of justice. "
        "(FAC ¶ 21.) This Court already accepted those allegations as supporting a "
        "plausible inference of false imprisonment based on fabricated evidence. "
        "(Dkt. No. 5 at 4.) And Defendant's attack on the helpfulness presumption "
        "inverts subdivision (h): if no assistance was requested, the victim has not "
        "\"refused or failed to provide\" it. The FAC further alleges affirmative "
        "cooperation through complaints and production of the agency's own records. "
        "(FAC ¶¶ 23, 47.)",
    )

    # E. Declaratory / Injunctive
    subhead(
        doc,
        "E. Declaratory and Injunctive Relief Are Proper.",
    )
    body(
        doc,
        "Plaintiff does not oppose treating the fourth cause of action as a prayer for "
        "remedy rather than a standalone cause of action. Declaratory relief is "
        "properly characterized as a form of relief. The relief sought, however, "
        "remains proper and should not be stricken. Plaintiff does not seek an order "
        "compelling Defendant to sign the Supplement B in this action. Consistent with "
        "this Court's recognition of certification discretion for Section 1983 "
        "purposes, Plaintiff seeks vacatur of the April 20, 2026 denial and a remand "
        "for a new decision that applies the correct statutory standards, engages with "
        "the evidence, and is free of retaliatory motive-leaving Defendant's "
        "substantive certification judgment intact while correcting the constitutional "
        "defects. Nothing in that federal remedy request waives Petitioner's "
        "state-law mandate claims in Case No. 26CV191136 concerning section 679.10's "
        "enforceable processing and explanation duties.",
    )
    cite_body(
        doc,
        "The FAC seeks prospective relief against Defendant in his official capacity: "
        "a declaration that the April 20, 2026 denial violated constitutional "
        "standards and that Plaintiff is entitled to a new certification decision "
        "applying the correct standards to the evidence in CHP's possession, together "
        "with corresponding injunctive relief. (FAC ¶¶ 53-54, Prayer ¶¶ E-F.) To the "
        "extent any prayer language could be read more broadly, Plaintiff clarifies "
        "that the operative request on this motion is process correction-vacatur and "
        "redo-not a directed Form B signature. That is prospective relief authorized "
        "by ",
        "Ex parte Young",
        ", 209 U.S. 123 (1908). It is not duplicative of the damages claims against "
        "Defendant in his individual capacity.",
    )
    body(
        doc,
        "Defendant's authorities involve plaintiffs seeking declarations about "
        "completed foreclosures or other purely past wrongs with no forward-looking "
        "component. (MTD at 12.) Here an actual controversy remains live: Plaintiff's "
        "certification remains denied; he still needs a lawful certification decision "
        "to pursue U nonimmigrant status; and the parties dispute whether the April 20 "
        "denial complied with constitutional and statutory standards. A new decision "
        "on a correct legal standard is forward-looking relief, not a retrospective "
        "damages substitute.",
    )

    # F. Related cases - ACCEPT Fickes denial as true, distinguish
    subhead(
        doc,
        "F. The Related-Case Narrative Does Not Defeat the FAC.",
    )
    body(
        doc,
        "Defendant argues that Judge Fickes's denial of Plaintiff's judicial U-visa "
        "certification motion in Case No. 26CV168913, Plaintiff's voluntary dismissals "
        "of earlier actions, and an Eastern District report and recommendation show "
        "that retaliation is implausible and that leave to amend would be futile. "
        "(MTD at 11, 16-17.) Plaintiff accepts those procedural facts for purposes of "
        "this opposition. They still do not warrant dismissal.",
    )
    add_para(
        doc,
        "1. Extrinsic Materials Are Improper on a Bare Rule 12(b)(6) Record.",
        bold=True,
        double=True,
    )
    cite_body(
        doc,
        "On a Rule 12(b)(6) motion, the court generally may not consider materials "
        "outside the pleadings. ",
        "Lee v. City of Los Angeles",
        ", 250 F.3d 668, 688-89 (9th Cir. 2001). Judicial notice may reach an order's "
        "existence but not the truth of disputed matters recited within it, and may "
        "not be used to supply missing elements or to resolve competing inferences "
        "against the plaintiff. Khoja v. Orexigen Therapeutics, Inc., 899 F.3d 988, "
        "998-1003 (9th Cir. 2018). Defendant submits no request for judicial notice, "
        "no declaration, and no exhibits. Even if the Court takes notice that Judge "
        "Fickes denied a certification motion and that other cases were dismissed, "
        "those facts do not establish-much less conclusively establish-that Serrato's "
        "April 20 denial was lawful or non-retaliatory. What Defendant actually asks "
        "is that the Court draw adverse inferences about Plaintiff's credibility and "
        "litigation motives from materials the Court cannot test on this record. That "
        "is the functional equivalent of a credibility determination-exactly what "
        "Rule 12(b)(6) forbids.",
    )
    add_para(
        doc,
        "2. Judge Fickes's Denial Does Not Resolve This Case.",
        bold=True,
        double=True,
    )
    body(
        doc,
        "Accepting that Judge Fickes denied Plaintiff's motion for judicial U-visa "
        "certification on June 18, 2026, that denial does not defeat the FAC for at "
        "least four independent reasons.",
    )
    body(
        doc,
        "First, different certifying official. Section 679.10 and 8 C.F.R. "
        "§ 214.14(a)(2) authorize multiple categories of certifying officials, "
        "including judges and law-enforcement supervisors. Judge Fickes's decision "
        "concerned whether a superior-court judge should certify Form I-918 "
        "Supplement B in a stayed civil tort action. This case concerns whether "
        "Captain Serrato-Commander of the CHP Dublin Area, supervisor of the accused "
        "officers, and the official who signed the April 20, 2026 denial-violated "
        "Plaintiff's constitutional rights in performing that agency certification "
        "function. One certifying official's denial does not immunize another's "
        "allegedly retaliatory or arbitrary denial.",
    )
    body(
        doc,
        "Second, different legal question. The Fickes motion asked a state judge to "
        "issue an affirmative certification. This action asks whether Serrato's "
        "existing denial was unconstitutional-because it was motivated by retaliation "
        "for protected petitioning and because the denial process ignored statutory "
        "explanation and evidence-engagement requirements. A \"no\" on judicial "
        "certification is not a \"yes\" on the lawfulness of Serrato's motive or "
        "process. Even if Judge Fickes's denial was substantively correct, that would "
        "not immunize Serrato's allegedly retaliatory or procedurally defective "
        "denial. The constitutional violation is in the how, not just the what.",
    )
    body(
        doc,
        "Third, different record posture and conflict. Serrato decided the request "
        "while personally supervising the accused officers, after acknowledging "
        "Plaintiff's POST/citizen complaint, and while those officers were defendants "
        "in pending civil suits. (FAC ¶¶ 48-49.) Judge Fickes did not occupy that "
        "structural conflict. The retaliation and bias allegations that this Court "
        "found plausible at screening are specific to Serrato.",
    )
    body(
        doc,
        "Fourth, no preclusion showing. Defendant has not pleaded or briefed claim "
        "preclusion, issue preclusion, or Rooker-Feldman. He offers the Fickes denial "
        "as atmosphere for a futility / \"serial litigation\" narrative. Atmosphere is "
        "not a Rule 12(b)(6) defense. And Defendant cannot use another forum's "
        "certification denial to contradict this Court's screening determination that "
        "false imprisonment based on fabricated evidence is plausibly pleaded "
        "qualifying criminal activity here. (Dkt. No. 5 at 4.)",
    )
    add_para(
        doc,
        "3. The Related Actions Are Not Duplicative of This One.",
        bold=True,
        double=True,
    )
    body(
        doc,
        "As the FAC discloses, the related actions involve different defendants, "
        "different legal theories, and different forms of relief. (FAC ¶¶ 11-12.) The "
        "Eastern District case concerned Fourth Amendment claims against the "
        "arresting officers. The Alameda tort case concerned false imprisonment, "
        "battery, and Bane Act theories against those officers and the State. The "
        "Alameda writ case (Matter 20) seeks state-law mandamus against CHP in its "
        "official capacity under Code of Civil Procedure section 1085. This case-the "
        "only one asserting Section 1983 damages and Ex parte Young relief against "
        "Defendant Serrato for his certification denial-is not duplicative. Voluntary "
        "dismissals without prejudice of other dockets do not adjudicate the merits of "
        "these claims.",
    )

    # G. QI
    subhead(doc, "G. Qualified Immunity Does Not Apply.")
    body(
        doc,
        "As a threshold matter, qualified immunity does not reach Plaintiff's "
        "official-capacity claims for prospective injunctive and declaratory relief. "
        "Defendant's own notice limits qualified immunity to his individual capacity. "
        "(MTD at 2, 14.) Qualified immunity provides no defense to those "
        "official-capacity prospective claims.",
    )
    cite_body(
        doc,
        "As to the individual-capacity claims, qualified immunity protects officials "
        "\"from liability for civil damages insofar as their conduct does not violate "
        "clearly established statutory or constitutional rights of which a reasonable "
        "person would have known.\" ",
        "Pearson v. Callahan",
        ", 555 U.S. 223, 231 (2009). Dismissal on qualified-immunity grounds at the "
        "12(b)(6) stage is inappropriate \"unless the court can determine from the "
        "complaint alone that qualified immunity applies.\" Keates v. Koile, 883 F.3d "
        "1228, 1235 (9th Cir. 2018). It cannot do so here.",
    )
    add_para(doc, "1. Defendant Violated Constitutional Rights.", bold=True, double=True)
    body(
        doc,
        "As set forth above, the FAC adequately alleges violations of substantive and "
        "procedural due process and First Amendment retaliation. This Court has "
        "already found these allegations sufficient: the complaint \"supports the "
        "plausible inferences that CHP officers falsely imprisoned him in November "
        "2024 based on fabricated evidence\" and that \"Defendant Serrato retaliated "
        "against him by wrongfully denying his certification request.\" (Dkt. No. 5 at "
        "4.)",
    )
    add_para(doc, "2. The Unlawfulness Was Clearly Established.", bold=True, double=True)
    body(
        doc,
        "The clearly established law is clearest on retaliation-and that is enough to "
        "defeat qualified immunity on the lead claim.",
    )
    cite_body(
        doc,
        "First, it was clearly established by April 2026 that a government official "
        "may not deny a discretionary benefit in retaliation for protected petitioning. ",
        "Perry v. Sindermann",
        ", 408 U.S. 593, 597 (1972); Bd. of Cnty. Comm'rs v. Umbehr, 518 U.S. 668, "
        "674 (1996); Borough of Duryea v. Guarnieri, 564 U.S. 379, 387 (2011); "
        "Hartman v. Moore, 547 U.S. 250, 256 (2006). The analogue here is concrete: "
        "denying a statutory certification benefit because the applicant filed "
        "complaints and litigation against officers under the official's supervision. "
        "Defendant's own authority confirms the elements: Ford v. City of Yakima, "
        "706 F.3d at 1193. Capp, 940 F.3d at 1055, reversed dismissal of a "
        "retaliation claim on analogous pleading of retaliatory motive. Wesby's "
        "caution against defining clearly established law at too high a level of "
        "generality, 583 U.S. at 64, does not require a prior case about U-visa "
        "certifications; it requires that the unlawfulness follow from established "
        "principles. Retaliatory denial of a discretionary benefit for protected "
        "petitioning is not a close call-especially after this Court stated that "
        "Serrato \"did not have discretion to retaliate.\" (Dkt. No. 5 at 4.)",
    )
    body(
        doc,
        "Second, as to the secondary due-process theories, section 679.10's specific "
        "written-explanation and non-dispositive-absence-of-charges requirements gave "
        "Defendant fair notice that a boilerplate denial ignoring the agency's own "
        "evidence would violate those constraints. Hope v. Pelzer, 536 U.S. 730, 741 "
        "(2002). Those theories are preserved; they are not the lead clearly-"
        "established path.",
    )

    # H. Leave
    subhead(doc, "H. If Any Claim Is Dismissed, Leave to Amend Must Be Granted.")
    cite_body(
        doc,
        "Defendant argues leave to amend should be denied because Plaintiff has "
        "\"substantial experience with the legal process,\" has already amended once, "
        "and has pursued related litigation. (MTD at 16-17.) The standard does not "
        "turn on litigation history or amendment count; it turns on whether amendment "
        "would be futile. \"[T]he rule favoring liberality in amendments to pleadings "
        "is particularly important for the pro se litigant.\" ",
        "Lopez v. Smith",
        ", 203 F.3d 1122, 1131 (9th Cir. 2000) (en banc). Leave should be granted "
        "unless it is \"absolutely clear that the deficiencies of the complaint could "
        "not be cured by amendment.\" Id. at 1137 (quoting Noll v. Carlson, 809 F.2d "
        "1446, 1448 (9th Cir. 1987)). This Court granted leave to file the First "
        "Amended Complaint. A single prior amendment does not establish futility; "
        "the question is whether the deficiencies could be cured, not how many times "
        "the complaint has been amended. Defendant has not demonstrated futility.",
    )
    body(
        doc,
        "Even accepting Defendant's related-case narrative in full, it does not show "
        "futility. The Eastern District report and recommendation addressed different "
        "claims against different defendants and never became a final judgment-the "
        "action was dismissed without prejudice. Judge Fickes's denial of a judicial "
        "certification motion does not adjudicate Serrato's individual-capacity "
        "liability for a retaliatory or arbitrary agency denial. The pending state "
        "writ petition seeks mandamus against CHP under state law, not Section 1983 "
        "damages against Serrato. And this Court has already held the operative "
        "theory here plausible. (Dkt. No. 5 at 4.)",
    )
    body(
        doc,
        "To the extent Defendant quarrels with the FAC's illustrative California "
        "Penal Code cross-references for the enumerated federal qualifying crimes "
        "(FAC ¶ 21), any such pleading gap is curable by amendment and is not a "
        "basis for dismissal with prejudice. The federal categories-false "
        "imprisonment, unlawful criminal restraint, felonious assault, perjury, and "
        "obstruction of justice-are pleaded under 8 U.S.C. § 1101(a)(15)(U)(iii) and "
        "were accepted as plausible at screening. (Dkt. No. 5 at 4.) Denial of leave "
        "to amend based on characterizations of other litigation-particularly where "
        "this Court has already screened these claims as sufficient-would be an "
        "abuse of discretion.",
    )

    # ---- IV. CONCLUSION ----
    heading(doc, "IV. CONCLUSION")
    body(
        doc,
        "Plaintiff respectfully requests that this Court: (1) deny Defendant's motion "
        "to dismiss in its entirety, with particular emphasis on the First Amendment "
        "retaliation claim already found plausible at screening; (2) deny Defendant's "
        "motions to strike; (3) permit Plaintiff to treat the fourth cause of action "
        "as a prayer for declaratory and injunctive process-correction relief rather "
        "than a standalone claim or a compel-certification order; and (4) in the "
        "alternative, grant leave to amend should the Court find any deficiency in "
        "the current pleading.",
    )
    add_para(doc, "", double=True)
    add_para(doc, "Dated: August 27, 2026", double=True)
    add_para(doc, "", double=True)
    add_para(doc, "Respectfully submitted,", double=True)
    add_para(doc, "", double=True)
    add_para(doc, "", double=True)

    if SIG_IMG.exists():
        p = add_para(doc, "", double=False)
        run = p.add_run()
        run.add_picture(str(SIG_IMG), width=Inches(1.8))

    add_para(doc, "____________________________________", double=False)
    add_para(doc, "BRENDAN NGEHSI NEWANFORBI", bold=True, double=False)
    add_para(doc, "Plaintiff, In Pro Per", double=False)

    OUT_DOCX.parent.mkdir(parents=True, exist_ok=True)
    OUT_MATTER24.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(OUT_DOCX))
    doc.save(str(OUT_MATTER24))
    print(f"Wrote {OUT_DOCX}")
    print(f"Wrote {OUT_MATTER24}")


if __name__ == "__main__":
    build()
