#!/usr/bin/env python3
"""Matter 42 -- Nforbi v. Staples The Office Superstore, LLC (N.D. Cal., San Jose).

Complaint for Damages and Injunctive Relief on portfolio pleading paper.
Pipeline follows internal/scripts/build_matter29_discovery_packet.py:
  1. Source paragraphs (extracted verbatim from the LibreOffice complaint PDF,
     src/paras.json) -> Word pleading-paper DOCX (Times New Roman 12, exact
     24-pt lines, 28 numbered lines in a header text box, rule lines in the
     header, inline signature image, named "Pleading ..." styles).
  2. The DOCX is read back by paragraph style and rendered onto
     lib/pleading_paper.PleadingPaper (the formatter engine); signature drawn
     with draw_signature_image from signature_stamp.SIGNATURE_PATH.
Writes to $M42_OUT (default /tmp/m42-staples-complaint); nothing to R2 or D1.
The committed copies live in documents/matter-42/ndcal/to-file/ under
descriptive names (final, not yet filed).

    python3 internal/scripts/matter42-staples-complaint.py
"""
from __future__ import annotations

import datetime as _dt
import json
import os
import re
import sys
import zipfile
from pathlib import Path

sys.dont_write_bytecode = True
REPO = Path(__file__).resolve().parents[2]
SCRIPTS = REPO / "internal" / "scripts"
sys.path.insert(0, str(SCRIPTS / "lib"))
sys.path.insert(0, str(SCRIPTS))

from docx import Document  # noqa: E402
from docx.enum.style import WD_STYLE_TYPE  # noqa: E402
from docx.enum.table import WD_ROW_HEIGHT_RULE  # noqa: E402
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK, WD_LINE_SPACING  # noqa: E402
from docx.oxml import OxmlElement, parse_xml  # noqa: E402
from docx.oxml.ns import qn  # noqa: E402
from docx.shared import Inches, Pt  # noqa: E402
from reportlab.pdfbase.pdfmetrics import stringWidth  # noqa: E402

from pleading_paper import (  # noqa: E402
    CONTENT_LEFT, CONTENT_RIGHT, CONTENT_WIDTH, LINE_SPACING, NUM_LINES, PAGE_H, PAGE_W,
    VERT_LINE_LEFT, VERT_LINE_RIGHT, PleadingPaper,
)
from signature_stamp import (  # noqa: E402
    SIGNATURE_ASPECT, SIGNATURE_NATIVE_PX, SIGNATURE_PATH, _resolve_stamp_path,
)

SRC = REPO / "internal/docs/matter-42/ndcal/staples-complaint-source-paragraphs.json"
OUT = Path(os.environ.get("M42_OUT", "/tmp/m42-staples-complaint"))
STEM = "Nforbi_v_Staples_Complaint_NDCal_SJ"

AUTHOR = "Brendan Ngwa Nforbi"
FOOTER = "COMPLAINT FOR DAMAGES AND INJUNCTIVE RELIEF"
SIG_LINE = "___________________________________"
FONT = "Times New Roman"

# ---------------------------------------------------------------- source
# User instruction (Oct 19, 2026): no exhibits will be attached -- remove every
# exhibit mention with the smallest edit. Each pair is (paragraph prefix, exact
# sentence removed); every removed sentence existed only to point to an exhibit.
EXHIBIT_SENTENCES = [
    ("16. ", " A true and correct copy of the posting may be attached as Exhibit D."),
    ("18. ", " A true and correct copy of the offer email may be attached as Exhibit A."),
    ("22. ", " A true and correct copy may be attached as Exhibit C."),
    ("24. ", " A true and correct copy may be attached as Exhibit B."),
]


