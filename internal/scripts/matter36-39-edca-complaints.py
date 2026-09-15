#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Render Matters 36–39 E.D. Cal. complaints from the v4 review drafts.

Authoritative prose lives in:

  internal/docs/matter-36/EDCA_FEDERAL_COMPLAINT_REVIEW_DRAFT.md
  internal/docs/matter-37/EDCA_FEDERAL_COMPLAINT_REVIEW_DRAFT.md
  internal/docs/matter-38/FILING_COMPLAINT_REVIEW_DRAFT.md
  internal/docs/matter-39/EDCA_FEDERAL_COMPLAINT_REVIEW_DRAFT.md

File-ready PDF: September 15, 2026 date, canonical signature, no review-draft
banner, no Lerma in the caption. Does not reprint the San Joaquin verified
complaints (wrong court).

    python3 internal/scripts/matter36-39-edca-complaints.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR / "lib"))
sys.path.insert(0, str(SCRIPT_DIR))

from pleading_paper import CONTENT_LEFT, CONTENT_WIDTH, PleadingPaper  # noqa: E402
from signature_stamp import SIGNATURE_NATIVE_PX, SIGNATURE_PATH  # noqa: E402

ROOT = SCRIPT_DIR.parents[1]
DOCS = ROOT / "internal/public/documents"
EXEC_DATE = "September 15, 2026"
SIG_LINE = "___________________________________"
SIGNOFF_NAME = "BRENDAN NGWA NFORBI"
SIGNOFF_ROLE = "Plaintiff, In Propria Persona"

COURT_LINE1 = "UNITED STATES DISTRICT COURT"
COURT_LINE2 = "EASTERN DISTRICT OF CALIFORNIA -- SACRAMENTO DIVISION"

PLAINTIFF_BLOCK = [
    ("BRENDAN NGWA NFORBI", "Times-Bold", 12),
    ("Plaintiff, In Propria Persona", "Times-Roman", 12),
    ("1455 Cat Tail Drive", "Times-Roman", 12),
    ("Stockton, CA 95204", "Times-Roman", 12),
    ("Telephone: (209) 801-4442", "Times-Roman", 12),
    ("E-mail: bnn.cdl@gmail.com", "Times-Roman", 12),
]

_BOLD = re.compile(r"\*\*(.+?)\*\*")
_NUMBERED = re.compile(r"^(\d+)\.\s+(.*)$")
_LETTERED = re.compile(r"^([A-G])\.\s+(.*)$")
_H2_HEADER = re.compile(
    r"^(INTRODUCTION|JURISDICTION|PARTIES|TIMELINESS|FACTUAL|"
    r"FIRST |SECOND |THIRD |PRAYER|DEMAND FOR)",
    re.I,
)


def _inline(text: str) -> str:
    return _BOLD.sub(lambda m: f"<<b:{m.group(1)}>>", text)


