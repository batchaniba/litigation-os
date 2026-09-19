#!/usr/bin/env python3
"""Render WESTLAW_PORTFOLIO_QUEUE.pdf from westlaw_portfolio_queue.json.

Library checklist. Not a filing. No repo URLs.
"""

from __future__ import annotations

import json
from pathlib import Path

try:
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    from reportlab.lib.pagesizes import letter, landscape
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import (
        KeepTogether,
        PageBreak,
        Paragraph,
        SimpleDocTemplate,
        Spacer,
        Table,
        TableStyle,
    )
except ImportError as exc:
    raise SystemExit("Install reportlab: python3 -m pip install reportlab") from exc

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "internal/docs/westlaw_portfolio_queue.json"
OUT = ROOT / "internal/docs/WESTLAW_PORTFOLIO_QUEUE.pdf"

NAVY = colors.HexColor("#17324D")
BLUE = colors.HexColor("#2E5D7B")
PALE = colors.HexColor("#EAF1F5")
PALE_GOLD = colors.HexColor("#F7F1DF")
PALE_RED = colors.HexColor("#F6E8E8")
CHAR = colors.HexColor("#263238")
GRAY = colors.HexColor("#66727A")
LINE = colors.HexColor("#C5CDD3")
WHITE = colors.white

PAGE = landscape(letter)
LEFT = 0.55 * inch
RIGHT = 0.55 * inch
TOP = 0.55 * inch
BOTTOM = 0.5 * inch
USABLE = PAGE[0] - LEFT - RIGHT


def esc(s: str) -> str:
    return (
        (s or "")
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(LINE)
    canvas.line(LEFT, 0.34 * inch, PAGE[0] - RIGHT, 0.34 * inch)
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(GRAY)
    canvas.drawString(
        LEFT,
        0.18 * inch,
        "Westlaw Patron Access KeyCite queue — library use — not for filing — yellow ≠ miscited",
    )
    canvas.drawRightString(PAGE[0] - RIGHT, 0.18 * inch, f"{doc.page}")
    canvas.restoreState()


def styles():
    return {
        "h1": ParagraphStyle(
            "h1",
            fontName="Helvetica-Bold",
            fontSize=18,
            leading=22,
            textColor=NAVY,
            alignment=TA_CENTER,
            spaceAfter=6,
        ),
        "sub": ParagraphStyle(
            "sub",
            fontName="Helvetica",
            fontSize=10,
            leading=13,
            textColor=GRAY,
            alignment=TA_CENTER,
            spaceAfter=10,
        ),
        "h2": ParagraphStyle(
            "h2",
            fontName="Helvetica-Bold",
            fontSize=12,
            leading=15,
            textColor=NAVY,
            spaceBefore=8,
            spaceAfter=4,
        ),
        "p": ParagraphStyle(
            "p",
            fontName="Helvetica",
            fontSize=9,
            leading=12,
            textColor=CHAR,
            spaceAfter=4,
        ),
        "tiny": ParagraphStyle(
            "tiny",
            fontName="Helvetica",
            fontSize=7.5,
            leading=9.5,
            textColor=CHAR,
        ),
        "th": ParagraphStyle(
            "th",
            fontName="Helvetica-Bold",
            fontSize=7.5,
            leading=9,
            textColor=WHITE,
        ),
        "cell": ParagraphStyle(
            "cell",
            fontName="Helvetica",
            fontSize=7.5,
            leading=9.5,
            textColor=CHAR,
        ),
        "cellb": ParagraphStyle(
            "cellb",
            fontName="Helvetica-Bold",
            fontSize=7.5,
            leading=9.5,
            textColor=NAVY,
        ),
    }


def section_table(rows: list[dict], S: dict, with_checks: bool = True) -> Table:
    head = [
        Paragraph("#", S["th"]),
        Paragraph("Search (type this)", S["th"]),
        Paragraph("Status", S["th"]),
        Paragraph("Matters", S["th"]),
        Paragraph("Uses", S["th"]),
        Paragraph("N / Y / R", S["th"]),
        Paragraph("KEEP / DROP", S["th"]),
        Paragraph("Notes", S["th"]),
    ]
    data = [head]
    for r in rows:
        matters = ", ".join(str(m) for m in r.get("matters") or [])
        data.append(
            [
                Paragraph(str(r.get("n") or ""), S["cell"]),
                Paragraph(esc(r.get("search") or r.get("display") or ""), S["cellb"]),
                Paragraph(esc(r.get("status") or ""), S["cell"]),
                Paragraph(esc(matters), S["cell"]),
                Paragraph(str(r.get("occurrenceCount") or ""), S["cell"]),
                Paragraph("☐  ☐  ☐", S["cell"]),
                Paragraph("☐     ☐", S["cell"]),
                Paragraph("", S["cell"]),
            ]
        )
    col = [0.35 * inch, 4.15 * inch, 1.15 * inch, 0.85 * inch, 0.45 * inch, 0.7 * inch, 0.85 * inch, 1.5 * inch]
    t = Table(data, colWidths=col, repeatRows=1)
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 3),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3),
        ("TOPPADDING", (0, 0), (-1, -1), 2.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
        ("GRID", (0, 0), (-1, -1), 0.3, LINE),
        ("ALIGN", (0, 1), (0, -1), "CENTER"),
        ("ALIGN", (4, 1), (6, -1), "CENTER"),
    ]
    for i, r in enumerate(rows, 1):
        bg = WHITE
        if r.get("bucket") == "confirm_absent":
            bg = PALE_RED
        elif r.get("bucket") in {"p0", "p1"}:
            bg = PALE_GOLD
        elif r.get("bucket") == "done":
            bg = PALE
        elif i % 2 == 0:
            bg = colors.HexColor("#F4F7F8")
        style.append(("BACKGROUND", (0, i), (-1, i), bg))
    t.setStyle(TableStyle(style))
    return t


