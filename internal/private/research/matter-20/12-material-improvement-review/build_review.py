"""Generate private review drafts without overwriting any source record."""
from pathlib import Path
from collections import OrderedDict
import difflib
import hashlib
import json
import re
import subprocess
import unicodedata

import pymupdf as fitz
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = ROOT / "10-working-motion/Newanforbi_26CV191136_Working_Motion_Packet_Federal_Order_Revision.pdf"
MEMO = HERE / "Revised-Writ-Memorandum.md"
FONTDIR = Path("/usr/share/fonts/truetype/liberation")
for name, filename in (
    ("Legal", "LiberationSerif-Regular.ttf"),
    ("LegalBold", "LiberationSerif-Bold.ttf"),
    ("LegalSans", "LiberationSans-Regular.ttf"),
):
    pdfmetrics.registerFont(TTFont(name, str(FONTDIR / filename)))

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

source_hash = sha(BASE)
source = fitz.open(BASE)
assert len(source) == 31
links = OrderedDict()
labels = {}

def inline(text):
    def replace(m):
        label, url = m.groups()
        if url not in links:
            links[url] = len(links) + 1
            labels[links[url]] = label
        return label + " {{" + str(links[url]) + "}}"
    return re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", replace, text)

def width(word, font="Legal", size=12):
    return pdfmetrics.stringWidth(word, font, size)

def wrap(text, font="Legal", size=12, available=471.6, indent=0):
    """Preserve literal URL characters while allowing a wrap within long URLs."""
    tokens = []
    for word in text.split():
        if width(word, font, size) > available:
            piece = ""
            for char in word:
                if width(piece + char, font, size) > available:
                    tokens.append(piece)
                    piece = char
                else:
                    piece += char
            if piece:
                tokens.append(piece)
        else:
            tokens.append(word)
    lines, current = [], []
    for word in tokens:
        proposed = current + [word]
        displayed = re.sub(r"\{\{(\d+)\}\}", r"\1", " ".join(proposed))
        limit = available - (indent if not lines else 0)
        if current and width(displayed, font, size) > limit:
            lines.append(" ".join(current))
            current = [word]
        else:
            current = proposed
    if current:
        lines.append(" ".join(current))
    return lines

def plain(text):
    return re.sub(r"\{\{\d+\}\}", "", text).replace("  ", " ").strip()

def blocks(path, add_links=True):
    out = []
    for paragraph in re.split(r"\n\n|\n(?=\d+\.\s)", path.read_text().strip()):
        if paragraph.startswith("# "):
            continue
        heading = paragraph.startswith("## ")
        text = paragraph.removeprefix("## ")
        if add_links:
            text = inline(text)
        else:
            text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
        out.append((heading, text))
    return out

memo_blocks = blocks(MEMO)
urls = {number: url for url, number in links.items()}

def notes_lines(numbers):
    out = []
    for number in sorted(numbers):
        for index, line in enumerate(wrap(urls[number], available=444)):
            prefix = f"{number}. " if index == 0 else "    "
            out.append((prefix + line, urls[number]))
    return out

def paginate(items, notes=True):
    pages, page, numbers = [], [], set()
    sections = {}
    def flush():
        nonlocal page, numbers
        if page:
            pages.append((page, set(numbers)))
            page, numbers = [], set()
    for block_index, (heading, text) in enumerate(items):
        font = "LegalBold" if heading else "Legal"
        indent = 0 if heading or re.match(r"^\d+\.\s", text) or text.startswith(("DATED:", "____", "BRENDAN", "Petitioner,", "JUDGE", "CLERK", "By:", "IT IS", "WITNESS")) else 36
        lines = wrap(text, font, indent=indent)
        if heading and len(page) >= 18:
            flush()
        if text.startswith(("DATED:", "WITNESS", "IT IS SO ORDERED")):
            needed = sum(len(wrap(rest, "LegalBold" if is_heading else "Legal")) + 1
                         for is_heading, rest in items[block_index:]) - 1
            if len(page) + needed > 28:
                flush()
        for index, line in enumerate(lines):
            added = set(map(int, re.findall(r"\{\{(\d+)\}\}", line))) if notes else set()
            prospective = numbers | added
            foot_top = 76 + len(notes_lines(prospective)) * 14 if prospective else 50
            y = 720 - len(page) * 24
            if len(lines) - index == 2 and page:
                both = prospective | (set(map(int, re.findall(r"\{\{(\d+)\}\}", lines[index + 1]))) if notes else set())
                both_top = 76 + len(notes_lines(both)) * 14 if both else 50
                if len(page) + 1 >= 28 or y - 24 < max(72, both_top + 28):
                    flush()
                    y = 720
            if len(page) >= 28 or y < max(72, foot_top + 28):
                flush()
            if heading and index == 0:
                sections[text] = len(pages) + 1
            page.append((line, font, indent if index == 0 else 0, heading))
            numbers |= added
        if len(page) < 27:
            page.append(("", "Legal", 0, False))
    flush()
    assert all(len(p[0]) <= 28 for p in pages)
    return pages, sections

