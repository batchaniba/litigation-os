#!/usr/bin/env python3
"""Isolate the wet signature by zooming in and painting non-ink white.

Better than a tight rectangle crop: keep a generous canvas, upscale first,
then decide every pixel. Signature ink stays. Everything else is painted
out (white on the working plate, transparent on the stamp).

  1. upscale 8× (LANCZOS) so the work is done on zoomed pixels
  2. threshold ink
  3. drop isolated specks and wide/thin form-rule slivers
  4. keep only components attached to the main signature body
  5. paint every other pixel out
  6. write charcoal-on-transparent RGBA (not pure #000)

Does not restamp any already-filed PDF. The originating scan is not stored.

    python3 internal/scripts/extract-signature-scan.py
"""
from __future__ import annotations

from collections import defaultdict
from pathlib import Path

import numpy as np
from PIL import Image

REPO = Path(__file__).resolve().parents[2]
SRC_JPG = REPO / "internal/assets/signature/brendan-newanforbi-signature-source.jpg"
OUT_PNG = REPO / "internal/assets/signature/brendan-newanforbi-signature.png"
PREVIEW_PNG = (
    REPO / "internal/assets/signature/brendan-newanforbi-signature-preview.png"
)

SCALE = 8
INK_MAX = 168
MIN_COMPONENT = 40  # at upscaled resolution; drops JPEG dirt
RULE_WIDTH_FRAC = 0.45
RULE_MAX_HEIGHT = 10
SLIVER_MAX_HEIGHT = 22  # dashed form-rule fragments after they break off
SLIVER_MIN_ASPECT = 5
INK_RGB = 40
PAD = 24  # transparent / white margin after isolation, not a content crop


def _label_4(mask: np.ndarray) -> list[np.ndarray]:
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
    if idx.size == 0:
        return []
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
        comps[find(i)].append(int(i))
    return [np.array(v, dtype=np.int32) for v in comps.values()]


def _bbox(pixels: np.ndarray, w: int) -> tuple[int, int, int, int]:
    ys, xs = np.divmod(pixels, w)
    return int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())


def _is_form_rule(width: int, height: int, img_w: int) -> bool:
    """Printed signature-line fragments: wide and flat, not pen strokes."""
    if height <= 5:
        return True
    if width >= int(img_w * RULE_WIDTH_FRAC) and height <= RULE_MAX_HEIGHT:
        return True
    if height <= SLIVER_MAX_HEIGHT and width >= 40 and width >= SLIVER_MIN_ASPECT * height:
        return True
    return False


def _column_clusters(keep: np.ndarray, x: int) -> list[np.ndarray]:
    ys = np.where(keep[:, x])[0]
    if ys.size == 0:
        return []
    gaps = np.where(np.diff(ys) > 2)[0]
    starts = np.r_[0, gaps + 1]
    ends = np.r_[gaps, ys.size - 1]
    return [ys[a : b + 1] for a, b in zip(starts, ends)]


def _keep_signature(ink: np.ndarray) -> np.ndarray:
    """Paint-out mask: True = keep as ink. Everything else will be cleared."""
    h, w = ink.shape
    keep = np.zeros_like(ink, dtype=bool)
    comps = _label_4(ink)
    if not comps:
        raise SystemExit("no ink after threshold")

    scored = []
    for pix in comps:
        x0, y0, x1, y1 = _bbox(pix, w)
        width, height = x1 - x0 + 1, y1 - y0 + 1
        scored.append((pix.size, width, height, pix))

    # Main body = largest component that is not a form-rule sliver.
    body = None
    for n, width, height, pix in sorted(scored, key=lambda t: t[0], reverse=True):
        if _is_form_rule(width, height, w):
            continue
        if n < MIN_COMPONENT:
            continue
        body = pix
        break
    if body is None:
        raise SystemExit("no signature body survived the rule/speck filter")

    keep.ravel()[body] = True

    # Keep other components only if they sit inside/near the body bbox
    # (inner ticks of the loops). Drop far specks and rule stubs.
    bx0, by0, bx1, by1 = _bbox(body, w)
    pad_x, pad_y = 8, 8
    for n, width, height, pix in scored:
        if np.array_equal(pix, body):
            continue
        if n < MIN_COMPONENT:
            continue
        if _is_form_rule(width, height, w):
            continue
        x0, y0, x1, y1 = _bbox(pix, w)
        cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
        if (bx0 - pad_x) <= cx <= (bx1 + pad_x) and (by0 - pad_y) <= cy <= (
            by1 + pad_y
        ):
            keep.ravel()[pix] = True
    return _paint_form_rule_tail(keep)