def build():
    payload = json.loads(SRC.read_text())
    rows = payload["rows"]
    c = payload["counts"]
    S = styles()
    by = {b: [r for r in rows if r["bucket"] == b] for b in (
        "confirm_absent", "p0", "p1", "live_plaintiff", "other_plaintiff", "joined", "done"
    )}
    todo = [r for r in rows if r["bucket"] not in {"done", "confirm_absent"}]
    session1 = todo[:20]

    story = []
    story.append(Paragraph("Westlaw KeyCite queue", S["h1"]))
    story.append(
        Paragraph(
            f"Portfolio-wide · generated {esc(payload.get('generatedDate') or '')} · "
            "Patron Access for Pro Se · 20 views / session",
            S["sub"],
        )
    )
    story.append(
        Paragraph(
            f"<b>{c['uniquePins']}</b> unique pins from <b>{c['ledgerAuthorities']}</b> ledger rows. "
            f"<b>{c.get('done', 0)}</b> already KeyCited (UNIFIED / Round 12). "
            f"<b>{c.get('confirm_absent', 0)}</b> confirm-absent. "
            f"<b>{c['todoKeyCite']}</b> still to KeyCite "
            f"({c.get('p0', 0)} P0 + {c.get('p1', 0)} P1 + {c.get('live_plaintiff', 0)} live-plaintiff "
            f"+ {c.get('other_plaintiff', 0)} other-plaintiff + {c.get('joined', 0)} court/opposing) · "
            f"<b>{c['sessionsOf20']}</b> sessions of 20.",
            S["p"],
        )
    )
    story.append(Paragraph("Rules at the seat", S["h2"]))
    story.append(
        Paragraph(
            "1. Enter only through the San Diego Law Library Westlaw Remote for Pro Se link. "
            "Sign Off when done — two shared seats.",
            S["p"],
        )
    )
    story.append(
        Paragraph(
            "2. KeyCite is <b>treatment</b>, not existence. Run the free funnel first. "
            "Yellow ≠ MISCITED. A clean flag does not clear a proposition error "
            "(<i>Chavez v. Robinson</i>, 12 F.4th 978 stays MISCHARACTERIZED).",
            S["p"],
        )
    )
    story.append(
        Paragraph(
            "3. Exhaust each cite in one visit: search → flag color (N none / Y yellow / R red) → "
            "on yellow/red, open negative treatment and write whether it touches <b>your</b> "
            "proposition. Do not spend a second session on the same cite.",
            S["p"],
        )
    )
    story.append(
        Paragraph(
            "4. Flag-glance the batch first. Deep-read only flags that could matter. "
            "Statutes, rules, and constitutional provisions are not in this packet.",
            S["p"],
        )
    )
    story.append(
        Paragraph(
            "5. Known fabrications (pink rows): search only. A miss is the point. "
            "Do not introduce them into a new plaintiff filing.",
            S["p"],
        )
    )

    story.append(Paragraph("Session 1 — do these first (20)", S["h2"]))
    story.append(
        Paragraph(
            "P0 then P1. Type the Search column. Mark N/Y/R and KEEP/DROP before leaving the document.",
            S["p"],
        )
    )
    story.append(KeepTogether([section_table(session1, S)]))

    story.append(PageBreak())
    story.append(Paragraph("Confirm-absent — search only", S["h2"]))
    story.append(
        Paragraph(
            "Known fabrications. Do not open KeyCite. Do not file these pins again.",
            S["p"],
        )
    )
    story.append(section_table(by["confirm_absent"], S))

    story.append(Paragraph("P0 — plaintiff-only UNVERIFIED", S["h2"]))
    story.append(section_table(by["p0"], S))

    story.append(Paragraph("P1 — plaintiff-only bad status", S["h2"]))
    story.append(
        Paragraph(
            "Treatment does not clear MISCITED / MISCHARACTERIZED. Confirm the real caption and pin.",
            S["p"],
        )
    )
    story.append(section_table(by["p1"], S))

    story.append(PageBreak())
    story.append(Paragraph("Live-matter plaintiff filings (not yet KeyCited)", S["h2"]))
    story.append(
        Paragraph(
            "Matters 12, 19, 20, 24–29, 32, 33, 35. Load-bearing by use count. "
            f"{len(by['live_plaintiff'])} pins.",
            S["p"],
        )
    )
    story.append(section_table(by["live_plaintiff"], S))

    story.append(PageBreak())
    story.append(Paragraph("Other plaintiff filings (closed / archived matters)", S["h2"]))
    story.append(section_table(by["other_plaintiff"], S))

    story.append(PageBreak())
    story.append(Paragraph("Court / opposing / research only", S["h2"]))
    story.append(
        Paragraph(
            "Flag-glance if a session has leftover views. Do not deep-read these until P0/P1 and live-plaintiff are empty.",
            S["p"],
        )
    )
    story.append(section_table(by["joined"], S))

    story.append(PageBreak())
    story.append(Paragraph("Already KeyCited — skip", S["h2"]))
    story.append(
        Paragraph(
            "UNIFIED memo, 2026-09-19. 27/27 names confirmed. "
            "<i>Chavez</i> 12 F.4th: KeyCite NONE; still MISCHARACTERIZED — do not claim QI-denial reversal.",
            S["p"],
        )
    )
    story.append(section_table(by["done"], S))

    story.append(Paragraph("20-view session map", S["h2"]))
    sess_head = [
        Paragraph("Session", S["th"]),
        Paragraph("Rows", S["th"]),
        Paragraph("First search", S["th"]),
        Paragraph("Last search", S["th"]),
    ]
    sess_data = [sess_head]
    for s in payload.get("sessions") or []:
        sess_data.append(
            [
                Paragraph(str(s["session"]), S["cell"]),
                Paragraph(f"{s['from']}–{s['to']} ({s['count']})", S["cell"]),
                Paragraph(esc(s["searches"][0]), S["cell"]),
                Paragraph(esc(s["searches"][-1]), S["cell"]),
            ]
        )
    st = Table(sess_data, colWidths=[0.8 * inch, 1.4 * inch, 4.4 * inch, 4.4 * inch], repeatRows=1)
    st.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("GRID", (0, 0), (-1, -1), 0.3, LINE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 3),
                ("RIGHTPADDING", (0, 0), (-1, -1), 3),
                ("TOPPADDING", (0, 0), (-1, -1), 2),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
            ]
        )
    )
    story.append(st)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=PAGE,
        leftMargin=LEFT,
        rightMargin=RIGHT,
        topMargin=TOP,
        bottomMargin=BOTTOM,
        title="Westlaw KeyCite queue — portfolio",
        author="Brendan Ngwa Nforbi",
        subject="Library KeyCite checklist — not for filing",
    )
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print(f"Wrote {OUT} ({OUT.stat().st_size} bytes, {doc.page} pages)")


if __name__ == "__main__":
    build()
