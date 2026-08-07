#!/usr/bin/env python3
"""Fill the N.D. Cal. intake packet for Nforbi v. Meza-Gonzalez (Matter 32).

Companion filings to the August 7, 2026 Complaint for Damages (42 U.S.C.
§ 1983) at documents/matter-32/:

- JS 44 Civil Cover Sheet (Rev. 03/24)
- AO 440 Summons in a Civil Action — one per served Defendant
  (Meza-Gonzalez, Melano; DOES 1-10 are not served)
- Consent or Declination to Magistrate Judge Jurisdiction (N.D. Cal., 10/2020)

Every value traces to the complaint: caption and parties from the caption
block and ¶¶ 12-15, plaintiff's address from the caption, jurisdiction from
¶ 9, and the related Serrato action from ¶¶ 50-52. The one exception is the
service address on each summons, which is the officer's current duty station
rather than the November 2024 Dublin assignment pleaded at ¶¶ 13-14.

Left deliberately blank, because the court fills them in: the civil action
number on both summonses, the clerk's date/signature block, the case number
on the consent form, the JS 44 "FOR OFFICE USE ONLY" strip, and the entire
AO 440 proof-of-service page (completed by the process server after service).
"""

from __future__ import annotations

import io
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from pypdf.generic import (
    ArrayObject,
    DecodedStreamObject,
    DictionaryObject,
    FloatObject,
    NameObject,
    NumberObject,
    TextStringObject,
)

ROOT = Path(__file__).resolve().parents[2]
FORMS = ROOT / "internal/public/documents/_form-library"
OUT_DIR = ROOT / "internal/public/documents/matter-32"

JS44_TEMPLATE = FORMS / "js44-civil-cover-sheet-blank-template.pdf"
AO440_TEMPLATE = FORMS / "ao440-summons-blank-template.pdf"
CONSENT_TEMPLATE = FORMS / "ndcal-magistrate-consent-declination-blank-template.pdf"

# ---------------------------------------------------------------- case facts

PLAINTIFF = "BRENDAN NGWA NFORBI"
PLAINTIFF_MIXED = "Brendan Ngwa Nforbi"
PLAINTIFF_COUNTY = "San Joaquin"
PLAINTIFF_ADDRESS = "1455 Cat Tail Drive"
PLAINTIFF_CITY_LINE = "Stockton, CA 95204"
PHONE = "(209) 801-4442"
EMAIL = "bnn.cdl@gmail.com"

# Complaint caption + ¶¶ 13-15.
DEFENDANTS_BLOCK = (
    "SANTIAGO MEZA-GONZALEZ (CHP Badge #023295), in his individual capacity; "
    "JOSE MELANO (CHP Badge #023054), in his individual capacity; and "
    "DOES 1 through 10, inclusive"
)
# The JS 44 caption box is a two-line field — same parties, tighter.
DEFENDANTS_SHORT = (
    "SANTIAGO MEZA-GONZALEZ (CHP #023295) and JOSE MELANO (CHP #023054), "
    "each in his individual capacity; and DOES 1-10"
)

# Current duty stations, per Plaintiff. These are not the CHP Dublin Area
# office the Complaint pleads at ¶¶ 13-14 — Dublin is where both officers
# were assigned on November 1, 2024; each has since moved to a different
# Area office, and a summons has to reach the officer where he is now.
CHP_MODESTO = ["California Highway Patrol, Modesto Area", "4030 Kiernan Avenue", "Modesto, CA 95356"]
CHP_SOUTH_SACRAMENTO = [
    "California Highway Patrol, South Sacramento Area",
    "6 Massie Court",
    "Sacramento, CA 95823",
]

# Both signature lines are left empty; Plaintiff signs by hand.
FILING_DATE = "08/07/2026"
CONSENT_DATE = "August 7"
CONSENT_YEAR = "26"

# Complaint ¶¶ 50-52. The order at Dkt. 4 in that case names the assigned
# judge as the Hon. Ajay Krishnan; the complaint's "Ambadas S. Krishnan"
# appears to be a drafting slip. The cover sheet follows the docket.
RELATED_JUDGE = "Hon. Ajay S. Krishnan (Oakland Div.)"
RELATED_DOCKET = "4:26-cv-05953-ASK"