SPECS = {
    36: {
        "draft": ROOT / "internal/docs/matter-36/EDCA_FEDERAL_COMPLAINT_REVIEW_DRAFT.md",
        "filename": (
            "Complaint - Ngwa Nforbi v. AT&T Mobility Services LLC "
            "(E.D. Cal.) (Sep 15 2026).pdf"
        ),
        "footer": (
            "COMPLAINT FOR DAMAGES -- NGWA NFORBI v. AT&T MOBILITY "
            "SERVICES LLC (E.D. Cal.)"
        ),
        "caption_left": [
            ("BRENDAN NGWA NFORBI,", True, False),
            ("", False, False),
            ("                          Plaintiff,", False, False),
            ("", False, False),
            ("       v.", False, False),
            ("", False, False),
            ("AT&T MOBILITY SERVICES LLC,", True, False),
            ("a Delaware limited liability", True, False),
            ("company,", True, False),
            ("", False, False),
            ("                          Defendant.", False, False),
        ],
        "caption_right": [
            ("Case No. ________________", False, False),
            ("", False, False),
            ("COMPLAINT FOR DAMAGES", True, False),
            ("", False, False),
            ("(1) FCRA, 15 U.S.C.", False, False),
            ("      § 1681b(b)(3)(A);", False, False),
            ("(2) ICRAA, Civ. Code", False, False),
            ("      §§ 1786.40, 1786.50;", False, False),
            ("(3) Penal Code", False, False),
            ("      § 290.46(j)", False, False),
            ("", False, False),
            ("[Jury Trial Demanded]", False, True),
        ],
    },
    37: {
        "draft": ROOT / "internal/docs/matter-37/EDCA_FEDERAL_COMPLAINT_REVIEW_DRAFT.md",
        "filename": (
            "Complaint - Ngwa Nforbi v. Home Depot U.S.A., Inc. "
            "(E.D. Cal.) (Sep 15 2026).pdf"
        ),
        "footer": (
            "COMPLAINT FOR DAMAGES -- NGWA NFORBI v. HOME DEPOT U.S.A., "
            "INC. (E.D. Cal.)"
        ),
        "caption_left": [
            ("BRENDAN NGWA NFORBI,", True, False),
            ("", False, False),
            ("                          Plaintiff,", False, False),
            ("", False, False),
            ("       v.", False, False),
            ("", False, False),
            ("HOME DEPOT U.S.A., INC.,", True, False),
            ("a Delaware corporation,", True, False),
            ("", False, False),
            ("                          Defendant.", False, False),
        ],
        "caption_right": [
            ("Case No. ________________", False, False),
            ("", False, False),
            ("COMPLAINT FOR DAMAGES", True, False),
            ("", False, False),
            ("Penal Code § 290.46(j)", False, False),
            ("(2)(E), (j)(4)(A)", False, False),
            ("", False, False),
            ("[Jury Trial Demanded]", False, True),
        ],
    },
    38: {
        "draft": ROOT / "internal/docs/matter-38/FILING_COMPLAINT_REVIEW_DRAFT.md",
        "filename": (
            "Complaint - Ngwa Nforbi v. Swift Transportation Co. of "
            "Arizona LLC (E.D. Cal.) (Sep 15 2026).pdf"
        ),
        "footer": (
            "COMPLAINT FOR DAMAGES -- NGWA NFORBI v. SWIFT TRANSPORTATION "
            "CO. OF ARIZONA LLC (E.D. Cal.)"
        ),
        "caption_left": [
            ("BRENDAN NGWA NFORBI,", True, False),
            ("", False, False),
            ("                          Plaintiff,", False, False),
            ("", False, False),
            ("       v.", False, False),
            ("", False, False),
            ("SWIFT TRANSPORTATION CO. OF", True, False),
            ("ARIZONA LLC, a Delaware limited", True, False),
            ("liability company, d/b/a SWIFT", True, False),
            ("TRANSPORTATION,", True, False),
            ("", False, False),
            ("                          Defendant.", False, False),
        ],
        "caption_right": [
            ("Case No. ________________", False, False),
            ("", False, False),
            ("COMPLAINT FOR DAMAGES", True, False),
            ("", False, False),
            ("(1) Cal. Penal Code", False, False),
            ("      section 290.46(j);", False, False),
            ("(2) ICRAA, Cal. Civ. Code", False, False),
            ("      sections 1786.40, 1786.50;", False, False),
            ("(3) UCL, Cal. Bus. & Prof.", False, False),
            ("      Code section 17200", False, False),
            ("", False, False),
            ("[Jury Trial Demanded]", False, True),
        ],
    },
    39: {
        "draft": ROOT / "internal/docs/matter-39/EDCA_FEDERAL_COMPLAINT_REVIEW_DRAFT.md",
        "filename": (
            "Complaint - Ngwa Nforbi v. Best Buy Co., Inc. "
            "(E.D. Cal.) (Sep 15 2026).pdf"
        ),
        "footer": (
            "COMPLAINT FOR DAMAGES -- NGWA NFORBI v. BEST BUY CO., INC. "
            "(E.D. Cal.)"
        ),
        "caption_left": [
            ("BRENDAN NGWA NFORBI,", True, False),
            ("", False, False),
            ("                          Plaintiff,", False, False),
            ("", False, False),
            ("       v.", False, False),
            ("", False, False),
            ("BEST BUY CO., INC.,", True, False),
            ("a Minnesota corporation,", True, False),
            ("", False, False),
            ("                          Defendant.", False, False),
        ],
        "caption_right": [
            ("Case No. ________________", False, False),
            ("", False, False),
            ("COMPLAINT FOR DAMAGES", True, False),
            ("", False, False),
            ("Penal Code § 290.46(j)", False, False),
            ("(2)(E), (j)(4)(A)", False, False),
            ("", False, False),
            ("[Jury Trial Demanded]", False, True),
        ],
    },
}


def complaint_path(number: int, out_dir: Path | None = None) -> Path:
    spec = SPECS[number]
    dest = out_dir or (DOCS / f"matter-{number}" / "edca")
    return dest / spec["filename"]


def _body_source_lines(markdown: str) -> list[str]:
    lines = markdown.splitlines()
    start = None
    for i, line in enumerate(lines):
        low = line.lower()
        if "alleges" in low and "plaintiff" in low:
            start = i
            break
    if start is None:
        raise SystemExit("Could not find the 'alleges' lead-in in a draft")
    out: list[str] = []
    for line in lines[start:]:
        stripped = line.strip()
        if stripped.startswith("Dated:"):
            break
        if stripped.startswith("Respectfully submitted"):
            break
        if stripped in ("---",):
            continue
        out.append(line.rstrip())
    return out


def _heading_kind(hashes: str, title: str) -> str:
    if hashes == "#":
        return "HEADER"
    if hashes == "###":
        return "SUBHEAD"
    if title == title.upper() and any(ch.isalpha() for ch in title):
        return "HEADER"
    if _H2_HEADER.match(title):
        return "HEADER"
    return "SUBHEAD"


