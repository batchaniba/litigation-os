# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
Matter 24 -- Plaintiff's Opposition to Serrato MTD / Motion to Strike (v4)
on portfolio pleading paper, with the universal signature affixed.

  python3 internal/scripts/matter24-opposition-mtd-v4-pleading.py

Reads the Word draft (Opposition to MTD v4.docx) for body text so the
pleading-paper PDF stays in sync with the filed Word vehicle, then renders
onto lib/pleading_paper.PleadingPaper and stamps
internal/assets/signature/brendan-newanforbi-signature.png.
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR / "lib"))
sys.path.insert(0, str(SCRIPT_DIR))

from pleading_paper import CONTENT_LEFT, PleadingPaper  # noqa: E402
from signature_stamp import (  # noqa: E402
    SIGNATURE_PATH,
    SIGNATURE_NATIVE_PX,
)

try:
    from docx import Document
except ImportError:
    os.system(f"{sys.executable} -m pip install -q python-docx")
    from docx import Document

REPO_ROOT = SCRIPT_DIR.parent.parent
SOURCE_DOCX = REPO_ROOT / "Opposition to MTD v4.docx"

OUT_PATHS = [
    REPO_ROOT
    / "internal"
    / "public"
    / "documents"
    / "matter-24"
    / "Opposition to Serrato MTD FAC and Strike v4 - Pleading Paper (Sep 2 2026).pdf",
    REPO_ROOT / "Opposition to MTD v4 - Pleading Paper.pdf",
    Path("/opt/cursor/artifacts/Opposition-to-Serrato-MTD-v4-Pleading-Paper.pdf"),
]

DOC_TITLE_FOOTER = (
    "OPPOSITION TO MTD / MOTION TO STRIKE -- NEWANFORBI v. SERRATO (N.D. Cal.)"
)
COURT_LINE1 = "UNITED STATES DISTRICT COURT"
COURT_LINE2 = "NORTHERN DISTRICT OF CALIFORNIA"

FILED_STATUS = False

SIG_IMG_W_PX, SIG_IMG_H_PX = SIGNATURE_NATIVE_PX
SIG_WIDTH = 160

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
    ("CAPTAIN G. SERRATO, in his", True, False),
    ("individual and official capacities", True, False),
    ("as Commander, Dublin Area,", True, False),
    ("California Highway Patrol,", True, False),
    ("", False, False),
    ("                          Defendant.", False, False),
]

CAPTION_RIGHT = [
    ("Case No. 4:26-cv-05953-ASK", False, False),
    ("", False, False),
    ("PLAINTIFF'S OPPOSITION TO", True, False),
    ("DEFENDANT'S MOTION TO", True, False),
    ("DISMISS FIRST AMENDED", True, False),
    ("COMPLAINT AND/OR MOTION", True, False),
    ("TO STRIKE PORTIONS OF THE", True, False),
    ("FIRST AMENDED COMPLAINT", True, False),
    ("", False, False),
    ("Date: September 16, 2026", False, False),
    ("Time: 1:30 p.m.", False, False),
    ("Judge: Mag. Ajay S. Krishnan", False, False),
    ("", False, False),
    ("Action Filed: June 17, 2026", False, False),
]

# Longest-first so "Bd. of Cnty. Comm'rs v. Umbehr" beats shorter prefixes.
CASE_ITALICS = sorted(
    [
        "Ashcroft v. Iqbal",
        "Bd. of Cnty. Comm'rs v. Umbehr",
        "Bd. of Regents v. Roth",
        "Bell Atl. Corp. v. Twombly",
        "Borough of Duryea v. Guarnieri",
        "Bureerong v. Uvawas",
        "Capp v. Cnty. of San Diego",
        "Catholic Charities CYO v. Chertoff",
        "County of Sacramento v. Lewis",
        "District of Columbia v. Wesby",
        "Erickson v. Pardus",
        "Ex parte Young",
        "Ford v. City of Yakima",
        "Garity v. APWU Nat'l Lab. Org.",
        "Goldberg v. Kelly",
        "Hartman v. Moore",
        "Hebbe v. Pliler",
        "Hope v. Pelzer",
        "Kay v. Ehrler",
        "Keates v. Koile",
        "Khoja v. Orexigen Therapeutics, Inc.",
        "Knievel v. ESPN",
        "Lee v. City of Los Angeles",
        "Lopez v. Smith",
        "Mathews v. Eldridge",
        "Mt. Healthy City Sch. Dist. Bd. of Educ. v. Doyle",
        "Navarro v. Block",
        "Nieves v. Bartlett",
        "Pearson v. Callahan",
        "Perez Perez v. Wolf",
        "Perry v. Sindermann",
        "Pratt v. Rowland",
        "Shanks v. Dressel",
        "Smith v. Wade",
        "Whittlestone, Inc. v. Handi-Craft Co.",
        "Wilkerson v. Butler",
        "Winter v. Nat. Res. Def. Council, Inc.",
        "Withrow v. Larkin",
        "Twombly",
        "Iqbal",
        "Capp",
        "Ford",
        "Wesby",
    ],
    key=len,
    reverse=True,
)


