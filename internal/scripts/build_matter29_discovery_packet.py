#!/usr/bin/env python3
"""Matter 29 -- discovery set one on portfolio pleading paper.

Newanforbi v. Amazon.com Services, LLC, et al., N.D. Cal. No. 4:26-cv-09249-ASK.

Pipeline (pattern of matter25-discovery-set-one.py, matter24-opposition-mtd-v4-
pleading.py, and matter28-initial-disclosures-pleading.py):

  1. Markdown sources in internal/docs/matter-29/discovery-set-one/ -> Word
     pleading-paper DOCX (Times New Roman 12, exact 24-pt lines, 28 numbered
     lines in a header-anchored VML text box, rule lines in the header, inline
     signature image, named "Pleading ..." paragraph styles).
  2. The DOCX is read back with python-docx (by paragraph style) and rendered
     onto the portfolio pleading-paper formatter, lib/pleading_paper.PleadingPaper
     -- the same engine behind pleading-paper-formatter-script.py and every
     prior pleading-paper filing. The signature is drawn with
     PleadingPaper.draw_signature_image from signature_stamp.SIGNATURE_PATH.
  3. Proofs of service come from the portfolio federal POS template,
     lib/proof_of_service.build_proof_of_service (canonical blank:
     internal/public/documents/_form-library/proof-of-service-blank-template.pdf),
     and are appended to each discovery set and collected per defendant in
     10_/11_ service packets. RFP proofs (Rule 26(d)(2) early delivery) are
     dated and signed October 19, 2026; interrogatory and RFA proofs stay
     undated and unsigned until actual service.

REVIEW_DRAFT (off) would restore a "REVIEW DRAFT -- NOT SERVED" marker: in the
DOCX as its own footer paragraph, in the PDF appended to the formatter footer
line, as matter28 does with "-- WORKING DRAFT". Nothing here files, sends, or
serves.

    python3 internal/scripts/build_matter29_discovery_packet.py
"""
from __future__ import annotations

import datetime as _dt
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR / "lib"))
sys.path.insert(0, str(SCRIPT_DIR))

from docx import Document  # noqa: E402
from docx.enum.style import WD_STYLE_TYPE  # noqa: E402
from docx.enum.table import WD_ROW_HEIGHT_RULE  # noqa: E402
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK, WD_LINE_SPACING  # noqa: E402
from docx.oxml import OxmlElement, parse_xml  # noqa: E402
from docx.oxml.ns import qn  # noqa: E402
from docx.shared import Inches, Pt  # noqa: E402

from pdf_packet import assemble  # noqa: E402
from pleading_paper import (  # noqa: E402
    CONTENT_LEFT,
    CONTENT_RIGHT,
    LINE_SPACING,
    NUM_LINES,
    PAGE_H,
    PAGE_W,
    VERT_LINE_LEFT,
    VERT_LINE_RIGHT,
    PleadingPaper,
)
from proof_of_service import (  # noqa: E402
    DISTRICT_NDCAL,
    ProofOfServiceFields,
    build_proof_of_service,
)
from signature_stamp import (  # noqa: E402
    SIGNATURE_ASPECT,
    SIGNATURE_NATIVE_PX,
    SIGNATURE_PATH,
    _resolve_stamp_path,
)

ROOT = SCRIPT_DIR.parent / "docs" / "matter-29" / "discovery-set-one"
OUT = ROOT / "generated"

REVIEW_DRAFT = False  # draft marker removed for service (Oct 17, 2026)
DRAFT_MARKER = "REVIEW DRAFT -- NOT SERVED"
AUTHOR = "Brendan Ngehsi Newanforbi"
CASE_NO = "4:26-cv-09249-ASK"
SHORT_CAPTION = "NEWANFORBI v. AMAZON.COM SERVICES, LLC, et al."
SIGN_DATE = "October 19, 2026"
SIGNER = "Brendan Ngehsi Newanforbi"
SIGNER_ROLE = "Plaintiff, In Propria Persona"
SIG_LINE = "___________________________________"
JUDGE_LINE = "Magistrate Judge Ajay S. Krishnan"

PARTY_BLOCK = [
    ("BRENDAN NGEHSI NEWANFORBI", True),
    ("Plaintiff, In Propria Persona", False),
    ("1455 Cat Tail Drive", False),
    ("Stockton, CA 95204", False),
    ("Telephone: (209) 801-4442", False),
    ("E-mail: bnn.cdl@gmail.com", False),
]
COURT_LINES = ["UNITED STATES DISTRICT COURT", "NORTHERN DISTRICT OF CALIFORNIA", "OAKLAND DIVISION"]
CAPTION_LEFT = [
    ("BRENDAN NGEHSI NEWANFORBI,", True),
    ("", False),
    ("                          Plaintiff,", False),
    ("", False),
    ("       v.", False),
    ("", False),
    ("AMAZON.COM SERVICES, LLC;", True),
    ("ACCURATE BACKGROUND, LLC; and", True),
    ("DOES 1-10, inclusive,", True),
    ("", False),
    ("                          Defendants.", False),
    ("", False),
]
CAPTION_ROWS = 12  # even: 12 rows x 12 pt = 6 pleading lines in Word

AMAZON = "AMAZON.COM SERVICES, LLC"
ACCURATE = "ACCURATE BACKGROUND, LLC"

