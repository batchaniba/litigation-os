"""Counsel of record for Matter 33 (Nforbi v. Candelaria, 3:26-cv-08272-LJC).

PACER lists Fiel Dizon Tigno as lead counsel / attorney to be noticed for both
defendants. William J. McMahon signed the Dkt. 11 Answer. Every Rule 5 proof of
service after that September 4, 2026 appearance must name Tigno. Do not list
McMahon alone.
"""

from __future__ import annotations

TIGNO_NAME = "Fiel Dizon Tigno"
TIGNO_TITLE = "Supervising Deputy Attorney General"
MCMAHON_NAME = "William J. McMahon"
MCMAHON_TITLE = "Deputy Attorney General"

AG_OFFICE_LINES = [
    "Office of the Attorney General, California Department of Justice",
    "1515 Clay Street, 20th Floor, P.O. Box 70550",
    "Oakland, CA 94612-0550",
]

DMV_SERVICE_LINES = [
    "Diana Candelaria and Steve Gordon",
    "California Department of Motor Vehicles",
    "Legal Affairs Division, Mail Station C128",
    "2415 First Avenue",
    "Sacramento, CA 95818",
]


def counsel_pos_recipients(*, include_defendants: bool = True) -> list[str]:
    """Mailing block for Matter 33 papers after the AG appearance.

    Tigno is first on purpose. He is the PACER lead / attorney to be noticed.
    """
    lines = [
        f"{TIGNO_NAME}, {TIGNO_TITLE}",
        f"{MCMAHON_NAME}, {MCMAHON_TITLE}",
        *AG_OFFICE_LINES,
        "Attorneys for Defendants Diana Candelaria and Steve Gordon",
    ]
    if include_defendants:
        lines += ["", *DMV_SERVICE_LINES]
    joined = "\n".join(lines)
    if TIGNO_NAME not in joined:
        raise RuntimeError(
            "Matter 33 POS must name Fiel Dizon Tigno "
            "(PACER lead / attorney to be noticed)."
        )
    if MCMAHON_NAME in joined and joined.index(TIGNO_NAME) > joined.index(MCMAHON_NAME):
        raise RuntimeError(
            "List Fiel Dizon Tigno before William J. McMahon — "
            "Tigno is lead counsel to be noticed."
        )
    return lines