def load_paras():
    paras = json.loads(SRC.read_text(encoding="utf-8"))
    for prefix, sentence in EXHIBIT_SENTENCES:
        hits = [q for q in paras if q["text"].startswith(prefix)]
        assert len(hits) == 1 and hits[0]["text"].count(sentence) == 1, (prefix, sentence)
        hits[0]["text"] = hits[0]["text"].replace(sentence, "")
    # Drop the PROPOSED EXHIBITS heading and its A-D list entirely.
    k = next(i for i, q in enumerate(paras) if q["text"] == "PROPOSED EXHIBITS")
    assert all(q["text"].startswith("Exhibit ") for q in paras[k + 1:]) and len(paras) - k == 5
    paras = paras[:k]
    assert not any("Exhibit" in q["text"] for q in paras)
    # User-approved (Oct 19, 2026): new e-mail address everywhere it appears.
    n = 0
    for q in paras:
        n += q["text"].count("bnn.cdl@gmail.com")
        q["text"] = q["text"].replace("bnn.cdl@gmail.com", "brendan@ngwanforbi.com")
    assert n == 1, n
    # Counsel-block labels kept (user reversed the label removal, Oct 19, 2026).
    assert paras[3]["text"] == "Telephone: (209) 801-4442" and paras[4]["text"] == "Email: brendan@ngwanforbi.com"
    # User-approved (Oct 19, 2026): new opening line.
    assert paras[22]["text"] == "Plaintiff Brendan Ngwa Nforbi alleges as follows:"
    paras[22]["text"] = "Plaintiff BRENDAN NGWA NFORBI, appearing on his own behalf, alleges:"
    return paras


P = [p["text"] for p in load_paras()]
# Indices into the verbatim source paragraph list (see paras.py listing).
PARTY_BLOCK = [(P[0], True), (P[5], False), (P[1], False), (P[2], False), (P[3], False), (P[4], False)]
COURT_LINES = [P[6], P[7]]  # SAN JOSE DIVISION (P[8]) dropped at user request
CASE_LINE = P[14]
TITLE = P[15]
CLAIMS = P[16:20]
JURY_CAPTION = P[20]
assert P[9].startswith("BRENDAN NGWA NFORBI") and P[12].startswith("STAPLES") and P[13] == "Defendants."
assert TITLE == P[21] == FOOTER and JURY_CAPTION == "JURY TRIAL DEMANDED"


def classify(paras):
    """Body blocks from source paragraph 21 onward -> (kind, text)."""
    blocks, i = [], 21
    while i < len(paras):
        p = paras[i]
        t, bold = p["text"], p["bold"]
        if i == 21:
            pass  # repeated body title under the caption: deleted (user-approved Oct 19, 2026)
        elif bold and t.endswith("CAUSE OF ACTION"):
            blocks.append(("COA", t))
            blocks.append(("COATITLE", paras[i + 1]["text"]))
            i += 1
        elif bold and re.match(r"[A-F]\. ", t):
            blocks.append(("SUB", t))
        elif bold:
            blocks.append(("H", t))
        elif t.startswith("Dated:"):
            blocks.append(("DATED", t))
        elif t == "Respectfully submitted,":
            blocks.append(("SIGNOFF", t))
        elif set(t) == {"_"}:
            blocks.append(("SIGIMG", t))
        elif t == "BRENDAN NGWA NFORBI":
            blocks.append(("SIGNER", t))
        elif t == "Plaintiff, In Propria Persona" and i > 30:
            blocks.append(("ROLE", t))
        elif re.match(r"(\d+|[A-M])\. ", t) or t.startswith("Exhibit "):
            blocks.append(("NUM", t))
        else:
            blocks.append(("BODY", t))
        i += 1
    return blocks


# ---------------------------------------------------------------- caption
CAP_PT = 10
RIGHT_AVAIL = 196.0   # fits both the PDF right column (206 pt) and the Word cell (207 pt)


NBSP = "\u00a0"


def glue(text):
    """Keep a section sign with its number on one line (PDF layout only)."""
    return re.sub(r"(§§?) ", lambda m: m.group(1) + NBSP, text)


def wrap(text, font, size, avail, cont_indent=""):
    """Width wrap; a section sign never ends a line. Returns plain-space lines."""
    words, lines, cur = glue(text).split(" "), [], ""
    for w in words:
        trial = (cur + " " + w) if cur else w
        lead = cont_indent if lines else ""
        if cur and stringWidth(lead + trial, font, size) > avail:
            lines.append(lead + cur)
            cur = w
        else:
            cur = trial
    lines.append((cont_indent if lines else "") + cur)
    return [ln.replace(NBSP, " ") for ln in lines]


