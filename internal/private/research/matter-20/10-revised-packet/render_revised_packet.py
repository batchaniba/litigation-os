#!/usr/bin/env python3
"""Render Matter 20 revised writ papers onto CRC 2.100 pleading paper.

Research draft only. Does not file, serve, or email.

    python3 internal/private/research/matter-20/10-revised-packet/render_revised_packet.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
sys.path.insert(0, str(REPO / "internal" / "scripts" / "lib"))

from pleading_paper import PleadingPaper  # noqa: E402

CASE_NO = "26CV191136"
FOOTER_CASE = "NEWANFORBI v. CHP, 26CV191136"

CAPTION_LEFT = [
    ("BRENDAN NGEHSI NEWANFORBI,", True, False),
    ("", False, False),
    ("                          Petitioner,", False, False),
    ("", False, False),
    ("       v.", False, False),
    ("", False, False),
    ("CALIFORNIA HIGHWAY PATROL;", True, False),
    ("G. SERRATO, in his official", True, False),
    ("capacity as Captain and", True, False),
    ("Commander of CHP Dublin Area,", True, False),
    ("", False, False),
    ("                          Respondents.", False, False),
]

HEARING_RIGHT = [
    ("Hon. Jenna M. Whitman, Dept. 25", False, False),
    ("Hearing: January 8, 2027, 9:00 a.m.", False, False),
    ("Reservation No. 958052306492", False, False),
    ("Action filed May 29, 2026", False, False),
]


def right_caption(*title_lines: str):
    rows = [("Case No. " + CASE_NO, False, False), ("", False, False)]
    for i, line in enumerate(title_lines):
        rows.append((line, True, False))
    rows.append(("", False, False))
    rows.extend(HEARING_RIGHT)
    return rows


PAPERS = {
    "PETITIONER’S NOTICE OF MOTION AND MOTION FOR ISSUANCE OF A PEREMPTORY WRIT OF MANDATE": {
        "footer": "NOTICE OF MOTION -- " + FOOTER_CASE,
        "right": right_caption(
            "PETITIONER'S NOTICE OF MOTION",
            "AND MOTION FOR ISSUANCE OF",
            "PEREMPTORY WRIT OF MANDATE",
        ),
        "center_title": False,
    },
    "MEMORANDUM OF POINTS AND AUTHORITIES": {
        "footer": "MEMORANDUM OF POINTS AND AUTHORITIES -- " + FOOTER_CASE,
        "right": right_caption(
            "MEMORANDUM OF POINTS AND",
            "AUTHORITIES",
        ),
        "center_title": True,
        "track_mpa": True,
    },
    "DECLARATION OF BRENDAN NGEHSI NEWANFORBI": {
        "footer": "DECLARATION OF B.N. NEWANFORBI -- " + FOOTER_CASE,
        "right": right_caption(
            "DECLARATION OF BRENDAN",
            "NGEHSI NEWANFORBI IN SUPPORT",
            "OF MOTION FOR PEREMPTORY",
            "WRIT OF MANDATE",
        ),
        "center_title": True,
    },
    "[PROPOSED] ORDER ON MOTION FOR PEREMPTORY WRIT OF MANDATE": {
        "footer": "[PROPOSED] ORDER -- " + FOOTER_CASE,
        "right": right_caption(
            "[PROPOSED] ORDER ON MOTION",
            "FOR PEREMPTORY WRIT OF",
            "MANDATE",
        ),
        "center_title": True,
        "no_attorney_close": True,
    },
    "PROOF OF SERVICE": {
        "footer": "PROOF OF SERVICE -- " + FOOTER_CASE,
        "right": right_caption("PROOF OF SERVICE"),
        "center_title": True,
        "no_attorney_close": True,
    },
    "PETITIONER’S REQUEST FOR JUDICIAL NOTICE": {
        "footer": "REQUEST FOR JUDICIAL NOTICE -- " + FOOTER_CASE,
        "right": right_caption("PETITIONER'S REQUEST FOR", "JUDICIAL NOTICE"),
        "center_title": True,
    },
    "PETITIONER’S NOTICE OF LODGING OF ADMINISTRATIVE AND PRODUCED RECORD": {
        "footer": "NOTICE OF LODGING -- " + FOOTER_CASE,
        "right": right_caption(
            "PETITIONER'S NOTICE OF",
            "LODGING OF ADMINISTRATIVE",
            "AND PRODUCED RECORD",
        ),
        "center_title": True,
    },
}


def md_inline(text: str) -> str:
    text = text.replace("\u2019", "'").replace("\u201c", '"').replace("\u201d", '"')
    text = text.replace("\u2014", "--").replace("\u2013", "--")
    text = re.sub(r"\*\*(.+?)\*\*", r"<<b:\1>>", text)
    text = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<<i:\1>>", text)
    return text


def is_sig_line(text: str) -> bool:
    t = text.strip()
    return t.startswith("DATED:") or t.startswith("Dated:") or t.startswith("Executed on") or t.startswith("IT IS SO ORDERED") or t.startswith("JUDGE OF THE") or t.startswith("Signature of server") or t.startswith("Printed name:") or t == "BRENDAN NGEHSI NEWANFORBI" or t.startswith("Petitioner, In Propria")


def draw_attorney_block(d: PleadingPaper) -> None:
    d.write_line("BRENDAN NGEHSI NEWANFORBI", bold=True)
    d.write_line("1455 Cat Tail Drive, Stockton, CA 95204")
    d.write_line("Telephone: (209) 801-4442    Email: bnn.cdl@gmail.com")
    d.write_line("Petitioner, in propria persona")
    d.blank_line()


def start_paper(d: PleadingPaper, meta: dict, first: bool) -> None:
    if not first:
        d.start_new_page()
        d.doc_title_footer = meta["footer"]
        # footer is drawn at page start; rewrite this page's footer title
        d.start_new_page()  # consumed; we need to set footer before drawing
    d.doc_title_footer = meta["footer"]
    if first:
        # Footer already drawn on page 1 with constructor value; redraw is OK.
        pass
    draw_attorney_block(d)
    d.write_line("SUPERIOR COURT OF THE STATE OF CALIFORNIA", bold=True, center=True)
    d.write_line("COUNTY OF ALAMEDA", bold=True, center=True)
    d.blank_line()
    d.draw_caption_block(CAPTION_LEFT, meta["right"], caption_size=9, tight_lh=12, boxed=True)
    d.blank_line()


def split_docs(md: str) -> list[tuple[str, str]]:
    """Return (title, body) for each '# TITLE' document after the first --- pair."""
    # Drop research header / caption notes: keep from the first H1 that is a paper.
    lines = md.splitlines()
    docs: list[tuple[str, str]] = []
    title = None
    buf: list[str] = []
    for line in lines:
        if line.startswith("# ") and not line.startswith("# Revised") and not line.startswith("# Request") and not line.startswith("# Notice of Lodging (research"):
            if title is not None:
                docs.append((title, "\n".join(buf).strip()))
            title = line[2:].strip()
            buf = []
        elif title is not None:
            buf.append(line)
    if title is not None:
        docs.append((title, "\n".join(buf).strip()))
    return docs


def render_body(d: PleadingPaper, body: str, meta: dict, stats: dict) -> None:
    in_code = False
    in_toa_table = False
    mpa_substance_started = False
    substance_start_page = None

    blocks = re.split(r"\n\s*\n", body)
    for raw in blocks:
        raw = raw.strip()
        if not raw:
            continue
        if raw.startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        if raw.strip() in ("---", "***", "___"):
            continue

        first = raw.splitlines()[0].strip()

        if first.startswith("## Table of contents") or first.startswith("## Table of authorities") or first.startswith("### "):
            d.ensure_space(3)
            heading = first.lstrip("#").strip()
            d.write_line(heading, bold=True, center=True)
            rest = "\n".join(raw.splitlines()[1:]).strip()
            if rest:
                for row in rest.splitlines():
                    row = row.strip()
                    if not row or row.startswith("|---") or row.startswith("|---"):
                        continue
                    if row.startswith("|"):
                        cells = [c.strip() for c in row.strip("|").split("|")]
                        d.write_wrapped(md_inline("  ".join(cells)), first_indent=0, indent=12)
                    else:
                        d.write_wrapped(md_inline(row), first_indent=0)
            d.blank_line()
            continue

        if first.startswith("## "):
            if meta.get("track_mpa") and not mpa_substance_started and first.startswith("## I."):
                mpa_substance_started = True
                substance_start_page = d.page_num
            d.ensure_space(4)
            for line in _heading_lines(first[3:].strip()):
                d.write_line(line, bold=True, center=True)
            d.blank_line()
            rest = "\n".join(raw.splitlines()[1:]).strip()
            if rest:
                _write_para(d, rest)
            continue

        _write_para(d, raw)

    if meta.get("track_mpa") and substance_start_page:
        stats["mpa_substance_pages"] = d.page_num - substance_start_page + 1
        stats["mpa_last_page"] = d.page_num


def _write_para(d: PleadingPaper, raw: str) -> None:
    lines = [ln.rstrip() for ln in raw.splitlines() if ln.strip()]
    if not lines:
        return

    # Signature / date blocks
    if all(is_sig_line(ln) or ln.startswith("[ ]") or ln.startswith("Person served") or ln.startswith("Address:") or ln.startswith("E-mail") or ln.startswith("Method") or ln.startswith("I am at least") or ln.startswith("On ________") or ln.startswith("I declare under penalty") or ln.startswith("STATE OF CALIFORNIA") or ln.startswith("THE COURT FINDS") or ln.startswith("This order concerns") or ln.startswith("The clerk shall") for ln in lines) and any(is_sig_line(ln) for ln in lines):
        lead = lines[0]
        if lead.startswith("DATED") or lead.startswith("Dated") or lead.startswith("Executed") or lead.startswith("IT IS"):
            d.ensure_space(7)
        else:
            d.ensure_space(3)
        for ln in lines:
            if ln.startswith("BRENDAN NGEHSI") or ln.startswith("Petitioner, In") or ln.startswith("JUDGE OF") or ln.startswith("DATED") or ln.startswith("Dated") or ln.startswith("IT IS SO"):
                d.write_line(ln, right=True, right_margin_offset=20)
            else:
                d.write_wrapped(md_inline(ln), first_indent=0)
        d.blank_line()
        return

    # TOC / TOA / short catalog lines: keep one item per pleading line.
    cite_like = all(
        (" v. " in ln)
        or ("Code" in ln)
        or ("U.S.C." in ln)
        or ("C.F.R." in ln)
        or ("Rules of Court" in ln)
        or ln.startswith("Order ")
        or re.match(r"^[IVX]+\.\s", ln)
        for ln in lines
    )
    if len(lines) >= 2 and (cite_like or all(len(ln) < 100 for ln in lines)):
        if cite_like or any(re.match(r"^[IVX]+\.\s", ln) for ln in lines):
            for ln in lines:
                d.write_wrapped(md_inline(ln), first_indent=0, indent=18)
            d.blank_line()
            return

    joined = " ".join(ln.strip() for ln in lines)

    # Numbered / lettered lists kept line-by-line when every line is a list marker
    listish = all(re.match(r"^(\d+\.|[a-f]\.|\[\s*\]|\*\*)", ln.strip()) for ln in lines)
    if listish and len(lines) > 1:
        for ln in lines:
            d.write_wrapped(md_inline(ln.strip()), first_indent=18, indent=0)
        d.blank_line()
        return

    # Alternative headings and short headings
    if joined.startswith("**Alternative") or joined.startswith("Alternative "):
        d.ensure_space(3)
        d.write_wrapped(md_inline(joined), bold=True, first_indent=0)
        d.blank_line()
        return

    # Checkbox / POS lines
    if joined.startswith("[ ]") or joined.startswith("Person served:") or joined.startswith("Address:") or joined.startswith("E-mail") or joined.startswith("Method ("):
        d.write_wrapped(md_inline(joined), first_indent=0)
        d.blank_line()
        return

    # Declaration numbered paragraphs: "1. I am the petitioner..."
    if re.match(r"^\d+\.\s", joined):
        d.write_wrapped(md_inline(joined), first_indent=36)
        d.blank_line()
        return

    if is_sig_line(joined):
        if joined.startswith("DATED") or joined.startswith("Dated") or joined.startswith("Executed"):
            d.ensure_space(7)
        else:
            d.ensure_space(3)
        for ln in lines:
            d.write_line(md_inline(ln.strip()), right=True, right_margin_offset=20)
        d.blank_line()
        return

    d.write_wrapped(md_inline(joined), first_indent=36)
    d.blank_line()


def render_markdown(md_path: Path, out_path: Path, default_footer: str) -> dict:
    md = md_path.read_text(encoding="utf-8")
    docs = split_docs(md)
    if not docs:
        raise SystemExit(f"no papers found in {md_path}")

    first_title, _ = docs[0]
    first_meta = PAPERS[first_title]
    d = PleadingPaper(str(out_path), doc_title_footer=first_meta["footer"])
    stats = {"papers": [], "pages": 0}

    # Constructor already drew page 1 frame. Draw caption on it.
    # Re-apply attorney + caption without an extra blank page.
    draw_attorney_block(d)
    d.write_line("SUPERIOR COURT OF THE STATE OF CALIFORNIA", bold=True, center=True)
    d.write_line("COUNTY OF ALAMEDA", bold=True, center=True)
    d.blank_line()
    d.draw_caption_block(CAPTION_LEFT, first_meta["right"], caption_size=9, tight_lh=12, boxed=True)
    d.blank_line()
    if first_meta.get("center_title"):
        d.ensure_space(3)
        d.write_line(first_title.replace("PETITIONER’S", "PETITIONER'S"), bold=True, center=True)
        d.blank_line()
    render_body(d, docs[0][1], first_meta, stats)
    stats["papers"].append(first_title)

    for title, body in docs[1:]:
        meta = PAPERS[title]
        d.start_new_page()
        d.doc_title_footer = meta["footer"]
        # The frame/footer on the new page used the previous footer string.
        # Redraw footer title by patching the just-started page is hard;
        # set footer before start_new_page instead.
        stats["papers"].append(title)
        draw_attorney_block(d)
        d.write_line("SUPERIOR COURT OF THE STATE OF CALIFORNIA", bold=True, center=True)
        d.write_line("COUNTY OF ALAMEDA", bold=True, center=True)
        d.blank_line()
        d.draw_caption_block(CAPTION_LEFT, meta["right"], caption_size=9, tight_lh=12, boxed=True)
        d.blank_line()
        if meta.get("center_title"):
            d.ensure_space(3)
            d.write_line(title.replace("PETITIONER’S", "PETITIONER'S"), bold=True, center=True)
            d.blank_line()
        render_body(d, body, meta, stats)

    d.save()
    stats["pages"] = d.page_num
    stats["out"] = str(out_path)
    return stats


def _fix_footer_timing(md_path: Path, out_path: Path) -> dict:
    """Render with footer set before each new paper's page is drawn."""
    md = md_path.read_text(encoding="utf-8")
    docs = split_docs(md)
    if not docs:
        raise SystemExit(f"no papers found in {md_path}")

    stats: dict = {"papers": [], "mpa_substance_pages": None}
    first_title, first_body = docs[0]
    first_meta = PAPERS[first_title]
    d = PleadingPaper(str(out_path), doc_title_footer=first_meta["footer"])
    draw_attorney_block(d)
    d.write_line("SUPERIOR COURT OF THE STATE OF CALIFORNIA", bold=True, center=True)
    d.write_line("COUNTY OF ALAMEDA", bold=True, center=True)
    d.blank_line()
    d.draw_caption_block(CAPTION_LEFT, first_meta["right"], caption_size=9, tight_lh=12, boxed=True)
    d.blank_line()
    if first_meta.get("center_title"):
        d.ensure_space(3)
        for line in _wrap_center_title(first_title):
            d.write_line(line, bold=True, center=True)
        d.blank_line()
    render_body(d, first_body, first_meta, stats)
    stats["papers"].append(first_title)

    for title, body in docs[1:]:
        meta = PAPERS[title]
        # Set footer first so the next page frame uses it.
        d.doc_title_footer = meta["footer"]
        d.start_new_page()
        draw_attorney_block(d)
        d.write_line("SUPERIOR COURT OF THE STATE OF CALIFORNIA", bold=True, center=True)
        d.write_line("COUNTY OF ALAMEDA", bold=True, center=True)
        d.blank_line()
        d.draw_caption_block(CAPTION_LEFT, meta["right"], caption_size=9, tight_lh=12, boxed=True)
        d.blank_line()
        if meta.get("center_title"):
            d.ensure_space(3)
            for line in _wrap_center_title(title):
                d.write_line(line, bold=True, center=True)
            d.blank_line()
        render_body(d, body, meta, stats)
        stats["papers"].append(title)

    d.save()
    stats["pages"] = d.page_num
    stats["out"] = str(out_path)
    return stats


