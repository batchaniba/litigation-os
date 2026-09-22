# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
Matter 29 -- Plaintiff's Opposition to Amazon.com Services LLC's Motion to
Dismiss Plaintiff's Fifth, Sixth, and Seventh Claims (N.D. Cal. Rule 12(b)(6)),
rendered on portfolio pleading paper with the universal signature affixed.

  python3 internal/scripts/matter29-opposition-amazon-mtd.py

Strategy (per case posture): FIGHT the Fifth Claim (invasion of privacy) on the
merits; NARROW-oppose the Sixth Claim (UCL) -- concede the Sonner forum point but
force dismissal WITHOUT prejudice + state forum (Guzman) + leave to amend; and
NON-oppose the Seventh Claim (IIED) without prejudice and with leave to amend.

Every authority below is verified against internal/docs/citation_index.json:
  Ashcroft v. Iqbal, 556 U.S. 662 (2009)
  Bell Atlantic Corp. v. Twombly, 550 U.S. 544 (2007)
  Erickson v. Pardus, 551 U.S. 89 (2007)
  Epstein v. Washington Energy Co., 83 F.3d 1136 (9th Cir. 1996)
  Hill v. National Collegiate Athletic Assn., 7 Cal.4th 1 (1994)
  Sonner v. Premier Nutrition Corp., 971 F.3d 834 (9th Cir. 2020)
  Guzman v. Polaris Industries Inc., 49 F.4th 1308 (9th Cir. 2022)
Amazon's own privacy authorities are cited only to distinguish them.

Sign-off date is set to the anticipated filing date (opposition due ~Oct. 6,
2026 under Civ. L.R. 7-3(a)). VERIFY the date and all pins before filing.
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR / "lib"))
sys.path.insert(0, str(SCRIPT_DIR))

from pleading_paper import (  # noqa: E402
    CONTENT_LEFT, CONTENT_RIGHT, CONTENT_WIDTH, PleadingPaper,
)
from signature_stamp import SIGNATURE_PATH, SIGNATURE_NATIVE_PX  # noqa: E402

REPO_ROOT = SCRIPT_DIR.parent.parent

OUT_PATHS = [
    REPO_ROOT / "internal" / "public" / "documents" / "matter-29"
    / "Opposition to Amazon MTD - Pleading Paper (DRAFT).pdf",
]
SCRATCH_OUT = Path(
    "/tmp/claude-0/-home-user-interactive-litigation-portfolio/"
    "fde9b68e-7f08-5546-b231-a91ce9f193c5/scratchpad/"
    "Opposition-to-Amazon-MTD-DRAFT.pdf"
)

SIGN_OFF_DATE = "October 6, 2026"

DOC_TITLE_FOOTER = (
    "PLAINTIFF'S OPPOSITION TO AMAZON'S MOTION TO DISMISS -- "
    "NEWANFORBI v. AMAZON.COM SERVICES, LLC (N.D. Cal.)"
)
COURT_LINE1 = "UNITED STATES DISTRICT COURT"
COURT_LINE2 = "NORTHERN DISTRICT OF CALIFORNIA"

SIG_IMG_W_PX, SIG_IMG_H_PX = SIGNATURE_NATIVE_PX
SIG_WIDTH = 235
SIG_RIGHT_OFFSET = 28
SIG_HEIGHT_SCALE = 1.25

ATTORNEY_BLOCK = [
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
    ("AMAZON.COM SERVICES, LLC, a", True, False),
    ("Delaware limited liability company;", True, False),
    ("ACCURATE BACKGROUND, LLC, a", True, False),
    ("California limited liability company;", True, False),
    ("and DOES 1-10, inclusive,", True, False),
    ("", False, False),
    ("                          Defendants.", False, False),
    ("", False, False),
]

CAPTION_RIGHT = [
    ("Case No. 4:26-cv-09249-ASK", False, False),
    ("", False, False),
    ("PLAINTIFF'S OPPOSITION TO", True, False),
    ("DEFENDANT AMAZON.COM", True, False),
    ("SERVICES LLC'S MOTION TO", True, False),
    ("DISMISS PLAINTIFF'S FIFTH,", True, False),
    ("SIXTH, AND SEVENTH CLAIMS", True, False),
    ("FOR RELIEF", True, False),
    ("", False, False),
    ("Date: November 18, 2026", False, False),
    ("Time: 1:30 p.m.", False, False),
    ("Courtroom: 4, 3rd Floor", False, False),
    ("Judge: Hon. Ajay S. Krishnan", False, False),
]

