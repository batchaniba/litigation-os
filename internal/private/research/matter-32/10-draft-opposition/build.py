# -*- coding: utf-8 -*-
import re, sys, subprocess, json
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer,
                                Table, TableStyle, PageBreak, Flowable, KeepTogether)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.units import inch
from pypdf import PdfReader, PdfWriter
sys.path.insert(0, '/home/user/workspace/m32-brief')
from content import BODY, SIGNATURE, AUTHORITIES, CASE_NO, SHORT_TITLE

FONT_DIR = '/usr/share/fonts/truetype/liberation/'
pdfmetrics.registerFont(TTFont('Serif', FONT_DIR + 'LiberationSerif-Regular.ttf'))
pdfmetrics.registerFont(TTFont('Serif-Bold', FONT_DIR + 'LiberationSerif-Bold.ttf'))
pdfmetrics.registerFont(TTFont('Serif-Italic', FONT_DIR + 'LiberationSerif-Italic.ttf'))
pdfmetrics.registerFont(TTFont('Serif-BoldItalic', FONT_DIR + 'LiberationSerif-BoldItalic.ttf'))
from reportlab.pdfbase.pdfmetrics import registerFontFamily
registerFontFamily('Serif', normal='Serif', bold='Serif-Bold', italic='Serif-Italic', boldItalic='Serif-BoldItalic')

W, H = letter
LEAD = 24.0
LINES = 28
FRAME_TOP = H - 1.0 * inch
FRAME_H = LINES * LEAD
FRAME_BOTTOM = FRAME_TOP - FRAME_H
LEFT = 1.25 * inch
RIGHT = 7.5 * inch
TEXT_W = RIGHT - LEFT
BASE_OFF = 12.0

OUT = '/home/user/workspace/m32-brief/'

def style(name, **kw):
    base = dict(fontName='Serif', fontSize=12, leading=LEAD, alignment=TA_JUSTIFY,
                spaceBefore=0, spaceAfter=0)
    base.update(kw)
    return ParagraphStyle(name, **base)

S_P = style('p', firstLineIndent=0.5 * inch)
S_NP = style('np')
S_H1 = style('h1', fontName='Serif-Bold', alignment=TA_CENTER, keepWithNext=1)
S_H2 = style('h2', fontName='Serif-Bold', alignment=TA_LEFT, leftIndent=0.5 * inch,
             firstLineIndent=-0.5 * inch, keepWithNext=1)
S_H3 = style('h3', fontName='Serif-Bold', alignment=TA_LEFT, leftIndent=1.0 * inch,
             firstLineIndent=-0.5 * inch, keepWithNext=1)
S_BQ = style('bq', leftIndent=1.0 * inch, rightIndent=0.5 * inch)
S_CAP = style('cap', alignment=TA_LEFT)
S_CAPC = style('capc', alignment=TA_CENTER)
S_CAPB = style('capb', fontName='Serif-Bold', alignment=TA_CENTER)
S_TOC = style('toc', alignment=TA_LEFT)
S_FOOT = ParagraphStyle('foot', fontName='Serif', fontSize=9, leading=11, alignment=TA_CENTER)

CASE_RE = re.compile(r'((?:[A-Z][A-Za-z\.&\u2019\' ]+?) v\. [A-Z][A-Za-z\.&\u2019\', ]+?(?:, Inc\.|, LLC)?)(?=, \d|\s\(|,\s\d)')