body_pages, sections = paginate(memo_blocks)
assert len(body_pages) <= 15, f"Body exceeds general limit: {len(body_pages)}"
authority_pages = {}
for index, (_, numbers) in enumerate(body_pages, 1):
    for number in numbers:
        authority_pages.setdefault(number, []).append(index)
for number, url in urls.items():
    label = labels[number]
    if re.fullmatch(r"\d+", label):
        code = "Evid. Code" if "lawCode=EVID" in url else "Code Civ. Proc."
        labels[number] = f"{code}, § {label}"
    aliases = []
    if "679.10." in url:
        aliases = ["section 679.10", "§ 679.10"]
    elif "96/824" in url:
        aliases = ["California Correctional Supervisors Organization"]
    for index, (lines, _) in enumerate(body_pages, 1):
        page_text = " ".join(plain(line) for line, *_ in lines)
        if any(alias in page_text for alias in aliases):
            authority_pages[number] = sorted(set(authority_pages[number] + [index]))

def frame(c, page_label, title):
    c.setLineWidth(.5)
    for x in (93.6, 97.2, 576):
        c.line(x, 0, x, 792)
    c.line(97.2, 56.4, 576, 56.4)
    for number in range(1, 29):
        c.setFont("LegalSans", 10)
        c.drawRightString(87.84, 720 - (number - 1) * 24, str(number))
    c.setFont("LegalSans", 9)
    c.drawCentredString(335, 42, str(page_label))
    c.setFont("LegalSans", 8)
    c.drawCentredString(335, 27, title[:90])

def metadata(c, title):
    c.setTitle(title)
    c.setAuthor("Perplexity Computer")
    c.setSubject("Unsigned private review draft; not filed or served")

def cover(c, title):
    frame(c, "i", "26CV191136 | REVIEW DRAFT")
    c.setFont("Legal", 12)
    contact = ["BRENDAN NGEHSI NEWANFORBI", "1455 Cat Tail Drive",
               "Stockton, CA 95204", "Telephone: (209) 801-4442",
               "Email: bnn.cdl@gmail.com", "Petitioner, in propria persona"]
    for index, line in enumerate(contact):
        c.drawString(104.4, 728 - index * 14, line)
    c.setFont("LegalBold", 12)
    c.drawCentredString(336, 602, "SUPERIOR COURT OF THE STATE OF CALIFORNIA")
    c.drawCentredString(336, 578, "COUNTY OF ALAMEDA")
    c.setLineWidth(.5)
    c.line(335, 370, 335, 545)
    c.setFont("Legal", 12)
    left = ["BRENDAN NGEHSI", "NEWANFORBI,", "                    Petitioner,", "v.",
            "CALIFORNIA HIGHWAY PATROL;",
            "G. SERRATO, in his official", "capacity as Captain and Commander",
            "of CHP Dublin Area,", "                    Respondents."]
    for index, line in enumerate(left):
        c.drawString(104.4, 530 - 18 * index, line)
    right = ["Case No. 26CV191136", "", "Hon. Jenna M. Whitman, Dept. 25",
             "", "Hearing: January 8, 2027", "9:00 a.m., Department 25",
             "Reservation No. 958052306492", "Action filed May 29, 2026",
             "Trial: Not set"]
    for index, line in enumerate(right):
        c.drawString(344, 530 - 18 * index, line)
    c.setFont("LegalBold", 12)
    for index, line in enumerate(wrap(title.upper(), "LegalBold")):
        c.drawCentredString(336, 300 - index * 24, line)
    c.setFont("Legal", 12)
    caveat = "Review draft. Historical hearing particulars are preserved, not freshly confirmed. Signatures, exhibits, service and current case status require completion."
    for index, line in enumerate(wrap(caveat)):
        c.drawString(104.4, 192 - index * 24, line)
    c.showPage()