CASE_ITALICS = sorted(
    [
        "Hill v. National Collegiate Athletic Assn.",
        "Sonner v. Premier Nutrition Corp.",
        "Guzman v. Polaris Industries Inc.",
        "Bell Atlantic Corp. v. Twombly",
        "Epstein v. Washington Energy Co.",
        "Smith v. YETI Coolers, LLC",
        "In re Yahoo Mail Litig.",
        "Saleh v. Nike, Inc.",
        "King v. Facebook, Inc.",
        "Brahmana v. Henard",
        "Estate of Hearst",
        "Erickson v. Pardus",
        "Ashcroft v. Iqbal",
        "Lerma v. Amazon.com Services, LLC",
        "Guzman",
        "Sonner",
        "Twombly",
        "Epstein",
        "Erickson",
        "Brahmana",
        "Saleh",
        "Iqbal",
        "Hearst",
        "Lerma",
        "Hill",
    ],
    key=len,
    reverse=True,
)


def italicize_cases(text: str) -> str:
    out = text
    for name in CASE_ITALICS:
        if f"<<i:{name}>>" in out:
            continue
        pattern = re.compile(r"(?<![A-Za-z])" + re.escape(name) + r"(?![A-Za-z])")
        parts = re.split(r"(<<i:[^>]+>>)", out)
        rebuilt = []
        for part in parts:
            if part.startswith("<<i:"):
                rebuilt.append(part)
            else:
                rebuilt.append(pattern.sub(f"<<i:{name}>>", part))
        out = "".join(rebuilt)
    return out


# ==========================================================
# BODY CONTENT
# ==========================================================
H, S, P, L = "HEADER", "SUBHEAD", "PARA", "LIST"

