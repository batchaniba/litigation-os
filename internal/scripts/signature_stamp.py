# Portfolio universal signature: brendan-newanforbi-signature.png
# Photographed loops mark, cropped/upscaled/smoothed by
# process-signature-photo.py (charcoal on transparent). Use this for all
# generated filings that need a signature affixed rather than a typed
# name. Supersedes the CIV-100 4b extract merged in #566. Do not use the
# older cropped pen asset under internal/scripts/assets/. Prior loops
# stamps are archived next to this file as *-v1-abstract-loops.png.
import struct
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
SIGNATURE_PATH = str(
    _REPO_ROOT / "internal/assets/signature/brendan-newanforbi-signature.png"
)


def _png_size(path: str) -> tuple[int, int]:
    with open(path, "rb") as fh:
        if fh.read(8) != b"\x89PNG\r\n\x1a\n":
            raise SystemExit(f"Not a PNG: {path}")
        length, typ = struct.unpack(">I4s", fh.read(8))
        if typ != b"IHDR" or length < 8:
            raise SystemExit(f"PNG missing IHDR: {path}")
        width, height = struct.unpack(">II", fh.read(8))
    return width, height


SIGNATURE_NATIVE_PX = _png_size(SIGNATURE_PATH)
# Draw slightly taller than the PNG so the loops expand upward from the
# signature line without getting wider.
SIGNATURE_HEIGHT_SCALE = 1.15
SIGNATURE_ASPECT = (
    SIGNATURE_NATIVE_PX[1] / SIGNATURE_NATIVE_PX[0]
) * SIGNATURE_HEIGHT_SCALE

# Judicial Council SER-001 page 4, right-hand "Sign your name" line
# (PyMuPDF top-origin coords). Shared by every fill-*-ser001.py.
SER001_SIG_PAGE_INDEX = 3
SER001_SIG_WIDTH = 120.0
SER001_SIG_BASELINE = 645.0
SER001_SIG_X = 360.0


def affix_signature(canvas_obj, x, y, width=185, path=SIGNATURE_PATH):
    """Draws the canonical signature onto a reportlab canvas at (x, y),
    scaled to `width` points wide and slightly taller than native aspect
    so the loops expand upward from the line."""
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
    page.insert_image(rect, filename=path, keep_proportion=False)
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
