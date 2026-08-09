#!/usr/bin/env python3
"""Re-encode the header branding artwork at the size the CSS actually renders it.

The source files are full-resolution originals — logo-dark.png is 1254x1254 for
a slot that is never taller than 220 CSS pixels, and garcia-gurney-dark.png is
2401x408 for a 130x44 slot. Shipping those to a browser costs about 1.7 MB on
first paint, roughly eleven times the entire JS+CSS bundle.

This writes 2x WebP alongside the originals. It is run on demand, not in the
build: the artwork changes approximately never, so a committed output beats a
build-time dependency on an image toolchain.

    python3 -m pip install pillow
    python3 internal/scripts/optimize-branding-images.py

Pass --check to verify the committed WebP files match the sources. Not wired into
CI, which deliberately skips installing the Python image/PDF stack — run it by
hand after touching anything in internal/assets/branding/source/.
"""

import sys
from io import BytesIO
from pathlib import Path

try:
    from PIL import Image
except ImportError:  # pragma: no cover - developer convenience path
    sys.exit("Pillow is required: python3 -m pip install pillow")

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets" / "branding" / "source"  # originals, deliberately outside publicDir
PUBLIC = ROOT / "public"

# (source, output, rendered CSS size at the largest breakpoint).
# Height drives the resize; width is derived from the source aspect ratio unless
# the CSS pins both (the Garcia wordmark and the circular DAG crest).
TARGETS = [
    ("logo-dark.png", "logo-dark.webp", (220, 220)),
    ("logo-light.png", "logo-light.webp", (220, 220)),
    # Same CSS box for both themes (see .legacy-slb-logo) so the header does
    # not reflow when the theme toggle swaps the file. Light artwork letterboxes
    # inside the taller dark-mode aspect via object-fit: contain.
    ("slb-dark.png", "branding/slb-dark.webp", (118, 62)),
    ("slb-light.png", "branding/slb-light.webp", (118, 62)),
    ("garcia-gurney-dark.png", "branding/garcia-gurney-dark.webp", (130, 44)),
    ("garcia-gurney.png", "branding/garcia-gurney.webp", (130, 44)),
    ("dag-dark.jpg", "branding/dag-dark.webp", (64, 64)),
    ("dag-light.jpg", "branding/dag-light.webp", (64, 64)),
]

SCALE = 2  # serve 2x so the artwork stays crisp on retina displays
QUALITY = 82


def encode(source: Path, css_size: tuple) -> bytes:
    image = Image.open(source).convert("RGBA")
    css_width, css_height = css_size
    height = css_height * SCALE
    width = css_width * SCALE if css_width else round(image.width * height / image.height)
    resized = image.resize((width, height), Image.LANCZOS)
    buffer = BytesIO()
    resized.save(buffer, "WEBP", quality=QUALITY, method=6)
    return buffer.getvalue()


def main() -> int:
    check = "--check" in sys.argv
    stale, before, after = [], 0, 0

    for source_name, output_name, css_size in TARGETS:
        source, output = SOURCE / source_name, PUBLIC / output_name
        if not source.exists():
            sys.exit(f"missing source image: {source}")
        data = encode(source, css_size)
        before += source.stat().st_size
        after += len(data)

        if check:
            if not output.exists() or output.read_bytes() != data:
                stale.append(output_name)
            continue

        output.write_bytes(data)
        print(f"{output_name:38} {source.stat().st_size / 1024:8.1f} KB -> {len(data) / 1024:6.1f} KB")

    if check:
        if stale:
            print("Branding WebP files are out of date: " + ", ".join(stale))
            print("Run: python3 internal/scripts/optimize-branding-images.py")
            return 1
        print(f"Branding images current ({len(TARGETS)} files).")
        return 0

    print(f"\n{'total':38} {before / 1024:8.1f} KB -> {after / 1024:6.1f} KB  ({before / after:.0f}x smaller)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