CONTENT = [
    (H, "I. INTRODUCTION"),
    (P, "Amazon's motion is notable first for what it does not seek. Plaintiff's Complaint pleads seven causes of action. Amazon moves against only three of them -- the Fifth (invasion of privacy), the Sixth (California's Unfair Competition Law), and the Seventh (intentional infliction of emotional distress). It does not move against Plaintiff's First Claim under Penal Code section 290.46(j)(2)(E), his Second Claim under the California Fair Chance Act, his Third Claim under the Fair Credit Reporting Act, or his Fourth Claim under the Investigative Consumer Reporting Agencies Act. Those claims -- which carry the core of this case -- are not before the Court on this motion and proceed regardless of its outcome. Even if granted in full, Amazon's motion would not dispose of this action."),
    (P, "As to the three claims Amazon does challenge, the motion should be denied as to the Fifth Claim and, as to the Sixth and Seventh, resolved without prejudice and with leave to amend. Amazon's attack on the invasion-of-privacy claim rests on a mischaracterization: it treats the claim as an assertion that sex-offender-registry information is secret, then answers that public records cannot be private. But Plaintiff has never alleged the registry is secret. He alleges a legally protected interest in registry information 'insofar as that information is used for purposes expressly prohibited by Penal Code section 290.46(j)(2)' -- a statutory use-restriction the Legislature enacted and backed with a private right of action. Compl. para. 73. Amazon's public-records authorities do not touch that theory. And Amazon does not argue that Plaintiff failed to plausibly allege the prohibited use itself -- the very conduct underlying the unchallenged First Claim -- so it cannot obtain dismissal of the privacy claim while leaving standing the registry-misuse claim on which it is built."),
    (P, "The Sixth Claim (UCL) presents only a remedial-forum question, not a merits defect. Amazon invokes Sonner v. Premier Nutrition Corp. for the rule that a federal court sitting in equity may not entertain a UCL claim absent an allegation that the plaintiff lacks an adequate legal remedy. Even assuming that rule applies here, the consequence under controlling Ninth Circuit authority is dismissal without prejudice so the claim may be pursued in the state court from which Amazon removed it -- not the with-prejudice dismissal Amazon requests. Amazon does not, and cannot, contend that the conduct underlying the UCL claim is lawful; the claim's unlawful-prong predicates are the section 290.46, FCRA, and ICRAA violations Amazon has not challenged."),
    (P, "Plaintiff does not oppose dismissal of the Seventh Claim (IIED), provided the dismissal is without prejudice and with leave to amend once the Accurate Background report and Amazon's decision record -- which the Complaint expressly reserves the right to obtain -- are in hand."),
    (P, "Finally, Amazon's suggestion, raised only in a footnote, that 'this entire action ... was prematurely filed' (Mot. 1 n.1) is not a ground of its motion, seeks relief this Court cannot grant on the three challenged claims, and is contradicted by the well-pleaded allegations -- accepted as true on this motion -- that Amazon silently vacated Plaintiff's confirmed, dated training shift one day before it was to begin, effecting a de facto revocation of the specific position offered. Compl. paras. 22-25."),

    (H, "II. STATEMENT OF RELEVANT ALLEGATIONS"),
    (P, "On July 3, 2026, Amazon extended Plaintiff a conditional offer for a Seasonal XL Warehouse Associate position at its Fremont fulfillment center, with training fixed for July 28-29 and August 4-5, 2026. Compl. paras. 7-10. Amazon procured a consumer report on Plaintiff through its background-check vendor, Defendant Accurate Background, which identified itself in writing as 'a consumer reporting agency' retained by 'Amazon Salesforce' to conduct the screening. Id. paras. 2, 15-16."),
    (P, "Plaintiff is a registrant on California's Sex Offender Registry. Id. para. 26. He alleges that his registry status was used -- directly or through Accurate Background -- to deny him employment by silently withdrawing the offered position. As of July 27, 2026, the background check remained in 'Pending' status twenty days after submission (roughly four times Amazon's own stated five-day norm), and Amazon's onboarding checklist had replaced his confirmed shift with 'You do not have a shift selected,' one day before the fixed start date. Id. paras. 21-25. No adverse-action notice, no copy of the report, and no opportunity to respond was ever provided. Id. para. 23. Plaintiff further alleges, in the alternative and pending receipt of the report he has demanded but not received, the means by which registry-derived information entered the screening. Id. paras. 28-30, 75."),
    (P, "On a Rule 12(b)(6) motion, these allegations are accepted as true."),

    (H, "III. LEGAL STANDARD"),
    (P, "A Rule 12(b)(6) motion tests the sufficiency of the pleading, not the merits. A claim survives if it pleads 'factual content that allows the court to draw the reasonable inference that the defendant is liable for the misconduct alleged.' Ashcroft v. Iqbal, 556 U.S. 662, 678 (2009); see Bell Atlantic Corp. v. Twombly, 550 U.S. 544 (2007). The court accepts all well-pleaded factual allegations as true and construes them in the light most favorable to the plaintiff. Epstein v. Washington Energy Co., 83 F.3d 1136, 1140 (9th Cir. 1996). A pro se litigant's pleadings are held to less stringent standards and are construed liberally. Erickson v. Pardus, 551 U.S. 89, 94 (2007). When a claim is dismissed, leave to amend should be freely given unless amendment would be futile. Fed. R. Civ. P. 15(a)(2)."),

    (H, "IV. ARGUMENT"),

    (S, "A. Plaintiff's Fifth Claim for Invasion of Privacy Is Adequately Pleaded."),
    (P, "California recognizes a private right of action for invasion of the constitutional right to privacy. Cal. Const. art. I, section 1. The elements are (1) a legally protected privacy interest, (2) a reasonable expectation of privacy under the circumstances, and (3) conduct constituting a serious invasion of privacy. Hill v. National Collegiate Athletic Assn., 7 Cal.4th 1, 35-37 (1994). Amazon contests each element, but its arguments answer a claim Plaintiff has not brought and depend on factual determinations that cannot be made on the pleadings."),

    (S, "1. Plaintiff pleads a legally protected privacy interest -- a statutory use-restriction, not secrecy."),
    (P, "Amazon's principal argument is that Plaintiff 'has no legally protected privacy interest in public information relating to criminal convictions or information posted on a government website.' Mot. 5. That argument refutes a secrecy claim Plaintiff never made. The Complaint does not allege that the existence of Plaintiff's registry listing is confidential. It alleges a protected interest in that information 'insofar as that information is used for purposes expressly prohibited by Penal Code section 290.46, subdivision (j)(2).' Compl. para. 73 (emphasis added)."),
    (P, "That is a cognizable interest under Hill. Whether a privacy interest is 'legally protected' is informed by 'common law or statutory enactment,' and the interest in precluding the misuse of sensitive information is a recognized species of informational privacy. Hill, 7 Cal.4th at 35. The Legislature has spoken directly here. Penal Code section 290.46(j)(2) declares that registry information 'shall not be used' for enumerated purposes, expressly including to 'deny ... employment,' section 290.46(j)(2)(E), and it created a private civil remedy for violations, section 290.46(j)(4)(A). A statutory command that particular information not be used for a particular purpose, coupled with a private right of action, is precisely the kind of established norm that defines a legally protected privacy interest under Hill."),
    (P, "The public availability of the underlying listing does not defeat that interest. The statute's design is that the information is disclosed to the public for limited protective purposes while its use to deny employment is categorically forbidden. Privacy under California law is not an all-or-nothing concept; a limited disclosure for one purpose does not forfeit protection against a different, prohibited use. Hill, 7 Cal.4th at 35-37. Amazon's authorities do not hold otherwise. Brahmana v. Henard and Estate of Hearst stand only for the unremarkable proposition that court records are public. Neither addresses a statutory restriction on the use of otherwise-public information, and neither immunizes an employer's use of registry data for the one purpose the Penal Code forbids."),

    (S, "2. Plaintiff pleads a reasonable expectation of privacy; consent to a background check is not consent to a prohibited use."),
    (P, "Amazon next argues that Plaintiff consented to a background check and therefore had no reasonable expectation of privacy. Mot. 5 (citing Saleh v. Nike, Inc.). That argument fails at the pleading stage for two independent reasons. First, the scope of any consent is a question of fact that cannot be resolved on a Rule 12(b)(6) motion. The Complaint alleges consent to 'a background check' generally, Compl. paras. 7-8, 20 -- not consent to the use of registry information to deny employment. Second, a person cannot, as a matter of law, be deemed to have consented to a use the Legislature has categorically prohibited. Consent to a lawful screening does not waive the statutory protection of section 290.46(j)(2)(E), any more than consent to a credit check waives the protections of the FCRA. Reasonable expectations of privacy are measured against 'widely accepted community norms,' Hill, 7 Cal.4th at 36-37, and the governing norm here is codified: employers may not use registry information to deny employment."),

    (S, "3. Plaintiff pleads a serious invasion, and the Hill balancing is premature on the pleadings."),
    (P, "The third element -- conduct constituting an egregious breach of social norms -- is ordinarily a question of fact. Hill, 7 Cal.4th at 37. Plaintiff alleges that Defendants used his registry status to deny him a specific, dated job, in direct contravention of a statute enacted to prevent exactly that harm, and without any of the notices the law requires. Compl. paras. 22-25, 75. Where the alleged invasion is the very conduct the Legislature prohibited and made privately actionable, the seriousness of the invasion is at least plausibly pleaded. The 'high bar' Amazon invokes, Mot. 4 (quoting In re Yahoo Mail Litig.), describes what a plaintiff must ultimately prove after a fact-intensive balancing of competing interests -- not the sufficiency of a pleading. That balancing cannot be performed on the face of the Complaint."),
    (P, "One further point confirms the claim's sufficiency. The privacy claim rests on the same registry-misuse conduct as Plaintiff's First Claim under section 290.46(j)(2)(E) -- and Amazon has not moved to dismiss the First Claim. In its privacy argument, Amazon does not contend that Plaintiff failed to plausibly allege the prohibited use; it argues only public-record status and consent. Having declined to challenge the plausibility of the underlying registry-misuse allegations, Amazon cannot obtain dismissal of the privacy claim built upon them."),

    (S, "B. If the Court Applies Sonner to the Sixth Claim, Dismissal Should Be Without Prejudice to Refiling in State Court and With Leave to Amend."),
    (P, "Amazon argues that Plaintiff's UCL claim must be dismissed because the UCL affords only equitable relief and, under Sonner v. Premier Nutrition Corp., 971 F.3d 834 (9th Cir. 2020), a federal court may not award equitable relief absent an allegation that the plaintiff lacks an adequate remedy at law. Plaintiff does not dispute that Sonner states the governing rule for a UCL claim proceeding in federal court. But two consequences follow that Amazon's requested disposition ignores."),
    (P, "First, Sonner is a limitation on a federal court's equitable jurisdiction; it is not an adjudication that the underlying conduct is lawful. The UCL's 'unlawful' prong borrows as its predicates the section 290.46, FCRA, and ICRAA violations pleaded elsewhere in the Complaint. Compl. para. 79. Amazon has not moved to dismiss any of those predicate claims. Dismissal of the UCL count on Sonner grounds would therefore say nothing about the merits of the conduct it targets."),
    (P, "Second, because the defect is jurisdictional and remedial rather than substantive, the proper disposition is dismissal without prejudice so the claim may be pursued in state court -- not the dismissal with prejudice Amazon seeks. Guzman v. Polaris Industries Inc., 49 F.4th 1308, 1313-15 (9th Cir. 2022) (a UCL claim a federal court lacks equitable jurisdiction to hear is dismissed without prejudice and remains available in state court). That result is especially apt here: Amazon removed this action from the Superior Court of California, County of Alameda, where the Sonner rule does not apply and the UCL claim may proceed. A with-prejudice dismissal would improperly extinguish a state-law remedy that removal cannot defeat."),
    (P, "Third, to the extent the Court is inclined to dismiss the claim outright rather than preserve it, leave to amend should be granted. Fed. R. Civ. P. 15(a)(2). Plaintiff can allege that his legal remedies are inadequate as to the prospective injunctive relief he seeks -- an order enjoining Defendants' continued use of registry information for employment purposes and their practice of effecting adverse employment outcomes without the notices the FCRA and ICRAA require. Compl., Prayer para. 9. Backward-looking damages do not redress the risk that Plaintiff, a continuing applicant, will again be screened through the same unlawful process. Amendment would not be futile."),

    (S, "C. Plaintiff Does Not Oppose Dismissal of the Seventh Claim Without Prejudice and With Leave to Amend."),
    (P, "In the interest of focusing the Court's and the parties' resources, Plaintiff does not oppose dismissal of his Seventh Claim for intentional infliction of emotional distress. Plaintiff respectfully requests, however, that any dismissal be without prejudice and with leave to amend under Rule 15(a)(2). The Complaint reserves Plaintiff's right to obtain the Accurate Background report (screening Y94611404) and Amazon's decision record through 15 U.S.C. section 1681g, Civil Code section 1786.10, and discovery. Compl. paras. 29, 45. Once those materials are in hand, Plaintiff can plead with greater particularity both the outrageousness of the conduct -- including the knowing use of protected registry status to deny employment -- and the severity of the resulting distress. Dismissal with prejudice would be premature."),

    (H, "V. CONCLUSION"),
    (P, "For the foregoing reasons, Plaintiff respectfully requests that the Court: (1) deny Amazon's motion to dismiss the Fifth Claim for invasion of privacy; (2) as to the Sixth Claim under the UCL, deny the motion or, if the Court applies Sonner, dismiss the claim without prejudice to refiling in state court and with leave to amend; and (3) dismiss the Seventh Claim for intentional infliction of emotional distress without prejudice and with leave to amend. In all events, Amazon's motion does not reach Plaintiff's First through Fourth Claims for Relief, which proceed."),
]