DEFENDANTS_TO_SERVE = [
    {
        "slug": "Santiago Meza-Gonzalez",
        "filename": "AO 440 Summons - Santiago Meza-Gonzalez (N.D. Cal.) (Aug 7 2026).pdf",
        "address": ["Officer Santiago Meza-Gonzalez (Badge #023295)", *CHP_MODESTO],
        "proof_of_service_name": "Officer Santiago Meza-Gonzalez, California Highway Patrol",
    },
    {
        "slug": "Jose Melano",
        "filename": "AO 440 Summons - Jose Melano (N.D. Cal.) (Aug 7 2026).pdf",
        "address": ["Officer Jose Melano (Badge #023054)", *CHP_SOUTH_SACRAMENTO],
        "proof_of_service_name": "Officer Jose Melano, California Highway Patrol",
    },
]

JS44_NAME = "JS 44 Civil Cover Sheet - Nforbi v. Meza-Gonzalez (N.D. Cal.) (Aug 7 2026).pdf"
CONSENT_NAME = (
    "Consent to Magistrate Judge Jurisdiction - "
    "Nforbi v. Meza-Gonzalez (N.D. Cal.) (Aug 7 2026).pdf"
)
PACKET_NAME = (
    "N.D. Cal. Intake Packet (print copy) - "
    "Nforbi v. Meza-Gonzalez (Aug 7 2026).pdf"
)

# ------------------------------------------------------------ field mappings

# JS 44 (Rev. 03/24). Radio-group export values were read off the widget
# rectangles against the printed labels; the comments record what each picks.
JS = "topmostSubform[0].Page1[0]"
JS44_FIELDS: dict[str, object] = {
    f"{JS}.plaintiffs[0]": PLAINTIFF,
    f"{JS}.defendants[0]": DEFENDANTS_SHORT,
    f"{JS}.plCty[0]": PLAINTIFF_COUNTY,
    # defCty[0] is "IN U.S. PLAINTIFF CASES ONLY" — left blank.
    f"{JS}.attorneysPL[0]": (
        f"{PLAINTIFF_MIXED}, Pro Se (In Propria Persona)\n"
        f"{PLAINTIFF_ADDRESS}, {PLAINTIFF_CITY_LINE}\n"
        f"Tel: {PHONE}; E-mail: {EMAIL}"
    ),
    # attorneysDef[0]: none appeared — left blank.
    f"{JS}.q2[0]": NameObject("/2"),  # II. Basis of jurisdiction: 3 Federal Question
    # III. Citizenship of principal parties is for diversity cases only — blank.
    f"{JS}.q4[0]": NameObject("/35"),  # IV. Nature of suit: 440 Other Civil Rights
    f"{JS}.q5[0]": NameObject("/0"),  # V. Origin: 1 Original Proceeding
    f"{JS}.S6stat[0]": (
        "42 U.S.C. § 1983 (jurisdiction: 28 U.S.C. §§ 1331, 1343(a)(3), (a)(4)); "
        "U.S. Const. amends. I, IV, XIV"
    ),
    f"{JS}.S6cause[0]": (
        "Warrantless vehicle entry and search, arrest without probable cause, "
        "judicial deception, fabricated evidence, and retaliatory arrest."
    ),
    f"{JS}.S7demand[0]": "According to proof",
    f"{JS}.jury[0]": NameObject("/0"),  # VII. Jury demand: Yes (Complaint, Rule 38 demand)
    f"{JS}.S8judge[0]": RELATED_JUDGE,
    f"{JS}.S8docket[0]": RELATED_DOCKET,
    f"{JS}.date[0]": FILING_DATE,
    # sig[0] stays empty — Plaintiff signs the cover sheet by hand.
}

# The caption boxes hold more text than fits at the template's 10 pt default:
# the defendant list wraps to two lines, the pro se contact block to three.
JS44_FONT_OVERRIDES = {
    f"{JS}.defendants[0]": "/ArialMT 8.00 Tf 0 g",
    f"{JS}.attorneysPL[0]": "/ArialMT 7.00 Tf 0 g",
}

# AO 440 district dropdown — must match the /Opt string byte for byte.
AO440_DISTRICT = "        Northern District of California"

# The template's "Plaintiff address" box starts 8.3 pt above the top of
# "whose name and address are:" (that sentence sits at y=289.6-300.5) and
# ends 1.6 pt above "If you fail to respond..." (y=216.1) below it — so the
# name block rendered flush against both neighbors, with "Brendan Ngwa
# Nforbi" crowding the sentence above it. Shrink the box to y=219-286,
# clearing both lines by a few points, and drop the font to 9 pt so five
# lines still fit comfortably in the smaller box.
AO440_PLAINTIFF_ADDRESS_RECT = (219.0, 286.0)  # (bottom, top); left/right unchanged
AO440_FONT_OVERRIDES = {"Plaintiff address": "/Helv 9.00 Tf 0 g"}

