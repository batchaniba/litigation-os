"""Narrow, reproducible PDF revision. Source PDFs are never overwritten."""

from pathlib import Path
import hashlib
import json
import re

import pymupdf as fitz
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = ROOT / "00-user-inputs/Newanforbi_26CV191136_Writ_Motion_Packet.pdf"
ORDER = ROOT / "00-user-inputs/Newanforbi-v-Serrato-USDC-NDCal-IFP-Granted-Complaint-Sufficient-Jun-29-2026.pdf"
PACKET = HERE / "Newanforbi_26CV191136_Working_Motion_Packet_Federal_Order_Revision.pdf"
MEMO = HERE / "Matter-20-Writ-Memorandum-Federal-Order-Revision.pdf"
INSERT = HERE / "Federal-Screening-Order-Insertion.pdf"
URL = "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=PEN&sectionNum=679.10."
EXPECTED_BASE = "03d89a03a776b3b723c4937f7d6c9e1d8260c87e8871427a266f47c96968daa0"
EXPECTED_ORDER = "9f00bb4d807287a39687835a503beb4a2754bef01b9bd5b38f0339ba25c7f444"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


assert sha(BASE) == EXPECTED_BASE
assert sha(ORDER) == EXPECTED_ORDER
fonts = Path("/usr/share/fonts/truetype/liberation")
pdfmetrics.registerFont(TTFont("PleadingSerif", str(fonts / "LiberationSerif-Regular.ttf")))
pdfmetrics.registerFont(TTFont("PleadingBold", str(fonts / "LiberationSerif-Bold.ttf")))
pdfmetrics.registerFont(TTFont("PleadingSans", str(fonts / "LiberationSans-Regular.ttf")))

raw = (HERE / "federal-screening-order-insertion.md").read_text()
substantive = raw.split("\n## Publication reference")[0].strip().split("\n\n")
heading = substantive[0].removeprefix("# ").upper()
paragraphs = substantive[1:]


def wrap(text, font, size, width, indent=0):
    words = text.split()
    lines = []
    current = ""
    for word in words:
        candidate = (current + " " + word).strip()
        limit = width - (indent if not lines else 0)
        if current and pdfmetrics.stringWidth(candidate, font, size) > limit:
            lines.append(current)
            current = word
        else:
            current = candidate
    if current:
        lines.append(current)
    for i, line in enumerate(lines):
        limit = width - (indent if i == 0 else 0)
        assert pdfmetrics.stringWidth(line, font, size) <= limit + 0.01, line
    return lines


c = canvas.Canvas(str(INSERT), pagesize=(612, 792))
c.setTitle("Matter 20 Federal Screening-Order Argument")
c.setAuthor("Perplexity Computer")
c.setSubject("Unsigned working revision; limited persuasive screening-stage support")
c.setLineWidth(0.5)
for x in (93.6, 97.2, 576):
    c.line(x, 0, x, 792)
c.line(97.2, 56.4, 576, 56.4)
for n in range(1, 29):
    c.setFont("PleadingSans", 10)
    c.drawRightString(87.84, 720 - 24 * (n - 1), str(n))

line_no = 0
for line in wrap(heading, "PleadingBold", 12, 472):
    c.setFont("PleadingBold", 12)
    c.drawCentredString(340, 720 - 24 * line_no, line)
    line_no += 1
line_no += 1
for para_index, para in enumerate(paragraphs):
    lines = wrap(para, "PleadingSerif", 12, 472, indent=36)
    for i, line in enumerate(lines):
        y = 720 - 24 * line_no
        x = 104 + (36 if i == 0 else 0)
        c.setFont("PleadingSerif", 12)
        c.drawString(x, y, line)
        if para_index == len(paragraphs) - 1 and i == len(lines) - 1:
            c.setFont("PleadingSerif", 8)
            c.drawString(x + pdfmetrics.stringWidth(line, "PleadingSerif", 12) + 1, y + 5, "1")
        line_no += 1
    if para_index < len(paragraphs) - 1:
        line_no += 1
assert line_no <= 24, f"Body would collide with footnote: {line_no} lines"

c.setLineWidth(0.4)
c.line(104, 134, 240, 134)
c.setFont("PleadingSerif", 12)
c.drawString(104, 117, "1. Penal Code § 679.10(g)(1), official text:")
# Break at a URL delimiter without changing the displayed source literal.
url_lines = [URL[:URL.index("?") + 1], URL[URL.index("?") + 1:]]
assert "".join(url_lines) == URL
for i, line in enumerate(url_lines):
    y = 102 - i * 14
    c.drawString(104, y, line)
    c.linkURL(URL, (104, y - 2, 104 + pdfmetrics.stringWidth(line, "PleadingSerif", 12), y + 11), relative=0)