def signature_block() -> str:
    return (
        f"Dated: {SIGN_OFF_DATE}\n"
        "\n"
        "Respectfully submitted,\n"
        "\n"
        "\n"
        "___________________________________\n"
        "BRENDAN NGEHSI NEWANFORBI\n"
        "Plaintiff, In Pro Per"
    )


def is_toc_entry(ctype: str, text: str):
    if ctype == H:
        return ("roman", text)
    if ctype == S and re.match(r"^[A-H]\.\s", text):
        return ("letter", text)
    return None


def toc_row(d, label: str, page_str: str, bold: bool = False, indent: float = 0,
            num_reserve: float = 30) -> None:
    c = d.c
    fn = "Times-Bold" if bold else "Times-Roman"
    size = 12
    left_x = CONTENT_LEFT + indent
    right_x = CONTENT_RIGHT - 8
    avail = CONTENT_WIDTH - indent - num_reserve - 6
    words = label.split(" ")
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if c.stringWidth(t, fn, size) > avail and cur:
            lines.append(cur)
            cur = w
        else:
            cur = t
    if cur:
        lines.append(cur)
    for i, ln in enumerate(lines):
        d._ensure_line()
        y = d._line_y(d.current_line)
        c.setFont(fn, size)
        c.drawString(left_x, y, ln)
        if i == len(lines) - 1:
            c.setFont("Times-Roman", size)
            c.drawRightString(right_x, y, page_str)
            label_end = left_x + c.stringWidth(ln, fn, size) + 4
            num_w = c.stringWidth(page_str, "Times-Roman", size)
            leader_end = right_x - num_w - 4
            if leader_end > label_end:
                dw = c.stringWidth(". ", "Times-Roman", size)
                ndots = max(0, int((leader_end - label_end) / dw))
                c.drawString(label_end, y, ". " * ndots)
        d.current_line += 1