# Rule 5(a)(1)(C): every paper is served on every party, so each proof lists
# both firms. Mailing addresses are exactly as the counsel blocks show them:
#   Morgan Lewis -- Amazon MTD, Dkt. 19 (Sep 22, 2026), p. 1 (also the Oct 13
#     Reply ISO MTD): Frederick, Palo Alto; Douglass G. Brown, Dallas.
#   Seyfarth -- Accurate Answer, Dkt. 21 (Sep 22, 2026), p. 1: Los Angeles.
#     Dkt. 21 lists only Ms. Stanzick; John Drury's own office address is not
#     in the filings, so his copy goes to the firm's address of record.
# Suga Ikeda (Mr. Frederick's assistant) appears in no counsel block: e-mail only.
SERVICE_LIST = [
    "Andrew P. Frederick -- andrew.frederick@morganlewis.com",
    "    1400 Page Mill Road, Palo Alto, CA 94304",
    "Douglass G. Brown -- douglass.brown@morganlewis.com",
    "    1717 Main Street, Suite 3200, Dallas, TX 75201",
    "Suga Ikeda -- suga.ikeda@morganlewis.com (e-mail only)",
    "Morgan, Lewis & Bockius LLP -- Attorneys for Defendant Amazon.com Services, LLC",
    "",
    "John Drury -- JDrury@seyfarth.com",
    "Jasmine J. Stanzick -- jstanzick@seyfarth.com",
    "    Seyfarth Shaw LLP, 2029 Century Park East, Suite 3500,",
    "    Los Angeles, California 90067-3021",
    "Seyfarth Shaw LLP -- Attorneys for Defendant Accurate Background, LLC",
]
MAILED_FROM = "San Jose, California"  # place of mailing (not the party address)
EARLY_DELIVERY_NOTE = [
    "",
    "Delivered early under Fed. R. Civ. P. 26(d)(2)(A); deemed served at the",
    "parties' first Rule 26(f) conference (Fed. R. Civ. P. 26(d)(2)(B)).",
]

# key: (defendant, kind, caption title lines, rules cite, salutation?)
DOCS = {
    "01_Amazon_RFP_Set_One": dict(defendant=AMAZON, kind="RFP", rule="(Fed. R. Civ. P. 26, 34)",
        title=["PLAINTIFF'S FIRST REQUESTS FOR", "PRODUCTION OF DOCUMENTS TO", "DEFENDANT AMAZON.COM", "SERVICES, LLC"],
        heading=["PLAINTIFF'S FIRST REQUESTS FOR PRODUCTION OF", "DOCUMENTS TO DEFENDANT AMAZON.COM SERVICES, LLC"],
        footer="PLAINTIFF'S FIRST REQUESTS FOR PRODUCTION TO AMAZON"),
    "02_Accurate_RFP_Set_One": dict(defendant=ACCURATE, kind="RFP", rule="(Fed. R. Civ. P. 26, 34)",
        title=["PLAINTIFF'S FIRST REQUESTS FOR", "PRODUCTION OF DOCUMENTS TO", "DEFENDANT ACCURATE", "BACKGROUND, LLC"],
        heading=["PLAINTIFF'S FIRST REQUESTS FOR PRODUCTION OF", "DOCUMENTS TO DEFENDANT ACCURATE BACKGROUND, LLC"],
        footer="PLAINTIFF'S FIRST REQUESTS FOR PRODUCTION TO ACCURATE"),
    "03_Amazon_Interrogatories_Set_One": dict(defendant=AMAZON, kind="ROG", rule="(Fed. R. Civ. P. 26, 33)",
        title=["PLAINTIFF'S FIRST SET OF", "INTERROGATORIES TO", "DEFENDANT AMAZON.COM", "SERVICES, LLC"],
        heading=["PLAINTIFF'S FIRST SET OF INTERROGATORIES", "TO DEFENDANT AMAZON.COM SERVICES, LLC"],
        footer="PLAINTIFF'S FIRST SET OF INTERROGATORIES TO AMAZON"),
    "04_Accurate_Interrogatories_Set_One": dict(defendant=ACCURATE, kind="ROG", rule="(Fed. R. Civ. P. 26, 33)",
        title=["PLAINTIFF'S FIRST SET OF", "INTERROGATORIES TO", "DEFENDANT ACCURATE", "BACKGROUND, LLC"],
        heading=["PLAINTIFF'S FIRST SET OF INTERROGATORIES", "TO DEFENDANT ACCURATE BACKGROUND, LLC"],
        footer="PLAINTIFF'S FIRST SET OF INTERROGATORIES TO ACCURATE"),
    "05_Amazon_RFA_Set_One": dict(defendant=AMAZON, kind="RFA", rule="(Fed. R. Civ. P. 26, 36)",
        title=["PLAINTIFF'S FIRST REQUESTS FOR", "ADMISSION TO DEFENDANT", "AMAZON.COM SERVICES, LLC"],
        heading=["PLAINTIFF'S FIRST REQUESTS FOR ADMISSION", "TO DEFENDANT AMAZON.COM SERVICES, LLC"],
        footer="PLAINTIFF'S FIRST REQUESTS FOR ADMISSION TO AMAZON"),
    "06_Accurate_RFA_Set_One": dict(defendant=ACCURATE, kind="RFA", rule="(Fed. R. Civ. P. 26, 36)",
        title=["PLAINTIFF'S FIRST REQUESTS FOR", "ADMISSION TO DEFENDANT", "ACCURATE BACKGROUND, LLC"],
        heading=["PLAINTIFF'S FIRST REQUESTS FOR ADMISSION", "TO DEFENDANT ACCURATE BACKGROUND, LLC"],
        footer="PLAINTIFF'S FIRST REQUESTS FOR ADMISSION TO ACCURATE"),
    "07_Rule_26f_ESI_Proposal": dict(defendant=None, kind="ESI", rule="(Fed. R. Civ. P. 26(f))",
        title=["PLAINTIFF'S RULE 26(f) ESI", "MEET-AND-CONFER PROPOSAL", "(DRAFT FOR CONFERENCE --", "NOT A STIPULATION)"],
        heading=["PLAINTIFF'S RULE 26(f) ESI MEET-AND-CONFER PROPOSAL"],
        footer="PLAINTIFF'S RULE 26(f) ESI PROPOSAL"),
    "08_Amazon_30b6_Draft_HOLD": dict(defendant=AMAZON, kind="HOLD", rule="(Fed. R. Civ. P. 30(b)(6))",
        title=["DRAFT RULE 30(b)(6) TOPICS --", "AMAZON.COM SERVICES, LLC", "(HOLD -- NOT A NOTICE OF", "DEPOSITION)"],
        heading=["DRAFT RULE 30(b)(6) DEPOSITION TOPICS", "AMAZON.COM SERVICES, LLC"],
        footer="DRAFT RULE 30(b)(6) TOPICS (AMAZON) -- HOLD"),
    "09_Accurate_30b6_Draft_HOLD": dict(defendant=ACCURATE, kind="HOLD", rule="(Fed. R. Civ. P. 30(b)(6))",
        title=["DRAFT RULE 30(b)(6) TOPICS --", "ACCURATE BACKGROUND, LLC", "(HOLD -- NOT A NOTICE OF", "DEPOSITION)"],
        heading=["DRAFT RULE 30(b)(6) DEPOSITION TOPICS", "ACCURATE BACKGROUND, LLC"],
        footer="DRAFT RULE 30(b)(6) TOPICS (ACCURATE) -- HOLD"),
}
SERVED_SETS = [k for k, v in DOCS.items() if v["kind"] in ("RFP", "ROG", "RFA")]
PLEADING_DOCS = list(DOCS)
SERVICE_PACKETS = {
    "10_Amazon_Service_Record": ("01_Amazon_RFP_Set_One", "03_Amazon_Interrogatories_Set_One", "05_Amazon_RFA_Set_One"),
    "11_Accurate_Service_Record": ("02_Accurate_RFP_Set_One", "04_Accurate_Interrogatories_Set_One", "06_Accurate_RFA_Set_One"),
}
KIND_NAME = {"RFP": "First Requests for Production of Documents",
             "ROG": "First Set of Interrogatories",
             "RFA": "First Requests for Admission"}
