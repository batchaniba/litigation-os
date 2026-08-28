#!/usr/bin/env python3
"""Clean the photographed signature into the canonical transparent PNG.

Source is a low-resolution JPEG of the abstract-loops mark (lots of empty
top canvas, JPEG ringing, thin aliased strokes). This script:

  1. crops to the ink
  2. upscales 12× (LANCZOS) so the PDF stamp downsamples instead of upsamples
  3. closes gaps, dilates for stroke weight (prominence)
  4. Gaussian-blurs then re-thresholds a solid core so 12× stair-steps round
     off, keeping a short alpha fringe for PDF downsampling
  5. writes black-on-transparent RGBA

Does not restamp any already-filed PDF.

    python3 internal/scripts/process-signature-photo.py
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
    REPO / "internal/assets/signature/brendan-newanforbi-signature-v1-abstract-loops.png"
)

# Upload that produced this revision (copied into SRC_JPG on first run).
UPLOAD = Path(
    "/home/ubuntu/.cursor/projects/workspace/assets/"
    "01a04771-bab9-7745-9d75-515118915e3c.jpg"
)

INK_MAX = 210  # grayscale; below this is treated as ink
CROP_PAD = 6
SCALE = 12
DILATE_A = 7  # MaxFilter size at hi-res (odd)
DILATE_B = 3
CLOSE_SIZE = 3
BLUR = 5.0
CORE_T = 140  # blur luminance at/above this becomes solid ink
ALPHA_FLOOR = 18  # below this, treat as background
TRIM_PAD = 12


def _ensure_source() -> None:
    SRC_JPG.parent.mkdir(parents=True, exist_ok=True)
    if SRC_JPG.is_file():
        return
    if not UPLOAD.is_file():
        raise SystemExit(f"Missing signature source: {SRC_JPG} and {UPLOAD}")
    shutil.copy2(UPLOAD, SRC_JPG)


def _archive_previous() -> None:
    if OUT_PNG.is_file() and not ARCHIVE_PNG.is_file():
        shutil.copy2(OUT_PNG, ARCHIVE_PNG)


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
    bold = closed.filter(ImageFilter.MaxFilter(DILATE_A)).filter(
        ImageFilter.MaxFilter(DILATE_B)
    )
    return bold.filter(ImageFilter.GaussianBlur(radius=BLUR))


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
    rgba[..., 3] = alpha_u8
    return Image.fromarray(rgba, "RGBA")


def main() -> None:
    _ensure_source()
    _archive_previous()
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