def render(out_path: Path, toc_pages: dict, capture: dict | None = None) -> int:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    d = PleadingPaper(str(out_path), doc_title_footer=DOC_TITLE_FOOTER)

    c = d.c
    atty_y = d._line_y(0)
    atty_lh = 15
    for i, (text, font, size) in enumerate(ATTORNEY_BLOCK):
        c.setFont(font, size)
        c.drawString(CONTENT_LEFT, atty_y - i * atty_lh, text)
    d.current_line = 4
    d.blank_line()

    d.write_line(COURT_LINE1, bold=True, center=True)
    d.write_line(COURT_LINE2, bold=True, center=True)
    d.blank_line()

    d.draw_caption_block(CAPTION_LEFT, CAPTION_RIGHT, caption_size=10, tight_lh=13, boxed=True)
    d.blank_line()

    d.write_wrapped(
        "Hearing Date: November 18, 2026, at 1:30 p.m., in Courtroom 4, 3rd Floor, "
        "before the Honorable Ajay S. Krishnan, United States District Court for the "
        "Northern District of California, 1301 Clay Street, Oakland, CA 94612.",
        first_indent=0,
    )
    d.blank_line()

    d.ensure_space(4)
    d.write_line("TABLE OF CONTENTS", bold=True, center=True)
    d.blank_line()
    for ctype, text in CONTENT:
        te = is_toc_entry(ctype, text)
        if not te:
            continue
        level, label = te
        pg = str(toc_pages.get(label, "0"))
        toc_row(d, label, pg, bold=(level == "roman"),
                indent=(0 if level == "roman" else 18))
    d.blank_line()

    for c_type, text in CONTENT:
        if c_type == H:
            d.ensure_space(4)
            if capture is not None:
                capture[text] = d.page_num
            d.write_line(text, bold=True, center=True)
            d.blank_line()
        elif c_type == S:
            d.ensure_space(6)
            if capture is not None and re.match(r"^[A-H]\.\s", text):
                capture[text] = d.page_num
            d.write_wrapped(f"<<b:{text}>>", first_indent=0)
            d.blank_line()
        elif c_type == P:
            d.write_wrapped(italicize_cases(text), first_indent=36)
            d.blank_line()
        elif c_type == L:
            d.write_wrapped("- " + italicize_cases(text), indent=36, first_indent=0)
            d.blank_line()

    d.ensure_space(9)
    for line in signature_block().split("\n"):
        if line.startswith("_") and os.path.isfile(SIGNATURE_PATH):
            d.draw_signature_image(
                SIGNATURE_PATH, SIG_IMG_W_PX, SIG_IMG_H_PX, line,
                width=SIG_WIDTH, right_margin_offset=SIG_RIGHT_OFFSET,
                height_scale=SIG_HEIGHT_SCALE,
            )
            d.write_line(line, right=True, right_margin_offset=SIG_RIGHT_OFFSET)
        else:
            d.write_line(line, right=True, right_margin_offset=SIG_RIGHT_OFFSET)
    d.blank_line()

    d.save()
    print(f"Wrote {out_path} ({out_path.stat().st_size} bytes, {d.page_num} pages)")
    return d.page_num


def main() -> None:
    if not Path(SIGNATURE_PATH).is_file():
        raise SystemExit(f"Missing universal signature: {SIGNATURE_PATH}")
    capture: dict = {}
    tmp = SCRATCH_OUT.parent / "_toc_pass1.pdf"
    SCRATCH_OUT.parent.mkdir(parents=True, exist_ok=True)
    render(tmp, {}, capture=capture)
    try:
        tmp.unlink()
    except OSError:
        pass
    for out in list(OUT_PATHS) + [SCRATCH_OUT]:
        render(out, capture)
    print("NOTE: DRAFT -- not yet e-filed/served. Verify the filing date, page pins, "
          "and Amazon MTD internal page cites (Mot. 4-5) before filing.")


if __name__ == "__main__":
    main()