LABELS = {"REQUEST FOR PRODUCTION", "INTERROGATORY", "REQUEST FOR ADMISSION"}


def footer_title(key: str) -> str:
    return f"{DOCS[key]['footer']} -- Case No. {CASE_NO}"


# ======================================================================
# Markdown -> blocks
# ======================================================================

SKIP_PREFIXES = ("**UNITED STATES DISTRICT COURT", "**BRENDAN NGEHSI NEWANFORBI, Plaintiff",
                 "**Case No.", "**DRAFT — NOT FILED OR SERVED**")


def parse_markdown(path: Path) -> list[tuple[str, str]]:
    """Return [(kind, text)] with kind in H, P, LIST, BULLET, REQ, DATED, SIG."""
    blocks: list[tuple[str, str]] = []
    after_sig = False
    for raw in re.split(r"\n\s*\n", path.read_text(encoding="utf-8")):
        text = raw.strip()
        if not text or text.startswith(SKIP_PREFIXES):
            continue
        if after_sig:  # typed name and contact line: rendered from constants
            continue
        if text.startswith("# "):
            continue  # document title comes from DOCS (caption + centered title)
        if text.startswith("## "):
            blocks.append(("H", text[3:].strip().upper()))
            continue
        m = re.match(r"\*\*(REQUEST FOR PRODUCTION|INTERROGATORY|REQUEST FOR ADMISSION) NO\. (\d+)\.\*\*\s*(.*)", text, re.S)
        if m:
            blocks.append(("REQ", f"{m.group(1)} NO. {int(m.group(2))}:\x00{m.group(3).strip()}"))
            continue
        m = re.match(r"\*\*Dated:\*\*\s*(.*)", text)
        if m:
            blocks.append(("DATED", m.group(1).strip()))
            continue
        if text == "[[SIGNATURE]]":
            blocks.append(("SIG", ""))
            after_sig = True
            continue
        lines = text.split("\n")
        if all(ln.startswith("- ") for ln in lines):
            for ln in lines:
                blocks.append(("BULLET", ln[2:].strip()))
            continue
        if re.match(r"\d+\. ", text):
            blocks.append(("LIST", " ".join(lines)))
            continue
        blocks.append(("P", " ".join(ln.strip() for ln in lines)))
    return blocks


def salutation(defendant: str) -> str:
    return f"TO DEFENDANT {defendant} AND ITS ATTORNEYS OF RECORD:"


# ======================================================================
# DOCX pleading paper
# ======================================================================

FONT = "Times New Roman"
TOP_TW = 1080      # 0.75 in
BOTTOM_TW = 1300   # body = 13460 tw >= 28 x 480 tw
LEFT_TW = round(CONTENT_LEFT * 20)               # matches the formatter's text column
RIGHT_TW = round((PAGE_W - CONTENT_RIGHT + 16) * 20)
HEADER_TW = 360
FOOTER_TW = 288


def _fonts(rpr_owner, size_pt=12, bold=None):
    rpr = rpr_owner
    rpr.font.name = FONT
    rpr.font.size = Pt(size_pt)
    if bold is not None:
        rpr.font.bold = bold
    rel = rpr.element.get_or_add_rPr() if hasattr(rpr, "element") else None
    return rel


def _set_style_fonts(style, size_pt=12, bold=False):
    style.font.name = FONT
    style.font.size = Pt(size_pt)
    style.font.bold = bold
    rpr = style.element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.insert(0, rfonts)
    for a in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
        rfonts.set(qn(a), FONT)
    for a in ("w:asciiTheme", "w:hAnsiTheme", "w:eastAsiaTheme", "w:cstheme"):
        rfonts.attrib.pop(qn(a), None)


def _pstyle(doc, name, *, size=12, bold=False, align=None, exact=24, before=0, after=0,
            first=None, left=None, right=None, keep_next=False, base="Normal"):
    styles = doc.styles
    st = styles[name] if name in [s.name for s in styles] else styles.add_style(name, WD_STYLE_TYPE.PARAGRAPH)
    st.base_style = styles[base] if base else None
    st.quick_style = True
    _set_style_fonts(st, size, bold)
    pf = st.paragraph_format
    pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    pf.line_spacing = Pt(exact)
    pf.space_before = Pt(before)
    pf.space_after = Pt(after)
    pf.widow_control = False
    if align is not None:
        pf.alignment = align
    if first is not None:
        pf.first_line_indent = Pt(first)
    if left is not None:
        pf.left_indent = Pt(left)
    if right is not None:
        pf.right_indent = Pt(right)
    pf.keep_with_next = keep_next
    return st