def italicize(t):
    # italicize case names, Id., id., See, see also, cf., supra
    names = ["Bell Atl. Corp. v. Twombly", "Bell Atlantic Corp. v. Twombly", "Bostock v. Clayton County", "Ashcroft v. Iqbal", "Twombly", "Starr v. Baca", "Starr",
             "Hebbe v. Pliler", "Khoja v. Orexigen Therapeutics, Inc.", "Khoja",
             "Benavidez v. County of San Diego", "Chism v. Washington State", "Chism",
             "Franks v. Delaware", "Franks", "Hervey v. Estes", "Hervey",
             "Galbraith v. County of Santa Clara", "Bell v. Burson",
             "Caldwell v. City & County of San Francisco", "Caldwell",
             "Costanich v. Department of Social & Health Services", "Costanich",
             "Hardwick v. Vreeken", "Spencer v. Peters", "United States v. Ngumezi", "Ngumezi",
             "Brigham City v. Stuart", "Brigham City", "United States v. Snipe", "Snipe",
             "Mincey v. Arizona", "Mincey", "Arizona v. Gant", "Sialoi v. City of San Diego", "Sialoi",
             "Devenpeck v. Alford", "Devenpeck", "Bostock", "Nieves v. Bartlett", "Nieves",
             "Zamani v. Carnes", "Keates v. Koile", "Devereaux v. Abbey",
             "Whittlestone, Inc. v. Handi-Craft Co.", "Smith v. Wade", "Kay v. Ehrler", "Kay",
             "Lopez v. Smith", "Eminence Capital, LLC v. Aspeon, Inc."]
    names.sort(key=len, reverse=True)
    out = t
    for n in names:
        pat = r'(?<![A-Za-z>])' + re.escape(n) + r'(?![A-Za-z<])'
        out = re.sub(pat, lambda m: '<i>' + m.group(0) + '</i>', out)
    out = re.sub(r'<i>(<i>[^<]*</i>)</i>', r'\1', out)
    # nested like <i>Starr</i> inside <i>Starr v. Baca</i>
    out = re.sub(r'<i>([^<]*)<i>([^<]*)</i>([^<]*)</i>', r'<i>\1\2\3</i>', out)
    out = re.sub(r'(?<![A-Za-z])(Id\.|id\.)', r'<i>\1</i>', out)
    out = re.sub(r'(?<![A-Za-z])(See, e\.g\.,|See also|see also|See|see|cf\.|Cf\.)(?=\s)', r'<i>\1</i>', out)
    return out

class Mark(Flowable):
    """Zero-height flowable recording the page where it lands."""
    def __init__(self, key, store):
        Flowable.__init__(self); self.key = key; self.store = store
        self.width = 0; self.height = 0
    def draw(self):
        self.store.setdefault(self.key, self.canv.getPageNumber())

def page_decor(canv, doc, numfmt):
    canv.saveState()
    # line numbers
    canv.setFont('Serif', 12)
    for i in range(LINES):
        y = FRAME_TOP - BASE_OFF - i * LEAD
        canv.drawRightString(0.85 * inch, y, str(i + 1))
    # vertical rules
    canv.setLineWidth(0.75)
    canv.line(1.05 * inch, 0.55 * inch, 1.05 * inch, H - 0.5 * inch)
    canv.line(1.10 * inch, 0.55 * inch, 1.10 * inch, H - 0.5 * inch)
    canv.line(7.65 * inch, 0.55 * inch, 7.65 * inch, H - 0.5 * inch)
    # page number and footer
    pn = numfmt(canv.getPageNumber())
    if pn:
        canv.setFont('Serif', 12)
        canv.drawCentredString((LEFT + RIGHT) / 2, 0.62 * inch, pn)
    canv.setLineWidth(0.75)
    canv.line(LEFT, 0.55 * inch, RIGHT, 0.55 * inch)
    canv.setFont('Serif', 9)
    canv.drawCentredString((LEFT + RIGHT) / 2, 0.40 * inch, SHORT_TITLE)
    canv.drawCentredString((LEFT + RIGHT) / 2, 0.27 * inch, 'Case No. ' + CASE_NO)
    canv.restoreState()

