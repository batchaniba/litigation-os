#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Matter 40 — N.D. Cal. complaint PDF (premier review draft for print).

Source of truth:
  internal/docs/matter-40/ND_CAL_COMPLAINT_REVIEW_DRAFT_V2.md

Strips the internal MTD memo / supporting-docs notes. Plaintiff signs.
No REVIEW DRAFT banner on the caption. No phone/email on the close
(caption address block matches the markdown draft). No division line —
the Northern District designates division. No exhibits attached.

    python3 internal/scripts/matter40-ndcal-complaint.py
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
sys.path.insert(0, str(SCRIPT_DIR / "lib"))

from pleading_paper import CONTENT_LEFT, PleadingPaper  # noqa: E402
from signature_stamp import SIGNATURE_NATIVE_PX, SIGNATURE_PATH  # noqa: E402

ROOT = SCRIPT_DIR.parents[1]
MD_PATH = ROOT / "internal/docs/matter-40/ND_CAL_COMPLAINT_REVIEW_DRAFT_V2.md"
DEFAULT_OUT = (
    ROOT
    / "internal/public/documents/matter-40"
    / "Complaint - Ngwa Nforbi v Uber Technologies Inc "
    "(N.D. Cal.) (Sep 24 2026).pdf"
)

DOC_TITLE_FOOTER = (
    "COMPLAINT FOR DAMAGES -- NGWA NFORBI v. UBER TECHNOLOGIES, INC., ET AL. "
    "(N.D. Cal.)"
)

EXEC_DATE = "September 24, 2026"
SIG_LINE = "___________________________________"

COURT_LINE1 = "UNITED STATES DISTRICT COURT"
COURT_LINE2 = "NORTHERN DISTRICT OF CALIFORNIA"

PLAINTIFF_BLOCK = [
    ("BRENDAN NGWA NFORBI", "Times-Bold", 12),
    ("Plaintiff, In Propria Persona", "Times-Roman", 12),
    ("1455 Cat Tail Drive", "Times-Roman", 12),
    ("Stockton, California 95204", "Times-Roman", 12),
]

CAPTION_LEFT = [
    ("BRENDAN NGWA NFORBI,", True, False),
    ("", False, False),
    ("                          Plaintiff,", False, False),
    ("", False, False),
    ("       v.", False, False),
    ("", False, False),
    ("UBER TECHNOLOGIES, INC., a", True, False),
    ("Delaware corporation;", True, False),
    ("TASKUS HOLDINGS, INC., a", True, False),
    ("Delaware corporation;", True, False),
    ("TASKUS USA, LLC, a Delaware", True, False),
    ("limited liability company; and", True, False),
    ("DOES 1 through 20, inclusive,", True, False),
    ("", False, False),
    ("                          Defendants.", False, False),
]

CAPTION_RIGHT = [
    ("Case No. ________________", False, False),
    ("", False, False),
    ("COMPLAINT FOR DAMAGES", True, False),
    ("", False, False),
    ("(1) FCRA, 15 U.S.C.", False, False),
    ("      section 1681b(b)(2)(A);", False, False),
    ("(2) ICRAA, Civ. Code", False, False),
    ("      sections 1786.16,", False, False),
    ("      1786.50;", False, False),
    ("(3) FCRA, 15 U.S.C.", False, False),
    ("      section 1681b(b)(3)(A);", False, False),
    ("(4) Penal Code section", False, False),
    ("      290.46(j)(2)(E), (j)(4)(A);", False, False),
    ("(5) ICRAA, Civ. Code", False, False),
    ("      sections 1786.40,", False, False),
    ("      1786.50", False, False),
    ("", False, False),
    ("DEMAND FOR JURY TRIAL", True, False),
]

SIGNATURE_BLOCK = None  # dated + house stamp drawn in main()