def _wrap_center_title(title: str) -> list[str]:
    title = title.replace("PETITIONER’S", "PETITIONER'S")
    if len(title) <= 64:
        return [title]
    # Split long titles at a natural break.
    for cut in [title.rfind(" OF ", 0, 64), title.rfind(" AND ", 0, 64), 60]:
        if cut > 20:
            return [title[:cut].strip(), title[cut:].strip()]
    return [title]


def _heading_lines(text: str) -> list[str]:
    """Split a long ALL-CAPS heading so it stays inside the right rule."""
    text = text.replace("PETITIONER’S", "PETITIONER'S")
    if len(text) <= 58:
        return [text]
    for sep in [", AND ", " AND IS NOT ", " AND ", "; ", " -- "]:
        idx = text.find(sep)
        if 20 <= idx <= 58:
            return [text[:idx].strip().rstrip(","), text[idx:].lstrip(" ,")]
    for cut in range(58, 24, -1):
        if text[cut] == " ":
            return [text[:cut], text[cut + 1 :]]
    return [text]


def _page_has_body(page) -> bool:
    lines = [ln.strip() for ln in page.get_text().splitlines() if ln.strip()]
    footer_marks = (
        "NEWANFORBI v. CHP",
        "NOTICE OF MOTION",
        "MEMORANDUM OF POINTS",
        "DECLARATION OF",
        "PROPOSED] ORDER",
        "PROOF OF SERVICE",
        "REQUEST FOR JUDICIAL",
        "NOTICE OF LODGING",
    )
    for ln in lines:
        if re.fullmatch(r"\d{1,2}", ln) or ln.startswith("Page "):
            continue
        if any(m in ln for m in footer_marks):
            continue
        return True
    return False


