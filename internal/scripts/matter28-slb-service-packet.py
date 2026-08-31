#!/usr/bin/env python3
"""Matter 28 — SLB counsel-acceptance Rule 4 service packet.

Newanforbi v. Shannon Smith, LCSW, et al., N.D. Cal. No. 3:26-cv-07504-LJC.

Blaze Van Dine (Sims, Lawrence & Broghammer) stated during meet-and-confer that
SLB would accept service on behalf of Shannon Smith and HOPE Psychotherapy,
Inc. This packet assembles the papers to transmit by email (with
slb-eservice@sims-law.net on the To/Cc line) and the forms needed to file
proof after counsel confirms acceptance in writing.

Outputs under internal/public/documents/matter-28/service-packet-slb/:
  00_Cover_Sheet.pdf
  01_Acknowledgment_of_Acceptance_of_Service.pdf
  02_AO_440_Summons_Shannon_Smith.pdf
  03_AO_440_Summons_HOPE_Psychotherapy.pdf
  04_Complaint_as_filed.pdf  (copy)
  05_Dkt_11_Order_Directing_Service.pdf  (copy)
  06_Proof_of_Service_Electronic_Delivery_to_SLB.pdf
  EMAIL_DRAFT_Service_on_SLB.txt
  COMPLETE_Service_Packet_SLB_Acceptance.pdf  (assembled)
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

from pypdf.generic import (
    ArrayObject,
    FloatObject,
    NameObject,
    TextStringObject,
)
from pypdf import PdfReader, PdfWriter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR / "lib"))
from pdf_packet import assemble  # noqa: E402
from proof_of_service import (  # noqa: E402
    DISTRICT_NDCAL,
    ProofOfServiceFields,
    build_proof_of_service,
)

ROOT = Path(__file__).resolve().parents[2]
M28 = ROOT / "internal/public/documents/matter-28"
OUT = M28 / "service-packet-slb"
FORMS = ROOT / "internal/public/documents/_form-library"
AO440_TEMPLATE = FORMS / "ao440-blank-template.pdf"

COMPLAINT_SRC = M28 / (
    "Complaint_Newanforbi_v_Smith_NDCA (as filed, served on SLB Jul 22 2026).pdf"
)
DKT11_SRC = M28 / (
    "Dkt 11 - Order Regarding Filing Fee IFP and Directing Service (Filed Aug 26 2026).pdf"
)

CASE = "3:26-cv-07504-LJC"
PLAINTIFF = "BRENDAN NGEHSI NEWANFORBI"
PLAINTIFF_MIXED = "Brendan Ngehsi Newanforbi"
PLAINTIFF_ADDRESS = "1455 Cat Tail Drive"
PLAINTIFF_CITY = "Stockton, CA 95204"
PHONE = "(209) 801-4442"
EMAIL = "bnn.cdl@gmail.com"

DEFENDANTS_BLOCK = (
    "SHANNON SMITH, LCSW, Chief Executive Officer and Founder of HOPE Program, "
    "an individual; and HOPE PSYCHOTHERAPY, INC., d/b/a HOPE PROGRAM, "
    "a California corporation"
)

AO440_DISTRICT = "        Northern District of California"
AO440_PLAINTIFF_ADDRESS_RECT = (219.0, 286.0)
AO440_FONT_OVERRIDES = {"Plaintiff address": "/Helv 9.00 Tf 0 g"}

DEFENDANTS = [
    {
        "filename": "02_AO_440_Summons_Shannon_Smith.pdf",
        "address": [
            "Shannon Smith, LCSW, Chief Executive Officer",
            "HOPE Psychotherapy, Inc. d/b/a HOPE Program",
            "1245 B Street",
            "Hayward, CA 94541",
        ],
        "proof_of_service_name": "Shannon Smith, LCSW, CEO — HOPE Program",
    },
    {
        "filename": "03_AO_440_Summons_HOPE_Psychotherapy.pdf",
        "address": [
            "HOPE Psychotherapy, Inc. d/b/a HOPE Program",
            "c/o Shannon Smith, LCSW, Chief Executive Officer",
            "1245 B Street",
            "Hayward, CA 94541",
        ],
        "proof_of_service_name": "HOPE Psychotherapy, Inc. d/b/a HOPE Program",
    },
]


def set_default_appearance(writer: PdfWriter, qualified_name: str, da: str) -> None:
    leaf = qualified_name.split(".")[-1]
    for page in writer.pages:
        for annot in page.get("/Annots") or []:
            obj = annot.get_object()
            if str(obj.get("/T")) == leaf:
                obj[NameObject("/DA")] = TextStringObject(da)


def set_field_rect(writer: PdfWriter, field_name: str, bottom: float, top: float) -> None:
    for page in writer.pages:
        for annot in page.get("/Annots") or []:
            obj = annot.get_object()
            if str(obj.get("/T")) != field_name:
                continue
            x0, _, x1, _ = (float(v) for v in obj["/Rect"])
            obj[NameObject("/Rect")] = ArrayObject(
                [FloatObject(x0), FloatObject(bottom), FloatObject(x1), FloatObject(top)]
            )


def fill_form(template: Path, out_path: Path, fields: dict[str, object], page_index: int = 0,
              font_overrides: dict[str, str] | None = None) -> Path:
    reader = PdfReader(str(template))
    writer = PdfWriter()
    writer.append(reader)
    writer.update_page_form_field_values(writer.pages[page_index], fields)
    for name, da in (font_overrides or {}).items():
        set_default_appearance(writer, name, da)
    writer.set_need_appearances_writer(True)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "wb") as fh:
        writer.write(fh)
    return out_path


def fill_summons(defendant: dict) -> Path:
    fields: dict[str, object] = {
        "Dist.Info": AO440_DISTRICT,
        "Plaintiff": PLAINTIFF,
        "Defendant": DEFENDANTS_BLOCK,
        "Civil action number": CASE,
        "Defendant address": "\n".join(defendant["address"]),
        "Plaintiff address": "\n".join(
            [
                PLAINTIFF_MIXED,
                "Plaintiff, In Pro Per",
                PLAINTIFF_ADDRESS,
                PLAINTIFF_CITY,
                f"Telephone: {PHONE} — E-mail: {EMAIL}",
            ]
        ),
    }
    out_path = fill_form(
        AO440_TEMPLATE,
        OUT / defendant["filename"],
        fields,
        font_overrides=AO440_FONT_OVERRIDES,
    )
    reader = PdfReader(str(out_path))
    writer = PdfWriter()
    writer.append(reader)
    set_field_rect(writer, "Plaintiff address", *AO440_PLAINTIFF_ADDRESS_RECT)
    writer.set_need_appearances_writer(True)
    with open(out_path, "wb") as fh:
        writer.write(fh)

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


def write_cover(path: Path) -> None:
    c = canvas.Canvas(str(path), pagesize=letter)
    w, h = letter
    y = h - 54

    def line(text: str, size: float = 10, bold: bool = False, dy: float = 14) -> None:
        nonlocal y
        c.setFont("Helvetica-Bold" if bold else "Helvetica", size)
        c.drawString(54, y, text[:95])
        y -= dy

    line("RULE 4 SERVICE PACKET — COUNSEL ACCEPTANCE", 13, True, 18)
    line("Newanforbi v. Shannon Smith, LCSW, et al.", 11, True)
    line(f"U.S. District Court, N.D. Cal.  |  Case No. {CASE}  |  Hon. Lisa J. Cisneros", 10, True, 18)

    line("PURPOSE", 10, True)
    line("  Transmit process to Sims, Lawrence & Broghammer (Blaze Van Dine), who stated")
    line("  during meet-and-confer that SLB would accept service on behalf of both")
    line("  defendants. Include slb-eservice@sims-law.net on every service email.")
    y -= 6

    line("DEFENDANTS TO BE SERVED (via authorized counsel)", 10, True)
    line("  1. Shannon Smith, LCSW, CEO (individual capacity)")
    line("  2. HOPE Psychotherapy, Inc. d/b/a HOPE Program")
    line("  Principal office (defendants): 1245 B Street, Hayward, CA 94541")
    line("  Accepting counsel: Blaze Van Dine, Esq. — blaze@sims-law.net")
    line("  Firm e-service: slb-eservice@sims-law.net")
    y -= 6

    line("PACKET CONTENTS (this assembled PDF, in order)", 10, True)
    for item in [
        "1. This cover sheet",
        "2. Acknowledgment of Acceptance of Service (ask counsel to confirm in writing)",
        "3. AO 440 Summons — Shannon Smith (case no. filled; clerk stamp if issued)",
        "4. AO 440 Summons — HOPE Psychotherapy, Inc.",
        "5. Complaint (as filed / courtesy copy previously emailed Jul. 22, 2026)",
        "6. Dkt. 11 — Order directing Rule 4 service (filed Aug. 26, 2026)",
        "7. Proof of Service — Electronic Delivery to SLB (file after confirmation)",
    ]:
        line(f"  {item}")
    y -= 6

    line("IMPORTANT — ISSUED SUMMONS", 10, True)
    line("  Dkt. 3 on the early docket was a Proposed Summons. If CM/ECF now shows a")
    line("  clerk-ISSUED summons (stamped Date + Deputy Clerk), download those pages")
    line("  and substitute them for documents 3–4 before sending, or attach them as")
    line("  the controlling summonses. Do not rely on an unissued proposed summons")
    line("  alone if an issued copy is available.")
    y -= 6

    line("AFTER COUNSEL CONFIRMS ACCEPTANCE", 10, True)
    line("  1. Save the reply email (acceptance for both defendants, date certain).")
    line("  2. Complete / date the Proof of Service (document 7) and file it on CM/ECF.")
    line("  3. Calendar the Rule 12 response clock (typically 21 days from acceptance).")
    line(f"  4. Rule 4(m) outer window from complaint filing (~Jul. 20–21, 2026) ≈ Oct. 19, 2026.")
    y -= 8

    line(f"Prepared for Plaintiff {PLAINTIFF_MIXED}, In Propria Persona", 9)
    line(f"{PLAINTIFF_ADDRESS}, {PLAINTIFF_CITY}  |  {PHONE}  |  {EMAIL}", 9)
    c.save()


def write_acknowledgment(path: Path) -> None:
    c = canvas.Canvas(str(path), pagesize=letter)
    w, h = letter
    y = h - 54

    def line(text: str, size: float = 10, bold: bool = False, dy: float = 13) -> None:
        nonlocal y
        c.setFont("Helvetica-Bold" if bold else "Helvetica", size)
        c.drawString(54, y, text[:100])
        y -= dy

    def wrapped(text: str, size: float = 10, dy: float = 13, indent: float = 54) -> None:
        nonlocal y
        c.setFont("Helvetica", size)
        words = text.split()
        row = ""
        max_w = w - indent - 54
        for word in words:
            trial = (row + " " + word).strip()
            if c.stringWidth(trial, "Helvetica", size) <= max_w:
                row = trial
            else:
                c.drawString(indent, y, row)
                y -= dy
                row = word
        if row:
            c.drawString(indent, y, row)
            y -= dy

    line("ACKNOWLEDGMENT OF ACCEPTANCE OF SERVICE", 13, True, 18)
    line("Fed. R. Civ. P. 4 — service on authorized agent / counsel", 10, True, 16)
    line(f"{PLAINTIFF_MIXED} v. Shannon Smith, LCSW, et al.", 10, True)
    line(f"U.S. District Court, Northern District of California — Case No. {CASE}", 10, True, 16)

    wrapped(
        "I, Blaze Van Dine, Esq., of Sims, Lawrence & Broghammer, state that I am "
        "authorized to accept service of process on behalf of the defendants named "
        "below in the above-captioned action, and that I hereby accept service of "
        "the Summons and Complaint (and the enclosed Dkt. 11 Order) transmitted by "
        "email to blaze@sims-law.net and slb-eservice@sims-law.net."
    )
    y -= 4
    line("Defendants for whom service is accepted:", 10, True)
    line("  [ ]  Shannon Smith, LCSW (individual capacity)")
    line("  [ ]  HOPE Psychotherapy, Inc. d/b/a HOPE Program")
    line("  [ ]  Both of the above")
    y -= 6
    line("Date of acceptance (effective date of service): ________________________", 10, False, 18)
    line("Manner: Electronic mail (PDF attachments), pursuant to counsel’s agreement", 10, False, 18)
    line("to accept service on behalf of the clients during meet-and-confer.", 10, False, 18)

    wrapped(
        "I understand that this acknowledgment is intended to perfect service under "
        "Rule 4 and to start the time to answer or otherwise respond under Rule 12, "
        "and that Plaintiff may file this acknowledgment (or my confirming email) "
        "with a Proof of Service on the Court’s docket."
    )
    y -= 10
    line("Signature: ________________________________     Date: ______________", 10, False, 18)
    line("Printed name: Blaze Van Dine, Esq.", 10, False, 14)
    line("Sims, Lawrence & Broghammer", 10, False, 14)
    line("1478 Stone Point Drive, Suite 450, Roseville, CA 95661", 10, False, 14)
    line("(916) 797-8881  |  blaze@sims-law.net  |  slb-eservice@sims-law.net", 10, False, 18)

    line("Alternatively: a reply email stating that SLB accepts service for both", 9)
    line("defendants as of a stated date is sufficient; Plaintiff will file that reply", 9)
    line("with the Proof of Service.", 9)
    c.save()


def write_email_draft(path: Path) -> None:
    text = f"""To: blaze@sims-law.net; slb-eservice@sims-law.net