def setup_styles(doc):
    normal = doc.styles["Normal"]
    _set_style_fonts(normal, 12, False)
    npf = normal.paragraph_format
    npf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    npf.line_spacing = Pt(24)
    npf.space_before = Pt(0)
    npf.space_after = Pt(0)
    C, R = WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.RIGHT
    _pstyle(doc, "Pleading Party Info", exact=12, after=96)
    _pstyle(doc, "Pleading Court Title", bold=True, align=C, after=24)
    _pstyle(doc, "Pleading Caption", size=10, exact=12)
    _pstyle(doc, "Pleading Document Title", bold=True, align=C, before=24, after=24, keep_next=True)
    _pstyle(doc, "Pleading Heading", bold=True, align=C, after=24, keep_next=True)
    _pstyle(doc, "Pleading Body", first=36, after=24)
    _pstyle(doc, "Pleading Body Flush", first=0, after=24)
    _pstyle(doc, "Pleading List", first=0, after=24)
    _pstyle(doc, "Pleading Bullet", left=36, first=-18, after=0)
    _pstyle(doc, "Pleading Request Label", bold=True, keep_next=True)
    _pstyle(doc, "Pleading Signature Date", after=24, keep_next=True)
    _pstyle(doc, "Pleading Signoff", align=R, right=20, keep_next=True)
    # 2 pleading lines tall; the inline image sits on a bottom-border rule.
    _pstyle(doc, "Pleading Signature Image", align=R, right=20, exact=48, keep_next=True)
    _pstyle(doc, "Pleading Signer", align=R, right=20, keep_next=True)
    _pstyle(doc, "Pleading Line Number", align=R, base=None)
    _pstyle(doc, "Pleading Header", size=1, exact=1, base=None)
    _pstyle(doc, "Pleading Footer", size=10, exact=12, align=C, base=None)
    _pstyle(doc, "Pleading Footer Title", size=8, exact=10, align=C, base=None)
    if REVIEW_DRAFT:
        _pstyle(doc, "Pleading Footer Draft Marker", size=8, exact=10, align=C, base=None, bold=True)


def _rule(shape_no: int, x_pt: float) -> str:
    """Full-height vertical pleading rule anchored to the page, written the way
    Word itself saves a shape: DrawingML (wps) with a VML fallback."""
    emu = lambda pt: int(round(pt * 12700))  # noqa: E731
    h = emu(PAGE_H)
    a = "http://schemas.openxmlformats.org/drawingml/2006/main"
    choice = (
        f'<w:drawing><wp:anchor distT="0" distB="0" distL="0" distR="0" simplePos="0" '
        f'relativeHeight="{251650000 + shape_no}" behindDoc="1" locked="1" layoutInCell="1" allowOverlap="1">'
        '<wp:simplePos x="0" y="0"/>'
        f'<wp:positionH relativeFrom="page"><wp:posOffset>{emu(x_pt)}</wp:posOffset></wp:positionH>'
        '<wp:positionV relativeFrom="page"><wp:posOffset>0</wp:posOffset></wp:positionV>'
        f'<wp:extent cx="0" cy="{h}"/><wp:effectExtent l="0" t="0" r="0" b="0"/><wp:wrapNone/>'
        f'<wp:docPr id="{shape_no}" name="Pleading Rule {shape_no}"/><wp:cNvGraphicFramePr/>'
        f'<a:graphic xmlns:a="{a}"><a:graphicData uri="http://schemas.microsoft.com/office/word/2010/wordprocessingShape">'
        '<wps:wsp><wps:cNvCnPr/><wps:spPr>'
        f'<a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="{h}"/></a:xfrm>'
        '<a:prstGeom prst="line"><a:avLst/></a:prstGeom>'
        '<a:ln w="6350"><a:solidFill><a:srgbClr val="000000"/></a:solidFill></a:ln>'
        '</wps:spPr><wps:bodyPr/></wps:wsp></a:graphicData></a:graphic></wp:anchor></w:drawing>'
    )
    fallback = (
        f'<w:pict><v:line id="PleadingRule{shape_no}" o:spid="_x0000_s{shape_no}" '
        f'style="position:absolute;z-index:-{251650000 + shape_no};mso-position-horizontal-relative:page;'
        f'mso-position-vertical-relative:page" from="{x_pt:.2f}pt,0" to="{x_pt:.2f}pt,{PAGE_H:.0f}pt" '
        'strokeweight=".5pt"/></w:pict>'
    )
    return (f'<mc:AlternateContent><mc:Choice Requires="wps">{choice}</mc:Choice>'
            f'<mc:Fallback>{fallback}</mc:Fallback></mc:AlternateContent>')


def _line_number_box():
    top_pt = TOP_TW / 20
    paras = "".join(
        f'<w:p><w:pPr><w:pStyle w:val="PleadingLineNumber"/></w:pPr><w:r><w:t>{i}</w:t></w:r></w:p>'
        for i in range(1, NUM_LINES + 1)
    )
    left = 36.0
    width = (VERT_LINE_LEFT - 6) - left
    return (
        '<v:shapetype id="_x0000_t202" coordsize="21600,21600" o:spt="202" path="m,l,21600r21600,l21600,xe">'
        '<v:stroke joinstyle="miter"/><v:path gradientshapeok="t" o:connecttype="rect"/></v:shapetype>'
        f'<v:shape id="PleadingLineNumbers" o:spid="_x0000_s2001" type="#_x0000_t202" '
        f'style="position:absolute;margin-left:{left:.2f}pt;margin-top:{top_pt:.2f}pt;width:{width:.2f}pt;'
        f'height:{NUM_LINES * LINE_SPACING + 6}pt;z-index:-251649000;mso-position-horizontal-relative:page;'
        f'mso-position-vertical-relative:page" filled="f" stroked="f">'
        f'<v:textbox inset="0,0,0,0"><w:txbxContent>{paras}</w:txbxContent></v:textbox></v:shape>'
    )