def parse_blocks(markdown: str) -> list[tuple[str, str]]:
    lines = _body_source_lines(markdown)
    blocks: list[tuple[str, str]] = []
    i = 0
    while i < len(lines):
        stripped = lines[i].strip()
        if not stripped:
            i += 1
            continue
        heading = re.match(r"^(#{1,3})\s+(.*)$", stripped)
        if heading:
            kind = _heading_kind(heading.group(1), heading.group(2).strip())
            blocks.append((kind, heading.group(2).strip()))
            i += 1
            continue
        collected = [stripped]
        i += 1
        while i < len(lines):
            nxt = lines[i].strip()
            if not nxt:
                break
            if re.match(r"^#{1,3}\s+", nxt):
                break
            if _NUMBERED.match(nxt) or _LETTERED.match(nxt):
                break
            if nxt.startswith("Dated:") or nxt.startswith("Respectfully"):
                break
            collected.append(nxt)
            i += 1
        text = " ".join(collected)
        if _LETTERED.match(text):
            blocks.append(("LIST_ITEM", text))
        else:
            blocks.append(("PARA", text))
    return blocks


def _write_header(d: PleadingPaper, text: str) -> None:
    width = d.c.stringWidth(text, "Times-Bold", 12)
    d.ensure_space(4)
    if width > CONTENT_WIDTH - 8:
        d.write_wrapped(_inline(text), bold=True, first_indent=0)
    else:
        d.write_line(text, bold=True, center=True)
    d.blank_line()


def _write_subhead(d: PleadingPaper, text: str) -> None:
    d.ensure_space(3)
    width = d.c.stringWidth(text, "Times-Bold", 12)
    if width > CONTENT_WIDTH - 8:
        d.write_wrapped(_inline(text), bold=True, first_indent=0)
    else:
        d.write_line(text, bold=True)
    d.blank_line()


def _signature_block(d: PleadingPaper) -> None:
    d.ensure_space(8)
    d.write_line(f"Dated: {EXEC_DATE}")
    d.blank_line()
    d.write_respectfully_submitted()
    d.draw_signature_image(
        SIGNATURE_PATH,
        SIGNATURE_NATIVE_PX[0],
        SIGNATURE_NATIVE_PX[1],
        SIG_LINE,
    )
    d.write_line(SIG_LINE, right=True, right_margin_offset=20)
    d.write_line(SIGNOFF_NAME, right=True, right_margin_offset=20)
    d.write_line(SIGNOFF_ROLE, right=True, right_margin_offset=20)


def build_complaint(number: int, out_dir: Path | None = None) -> Path:
    spec = SPECS[number]
    draft = spec["draft"]
    if not draft.is_file():
        raise SystemExit(f"Missing complaint draft: {draft}")
    if not Path(SIGNATURE_PATH).is_file():
        raise SystemExit(f"Missing signature: {SIGNATURE_PATH}")
    out = complaint_path(number, out_dir)
    out.parent.mkdir(parents=True, exist_ok=True)
    markdown = draft.read_text(encoding="utf-8")
    if re.search(r"Lerma", markdown, re.I):
        raise SystemExit(f"{draft} still names Lerma — v4 forbids that in the pleading")
    blocks = parse_blocks(markdown)
    if not blocks:
        raise SystemExit(f"No pleading body parsed from {draft}")

    d = PleadingPaper(str(out), doc_title_footer=spec["footer"])
    c = d.c
    atty_y = d._line_y(0)
    for i, (txt, font_name, size) in enumerate(PLAINTIFF_BLOCK):
        c.setFont(font_name, size)
        c.drawString(CONTENT_LEFT, atty_y - i * 15, txt)
    d.current_line = 4
    d.blank_line()
    d.write_line(COURT_LINE1, bold=True, center=True)
    d.write_line(COURT_LINE2, bold=True, center=True)
    d.blank_line()
    d.draw_caption_block(
        spec["caption_left"],
        spec["caption_right"],
        caption_size=10,
        tight_lh=13,
        boxed=True,
    )
    d.blank_line()

    for kind, text in blocks:
        if kind == "HEADER":
            _write_header(d, text)
        elif kind == "SUBHEAD":
            _write_subhead(d, text)
        elif kind == "LIST_ITEM":
            d.write_wrapped(_inline(text), indent=36, first_indent=0)
            d.blank_line()
        elif kind == "PARA":
            first = 0 if not _NUMBERED.match(text) else 36
            d.write_wrapped(_inline(text), first_indent=first)
            d.blank_line()
        else:
            raise ValueError(f"unknown block kind {kind!r}")

    _signature_block(d)
    d.save()
    print(f"Wrote {out}")
    return out


def build_all(out_dir_for: dict[int, Path] | None = None) -> dict[int, Path]:
    written: dict[int, Path] = {}
    for number in SPECS:
        dest = None if not out_dir_for else out_dir_for.get(number)
        written[number] = build_complaint(number, dest)
    return written


def main() -> None:
    build_all()


if __name__ == "__main__":
    main()