def _paint_form_rule_tail(keep: np.ndarray) -> np.ndarray:
    """Paint white over the printed signature-line dashes past the oval.

    A tight crop leaves those pixels because they share a y with the oval.
    Zoomed, they are a thin horizontal run that dies into white on the right
    — either detached dashes or a short rectangular cap still touching the
    oval at the junction. The descending oval is a diagonal (y-extent
    grows) and is left alone; walking until the first thick cluster would
    slice the neck.
    """
    out = keep.copy()
    h, w = out.shape
    y_lo, y_hi = int(h * 0.30), int(h * 0.55)
    x_from = int(w * 0.62)
    # (x, y0, y1, cluster)
    thin: list[tuple[int, int, int, np.ndarray]] = []
    for x in range(x_from, w):
        for cluster in _column_clusters(out, x):
            span = int(cluster[-1] - cluster[0] + 1)
            mid = int(cluster[0] + cluster[-1]) // 2
            if span <= 16 and y_lo <= mid <= y_hi:
                thin.append((x, int(cluster[0]), int(cluster[-1]), cluster))
    if not thin:
        return out

    # Consecutive-x runs with a stable y-band (a horizontal cap, not a diagonal).
    runs: list[list[tuple[int, int, int, np.ndarray]]] = []
    current = [thin[0]]
    for item in thin[1:]:
        prev = current[-1]
        same_x_step = item[0] <= prev[0] + 2
        stable_y = abs(item[1] - prev[1]) <= 3 and abs(item[2] - prev[2]) <= 3
        if same_x_step and stable_y:
            current.append(item)
        else:
            runs.append(current)
            current = [item]
    runs.append(current)

    for run in runs:
        if len(run) < 8:
            continue
        y0 = min(t[1] for t in run)
        y1 = max(t[2] for t in run)
        x_right = max(t[0] for t in run)
        # Must die into white: no ink in this y-band just to the right.
        if x_right + 1 < w and out[y0:y1 + 1, x_right + 1].any():
            continue
        for x, _, _, cluster in run:
            out[cluster, x] = False
    return out


def isolate(gray: Image.Image) -> tuple[Image.Image, Image.Image]:
    """Return (transparent stamp, white-background preview) at zoomed size."""
    hi = gray.resize(
        (gray.size[0] * SCALE, gray.size[1] * SCALE), Image.Resampling.LANCZOS
    )
    g = np.array(hi.convert("L"), dtype=np.uint8)
    keep = _keep_signature(g < INK_MAX)

    # Strength of kept ink from the zoomed grayscale; paper is painted out.
    darkness = np.clip((INK_MAX - g.astype(np.float32)) / INK_MAX, 0.0, 1.0)
    alpha = np.where(keep, np.clip(darkness * 255.0 * 1.15, 0, 255), 0).astype(
        np.uint8
    )
    alpha[keep & (alpha < 40)] = 40  # keep thin stroke ends visible

    ys, xs = np.where(keep)
    y0 = max(0, int(ys.min()) - PAD)
    y1 = min(keep.shape[0], int(ys.max()) + PAD + 1)
    x0 = max(0, int(xs.min()) - PAD)
    x1 = min(keep.shape[1], int(xs.max()) + PAD + 1)
    alpha = alpha[y0:y1, x0:x1]
    keep_c = keep[y0:y1, x0:x1]

    rgba = np.zeros((alpha.shape[0], alpha.shape[1], 4), dtype=np.uint8)
    rgba[..., 0] = INK_RGB
    rgba[..., 1] = INK_RGB
    rgba[..., 2] = INK_RGB
    rgba[..., 3] = alpha
    stamp = Image.fromarray(rgba, "RGBA")

    plate = np.full((alpha.shape[0], alpha.shape[1], 3), 255, dtype=np.uint8)
    plate[keep_c] = INK_RGB
    preview = Image.fromarray(plate, "RGB")
    return stamp, preview


def write_tiles(preview: Image.Image, dest: Path) -> None:
    """Nearest-neighbor zoom tiles so leftover non-ink is visible."""
    dest.mkdir(parents=True, exist_ok=True)
    arr = np.array(preview)
    h, w = arr.shape[:2]
    rows, cols = 2, 3
    tile_h, tile_w = h // rows, w // cols
    for r in range(rows):
        for c in range(cols):
            y0, x0 = r * tile_h, c * tile_w
            y1 = h if r == rows - 1 else y0 + tile_h
            x1 = w if c == cols - 1 else x0 + tile_w
            tile = Image.fromarray(arr[y0:y1, x0:x1])
            zoom = tile.resize(
                (tile.size[0] * 2, tile.size[1] * 2), Image.Resampling.NEAREST
            )
            zoom.save(dest / f"tile_r{r}_c{c}.png", optimize=True)


def main() -> None:
    if not SRC_JPG.is_file():
        raise SystemExit(f"Missing signature source: {SRC_JPG}")
    stamp, preview = isolate(Image.open(SRC_JPG))
    stamp.save(OUT_PNG, optimize=True)
    # Phone-readable preview: white plate, signature on a rule.
    pad_x, pad_top, pad_bot = 48, 56, 72
    target_w = 1400
    ratio = target_w / preview.size[0]
    shown = preview.resize(
        (target_w, int(preview.size[1] * ratio)), Image.Resampling.LANCZOS
    )
    page = Image.new(
        "RGB",
        (shown.size[0] + pad_x * 2, shown.size[1] + pad_top + pad_bot),
        (255, 255, 255),
    )
    page.paste(shown, (pad_x, pad_top))
    from PIL import ImageDraw

    draw = ImageDraw.Draw(page)
    y_line = pad_top + shown.size[1] - 14
    draw.line(
        (pad_x + 16, y_line, page.size[0] - pad_x - 16, y_line),
        fill=(30, 30, 30),
        width=3,
    )
    page.save(PREVIEW_PNG, optimize=True)
    art = Path("/opt/cursor/artifacts/screenshots")
    art.mkdir(parents=True, exist_ok=True)
    page.save(art / "canonical_signature_stamp_paintout.png", optimize=True)
    write_tiles(preview, Path("/tmp/sig-tiles"))
    print(
        f"wrote {OUT_PNG.relative_to(REPO)} {stamp.size[0]}×{stamp.size[1]}  "
        f"aspect={stamp.size[1]/stamp.size[0]:.4f}"
    )
    print(f"wrote {PREVIEW_PNG.relative_to(REPO)} {page.size[0]}×{page.size[1]}")


if __name__ == "__main__":
    main()
