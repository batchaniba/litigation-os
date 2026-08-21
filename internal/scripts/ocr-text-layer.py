"""Add an invisible OCR text layer to scanned PDFs, in place.

The document and citation indexes read every PDF under internal/public/documents/
with PyMuPDF and search whatever text layer they find. A scanned exhibit has
none, so it contributes zero citations -- which build-citation-index.py records
as `no_text_layer` precisely because that is not the same as "cites nothing".
Those documents are invisible to the citation ledger until someone OCRs them.

This writes the recognised words back into the page as invisible text
(PDF render mode 3) positioned over the words in the scan. The original page
content is untouched: the scan still renders exactly as it did, and a reader
sees no difference. Only extraction and search change.

The pdf-audit tier scripts also OCR, but into .cache/pdf-audit/ for their own
cross-checking, and only the first few pages. That cache is not wired to the
indexes. This is the complementary half: it makes the PDF itself searchable.

    python3 internal/scripts/ocr-text-layer.py <path> [<path> ...]
    python3 internal/scripts/ocr-text-layer.py --all --dry-run

After running, rebuild the indexes so the new text is picked up:

    npm run index:build && npm run citations:index
"""

import argparse
import os
import statistics
import sys
import unicodedata

import pymupdf
import pypdfium2 as pdfium
import pytesseract
from pytesseract import Output

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DOCS_ROOT = os.path.join(REPO_ROOT, "internal", "public", "documents")

# build-citation-index.py calls a PDF `no_text_layer` at 50 characters or
# fewer; matching that keeps "needs OCR" here and "was not searched" there as
# the same set of documents.
MIN_CHARS = 50

# 72 dpi is PDF user space, so this is the pixel-per-point factor. Tesseract
# wants roughly 300 dpi for body text; below that its word boxes drift.
RENDER_DPI = 300

# Tesseract scores some correctly-read tokens at zero -- heavily punctuated
# ones especially, so `1101(a)(15)(U)` and `(iii).` in a statutory cite both
# come back at 0 alongside their high-scoring neighbours. Discarding those
# would quietly drop exactly the citations this exists to index, so nothing is
# rejected on its own score; the line-level checks below do the filtering.
MIN_CONFIDENCE = 0

# A word read sideways is taller than it is wide. Real body words run about
# 1.5:1 and up, the rotated court name down the margin of a pleading caption
# about 0.3:1, so anything under this is the caption sidebar rather than text.
VERTICAL_ASPECT = 0.6

# Points of baseline drift treated as the same row when ordering. Wide enough
# to absorb the skew of a scan, narrower than the leading of double-spaced
# pleading text, so the two halves of a caption stay on one row.
BASELINE_BUCKET = 3.0

# Applied to a whole recognised line. Body text on these scans comes back in
# the high 70s and above; speckle, staple shadows and the rotated sidebar of a
# pleading caption come back well below. Dropping those is not only about
# cleanliness -- a noise line sitting between two body lines splits the page
# into separate blocks, and MuPDF then emits the text out of reading order.
MIN_LINE_CONFIDENCE = 70

# Base-14, so nothing is embedded. The text never renders, and the glyph
# widths only need to be close enough that words land in reading order.
FONTNAME = "helv"

_TYPOGRAPHIC = {
    "\u2018": "'", "\u2019": "'", "\u201a": ",", "\u201c": '"', "\u201d": '"',
    "\u2013": "-", "\u2014": "-", "\u2212": "-", "\u2026": "...", "\u00a0": " ",
}


def to_latin1(word):
    """Fold OCR output down to what the base-14 fonts can encode.

    Tesseract emits curly quotes and dashes that Helvetica's Latin-1 encoding
    cannot represent, and PyMuPDF substitutes a bullet for each one. Since this
    text is only ever read by the extractor, a straight quote carries the same
    meaning and keeps citation patterns like `Cal.App. 4th` matchable.
    """
    word = "".join(_TYPOGRAPHIC.get(ch, ch) for ch in word)
    word = unicodedata.normalize("NFKD", word)
    return word.encode("latin-1", "ignore").decode("latin-1")


