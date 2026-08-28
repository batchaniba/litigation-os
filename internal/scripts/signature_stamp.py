# Portfolio universal signature: brendan-newanforbi-signature.png
# Extracted from CIV-100 p.2 item 7 (Matter 12 Diamond, 15 June 2026) —
# signature 4b. Transparent background. Use this for all generated filings
# that need a signature affixed rather than a typed name. Do not use the
# older cropped pen asset under internal/scripts/assets/. The prior loops
# stamp is archived next to this file as *-v1-abstract-loops.png.
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
SIGNATURE_PATH = str(
    _REPO_ROOT / "internal/assets/signature/brendan-newanforbi-signature.png"
)
SIGNATURE_ASPECT = 236.0 / 1840.0  # height / width
SIGNATURE_NATIVE_PX = (1840, 236)

# Judicial Council SER-001 page 4, right-hand "Sign your name" line
# (PyMuPDF top-origin coords). Shared by every fill-*-ser001.py.
SER001_SIG_PAGE_INDEX = 3
SER001_SIG_WIDTH = 120.0
SER001_SIG_BASELINE = 645.0
SER001_SIG_X = 360.0


def affix_signature(canvas_obj, x, y, width=150, path=SIGNATURE_PATH):
    """Draws the canonical signature onto a reportlab canvas at (x, y),
    scaled to `width` points wide, preserving native aspect ratio."""
    height = width * SIGNATURE_ASPECT
    canvas_obj.drawImage(path, x, y, width=width, height=height, mask="auto")
    return height


def stamp_on_pdf_line(page, x0, x1, y_line, path=SIGNATURE_PATH):
    """Stamp the canonical signature onto a PyMuPDF page, sitting on y_line."""
    import fitz

    width = x1 - x0
    height = width * SIGNATURE_ASPECT
    rect = fitz.Rect(x0, y_line - height, x1, y_line)
    page.draw_rect(rect, color=(1, 1, 1), fill=(1, 1, 1), width=0)
    page.insert_image(rect, filename=path, keep_proportion=True)
    return rect


def stamp_ser001_signature(path, *, page_index=SER001_SIG_PAGE_INDEX):
    """Stamp the canonical signature on SER-001 page 4's signature line."""
    import fitz

    path = Path(path)
    if not Path(SIGNATURE_PATH).is_file():
        raise SystemExit(f"Missing signature image: {SIGNATURE_PATH}")
    doc = fitz.open(path)
    try:
        page = doc[page_index]
        stamp_on_pdf_line(
            page,
            SER001_SIG_X,
            SER001_SIG_X + SER001_SIG_WIDTH,
            SER001_SIG_BASELINE,
        )
        tmp = path.with_name(path.stem + ".signed.pdf")
        doc.save(tmp, garbage=4, deflate=True, incremental=False)
    finally:
        doc.close()
    tmp.replace(path)
    return path
