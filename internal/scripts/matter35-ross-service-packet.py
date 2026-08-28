#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Matter 35 - Process-server packet for Ross Stores, Inc. and Ross Dress for Less, Inc.

Order (CRC 3.221 / Santa Clara practice):
  1. SUM-100 Summons (issued)
  2. Verified Complaint (conformed)
  3. Other served papers: CV-5012 (clerk-stamped) + CV-5003 ADR Information Sheet

Same packet is used for each corporate defendant (agent for service:
C T Corporation System, Glendale). DOEs are not served with this packet.
Internal Damages Worksheet is intentionally excluded (DO NOT FILE / do not serve).
"""
from __future__ import annotations

from pathlib import Path

import pymupdf
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[1]
M35 = ROOT / "public/documents/matter-35"

SUMMONS = M35 / "SUM-100 Summons (ISSUED, Filed Aug 26 2026) - 26CV501995.pdf"
COMPLAINT = M35 / "Verified Complaint (CONFORMED, Filed Aug 26 2026) - 26CV501995.pdf"
CV5012 = M35 / "CV-5012 Civil Lawsuit Notice (Clerk-Stamped) - 26CV501995.pdf"
ADR = M35 / "CV-5003 ADR Information Sheet (Santa Clara).pdf"

OUT_PACKET = (
    M35
    / "Service Packet - Ross Stores Inc and Ross Dress for Less Inc "
      "(Summons, Complaint, CV-5012, ADR) (Aug 27 2026).pdf"
)
OUT_ROOT = (
    ROOT.parent
    / "Service Packet - Ross Defendants (Summons Complaint CV-5012 ADR) "
      "(26CV501995 Aug 27 2026).pdf"
)
OUT_INSTRUCTIONS = (
    M35
    / "Process Server Instructions - Ross Stores Inc and Ross Dress for Less Inc "
      "(Aug 27 2026).pdf"
)


def build_instructions(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(path), pagesize=letter)
    w, h = letter
    y = h - 72
    left = 72

    def line(text: str, *, bold: bool = False, size: float = 11, gap: float = 14) -> None:
        nonlocal y
        c.setFont("Times-Bold" if bold else "Times-Roman", size)
        c.drawString(left, y, text)
        y -= gap

    line("PROCESS SERVER INSTRUCTIONS", bold=True, size=14, gap=20)
    line("Ngwa Nforbi v. Ross Stores, Inc., et al.", bold=True, size=12)
    line("Santa Clara Superior Court - Case No. 26CV501995", gap=18)

    line("Serve BOTH corporate defendants with an identical copy of the Service Packet:", gap=16)
    line("  1. Ross Stores, Inc. (Delaware; CA SOS State ID 01642535)", gap=14)
    line("  2. Ross Dress for Less, Inc. (Virginia; CA Doc. No. 2642531)", gap=18)

    line("Agent for service of process (information and belief):", bold=True, gap=16)
    line("  C T Corporation System", gap=14)
    line("  330 N. Brand Blvd., Suite 700", gap=14)
    line("  Glendale, CA 91203", gap=18)

    line("Corporate HQ (for reference; service is on the agent):", bold=True, gap=16)
    line("  5130 Hacienda Drive, Dublin, CA 94568", gap=18)

    line("Packet contents (in order):", bold=True, gap=16)
    line("  1. SUM-100 Summons (issued / clerk-filed Aug. 26, 2026)", gap=14)
    line("  2. Verified Complaint (conformed / clerk-filed Aug. 26, 2026)", gap=14)
    line("  3. CV-5012 Civil Lawsuit Notice (clerk-stamped)", gap=14)
    line("  4. CV-5003 ADR Information Sheet (Santa Clara)", gap=18)

    line("Do NOT serve:", bold=True, gap=16)
    line("  - Internal Damages Worksheet (do not file; do not serve)", gap=14)
    line("  - DOE defendants (serve only after identification / amendment)", gap=18)

    line("After service: complete and return POS-010 for each defendant served.", gap=16)
    line("Service deadline: within 60 days of filing (~October 25, 2026).", gap=18)

    line("Plaintiff contact:", bold=True, gap=16)
    line("  Brendan Ngwa Nforbi, In Propria Persona", gap=14)
    line("  1455 Cat Tail Drive, Stockton, CA 95204", gap=14)
    line("  (209) 801-4442 | bnn.cdl@gmail.com", gap=18)

    c.setFont("Times-Roman", 8)
    c.drawString(left, 40, "Matter 35 - companion to Service Packet (not for service on defendants)")
    c.save()
    print(f"Wrote {path} ({path.stat().st_size} bytes)")


def merge_packet(out: Path) -> None:
    parts = [SUMMONS, COMPLAINT, CV5012, ADR]
    for p in parts:
        if not p.is_file():
            raise SystemExit(f"Missing required packet component: {p}")

    merged = pymupdf.open()
    labels = []
    for p in parts:
        doc = pymupdf.open(p)
        labels.append(f"{p.name} ({doc.page_count}p)")
        merged.insert_pdf(doc)
        doc.close()

    out.parent.mkdir(parents=True, exist_ok=True)
    merged.save(out)
    print(f"Wrote {out} ({out.stat().st_size} bytes, {merged.page_count} pages)")
    print("  Order: " + " -> ".join(labels))
    merged.close()


def main() -> None:
    build_instructions(OUT_INSTRUCTIONS)
    merge_packet(OUT_PACKET)
    merge_packet(OUT_ROOT)


if __name__ == "__main__":
    main()