c.setFont("PleadingSans", 10)
c.drawCentredString(334.8, 43, "Page 6")
c.setFont("PleadingSans", 9)
c.drawCentredString(334.8, 25, "MEMORANDUM OF POINTS AND AUTHORITIES - 26CV191136")
c.save()

source = fitz.open(BASE)
addition = fitz.open(INSERT)
result = fitz.open(BASE)
assert len(source) == 30 and len(addition) == 1
# Insert after original PDF p. 8 / memorandum p. 5, before section V.
result.insert_pdf(addition, start_at=8)
for old_index in range(8, 14):
    page = result[old_index + 1]
    page.add_redact_annot(fitz.Rect(303, 738, 369, 757), fill=(1, 1, 1))
    page.apply_redactions()
    label = f"Page {old_index - 1}"
    label_width = fitz.get_text_length(label, fontname="helv", fontsize=10)
    page.insert_text(
        fitz.Point(334.8 - label_width / 2, 751.6),
        label, fontsize=10, fontname="helv",
    )

metadata = dict(result.metadata)
metadata.update({
    "title": "Matter 20 Working Motion Packet: Federal Screening-Order Revision",
    "author": "Perplexity Computer",
    "subject": "Review draft; one memorandum insertion; hearing and filing readiness not verified",
})
result.set_metadata(metadata)
result.save(PACKET, garbage=4, deflate=True)
result.close()
updated = fitz.open(PACKET)
memo = fitz.open()
memo.insert_pdf(updated, from_page=3, to_page=14)
memo.set_metadata({
    "title": "Matter 20 Writ Memorandum with Federal Screening-Order Argument",
    "author": "Perplexity Computer",
    "subject": "Twelve-page unsigned working memorandum extracted from the revised packet",
})
memo.save(MEMO, garbage=4, deflate=True)
memo.close()

def digest_pixels(page, clip=None):
    pix = page.get_pixmap(matrix=fitz.Matrix(1, 1), clip=clip, alpha=False)
    return hashlib.sha256(pix.samples).hexdigest()

preservation = []
for old_index, original in enumerate(source):
    new_index = old_index if old_index < 8 else old_index + 1
    footer_changed = 8 <= old_index < 14
    clip = fitz.Rect(0, 0, 612, 738) if footer_changed else None
    same = digest_pixels(original, clip) == digest_pixels(updated[new_index], clip)
    assert same, f"Unexpected visual change on source page {old_index + 1}"
    preservation.append({
        "source_pdf_page": old_index + 1,
        "revised_pdf_page": new_index + 1,
        "comparison": "entire page" if not footer_changed else "entire page above memorandum footer",
        "pixel_identical": same,
    })
assert len(updated) == 31
for memo_page in range(1, 13):
    text = updated[memo_page + 2].get_text()
    assert re.search(rf"Page\s+{memo_page}(?!\d)", text), f"Missing memo page {memo_page}"

verification = {
    "date": "2026-10-24",
    "baseline_packet": {"path": str(BASE.relative_to(ROOT)), "sha256": sha(BASE), "pages": 30},
    "federal_order": {"path": str(ORDER.relative_to(ROOT)), "sha256": sha(ORDER), "pages": 5},
    "revision": {
        "inserted_at_pdf_page": 9,
        "inserted_at_memorandum_page": 6,
        "packet_pages": 31,
        "memorandum_pages": 12,
        "body_line_count_on_insert": line_no,
        "original_packet_body_preserved": True,
        "original_other_documents_preserved": True,
        "only_original_page_changes": "Memorandum footer page numbers 6–11 renumbered 7–12",
        "federal_order_attached_as_new_exhibit": False,
        "judicial_notice_request_created_or_filed": False,
        "live_federal_docket_checked": False,
        "hearing_or_reservation_confirmed": False,
    },
    "outputs": [
        {"path": str(p.relative_to(ROOT)), "sha256": sha(p), "bytes": p.stat().st_size}
        for p in (PACKET, MEMO, INSERT)
    ],
    "source_page_preservation": preservation,
}
(HERE / "revision-verification.json").write_text(json.dumps(verification, indent=2) + "\n")
print(json.dumps({"packet_pages": len(updated), "memorandum_pages": 12, "body_lines": line_no, "preserved_source_pages": len(preservation)}, indent=2))
