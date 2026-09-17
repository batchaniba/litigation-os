#!/usr/bin/env python3
"""Historical: photographed loops mark → archived canonical PNG.

Superseded. The live stamp is internal/assets/signature/
brendan-newanforbi-signature.png, produced by extract-signature-scan.py.
Running this script must not overwrite that file; it only rebuilds the
archived photograph at *-v2-photo-loops.png.

Does not restamp any already-filed PDF.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

REPO = Path(__file__).resolve().parents[2]
SRC_JPG = (
    REPO / "internal/assets/signature/brendan-newanforbi-signature-source-v2-photo.jpg"
)
OUT_PNG = (
    REPO / "internal/assets/signature/brendan-newanforbi-signature-v2-photo-loops.png"
)
CANONICAL_PNG = REPO / "internal/assets/signature/brendan-newanforbi-signature.png"

INK_MAX = 210  # grayscale; below this is treated as ink
CROP_PAD = 6
SCALE = 12
CLOSE_SIZE = 3  # morphological close only; do not dilate
ERODE_SIZE = 5  # slight thin after close (odd Max/Min neighborhood)
BLUR = 3.0
CORE_T = 212  # blur luminance at/above this becomes solid ink
ALPHA_FLOOR = 22  # below this, treat as background
INK_RGB = 40  # charcoal, not pure black — dials down visual weight
TRIM_PAD = 12


def _crop_ink(gray: Image.Image) -> Image.Image:
    g = np.array(gray, dtype=np.uint8)
    ys, xs = np.where(g < INK_MAX)
    if ys.size == 0:
        raise SystemExit("no ink found in source JPEG")
    y0 = max(0, int(ys.min()) - CROP_PAD)
    y1 = min(g.shape[0], int(ys.max()) + CROP_PAD + 1)
    x0 = max(0, int(xs.min()) - CROP_PAD)
    x1 = min(g.shape[1], int(xs.max()) + CROP_PAD + 1)
    return gray.crop((x0, y0, x1, y1))


def _mask(hi: Image.Image) -> Image.Image:
    g = np.array(hi, dtype=np.uint8)
    core = Image.fromarray(((g < 185).astype(np.uint8) * 255), "L")
    closed = core.filter(ImageFilter.MaxFilter(CLOSE_SIZE)).filter(
        ImageFilter.MinFilter(CLOSE_SIZE)
    )
    thinned = closed.filter(ImageFilter.MinFilter(ERODE_SIZE))
    return thinned.filter(ImageFilter.GaussianBlur(radius=BLUR))


def _to_rgba(alpha_img: Image.Image) -> Image.Image:
    a = np.array(alpha_img, dtype=np.float32)
    solid = a >= CORE_T
    fringe = np.clip((a - ALPHA_FLOOR) / (CORE_T - ALPHA_FLOOR), 0.0, 1.0)
    alpha = np.where(solid, 1.0, fringe)
    alpha_u8 = (alpha * 255.0).astype(np.uint8)
    ys, xs = np.where(alpha_u8 > 8)
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
    if OUT_PNG.resolve() == CANONICAL_PNG.resolve():
        raise SystemExit("refusing to overwrite the canonical scan stamp")
    if not SRC_JPG.is_file():
        raise SystemExit(f"Missing archived photo source: {SRC_JPG}")
    gray = Image.open(SRC_JPG).convert("L")
    crop = _crop_ink(gray)
    hi = crop.resize(
        (crop.size[0] * SCALE, crop.size[1] * SCALE), Image.Resampling.LANCZOS
    )
    rgba = _to_rgba(_mask(hi))
    rgba.save(OUT_PNG, optimize=True)
    print(
        f"wrote {OUT_PNG} {rgba.size[0]}×{rgba.size[1]}  "
        f"aspect={rgba.size[1]/rgba.size[0]:.4f}  "
        f"from crop {crop.size}"
    )


if __name__ == "__main__":
    main()