Cc: cynthia@sims-law.net; bryan@sims-law.net; kschmitt@sims-law.net; june@sims-law.net
Subject: Service of Process — Newanforbi v. Smith, et al., No. 3:26-cv-07504-LJC (N.D. Cal.)

Mr. Van Dine:

I write to effect service of process in Newanforbi v. Shannon Smith, LCSW, et al., United States District Court for the Northern District of California, Case No. {CASE}, Hon. Lisa J. Cisneros.

During our meet-and-confer, you stated that Sims, Lawrence & Broghammer would accept service on behalf of your clients in this action. Pursuant to that agreement, and consistent with Fed. R. Civ. P. 4 and this Court’s August 26, 2026 Order (Dkt. 11) directing service under Rule 4, please find attached a complete service packet containing:

  1. Cover sheet;
  2. Acknowledgment of Acceptance of Service (for your written confirmation);
  3. AO 440 Summons — Shannon Smith, LCSW;
  4. AO 440 Summons — HOPE Psychotherapy, Inc. d/b/a HOPE Program;
  5. Complaint (the same operative pleading previously transmitted as a courtesy copy on July 22, 2026);
  6. Dkt. 11 — Order Regarding Payment of Filing Fee / Directing Rule 4 Service (filed Aug. 26, 2026).

