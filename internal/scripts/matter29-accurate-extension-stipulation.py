#!/usr/bin/env python3
"""Matter 29 — Plaintiff-executed counterpart of the Accurate response
extension, plus a letter telling Seyfarth they may not affix his signature.

John Drury (Seyfarth) emailed the draft on September 1, 2026, already
carrying a conformed "/s/ Brendan Ngehis Newanforbi" and asked for consent
to file. Plaintiff already agreed by email on August 31 to September 22
as to Accurate Background LLC only. He signs his own paper. He does not
authorize counsel to apply a conformed /s/.

  python3 internal/scripts/matter29-accurate-extension-stipulation.py
"""
from __future__ import annotations

import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
sys.path.insert(0, str(SCRIPT_DIR / "lib"))

from pleading_paper import CONTENT_LEFT, PleadingPaper  # noqa: E402
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer
from short_link import publish_short_link  # noqa: E402
from signature_stamp import (  # noqa: E402
    SIGNATURE_ASPECT,
    SIGNATURE_NATIVE_PX,
    SIGNATURE_PATH,
)

ROOT = SCRIPT_DIR.parent
MATTER29 = ROOT / "public/documents/matter-29"

EXEC_DATE = "September 1, 2026"
CASE_NO = "3:26-cv-09249-ASK"
FOOTER = (
    "STIPULATION TO EXTEND TIME -- NEWANFORBI v. AMAZON.COM SERVICES, LLC"
)

OUT_STIP = MATTER29 / (
    "Stipulation to Extend Time for Accurate Background to Respond "
    "(Plaintiff Counterpart, Sep 1 2026).pdf"
)
OUT_STIP_DOCX = MATTER29 / (
    "Stipulation to Extend Time for Accurate Background to Respond "
    "(Plaintiff Counterpart, Sep 1 2026).docx"
)
OUT_LETTER = MATTER29 / (
    "Letter - Seyfarth May Not Affix Plaintiff's Signature "
    "(Accurate Stipulation) (Sep 1 2026).pdf"
)
OUT_LETTER_DOCX = MATTER29 / (
    "Letter - Seyfarth May Not Affix Plaintiff's Signature "
    "(Accurate Stipulation) (Sep 1 2026).docx"
)
OUT_EMAIL = MATTER29 / "EMAIL_DRAFT_Accurate_Stip_Signature_Notice.txt"

STIP_SLUG = "accurate-stip"
LETTER_SLUG = "accurate-sig-notice"

ATTY = [
    ("BRENDAN NGEHSI NEWANFORBI", "Times-Bold", 12),
    ("Plaintiff, In Pro Per", "Times-Roman", 12),
    ("1455 Cat Tail Drive", "Times-Roman", 12),
    ("Stockton, CA 95204", "Times-Roman", 12),
    ("Telephone: (209) 801-4442", "Times-Roman", 12),
    ("E-mail: bnn.cdl@gmail.com", "Times-Roman", 12),
]

SIG_LINE = "___________________________________"

LETTER_PARAS = [
    (
        "I am the plaintiff, in pro per, in Newanforbi v. Amazon.com Services, "
        "LLC, et al., N.D. Cal. No. 3:26-cv-09249-ASK. This letter follows "
        "Mr. Drury’s September 1, 2026 e-mail attaching a draft stipulation "
        "and asking for my consent to file."
    ),
    (
        "The extension is acceptable: Accurate Background LLC only, through "
        "and including September 22, 2026. It does not extend Amazon.com "
        "Services, LLC."
    ),
    (
        "I do not authorize you, Seyfarth Shaw LLP, Accurate Background LLC, "
        "or anyone acting for them to apply, reproduce, affix, or file my "
        "signature — including a conformed “/s/” — on this paper or on any "
        "other paper. I respectfully ask that you not request that again."
    ),
    (
        "The draft you circulated already carried a conformed "
        "“/s/ Brendan Ngehis Newanforbi.” My middle name is Ngehsi. I had "
        "not signed that paper. I have signed the enclosed counterpart "
        "myself. Please file that counterpart. Leave my signature block "
        "blank on any version you prepare. Electronic service remains "
        "bnn.cdl@gmail.com. Please confirm by reply when the counterpart "
        "is on file."
    ),
]