def caption_rows():
    right = [(CASE_LINE, False), ("", False)]
    right += [(t, True) for t in wrap(TITLE, "Times-Bold", CAP_PT, RIGHT_AVAIL)]
    right += [("", False)]
    for c in CLAIMS:
        right += [(t, False) for t in wrap(c, "Times-Roman", CAP_PT, RIGHT_AVAIL, cont_indent="     ")]
    right += [("", False), (JURY_CAPTION, True)]
    # Explicit break after "LLC;" (user request); NBSP keeps "SUPERSTORE, LLC;" together in Word.
    head, tail = P[12].split("LLC; ", 1)
    assert head == "STAPLES THE OFFICE SUPERSTORE, " and tail == "and DOES 1 through 25, inclusive,"
    dfn = [head.rstrip() + NBSP + "LLC;", tail]
    left_top = [(P[9], True), ("", False), ("                          " + P[10], False), ("", False),
                ("       " + P[11], False), ("", False)] + [(t, True) for t in dfn]
    rows = max(len(right), len(left_top) + 2)
    rows += rows % 2  # even: rows x 12 pt fill whole pleading lines in Word
    left = left_top + [("", False)] * (rows - len(left_top) - 1) + [("                          " + P[13], False)]
    right += [("", False)] * (rows - len(right))
    return left, right, rows


# ---------------------------------------------------------------- DOCX
TOP_TW, BOTTOM_TW = 1080, 1300
LEFT_TW = round(CONTENT_LEFT * 20)
RIGHT_TW = round((PAGE_W - CONTENT_RIGHT + 16) * 20)
HEADER_TW, FOOTER_TW = 360, 288


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
    _pstyle(doc, "Pleading Party Info", exact=12, after=72)          # 6 lines: court title on line 7 (user request)
    _pstyle(doc, "Pleading Court Title", bold=True, align=C, after=24)  # 1 blank line (9): caption on line 10
    _pstyle(doc, "Pleading Caption", size=CAP_PT, exact=12)
    _pstyle(doc, "Pleading Document Title", bold=True, align=C, before=24, after=24, keep_next=True)
    _pstyle(doc, "Pleading Heading", bold=True, align=C, after=24, keep_next=True)
    _pstyle(doc, "Pleading Claim Heading", bold=True, align=C, after=0, keep_next=True)
    _pstyle(doc, "Pleading Claim Title", bold=True, align=C, left=36, right=36, after=24, keep_next=True)
    _pstyle(doc, "Pleading Subheading", bold=True, after=24, keep_next=True)
    _pstyle(doc, "Pleading Body", first=36, after=24)
    _pstyle(doc, "Pleading Numbered", left=0, first=0, after=24)  # flush left, no hanging (user sample)
    _pstyle(doc, "Pleading Signature Date", after=0, keep_next=True)
    _pstyle(doc, "Pleading Signoff", align=R, right=20, keep_next=True)
    _pstyle(doc, "Pleading Signature Image", align=R, right=20, exact=48, keep_next=True)
    _pstyle(doc, "Pleading Signer", bold=True, align=R, right=20, keep_next=True)
    _pstyle(doc, "Pleading Signer Role", align=R, right=20, after=24)
    _pstyle(doc, "Pleading Line Number", align=R, base=None)
    _pstyle(doc, "Pleading Header", size=1, exact=1, base=None)
    _pstyle(doc, "Pleading Footer", size=10, exact=12, align=C, base=None)
    _pstyle(doc, "Pleading Footer Title", size=8, exact=10, align=C, base=None)