def _strip_md(s: str) -> str:
    s = s.replace("\u2014", "--").replace("\u2013", "-")
    s = s.replace("\u2018", "'").replace("\u2019", "'")
    s = s.replace("\u201c", '"').replace("\u201d", '"')
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"`([^`]+)`", r"\1", s)
    s = s.replace("<b>", "").replace("</b>", "")  # PleadingPaper uses ** via _parse
    # Restore bold markers PleadingPaper understands
    s = re.sub(r"\*\*(.+?)\*\*", r"**\1**", s)
    return s.strip()


def _md_to_bold_markers(s: str) -> str:
    """Convert **bold** to PleadingPaper <<b:...>> markers."""
    s = s.replace("\u2014", "--").replace("\u2013", "-")
    s = s.replace("\u2018", "'").replace("\u2019", "'")
    s = s.replace("\u201c", '"').replace("\u201d", '"')
    s = re.sub(r"`([^`]+)`", r"\1", s)
    s = re.sub(r"\*\*(.+?)\*\*", lambda m: f"<<b:{m.group(1)}>>", s)
    return s.strip()


def extract_pleading_body(md: str) -> str:
    """From address block through signature; drop internal memo + exhibit notes."""
    # Prefer the pleading that starts after the first horizontal rule following memo
    marker = "BRENDAN NGWA NFORBI  \nPlaintiff, In Propria Persona"
    idx = md.find(marker)
    if idx < 0:
        idx = md.find("BRENDAN NGWA NFORBI\nPlaintiff, In Propria Persona")
    if idx < 0:
        raise SystemExit("could not find pleading address block in markdown")
    body = md[idx:]
    # Cut at exhibit list / second --- after signature
    for cut in (
        "\n---\n\n## Document inventory",
        "\n## Document inventory",
        "\n---\n\n## Exhibit list",
        "\n## Exhibit list",
        "\n## Exhibits (filed",
        "\n## Filing packet",
        "\n## Supporting documents",
        "\n# INTERNAL POST-DRAFT",
    ):
        cidx = body.find(cut)
        if cidx > 0:
            body = body[:cidx]
            break
    return body


def parse_content(body: str) -> list[tuple[str, str]]:
    """Return CONTENT list of (kind, text). Skip address/court/caption — drawn separately."""
    lines = body.splitlines()
    # Skip through DEMAND FOR JURY TRIAL / alleges intro until Nature section
    start = 0
    for i, line in enumerate(lines):
        if line.startswith("# I. NATURE OF THE ACTION"):
            start = i
            break
    lines = lines[start:]

    content: list[tuple[str, str]] = [
        (
            "NOTICE",
            "Plaintiff BRENDAN NGWA NFORBI, appearing in propria persona, alleges:",
        )
    ]

    buf: list[str] = []
    mode = None  # PARA | HEADER | SUBHEAD | LIST | QUOTE

    def flush():
        nonlocal buf, mode
        if not buf:
            mode = None
            return
        text = _md_to_bold_markers(" ".join(x.strip() for x in buf if x.strip()))
        if mode == "HEADER":
            content.append(("HEADER", text.replace("# ", "").replace("#", "")))
        elif mode == "SUBHEAD":
            content.append(("SUBHEAD", text.replace("## ", "").replace("### ", "")))
        elif mode == "LIST":
            content.append(("LIST_ITEM", text))
        elif mode == "QUOTE":
            content.append(("PARA", text))
        else:
            # Drop bare "Plaintiff ... alleges:" if duplicated
            if not text.startswith("Plaintiff BRENDAN NGWA NFORBI, appearing"):
                content.append(("PARA", text))
        buf = []
        mode = None

    for raw in lines:
        line = raw.rstrip()
        if not line.strip():
            flush()
            continue
        if re.match(r"^# (I|V?I{0,3}|IX|X{0,3}V?I{0,3})\.", line):
            flush()
            title = line.lstrip("# ").strip()
            content.append(("HEADER", title))
            continue
        if line.startswith("## ") or line.startswith("### "):
            flush()
            content.append(("SUBHEAD", line.lstrip("# ").strip()))
            continue
        if line.startswith("# "):
            flush()
            content.append(("HEADER", line.lstrip("# ").strip()))
            continue
        if line.startswith("> "):
            flush()
            mode = "QUOTE"
            buf.append(line[2:].strip())
            continue
        if line.startswith("- "):
            flush()
            mode = "LIST"
            buf.append("\u2022  " + line[2:].strip())
            continue
        if line.startswith("Dated:") or line.startswith("Respectfully") or line.startswith("___"):
            flush()
            continue
        if line.strip() in {"BRENDAN NGWA NFORBI", "Plaintiff, In Propria Persona"}:
            flush()
            continue
        if line.strip().startswith("Dated: September"):
            flush()
            continue
        if mode is None:
            mode = "PARA"
        buf.append(line)

    flush()

    # Prayer / WHEREFORE as paragraphs already; ensure jury demand present
    return content


