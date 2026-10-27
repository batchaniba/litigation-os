# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
Matter 32 -- Plaintiff's Opposition to Defendants' Motion to Dismiss FAC and
Motion to Strike (ECF 22), service version dated October 26, 2026.

  python3 internal/scripts/matter32-opposition-final-oct26.py

Text: Plaintiff's v2 (LibreOffice edit, 22 pp.), reproduced from
internal/private/research/matter-32/13-opposition-final/opposition-final-oct26.txt.
Layout: portfolio pleading paper (lib/pleading_paper). Signature: the Oct. 26
signature Plaintiff supplied (brendan-newanforbi-signature-v3-oct26.png).
Proof of service: house form (lib/proof_of_service), by e-mail to DAG Li.

Outputs (13-opposition-final/):
  Opposition ... (Oct 26 2026).pdf            memorandum only
  Proof of Service by Email ... (Oct 26 2026).pdf
  Opposition + POS ... (Oct 26 2026).pdf      one file for the e-mail

Spacing: one blank line before each Roman-numeral heading, none after it;
lettered and numbered subheadings sit on the line after the preceding text
with no extra blank, so the double-spaced paper itself separates sections.
"""

from __future__ import annotations

import re
import struct
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR / "lib"))
sys.path.insert(0, str(SCRIPT_DIR))

from pleading_paper import (  # noqa: E402
    CONTENT_LEFT, CONTENT_RIGHT, CONTENT_WIDTH, PleadingPaper,
)
import proof_of_service as pos  # noqa: E402

REPO_ROOT = SCRIPT_DIR.parent.parent
M32 = REPO_ROOT / "internal" / "private" / "research" / "matter-32"
CONTENT_FILE = M32 / "13-opposition-final" / "opposition-final-oct26.txt"
OUT_DIR = M32 / "13-opposition-final"
CASE = "4:26-cv-08271-ASK"
OPP_PDF = OUT_DIR / "Opposition to MTD (ECF 22) - N.D. Cal. 4-26-cv-08271-ASK (Oct 26 2026).pdf"
POS_PDF = OUT_DIR / "Proof of Service by Email - Opposition to MTD (ECF 22) (Oct 26 2026).pdf"
COMBINED_PDF = OUT_DIR / "Opposition to MTD (ECF 22) with Proof of Service (Oct 26 2026).pdf"
SCRATCH_DIR = Path(
    "/tmp/claude-0/-home-user-interactive-litigation-portfolio/"
    "5d8752f5-0059-5673-9c7e-bba513c7c835/scratchpad"
)

SIGNATURE_PATH = str(REPO_ROOT / "internal/assets/signature/brendan-newanforbi-signature-v3-oct26-900w.png")


def _png_size(path: str) -> tuple[int, int]:
    with open(path, "rb") as fh:
        fh.read(16)
        return struct.unpack(">II", fh.read(8))


SIG_IMG_W_PX, SIG_IMG_H_PX = _png_size(SIGNATURE_PATH)
SIG_WIDTH = 210
SIG_RIGHT_OFFSET = 28
SIG_HEIGHT_SCALE = 1.0

# Docket name in this action (FAC ¶ 35 ties it to "Brendan Ngehsi Newanforbi").
PLAINTIFF_NAME = "BRENDAN NGWA NFORBI"
SIGN_DATE = "October 26, 2026"

DOC_TITLE_FOOTER = (
    "PL.'S OPP. TO MOT. TO DISMISS FAC AND STRIKE -- NFORBI v. MEZA-GONZALEZ "
    f"(No. {CASE})"
)

ATTORNEY_BLOCK = [
    (PLAINTIFF_NAME, "Times-Bold", 12),
    ("Plaintiff, In Pro Per", "Times-Roman", 12),
    ("1455 Cat Tail Drive", "Times-Roman", 12),
    ("Stockton, CA 95204", "Times-Roman", 12),
    ("Telephone: (209) 801-4442", "Times-Roman", 12),
    ("E-mail: bnn.cdl@gmail.com", "Times-Roman", 12),
]

CAPTION_LEFT = [
    (PLAINTIFF_NAME + ",", True, False),
    ("", False, False),
    ("                          Plaintiff,", False, False),
    ("", False, False),
    ("       v.", False, False),
    ("", False, False),
    ("SANTIAGO MEZA-GONZALEZ (CHP Badge", True, False),
    ("#023295), in his individual capacity;", True, False),
    ("JOSE MELANO (CHP Badge #023054), in", True, False),
    ("his individual capacity; and DOES 1", True, False),
    ("through 10, inclusive,", True, False),
    ("", False, False),
    ("                          Defendants.", False, False),
    ("", False, False),
]

CAPTION_RIGHT = [
    (f"Case No. {CASE}", False, False),
    ("", False, False),
    ("PLAINTIFF'S OPPOSITION TO", True, False),
    ("DEFENDANTS' MOTION TO DISMISS", True, False),
    ("FIRST AMENDED COMPLAINT AND", True, False),
    ("MOTION TO STRIKE (ECF 22)", True, False),
    ("", False, False),
    ("Date: December 9, 2026", False, False),
    ("Time: 1:30 p.m.", False, False),
    ("Courtroom: 4", False, False),
    ("Judge: Hon. Ajay S. Krishnan", False, False),
    ("(as noticed; reassignment pending)", False, False),
]

HEARING_LINE = (
    "Hearing as noticed by Defendants: December 9, 2026, at 1:30 p.m., Courtroom 4, "
    "1301 Clay Street, Oakland, before the Honorable Ajay S. Krishnan. Defendants have "
    "declined magistrate-judge jurisdiction (ECF 23), and the hearing may be reset upon "
    "reassignment."
)

# (category, display, regex that finds it in body text). Complete list of
# every authority the memorandum cites (Civil L.R. 7-4(a)(2)).
AUTHORITIES = [
    ("Cases", "Akhtar v. Mesa, 698 F.3d 1202 (9th Cir. 2012)", r"Akhtar"),
    ("Cases", "Arizona v. Hicks, 480 U.S. 321 (1987)", r"Hicks"),
    ("Cases", "Ashcroft v. Iqbal, 556 U.S. 662 (2009)", r"Iqbal"),
    ("Cases", "Bell Atlantic Corp. v. Twombly, 550 U.S. 544 (2007)", r"Twombly"),
    ("Cases", "Bretz v. Kelman, 773 F.2d 1026 (9th Cir. 1985) (en banc)", r"Bretz"),
    ("Cases", "Brigham City v. Stuart, 547 U.S. 398 (2006)", r"Brigham City"),
    ("Cases", "Bureerong v. Uvawas, 922 F. Supp. 1450 (C.D. Cal. 1996)", r"Bureerong"),
    ("Cases", "Caldwell v. City & County of San Francisco, 889 F.3d 1105 (9th Cir. 2018)", r"Caldwell"),
    ("Cases", "Chism v. Washington State, 661 F.3d 380 (9th Cir. 2011)", r"Chism"),
    ("Cases", "Costanich v. Department of Social & Health Services, 627 F.3d 1101 (9th Cir. 2010)", r"Costanich"),
    ("Cases", "Devenpeck v. Alford, 543 U.S. 146 (2004)", r"Devenpeck"),
    ("Cases", "District of Columbia v. Wesby, 583 U.S. 48 (2018)", r"Wesby"),
    ("Cases", "Doe v. United States, 58 F.3d 494 (9th Cir. 1995)", r"Doe v\. United States"),
    ("Cases", "Eminence Capital, LLC v. Aspeon, Inc., 316 F.3d 1048 (9th Cir. 2003)", r"Eminence"),
    ("Cases", "Garity v. APWU National Labor Organization, 828 F.3d 848 (9th Cir. 2016)", r"Garity"),
    ("Cases", "Hebbe v. Pliler, 627 F.3d 338 (9th Cir. 2010)", r"Hebbe"),
    ("Cases", "Hervey v. Estes, 65 F.3d 784 (9th Cir. 1995)", r"Hervey"),
    ("Cases", "Hopkins v. Bonvicino, 573 F.3d 752 (9th Cir. 2009)", r"Hopkins"),
    ("Cases", "Kay v. Ehrler, 499 U.S. 432 (1991)", r"Kay v\. Ehrler"),
    ("Cases", "Keates v. Koile, 883 F.3d 1228 (9th Cir. 2018)", r"Keates"),
    ("Cases", "Khoja v. Orexigen Therapeutics, Inc., 899 F.3d 988 (9th Cir. 2018)", r"Khoja"),
    ("Cases", "Knowles v. Iowa, 525 U.S. 113 (1998)", r"Knowles"),
    ("Cases", "Liston v. County of Riverside, 120 F.3d 965 (9th Cir. 1997)", r"Liston"),
    ("Cases", "Lopez v. Smith, 203 F.3d 1122 (9th Cir. 2000) (en banc)", r"Lopez v\. Smith"),
    ("Cases", "Michigan v. Fisher, 558 U.S. 45 (2009) (per curiam)", r"Fisher"),
    ("Cases", "Mincey v. Arizona, 437 U.S. 385 (1978)", r"Mincey"),
    ("Cases", "Newanforbi v. Serrato, No. 3:26-cv-05953-CRB, ECF No. 5 (N.D. Cal. June 29, 2026)", r"Serrato, No\. 3:26"),
    ("Cases", "Rosenbaum v. Washoe County, 663 F.3d 1071 (9th Cir. 2011)", r"Rosenbaum"),
    ("Cases", "Sialoi v. City of San Diego, 823 F.3d 1223 (9th Cir. 2016)", r"Sialoi"),
    ("Cases", "Smith v. Wade, 461 U.S. 30 (1983)", r"Smith v\. Wade"),
    ("Cases", "Spencer v. Peters, 857 F.3d 789 (9th Cir. 2017)", r"Spencer"),
    ("Cases", "Starr v. Baca, 652 F.3d 1202 (9th Cir. 2011)", r"Starr"),
    ("Cases", "Terry v. Ohio, 392 U.S. 1 (1968)", r"Terry"),
    ("Cases", "United States v. Jones, 565 U.S. 400 (2012)", r"United States v\. Jones"),
    ("Cases", "United States v. Lopez, 482 F.3d 1067 (9th Cir. 2007)", r"United States v\. Lopez|Lopez, 482"),
    ("Cases", "United States v. Ngumezi, 980 F.3d 1285 (9th Cir. 2020)", r"Ngumezi"),
    ("Cases", "United States v. Prescott, 581 F.2d 1343 (9th Cir. 1978)", r"Prescott"),
    ("Cases", "United States v. Rodgers, 656 F.3d 1023 (9th Cir. 2011)", r"Rodgers"),
    ("Cases", "United States v. Snipe, 515 F.3d 947 (9th Cir. 2008)", r"Snipe"),
    ("Cases", "United States v. Stafford, 416 F.3d 1068 (9th Cir. 2005)", r"Stafford"),
    ("Cases", "United States v. Stanert, 762 F.2d 775 (9th Cir. 1985)", r"Stanert"),
    ("Cases", "Whittlestone, Inc. v. Handi-Craft Co., 618 F.3d 970 (9th Cir. 2010)", r"Whittlestone"),
    ("Cases", "Wilkerson v. Butler, 229 F.R.D. 166 (E.D. Cal. 2005)", r"Wilkerson"),
    ("Cases", "Zamani v. Carnes, 491 F.3d 990 (9th Cir. 2007)", r"Zamani"),
    ("Statutes and Rules", "28 U.S.C. § 1915(e)(2)", r"1915"),
    ("Statutes and Rules", "42 U.S.C. § 1983", r"§ 1983|section 1983"),
    ("Statutes and Rules", "42 U.S.C. § 1988", r"§ 1988"),
    ("Statutes and Rules", "Cal. Penal Code § 851.6", r"851\.6"),
    ("Statutes and Rules", "Cal. Veh. Code § 21718", r"21718"),
    ("Statutes and Rules", "Cal. Veh. Code § 23612", r"23612"),
    ("Statutes and Rules", "Fed. R. Civ. P. 12(b)(6)", r"12\(b\)\(6\)"),
    ("Statutes and Rules", "Fed. R. Civ. P. 12(f)", r"12\(f\)"),
    ("Statutes and Rules", "Fed. R. Civ. P. 15(a)(2)", r"15\(a\)\(2\)"),
    ("Statutes and Rules", "Fed. R. Civ. P. 54(d)", r"54\(d\)"),
    ("Statutes and Rules", "N.D. Cal. Civil L.R. 7-4(a)(2)", r"Civil L\.R\. 7-4"),
]

CASE_ITALICS = sorted(
    [
        "Akhtar v. Mesa", "Arizona v. Hicks", "Ashcroft v. Iqbal", "Bell Atlantic Corp. v. Twombly",
        "Bretz v. Kelman", "Brigham City v. Stuart", "Bureerong v. Uvawas",
        "Caldwell v. City & County of San Francisco", "Chism v. Washington State",
        "Costanich v. Dep't of Soc. & Health Servs.", "Devenpeck v. Alford",
        "District of Columbia v. Wesby", "Doe v. United States",
        "Eminence Capital, LLC v. Aspeon, Inc.", "Garity v. APWU Nat'l Lab. Org.",
        "Hebbe v. Pliler", "Hervey v. Estes", "Hopkins v. Bonvicino", "Kay v. Ehrler",
        "Keates v. Koile", "Khoja v. Orexigen Therapeutics, Inc.", "Knowles v. Iowa",
        "Liston v. County of Riverside", "Lopez v. Smith", "Michigan v. Fisher",
        "Mincey v. Arizona", "Newanforbi v. Serrato", "Rosenbaum v. Washoe County",
        "Sialoi v. City of San Diego", "Smith v. Wade", "Spencer v. Peters", "Starr v. Baca",
        "Terry v. Ohio", "United States v. Jones", "United States v. Lopez",
        "United States v. Ngumezi", "United States v. Prescott", "United States v. Rodgers",
        "United States v. Snipe", "United States v. Stafford", "United States v. Stanert",
        "Whittlestone, Inc. v. Handi-Craft Co.", "Wilkerson v. Butler", "Zamani v. Carnes",
        "Akhtar", "Hicks", "Iqbal", "Twombly", "Brigham City", "Caldwell", "Chism",
        "Costanich", "Devenpeck", "Wesby", "Eminence", "Hebbe", "Hervey", "Hopkins",
        "Keates", "Khoja", "Knowles", "Fisher", "Mincey", "Sialoi", "Starr", "Lopez",
        "Ngumezi", "Prescott", "Snipe", "Whittlestone", "Zamani", "Terry",
        "Id.", "id.", "See", "see",
    ],
    key=len, reverse=True,
)


def italicize_cases(text: str) -> str:
    out = text
    for name in CASE_ITALICS:
        pattern = re.compile(r"(?<![A-Za-z<:])" + re.escape(name) + r"(?![A-Za-z])")
        parts = re.split(r"(<<[bi]{1,2}:[^>]+>>)", out)
        out = "".join(p if p.startswith("<<") else pattern.sub(f"<<i:{name}>>", p) for p in parts)
    return out


H, S, S2, P, N, B = "H", "S", "S2", "P", "N", "B"


def load_content() -> list[tuple[str, str, str]]:
    """Each entry: (tag, label, text). label is the "A." / "1." prefix, if any."""
    out = []
    for raw in CONTENT_FILE.read_text(encoding="utf-8").splitlines():
        if not raw.strip() or raw.startswith("##"):
            continue
        tag, rest = raw.split("|", 1)
        rest = rest.strip()
        label = ""
        if tag in (S, S2, N):
            label, rest = rest.split("|", 1)
        out.append((tag, label.strip(), rest.strip()))
    return out


CONTENT = load_content()


def toc_label(tag: str, label: str, text: str) -> str:
    return f"{label} {text}" if label else text


def toc_row(d, label: str, page_str: str, bold: bool = False, indent: float = 0,
            num_reserve: float = 30) -> None:
    c = d.c
    fn = "Times-Bold" if bold else "Times-Roman"
    size = 12
    left_x = CONTENT_LEFT + indent
    right_x = CONTENT_RIGHT - 8
    avail = CONTENT_WIDTH - indent - num_reserve - 6
    lines, cur = [], ""
    for w in label.split(" "):
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
        c.drawString(left_x + (0 if i == 0 else 18), y, ln)
        if i == len(lines) - 1:
            c.setFont("Times-Roman", size)
            c.drawRightString(right_x, y, page_str)
            label_end = left_x + (0 if i == 0 else 18) + c.stringWidth(ln, fn, size) + 4
            leader_end = right_x - c.stringWidth(page_str, "Times-Roman", size) - 4
            if leader_end > label_end:
                dw = c.stringWidth(". ", "Times-Roman", size)
                c.drawString(label_end, y, ". " * max(0, int((leader_end - label_end) / dw)))
        d.current_line += 1


def fmt_pages(pages: set) -> str:
    if not pages:
        return "0"
    ps = sorted(pages)
    return "passim" if len(ps) > 5 else ", ".join(str(p) for p in ps)


def hanging(d, label: str, text: str, label_x: float, text_indent: float, bold: bool = False) -> None:
    """Label at label_x; text wraps flush at text_indent (hanging indent)."""
    d._ensure_line()
    y = d._line_y(d.current_line)
    d.c.setFont("Times-Bold" if bold else "Times-Roman", 12)
    d.c.drawString(CONTENT_LEFT + label_x, y, label)
    d.write_wrapped(f"<<b:{text}>>" if bold else text, indent=text_indent, first_indent=0)


def render(out_path: Path, toc_pages: dict, toa_pages: dict,
           capture: dict | None = None, cites: dict | None = None) -> int:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    d = PleadingPaper(str(out_path), doc_title_footer=DOC_TITLE_FOOTER)
    c = d.c
    atty_y = d._line_y(0)
    for i, (text, font, size) in enumerate(ATTORNEY_BLOCK):
        c.setFont(font, size)
        c.drawString(CONTENT_LEFT, atty_y - i * 15, text)
    d.current_line = 4
    d.blank_line()
    d.write_line("UNITED STATES DISTRICT COURT", bold=True, center=True)
    d.write_line("NORTHERN DISTRICT OF CALIFORNIA", bold=True, center=True)
    d.blank_line()
    d.draw_caption_block(CAPTION_LEFT, CAPTION_RIGHT, caption_size=10, tight_lh=13, boxed=True)
    d.blank_line()
    d.write_wrapped(HEARING_LINE, first_indent=0)

    # Table of contents: two lines below the hearing paragraph
    d.blank_line()
    d.blank_line()
    d.ensure_space(4)
    d.write_line("TABLE OF CONTENTS", bold=True, center=True)
    d.blank_line()
    for tag, label, text in CONTENT:
        if tag not in (H, S):
            continue
        key = toc_label(tag, label, text)
        toc_row(d, key, str(toc_pages.get(key, "0")), bold=(tag == H),
                indent=(0 if tag == H else 18))

    # Table of authorities: two lines below the table of contents
    d.blank_line()
    d.blank_line()
    d.ensure_space(4)
    d.write_line("TABLE OF AUTHORITIES", bold=True, center=True)
    current_cat = None
    for cat, display, _pat in AUTHORITIES:
        if cat != current_cat:
            d.ensure_space(3)
            if current_cat is not None:
                d.blank_line()
            d.write_line(cat, bold=True)
            current_cat = cat
        toc_row(d, display, fmt_pages(toa_pages.get(display, set())))

    # Memorandum: three lines below the table of authorities
    d.blank_line()
    d.blank_line()
    d.blank_line()
    body_first_page = d.page_num
    prev = None
    for tag, label, text in CONTENT:
        key = toc_label(tag, label, text)
        start = d.page_num
        if tag == H:
            if text.endswith("CONCLUSION"):
                d.ensure_space(14)  # keep the conclusion with the signature (heading, text, 7-line block)
            else:
                d.ensure_space(4)
            # One blank before a Roman heading, but not right after the
            # memorandum title or at the top of a page.
            if prev not in (None, H) and d.current_line != 0:
                d.blank_line()
            if capture is not None:
                capture[key] = d.page_num
            d.write_line(text, bold=True, center=True)
        elif tag in (S, S2):
            d.ensure_space(4 if tag == S else 3)  # heading plus two lines of text
            if capture is not None and tag == S:
                capture[key] = d.page_num
            if tag == S:
                hanging(d, label, text, 0, 22, bold=True)
            else:
                hanging(d, label, text, 22, 40, bold=True)
        elif tag == P:
            d.write_wrapped(italicize_cases(text), first_indent=36)
        elif tag == N:
            hanging(d, label, italicize_cases(text), 36, 58)
        elif tag == B:
            hanging(d, "•", italicize_cases(text), 36, 54)
        if cites is not None and tag in (P, N, B):
            for _cat, display, pat in AUTHORITIES:
                if re.search(pat, text):
                    cites.setdefault(display, set()).update(range(start, d.page_num + 1))
        prev = tag

    # Seven lines: date, "Respectfully submitted,", two lines of air for the
    # stamp (one clear line above it), the signature rule, name, and role.
    d.ensure_space(7)
    d.write_line(f"Dated: {SIGN_DATE}")
    d.write_line("Respectfully submitted,", right=True, right_margin_offset=SIG_RIGHT_OFFSET)
    d.blank_line()
    d.blank_line()
    rule = "___________________________________"
    y = d._line_y(d.current_line)
    img_h = SIG_WIDTH * (SIG_IMG_H_PX / SIG_IMG_W_PX) * SIG_HEIGHT_SCALE
    line_right = CONTENT_RIGHT - SIG_RIGHT_OFFSET
    line_center = line_right - d.c.stringWidth(rule, "Times-Roman", 12) / 2
    d.c.drawImage(SIGNATURE_PATH, line_center - SIG_WIDTH / 2, y + 3, width=SIG_WIDTH,
                  height=img_h, mask="auto", preserveAspectRatio=False)
    for line in (rule, PLAINTIFF_NAME, "Plaintiff, In Pro Per"):
        d.write_line(line, right=True, right_margin_offset=SIG_RIGHT_OFFSET)
    body_last_page = d.page_num

    d.save()
    print(f"Wrote {out_path.name} ({d.page_num} pages; memorandum pp. "
          f"{body_first_page}-{body_last_page})")
    return d.page_num


# ---------------------------------------------------------------------------
# Proof of service (house form), by e-mail. No consent recital, per Plaintiff.
# ---------------------------------------------------------------------------
SERVICE_LIST = [
    "Haiyang A. Li, Deputy Attorney General",
    "Office of the Attorney General",
    "300 South Spring Street, Suite 1702",
    "Los Angeles, CA 90013-1230",
    "E-mail: Haiyang.Li@doj.ca.gov",
]


def pos_fields() -> pos.ProofOfServiceFields:
    return pos.ProofOfServiceFields(
        plaintiff_line=PLAINTIFF_NAME,
        plaintiff_role="Plaintiff",
        defendant_lines=[
            "SANTIAGO MEZA-GONZALEZ; JOSE MELANO;",
            "and DOES 1 through 10, inclusive",
        ],
        defendant_role="Defendants",
        case_number=CASE,
        title="PROOF OF SERVICE",
        service_date=SIGN_DATE,
        document_title=(
            "PLAINTIFF'S OPPOSITION TO DEFENDANTS' MOTION TO DISMISS FIRST AMENDED "
            "COMPLAINT AND MOTION TO STRIKE (ECF 22)"
        ),
        recipients=SERVICE_LIST + [
            "",
            "Attorneys for Defendants Santiago Meza-Gonzalez",
            "and Jose Melano",
        ],
        server_name="Brendan Ngwa Nforbi",
        stamp_signature=True,
        district_line=pos.DISTRICT_NDCAL,
        by_email=True,
        ecf_header_border=True,
    )


def build_pos() -> None:
    # Stamp the Oct. 26 signature instead of the module default.
    pos.SIGNATURE_PATH = SIGNATURE_PATH
    pos.SIGNATURE_ASPECT = SIG_IMG_H_PX / SIG_IMG_W_PX
    pos.build_proof_of_service(POS_PDF, pos_fields())
    print(f"Wrote {POS_PDF.name}")


def combine() -> None:
    from pypdf import PdfWriter

    out = PdfWriter()
    for p in (OPP_PDF, POS_PDF):
        out.append(str(p))
    for page in out.pages:
        page.compress_content_streams()
    out.compress_identical_objects(remove_identicals=True, remove_orphans=True)
    with open(COMBINED_PDF, "wb") as fh:
        out.write(fh)
    print(f"Wrote {COMBINED_PDF.name} ({len(out.pages)} pages)")


def main() -> None:
    SCRATCH_DIR.mkdir(parents=True, exist_ok=True)
    capture: dict = {}
    cites: dict = {}
    tmp = SCRATCH_DIR / "_m32_final_pass1.pdf"
    render(tmp, {}, {}, capture=capture, cites=cites)
    tmp.unlink(missing_ok=True)
    render(OPP_PDF, capture, cites)
    build_pos()
    combine()


if __name__ == "__main__":
    main()