def _header(d: PleadingPaper) -> None:
    c = d.c
    atty_y = d._line_y(0)
    for i, (txt, fn, sz) in enumerate(ATTY):
        c.setFont(fn, sz)
        c.drawString(CONTENT_LEFT, atty_y - i * 14, txt)
    d.current_line = 4
    d.blank_line()
    d.write_line("UNITED STATES DISTRICT COURT", bold=True, center=True)
    d.write_line("NORTHERN DISTRICT OF CALIFORNIA", bold=True, center=True)
    d.blank_line()


def _plaintiff_sign_block(d: PleadingPaper) -> None:
    d.ensure_space(8)
    d.write_line(f"Dated: {EXEC_DATE}")
    d.blank_line()
    d.blank_line()
    d.blank_line()
    d.draw_signature_image(
        SIGNATURE_PATH,
        SIGNATURE_NATIVE_PX[0],
        SIGNATURE_NATIVE_PX[1],
        SIG_LINE,
        width=220,
        x_offset=15,
    )
    d.write_line(SIG_LINE, right=True, right_margin_offset=20)
    d.write_line(
        "BRENDAN NGEHSI NEWANFORBI",
        bold=True,
        right=True,
        right_margin_offset=20,
    )
    d.write_line("Plaintiff, In Pro Per", right=True, right_margin_offset=20)