def build_content_from_md() -> list[tuple[str, str]]:
    md = MD_PATH.read_text(encoding="utf-8")
    body = extract_pleading_body(md)
    return parse_content(body)


def main() -> None:
    out = Path(os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else DEFAULT_OUT))
    out.parent.mkdir(parents=True, exist_ok=True)
    content = build_content_from_md()

    d = PleadingPaper(str(out), doc_title_footer=DOC_TITLE_FOOTER)

    c = d.c
    atty_y = d._line_y(0)
    for i, (txt, fn, sz) in enumerate(PLAINTIFF_BLOCK):
        c.setFont(fn, sz)
        c.drawString(CONTENT_LEFT, atty_y - i * 15, txt)
    d.current_line = 4
    d.blank_line()

    d.write_line(COURT_LINE1, bold=True, center=True)
    d.write_line(COURT_LINE2, bold=True, center=True)
    d.blank_line()

    d.draw_caption_block(
        CAPTION_LEFT, CAPTION_RIGHT, caption_size=9, tight_lh=12, boxed=True
    )
    d.blank_line()

    for kind, text in content:
        if kind == "NOTICE":
            d.ensure_space(4)
            d.write_wrapped(text, bold=True, first_indent=0)
            d.blank_line()
        elif kind == "HEADER":
            lines = [ln for ln in text.split("\n") if ln.strip()]
            d.ensure_space(len(lines) + 2)
            for line in lines:
                # Keep short Roman numerals centered; wrap long titles instead of truncating.
                if len(line) <= 48:
                    d.write_line(line, bold=True, center=True)
                else:
                    d.write_wrapped(f"<<b:{line}>>", first_indent=0, indent=0)
            d.blank_line()
        elif kind == "SUBHEAD":
            d.ensure_space(3)
            d.write_line(text, bold=True, center=True)
            d.blank_line()
        elif kind == "PARA":
            d.write_wrapped(text, first_indent=36)
            d.blank_line()
        elif kind == "LIST_ITEM":
            d.write_wrapped(text, indent=18, first_indent=0)
            d.blank_line()
        else:
            raise ValueError(f"unknown content kind {kind!r}")

    if not Path(SIGNATURE_PATH).is_file():
        raise SystemExit(f"Missing house signature: {SIGNATURE_PATH}")

    d.ensure_space(10)
    d.write_line(f"Dated: {EXEC_DATE}")
    d.blank_line()
    d.write_respectfully_submitted()
    d.draw_signature_image(
        SIGNATURE_PATH,
        SIGNATURE_NATIVE_PX[0],
        SIGNATURE_NATIVE_PX[1],
        SIG_LINE,
        width=220,
        x_offset=15,
    )
    d.write_line(SIG_LINE, right=True, right_margin_offset=20)
    d.write_line("BRENDAN NGWA NFORBI", bold=True, right=True, right_margin_offset=20)
    d.write_line("Plaintiff, In Propria Persona", right=True, right_margin_offset=20)

    d.save()
    print(f"Wrote {out}")
    print(f"Pages: {d.page_num}")
    print(f"Dated: {EXEC_DATE}; house signature affixed from {SIGNATURE_PATH}")


if __name__ == "__main__":
    main()