def draw_body(c, pages, footer):
    for page_num, (lines, numbers) in enumerate(pages, 1):
        frame(c, page_num, footer)
        c.bookmarkPage("body-" + str(page_num))
        for line_no, (line, font, indent, heading) in enumerate(lines):
            y, x = 720 - line_no * 24, 104.4 + indent
            for piece in re.split(r"(\{\{\d+\}\})", line):
                marker = re.fullmatch(r"\{\{(\d+)\}\}", piece)
                if marker:
                    c.setFont("Legal", 8)
                    c.drawString(x, y + 5, marker[1])
                    x += width(marker[1], "Legal", 8)
                else:
                    c.setFont(font, 12)
                    c.drawString(x, y, piece)
                    x += width(piece, font)
            assert x <= 577, (page_num, line)
        note_lines = notes_lines(numbers)
        if note_lines:
            top = 76 + len(note_lines) * 14
            c.line(104.4, top + 9, 250, top + 9)
            for index, (line, url) in enumerate(note_lines):
                y = top - index * 14
                c.setFont("Legal", 12)
                c.drawString(104.4, y, line)
                c.linkURL(url, (104.4, y - 2, 104.4 + width(line), y + 11))
        c.showPage()

out = HERE / "Matter-20-Revised-Writ-Memorandum.pdf"
c = canvas.Canvas(str(out), pagesize=(612, 792), pageCompression=1, invariant=1)
metadata(c, "Matter 20: Materially Revised Writ Memorandum")
cover(c, "Memorandum of Points and Authorities")
frame(c, "ii", "CONTENTS | 26CV191136 | REVIEW DRAFT")
c.setFont("LegalBold", 12)
c.drawString(104.4, 720, "TABLE OF CONTENTS")
y = 672
for section, page_no in sections.items():
    for index, line in enumerate(wrap(section, available=425)):
        c.setFont("Legal", 12)
        c.drawString(104.4, y, line)
        if index == 0:
            c.drawRightString(568, y, str(page_no))
        c.linkRect("", "body-" + str(page_no), (104.4, y - 2, 572, y + 13))
        y -= 18
    y -= 8
assert y > 75
c.showPage()

toa_index = 0
def toa_new():
    global toa_index
    toa_index += 1
    frame(c, "Authorities " + str(toa_index), "AUTHORITIES | 26CV191136 | REVIEW DRAFT")
    c.setFont("LegalBold", 12)
    c.drawString(104.4, 720, "TABLE OF AUTHORITIES" + (" (continued)" if toa_index > 1 else ""))
    return 685

y = toa_new()
for number, url in sorted(urls.items()):
    label = labels[number] + " [body pp. " + ", ".join(map(str, authority_pages[number])) + "]"
    lines = [(line, True) for line in wrap(label, "LegalBold")]
    lines += [(line, False) for line in wrap(url)]
    needed = len(lines) * 14 + 10
    if y - needed < 78:
        c.showPage()
        y = toa_new()
    for line, is_label in lines:
        c.setFont("LegalBold" if is_label else "Legal", 12)
        c.drawString(104.4, y, line)
        if not is_label:
            c.linkURL(url, (104.4, y - 2, 104.4 + width(line), y + 11))
        y -= 14
    y -= 10
court_records = [
    ("Order Sustaining Demurrer in Part (Aug. 29, 2026), No. 26CV191136", ["August 29 order", "Aug. 29 Order", "Aug. 29, 2026"]),
    ("Newanforbi v. Serrato (N.D.Cal. June 29, 2026), No. 4:26-cv-05953-ASK, ECF 5", ["related federal order", "4:26-cv-05953-ASK"]),
]
if y < 215:
    c.showPage()
    y = toa_new()
c.setFont("LegalBold", 12)
c.drawString(104.4, y, "COURT RECORDS")
y -= 22
for label, aliases in court_records:
    found = [index for index, (lines, _) in enumerate(body_pages, 1)
             if any(alias in " ".join(plain(line) for line, *_ in lines) for alias in aliases)]
    for line in wrap(label + " [body pp. " + ", ".join(map(str, found)) + "]"):
        c.setFont("Legal", 12)
        c.drawString(104.4, y, line)
        y -= 14
    y -= 10
c.showPage()
draw_body(c, body_pages, "MEMORANDUM | 26CV191136 | REVIEW DRAFT")
c.save()

order_outputs = []
for path in sorted(HERE.glob("Proposed-*.md")):
    title = path.read_text().splitlines()[0].removeprefix("# ")
    pages, _ = paginate(blocks(path, add_links=False), notes=False)
    dest = path.with_suffix(".pdf")
    c = canvas.Canvas(str(dest), pagesize=(612, 792), pageCompression=1, invariant=1)
    metadata(c, "Matter 20: " + title)
    cover(c, title)
    draw_body(c, pages, "PROPOSED ONLY | 26CV191136 | REVIEW DRAFT")
    c.save()
    order_outputs.append(dest)

