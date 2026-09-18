#!/usr/bin/env python3
"""Extract signature 4b (CIV-100 p.2, item 7, 15 June 2026) to an archive PNG.

This is historical. The canonical stamp is the photographed loops mark at
internal/assets/signature/brendan-newanforbi-signature.png (rebuild with
process-signature-photo.py). Running this script must not overwrite that file.

Source: matter-12/014a CIV100 Request for Entry of Default or Default
Judgment.pdf, page 2, native 1-bit scan (1701×2215). The mark sits on
the item-7 "(SIGNATURE OF DECLARANT)" line. This script:

  1. pulls the embedded scan (no PDF resampling)
  2. keeps the largest ink component in the item-7 block
  3. drops the printed caption below the line
  4. trims the printed rule where it sticks out past the ink
  5. writes black-on-transparent RGBA, 4× with a light alpha fringe

Does not restamp any already-filed PDF.
"""
from __future__ import annotations

import io
from collections import defaultdict
from pathlib import Path

import fitz
from PIL import Image, ImageFilter
import numpy as np

REPO = Path(__file__).resolve().parents[2]
SRC_PDF = (
    REPO
    / "internal/public/documents/matter-12"
    / "014a CIV100 Request for Entry of Default or Default Judgment.pdf"
)
OUT_PNG = (
    REPO / "internal/assets/signature/brendan-newanforbi-signature-4b-civ100.png"
)
CANONICAL_PNG = REPO / "internal/assets/signature/brendan-newanforbi-signature.png"

# Native-scan crop around item 7's signature block (page-2 pixels).
CROP = (620, 1638, 1580, 1768)  # x0, y0, x1, y1
# Relative row in that crop: keep ink at y < this (drops "(SIGNATURE OF DECLARANT)").
CAPTION_Y = 92
# Form-line band inside the crop (density spike of the printed rule).
LINE_Y0, LINE_Y1 = 84, 89
PAD = 10
SCALE = 4


def _label_4connected(mask: np.ndarray) -> list[np.ndarray]:
    h, w = mask.shape
    parent = np.arange(h * w, dtype=np.int32)

    def find(x: int) -> int:
        r = x
        while parent[r] != r:
            r = parent[r]
        while parent[x] != x:
            nxt = parent[x]
            parent[x] = r
            x = nxt
        return r

    idx = np.flatnonzero(mask)
    ys, xs = np.divmod(idx, w)
    for y, x, i in zip(ys, xs, idx):
        if x + 1 < w and mask[y, x + 1]:
            a, b = find(i), find(i + 1)
            if a != b:
                parent[b] = a
        if y + 1 < h and mask[y + 1, x]:
            a, b = find(i), find(i + w)
            if a != b:
                parent[b] = a
    comps: dict[int, list[int]] = defaultdict(list)
    for i in idx:
        comps[find(i)].append(i)
    return [np.array(v) for v in comps.values()]


def _mask_from_pixels(pix: np.ndarray, h: int, w: int) -> np.ndarray:
    m = np.zeros((h, w), dtype=bool)
    yy, xx = np.divmod(pix, w)
    m[yy, xx] = True
    return m


def extract() -> Image.Image:
    if not SRC_PDF.is_file():
        raise SystemExit(f"Missing source PDF: {SRC_PDF}")
    doc = fitz.open(SRC_PDF)
    try:
        page = doc[1]
        images = page.get_images(full=True)
        if not images:
            raise SystemExit("CIV-100 page 2 has no embedded image")
        info = doc.extract_image(images[0][0])
    finally:
        doc.close()
    page_im = np.array(Image.open(io.BytesIO(info["image"])))
    ink = page_im < 128
    x0, y0, x1, y1 = CROP
    crop = ink[y0:y1, x0:x1]
    h, w = crop.shape
    comps = _label_4connected(crop)
    if not comps:
        raise SystemExit("No ink in item-7 crop")
    body = _mask_from_pixels(max(comps, key=len), h, w)
    body[CAPTION_Y:, :] = False

    # Natural right edge of the loops (rows above the printed rule).
    upper = body.copy()
    upper[LINE_Y0:, :] = False
    upper_cols = np.where(upper.any(axis=0))[0]
    if upper_cols.size == 0:
        raise SystemExit("Signature body above the form line is empty")
    right_edge = int(upper_cols.max()) + 8  # keep the short right-hand ticks
    # Printed rule sticking out past the ink.
    tail = body.copy()
    tail[:, :right_edge] = False
    tail[:LINE_Y0, :] = False
    body &= ~tail

    ys, xs = np.where(body)
    by0, by1 = max(0, int(ys.min()) - PAD), min(h, int(ys.max()) + 1 + PAD)
    bx0, bx1 = max(0, int(xs.min()) - PAD), min(w, int(xs.max()) + 1 + PAD)
    tight = body[by0:by1, bx0:bx1]

    # 4× nearest, then a light blur so the stamp's alpha fringe isn't 1-bit jaggy.
    native = Image.fromarray((~tight).astype(np.uint8) * 255)
    up = native.resize(
        (tight.shape[1] * SCALE, tight.shape[0] * SCALE),
        Image.Resampling.NEAREST,
    )
    blurred = np.array(up.filter(ImageFilter.GaussianBlur(radius=0.55)), dtype=np.float32)
    alpha = np.clip((255.0 - blurred) * 1.12, 0, 255).astype(np.uint8)
    alpha[alpha < 16] = 0
    rgba = np.zeros((alpha.shape[0], alpha.shape[1], 4), dtype=np.uint8)
    rgba[..., 3] = alpha
    return Image.fromarray(rgba, "RGBA")


def main() -> None:
    img = extract()
    OUT_PNG.parent.mkdir(parents=True, exist_ok=True)
    if OUT_PNG.resolve() == CANONICAL_PNG.resolve():
        raise SystemExit("refusing to overwrite the canonical photographed stamp")
    img.save(OUT_PNG, optimize=True)
    opaque = np.array(img)[..., 3]
    print(
        f"wrote {OUT_PNG.relative_to(REPO)}  "
        f"{img.size[0]}×{img.size[1]}  opaque={(opaque > 0).sum()}  "
        f"aspect={img.size[1] / img.size[0]:.6f}"
    )


if __name__ == "__main__":
    main()