def setup_header_footer(doc, key):
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Inches(8.5), Inches(11)
    sec.top_margin = Pt(TOP_TW / 20)
    sec.bottom_margin = Pt(BOTTOM_TW / 20)
    sec.left_margin = Pt(LEFT_TW / 20)
    sec.right_margin = Pt(RIGHT_TW / 20)
    sec.header_distance = Pt(HEADER_TW / 20)
    sec.footer_distance = Pt(FOOTER_TW / 20)
    # Line-number style id has no spaces: python-docx derives it from the name.
    doc.styles["Pleading Line Number"].element.set(qn("w:styleId"), "PleadingLineNumber")

    hp = sec.header.paragraphs[0]
    hp.style = doc.styles["Pleading Header"]
    ns = ('xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
          'xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office" '
          'xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" '
          'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
          'xmlns:wps="http://schemas.microsoft.com/office/word/2010/wordprocessingShape"')
    for no, x in ((1001, VERT_LINE_LEFT), (1002, VERT_LINE_RIGHT), (1003, CONTENT_RIGHT)):
        hp._p.append(parse_xml(f"<w:r {ns}>{_rule(no, x)}</w:r>"))
    hp._p.append(parse_xml(f"<w:r {ns}><w:pict>{_line_number_box()}</w:pict></w:r>"))

    ft = sec.footer
    p1 = ft.paragraphs[0]
    p1.style = doc.styles["Pleading Footer"]
    ppr = p1._p.get_or_add_pPr()
    bdr = OxmlElement("w:pBdr")
    top = OxmlElement("w:top")
    for k, v in (("w:val", "single"), ("w:sz", "4"), ("w:space", "1"), ("w:color", "000000")):
        top.set(qn(k), v)
    bdr.append(top)
    ppr.append(bdr)
    p1.add_run("Page ")
    fld = OxmlElement("w:fldSimple")
    fld.set(qn("w:instr"), " PAGE ")
    r = OxmlElement("w:r")
    t = OxmlElement("w:t")
    t.text = "1"
    r.append(t)
    fld.append(r)
    p1._p.append(fld)
    ft.add_paragraph(footer_title(key), style=doc.styles["Pleading Footer Title"])
    if REVIEW_DRAFT:
        ft.add_paragraph(DRAFT_MARKER, style=doc.styles["Pleading Footer Draft Marker"])


def _add_marked_text(p, text):
    for chunk in re.split(r"(\*\*.*?\*\*)", text):
        if not chunk:
            continue
        if chunk.startswith("**") and chunk.endswith("**"):
            p.add_run(chunk[2:-2]).bold = True
        else:
            p.add_run(chunk)


def _cell_border(cell, **edges):
    tcpr = cell._tc.get_or_add_tcPr()
    b = OxmlElement("w:tcBorders")
    for edge in ("top", "left", "bottom", "right"):
        el = OxmlElement(f"w:{edge}")
        if edge in edges:
            el.set(qn("w:val"), "single")
            el.set(qn("w:sz"), "6")
            el.set(qn("w:space"), "0")
            el.set(qn("w:color"), "000000")
        else:
            el.set(qn("w:val"), "nil")
        b.append(el)
    tcpr.append(b)


def add_caption_table(doc, right_rows):
    tbl = doc.add_table(rows=CAPTION_ROWS, cols=2)
    tbl.autofit = False
    tblpr = tbl._tbl.tblPr
    for tag in ("w:tblStyle",):
        el = tblpr.find(qn(tag))
        if el is not None:
            tblpr.remove(el)
    mar = OxmlElement("w:tblCellMar")
    for edge, w in (("top", 0), ("bottom", 0), ("left", 115), ("right", 115)):
        e = OxmlElement(f"w:{edge}")
        e.set(qn("w:w"), str(w))
        e.set(qn("w:type"), "dxa")
        mar.append(e)
    tblpr.append(mar)
    body_w = (12240 - LEFT_TW - RIGHT_TW)
    widths = [round(body_w * 0.52), body_w - round(body_w * 0.52)]
    left = (CAPTION_LEFT + [("", False)] * CAPTION_ROWS)[:CAPTION_ROWS]
    right = (right_rows + [("", False)] * CAPTION_ROWS)[:CAPTION_ROWS]
    for i, row in enumerate(tbl.rows):
        row.height = Pt(12)
        row.height_rule = WD_ROW_HEIGHT_RULE.EXACTLY
        for j, (cell, (text, bold)) in enumerate(zip(row.cells, (left[i], right[i]))):
            cell.width = widths[j]
            p = cell.paragraphs[0]
            p.style = doc.styles["Pleading Caption"]
            if text:
                p.add_run(text).bold = bold
            if j == 0:
                edges = {"right": 1}
                if i == 0:
                    edges["top"] = 1
                _cell_border(cell, **edges)
                if i == CAPTION_ROWS - 1:
                    # Bottom rule as an underscore tab leader: a cell bottom
                    # border adds its width to the row in LibreOffice and
                    # would shift every later line off the numbers.
                    pos = widths[0] - 2 * 115 - 20
                    tabs = OxmlElement("w:tabs")
                    tab = OxmlElement("w:tab")
                    tab.set(qn("w:val"), "right")
                    tab.set(qn("w:leader"), "underscore")
                    tab.set(qn("w:pos"), str(pos))
                    tabs.append(tab)
                    p._p.get_or_add_pPr().append(tabs)
                    p.add_run().add_tab()
            else:
                _cell_border(cell)
    return tbl


def right_caption(key):
    meta = DOCS[key]
    rows = [(f"Case No. {CASE_NO}", False), ("", False)]
    rows += [(t, True) for t in meta["title"]]
    rows += [("", False)]
    if meta["kind"] in ("RFP", "ROG", "RFA"):
        rows += [("Propounding Party: Plaintiff", False),
                 (f"Responding Party: {meta['defendant'].title().replace('Llc', 'LLC').replace('.Com', '.com')}", False),
                 ("Set No.: One", False)]
    rows += [(meta["rule"], False), (JUDGE_LINE, False)]
    return rows[:CAPTION_ROWS]


