#!/usr/bin/env python3
"""Fill the N.D. Cal. intake packet for Ngwa Nforbi v. Candelaria & Gordon (Matter 33).

Companion filings to the August 7, 2026 Complaint for Damages and for
Declaratory and Injunctive Relief (42 U.S.C. § 1983; 28 U.S.C. §§ 2201, 2202;
Ex parte Young) at documents/matter-33/:

- JS 44 Civil Cover Sheet (Rev. 03/24)
- AO 440 Summons in a Civil Action — one per Defendant (Candelaria, Gordon;
  DOES 1-10 are not served)
- Consent or Declination to Magistrate Judge Jurisdiction (N.D. Cal., 10/2020)

Matter 33 is the N.D. Cal. counterpart to Matter 7 (Newanforbi v. Candelaria,
E.D. Cal., 2:26-cv-00983-DC-CSK) — the same relationship Matter 32 has to
Matters 1/2 for the CHP officers. Same plaintiff, same two defendants, new
caption and new district.

Every value traces to the complaint: caption and parties from the caption
block and ¶¶ 15-19, plaintiff's address from the caption, jurisdiction from
¶ 10, venue from ¶¶ 12-13, and the related Serrato action from ¶ 8. The
service address for both defendants is the DMV's Legal Affairs Division at
Sacramento headquarters (Cal. Vehicle Code service-of-process practice) —
the complaint itself gives no office address for Candelaria; her January 24,
2025 hearing was conducted remotely over Microsoft Teams.

Left deliberately blank, because the court fills them in: the civil action
number on both summonses, the clerk's date/signature block, the case number
on the consent form, the JS 44 "FOR OFFICE USE ONLY" strip, and the entire
AO 440 proof-of-service page (completed by the process server after service).
Both the JS 44 and consent-form signature lines are also left blank —
Plaintiff signs both by hand.
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
OUT_DIR = ROOT / "internal/public/documents/matter-33/ndcal"

JS44_TEMPLATE = FORMS / "js44-civil-cover-sheet-blank-template.pdf"
AO440_TEMPLATE = FORMS / "ao440-blank-template.pdf"
CONSENT_TEMPLATE = FORMS / "ndcal-mj-consent-declination-blank-template.pdf"

# ---------------------------------------------------------------- case facts

PLAINTIFF = "BRENDAN NGWA NFORBI"
PLAINTIFF_MIXED = "Brendan Ngwa Nforbi"
PLAINTIFF_COUNTY = "San Joaquin"
PLAINTIFF_ADDRESS = "1455 Cat Tail Drive"
PLAINTIFF_CITY_LINE = "Stockton, CA 95204"
PHONE = "(209) 801-4442"
EMAIL = "bnn.cdl@gmail.com"

# Complaint caption + ¶¶ 16-17.
DEFENDANTS_BLOCK = (
    "DIANA CANDELARIA, in her individual capacity; and STEVE GORDON, "
    "Director of the California Department of Motor Vehicles, in his "
    "official capacity; and DOES 1 through 10, inclusive"
)
# The JS 44 caption box is a two-line field — same parties, tighter.
DEFENDANTS_SHORT = (
    "DIANA CANDELARIA, individually; and STEVE GORDON, Director, CA DMV, "
    "in his official capacity; and DOES 1-10"
)

# Service address for both Defendants. The complaint gives no office
# address for Candelaria (her hearing was conducted remotely), so this uses
# the DMV's own published address for service of process on the Department
# / Director's office — the same address applies to Gordon as Director.
DMV_LEGAL_AFFAIRS = [
    "California Department of Motor Vehicles",
    "Legal Affairs Division, Mail Station C128",
    "2415 First Avenue",
    "Sacramento, CA 95818",
]

# Both signature lines are left empty; Plaintiff signs by hand.
FILING_DATE = "08/07/2026"
CONSENT_DATE = "August 7"
CONSENT_YEAR = "26"

# Complaint ¶ 8. Same related Serrato action cited in the Meza-Gonzalez
# intake packet (Matter 32) — Judge Krishnan's June 29, 2026 screening order
# is the concrete, already-docketed related case; the Meza-Gonzalez
# complaint itself (Matter 32) has no case number yet to cite here.
RELATED_JUDGE = "Hon. Ajay S. Krishnan (Oakland Div.)"
RELATED_DOCKET = "4:26-cv-05953-ASK"

DEFENDANTS_TO_SERVE = [
    {
        "slug": "Diana Candelaria",
        "filename": "AO 440 Summons - Diana Candelaria (N.D. Cal.) (Aug 7 2026).pdf",
        "address": ["Diana Candelaria, Driver Safety Hearing Officer",
                     "California Department of Motor Vehicles", *DMV_LEGAL_AFFAIRS[1:]],
        "proof_of_service_name": "Diana Candelaria, California DMV Driver Safety Hearing Officer",
    },
    {
        "slug": "Steve Gordon",
        "filename": "AO 440 Summons - Steve Gordon (N.D. Cal.) (Aug 7 2026).pdf",
        "address": ["Steve Gordon, Director", *DMV_LEGAL_AFFAIRS],
        "proof_of_service_name": "Steve Gordon, Director, California DMV (official capacity)",
    },
]

JS44_NAME = "JS 44 Civil Cover Sheet - Ngwa Nforbi v. Candelaria & Gordon (N.D. Cal.) (Aug 7 2026).pdf"
CONSENT_NAME = (
    "Consent to Magistrate Judge Jurisdiction - "
    "Ngwa Nforbi v. Candelaria & Gordon (N.D. Cal.) (Aug 7 2026).pdf"
)
PACKET_NAME = (
    "N.D. Cal. Intake Packet (print copy) - "
    "Ngwa Nforbi v. Candelaria & Gordon (Aug 7 2026).pdf"
)

# ------------------------------------------------------------ field mappings

# JS 44 (Rev. 03/24). Radio-group export values were read off the widget
# rectangles against the printed labels for the Meza-Gonzalez packet
# (Matter 32) and carry over unchanged — same template, same choices for
# jurisdiction/nature-of-suit/origin/jury.
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
        "42 U.S.C. § 1983; 28 U.S.C. §§ 2201, 2202 (jurisdiction: 28 U.S.C. §§ 1331, "
        "1343(a)(3), (a)(4)); U.S. Const. amend. XIV"
    ),
    f"{JS}.S6cause[0]": (
        "Structural bias, denial of a fair hearing, and lack of jurisdiction in a "
        "DMV license-suspension hearing; declaratory and injunctive relief."
    ),
    # Prayer (¶¶ A.1-2) seeks not less than $150,000 compensatory and not
    # less than $100,000 punitive against Candelaria — a $250,000 floor,
    # not a verbatim figure from the complaint.
    f"{JS}.S7demand[0]": "$250,000 (min.)",
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
# "whose name and address are:" and ends 1.6 pt above "If you fail to
# respond..." below it, so a full-height block renders flush against both
# neighbors (see Matter 32's Aug. 7, 2026 fix). Shrink the box to y=219-286
# and drop the font to 9 pt so five lines still fit with clearance on both
# sides.
AO440_PLAINTIFF_ADDRESS_RECT = (219.0, 286.0)  # (bottom, top); left/right unchanged
AO440_FONT_OVERRIDES = {"Plaintiff address": "/Helv 9.00 Tf 0 g"}

CONSENT_FIELDS: dict[str, object] = {
    "Plaintiff Name(s)": PLAINTIFF,
    "Defendant Name(s)": "DIANA CANDELARIA, et al.",
    # "Case number" is assigned at filing — left blank, add it before filing.
    "Consent to Magistrate Judge Jurisdiction": NameObject("/On"),
    "DATE": CONSENT_DATE,
    "YEAR": CONSENT_YEAR,
    "NAME": PLAINTIFF_MIXED,
    # "sig" stays empty — Plaintiff signs this one by hand.
    "ProSe": "PRO SE",
}

# The signature-block fields on the consent form are short widgets sitting on
# top of printed rules, and a generated appearance drops the text a
# line-height too high (see Matter 32's Aug. 7, 2026 fix). Every rule on the
# DATE/NAME row shares a text baseline at y=227, and the "PRO SE" rule at
# y=161, so each value is drawn at that exact baseline in the form's own
# Times face instead.
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
        # Phone and e-mail share one line — the shrunk box only has room
        # for five lines, not six.
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