def page_text_chars(page):
    return len(page.get_text().strip())


def drop_specks(group):
    """Remove scanner dirt that tesseract read as stray punctuation.

    A speck reads as a confident lone comma or period a fraction of the height
    of the surrounding text. Left in, it is worse than a wrong character: a
    speck out in the margin becomes the leftmost thing on its line, and MuPDF
    then files the whole line under the margin's column instead of the body
    text, moving that sentence somewhere else in the extracted page.
    """
    if len(group) < 2:
        return group
    typical = statistics.median(w["height"] for w in group)
    return [
        w
        for w in group
        if not (len(w["text"]) == 1 and not w["text"].isalnum() and w["height"] < typical / 2)
    ] or group


def is_vertical(group):
    """Is this line the rotated court name printed down the caption margin?

    It is written sideways, so laying it out as horizontal text would stretch
    it clear across the page and straddle several body lines. MuPDF would then
    fold those lines into the sidebar's block and report them far from where
    they belong -- the reason a holding can surface at the top of the page.
    """
    words = [w for w in group if len(w["text"]) >= 3]
    if not words:
        return False
    return statistics.median(w["width"] / max(w["height"], 1e-6) for w in words) < VERTICAL_ASPECT


def is_text(group):
    """Does this recognised line look like words, or like dirt on the glass?

    Two signals together, because neither is enough alone. Confidence catches
    the misread smudges; requiring one real word catches the margin furniture
    tesseract reads confidently as a lone bracket or tick. The cost is that a
    genuine line holding nothing but a page number or a bare `Id.` is dropped
    with them -- an acceptable trade for text that comes out in reading order.
    """
    if statistics.mean(w["confidence"] for w in group) < MIN_LINE_CONFIDENCE:
        return False
    return any(len(w["text"]) >= 3 and any(c.isalpha() for c in w["text"]) for w in group)


def ocr_lines(pdf_page, scale):
    """Return (text, x, baseline, size, width) per text line, in PDF points."""
    bitmap = pdf_page.render(scale=scale)
    data = pytesseract.image_to_data(bitmap.to_pil(), output_type=Output.DICT)

    grouped = {}
    for i, raw in enumerate(data["text"]):
        word = to_latin1(raw.strip())
        if not word:
            continue
        try:
            confidence = float(data["conf"][i])
        except (TypeError, ValueError):
            continue
        if confidence < MIN_CONFIDENCE:
            continue
        key = (data["block_num"][i], data["par_num"][i], data["line_num"][i])
        grouped.setdefault(key, []).append(
            {
                "text": word,
                "confidence": confidence,
                "x": data["left"][i] / scale,
                "top": data["top"][i] / scale,
                "height": data["height"][i] / scale,
                "width": data["width"][i] / scale,
            }
        )

    candidates = [drop_specks(sorted(grouped[key], key=lambda w: w["x"])) for key in sorted(grouped)]
    candidates = [g for g in candidates if is_text(g)]

    # Only treat sideways lines as margin furniture when the page is mostly
    # upright. A page scanned in landscape is sideways in its entirety, and
    # there the rotated lines are the document -- dropping them would silently
    # empty the page instead of leaving it for a human to look at.
    upright = [g for g in candidates if not is_vertical(g)]
    if len(upright) >= len(candidates) / 2:
        candidates = upright

    lines = []
    for group in candidates:
        # A line goes down as one run rather than word by word. Word-by-word
        # placement has to shrink each word to its own box, and MuPDF reads a
        # normal word gap next to a shrunken font as a line break -- which
        # chopped single sentences into a dozen extracted lines.
        left = group[0]["x"]
        right = max(w["x"] + w["width"] for w in group)
        lines.append(
            (
                " ".join(w["text"] for w in group),
                left,
                statistics.median(w["top"] + w["height"] for w in group),
                statistics.median(w["height"] for w in group),
                right - left,
            )
        )
    # Tesseract numbers its blocks by its own segmentation, which on these
    # scans puts a mid-page line in an early block. MuPDF reports text in the
    # order it was written rather than by position, so writing in tesseract's
    # order strands that line at the top of the extracted page. Order down the
    # page instead, bucketing baselines so a caption's two columns still read
    # left to right rather than by a point of scanner skew.
    return sorted(lines, key=lambda line: (round(line[2] / BASELINE_BUCKET), line[1]))