def _rule(shape_no, x_pt):
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
        for i in range(1, NUM_LINES + 1))
    left = 36.0
    width = (VERT_LINE_LEFT - 6) - left
    return (
        '<v:shapetype id="_x0000_t202" coordsize="21600,21600" o:spt="202" path="m,l,21600r21600,l21600,xe">'
        '<v:stroke joinstyle="miter"/><v:path gradientshapeok="t" o:connecttype="rect"/></v:shapetype>'
        f'<v:shape id="PleadingLineNumbers" o:spid="_x0000_s2001" type="#_x0000_t202" '
        f'style="position:absolute;margin-left:{left:.2f}pt;margin-top:{top_pt:.2f}pt;width:{width:.2f}pt;'
        f'height:{NUM_LINES * LINE_SPACING + 6}pt;z-index:-251649000;mso-position-horizontal-relative:page;'
        f'mso-position-vertical-relative:page" filled="f" stroked="f">'
        f'<v:textbox inset="0,0,0,0"><w:txbxContent>{paras}</w:txbxContent></v:textbox></v:shape>')


def setup_header_footer(doc):
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Inches(8.5), Inches(11)
    sec.top_margin = Pt(TOP_TW / 20)
    sec.bottom_margin = Pt(BOTTOM_TW / 20)
    sec.left_margin = Pt(LEFT_TW / 20)
    sec.right_margin = Pt(RIGHT_TW / 20)
    sec.header_distance = Pt(HEADER_TW / 20)
    sec.footer_distance = Pt(FOOTER_TW / 20)
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
    ft.add_paragraph(FOOTER, style=doc.styles["Pleading Footer Title"])


def _cell_border(cell, **edges):
    tcpr = cell._tc.get_or_add_tcPr()
    b = OxmlElement("w:tcBorders")
    for edge in ("top", "left", "bottom", "right"):
        el = OxmlElement(f"w:{edge}")
        if edge in edges:
            for k, v in (("w:val", "single"), ("w:sz", "6"), ("w:space", "0"), ("w:color", "000000")):
                el.set(qn(k), v)
        else:
            el.set(qn("w:val"), "nil")
        b.append(el)
    tcpr.append(b)


def add_caption_table(doc):
    left, right, rows = caption_rows()
    tbl = doc.add_table(rows=rows, cols=2)
    tbl.autofit = False
    tblpr = tbl._tbl.tblPr
    el = tblpr.find(qn("w:tblStyle"))
    if el is not None:
        tblpr.remove(el)
    mar = OxmlElement("w:tblCellMar")
    for edge, w in (("top", 0), ("bottom", 0), ("left", 115), ("right", 115)):
        e = OxmlElement(f"w:{edge}")
        e.set(qn("w:w"), str(w))
        e.set(qn("w:type"), "dxa")
        mar.append(e)
    tblpr.append(mar)
    body_w = 12240 - LEFT_TW - RIGHT_TW
    widths = [round(body_w * 0.52), body_w - round(body_w * 0.52)]
    grid = tbl._tbl.tblGrid
    for gc, w in zip(grid.findall(qn("w:gridCol")), widths):
        gc.set(qn("w:w"), str(w))
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
                if i == rows - 1:
                    # bottom rule as an underscore tab leader (a cell bottom border
                    # adds height in LibreOffice and shifts lines off the numbers)
                    pos = widths[0] - 2 * 115 - 20
                    tabs = OxmlElement("w:tabs")
                    tab = OxmlElement("w:tab")
                    for k, v in (("w:val", "right"), ("w:leader", "underscore"), ("w:pos", str(pos))):
                        tab.set(qn(k), v)
                    tabs.append(tab)
                    p._p.get_or_add_pPr().append(tabs)
                    p.add_run().add_tab()
            else:
                _cell_border(cell)
    return tbl


def add_signature_image(doc):
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