This email includes slb-eservice@sims-law.net as required by your firm’s electronic-service notice.

Please reply confirming that SLB accepts service on behalf of (1) Shannon Smith, LCSW, and (2) HOPE Psychotherapy, Inc. d/b/a HOPE Program, and stating the effective date of acceptance. You may sign and return the enclosed Acknowledgment, or confirm by reply email. Upon your confirmation I will file proof of service on the docket.

If the Clerk has issued stamped summonses that supersede the enclosed AO 440 forms, please treat those issued summonses as controlling; I will promptly transmit any stamped copies from CM/ECF if they differ from what is attached.

Thank you for your professional courtesy.

Respectfully,

Brendan Ngehsi Newanforbi
Plaintiff In Propria Persona
{PLAINTIFF_ADDRESS}
{PLAINTIFF_CITY}
Tel: {PHONE}
Email: {EMAIL}

Attachments:
  COMPLETE_Service_Packet_SLB_Acceptance.pdf
  (or the individual packet PDFs listed above)

---
Note to self (do not send): After Blaze confirms, date and file
06_Proof_of_Service_Electronic_Delivery_to_SLB.pdf with the confirmation
email attached as an exhibit if the clerk’s practice prefers it.
"""
    path.write_text(text, encoding="utf-8")


def write_proof_of_service(path: Path) -> None:
    # Leave service_date blank for plaintiff to fill after Blaze confirms.
    fields = ProofOfServiceFields(
        plaintiff_line=PLAINTIFF,
        defendant_lines=[
            "SHANNON SMITH, LCSW, et al.",
            "HOPE PSYCHOTHERAPY, INC.",
        ],
        case_number=CASE,
        title="PROOF OF SERVICE",
        service_date="",  # fill after acceptance
        document_title=(
            "Summons (AO 440) as to Shannon Smith, LCSW; Summons (AO 440) as to "
            "HOPE Psychotherapy, Inc. d/b/a HOPE Program; Complaint; and Dkt. 11 "
            "Order Regarding Payment of Filing Fee and Directing Service"
        ),
        mailing_location="Stockton, California (electronic mail)",
        recipients=[
            "Blaze Van Dine, Esq. — blaze@sims-law.net",
            "Sims, Lawrence & Broghammer e-service — slb-eservice@sims-law.net",
            "1478 Stone Point Drive, Suite 450, Roseville, CA 95661",
            "(Authorized to accept service for Shannon Smith, LCSW, and",
            "HOPE Psychotherapy, Inc., per counsel’s meet-and-confer agreement)",
        ],
        server_name=PLAINTIFF_MIXED,
        stamp_signature=False,
        district_line=DISTRICT_NDCAL,
    )
    build_proof_of_service(path, fields)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    assert AO440_TEMPLATE.is_file(), f"missing {AO440_TEMPLATE}"
    assert COMPLAINT_SRC.is_file(), f"missing {COMPLAINT_SRC}"
    assert DKT11_SRC.is_file(), f"missing {DKT11_SRC}"

    cover = OUT / "00_Cover_Sheet.pdf"
    ack = OUT / "01_Acknowledgment_of_Acceptance_of_Service.pdf"
    pos = OUT / "06_Proof_of_Service_Electronic_Delivery_to_SLB.pdf"
    email = OUT / "EMAIL_DRAFT_Service_on_SLB.txt"
    complaint_out = OUT / "04_Complaint_as_filed.pdf"
    dkt11_out = OUT / "05_Dkt_11_Order_Directing_Service.pdf"
    complete = OUT / "COMPLETE_Service_Packet_SLB_Acceptance.pdf"

    write_cover(cover)
    write_acknowledgment(ack)
    summons_paths = [fill_summons(d) for d in DEFENDANTS]
    shutil.copy2(COMPLAINT_SRC, complaint_out)
    shutil.copy2(DKT11_SRC, dkt11_out)
    write_proof_of_service(pos)
    write_email_draft(email)

    pages = assemble(
        [cover, ack, *summons_paths, complaint_out, dkt11_out, pos],
        complete,
    )
    print(f"Wrote {complete} ({pages} pages)")
    for p in sorted(OUT.iterdir()):
        print(f"  {p.name}  ({p.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
