# De facto portfolio signature (for now): lifted from Doc 9's Notice
# signature block (Matter 28, Case 3:26-cv-07504-LJC, p.3), transparent
# background. Reuse this path when a generated filing needs a signature
# affixed rather than a typed name.
SIGNATURE_PATH = "internal/assets/signature/brendan-newanforbi-signature.png"
SIGNATURE_ASPECT = 360.0 / 1450.0  # height / width, native crop is 1450x360


def affix_signature(canvas_obj, x, y, width=150, path=SIGNATURE_PATH):
    """Draws the canonical signature onto a reportlab canvas at (x, y),
    scaled to `width` points wide, preserving native aspect ratio."""
    height = width * SIGNATURE_ASPECT
    canvas_obj.drawImage(path, x, y, width=width, height=height, mask="auto")
    return height
