#!/usr/bin/env python3
"""E.D. Cal. magistrate-judge consents for Matters 36–39.

Fills the court's consent/decline web form (consentmagweb) for the four
unfiled walk-up packets being mailed September 16, 2026. House practice
is CONSENT. Case number is left blank for the clerk. No proof of service
— these go in the Sacramento clerk envelope, not to the defendants.

  python3 internal/scripts/matter36-39-edca-mj-consents.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import pymupdf

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR / "lib"))
sys.path.insert(0, str(SCRIPT_DIR))

from pdf_packet import assemble  # noqa: E402
from short_link import publish_short_link  # noqa: E402
from signature_stamp import SIGNATURE_PATH, stamp_on_pdf_line  # noqa: E402

ROOT = SCRIPT_DIR.parents[1]
SRC = (
    ROOT
    / "internal/public/documents/_form-library"
    / "edcal-mj-consent-declination-blank-template.pdf"
)
DOCS = ROOT / "internal/public/documents"

EXEC_DATE = "September 16, 2026"
PRINT_NAME = "BRENDAN NGWA NFORBI"

SIG_LINE = (320.0, 487.4, 444.0)
CONSENT_PLTF_RADIO = (311.4, 476.0, 318.6, 483.2)
CONSENT_DFT_RADIO = (401.6, 476.2, 408.8, 483.4)

CASES = [
    {
        "matter": 36,
        "defendant": "AT&T MOBILITY SERVICES LLC",
        "short": "AT&T",
        "slug": "edca-att-consent",
        "filename": (
            "Consent to Magistrate Judge Jurisdiction - "
            "Ngwa Nforbi v. AT&T Mobility Services LLC "
            "(E.D. Cal.) (Sep 16 2026).pdf"
        ),
    },
    {
        "matter": 37,
        "defendant": "HOME DEPOT U.S.A., INC.",
        "short": "Home Depot",
        "slug": "edca-home-depot-consent",
        "filename": (
            "Consent to Magistrate Judge Jurisdiction - "
            "Ngwa Nforbi v. Home Depot U.S.A., Inc. "
            "(E.D. Cal.) (Sep 16 2026).pdf"
        ),
    },
    {
        "matter": 38,
        "defendant": "SWIFT TRANSPORTATION CO. OF ARIZONA LLC",
        "short": "Swift",
        "slug": "edca-swift-consent",
        "filename": (
            "Consent to Magistrate Judge Jurisdiction - "
            "Ngwa Nforbi v. Swift Transportation Co. of Arizona LLC "
            "(E.D. Cal.) (Sep 16 2026).pdf"
        ),
    },
    {
        "matter": 39,
        "defendant": "BEST BUY CO., INC.",
        "short": "Best Buy",
        "slug": "edca-best-buy-consent",
        "filename": (
            "Consent to Magistrate Judge Jurisdiction - "
            "Ngwa Nforbi v. Best Buy Co., Inc. "
            "(E.D. Cal.) (Sep 16 2026).pdf"
        ),
    },
]


def _paint_consent_plaintiff_radio(page) -> None:
    dft = pymupdf.Rect(*CONSENT_DFT_RADIO)
    dft_c = pymupdf.Point((dft.x0 + dft.x1) / 2, (dft.y0 + dft.y1) / 2)
    page.draw_circle(dft_c, dft.width / 2 + 0.6, color=(1, 1, 1), fill=(1, 1, 1), width=0)
    page.draw_circle(dft_c, 3.2, color=(0, 0, 0), fill=None, width=0.6)
    pltf = pymupdf.Rect(*CONSENT_PLTF_RADIO)
    pltf_c = pymupdf.Point((pltf.x0 + pltf.x1) / 2, (pltf.y0 + pltf.y1) / 2)
    page.draw_circle(pltf_c, 2.15, color=(0, 0, 0), fill=(0, 0, 0), width=0)


def _parent_xref(doc, kid_xref: int) -> int | None:
    m = re.search(r"/Parent (\d+) 0 R", doc.xref_object(kid_xref))
    return int(m.group(1)) if m else None


def fill_consent(out: Path, defendant: str) -> Path:
    if not Path(SIGNATURE_PATH).is_file():
        raise SystemExit(f"Missing universal signature: {SIGNATURE_PATH}")
    if not SRC.is_file() or SRC.stat().st_size < 10_000:
        raise SystemExit(f"Missing court form: {SRC}")

    doc = pymupdf.open(SRC)
    page = doc[0]
    g6_parent = g7_parent = None
    defendant_size = 8 if len(defendant) > 34 else 9

    for w in page.widgets():
        name = w.field_name
        if name == "PlaintiffsPetitioners":
            w.text_fontname = "tiro"
            w.text_fontsize = 9
            w.field_value = PRINT_NAME
        elif name == "CASE NO":
            w.field_value = ""
        elif name == "DefendantsRespondents":
            w.text_fontname = "tiro"
            w.text_fontsize = defendant_size
            w.field_value = defendant
        elif name == "Consent Check":
            w.field_value = w.on_state()
        elif name == "Decline Check":
            w.field_value = "Off"
        elif name == "Date":
            w.text_fontname = "tiro"
            w.text_fontsize = 10
            w.field_value = EXEC_DATE
        elif name == "Print Name":
            w.text_fontname = "tiro"
            w.text_fontsize = 9
            w.field_value = PRINT_NAME
        elif name == "Group6":
            w.field_value = "Pltf" if w.on_state() == "Pltf" else "Off"
            g6_parent = _parent_xref(doc, w.xref)
        elif name == "Group7":
            w.field_value = "Off"
            g7_parent = _parent_xref(doc, w.xref)
        elif w.field_type_string == "Text":
            w.field_value = ""
        w.update()

    for w in page.widgets():
        if w.field_name == "Group6":
            doc.xref_set_key(
                w.xref, "AS", "/Pltf" if w.on_state() == "Pltf" else "/Off"
            )
        elif w.field_name == "Group7":
            doc.xref_set_key(w.xref, "AS", "/Off")
    if g6_parent:
        doc.xref_set_key(g6_parent, "V", "/Pltf")
    if g7_parent:
        doc.xref_set_key(g7_parent, "V", "/Off")

    doc.bake(annots=True, widgets=True)
    _paint_consent_plaintiff_radio(page)
    stamp_on_pdf_line(page, SIG_LINE[0], SIG_LINE[1], SIG_LINE[2], whiteout=False)

    out.parent.mkdir(parents=True, exist_ok=True)
    doc.save(out, garbage=4, deflate=True)
    doc.close()
    return out


def main() -> None:
    written: list[Path] = []
    for case in CASES:
        out = DOCS / f"matter-{case['matter']}" / "edca" / case["filename"]
        fill_consent(out, case["defendant"])
        publish_short_link(out, case["slug"])
        written.append(out)
        print(f"OK matter {case['matter']} {case['short']}: {out}")

    combo = DOCS / (
        "matter-36/edca/Consent to Magistrate Judge Jurisdiction - "
        "Matters 36-39 (E.D. Cal.) (Sep 16 2026).pdf"
    )
    assemble(written, combo)
    publish_short_link(combo, "edca-mj-consents")
    print(f"OK print set: {combo}")
    print("Put one consent in each Sacramento envelope. Do not serve defendants.")
    print("Case number is blank for the clerk. CONSENT is checked.")


if __name__ == "__main__":
    main()