def ocr_pdf(path, dry_run=False, force=False):
    """OCR one PDF in place. Returns (chars_before, chars_after, pages_ocred)."""
    doc = pymupdf.open(path)
    before = sum(page_text_chars(p) for p in doc)
    if before > MIN_CHARS and not force:
        doc.close()
        return before, before, 0

    pdfium_doc = pdfium.PdfDocument(path)
    scale = RENDER_DPI / 72.0
    pages_ocred = 0

    font = pymupdf.Font(FONTNAME)
    for number, page in enumerate(doc):
        lines = ocr_lines(pdfium_doc[number], scale)
        if not lines:
            continue
        # One TextWriter per page, not one insertion per line: each direct
        # insertion appends its own content stream, and a page of them costs
        # more in PDF object overhead than the scan it annotates.
        writer = pymupdf.TextWriter(page.rect)
        for text, x, baseline, size, width in lines:
            # Helvetica is wider than the scanned serif, so set at the scan's
            # own line height the run would overhang the right margin. Scale
            # it to the width the line actually occupies.
            measured = font.text_length(text, fontsize=size)
            if measured > width > 0:
                size = size * width / measured
            writer.append((x, baseline), text, font=font, fontsize=max(size, 1.0))
        writer.write_text(page, render_mode=3)
        pages_ocred += 1

    after = sum(page_text_chars(p) for p in doc)
    if not dry_run and pages_ocred:
        # PyMuPDF refuses a non-incremental save over the open file, and an
        # incremental one would append the text layer as a revision, leaving
        # the original bytes recoverable and the file larger every re-run.
        tmp = f"{path}.ocr-tmp"
        doc.save(tmp, garbage=4, deflate=True)
        doc.close()
        os.replace(tmp, path)
    else:
        doc.close()
    pdfium_doc.close()
    return before, after, pages_ocred


def scannable_pdfs():
    for dirpath, _dirnames, filenames in os.walk(DOCS_ROOT):
        for name in sorted(filenames):
            if not name.lower().endswith(".pdf"):
                continue
            path = os.path.join(dirpath, name)
            try:
                doc = pymupdf.open(path)
            except Exception:
                continue
            chars = sum(page_text_chars(p) for p in doc)
            doc.close()
            if chars <= MIN_CHARS:
                yield path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", help="PDFs to OCR")
    parser.add_argument(
        "--all",
        action="store_true",
        help=f"OCR every PDF under documents/ with <= {MIN_CHARS} extractable characters",
    )
    parser.add_argument("--dry-run", action="store_true", help="report without writing")
    parser.add_argument(
        "--force", action="store_true", help="OCR even if a text layer is already present"
    )
    args = parser.parse_args()

    if args.all:
        targets = list(scannable_pdfs())
    else:
        targets = [os.path.abspath(p) for p in args.paths]
    if not targets:
        parser.error("give one or more PDF paths, or --all")

    written = 0
    for path in targets:
        if not os.path.exists(path):
            print(f"  MISSING  {path}", file=sys.stderr)
            continue
        before, after, pages = ocr_pdf(path, dry_run=args.dry_run, force=args.force)
        label = os.path.relpath(path, REPO_ROOT)
        if not pages:
            print(f"  skipped  {before:>6} chars already  {label}")
            continue
        written += 1
        verb = "would add" if args.dry_run else "added"
        print(f"  {verb} {after - before:>6} chars over {pages} page(s)  {label}")

    print(f"\n{written} of {len(targets)} file(s) {'would be ' if args.dry_run else ''}OCR'd.")
    if written and not args.dry_run:
        print("Rebuild the indexes: npm run index:build && npm run citations:index")


if __name__ == "__main__":
    main()
