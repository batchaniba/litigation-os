# Portfolio form library

Blank court forms and portfolio-generated templates live here
(`internal/public/documents/_form-library/`). Matter scripts fill from these
paths rather than copying court PDFs into each matter folder.

## De facto Proof of Service (federal Rule 5)

| | |
|---|---|
| **Blank PDF** | `proof-of-service-blank-template.pdf` |
| **Generator** | `internal/scripts/lib/proof_of_service.py` |
| **CLI** | `python3 internal/scripts/generate-proof-of-service.py` |

Use this form for all federal Rule 5 mail / paper service certificates going
forward (N.D. Cal. by default; set `district_line` for E.D. Cal. or another
district). Do not invent a new pleading-paper "Certificate of Service" layout
per matter.

```python
from pathlib import Path
from proof_of_service import ProofOfServiceFields, build_proof_of_service

build_proof_of_service(
    Path(".../Proof of Service - ....pdf"),
    ProofOfServiceFields(
        plaintiff_line="BRENDAN NGWA NFORBI",
        plaintiff_role="Plaintiff",
        defendant_lines=["DEFENDANT NAME"],
        defendant_role="Defendant",
        case_number="3:26-cv-xxxxx-XXX",
        service_date="August 21, 2026",
        document_title="First Amended Complaint (Dkt. 5)",
        mailing_location="San Jose, California",
        recipients=["Name", "Address line 1", "City, ST ZIP"],
        server_name="Brendan Ngwa Nforbi",
        stamp_signature=True,
    ),
)
```

## Stipulations (plaintiff-favorable — LOCKED)

There is no blank court PDF for a stipulation. Draft from
`.claude/skills/stipulation-defense/TEMPLATE.md`. Terms match
`.claude/skills/stipulation-defense/SKILL.md`. Clauses:
`.claude/skills/stipulation-defense/CLAUSES.md`. Always-on rule:
`.cursor/rules/stipulation-plaintiff-favor.mdc`.

Every stipulation in any matter is drafted most favorably to Plaintiff.
Shorten or hold a defense clock. Do not compress Plaintiff's own clocks.
Continue the event only — not the chain of deadlines. Date certain, never
a floating anchor. Never expand their ask. Named party only. Single shot.
He signs his own paper — do not sign counsel's draft, and do not let them
affix `/s/`.

Worked counterparts: Matter 29 Amazon (Aug. 31, 2026) and Accurate
(Sep. 1, 2026). Stay counter-draft: Matter 2 (Apr. 13–14, 2026).
Failure mode: Serrato Dkt. 22 — do not give more delay than they asked.

## Short public PDF links

Phone-tappable URLs live in `internal/public/short-links.json`. Each entry
is a hyphenated slug (`fedex-consent`) whose `/slug` 307s to `/slug.pdf`.
Vercel sets `Content-Disposition` to the long portfolio filename, so Save As
keeps the court-style name. Never put that long name in a Vercel redirect
`destination` — parentheses, especially `(b)`, get rejected.

After adding an entry, copy the packet to `internal/public/{slug}.pdf`
(`publish_short_link` in `internal/scripts/lib/short_link.py`) and run
`npm run sync:short-links`.

## Other blanks in this folder

| File | Use |
|---|---|
| `ao440-blank-template.pdf` | AO 440 summons |
| `js44-civil-cover-sheet-blank-template.pdf` | JS 44 / JS-CAND 44 |
| `edcal-mj-consent-declination-blank-template.pdf` | E.D. Cal. MJ consent (consentmagweb) |
| `ndcal-mj-consent-declination-blank-template.pdf` | N.D. Cal. MJ consent |
| `ser001-blank-template.pdf` | SER-001 sheriff service request |
| `sum100-blank-template.pdf` | SUM-100 state summons |
| `cm010-blank-template.pdf` | CM-010 civil case cover sheet |
| `fw003-blank-template.pdf` | FW-003 order on court fee waiver (clerk) |
| `cv-5012-blank-template.pdf` | Santa Clara CV-5012 Civil Lawsuit Notice (blank for clerk) |
| `hc004-blank-template.pdf` | HC-004 habeas |
| `stanislaus-cc-authorization-blank-template.pdf` | Stanislaus CC auth |
| `pos050-blank-template.pdf` | POS-050/EFS-050 Proof of Electronic Service (CRC 2.251) |
| `civ100-blank-template.pdf` | CIV-100 Request for Entry of Default (Judicial Council; courts.ca.gov) |