def make_doc(path, numfmt):
    doc = BaseDocTemplate(path, pagesize=letter, leftMargin=LEFT, rightMargin=W - RIGHT,
                          topMargin=H - FRAME_TOP, bottomMargin=FRAME_BOTTOM,
                          title="Plaintiff's Opposition to Motion to Dismiss and Motion to Strike",
                          author='Brendan Ngwa Nforbi')
    frame = Frame(LEFT, FRAME_BOTTOM, TEXT_W, FRAME_H, leftPadding=0, rightPadding=0,
                  topPadding=0, bottomPadding=0, id='f')
    doc.addPageTemplates([PageTemplate(id='pl', frames=[frame],
                                       onPage=lambda c, d: page_decor(c, d, numfmt))])
    return doc

def blank(n=1):
    return Spacer(1, LEAD * n)

def body_story(marks):
    st = []
    first = True
    for kind, txt in BODY:
        t = italicize(txt)
        if kind == 'h1':
            if not first: st.append(blank())
            st.append(Mark(txt, marks)); st.append(Paragraph(t, S_H1))
        elif kind == 'h2':
            st.append(blank()); st.append(Mark(txt, marks)); st.append(Paragraph(t, S_H2))
        elif kind == 'h3':
            st.append(blank()); st.append(Mark(txt, marks)); st.append(Paragraph(t, S_H3))
        elif kind == 'p':
            st.append(Paragraph(t, S_P))
        elif kind == 'np':
            st.append(Paragraph(t, S_NP))
        elif kind == 'bq':
            st.append(Paragraph(t, S_BQ))
        first = False
    st.append(blank())
    sig = [Paragraph(s if s else '&nbsp;', style('sig', alignment=TA_LEFT, leftIndent=3.25 * inch)) for s in SIGNATURE]
    st.append(KeepTogether(sig))
    return st

def caption_story():
    st = []
    for line in ["BRENDAN NGWA NFORBI", "Plaintiff, In Pro Per", "1455 Cat Tail Drive",
                 "Stockton, CA 95204", "Telephone: (209) 801-4442", "E-mail: bnn.cdl@gmail.com"]:
        st.append(Paragraph(line, S_CAP))
    st.append(blank())
    st.append(Paragraph("UNITED STATES DISTRICT COURT", S_CAPB))
    st.append(Paragraph("NORTHERN DISTRICT OF CALIFORNIA", S_CAPB))
    st.append(Paragraph("OAKLAND DIVISION", S_CAPB))
    st.append(blank())
    left = [Paragraph(x, S_CAP) for x in [
        "BRENDAN NGWA NFORBI,", "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Plaintiff,", "&nbsp;&nbsp;&nbsp;&nbsp;v.",
        "SANTIAGO MEZA-GONZALEZ, in his individual capacity; JOSE MELANO, in his individual capacity; and DOES 1 through 10, inclusive,",
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Defendants."]]
    right = [Paragraph(x, S_CAP) for x in [
        "Case No. " + CASE_NO,
        "<b>PLAINTIFF\u2019S OPPOSITION TO DEFENDANTS\u2019 MOTION TO DISMISS PLAINTIFF\u2019S FIRST AMENDED COMPLAINT AND MOTION TO STRIKE PORTIONS OF THE FIRST AMENDED COMPLAINT</b>",
        "Date: December 9, 2026", "Time: 1:30 p.m.", "Courtroom: 4", "Judge: Hon. Ajay S. Krishnan"]]
    lw = TEXT_W * 0.5
    tbl = Table([[left, right]], colWidths=[lw, TEXT_W - lw])
    tbl.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LINEAFTER', (0, 0), (0, 0), 0.75, 'black'),
        ('LINEBELOW', (0, 0), (0, 0), 0.75, 'black'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0), ('RIGHTPADDING', (0, 0), (0, 0), 8),
        ('LEFTPADDING', (1, 0), (1, 0), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 0), ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ]))
    st.append(tbl)
    st.append(blank())
    st.append(Paragraph("Plaintiff Brendan Ngwa Nforbi, in propria persona, submits this Opposition to "
                        "Defendants\u2019 Motion to Dismiss and Motion to Strike (ECF No. 22). For the reasons "
                        "stated in the accompanying Memorandum of Points and Authorities, the motion should be "
                        "denied in its entirety or, in the alternative, leave to amend should be granted.", S_P))
    return st