# Preserve original notice/declaration/service pages; correct title only, not testimony.
selected = list(range(3)) + list(range(15, 19)) + list(range(28, 31))
compilation = fitz.open()
changed = []
for index in selected:
    page_doc = fitz.open()
    page_doc.insert_pdf(source, from_page=index, to_page=index)
    page = page_doc[0]
    for block in page.get_text("dict")["blocks"]:
        if "lines" not in block:
            continue
        for line in block["lines"]:
            old = "".join(s["text"] for s in line["spans"])
            new = re.sub(r"\b[Vv]erified Answer\b", "Answer", old)
            if new == old:
                continue
            rect = fitz.Rect(line["bbox"])
            origin = line["spans"][0]["origin"]
            page.add_redact_annot(rect, fill=(1, 1, 1))
            page.apply_redactions()
            page.insert_font(fontname="LegalCorrection", fontfile=str(FONTDIR / "LiberationSerif-Regular.ttf"))
            page.insert_text(origin, new, fontname="LegalCorrection", fontsize=12)
            changed.append({"source_page": index + 1, "before": old, "after": new,
                            "bbox": list(rect), "purpose": "neutral document-title correction"})
    if index < 3:
        compilation.insert_pdf(page_doc)
        if index == 2:
            compilation.insert_pdf(fitz.open(out))
    else:
        compilation.insert_pdf(page_doc)
assert len(changed) == 3, changed
packet = HERE / "Matter-20-Revised-Moving-Papers-Review-Compilation.pdf"
compilation.set_metadata({"title": "Matter 20: Revised Moving Papers, Private Review Compilation",
                          "author": "Perplexity Computer",
                          "subject": "Unsigned review compilation; exhibits and execution incomplete; not e-filing instructions"})
compilation.save(packet, garbage=4, deflate=True, no_new_id=True)

# Quote audit and actual mechanical comparison; do not invent baseline quotations.
baseline_text = subprocess.run(["pdftotext", "-f", "4", "-l", "15", "-layout", str(BASE), "-"],
                               check=True, capture_output=True, text=True).stdout
clean_lines = []
for line in baseline_text.splitlines():
    line = re.sub(r"^\s*\d{1,2}\s+", "", line).strip()
    if re.fullmatch(r"Page \d+", line) or "MEMORANDUM OF POINTS AND AUTHORITIES - 26CV191136" in line:
        continue
    clean_lines.append(line)
clean_baseline = "\n".join(clean_lines)
def norm(text):
    text = unicodedata.normalize("NFKC", text)
    text = text.translate(str.maketrans({"’": "'", "‘": "'", "“": '"', "”": '"'}))
    return re.sub(r"\s+", "", text)

before_quotes = [
    "The record identifies a stationary vehicle on a freeway shoulder; it does not, simply by those words, establish roadway obstruction or another statutory exception.",
    "If the original recording corroborates the exchange, the report materially misattributes the reason for nonperformance and cannot fairly count that nonperformance as Petitioner's failure.",
    "The holding concerned evidentiary use at trial and did not itself decide every possible prearrest reasonable-cause application.",
    "No finding of legal error is sought merely because the denial letter is brief or an internal memorandum bears a later date.",
]
for quotation in before_quotes:
    assert norm(quotation) in norm(clean_baseline), quotation
new_text = "\n\n".join(plain(text) for _, text in memo_blocks)
diff = difflib.unified_diff(clean_baseline.splitlines(), new_text.splitlines(),
                            fromfile="Working memorandum: physical PDF pages 4-15",
                            tofile="Revised memorandum: clean text without web-footnote numbers",
                            lineterm="")
(HERE / "Memorandum-Text-Comparison.diff").write_text(
    "# Mechanical text comparison. PDF extraction retains line wraps; this is not tracked Word markup.\n"
    + "\n".join(diff) + "\n")

assert sha(BASE) == source_hash
outputs = [out, packet] + order_outputs
verification = {
    "review_date": "2026-10-24",
    "baseline_sha256": source_hash,
    "baseline_preserved": True,
    "memo_body_pages": len(body_pages),
    "memo_frontmatter_pages": 2 + toa_index,
    "memo_total_pages": len(fitz.open(out)),
    "public_authority_count": len(urls),
    "source_notice_declaration_service_pages": [n + 1 for n in selected],
    "neutral_title_corrections": changed,
    "before_quotes_checked_against_actual_baseline": before_quotes,
    "new_memo_section_pages": sections,
    "outputs": {p.name: {"sha256": sha(p), "pages": len(fitz.open(p))} for p in outputs},
    "not_completed": ["native MP4 review", "live state/federal docket confirmation",
                      "original reservation receipt recovery", "exhibit A-E assembly/authentication",
                      "signatures and service", "subscription citator and final historical-version check"],
}
(HERE / "generation-verification.json").write_text(json.dumps(verification, indent=2) + "\n")
print(json.dumps(verification, indent=2))