def sanitize_package(path: Path, title: str, subject: str):
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
        "<cp:category></cp:category></cp:coreProperties>")
    app = (
        "<?xml version='1.0' encoding='UTF-8' standalone='yes'?>\n"
        '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
        'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">'
        "<Template>Normal.dotm</Template><DocSecurity>0</DocSecurity><ScaleCrop>false</ScaleCrop>"
        "<Company></Company><LinksUpToDate>false</LinksUpToDate><SharedDoc>false</SharedDoc>"
        "<HyperlinksChanged>false</HyperlinksChanged></Properties>")
    src = zipfile.ZipFile(path)
    items = {n: src.read(n) for n in src.namelist()}
    src.close()
    for n in list(items):
        if n.startswith("customXml/") or n == "docProps/thumbnail.jpeg":
            del items[n]
    items["docProps/core.xml"] = core.encode()
    items["docProps/app.xml"] = app.encode()
    items["_rels/.rels"] = re.sub(r'<Relationship [^>]*thumbnail[^>]*/>', "", items["_rels/.rels"].decode()).encode()
    drels = items["word/_rels/document.xml.rels"].decode()
    items["word/_rels/document.xml.rels"] = re.sub(r'<Relationship [^>]*customXml[^>]*/>', "", drels).encode()
    ct = re.sub(r'<Override PartName="/customXml/[^>]*/>', "", items["[Content_Types].xml"].decode())
    items["[Content_Types].xml"] = ct.encode()
    s = items["word/settings.xml"].decode().replace(
        'w:name="compatibilityMode" w:uri="http://schemas.microsoft.com/office/word" w:val="14"',
        'w:name="compatibilityMode" w:uri="http://schemas.microsoft.com/office/word" w:val="15"')
    items["word/settings.xml"] = s.encode()
    order = ["[Content_Types].xml"] + [n for n in items if n != "[Content_Types].xml"]
    tmp = path.with_suffix(".tmp")
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as z:
        for n in order:
            z.writestr(n, items[n])
    tmp.replace(path)


STYLE_OF = {"TITLE": "Pleading Document Title", "H": "Pleading Heading", "COA": "Pleading Claim Heading",
            "COATITLE": "Pleading Claim Title", "SUB": "Pleading Subheading", "BODY": "Pleading Body",
            "NUM": "Pleading Numbered", "DATED": "Pleading Signature Date", "SIGNOFF": "Pleading Signoff",
            "SIGNER": "Pleading Signer", "ROLE": "Pleading Signer Role"}


# heading(1) + blank(1) + jury text(<=3) + blank(1) + Dated..role(7)
JURY_UNIT_LINES = 13


def nxt_is_dated(blocks, text):
    for (k, t), (k2, _) in zip(blocks, blocks[1:]):
        if t == text and k == "BODY":
            return k2 == "DATED"
    return False


def build_docx(dest: Path):
    paras = load_paras()
    blocks = classify(paras)
    doc = Document()
    setup_styles(doc)
    setup_header_footer(doc)
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
    add_caption_table(doc)
    first_body = True
    for kind, text in blocks:
        if kind == "BODY" and first_body:
            first_body = False
            para = doc.add_paragraph(text, style=doc.styles[STYLE_OF[kind]])
            para.paragraph_format.space_before = Pt(24)  # one blank line under the caption
            continue
        if kind == "SIGIMG":
            add_signature_image(doc)
        else:
            para = doc.add_paragraph(text, style=doc.styles[STYLE_OF[kind]])
            if kind == "BODY" and nxt_is_dated(blocks, text):
                para.paragraph_format.keep_with_next = True  # jury demand stays with signature
    doc.core_properties.author = AUTHOR
    doc.save(dest)
    sanitize_package(dest, TITLE, "Brendan Ngwa Nforbi v. Staples The Office Superstore, LLC (N.D. Cal., San Jose Division)")
    return blocks


# ---------------------------------------------------------------- PDF via formatter
def center_wrapped(d, text, bold=True, avail=None):
    fn = "Times-Bold" if bold else "Times-Roman"
    avail = avail or (CONTENT_WIDTH - 72)
    for line in wrap(text, fn, 12, avail):
        d.write_line(line, bold=bold, center=True)


class NoLeadingBlankPaper(PleadingPaper):
    """Formatter page with one rule added: a page never starts with a blank
    separator line (a separator that would land on line 1 is dropped)."""

    def blank_line(self):
        if self.current_line >= NUM_LINES:
            self.start_new_page()
            return
        if self.current_line == 0:
            return
        super().blank_line()