def dots_row(label, page, indent=0):
    lab = Paragraph(label, style('tl', alignment=TA_LEFT, leftIndent=indent))
    pg = Paragraph(str(page), style('tp', alignment=2))
    return [lab, pg]

def toc_story(marks, auth_pages):
    st = [Paragraph("TABLE OF CONTENTS", S_CAPB), blank()]
    rows = []
    for kind, txt in BODY:
        if kind in ('h1', 'h2', 'h3'):
            ind = {'h1': 0, 'h2': 0.4 * inch, 'h3': 0.8 * inch}[kind]
            rows.append(dots_row(txt, marks.get(txt, '?'), ind))
    tbl = Table(rows, colWidths=[TEXT_W - 0.7 * inch, 0.7 * inch])
    tbl.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP'), ('LEFTPADDING', (0, 0), (-1, -1), 0),
                             ('RIGHTPADDING', (0, 0), (0, -1), 12), ('RIGHTPADDING', (1, 0), (1, -1), 0), ('TOPPADDING', (0, 0), (-1, -1), 0),
                             ('BOTTOMPADDING', (0, 0), (-1, -1), 0)]))
    st.append(tbl)
    st.append(PageBreak())
    st.append(Paragraph("TABLE OF AUTHORITIES", S_CAPB)); st.append(blank())
    for cat, items in AUTHORITIES.items():
        st.append(Paragraph("<b>%s</b>" % cat, S_CAP))
        rows = []
        for disp, keys in items:
            pages = auth_pages.get(disp, [])
            pstr = ', '.join(str(p) for p in pages) if pages else 'passim'
            d = italicize(disp) if cat == 'Cases' else disp
            rows.append(dots_row(d, pstr, 0.3 * inch))
        tbl = Table(rows, colWidths=[TEXT_W - 1.1 * inch, 1.1 * inch])
        tbl.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP'), ('LEFTPADDING', (0, 0), (-1, -1), 0),
                                 ('RIGHTPADDING', (0, 0), (0, -1), 12), ('RIGHTPADDING', (1, 0), (1, -1), 0), ('TOPPADDING', (0, 0), (-1, -1), 0),
                                 ('BOTTOMPADDING', (0, 0), (-1, -1), 0)]))
        st.append(tbl); st.append(blank())
    return st

def page_texts(path):
    r = PdfReader(path)
    return [p.extract_text() or '' for p in r.pages]

def main():
    # pass 1: body
    marks = {}
    doc = make_doc(OUT + 'body.pdf', lambda n: str(n))
    doc.build(body_story(marks))
    texts = page_texts(OUT + 'body.pdf')
    auth_pages = {}
    for cat, items in AUTHORITIES.items():
        for disp, keys in items:
            pages = [i + 1 for i, t in enumerate(texts) if any(k in t for k in keys)]
            auth_pages[disp] = pages
    # front matter: caption page (no number) + TOC/TOA (roman)
    roman = ['', 'i', 'ii', 'iii', 'iv', 'v', 'vi']
    cap = make_doc(OUT + 'cap.pdf', lambda n: '')
    cap.build(caption_story())
    toc = make_doc(OUT + 'toc.pdf', lambda n: roman[n])
    toc.build(toc_story(marks, auth_pages))
    w = PdfWriter()
    for f in ['cap.pdf', 'toc.pdf', 'body.pdf']:
        for p in PdfReader(OUT + f).pages: w.add_page(p)
    w.add_metadata({'/Title': "Plaintiff's Opposition to Motion to Dismiss and Motion to Strike",
                    '/Author': 'Brendan Ngwa Nforbi'})
    final = OUT + 'Nforbi-Opposition-to-MTD-DRAFT.pdf'
    with open(final, 'wb') as fh: w.write(fh)
    print(json.dumps({'body_pages': len(texts), 'marks': marks, 'final': final}, indent=1))

if __name__ == '__main__':
    main()