CONSENT_FIELDS: dict[str, object] = {
    "Plaintiff Name(s)": PLAINTIFF,
    "Defendant Name(s)": "SANTIAGO MEZA-GONZALEZ, et al.",
    # "Case number" is assigned at filing — left blank, add it before filing.
    "Consent to Magistrate Judge Jurisdiction": NameObject("/On"),
    "DATE": CONSENT_DATE,
    "YEAR": CONSENT_YEAR,
    "NAME": PLAINTIFF_MIXED,
    # "sig" stays empty — Plaintiff signs this one by hand.
    "ProSe": "PRO SE",
}

# The signature-block fields on the consent form are short widgets sitting on
# top of printed rules, and a generated appearance drops the text a line-height
# too high — "August 7" floats above its rule and the year reads as a
# superscript on the preprinted "20". Every rule on that row shares a text
# baseline at y=227 (the printed "DATE:", "20" and "NAME:" all sit on it), and
# the "PRO SE" rule at y=161, so each value is drawn at that exact baseline in
# the form's own Times face instead.
CONSENT_BASELINES = {
    "DATE": 227.0,
    "YEAR": 227.0,
    "NAME": 227.0,
    "ProSe": 161.2,
}

# ------------------------------------------------------------------ plumbing


def fill(template: Path, out_path: Path, fields: dict[str, object], page_index: int = 0,
         font_overrides: dict[str, str] | None = None,
         baselines: dict[str, float] | None = None) -> Path:
    reader = PdfReader(str(template))
    writer = PdfWriter()
    writer.append(reader)
    writer.update_page_form_field_values(writer.pages[page_index], fields)
    for name, da in (font_overrides or {}).items():
        set_default_appearance(writer, name, da)
    for name, baseline in (baselines or {}).items():
        draw_on_baseline(writer, name, str(fields[name]), baseline)
    # A hand-placed appearance only survives if the viewer is not told to
    # rebuild every field itself, so /NeedAppearances goes off once we have
    # drawn the values ourselves.
    writer.set_need_appearances_writer(not baselines)
    with open(out_path, "wb") as fh:
        writer.write(fh)
    return out_path


def draw_on_baseline(writer: PdfWriter, field_name: str, text: str, baseline: float,
                     font: str = "/TiRo", size: float = 12.0, left_pad: float = 2.0) -> None:
    """Replace a field's appearance with one drawn at an absolute page baseline."""
    fonts = writer._root_object["/AcroForm"]["/DR"]["/Font"]
    escaped = text.replace("\\", r"\\").replace("(", r"\(").replace(")", r"\)")
    for page in writer.pages:
        for annot in page.get("/Annots") or []:
            obj = annot.get_object()
            if str(obj.get("/T")) != field_name:
                continue
            x0, y0, x1, y1 = (float(v) for v in obj["/Rect"])
            stream = DecodedStreamObject()
            stream.set_data(
                f"/Tx BMC q BT {font} {size} Tf 0 g "
                f"{left_pad} {baseline - y0} Td ({escaped}) Tj ET Q EMC".encode("latin-1")
            )
            stream[NameObject("/Type")] = NameObject("/XObject")
            stream[NameObject("/Subtype")] = NameObject("/Form")
            stream[NameObject("/FormType")] = NumberObject(1)
            stream[NameObject("/BBox")] = ArrayObject(
                [FloatObject(0), FloatObject(0), FloatObject(x1 - x0), FloatObject(y1 - y0)]
            )
            resources = DictionaryObject()
            resources[NameObject("/Font")] = fonts
            stream[NameObject("/Resources")] = resources
            appearance = DictionaryObject()
            appearance[NameObject("/N")] = writer._add_object(stream)
            obj[NameObject("/AP")] = appearance


def set_default_appearance(writer: PdfWriter, qualified_name: str, da: str) -> None:
    """Rewrite one field's /DA so its value renders at a smaller size."""
    leaf = qualified_name.split(".")[-1]
    for page in writer.pages:
        for annot in page.get("/Annots") or []:
            obj = annot.get_object()
            if str(obj.get("/T")) == leaf:
                obj[NameObject("/DA")] = TextStringObject(da)


