#!/usr/bin/env python3
"""Rebuild Matter 12 Diamond/Alpine default judgment packets.

Patches CIV-100 item 2 monetary fields, stamps the canonical signature over the CIV-100
signature markers, swaps in the regenerated August 3 declarations, and writes
filing-ready packet PDFs.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "internal/public/documents/matter-12"
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from signature_stamp import SIGNATURE_PATH  # noqa: E402

SIGNATURE_IMG = Path(SIGNATURE_PATH)

DIAMOND_OUT = OUT_DIR / (
    "1094 Diamond Default Judgment Packet "
    "(Corrected per Clerk Rejection, Ready to File Aug 3 2026).pdf"
)
ALPINE_OUT = OUT_DIR / (
    "1094 Alpine Default Judgment Packet "
    "(Corrected per Clerk Rejection, Ready to File Aug 3 2026).pdf"
)
# Prefer clean pre-fix backups when present so re-runs do not stack overlays.
_BACKUP_DIR = Path("/tmp/m12build")
DIAMOND_SRC = (
    _BACKUP_DIR / "backup_Diamond_packet_pre_fix.pdf"
    if (_BACKUP_DIR / "backup_Diamond_packet_pre_fix.pdf").is_file()
    else DIAMOND_OUT
)
_ALPINE_LEGACY = OUT_DIR / (
    "1094 Alpine Default Judgment Packet "
    "(Corrected per Clerk Rejection -- Pending Valid Re-Service, "
    "Execution Date Aug 3 2026).pdf"
)
ALPINE_SRC = (
    _BACKUP_DIR / "backup_Alpine_packet_pre_fix.pdf"
    if (_BACKUP_DIR / "backup_Alpine_packet_pre_fix.pdf").is_file()
    else _ALPINE_LEGACY
    if _ALPINE_LEGACY.is_file()
    else ALPINE_OUT
)

# CIV-100 item 2 amounts (match JUD-100 components / waiver of costs).
# Demand = compensatory damages $49,368.65 + punitive $25,000.00.
DEMAND = "74,368.65"
INTEREST = "4,302.55"
COSTS = "0.00"
TOTAL = "78,671.20"
ZERO = "0.00"

# Dollar-sign x anchors from the filled CIV-100 form pages.
AMT_X = 232.0
CRED_X = 346.0
BAL_X = 474.0
# Baseline y for each item-2 row (page 1 of CIV-100 / packet page index 1).
ROW_Y = {
    "a": 522.5,  # Demand of complaint
    "c": 568.8,  # Interest
    "d": 580.3,  # Costs
    "f": 603.3,  # TOTALS
}

# Signature stamp rects on CIV-100 pages (packet page indices 1-3).
# Cover the black triangular marker and sit on the signature line.
CIV100_SIGS = {
    1: [fitz.Rect(355, 655, 520, 688)],
    2: [fitz.Rect(355, 415, 520, 450), fitz.Rect(355, 610, 520, 645)],
    3: [fitz.Rect(355, 665, 520, 700)],
}

# Source packet page ranges (0-indexed, inclusive end exclusive).
DIAMOND_RANGES = {
    "pos": (0, 1),
    "civ100": (1, 4),
    "exhibits": (18, 52),
    "jud100": (52, 54),
}
ALPINE_RANGES = {
    "pos": (0, 1),
    "civ100": (1, 4),
    "exhibits": (11, 45),
    "jud100": (45, 47),
}


def run_declarations() -> tuple[Path, Path]:
    build_dir = Path("/tmp/m12build")
    build_dir.mkdir(parents=True, exist_ok=True)
    script = SCRIPT_DIR / "matter12-default-declaration-formatter.py"
    env = dict(**{k: v for k, v in __import__("os").environ.items()})
    env["MATTER12_DECL_OUT_DIR"] = str(build_dir)
    subprocess.check_call([sys.executable, str(script)], env=env)
    diamond = build_dir / "_build_Diamond_Declaration_ISO_Default_Judgment_Aug3_2026.pdf"
    alpine = build_dir / "_build_Alpine_Declaration_ISO_Default_Judgment_Aug3_2026.pdf"
    # Formatter uses those exact filenames.
    if not diamond.is_file():
        # Formatter writes without _build prefix historically; accept either.
        candidates = sorted(build_dir.glob("*Diamond*Declaration*.pdf"))
        if not candidates:
            raise SystemExit("Diamond declaration build output missing")
        diamond = candidates[-1]
    if not alpine.is_file():
        candidates = sorted(build_dir.glob("*Alpine*Declaration*.pdf"))
        if not candidates:
            raise SystemExit("Alpine declaration build output missing")
        alpine = candidates[-1]
    return diamond, alpine


def fill_money(page: fitz.Page, row: str, amount: str, credits: str, balance: str) -> None:
    y = ROW_Y[row]
    page.insert_text((AMT_X, y), amount, fontsize=9, fontname="helv", color=(0, 0, 0))
    page.insert_text((CRED_X, y), credits, fontsize=9, fontname="helv", color=(0, 0, 0))
    page.insert_text((BAL_X, y), balance, fontsize=9, fontname="helv", color=(0, 0, 0))


def stamp_signature(page: fitz.Page, rect: fitz.Rect) -> None:
    # White out the triangular marker / blank line area, then stamp.
    page.draw_rect(rect, color=(1, 1, 1), fill=(1, 1, 1), width=0)
    page.insert_image(rect, filename=str(SIGNATURE_IMG), keep_proportion=True)


def patch_civ100(src_doc: fitz.Document, start: int, end: int) -> fitz.Document:
    """Return a new 3-page CIV-100 doc with item 2 filled and signatures stamped."""
    out = fitz.open()
    out.insert_pdf(src_doc, from_page=start, to_page=end - 1)
    page0 = out[0]
    fill_money(page0, "a", DEMAND, ZERO, DEMAND)
    fill_money(page0, "c", INTEREST, ZERO, INTEREST)
    fill_money(page0, "d", COSTS, ZERO, COSTS)
    fill_money(page0, "f", TOTAL, ZERO, TOTAL)
    for page_idx, rects in CIV100_SIGS.items():
        page = out[page_idx - 1]
        for rect in rects:
            stamp_signature(page, rect)
    # Item 4: check "did not" (no LDA/UDA assistance).
    page1 = out[1]
    page1.draw_rect(
        fitz.Rect(215.5, 103.5, 224.5, 112.5),
        color=(0, 0, 0),
        fill=(0, 0, 0),
        width=0.5,
    )
    # JUD-100 costs already blank; CIV-100 7f already checked in source.
    return out


def set_jud100_costs_zero(src_doc: fitz.Document, start: int, end: int) -> fitz.Document:
    """Copy JUD-100 and explicitly put $0.00 in costs to match the waiver."""
    out = fitz.open()
    out.insert_pdf(src_doc, from_page=start, to_page=end - 1)
    # JUD-100 page 2 (index 1): costs field near (4) Costs $
    page = out[1]
    words = page.get_text("words")
    for w in words:
        if w[4] == "Costs" and w[1] > 200:
            # Insert 0.00 just after the nearby $ on same row if empty.
            # Prefer the first Costs on the left judgment column.
            page.insert_text(
                (w[2] + 55, w[3] - 1),
                "0.00",
                fontsize=9,
                fontname="helv",
                color=(0, 0, 0),
            )
            break
    return out


def assemble(
    src_path: Path,
    ranges: dict[str, tuple[int, int]],
    decl_path: Path,
    out_path: Path,
) -> None:
    src = fitz.open(src_path)
    civ = patch_civ100(src, *ranges["civ100"])
    jud = set_jud100_costs_zero(src, *ranges["jud100"])
    decl = fitz.open(decl_path)

    out = fitz.open()
    out.insert_pdf(src, from_page=ranges["pos"][0], to_page=ranges["pos"][1] - 1)
    out.insert_pdf(civ)
    out.insert_pdf(decl)
    out.insert_pdf(src, from_page=ranges["exhibits"][0], to_page=ranges["exhibits"][1] - 1)
    out.insert_pdf(jud)

    # Write via temp then replace, so in-place overwrite is safe.
    tmp = out_path.with_suffix(".tmp.pdf")
    out.save(tmp, garbage=4, deflate=True)
    out.close()
    civ.close()
    jud.close()
    decl.close()
    src.close()
    shutil.move(str(tmp), str(out_path))
    print(f"Wrote {out_path.name} ({fitz.open(out_path).page_count} pages)")


def verify(path: Path, expect_mc010: bool = False) -> None:
    doc = fitz.open(path)
    full = "\n".join(page.get_text() for page in doc)
    checks = {
        "item2_demand": DEMAND in full,
        "item2_interest": INTEREST in full,
        "item2_total": TOTAL in full,
        "exec_aug3": "August 3, 2026" in full or "08/03/2026" in full,
        "no_mc010_claim": ("Memorandum of Costs (Form MC-010)" not in full)
        or ("no Memorandum of Costs" in full.lower())
        or ("waives costs" in full.lower()),
        "signed_images": any(len(page.get_images()) > 0 for page in doc),
    }
    if "Alpine" in path.name:
        checks["stanislaus"] = "Stanislaus County" in full
        checks["usmani_family"] = "Usmani family" in full
        checks["no_osmani"] = "Osmani" not in full
        checks["no_pending_reserve_name"] = "Pending Valid Re-Service" not in path.name
    if "Diamond" in path.name:
        checks["costs_waived_language"] = "waives costs" in full.lower() or "Costs waived" in full or "item 7f" in full
        checks["no_concurrent_mc010"] = "filing concurrently" not in full.lower()
    print(f"Verify {path.name}:")
    for k, ok in checks.items():
        print(f"  {'OK' if ok else 'FAIL'}: {k}")
    if expect_mc010 is False and "MC-010);" in full and "no Memorandum" not in full:
        print("  WARN: residual MC-010 companion-list language may remain")
    # Ensure CIV-100 item 2 region shows inserted amounts (page index 1).
    p = doc[1]
    text = p.get_text()
    print(f"  CIV-100 page text contains demand {DEMAND}: {DEMAND in text}")
    print(f"  pages={doc.page_count} images_on_civ_p1={len(doc[1].get_images())}")
    doc.close()


def main() -> None:
    if not SIGNATURE_IMG.is_file():
        raise SystemExit(f"Missing signature image: {SIGNATURE_IMG}")
    if not DIAMOND_SRC.is_file() or DIAMOND_SRC.stat().st_size < 10_000:
        raise SystemExit(f"Bad/missing Diamond source packet: {DIAMOND_SRC}")
    if not ALPINE_SRC.is_file() or ALPINE_SRC.stat().st_size < 10_000:
        raise SystemExit(f"Bad/missing Alpine source packet: {ALPINE_SRC}")

    diamond_decl, alpine_decl = run_declarations()

    backup_dir = Path("/tmp/m12build")
    backup_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(DIAMOND_SRC, backup_dir / "backup_Diamond_packet_pre_fix.pdf")
    shutil.copy2(ALPINE_SRC, backup_dir / "backup_Alpine_packet_pre_fix.pdf")

    assemble(DIAMOND_SRC, DIAMOND_RANGES, diamond_decl, DIAMOND_OUT)
    assemble(ALPINE_SRC, ALPINE_RANGES, alpine_decl, ALPINE_OUT)

    # Remove superseded Alpine filename if still present in the docs folder.
    if _ALPINE_LEGACY.exists() and _ALPINE_LEGACY.resolve() != ALPINE_OUT.resolve():
        _ALPINE_LEGACY.unlink()
        print(f"Removed superseded {_ALPINE_LEGACY.name}")

    verify(DIAMOND_OUT)
    verify(ALPINE_OUT)

    # Clean temporary declaration/build backups from public docs? Keep build
    # decls for audit; delete only .tmp if any remain.
    for tmp in OUT_DIR.glob("*.tmp.pdf"):
        tmp.unlink()


if __name__ == "__main__":
    main()