def italicize_cases(text: str) -> str:
    """Wrap known case names in <<i:...>> once each, longest first."""
    out = text
    for name in CASE_ITALICS:
        # Skip if already marked
        if f"<<i:{name}>>" in out:
            continue
        # Avoid matching inside already-wrapped segments by simple replace
        # of the bare name only when not preceded by <<i:
        pattern = re.compile(re.escape(name))
        # Replace only first occurrence clusters carefully: replace all bare
        # occurrences that aren't already inside <<i:...>>
        parts = re.split(r"(<<i:[^>]+>>)", out)
        rebuilt = []
        for part in parts:
            if part.startswith("<<i:"):
                rebuilt.append(part)
            else:
                rebuilt.append(pattern.sub(f"<<i:{name}>>", part))
        out = "".join(rebuilt)
    return out


def classify_body(paras: list[str]) -> list[tuple[str, str]]:
    """Convert Word paragraphs from I. INTRODUCTION onward into CONTENT."""
    content: list[tuple[str, str]] = []
    started = False
    for raw in paras:
        t = raw.strip()
        if not started:
            if t.startswith("I. INTRODUCTION"):
                started = True
            else:
                continue
        if not t:
            continue
        # Skip TOC / TOA residue if any leaked
        if t in ("TABLE OF CONTENTS", "TABLE OF AUTHORITIES", "Cases", "Statutes and Rules"):
            continue
        if t.startswith("Dated:") or t.startswith("Respectfully") or set(t) <= {"_"}:
            # signature handled separately
            continue
        if t in ("BRENDAN NGEHSI NEWANFORBI", "Plaintiff, In Pro Per"):
            continue

        if re.match(r"^(I{1,3}|IV)\.\s+", t):
            content.append(("HEADER", t))
        elif re.match(r"^[A-H]\.\s+", t):
            content.append(("SUBHEAD", t))
        elif re.match(r"^\d+\.\s+[A-Z]", t) and len(t) < 120:
            # short numbered subheads like "1. Defendant Conflates..."
            content.append(("SUBHEAD", t))
        elif t.startswith("1 ") and "Civil L.R." in t:
            content.append(("FOOTNOTE", t))
        elif re.match(r"^\d+\s+Plaintiff also notes", t):
            content.append(("FOOTNOTE", t))
        else:
            content.append(("PARA", italicize_cases(t)))
    return content


def signature_block() -> str:
    return (
        "Dated: August 27, 2026\n"
        "\n"
        "Respectfully submitted,\n"
        "\n"
        "___________________________________\n"
        "BRENDAN NGEHSI NEWANFORBI\n"
        "Plaintiff, In Pro Per"
    )


def render(out_path: Path, content: list[tuple[str, str]]) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    d = PleadingPaper(str(out_path), doc_title_footer=DOC_TITLE_FOOTER)

    # Attorney block -- same six lines, compressed spacing (portfolio pattern).
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

    # Skip separate TOC/TOA on pleading paper (space); body is the filing meat.
    # Optionally note hearing info once.
    d.write_wrapped(
        "Hearing Date: September 16, 2026, at 1:30 p.m., before Magistrate Judge "
        "Ajay S. Krishnan, United States District Court for the Northern District "
        "of California.",
        first_indent=0,
    )
    d.blank_line()

    for c_type, text in content:
        if c_type == "HEADER":
            d.ensure_space(4)
            d.write_line(text, bold=True, center=True)
            d.blank_line()
        elif c_type == "SUBHEAD":
            lines = text.split("\n")
            d.ensure_space(len(lines) + 3)
            for line in lines:
                d.write_line(line, bold=True, center=False)
            d.blank_line()
        elif c_type == "PARA":
            d.write_wrapped(text, first_indent=36)
            d.blank_line()
        elif c_type == "FOOTNOTE":
            d.write_wrapped(text, size=10, first_indent=18)
            d.blank_line()
        elif c_type == "LIST_ITEM":
            d.write_wrapped(text, indent=36, first_indent=0)
            d.blank_line()

    # Signature with universal stamp
    d.ensure_space(8)
    for line in signature_block().split("\n"):
        if line.startswith("_") and os.path.isfile(SIGNATURE_PATH):
            d.draw_signature_image(
                SIGNATURE_PATH,
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

    d.save()
    print(f"Wrote {out_path} ({out_path.stat().st_size} bytes, {d.page_num} pages)")


def main() -> None:
    if not SOURCE_DOCX.is_file():
        raise SystemExit(f"Missing source draft: {SOURCE_DOCX}")
    if not Path(SIGNATURE_PATH).is_file():
        raise SystemExit(f"Missing universal signature: {SIGNATURE_PATH}")

    paras = [p.text for p in Document(str(SOURCE_DOCX)).paragraphs]
    content = classify_body(paras)
    if not content:
        raise SystemExit("No body content extracted from source docx")
    print(f"Extracted {len(content)} content blocks from {SOURCE_DOCX.name}")

    for out in OUT_PATHS:
        render(out, content)

    if not FILED_STATUS:
        print("NOTE: FILED_STATUS is False -- not yet e-filed/served.")


if __name__ == "__main__":
    main()