def add_signature(doc, dated):
    doc.add_paragraph(f"Dated: {dated}", style=doc.styles["Pleading Signature Date"])
    doc.add_paragraph("Respectfully submitted,", style=doc.styles["Pleading Signoff"])
    p = doc.add_paragraph(style=doc.styles["Pleading Signature Image"])
    width_pt = 220.0
    p.add_run().add_picture(_resolve_stamp_path(SIGNATURE_PATH),
                            width=Pt(width_pt), height=Pt(width_pt * SIGNATURE_ASPECT))
    ppr = p._p.get_or_add_pPr()
    bdr = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    for k, v in (("w:val", "single"), ("w:sz", "4"), ("w:space", "0"), ("w:color", "000000")):
        bottom.set(qn(k), v)
    bdr.append(bottom)
    ppr.append(bdr)
    usable = (12240 - LEFT_TW - RIGHT_TW) / 20
    p.paragraph_format.left_indent = Pt(usable - 20 - 240)
    doc.add_paragraph(SIGNER, style=doc.styles["Pleading Signer"])
    last = doc.add_paragraph(SIGNER_ROLE, style=doc.styles["Pleading Signer"])
    last.paragraph_format.keep_with_next = False


def sanitize_package(path: Path, title: str, subject: str):
    """Drop python-docx template leftovers (thumbnail, customXml, Mac Word app
    props) and write clean core properties."""
    now = _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    esc = lambda s: s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")  # noqa: E731
    core = (
        "<?xml version='1.0' encoding='UTF-8' standalone='yes'?>\n"
        '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
        'xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" '
        'xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
        f"<dc:title>{esc(title)}</dc:title><dc:subject>{esc(subject)}</dc:subject>"
        f"<dc:creator>{AUTHOR}</dc:creator><cp:keywords></cp:keywords><dc:description></dc:description>"
        f"<cp:lastModifiedBy>{AUTHOR}</cp:lastModifiedBy><cp:revision>1</cp:revision>"
        f'<dcterms:created xsi:type="dcterms:W3CDTF">{now}</dcterms:created>'
        f'<dcterms:modified xsi:type="dcterms:W3CDTF">{now}</dcterms:modified>'
        "<cp:category></cp:category></cp:coreProperties>"
    )
    app = (
        "<?xml version='1.0' encoding='UTF-8' standalone='yes'?>\n"
        '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
        'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">'
        "<Template>Normal.dotm</Template><DocSecurity>0</DocSecurity><ScaleCrop>false</ScaleCrop>"
        "<Company></Company><LinksUpToDate>false</LinksUpToDate><SharedDoc>false</SharedDoc>"
        "<HyperlinksChanged>false</HyperlinksChanged></Properties>"
    )
    src = zipfile.ZipFile(path)
    items = {n: src.read(n) for n in src.namelist()}
    src.close()
    for n in list(items):
        if n.startswith("customXml/") or n == "docProps/thumbnail.jpeg":
            del items[n]
    items["docProps/core.xml"] = core.encode()
    items["docProps/app.xml"] = app.encode()
    rels = items["_rels/.rels"].decode()
    items["_rels/.rels"] = re.sub(r'<Relationship [^>]*thumbnail[^>]*/>', "", rels).encode()
    drels = items["word/_rels/document.xml.rels"].decode()
    items["word/_rels/document.xml.rels"] = re.sub(r'<Relationship [^>]*customXml[^>]*/>', "", drels).encode()
    ct = items["[Content_Types].xml"].decode()
    ct = re.sub(r'<Override PartName="/customXml/[^>]*/>', "", ct)
    items["[Content_Types].xml"] = ct.encode()
    settings = items["word/settings.xml"].decode()
    settings = settings.replace('w:name="compatibilityMode" w:uri="http://schemas.microsoft.com/office/word" w:val="14"',
                                'w:name="compatibilityMode" w:uri="http://schemas.microsoft.com/office/word" w:val="15"')
    items["word/settings.xml"] = settings.encode()
    order = ["[Content_Types].xml"] + [n for n in items if n != "[Content_Types].xml"]
    tmp = path.with_suffix(".tmp")
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as z:
        for n in order:
            z.writestr(n, items[n])
    tmp.replace(path)


def build_docx(key: str, dest: Path) -> None:
    meta = DOCS[key]
    blocks = parse_markdown(ROOT / f"{key}.md")
    doc = Document()
    setup_styles(doc)
    setup_header_footer(doc, key)
    body = doc.element.body
    for p in list(body.iterchildren(qn("w:p"))):
        body.remove(p)
    p = doc.add_paragraph(style=doc.styles["Pleading Party Info"])
    for i, (t, b) in enumerate(PARTY_BLOCK):
        if i:
            p.add_run().add_break(WD_BREAK.LINE)
        p.add_run(t).bold = b
    p = doc.add_paragraph(style=doc.styles["Pleading Court Title"])
    for i, t in enumerate(COURT_LINES):
        if i:
            p.add_run().add_break(WD_BREAK.LINE)
        p.add_run(t)
    add_caption_table(doc, right_caption(key))
    p = doc.add_paragraph(style=doc.styles["Pleading Document Title"])
    for i, t in enumerate(meta["heading"]):
        if i:
            p.add_run().add_break(WD_BREAK.LINE)
        p.add_run(t)
    if meta["defendant"] and meta["kind"] in ("RFP", "ROG", "RFA"):
        doc.add_paragraph(salutation(meta["defendant"]), style=doc.styles["Pleading Body Flush"])
    for kind, text in blocks:
        if kind == "H":
            doc.add_paragraph(text, style=doc.styles["Pleading Heading"])
        elif kind == "REQ":
            label, rest = text.split("\x00")
            doc.add_paragraph(label, style=doc.styles["Pleading Request Label"])
            _add_marked_text(doc.add_paragraph(style=doc.styles["Pleading Body"]), rest)
        elif kind == "LIST":
            _add_marked_text(doc.add_paragraph(style=doc.styles["Pleading List"]), text)
        elif kind == "BULLET":
            _add_marked_text(doc.add_paragraph(style=doc.styles["Pleading Bullet"]), "•\t" + text)
        elif kind == "DATED":
            pass  # emitted with the signature block
        elif kind == "SIG":
            dated = next(t for k, t in blocks if k == "DATED")
            add_signature(doc, dated)
        else:
            _add_marked_text(doc.add_paragraph(style=doc.styles["Pleading Body"]), text)
    # A bullet run ends with a blank pleading line before the next block.
    paras = doc.paragraphs
    for a, b in zip(paras, paras[1:]):
        if a.style.name == "Pleading Bullet" and b.style.name != "Pleading Bullet":
            a.paragraph_format.space_after = Pt(24)
    if paras and paras[-1].style.name == "Pleading Bullet":
        paras[-1].paragraph_format.space_after = Pt(24)
    doc.core_properties.author = AUTHOR
    doc.save(dest)
    sanitize_package(dest, " ".join(meta["heading"]), f"{SHORT_CAPTION}, Case No. {CASE_NO}")


