#!/usr/bin/env python3
"""Build this private FAC with the portfolio's existing DOCX/PDF formatters.

The selected DOCX helpers are loaded directly from the existing discovery
formatter's AST, without executing that script's unrelated packet/service
imports or main routine. PDF rendering uses lib/pleading_paper.py unchanged.
Run from any directory with Python containing python-docx, Pillow, reportlab.
"""
import ast
import datetime as _dt
import re
import sys
import zipfile
from pathlib import Path

from PIL import Image
from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.table import WD_ROW_HEIGHT_RULE
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK, WD_LINE_SPACING
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn
from docx.shared import Inches, Pt

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
SCRIPTS = REPO / 'internal/scripts'
sys.path.insert(0, str(SCRIPTS / 'lib'))
from pleading_paper import (CONTENT_LEFT, CONTENT_RIGHT, CONTENT_WIDTH,
    LINE_SPACING, NUM_LINES, PAGE_H, PAGE_W, VERT_LINE_LEFT, VERT_LINE_RIGHT,
    PleadingPaper)

# Embed available Times-compatible Type 1 faces so the PDF does not depend
# on a viewer's substitute-font metrics. The shared page engine is unchanged.
from reportlab.pdfbase import pdfmetrics
for alias, face_name in [('Times-Roman', 'NimbusRoman-Regular'),
                         ('Times-Bold', 'NimbusRoman-Bold'),
                         ('Times-Italic', 'NimbusRoman-Italic'),
                         ('Times-BoldItalic', 'NimbusRoman-BoldItalic'),
                         ('Helvetica', 'NimbusSans-Regular')]:
    afm = Path('/usr/share/fonts/type1/urw-base35') / (face_name + '.afm')
    pfb = Path('/usr/share/fonts/X11/Type1') / (face_name + '.pfb')
    if afm.exists() and pfb.exists():
        face = pdfmetrics.EmbeddedType1Face(str(afm), str(pfb))
        pdfmetrics.registerTypeFace(face)
        pdfmetrics.registerFont(pdfmetrics.Font(alias, face.name, 'WinAnsiEncoding'))

_BasePaper = PleadingPaper
class PleadingPaper(_BasePaper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.c.setTitle('First Amended Complaint - 4:26-cv-09249-ASK')
        self.c.setAuthor('BRENDAN NGEHSI NEWANFORBI')
        self.c.setSubject('Private draft - not filed')

HELPER_SOURCE = SCRIPTS / 'build_matter29_discovery_packet.py'
HELPERS = {'_set_style_fonts', '_pstyle', 'setup_styles', '_rule',
    '_line_number_box', 'setup_header_footer', '_cell_border',
    'add_caption_table', 'add_signature', 'sanitize_package',
    '_para_markup', 'render_pdf_from_docx'}
tree = ast.parse(HELPER_SOURCE.read_text())
selected = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in HELPERS]
assert {n.name for n in selected} == HELPERS

FONT = 'Times New Roman'
TOP_TW, BOTTOM_TW = 1080, 1300
LEFT_TW = round(CONTENT_LEFT * 20)
RIGHT_TW = round((PAGE_W - CONTENT_RIGHT + 16) * 20)
HEADER_TW, FOOTER_TW = 360, 288
REVIEW_DRAFT = True
DRAFT_MARKER = 'DRAFT - NOT FILED'
AUTHOR = SIGNER = 'BRENDAN NGEHSI NEWANFORBI'
SIGNER_ROLE = 'Plaintiff, In Pro Per'
SIGNATURE_PATH = str(REPO / 'internal/assets/signature/brendan-newanforbi-signature.png')
SIGNATURE_NATIVE_PX = Image.open(SIGNATURE_PATH).size
SIGNATURE_ASPECT = SIGNATURE_NATIVE_PX[1] / SIGNATURE_NATIVE_PX[0] * 1.15
SIG_LINE = '_' * 34
def _resolve_stamp_path(path):
    if Path(path).resolve() != Path(SIGNATURE_PATH).resolve():
        raise ValueError('Only the existing canonical portfolio signature is permitted')
    return path
