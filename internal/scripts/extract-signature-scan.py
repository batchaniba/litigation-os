#!/usr/bin/env python3
"""Extract the page-1 wet signature into the canonical transparent PNG.

Source is a tight crop of the handwritten mark only (no form, no fingerprint,
no caption). The originating scan is discarded and is not in this repository.

  1. thresholds ink
  2. drops full-width form-rule slivers
  3. upscales 8× (LANCZOS) so the PDF stamp downsamples instead of upsamples
  4. closes tiny scan gaps, light erode, Gaussian-blur then re-threshold
  5. writes dark-charcoal-on-transparent RGBA (not pure #000)

Does not restamp any already-filed PDF.

    python3 internal/scripts/extract-signature-scan.py
"""
from __future__ import annotations

import shutil
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

REPO = Path(__file__).resolve().parents[2]
SRC_JPG = REPO / "internal/assets/signature/brendan-newanforbi-signature-source.jpg"
OUT_PNG = REPO / "internal/assets/signature/brendan-newanforbi-signature.png"
ARCHIVE_PNG = (
    REPO / "internal/assets/signature/brendan-newanforbi-signature-v2-photo-loops.png"
)
ARCHIVE_SRC = (
    REPO / "internal/assets/signature/brendan-newanforbi-signature-source-v2-photo.jpg"
)

INK_MAX = 175
SCALE = 8
CLOSE_SIZE = 3
ERODE_SIZE = 3
BLUR = 2.4
CORE_T = 208
ALPHA_FLOOR = 18
INK_RGB = 40
TRIM_PAD = 10
RULE_WIDTH_FRAC = 0.55
RULE_MAX_HEIGHT = 6


def _archive_previous() -> None:
    if OUT_PNG.is_file() and not ARCHIVE_PNG.is_file():
        shutil.copy2(OUT_PNG, ARCHIVE_PNG)
    src_v2 = REPO / "internal/assets/signature/brendan-newanforbi-signature-source.jpg"
    # Archive the photographed source if this file is still that photo
    # (short/wide JPEG from process-signature-photo.py). Skip if already the
    # scan crop.
    if src_v2.is_file() and not ARCHIVE_SRC.is_file():
        im = Image.open(src_v2)
        if im.size == (520, 214):
            shutil.copy2(src_v2, ARCHIVE_SRC)


def _drop_form_rules(ink: np.ndarray) -> np.ndarray:
    """Drop short, near-full-width bars (printed form rules), keep handwriting."""
    h, w = ink.shape
    out = ink.copy()
    min_w = int(w * RULE_WIDTH_FRAC)
    visited = np.zeros_like(ink, dtype=bool)
    ys, xs = np.where(ink)
    for y, x in zip(ys, xs):
        if visited[y, x]:
            continue
        # flood a 4-connected component
        stack = [(y, x)]
        cells = []
        visited[y, x] = True
        while stack:
            cy, cx = stack.pop()
            cells.append((cy, cx))
            for ny, nx in ((cy - 1, cx), (cy + 1, cx), (cy, cx - 1), (cy, cx + 1)):
                if 0 <= ny < h and 0 <= nx < w and ink[ny, nx] and not visited[ny, nx]:
                    visited[ny, nx] = True
                    stack.append((ny, nx))
        ys_c = [p[0] for p in cells]
        xs_c = [p[1] for p in cells]
        height = max(ys_c) - min(ys_c) + 1
        width = max(xs_c) - min(xs_c) + 1
        if width >= min_w and height <= RULE_MAX_HEIGHT:
            for cy, cx in cells:
                out[cy, cx] = False
    return out


def _to_rgba(alpha_img: Image.Image) -> Image.Image:
    a = np.array(alpha_img, dtype=np.float32)
    solid = a >= CORE_T
    fringe = np.clip((a - ALPHA_FLOOR) / (CORE_T - ALPHA_FLOOR), 0.0, 1.0)
    alpha = np.where(solid, 1.0, fringe)
    alpha_u8 = (alpha * 255.0).astype(np.uint8)
    ys, xs = np.where(alpha_u8 > 8)
    if ys.size == 0:
        raise SystemExit("no ink after threshold")
    y0 = max(0, int(ys.min()) - TRIM_PAD)
    y1 = min(alpha_u8.shape[0], int(ys.max()) + TRIM_PAD + 1)
    x0 = max(0, int(xs.min()) - TRIM_PAD)
    x1 = min(alpha_u8.shape[1], int(xs.max()) + TRIM_PAD + 1)
    alpha_u8 = alpha_u8[y0:y1, x0:x1]
    rgba = np.zeros((alpha_u8.shape[0], alpha_u8.shape[1], 4), dtype=np.uint8)
    rgba[..., 0] = INK_RGB
    rgba[..., 1] = INK_RGB
    rgba[..., 2] = INK_RGB
    rgba[..., 3] = alpha_u8
    return Image.fromarray(rgba, "RGBA")


def main() -> None:
    if not SRC_JPG.is_file():
        raise SystemExit(f"Missing signature source crop: {SRC_JPG}")
    _archive_previous()
    gray = Image.open(SRC_JPG).convert("L")
    g = np.array(gray, dtype=np.uint8)
    ink = _drop_form_rules(g < INK_MAX)
    ys, xs = np.where(ink)
    if ys.size == 0:
        raise SystemExit("no ink in source crop")
    y0 = max(0, int(ys.min()) - 4)
    y1 = min(ink.shape[0], int(ys.max()) + 5)
    x0 = max(0, int(xs.min()) - 4)
    x1 = min(ink.shape[1], int(xs.max()) + 5)
    tight = (~ink[y0:y1, x0:x1]).astype(np.uint8) * 255
    crop = Image.fromarray(tight, "L")
    hi = crop.resize(
        (crop.size[0] * SCALE, crop.size[1] * SCALE), Image.Resampling.LANCZOS
    )
    core = Image.fromarray(((np.array(hi) < 185).astype(np.uint8) * 255), "L")
    closed = core.filter(ImageFilter.MaxFilter(CLOSE_SIZE)).filter(
        ImageFilter.MinFilter(CLOSE_SIZE)
    )
    thinned = closed.filter(ImageFilter.MinFilter(ERODE_SIZE))
    blurred = thinned.filter(ImageFilter.GaussianBlur(radius=BLUR))
    rgba = _to_rgba(blurred)
    rgba.save(OUT_PNG, optimize=True)
    print(
        f"wrote {OUT_PNG.relative_to(REPO)} {rgba.size[0]}×{rgba.size[1]}  "
        f"aspect={rgba.size[1]/rgba.size[0]:.4f}  from crop {crop.size}"
    )


if __name__ == "__main__":
    main()
