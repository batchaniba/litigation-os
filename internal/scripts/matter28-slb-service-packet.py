#!/usr/bin/env python3
"""Matter 28 — SLB counsel-acceptance Rule 4 service packet.

Newanforbi v. Shannon Smith, LCSW, et al., N.D. Cal. No. 3:26-cv-07504-LJC.

Blaze Van Dine (Sims, Lawrence & Broghammer) stated during meet-and-confer that
SLB would accept service on behalf of Shannon Smith and HOPE Psychotherapy,
Inc. This packet transmits the clerk-issued AO 440 (Aug. 31, 2026, combined
form) with the complaint and Dkt. 11. Do not regenerate or restamp the issued
summons.

Outputs under internal/public/documents/matter-28/service-packet-slb/:
  00_Cover_Sheet.pdf  (plaintiff file only — not in COMPLETE)
  01_Acknowledgment_of_Acceptance_of_Service.pdf  (plaintiff file only — not in COMPLETE)
  02_AO_440_Summons_Issued.pdf  (copy of clerk-issued combined AO 440)
  03_Complaint_as_filed.pdf  (copy)
  04_Dkt_11_Order_Directing_Service.pdf  (copy)
  05_Proof_of_Service_Electronic_Delivery_to_SLB.pdf
  EMAIL_DRAFT_Service_on_SLB.txt
  COMPLETE_Service_Packet_SLB_Acceptance.pdf  (summons + complaint + Dkt. 11 + POS)
"""

from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path
from urllib.parse import quote

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

ISSUED_SUMMONS_SRC = M28 / (
    "AO 440 Summons Issued - Shannon Smith and HOPE Psychotherapy "
    "(N.D. Cal. 3-26-cv-07504-LJC) (Aug 31 2026).pdf"
)
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

# Raw links resolve on the branch that carries these PDFs. Override after merge:
#   PACKET_GITHUB_REF=main python3 internal/scripts/matter28-slb-service-packet.py
GITHUB_OWNER_REPO = "newanforbi/interactive-litigation-portfolio"
GITHUB_REF = os.environ.get("PACKET_GITHUB_REF", "cursor/slb-service-packet-issued-6baa")

PACKET_FILES = {
    "cover": "00_Cover_Sheet.pdf",
    "ack": "01_Acknowledgment_of_Acceptance_of_Service.pdf",
    "summons": "02_AO_440_Summons_Issued.pdf",
    "complaint": "03_Complaint_as_filed.pdf",
    "dkt11": "04_Dkt_11_Order_Directing_Service.pdf",
    "pos": "05_Proof_of_Service_Electronic_Delivery_to_SLB.pdf",
    "complete": "COMPLETE_Service_Packet_SLB_Acceptance.pdf",
}

# Leftover from the unissued two-form packet. Delete on each render.
OBSOLETE = (
    "02_AO_440_Summons_Shannon_Smith.pdf",
    "03_AO_440_Summons_HOPE_Psychotherapy.pdf",
    "04_Complaint_as_filed.pdf",
    "05_Dkt_11_Order_Directing_Service.pdf",
    "06_Proof_of_Service_Electronic_Delivery_to_SLB.pdf",
)