# ======================================================================
# DOCX -> pleading-paper PDF via lib/pleading_paper.PleadingPaper
# ======================================================================

def _para_markup(p) -> str:
    out = []
    for r in p.runs:
        t = r.text
        if not t:
            continue
        out.append(f"<<b:{t}>>" if r.bold else t)
    return "".join(out).replace("\t", " ")


def render_pdf_from_docx(key: str, docx_path: Path, pdf_path: Path) -> None:
    doc = Document(str(docx_path))
    title = footer_title(key) + (f" -- {DRAFT_MARKER}" if REVIEW_DRAFT else "")
    d = PleadingPaper(str(pdf_path), doc_title_footer=title)
    c = d.c
    body = doc.element.body
    from docx.table import Table
    from docx.text.paragraph import Paragraph
    for el in body.iterchildren():
        if el.tag == qn("w:tbl"):
            t = Table(el, doc)
            left, right = [], []
            for row in t.rows:
                for cell, acc in zip(row.cells, (left, right)):
                    p = cell.paragraphs[0]
                    # The last left row holds only a tab-leader rule for Word;
                    # a raw tab would print as a black box in the PDF.
                    txt = p.text.replace("\t", "").rstrip()
                    acc.append((txt, any(r.bold for r in p.runs if r.text.strip()), False))
            while left and not left[-1][0] and (not right or not right[len(left) - 1][0]):
                left.pop()
            right = [r for r in right]
            while right and not right[-1][0]:
                right.pop()
            d.draw_caption_block(left, right, caption_size=10, tight_lh=13, boxed=True)
            d.blank_line()
            continue
        if el.tag != qn("w:p"):
            continue
        p = Paragraph(el, doc)
        style = p.style.name
        text = p.text
        if style == "Pleading Party Info":
            y0 = d._line_y(0)
            for i, line in enumerate(text.split("\n")):
                c.setFont("Times-Bold" if i == 0 else "Times-Roman", 12)
                c.drawString(CONTENT_LEFT, y0 - i * 15, line)
            d.current_line = 7  # Civil L.R. 3-4(a)(3): court title commences on line 8
        elif style == "Pleading Court Title":
            for line in text.split("\n"):
                d.write_line(line, bold=True, center=True)
            d.blank_line()
        elif style == "Pleading Document Title":
            d.ensure_space(4)
            for line in text.split("\n"):
                d.write_line(line, bold=True, center=True)
            d.blank_line()
        elif style == "Pleading Heading":
            d.ensure_space(4)
            d.write_line(text, bold=True, center=True)
            d.blank_line()
        elif style == "Pleading Request Label":
            d.ensure_space(3)
            d.write_line(text, bold=True)
        elif style == "Pleading Body":
            d.write_wrapped(_para_markup(p), first_indent=36)
            d.blank_line()
        elif style in ("Pleading Body Flush", "Pleading List"):
            d.write_wrapped(_para_markup(p), first_indent=0)
            d.blank_line()
        elif style == "Pleading Bullet":
            d.write_wrapped(_para_markup(p).replace("•", "•", 1), indent=18, first_indent=0)
            if p.paragraph_format.space_after and p.paragraph_format.space_after.pt >= 24:
                d.blank_line()
        elif style == "Pleading Signature Date":
            d.ensure_space(11)
            d.write_line(text)
            d.blank_line()
        elif style == "Pleading Signoff":
            d.write_respectfully_submitted()
        elif style == "Pleading Signature Image":
            if not p._p.xpath(".//pic:pic"):
                raise SystemExit(f"{docx_path.name}: signature paragraph has no inline image")
            d.draw_signature_image(SIGNATURE_PATH, SIGNATURE_NATIVE_PX[0], SIGNATURE_NATIVE_PX[1],
                                   SIG_LINE, width=220, x_offset=15)
            d.write_line(SIG_LINE, right=True, right_margin_offset=20)
        elif style == "Pleading Signer":
            d.write_line(text, right=True, right_margin_offset=20)
        elif text.strip():
            raise SystemExit(f"{docx_path.name}: unhandled paragraph style {style!r}")
    d.save()


# ======================================================================
# Proofs of service (lib/proof_of_service.py)
# ======================================================================

