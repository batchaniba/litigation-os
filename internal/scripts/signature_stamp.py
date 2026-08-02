# De facto portfolio signature (for now): lifted from Doc 9's Notice
# signature block (Matter 28, Case 3:26-cv-07504-LJC, p.3), transparent
# background. Reuse this path when a generated filing needs a signature
# affixed rather than a typed name.
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
SIGNATURE_PATH = str(
    _REPO_ROOT / "internal/assets/signature/brendan-newanforbi-signature.png"
)
SIGNATURE_ASPECT = 360.0 / 1450.0  # height / width, native crop is 1450x360
SIGNATURE_NATIVE_PX = (1450, 360)


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