def render_pdf_from_docx(docx_path: Path, pdf_path: Path):
    from docx.table import Table
    from docx.text.paragraph import Paragraph
    doc = Document(str(docx_path))
    d = NoLeadingBlankPaper(str(pdf_path), doc_title_footer=FOOTER)
    c = d.c
    sig_stamped = None
    for el in doc.element.body.iterchildren():
        if el.tag == qn("w:tbl"):
            t = Table(el, doc)
            left, right = [], []
            for row in t.rows:
                for cell, acc in zip(row.cells, (left, right)):
                    cp = cell.paragraphs[0]
                    txt = cp.text.replace("\t", "").rstrip()  # tab-leader rule would print as a box
                    acc.append((txt, any(r.bold for r in cp.runs if r.text.strip()), False))
            while right and not right[-1][0]:
                right.pop()
            d.draw_caption_block(left, right, caption_size=CAP_PT, tight_lh=13, boxed=True)
            d.blank_line()
            continue
        if el.tag != qn("w:p"):
            continue
        p = Paragraph(el, doc)
        style, text = p.style.name, p.text
        if style == "Pleading Party Info":
            y0 = d._line_y(0)
            for i, line in enumerate(text.split("\n")):
                c.setFont("Times-Bold" if i == 0 else "Times-Roman", 12)
                c.drawString(CONTENT_LEFT, y0 - i * 15, line)
            d.current_line = 6  # court title on line 7 (user request)
        elif style == "Pleading Court Title":
            for line in text.split("\n"):
                d.write_line(line, bold=True, center=True)
            d.blank_line()  # line 9 blank: caption starts on line 10
        elif style == "Pleading Document Title":
            d.ensure_space(4)
            center_wrapped(d, text)
            d.blank_line()
        elif style == "Pleading Heading":
            d.ensure_space(JURY_UNIT_LINES if text == "DEMAND FOR JURY TRIAL" else 4)
            center_wrapped(d, text)
            d.blank_line()
        elif style == "Pleading Claim Heading":
            d.ensure_space(6)
            center_wrapped(d, text)
        elif style == "Pleading Claim Title":
            center_wrapped(d, text, avail=CONTENT_WIDTH - 110)
            d.blank_line()
        elif style == "Pleading Subheading":
            d.ensure_space(4)
            d.write_wrapped(f"<<b:{text}>>", first_indent=0)
            d.blank_line()
        elif style == "Pleading Body":
            d.write_wrapped(glue(text), first_indent=36)
            d.blank_line()
        elif style == "Pleading Numbered":
            d.write_wrapped(glue(text), indent=0, first_indent=0)  # flush left, no hanging
            d.blank_line()
        elif style == "Pleading Signature Date":
            d.ensure_space(8)
            d.write_line(text)
        elif style == "Pleading Signoff":
            d.write_respectfully_submitted()
        elif style == "Pleading Signature Image":
            if not p._p.xpath(".//pic:pic"):
                raise SystemExit("signature paragraph has no inline image")
            d.draw_signature_image(SIGNATURE_PATH, SIGNATURE_NATIVE_PX[0], SIGNATURE_NATIVE_PX[1],
                                   SIG_LINE, width=220, x_offset=0)
            sig_stamped = (d.page_num, d.current_line + 1)
            d.write_line(SIG_LINE, right=True, right_margin_offset=20)
        elif style == "Pleading Signer":
            d.write_line(text, bold=True, right=True, right_margin_offset=20)
        elif style == "Pleading Signer Role":
            d.write_line(text, right=True, right_margin_offset=20)
            d.blank_line()
        elif text.strip():
            raise SystemExit(f"unhandled paragraph style {style!r}")
    d.save()
    return d.page_num, sig_stamped


def main():
    if not Path(SIGNATURE_PATH).is_file():
        raise SystemExit(f"Missing signature image: {SIGNATURE_PATH}")
    OUT.mkdir(parents=True, exist_ok=True)
    docx_path = OUT / f"{STEM}.docx"
    pdf_path = OUT / f"{STEM}.pdf"
    blocks = build_docx(docx_path)
    pages, sig = render_pdf_from_docx(docx_path, pdf_path)
    print(f"blocks={len(blocks)} pages={pages} signature(page,line)={sig}")
    print(docx_path)
    print(pdf_path)


if __name__ == "__main__":
    main()