def pos_fields(key: str) -> ProofOfServiceFields:
    meta = DOCS[key]
    amazon = meta["defendant"] == AMAZON
    recipients = list(SERVICE_LIST)
    who = "Amazon.com Services, LLC" if amazon else "Accurate Background, LLC"
    doc_title = f"Plaintiff's {KIND_NAME[meta['kind']]} to Defendant {who} (Set One)"
    early = meta["kind"] == "RFP"
    if early:
        recipients += EARLY_DELIVERY_NOTE
        doc_title += ", delivered under Fed. R. Civ. P. 26(d)(2)"
    return ProofOfServiceFields(
        plaintiff_line="BRENDAN NGEHSI NEWANFORBI",
        plaintiff_role="Plaintiff",
        defendant_lines=["AMAZON.COM SERVICES, LLC; ACCURATE", "BACKGROUND, LLC; and DOES 1-10, inclusive"],
        defendant_role="Defendants",
        case_number=CASE_NO,
        title="PROOF OF SERVICE",
        service_date=SIGN_DATE if early else "",
        document_title=doc_title,
        mailing_location=MAILED_FROM,
        recipients=recipients,
        server_name=SIGNER,
        stamp_signature=early,
        district_line=DISTRICT_NDCAL,
        by_email=False,
        also_email=True,  # first-class U.S. Mail and e-mail, same day
        signature_on_second_page=True,
    )


# ======================================================================
# 00 checklist (internal; not served): plain review rendering
# ======================================================================

def build_internal_docx(source: Path, dest: Path) -> None:
    doc = Document()
    _set_style_fonts(doc.styles["Normal"], 11, False)
    doc.styles["Normal"].paragraph_format.space_after = Pt(5)
    for h in ("Heading 1", "Heading 2"):
        _set_style_fonts(doc.styles[h], 11, True)
        doc.styles[h].font.color.rgb = None
    sec = doc.sections[0]
    sec.top_margin = sec.bottom_margin = Inches(0.8)
    sec.left_margin = sec.right_margin = Inches(1.0)
    hp = sec.header.paragraphs[0]
    hp.text = f"CASE NO. {CASE_NO} | INTERNAL CHECKLIST — NOT FOR SERVICE"
    hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    body = doc.element.body
    for p in list(body.iterchildren(qn("w:p"))):
        body.remove(p)
    for block in re.split(r"\n\s*\n", source.read_text(encoding="utf-8")):
        t = block.strip()
        if not t:
            continue
        if t.startswith("# "):
            doc.add_paragraph(t[2:], style="Heading 1")
        elif t.startswith("## "):
            doc.add_paragraph(t[3:], style="Heading 2")
        else:
            _add_marked_text(doc.add_paragraph(style="Normal"), t)
    doc.save(dest)
    sanitize_package(dest, "Matter 29 Discovery Deployment Plan (internal)", f"{SHORT_CAPTION}, Case No. {CASE_NO}")


def lo_convert(paths: list[Path], outdir: Path) -> None:
    cmd = shutil.which("libreoffice") or shutil.which("soffice")
    if not cmd:
        raise SystemExit("LibreOffice is needed: install libreoffice-writer")
    subprocess.run([cmd, "-env:UserInstallation=file:///tmp/m29-lo-profile", "--headless",
                    "--convert-to", "pdf", "--outdir", str(outdir), *map(str, paths)],
                   check=True, timeout=300, capture_output=True)


def main() -> None:
    if not Path(SIGNATURE_PATH).is_file():
        raise SystemExit(f"Missing portfolio signature image: {SIGNATURE_PATH}")
    OUT.mkdir(parents=True, exist_ok=True)
    for stale in OUT.glob("*"):
        if stale.is_file():
            stale.unlink()
    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t)
        # 00 internal checklist (LibreOffice render is fine: not a court paper).
        build_internal_docx(ROOT / "00_README_Deployment_and_Checklist.md", OUT / "00_README_Deployment_and_Checklist.docx")
        lo_convert([OUT / "00_README_Deployment_and_Checklist.docx"], OUT)
        pos_pdfs = {}
        for key in PLEADING_DOCS:
            docx_path = OUT / f"{key}.docx"
            build_docx(key, docx_path)
            body_pdf = tmp / f"{key}.body.pdf"
            render_pdf_from_docx(key, docx_path, body_pdf)
            parts = [body_pdf]
            if key in SERVED_SETS:
                pos_pdf = tmp / f"{key}.pos.pdf"
                build_proof_of_service(pos_pdf, pos_fields(key))
                pos_pdfs[key] = pos_pdf
                parts.append(pos_pdf)
            assemble(parts, OUT / f"{key}.pdf")
        for packet, keys in SERVICE_PACKETS.items():
            assemble([pos_pdfs[k] for k in keys], OUT / f"{packet}.pdf")
        order = ["00_README_Deployment_and_Checklist"] + PLEADING_DOCS + list(SERVICE_PACKETS)
        assemble([OUT / f"{k}.pdf" for k in order], OUT / "Matter_29_Complete_Discovery_Packet.pdf")
        assemble([OUT / f"{k}.pdf" for k in ("01_Amazon_RFP_Set_One", "03_Amazon_Interrogatories_Set_One", "05_Amazon_RFA_Set_One")],
                 OUT / "Matter_29_Amazon_Discovery_Combined.pdf")
        assemble([OUT / f"{k}.pdf" for k in ("02_Accurate_RFP_Set_One", "04_Accurate_Interrogatories_Set_One", "06_Accurate_RFA_Set_One")],
                 OUT / "Matter_29_Accurate_Discovery_Combined.pdf")
    zip_path = OUT / "Matter_29_Complete_Discovery_Packet_DOCX_PDF.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(OUT.glob("*.docx")) + sorted(OUT.glob("*.pdf")):
            z.write(p, arcname=p.name)
        z.write(ROOT / "12_Cover_Email_Templates_NOT_SENT.txt", arcname="12_Cover_Email_Templates_NOT_SENT.txt")
        z.write(ROOT / "package_manifest.json", arcname="package_manifest.json")
    n_docx = len(list(OUT.glob("*.docx")))
    n_pdf = len(list(OUT.glob("*.pdf")))
    print(f"Built {n_docx} DOCX and {n_pdf} PDFs (pleading paper via lib/pleading_paper.py; "
          f"proofs via lib/proof_of_service.py); archive: {zip_path}")


if __name__ == "__main__":
    main()