def set_field_rect(writer: PdfWriter, field_name: str, bottom: float, top: float) -> None:
    """Move a field's top/bottom edges, keeping its left/right edges as-is."""
    for page in writer.pages:
        for annot in page.get("/Annots") or []:
            obj = annot.get_object()
            if str(obj.get("/T")) != field_name:
                continue
            x0, _, x1, _ = (float(v) for v in obj["/Rect"])
            obj[NameObject("/Rect")] = ArrayObject(
                [FloatObject(x0), FloatObject(bottom), FloatObject(x1), FloatObject(top)]
            )


def fill_summons(defendant: dict) -> Path:
    fields: dict[str, object] = {
        "Dist.Info": AO440_DISTRICT,
        "Plaintiff": PLAINTIFF,
        "Defendant": DEFENDANTS_BLOCK,
        # "Civil action number", "Date_Today" and "Deputy Clerk Signature"
        # are the clerk's to complete when the summons issues.
        "Defendant address": "\n".join(defendant["address"]),
        # Phone and e-mail share one line — see AO440_PLAINTIFF_ADDRESS_RECT
        # above for why this box only has room for five lines, not six.
        "Plaintiff address": "\n".join(
            [PLAINTIFF_MIXED, "Plaintiff, In Pro Per", PLAINTIFF_ADDRESS,
             PLAINTIFF_CITY_LINE, f"Telephone: {PHONE} — E-mail: {EMAIL}"]
        ),
    }
    out_path = fill(AO440_TEMPLATE, OUT_DIR / defendant["filename"], fields,
                     font_overrides=AO440_FONT_OVERRIDES)
    reader = PdfReader(str(out_path))
    writer = PdfWriter()
    writer.append(reader)
    set_field_rect(writer, "Plaintiff address", *AO440_PLAINTIFF_ADDRESS_RECT)
    writer.set_need_appearances_writer(True)
    with open(out_path, "wb") as fh:
        writer.write(fh)
    # Page 2 is the proof of service; only the "summons for" line is known
    # in advance. The server completes the rest after service.
    reader = PdfReader(str(out_path))
    writer = PdfWriter()
    writer.append(reader)
    writer.update_page_form_field_values(
        writer.pages[1], {"Defendant2": defendant["proof_of_service_name"]}
    )
    writer.set_need_appearances_writer(True)
    with open(out_path, "wb") as fh:
        writer.write(fh)
    return out_path


def build_print_packet(sources: list[Path], out_path: Path) -> Path:
    """Flatten the filled forms into one print-ready PDF.

    The individual files stay live AcroForms so fields can still be edited
    (case number, clerk blocks, proof of service). Flattening bakes the
    values into the page content so nothing depends on the printer's PDF
    viewer honoring /NeedAppearances.
    """
    import pypdfium2 as pdfium

    writer = PdfWriter()
    for source in sources:
        doc = pdfium.PdfDocument(str(source))
        doc.init_forms()
        for page in doc:
            page.flatten()
        buffer = io.BytesIO()
        doc.save(buffer)
        buffer.seek(0)
        writer.append(PdfReader(buffer))
    with open(out_path, "wb") as fh:
        writer.write(fh)
    return out_path


def report(path: Path) -> None:
    fields = PdfReader(str(path)).get_fields() or {}
    filled = {
        name: field.get("/V")
        for name, field in fields.items()
        if field.get("/V") not in (None, "", "/Off")
    }
    print(f"\n{path.name}: {len(filled)} filled field(s)")
    for name, value in filled.items():
        flat = str(value).replace("\n", " | ")
        print(f"  {name.split('.')[-1]}: {flat[:96]}")


def main() -> None:
    for template in (JS44_TEMPLATE, AO440_TEMPLATE, CONSENT_TEMPLATE):
        if not template.is_file():
            raise SystemExit(f"Missing template: {template}")
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    outputs = [
        fill(JS44_TEMPLATE, OUT_DIR / JS44_NAME, JS44_FIELDS,
             font_overrides=JS44_FONT_OVERRIDES),
        *[fill_summons(defendant) for defendant in DEFENDANTS_TO_SERVE],
        fill(CONSENT_TEMPLATE, OUT_DIR / CONSENT_NAME, CONSENT_FIELDS,
             baselines=CONSENT_BASELINES),
    ]
    for path in outputs:
        report(path)
    packet = build_print_packet(outputs, OUT_DIR / PACKET_NAME)
    print(f"\n{packet.name}: {len(PdfReader(str(packet)).pages)} flattened page(s)")
    print("\nDone.")


if __name__ == "__main__":
    main()