def build_stipulation(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    d = PleadingPaper(str(path), doc_title_footer=FOOTER)
    _header(d)
    left = [
        ("BRENDAN NGEHSI NEWANFORBI,", True, False),
        ("", False, False),
        ("                          Plaintiff,", False, False),
        ("", False, False),
        ("       v.", False, False),
        ("", False, False),
        ("AMAZON.COM SERVICES, LLC;", True, False),
        ("ACCURATE BACKGROUND LLC; and", True, False),
        ("DOES 1–10, inclusive,", True, False),
        ("", False, False),
        ("                          Defendants.", False, False),
    ]
    right = [
        (f"Case No. {CASE_NO}", False, False),
        ("", False, False),
        ("STIPULATION TO EXTEND TIME", True, False),
        ("FOR ACCURATE BACKGROUND LLC", True, False),
        ("TO RESPOND TO THE COMPLAINT", True, False),
        ("[Civil L.R. 6-1(a);", True, False),
        ("Fed. R. Civ. P. 6(b)(1)(A), 81(c)]", True, False),
        ("", False, False),
        ("Judge: Hon. Ajay S. Krishnan", False, False),
    ]
    d.draw_caption_block(left, right, caption_size=10, tight_lh=13, boxed=True)
    d.blank_line()
    d.write_line("STIPULATION TO EXTEND TIME", bold=True, center=True)
    d.write_line("(Accurate Background LLC Only)", bold=True, center=True)
    d.blank_line()
    d.write_wrapped(
        "Plaintiff Brendan Ngehsi Newanforbi, appearing in propria persona, and "
        "Defendant Accurate Background LLC, through its counsel of record, "
        "stipulate as follows:",
        first_indent=0,
    )
    d.blank_line()
    d.write_wrapped(
        "1. Amazon.com Services, LLC removed this action on August 31, 2026. "
        "Under Fed. R. Civ. P. 81(c)(2), Accurate Background LLC’s time to "
        "answer or otherwise respond to the Complaint is September 8, 2026.",
        first_indent=0,
    )
    d.blank_line()
    d.write_wrapped(
        "2. The parties agree to extend that deadline, as to Accurate "
        "Background LLC only, through and including September 22, 2026.",
        first_indent=0,
    )
    d.blank_line()
    d.write_wrapped(
        "3. This extension does not apply to Defendant Amazon.com Services, "
        "LLC or to any other party. Amazon.com Services, LLC’s deadline is "
        "unchanged by this stipulation.",
        first_indent=0,
    )
    d.blank_line()
    d.write_wrapped(
        "4. This is a single extension. It does not alter any date set by "
        "Court order. No further extension is implied. It does not waive any "
        "defense, objection, or right of any party, including Plaintiff’s "
        "right to seek default if no timely response is filed.",
        first_indent=0,
    )
    d.blank_line()
    d.write_wrapped(
        "5. This stipulation is made under Civil L.R. 6-1(a) and shall be "
        "promptly filed pursuant to Civil L.R. 5. No Court order is required.",
        first_indent=0,
    )
    d.blank_line()
    d.write_line("IT IS SO STIPULATED.", bold=True, center=True)
    d.blank_line()
    _plaintiff_sign_block(d)
    d.blank_line()
    d.ensure_space(7)
    d.write_line("Dated: ________________")
    d.blank_line()
    d.write_line(SIG_LINE, right=True, right_margin_offset=20)
    d.write_line(
        "JASMINE J. STANZICK (SBN 354704)",
        bold=True,
        right=True,
        right_margin_offset=20,
    )
    d.write_line("Seyfarth Shaw LLP", right=True, right_margin_offset=20)
    d.write_line("Attorneys for Defendant", right=True, right_margin_offset=20)
    d.write_line("Accurate Background LLC", right=True, right_margin_offset=20)
    d.save()


def _docx_helpers():
    try:
        from docx import Document
        from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
        from docx.oxml.ns import qn
        from docx.shared import Inches, Pt
    except ImportError:
        import os

        os.system(f"{sys.executable} -m pip install -q python-docx")
        from docx import Document
        from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
        from docx.oxml.ns import qn
        from docx.shared import Inches, Pt

    font_name = "Times New Roman"
    size = Pt(12)

    def set_run(run, *, bold=False, italic=False, run_size=size):
        run.font.name = font_name
        run._element.rPr.rFonts.set(qn("w:eastAsia"), font_name)
        run.font.size = run_size
        run.bold = bold
        run.italic = italic

    def add_para(
        document,
        text="",
        *,
        bold=False,
        center=False,
        right=False,
        justify=False,
        double=False,
        run_size=size,
        space_after=0,
    ):
        p = document.add_paragraph()
        pf = p.paragraph_format
        pf.space_before = Pt(0)
        pf.space_after = Pt(space_after)
        if double:
            pf.line_spacing_rule = WD_LINE_SPACING.DOUBLE
        else:
            pf.line_spacing = 1.0
            pf.line_spacing_rule = WD_LINE_SPACING.SINGLE
        if center:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        elif right:
            p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        elif justify:
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        if text:
            run = p.add_run(text)
            set_run(run, bold=bold, run_size=run_size)
        return p

    return Document, WD_ALIGN_PARAGRAPH, Inches, Pt, set_run, add_para


def build_stip_docx(path: Path) -> None:
    Document, WD_ALIGN_PARAGRAPH, Inches, Pt, set_run, add_para = (
        _docx_helpers()
    )
    sig_width = Inches(220 / 72)
    sig_height = Inches((220 / 72) * SIGNATURE_ASPECT)

    path.parent.mkdir(parents=True, exist_ok=True)
    doc = Document()
    section = doc.sections[0]
    section.page_width = Inches(8.5)
    section.page_height = Inches(11)
    section.left_margin = Inches(1.0)
    section.right_margin = Inches(1.0)
    section.top_margin = Inches(1.0)
    section.bottom_margin = Inches(1.0)
    footer = section.footer
    footer.is_linked_to_previous = False
    fp = footer.paragraphs[0]
    fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = fp.add_run(
        f"Case No. {CASE_NO}  —  STIPULATION TO EXTEND TIME (Accurate only)"
    )
    set_run(run, run_size=Pt(9))

    for line, fn, _sz in ATTY:
        add_para(doc, line, bold=("Bold" in fn))
    add_para(doc, "")
    add_para(doc, "UNITED STATES DISTRICT COURT", bold=True, center=True)
    add_para(doc, "NORTHERN DISTRICT OF CALIFORNIA", bold=True, center=True)
    add_para(doc, "")

    table = doc.add_table(rows=1, cols=2)
    left, right = table.rows[0].cells
    left_lines = [
        ("BRENDAN NGEHSI NEWANFORBI,", True),
        ("          Plaintiff,", False),
        ("", False),
        ("     v.", False),
        ("", False),
        ("AMAZON.COM SERVICES, LLC;", True),
        ("ACCURATE BACKGROUND LLC; and", True),
        ("DOES 1–10, inclusive,", True),
        ("          Defendants.", False),
    ]
    right_lines = [
        (f"Case No. {CASE_NO}", False),
        ("", False),
        ("STIPULATION TO EXTEND TIME", True),
        ("FOR ACCURATE BACKGROUND LLC", True),
        ("TO RESPOND TO THE COMPLAINT", True),
        ("[Civil L.R. 6-1(a);", True),
        ("Fed. R. Civ. P. 6(b)(1)(A), 81(c)]", True),
        ("", False),
        ("Judge: Hon. Ajay S. Krishnan", False),
    ]
    for cell, lines in ((left, left_lines), (right, right_lines)):
        cell.text = ""
        for i, (text, bold) in enumerate(lines):
            p = cell.paragraphs[0] if i == 0 else cell.add_paragraph()
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.0
            run = p.add_run(text)
            set_run(run, bold=bold, run_size=Pt(11))

    add_para(doc, "")
    add_para(doc, "STIPULATION TO EXTEND TIME", bold=True, center=True)
    add_para(doc, "(Accurate Background LLC Only)", bold=True, center=True)
    add_para(doc, "")
    add_para(
        doc,
        "Plaintiff Brendan Ngehsi Newanforbi, appearing in propria persona, and "
        "Defendant Accurate Background LLC, through its counsel of record, "
        "stipulate as follows:",
        double=True,
    )
    for text in (
        "1. Amazon.com Services, LLC removed this action on August 31, 2026. "
        "Under Fed. R. Civ. P. 81(c)(2), Accurate Background LLC’s time to "
        "answer or otherwise respond to the Complaint is September 8, 2026.",
        "2. The parties agree to extend that deadline, as to Accurate "
        "Background LLC only, through and including September 22, 2026.",
        "3. This extension does not apply to Defendant Amazon.com Services, "
        "LLC or to any other party. Amazon.com Services, LLC’s deadline is "
        "unchanged by this stipulation.",
        "4. This is a single extension. It does not alter any date set by "
        "Court order. No further extension is implied. It does not waive any "
        "defense, objection, or right of any party, including Plaintiff’s "
        "right to seek default if no timely response is filed.",
        "5. This stipulation is made under Civil L.R. 6-1(a) and shall be "
        "promptly filed pursuant to Civil L.R. 5. No Court order is required.",
    ):
        add_para(doc, text, double=True)
    add_para(doc, "")
    add_para(doc, "IT IS SO STIPULATED.", bold=True, center=True)
    add_para(doc, "")
    add_para(doc, f"Dated: {EXEC_DATE}")
    add_para(doc, "")
    add_para(doc, "")
    sig_p = add_para(doc, "", right=True)
    run = sig_p.add_run()
    run.add_picture(SIGNATURE_PATH, width=sig_width, height=sig_height)
    add_para(doc, SIG_LINE, right=True)
    add_para(doc, "BRENDAN NGEHSI NEWANFORBI", bold=True, right=True)
    add_para(doc, "Plaintiff, In Pro Per", right=True)
    add_para(doc, "")
    add_para(doc, "Dated: ________________")
    add_para(doc, "")
    add_para(doc, SIG_LINE, right=True)
    add_para(doc, "JASMINE J. STANZICK (SBN 354704)", bold=True, right=True)
    add_para(doc, "Seyfarth Shaw LLP", right=True)
    add_para(doc, "Attorneys for Defendant", right=True)
    add_para(doc, "Accurate Background LLC", right=True)
    doc.save(str(path))


def build_letter_pdf(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    body = ParagraphStyle(
        "body",
        fontName="Times-Roman",
        fontSize=12,
        leading=16.5,
        alignment=TA_JUSTIFY,
        spaceAfter=8,
    )
    plain = ParagraphStyle(
        "plain",
        fontName="Times-Roman",
        fontSize=12,
        leading=16.5,
        alignment=TA_LEFT,
    )
    bold = ParagraphStyle(
        "bold",
        fontName="Times-Bold",
        fontSize=12,
        leading=16.5,
        alignment=TA_LEFT,
    )
    story = [
        Paragraph("BRENDAN NGEHSI NEWANFORBI", bold),
        Paragraph("1455 Cat Tail Drive", plain),
        Paragraph("Stockton, CA 95204", plain),
        Paragraph("Telephone: (209) 801-4442", plain),
        Paragraph("E-mail: bnn.cdl@gmail.com", plain),
        Paragraph("Plaintiff In Pro Per", plain),
        Spacer(1, 14),
        Paragraph(EXEC_DATE, plain),
        Spacer(1, 10),
        Paragraph("Jasmine J. Stanzick, Esq.", plain),
        Paragraph("John Drury, Esq.", plain),
        Paragraph("Seyfarth Shaw LLP", plain),
        Paragraph("2029 Century Park East, Suite 3500", plain),
        Paragraph("Los Angeles, CA 90067-3021", plain),
        Paragraph("jstanzick@seyfarth.com", plain),
        Paragraph("JDrury@seyfarth.com", plain),
        Spacer(1, 8),
        Paragraph(
            "Re:&nbsp;&nbsp;<b>Newanforbi v. Amazon.com Services, LLC, et al.</b>"
            f" — N.D. Cal. No. {CASE_NO}<br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Accurate Background LLC — "
            "signed counterpart and notice that you may not affix my signature",
            body,
        ),
        Paragraph("Ms. Stanzick and Mr. Drury:", plain),
        Spacer(1, 6),
    ]
    for para in LETTER_PARAS:
        story.append(Paragraph(para, body))
    story.append(Paragraph("Respectfully,", plain))
    story.append(Spacer(1, 4))
    sig_w = 1.9 * inch
    sig_h = sig_w * SIGNATURE_ASPECT
    story.append(Image(SIGNATURE_PATH, width=sig_w, height=sig_h))
    story.append(Paragraph("Brendan Ngehsi Newanforbi", bold))
    story.append(Paragraph("Plaintiff, In Pro Per", plain))
    doc = SimpleDocTemplate(
        str(path),
        pagesize=letter,
        leftMargin=1.0 * inch,
        rightMargin=1.0 * inch,
        topMargin=0.7 * inch,
        bottomMargin=0.65 * inch,
        title=(
            "Letter — Seyfarth may not affix Plaintiff’s signature "
            f"({CASE_NO})"
        ),
        author="Brendan Ngehsi Newanforbi",
    )
    doc.build(story)


def build_letter_docx(path: Path) -> None:
    Document, _align, Inches, Pt, _set_run, add_para = _docx_helpers()
    sig_width = Inches(2.4)
    sig_height = Inches(2.4 * SIGNATURE_ASPECT)

    path.parent.mkdir(parents=True, exist_ok=True)
    doc = Document()
    section = doc.sections[0]
    section.page_width = Inches(8.5)
    section.page_height = Inches(11)
    section.left_margin = Inches(1.0)
    section.right_margin = Inches(1.0)
    section.top_margin = Inches(0.85)
    section.bottom_margin = Inches(0.85)

    for line, fn, _sz in ATTY:
        add_para(doc, line, bold=("Bold" in fn))
    add_para(doc, "")
    add_para(doc, EXEC_DATE)
    add_para(doc, "")
    add_para(doc, "Jasmine J. Stanzick, Esq.")
    add_para(doc, "John Drury, Esq.")
    add_para(doc, "Seyfarth Shaw LLP")
    add_para(doc, "2029 Century Park East, Suite 3500")
    add_para(doc, "Los Angeles, CA 90067-3021")
    add_para(doc, "jstanzick@seyfarth.com")
    add_para(doc, "JDrury@seyfarth.com")
    add_para(doc, "")
    add_para(
        doc,
        f"Re:  Newanforbi v. Amazon.com Services, LLC, et al. — "
        f"N.D. Cal. No. {CASE_NO}",
        bold=True,
    )
    add_para(
        doc,
        "Accurate Background LLC — signed counterpart and notice that you "
        "may not affix my signature",
        bold=True,
    )
    add_para(doc, "")
    add_para(doc, "Ms. Stanzick and Mr. Drury:")
    add_para(doc, "")
    for para in LETTER_PARAS:
        add_para(doc, para, justify=True, space_after=12)
    add_para(doc, "Respectfully,")
    add_para(doc, "")
    sig_p = add_para(doc, "")
    run = sig_p.add_run()
    run.add_picture(SIGNATURE_PATH, width=sig_width, height=sig_height)
    add_para(doc, "Brendan Ngehsi Newanforbi", bold=True)
    add_para(doc, "Plaintiff, In Pro Per")
    add_para(doc, "")
    add_para(doc, "Enclosures: signed counterpart (PDF and Word).")
    doc.save(str(path))


def build_email(path: Path) -> None:
    path.write_text(
        "To: JDrury@seyfarth.com; jstanzick@seyfarth.com\n"
        "Subject: Re: Newanforbi v. Amazon.com Services, LLC, et al. "
        "(Alameda No. 26CV201554) — Accurate Background: 14-Day Extension "
        "Offer and Settlement Demand\n"
        "\n"
        "Ms. Stanzick and Mr. Drury:\n"
        "\n"
        "Thank you for sending the draft.\n"
        "\n"
        "The extension is acceptable: Accurate Background LLC only, through "
        "and including September 22, 2026. It does not extend Amazon.com "
        "Services, LLC.\n"
        "\n"
        "I do not authorize you or anyone at your firm to apply, reproduce, "
        "affix, or file my signature. I respectfully ask that you not "
        "request that again.\n"
        "\n"
        "Your draft already carried a conformed /s/ with my middle name "
        "misspelled. I had not signed it. I have signed the enclosed "
        "counterpart myself (PDF and Word), and I am enclosing a letter "
        "on the same point. Please file the PDF, or use the Word file if "
        "your e-filing workflow requires it. Leave my signature block blank "
        "on any version you prepare.\n"
        "\n"
        "Electronic service remains bnn.cdl@gmail.com.\n"
        "\n"
        "Please confirm by reply when it is on file.\n"
        "\n"
        "Regards,\n"
        "Brendan Ngehsi Newanforbi\n"
        "(209) 801-4442\n"
        "bnn.cdl@gmail.com\n"
        "\n"
        "Attachments:\n"
        "  Letter - Seyfarth May Not Affix Plaintiff's Signature "
        "(Accurate Stipulation) (Sep 1 2026).pdf\n"
        "  Letter - Seyfarth May Not Affix Plaintiff's Signature "
        "(Accurate Stipulation) (Sep 1 2026).docx\n"
        "  Stipulation to Extend Time for Accurate Background to Respond "
        "(Plaintiff Counterpart, Sep 1 2026).pdf\n"
        "  Stipulation to Extend Time for Accurate Background to Respond "
        "(Plaintiff Counterpart, Sep 1 2026).docx\n"
        "\n"
        "---\n"
        "Note to self (do not send): Do not put a GitHub raw link in this "
        "email.\n"
        "Do not mention the 5-1 attestation page.\n"
        "Do not date this as sent until it goes out.\n"
        "After Seyfarth files, pull the PACER stamp and retire the unfiled "
        "counterpart. Sep. 8 remains the live Accurate clock until then.\n",
        encoding="utf-8",
    )


def main() -> None:
    if not Path(SIGNATURE_PATH).is_file():
        raise SystemExit(f"Missing signature image: {SIGNATURE_PATH}")
    build_stipulation(OUT_STIP)
    print(f"Wrote {OUT_STIP}")
    build_stip_docx(OUT_STIP_DOCX)
    print(f"Wrote {OUT_STIP_DOCX}")
    build_letter_pdf(OUT_LETTER)
    print(f"Wrote {OUT_LETTER}")
    build_letter_docx(OUT_LETTER_DOCX)
    print(f"Wrote {OUT_LETTER_DOCX}")
    build_email(OUT_EMAIL)
    print(f"Wrote {OUT_EMAIL}")
    publish_short_link(OUT_STIP, STIP_SLUG)
    publish_short_link(OUT_LETTER, LETTER_SLUG)
    print(f"Published /{STIP_SLUG} and /{LETTER_SLUG}")


if __name__ == "__main__":
    main()
