#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Matter 35 - CT Corporation private process-server packet + email draft.

Builds:
  - Process-server cover / instructions PDF
  - Combined service packet (cover + conformed complaint + issued summons
    + CV-5012 + CV-5003 ADR sheet + blank POS-010 x2)
  - Plain-text email draft for any private process server

    python3 internal/scripts/matter35-ct-process-server-packet.py
"""

from __future__ import annotations

import io
import textwrap
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

INTERNAL = Path(__file__).resolve().parents[1]  # .../internal
OUT = INTERNAL / "public/documents/matter-35"
ART = Path("/opt/cursor/artifacts")

CASE_NO = "26CV501995"
CAPTION = "Ngwa Nforbi v. Ross Stores, Inc., et al."
COURT = "Superior Court of California, County of Santa Clara"
DEPT = "Dept. 16 - Hon. Vince Parrett"
CMC = "February 11, 2027 (confirm time on portal; stamp shows Dept. 16)"

PLAINTIFF = "Brendan Ngwa Nforbi"
STREET = "1455 Cat Tail Drive"
CITY_STATE_ZIP = "Stockton, CA 95204"
PHONE = "(209) 801-4442"
EMAIL = "bnn.cdl@gmail.com"

AGENT_NAME = "C T Corporation System"
AGENT_ADDR = "330 N. Brand Boulevard, Suite 700"
AGENT_CITY = "Glendale, CA 91203"
AGENT_COUNTY = "Los Angeles County"

DEFS = [
    {
        "name": "Ross Stores, Inc.",
        "entity": "Delaware corporation",
        "sos": "CA SOS State ID 01642535",
        "hq": "5130 Hacienda Drive, Dublin, CA 94568",
        "label": "PACKET A - ROSS STORES, INC.",
    },
    {
        "name": "Ross Dress for Less, Inc.",
        "entity": "Virginia corporation",
        "sos": "CA Doc. No. 2642531",
        "hq": "5130 Hacienda Drive, Dublin, CA 94568 (owns/operates Sunnyvale store)",
        "label": "PACKET B - ROSS DRESS FOR LESS, INC.",
    },
]

SERVICE_DEADLINE = "on or before October 25, 2026"
# 60 days from Aug. 26, 2026 filing (CRC 3.110(b)); confirm calendar

DOCS = {
    "complaint": OUT
    / "Verified Complaint (CONFORMED, Filed Aug 26 2026) - 26CV501995.pdf",
    "summons": OUT / "SUM-100 Summons (ISSUED, Filed Aug 26 2026) - 26CV501995.pdf",
    "cv5012": OUT / "CV-5012 Civil Lawsuit Notice (Clerk-Stamped) - 26CV501995.pdf",
    "adr": OUT / "CV-5003 ADR Information Sheet - Civil Division (Santa Clara).pdf",
    "pos": OUT / "POS-010 Proof of Service of Summons (blank).pdf",
}


def _text_pages(lines: list[str], title: str | None = None) -> PdfReader:
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter)
    width, height = letter
    left = 0.7 * inch
    y = height - 0.65 * inch
    max_chars = 98

    def new_page():
        nonlocal y
        c.showPage()
        y = height - 0.65 * inch

    if title:
        c.setFont("Helvetica-Bold", 13)
        for chunk in textwrap.wrap(title, width=70) or [title]:
            c.drawString(left, y, chunk)
            y -= 16
        y -= 6

    for raw in lines:
        if raw == "":
            y -= 10
            continue
        if raw.startswith("## "):
            if y < 1.2 * inch:
                new_page()
            c.setFont("Helvetica-Bold", 11)
            c.drawString(left, y, raw[3:])
            y -= 15
            continue
        if raw.startswith("# "):
            if y < 1.2 * inch:
                new_page()
            c.setFont("Helvetica-Bold", 12)
            c.drawString(left, y, raw[2:])
            y -= 16
            continue
        font = "Helvetica"
        size = 10
        text = raw
        if raw.startswith("**") and raw.endswith("**"):
            font = "Helvetica-Bold"
            text = raw[2:-2]
        c.setFont(font, size)
        wrapped = textwrap.wrap(text, width=max_chars) or [""]
        for wline in wrapped:
            if y < 0.7 * inch:
                new_page()
                c.setFont(font, size)
            c.drawString(left, y, wline)
            y -= 12
    c.save()
    buf.seek(0)
    return PdfReader(buf)


def _append(writer: PdfWriter, reader: PdfReader) -> None:
    for page in reader.pages:
        writer.add_page(page)



def cover_lines() -> list[str]:
    return [
        "# PROCESS SERVER INSTRUCTIONS - PRIVATE SERVICE",
        f"**{CAPTION}**",
        f"**{COURT}**",
        f"**Case No. {CASE_NO}**  |  {DEPT}",
        f"First CMC: {CMC}",
        "",
        "## Plaintiff / requesting party (pro se)",
        f"{PLAINTIFF}",
        f"{STREET}",
        f"{CITY_STATE_ZIP}",
        f"Phone: {PHONE}",
        f"Email: {EMAIL}",
        "",
        "## What to serve (TWO corporate defendants - SAME agent)",
        "Serve BOTH of the following entities by personal delivery on their",
        "California registered agent for service of process:",
        "",
        f"**Agent for service:** {AGENT_NAME}",
        f"**Service address:** {AGENT_ADDR}, {AGENT_CITY}",
        f"**County of service:** {AGENT_COUNTY}",
        "",
        f"1. **{DEFS[0]['name']}** ({DEFS[0]['entity']}; {DEFS[0]['sos']})",
        f"2. **{DEFS[1]['name']}** ({DEFS[1]['entity']}; {DEFS[1]['sos']})",
        "",
        "DOE defendants are NOT to be served at this time.",
        "",
        "## Documents in EACH defendant's set (leave two complete sets)",
        "For EACH corporation, leave one complete packet containing:",
        "  - Verified Complaint (conformed, Case No. 26CV501995)",
        "  - Issued SUM-100 Summons",
        "  - Clerk-stamped CV-5012 Civil Lawsuit Notice",
        "  - CV-5003 ADR Information Sheet (Santa Clara Civil Division)",
        "",
        "Label the physical envelopes / clips:",
        f"  - {DEFS[0]['label']}",
        f"  - {DEFS[1]['label']}",
        "",
        "## Manner of service",
        "Personal service on C T Corporation System (or a person authorized to",
        "accept service on its behalf) at the Glendale address above.",
        "Do NOT mail. Do NOT substitute-serve at the Dublin HQ unless you first",
        "confirm with Plaintiff in writing.",
        "",
        "## Deadline",
        f"Please attempt service promptly and complete service {SERVICE_DEADLINE}",
        "(CRC 3.110(b) - 60 days from the Aug. 26, 2026 filing). File / return",
        "proofs as soon as service is effected so Plaintiff can e-file POS-010.",
        "",
        "## Proofs to return",
        "Complete a SEPARATE Judicial Council POS-010 for each defendant",
        "(two blanks are included at the end of this packet). On each POS-010:",
        "  - Caption: Ngwa Nforbi v. Ross Stores, Inc., et al.",
        f"  - Case No.: {CASE_NO}",
        "  - Party served: name ONE defendant only (Ross Stores, Inc. OR",
        "    Ross Dress for Less, Inc.)",
        "  - Person served / capacity: authorized agent of C T Corporation System",
        "    (registered agent for service of process)",
        f"  - Address: {AGENT_ADDR}, {AGENT_CITY}",
        "  - Date/time of service; your name, registration no. (if any), and signature",
        "",
        "Email scanned POS-010s to Plaintiff at the address above the same day,",
        "and mail or deliver the wet-ink originals to Plaintiff for court filing.",
        "",
        "## Fees / questions",
        "Reply to this packet / email with your flat fee for serving both entities",
        "at the same CT Corporation address (one trip, two sets). Call or email",
        f"Plaintiff at {PHONE} / {EMAIL} with any questions before attempting service.",
        "",
        f"Prepared: August 27, 2026 - {PLAINTIFF}, Plaintiff in propria persona",
    ]


def email_body() -> str:
    return textwrap.dedent(
        f"""\
        Subject: Service request - {CAPTION}, Santa Clara Sup. Ct. No. {CASE_NO}
        (serve BOTH Ross entities via C T Corporation System, Glendale)

        Hello,

        I am the plaintiff in {CAPTION}, Santa Clara Superior Court Case No. {CASE_NO}
        (Hon. Vince Parrett, Dept. 16). I am representing myself.

        Please serve BOTH corporate defendants through their California registered
        agent for service of process (same address for both):

            Agent:  {AGENT_NAME}
            Address: {AGENT_ADDR}
                     {AGENT_CITY}
            County:  {AGENT_COUNTY}

        Defendants to serve (two separate complete sets at the same visit):
            1. {DEFS[0]['name']} ({DEFS[0]['entity']}; {DEFS[0]['sos']})
            2. {DEFS[1]['name']} ({DEFS[1]['entity']}; {DEFS[1]['sos']})

        Do not serve the DOE defendants.

        Each set should include:
            - Verified Complaint (conformed)
            - Issued SUM-100 Summons
            - Clerk-stamped CV-5012 Civil Lawsuit Notice
            - CV-5003 ADR Information Sheet (Santa Clara Civil Division)

        Manner: personal service on C T Corporation System (or a person
        authorized to accept service for CT) at the Glendale address. Please
        do not mail and do not attempt substitute service at the Dublin
        headquarters without checking with me first.

        Deadline: please complete service {SERVICE_DEADLINE} (60 days from the
        August 26, 2026 filing under CRC 3.110(b)).

        Proofs: complete a separate Judicial Council POS-010 for each defendant,
        email me scans the same day at {EMAIL}, and send the originals to:

            {PLAINTIFF}
            {STREET}
            {CITY_STATE_ZIP}
            {PHONE}

        Please reply with (1) confirmation you can take the job, (2) your flat
        fee for serving both entities at CT in one trip, and (3) your soonest
        available attempt date. I will send the combined PDF service packet
        (or printed sets) as soon as you confirm.

        Thank you,
        {PLAINTIFF}
        Plaintiff, In Propria Persona
        {EMAIL} | {PHONE}
        """
    )


def build() -> None:
    for key, path in DOCS.items():
        if not path.is_file():
            raise FileNotFoundError(f"Missing {key}: {path}")

    cover = _text_pages(cover_lines())
    cover_path = OUT / (
        "Process Server Cover Sheet - CT Corporation Service "
        "(Ross Stores Inc and Ross Dress for Less Inc) (Aug 27 2026).pdf"
    )
    w = PdfWriter()
    _append(w, cover)
    with open(cover_path, "wb") as f:
        w.write(f)
    print("wrote", cover_path.name, f"({len(PdfReader(str(cover_path)).pages)} pp)")

    # Combined packet: court documents only (no cover / dividers / caption sheets).
    # Instructions live in the separate cover sheet + email draft.
    packet = PdfWriter()

    for _d in DEFS:
        for key in ("complaint", "summons", "cv5012", "adr"):
            _append(packet, PdfReader(str(DOCS[key])))

    # One blank POS-010 per defendant (no caption stickers)
    for _d in DEFS:
        _append(packet, PdfReader(str(DOCS["pos"])))

    packet_path = OUT / "Ross_CT_Corp_Service_Packet_court_docs_only.pdf"
    # Keep legacy filename in sync for older links
    legacy_path = OUT / (
        "Private Process Server Packet - CT Corporation "
        "(Ross Stores Inc and Ross Dress for Less Inc) (Aug 27 2026).pdf"
    )
    with open(packet_path, "wb") as f:
        packet.write(f)
    legacy_path.write_bytes(packet_path.read_bytes())
    pages = len(PdfReader(str(packet_path)).pages)
    print("wrote", packet_path.name, f"({pages} pp, {packet_path.stat().st_size // 1024} KB)")

    email_path = OUT / (
        "Email Draft - Process Server CT Corporation Service "
        "(Ross Stores Inc and Ross Dress for Less Inc) (Aug 27 2026).txt"
    )
    email_path.write_text(email_body())
    print("wrote", email_path.name)

    # Artifacts (flat, downloadable)
    ART.mkdir(parents=True, exist_ok=True)
    for src, name in [
        (cover_path, "ross_ct_process_server_cover.pdf"),
        (packet_path, "ross_ct_service_packet_court_docs_only.pdf"),
        (email_path, "ross_ct_process_server_email.txt"),
    ]:
        dest = ART / name
        dest.write_bytes(src.read_bytes())
        print("artifact", dest.name)


if __name__ == "__main__":
    build()
