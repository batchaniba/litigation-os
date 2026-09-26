"""Matter 28 — Newanforbi v. Smith / HOPE — service list for future proofs of service.

Effective September 26, 2026. Source: Martinez courtesy-copy acknowledgment
(Proposed Order Denying MTD) plus Plaintiff's instruction that all future
Matter 28 POS addressees are Eric Martinez, Kim Schmitt, June Meinecke,
Amber Krausse, and slb-eservice@sims-law.net.

Do not rewrite already-filed proofs (Opposition POS Sep. 22; SLB acceptance
POS Aug. 31 / Sep. 2). Import POS_RECIPIENTS and EMAIL_TO from here for
any new Matter 28 generator.

Blaze Van Dine and Cynthia Lawrence remain counsel of record / firm principals.
They stay on EMAIL_COURTESY. They are not in the POS addressee block unless
a later instruction puts them back.
"""

from __future__ import annotations

FIRM = "Sims, Lawrence & Broghammer"
FIRM_ADDRESS = "1478 Stone Point Drive, Suite 450, Roseville, CA 95661"
FIRM_PHONE = "(916) 797-8881"

ERIC = ("Eric T. Martinez, Esq.", "emartinez@sims-law.net")
KIM = ("Kim Schmitt", "kschmitt@sims-law.net")
JUNE = ("June Meinecke", "june@sims-law.net")
AMBER = ("Amber Krausse", "amber@sims-law.net")
SLB_ESERVICE = ("Sims, Lawrence & Broghammer e-service", "slb-eservice@sims-law.net")

POS_ADDRESSEES = (ERIC, KIM, JUNE, AMBER, SLB_ESERVICE)

EMAIL_TO = [email for _name, email in POS_ADDRESSEES]

EMAIL_COURTESY = [
    "blaze@sims-law.net",
    "cynthia@sims-law.net",
]

POS_RECIPIENTS: list[str] = [
    f"{name} — {email}" for name, email in POS_ADDRESSEES
] + [
    FIRM_ADDRESS,
    "Attorneys for Defendants Shannon Smith, LCSW, and",
    "HOPE Psychotherapy, Inc. (d/b/a HOPE Program)",
]


def email_headers() -> str:
    to = "; ".join(EMAIL_TO)
    cc = "; ".join(EMAIL_COURTESY)
    return f"To: {to}\nCc: {cc}"