def footer_title(key):
    return 'FIRST AMENDED COMPLAINT - 4:26-cv-09249-ASK'

CAPTION_LEFT = [
    ('BRENDAN NGEHSI NEWANFORBI,', True), ('', False),
    ('                    Plaintiff,', False), ('', False), ('v.', False), ('', False),
    ('AMAZON.COM SERVICES, LLC, a Delaware', False),
    ('limited liability company; ACCURATE', False),
    ('BACKGROUND LLC, a California limited', False),
    ('liability company; and DOES 1-10, inclusive,', False),
    ('', False), ('                    Defendants.', False), ('', False), ('', False)]
RIGHT_CAPTION = [
    ('Case No. 4:26-cv-09249-ASK', False), ('', False),
    ('FIRST AMENDED COMPLAINT', True), ('FOR DAMAGES', True), ('', False),
    ('(1) FCRA, 15 U.S.C. § 1681e(b)', False),
    ('(2) ICRAA, Civ. Code § 1786.20(b)', False),
    ('(3) FCRA, 15 U.S.C. § 1681b(b)(3)(A)', False),
    ('(4) ICRAA, Civ. Code § 1786.40(a)', False), ('', False),
    ('Hon. Ajay S. Krishnan', False), ('JURY TRIAL DEMANDED', True),
    ('', False), ('', False)]
CAPTION_ROWS = max(len(CAPTION_LEFT), len(RIGHT_CAPTION))
exec(compile(ast.Module(body=selected, type_ignores=[]), str(HELPER_SOURCE), 'exec'), globals())

def build():
    source = HERE / 'First_Amended_Complaint.md'
    text = source.read_text()
    doc = Document()
    setup_styles(doc)
    setup_header_footer(doc, 'fac')
    for name in ['Normal', 'Title', 'Heading 1', 'Heading 2', 'Heading 3']:
        _set_style_fonts(doc.styles[name], 12, name != 'Normal')
        doc.styles[name].font.color.rgb = __import__('docx').shared.RGBColor(0, 0, 0)
    p = doc.add_paragraph(style='Pleading Party Info')
    for i, line in enumerate(text.splitlines()[:6]):
        if i: p.add_run().add_break(WD_BREAK.LINE)
        p.add_run(line).bold = (i == 0)
    p = doc.add_paragraph(style='Pleading Court Title')
    p.add_run('UNITED STATES DISTRICT COURT').add_break(WD_BREAK.LINE)
    p.add_run('NORTHERN DISTRICT OF CALIFORNIA').add_break(WD_BREAK.LINE)
    p.add_run('OAKLAND DIVISION')
    add_caption_table(doc, RIGHT_CAPTION)
    doc.add_paragraph('FIRST AMENDED COMPLAINT FOR DAMAGES', style='Pleading Document Title')
    body = text.split('JURY TRIAL DEMANDED\n\n', 1)[1]
    body = body.split('\nDated: ', 1)[0]
    for block in body.strip().split('\n\n'):
        if block.startswith('## ' ) or block.startswith('### '):
            for heading in block.splitlines():
                if heading.startswith('### '):
                    doc.add_paragraph(heading[4:], style='Pleading Request Label')
                else:
                    doc.add_paragraph(heading[3:], style='Pleading Heading')
        else:
            p = doc.add_paragraph(block, style='Pleading Body')
    add_signature(doc, '____________')
    doc.core_properties.author = AUTHOR
    dest = HERE / 'First_Amended_Complaint.docx'
    doc.save(dest)
    sanitize_package(dest, 'First Amended Complaint', 'Newanforbi v. Amazon.com Services, LLC et al.; 4:26-cv-09249-ASK')
    render_pdf_from_docx('fac', dest, HERE / 'First_Amended_Complaint.pdf')
    print('Built First_Amended_Complaint.docx and First_Amended_Complaint.pdf')

if __name__ == '__main__':
    build()