def _drop_empty_trailing_pages(path: Path) -> None:
    try:
        import pymupdf
    except ImportError:
        return
    doc = pymupdf.open(path)
    changed = False
    while len(doc) > 1 and not _page_has_body(doc[-1]):
        doc.delete_page(-1)
        changed = True
    if changed:
        tmp = path.with_suffix(".tmp.pdf")
        doc.save(tmp)
        tmp.replace(path)
    doc.close()


def main() -> None:
    jobs = [
        (
            HERE / "Revised_Motion_Packet.md",
            HERE / "Revised_Motion_Packet.pdf",
            "NOTICE OF MOTION -- " + FOOTER_CASE,
        ),
        (
            HERE / "Request_for_Judicial_Notice.md",
            HERE / "Request_for_Judicial_Notice.pdf",
            "REQUEST FOR JUDICIAL NOTICE -- " + FOOTER_CASE,
        ),
        (
            HERE / "Notice_of_Lodging.md",
            HERE / "Notice_of_Lodging.pdf",
            "NOTICE OF LODGING -- " + FOOTER_CASE,
        ),
    ]
    for src, dest, footer in jobs:
        stats = _fix_footer_timing(src, dest)
        _drop_empty_trailing_pages(dest)
        try:
            import pymupdf
            actual = len(pymupdf.open(dest))
        except Exception:
            actual = stats["pages"]
        print(f"{dest.name}: {actual} pages; papers={stats['papers']}")
        if stats.get("mpa_substance_pages") is not None:
            print(f"  MPA substance pages (from I. Introduction): {stats['mpa_substance_pages']}")


if __name__ == "__main__":
    main()