def github_raw(filename: str) -> str:
    rel = f"internal/public/documents/matter-28/service-packet-slb/{filename}"
    return f"https://raw.githubusercontent.com/{GITHUB_OWNER_REPO}/{GITHUB_REF}/{quote(rel, safe='/')}"


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

    line("PACKET CONTENTS (assembled PDF transmitted to counsel, in order)", 10, True)
    for item in [
        "1. AO 440 Summons ISSUED Aug. 31, 2026 (combined — both defendants)",
        "2. Complaint (as filed / courtesy copy previously emailed Jul. 22, 2026)",
        "3. Dkt. 11 — Order directing Rule 4 service (filed Aug. 26, 2026)",
        "4. Proof of Service — Electronic Delivery to SLB (file after confirmation)",
    ]:
        line(f"  {item}")
    line("  Cover and acknowledgment are plaintiff-file only; they are not attached.")
    y -= 6

    line("ISSUED SUMMONS (CONTROLLING)", 10, True)
    line("  Combined AO 440 dated AUG 31 2026, Clerk Mark B. Busby, signed Charles Ho,")
    line("  Deputy Clerk. Names HOPE Psychotherapy, Inc. d/b/a HOPE Program c/o Shannon")
    line("  Smith, LCSW, and Shannon Smith individually, both at 1245 B Street, Hayward,")
    line("  CA 94541. This is the issued process Dkt. 11 required. Do not substitute an")
    line("  unissued proposed summons (Dkt. 3) or a generated blank AO 440.")
    y -= 6

    line("AFTER COUNSEL CONFIRMS ACCEPTANCE", 10, True)
    line("  1. Save the reply email (acceptance for both defendants, date certain).")
    line("  2. Complete / date the Proof of Service (last page) and file it on CM/ECF.")
    line("  3. Calendar the Rule 12 response clock (typically 21 days from acceptance).")
    line("  4. Rule 4(m) outer window from complaint filing (~Jul. 20–21, 2026) ≈ Oct. 19, 2026.")
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
        "the issued Summons (AO 440, dated August 31, 2026) and Complaint (and the "
        "enclosed Dkt. 11 Order) transmitted by email to blaze@sims-law.net and "
        "slb-eservice@sims-law.net."
    )
    y -= 4
    line("Defendants for whom service is accepted:", 10, True)
    line("  [ ]  Shannon Smith, LCSW (individual capacity)")
    line("  [ ]  HOPE Psychotherapy, Inc. d/b/a HOPE Program")
    line("  [ ]  Both of the above")
    y -= 6
    line("Date of acceptance (effective date of service): ________________________", 10, False, 18)
    line("Manner: Electronic mail (PDF attachments), pursuant", 10, False, 18)
    line("to counsel’s agreement to accept service on behalf of the clients during", 10, False, 18)
    line("meet-and-confer.", 10, False, 18)

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
    raw_complete = github_raw(PACKET_FILES["complete"])
    raw_summons = github_raw(PACKET_FILES["summons"])
    raw_complaint = github_raw(PACKET_FILES["complaint"])
    raw_dkt11 = github_raw(PACKET_FILES["dkt11"])
    raw_ack = github_raw(PACKET_FILES["ack"])
    raw_cover = github_raw(PACKET_FILES["cover"])

    text = f"""To: blaze@sims-law.net; slb-eservice@sims-law.net
Cc: cynthia@sims-law.net; bryan@sims-law.net; kschmitt@sims-law.net; june@sims-law.net
Subject: Service of Process — Newanforbi v. Smith, et al., No. 3:26-cv-07504-LJC (N.D. Cal.)

Mr. Van Dine:

Per your statement at meet-and-confer that SLB will accept service for Shannon Smith, LCSW, and HOPE Psychotherapy, Inc., and pursuant to Fed. R. Civ. P. 4 and Dkt. 11 (Aug. 26, 2026), please find the service packet attached.

Please reply confirming that SLB accepts service for both defendants and stating the effective date. I will file proof of service after your confirmation.

Respectfully,

Brendan Ngehsi Newanforbi
Plaintiff In Propria Persona
{PLAINTIFF_ADDRESS}
{PLAINTIFF_CITY}
Tel: {PHONE}
Email: {EMAIL}

Attachments:
  {PACKET_FILES["complete"]}
  {PACKET_FILES["summons"]}
  {PACKET_FILES["complaint"]}
  {PACKET_FILES["dkt11"]}

---
Note to self (do not send): Do not put GitHub raws in the email to SLB.
After Blaze confirms, date and file {PACKET_FILES["pos"]} with the
confirmation email as an exhibit if the clerk’s practice prefers it.
Do not treat SLB’s prior HOPE appearance as a waiver.

Plaintiff-only raws (branch {GITHUB_REF}; after merge use PACKET_GITHUB_REF=main):
  {raw_complete}
  {raw_summons}
  {raw_complaint}
  {raw_dkt11}
  {raw_ack}
  {raw_cover}
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
            "Issued Summons (AO 440, dated August 31, 2026) as to Shannon Smith, "
            "LCSW, and HOPE Psychotherapy, Inc. d/b/a HOPE Program; Complaint; "
            "and Dkt. 11 Order Regarding Payment of Filing Fee and Directing Service"
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
    assert ISSUED_SUMMONS_SRC.is_file(), f"missing {ISSUED_SUMMONS_SRC}"
    assert COMPLAINT_SRC.is_file(), f"missing {COMPLAINT_SRC}"
    assert DKT11_SRC.is_file(), f"missing {DKT11_SRC}"

    for name in OBSOLETE:
        stale = OUT / name
        if stale.is_file() and name not in PACKET_FILES.values():
            stale.unlink()

    cover = OUT / PACKET_FILES["cover"]
    ack = OUT / PACKET_FILES["ack"]
    summons_out = OUT / PACKET_FILES["summons"]
    complaint_out = OUT / PACKET_FILES["complaint"]
    dkt11_out = OUT / PACKET_FILES["dkt11"]
    pos = OUT / PACKET_FILES["pos"]
    email = OUT / "EMAIL_DRAFT_Service_on_SLB.txt"
    complete = OUT / PACKET_FILES["complete"]

    write_cover(cover)
    write_acknowledgment(ack)
    shutil.copy2(ISSUED_SUMMONS_SRC, summons_out)
    shutil.copy2(COMPLAINT_SRC, complaint_out)
    shutil.copy2(DKT11_SRC, dkt11_out)
    write_proof_of_service(pos)
    write_email_draft(email)

    pages = assemble(
        [summons_out, complaint_out, dkt11_out, pos],
        complete,
    )
    print(f"Wrote {complete} ({pages} pages)")
    print(f"GitHub raw ref: {GITHUB_REF}")
    for p in sorted(OUT.iterdir()):
        print(f"  {p.name}  ({p.stat().st_size} bytes)")
        if p.suffix.lower() == ".pdf" or p.name.startswith("EMAIL"):
            print(f"    {github_raw(p.name)}")


if __name__ == "__main__":
    main()
