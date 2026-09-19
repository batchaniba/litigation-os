# Westlaw portfolio queue

Generated 2026-09-19 from `citation_verification.json` (kind=`authority` only). Not a brief. KeyCite is **treatment**, not existence. Yellow ≠ MISCITED. Do not mark VERIFIED from a flag color.

Door: [WESTLAW_PATRON_ACCESS.md](WESTLAW_PATRON_ACCESS.md). 20 document views / session. Flag-glance the batch first; deep-read only yellow/red that could touch the proposition you are citing.

## Counts

- Ledger authority rows (OCR variants included): **987**
- Unique reporter / WL / name pins: **833**
- Already KeyCited (UNIFIED / Round 12): **27**
- Confirm-absent (known fabrications): **5**
- Still to KeyCite: **801** (8 P0 + 19 P1 + 270 live-plaintiff + 65 other-plaintiff + 439 court/opposing)
- Sessions at 20 views: **41**

## What this is not

- Statutes, regulations, court rules, and constitutional provisions — Westlaw statute books are a different trip; they are not in this queue.
- Existence. Run `npm run citations:lookup` first. Westlaw time is for flags and pins the free funnel left UNRESOLVED.
- A clean bill. *Chavez*, 12 F.4th 978 is KeyCite NONE and still MISCHARACTERIZED.

## Session 1 — do these first (20)

P0 + P1 + the first live-plaintiff leftovers, in that order. Search the **Search** column. Record flag color and, on yellow/red, whether the treatment goes to **your** proposition.

| # | Search | Bucket | Status | Matters |
|---|---|---|---|---|
| 6 | Benavidez v. County of San Diego, 993 F.3d 9 | p0 | UNVERIFIED | 32 |
| 7 | 2025 WL 25549 | p0 | UNVERIFIED | 26 |
| 8 | 574 U.S. 81 | p0 | UNVERIFIED | 26 |
| 9 | 2009 WL 6045700 | p0 | UNVERIFIED | 25 |
| 10 | 2010 WL 3411462 | p0 | UNVERIFIED | 25 |
| 11 | Davenport v. Mutual Ben. Health, 325 F.3d 785 | p0 | UNVERIFIED | 25 |
| 12 | In Aucina v. Amoco Oil Co, 871 F. Supp. 332 | p0 | UNVERIFIED | 25 |
| 13 | Villa v. Maricopa County, 865 F.3d 8 | p0 | UNVERIFIED | 33 |
| 14 | California Highway Patrol v. Superior Court, 158 Cal.App.4th 726 | p1 | MISCHARACTERIZED | 9, 19 |
| 15 | People v. Rizo, 22 Cal.4th 681 | p1 | MISCHARACTERIZED | 9, 19 |
| 16 | Rodriguez v. United States, 575 U.S. 348 | p1 | MISCITED | 1, 32 |
| 17 | In re Hudson, 1 Cal.App.4th 1 | p1 | MISCITED | 5, 15, 19 |
| 18 | Devenpeck v. Alford, 543 U.S. 11 | p1 | MISCITED | 32 |
| 19 | 874 F.2d 1310 | p1 | MISCITED | 24, 32 |
| 20 | 2015 WL 13650018 | p1 | MISCITED | 29 |
| 21 | 2021 WL 1034838 | p1 | MISCITED | 29 |
| 22 | 50 Cal.App.4th 1461 | p1 | MISCITED | 20, 32 |
| 23 | Devenpeck v. Alford, 3 U.S. 146 | p1 | MISCITED | 32 |
| 24 | 2014 WL 2807986 | p1 | MISCITED | 28 |
| 25 | Jessie v. United States, 79 M.J. 437 | p1 | MISCITED | 28 |

## Confirm-absent (search only)

Known fabrications. A miss is the point. Do not open KeyCite. Do not introduce these into a new plaintiff filing.

| Search / label | Status | Matters | Uses |
|---|---|---|---|
| In re Leman, 66 Cal.App.5th 200 | NOT_FOUND | 9, 19 | 9 |
| 2003 WL 23545858 | NOT_FOUND | 7, 32, 33 | 5 |
| 2015 WL 13752958 | NOT_FOUND | 28 | 3 |
| Collins v. Moore, 81 F.3d 167 | NOT_FOUND | 28 | 1 |
| Trinity River v. North Coast Regional Water Quality Control, 184 Cal.App.4th 1466 | UNVERIFIED | 14 | 1 |

## P0 — plaintiff-only UNVERIFIED

| # | Search | Status | Matters | Uses |
|---|---|---|---|---|
| 6 | Benavidez v. County of San Diego, 993 F.3d 9 | UNVERIFIED | 32 | 5 |
| 7 | 2025 WL 25549 | UNVERIFIED | 26 | 3 |
| 8 | 574 U.S. 81 | UNVERIFIED | 26 | 3 |
| 9 | 2009 WL 6045700 | UNVERIFIED | 25 | 1 |
| 10 | 2010 WL 3411462 | UNVERIFIED | 25 | 1 |
| 11 | Davenport v. Mutual Ben. Health, 325 F.3d 785 | UNVERIFIED | 25 | 1 |
| 12 | In Aucina v. Amoco Oil Co, 871 F. Supp. 332 | UNVERIFIED | 25 | 1 |
| 13 | Villa v. Maricopa County, 865 F.3d 8 | UNVERIFIED | 33 | 1 |

## P1 — plaintiff-only bad status

Treatment does not clear MISCITED / MISCHARACTERIZED. Use Westlaw to confirm the real caption/pin and whether anything is still citable at all.

| # | Search | Status | Matters | Uses |
|---|---|---|---|---|
| 14 | California Highway Patrol v. Superior Court, 158 Cal.App.4th 726 | MISCHARACTERIZED | 9, 19 | 15 |
| 15 | People v. Rizo, 22 Cal.4th 681 | MISCHARACTERIZED | 9, 19 | 12 |
| 16 | Rodriguez v. United States, 575 U.S. 348 | MISCITED | 1, 32 | 12 |
| 17 | In re Hudson, 1 Cal.App.4th 1 | MISCITED | 5, 15, 19 | 7 |
| 18 | Devenpeck v. Alford, 543 U.S. 11 | MISCITED | 32 | 5 |
| 19 | 874 F.2d 1310 | MISCITED | 24, 32 | 3 |
| 20 | 2015 WL 13650018 | MISCITED | 29 | 2 |
| 21 | 2021 WL 1034838 | MISCITED | 29 | 2 |
| 22 | 50 Cal.App.4th 1461 | MISCITED | 20, 32 | 2 |
| 23 | Devenpeck v. Alford, 3 U.S. 146 | MISCITED | 32 | 2 |
| 24 | 2014 WL 2807986 | MISCITED | 28 | 1 |
| 25 | Jessie v. United States, 79 M.J. 437 | MISCITED | 28 | 1 |
| 26 | Johnson v. City of Grants Pass, 50 F.4th 787 | MISCITED | 28 | 1 |
| 27 | Lockley v. Law Office, 91 Cal.App.4th 401 | MISCITED | 20, 32 | 1 |
| 28 | Pomona Police Officers' Ass'n v. City of Pomona, 58 Cal.App.4th 578 | MISCHARACTERIZED | 9 | 15 |
| 29 | Home v. Dep't of Health Care Services, 204 Cal.App.4th 676 | MISCITED | 9 | 9 |
| 30 | People v. Superior Court, 25 Cal.4th 703 | MISCITED | 9 | 6 |
| 31 | Caldwell v. Montoya, 10 Cal.4th 972 | MISCITED | 14, 15, 16 | 5 |
| 32 | County of Contra Costa v. State of California, 177 Cal.App.3d 62 | MISCITED | 9 | 3 |

## Live-matter plaintiff filings (not yet KeyCited)

Matters 12, 19, 20, 24–29, 32, 33, 35. Load-bearing first by use count.

| # | Search | Status | Matters | Uses |
|---|---|---|---|---|
| 33 | Mercer v. DMV, 53 Cal.3d 753 | UNVERIFIED | 1, 2, 7, 8, 32, 33 | 57 |
| 34 | Ashcroft v. Iqbal, 556 U.S. 662 | MISCITED | 1, 3, 7, 18, 24, 26, 29, 32, 33 | 42 |
| 35 | Clarke v. Gordon, 104 Cal.App.5th 1267 | VERIFIED | 7, 32, 33 | 40 |
| 36 | Mathews v. Eldridge, 424 U.S. 319 | VERIFIED | 7, 24, 32, 33 | 38 |
| 37 | Goldberg v. Kelly, 397 U.S. 254 | VERIFIED | 7, 24, 32, 33 | 34 |
| 38 | Withrow v. Larkin, 421 U.S. 35 | VERIFIED | 7, 24, 32, 33 | 34 |
| 39 | Knudsen v. DMV, 101 Cal.App.5th 186 | UNVERIFIED | 7, 8, 32, 33 | 32 |
| 40 | Bell Atlantic v. Twombly, 550 U.S. 544 | UNVERIFIED | 1, 3, 7, 18, 24, 26, 29, 32, 33 | 28 |
| 41 | California DUI Lawyers Ass'n v. DMV, 77 Cal.App.5th 517 | UNVERIFIED | 7, 8, 32, 33 | 26 |
| 42 | Villa v. Maricopa County, 865 F.3d 1224 | UNVERIFIED | 7, 32, 33 | 26 |
| 43 | Butz v. Economou, 438 U.S. 478 | VERIFIED | 7, 32, 33 | 22 |
| 44 | Smith v. Wade, 461 U.S. 30 | VERIFIED | 1, 3, 7, 24, 32, 33 | 22 |
| 45 | Franks v. Delaware, 438 U.S. 154 | VERIFIED | 32 | 19 |
| 46 | In re Thompson, 172 Cal.App.3d 256 | VERIFIED | 5, 9, 15, 19 | 19 |
| 47 | Cleavinger v. Saxner, 474 U.S. 193 | VERIFIED | 7, 32, 33 | 18 |
| 48 | Forrester v. White, 484 U.S. 219 | VERIFIED | 7, 32, 33 | 18 |
| 49 | Hope v. Pelzer, 536 U.S. 730 | VERIFIED | 24, 32, 33 | 18 |
| 50 | Topanga v. County of L.A, 11 Cal.3d 506 | UNVERIFIED | 8, 9, 19, 20, 32, 33 | 18 |
| 51 | Nieves v. Bartlett, 587 U.S. 391 | VERIFIED | 24, 32 | 17 |
| 52 | Patsy v. Bd. of Regents, 457 U.S. 496 | VERIFIED | 7, 28, 32, 33 | 17 |
| 53 | Stump v. Sparkman, 435 U.S. 349 | VERIFIED | 7, 8, 32, 33 | 17 |
| 54 | Galbraith v. County of, 307 F.3d 1119 | UNVERIFIED | 18, 29, 32 | 16 |
| 55 | Tameny v. Atl. Richfield Co, 27 Cal.3d 167 | UNVERIFIED | 22, 25, 26, 27 | 16 |
| 56 | 14 Cal.4th 557 | VERIFIED | 9, 15, 19 | 15 |
| 57 | Caperton v. A.T. Massey Coal Co, 556 U.S. 868 | VERIFIED | 33 | 15 |
| 58 | Fermino v. Fedco, 7 Cal.4th 701 | VERIFIED | 5, 15, 35 | 15 |
| 59 | In re Gadlin, 10 Cal.5th 915 | VERIFIED | 9, 19 | 15 |
| 60 | In re Murchison, 349 U.S. 133 | VERIFIED | 33 | 15 |
| 61 | Music v. DMV, 221 Cal.App.3d 841 | UNVERIFIED | 7, 8, 32, 33 | 15 |
| 62 | Costanich v. Dep't of Social, 627 F.3d 1101 | VERIFIED | 32 | 14 |
| 63 | Lopez v. Smith, 203 F.3d 1122 | VERIFIED | 7, 18, 24, 26, 32, 33 | 14 |
| 64 | O'Shea v. Littleton, 414 U.S. 488 | UNVERIFIED | 7, 33 | 14 |
| 65 | Blank v. Kirwan, 39 Cal.3d 311 | UNVERIFIED | 5, 9, 20, 32 | 13 |
| 66 | Chism v. Washington State, 661 F.3d 380 | VERIFIED | 32 | 13 |
| 67 | Devereaux v. Abbey, 263 F.3d 1070 | VERIFIED | 30, 32 | 13 |
| 68 | 20 Cal.4th 163 | UNVERIFIED | 5, 12, 26, 29 | 12 |
| 69 | Brown v. Texas, 443 U.S. 47 | VERIFIED | 1, 2, 7, 8, 32, 33 | 12 |
| 70 | Camara v. Municipal, 387 U.S. 523 | VERIFIED | 32 | 12 |
| 71 | Florida v. Royer, 460 U.S. 491 | VERIFIED | 1, 2, 7, 8, 32, 33 | 12 |
| 72 | Horn v. County of Ventura, 24 Cal.3d 605 | VERIFIED | 9, 19 | 12 |
| 73 | In re Taylor, 60 Cal.4th 1019 | VERIFIED | 9, 19 | 12 |
| 74 | Lacey v. Maricopa County, 693 F.3d 896 | UNVERIFIED | 3, 32, 33 | 12 |
| 75 | McDonnell v. DMV, 45 Cal.App.3d 653 | VERIFIED | 1, 2, 7, 8, 32, 33 | 12 |
| 76 | Terry v. Ohio, 392 U.S. 1 | VERIFIED | 1, 2, 7, 8, 32, 33 | 12 |
| 77 | Wong Sun v. United States, 371 U.S. 471 | VERIFIED | 1, 2, 7, 8, 32, 33 | 12 |
| 78 | 618 F.3d 970 | VERIFIED | 24, 33 | 11 |
| 79 | Ballentine v. Tucker, 28 F.4th 54 | VERIFIED | 32 | 11 |
| 80 | Beck v. Ohio, 379 U.S. 89 | VERIFIED | 32 | 11 |
| 81 | Devenpeck v. Alford, 543 U.S. 146 | MISCITED | 1, 32 | 11 |
| 82 | Haggis v. City of Los Angeles, 22 Cal.4th 490 | UNVERIFIED | 15, 20, 32 | 11 |
| 83 | Mosquito & Vector Control Dist. v. Cal. PERB, 35 Cal.4th 1072 | UNVERIFIED | 5, 9, 19 | 11 |
| 84 | People v. Torres, 173 Cal.App.4th 977 | VERIFIED | 1, 2, 7, 8, 32, 33 | 11 |
| 85 | Pratt v. Rowland, 65 F.3d 802 | VERIFIED | 3, 18, 24, 30 | 11 |
| 86 | Bd. of Cnty. Comm'rs v. Umbehr, 518 U.S. 668 | VERIFIED | 24 | 10 |
| 87 | Bell v. Burson, 402 U.S. 535 | VERIFIED | 7, 32, 33 | 10 |
| 88 | Duryea v. Guarnieri, 564 U.S. 379 | VERIFIED | 24, 32 | 10 |
| 89 | People v. Medina, 6 Cal.3d 484 | VERIFIED | 1, 2, 7, 8, 32, 33 | 10 |
| 90 | Perry v. Sindermann, 408 U.S. 593 | VERIFIED | 24 | 10 |
| 91 | U.S. v. Ritchie, 342 F.3d 903 | UNVERIFIED | 26, 29 | 10 |
| 92 | Verizon Md. Inc. v. Public Serv. Comm'n, 535 U.S. 635 | VERIFIED | 7, 32, 33 | 10 |
| 93 | 142 Cal.App.4th 1046 | VERIFIED | 9, 19 | 9 |
| 94 | Armondo v. Dep't of Motor Vehicles, 15 Cal.App.4th 1174 | VERIFIED | 7, 33 | 9 |
| 95 | Brown v. Illinois, 422 U.S. 590 | VERIFIED | 1, 2, 7, 8, 32, 33 | 9 |
| 96 | Catholic Charities CYO v. Chertoff, 622 F. Supp. 2d 865 | UNVERIFIED | 20, 24, 32 | 9 |
| 97 | In re Lawrence, 44 Cal.4th 1181 | VERIFIED | 9, 19 | 9 |
| 98 | Khoja v. Orexigen Therapeutics, 899 F.3d 988 | VERIFIED | 24, 26, 29 | 9 |
| 99 | Lee v. City of Los Angeles, 250 F.3d 668 | VERIFIED | 18, 24, 29 | 9 |
| 100 | Lungren v. Deukmejian, 45 Cal.3d 727 | VERIFIED | 9, 19 | 9 |
| 101 | Mackey v. Montrym, 443 U.S. 1 | VERIFIED | 7, 32, 33 | 9 |
| 102 | Morrissey v. Brewer, 408 U.S. 471 | VERIFIED | 3, 19, 28, 30 | 9 |
| 103 | Payton v. New York, 445 U.S. 573 | VERIFIED | 32 | 9 |
| 104 | Pearson v. Callahan, 555 U.S. 223 | VERIFIED | 1, 24, 32 | 9 |
| 105 | People v. Lent, 15 Cal.3d 481 | VERIFIED | 5, 14, 15, 19 | 9 |
| 106 | Vlandis v. Kline, 412 U.S. 441 | VERIFIED | 33 | 9 |
| 107 | West v. Atkins, 487 U.S. 42 | VERIFIED | 18, 28 | 9 |
| 108 | Caniglia v. Strom, 593 U.S. 194 | VERIFIED | 32 | 8 |
| 109 | City of Los Angeles v. Lyons, 461 U.S. 95 | UNVERIFIED | 7, 33 | 8 |
| 110 | Ford v. City of Yakima, 706 F.3d 1188 | VERIFIED | 24 | 8 |
| 111 | Gonzalez v. Trevino, 602 U.S. 653 | VERIFIED | 32 | 8 |
| 112 | Greenholtz v. Inmates of Nebraska Penal, 442 U.S. 1 | VERIFIED | 9, 28, 30 | 8 |
| 113 | Hill v. Nat’l Collegiate Athletic Ass’n, 7 Cal.4th 1 | VERIFIED | 5, 26, 27 | 8 |
| 114 | Idaho v. Coeur, 521 U.S. 261 | UNVERIFIED | 7, 33 | 8 |
| 115 | Kavanaugh v. West Sonoma County Union High School, 29 Cal.4th 911 | VERIFIED | 15, 20, 32 | 8 |
| 116 | Knievel v. ESPN, 393 F.3d 1068 | VERIFIED | 24, 29 | 8 |
| 117 | Mullane v. Central, 339 U.S. 306 | VERIFIED | 32 | 8 |
| 118 | Perez Perez v. Wolf, 943 F.3d 853 | VERIFIED | 24 | 8 |
| 119 | Sialoi v. City of San Diego, 823 F.3d 1223 | VERIFIED | 32 | 8 |
| 120 | Sonner v. Premier Nutrition Corp, 971 F.3d 834 | UNVERIFIED | 29 | 8 |
| 121 | United States v. Lopez, 482 F.3d 1067 | VERIFIED | 32 | 8 |
| 122 | United States v. Ngumezi, 980 F.3d 1285 | VERIFIED | 32 | 8 |
| 123 | Hebbe v. Pliler, 627 F.3d 338 | VERIFIED | 7, 24, 26, 32, 33 | 7 |
| 124 | In re Muszalski, 52 Cal.App.3d 500 | VERIFIED | 5, 15, 19 | 7 |
| 125 | Mendoza v. ADP Screening, 182 Cal.App.4th 1644 | VERIFIED | 25, 26, 29 | 7 |
| 126 | Regents v. Roth, 408 U.S. 564 | VERIFIED | 24, 32 | 7 |
| 127 | S v. JSS Scandinavia, 142 F.3d 1150 | VERIFIED | 25, 26 | 7 |
| 128 | Shanks v. Dressel, 540 F.3d 1082 | VERIFIED | 24, 32 | 7 |
| 129 | 284 F.3d 1007 | VERIFIED | 32 | 6 |
| 130 | Bd. of Educ. v. Loudermill, 470 U.S. 532 | VERIFIED | 33 | 6 |
| 131 | Bureerong v. Uvawas, 922 F. Supp. 1450 | VERIFIED | 1, 24, 32 | 6 |
| 132 | Carey v. Piphus, 435 U.S. 247 | VERIFIED | 33 | 6 |
| 133 | Collins v. Virginia, 584 U.S. 586 | VERIFIED | 32 | 6 |
| 134 | Cornell v. City & County, 17 Cal.App.5th 766 | UNVERIFIED | 2, 5, 14, 16, 30, 32 | 6 |
| 135 | Erickson v. Pardus, 551 U.S. 89 | VERIFIED | 18, 24, 26 | 6 |
| 136 | Hartman v. Moore, 547 U.S. 250 | VERIFIED | 24, 30 | 6 |
| 137 | Illinois v. Caballes, 543 U.S. 405 | VERIFIED | 32 | 6 |
| 138 | Jones v. Lodge, 42 Cal.4th 1158 | UNVERIFIED | 20, 32 | 6 |
| 139 | Kay v. Ehrler, 499 U.S. 432 | VERIFIED | 1, 24, 32 | 6 |
| 140 | Kentucky v. King, 563 U.S. 452 | VERIFIED | 32 | 6 |
| 141 | Navarro v. Block, 250 F.3d 729 | UNVERIFIED | 1, 24, 32 | 6 |
| 142 | Neitzke v. Williams, 490 U.S. 319 | VERIFIED | 1, 7, 18, 32, 33 | 6 |
| 143 | Noll v. Carlson, 809 F.2d 1446 | VERIFIED | 24, 26 | 6 |
| 144 | Wilkerson v. Butler, 229 F.R.D. 166 | VERIFIED | 1, 24, 32 | 6 |
| 145 | 2019 WL 6619348 | VERIFIED | 7, 32, 33 | 5 |
| 146 | Barnett v. Fireman's Fund Ins. Co, 90 Cal.App.4th 500 | UNVERIFIED | 20, 32 | 5 |
| 147 | Bd. of Educ. v. Doyle, 429 U.S. 274 | VERIFIED | 24, 30 | 5 |
| 148 | Behan v. Alexis, 116 Cal.App.3d 403 | VERIFIED | 33 | 5 |
| 149 | County of Sacramento v. Lewis, 523 U.S. 833 | VERIFIED | 3, 28 | 5 |
| 150 | Devereaux v. Abbey, 3 F.3d 1070 | VERIFIED | 32 | 5 |
| 151 | District of Columbia v. Wesby, 583 U.S. 48 | VERIFIED | 1, 24, 32 | 5 |
| 152 | Dunaway v. New, 442 U.S. 200 | VERIFIED | 1, 32 | 5 |
| 153 | Foucha v. Louisiana, 504 U.S. 71 | VERIFIED | 28 | 5 |
| 154 | Garity v. APWU Nat'l Lab. Org, 828 F.3d 848 | VERIFIED | 1, 7, 24, 32, 33 | 5 |
| 155 | People v. Pieters, 52 Cal.3d 894 | VERIFIED | 20, 26, 32 | 5 |
| 156 | Winter v. NRDC, 555 U.S. 7 | UNVERIFIED | 24 | 5 |
| 157 | 2022 WL 3030530 | UNVERIFIED | 29 | 4 |
| 158 | Arizona v. Gant, 556 U.S. 332 | VERIFIED | 1, 32 | 4 |
| 159 | California DUI Lawyers Ass'n v. DMV, 11 Cal.App.5th 517 | VERIFIED | 33 | 4 |
| 160 | Capp v. Cnty. of San Diego, 940 F.3d 1046 | VERIFIED | 24 | 4 |
| 161 | Cedars-Sinai Medical Center v. Superior Court, 18 Cal.4th 1 | VERIFIED | 22, 25, 26 | 4 |
| 162 | Chavez v. JPMorgan Chase, 888 F.3d 413 | VERIFIED | 25, 26 | 4 |
| 163 | City of Moorpark v. Superior Court, 18 Cal.4th 1143 | VERIFIED | 25, 26 | 4 |
| 164 | Common Cause v. Board of Supervisors, 49 Cal.3d 432 | UNVERIFIED | 20, 32 | 4 |
| 165 | Dent v. Nat’l Football League, 902 F.3d 1109 | VERIFIED | 26 | 4 |
| 166 | Fritsch v. Swift Transp. Co, 899 F.3d 785 | VERIFIED | 25, 26 | 4 |
| 167 | Guzman v. Polaris Industries Inc, 49 F.4th 1308 | VERIFIED | 29 | 4 |
| 168 | Harlow v. Fitzgerald, 457 U.S. 800 | VERIFIED | 7, 32, 33 | 4 |
| 169 | Kanter v. Warner-Lambert Co, 265 F.3d 853 | VERIFIED | 25, 26 | 4 |
| 170 | Keates v. Koile, 883 F.3d 1228 | VERIFIED | 24 | 4 |
| 171 | Kenneth Rothschild Trust v. Morgan Stanley Dean Witter, 199 F. Supp. 2d 993 | VERIFIED | 25, 26 | 4 |
| 172 | Lathus v. City of Huntington Beach, 56 F.4th 1238 | UNVERIFIED | 7, 24, 32, 33 | 4 |
| 173 | Lew v. Moss, 797 F.2d 747 | VERIFIED | 25, 26 | 4 |
| 174 | Marder v. Lopez, 450 F.3d 445 | UNVERIFIED | 29 | 4 |
| 175 | Mir v. Little Co, 844 F.2d 646 | VERIFIED | 26, 29 | 4 |
| 176 | Podolsky v. First Healthcare Corp, 50 Cal.App.4th 632 | VERIFIED | 26 | 4 |
| 177 | Quelimane Co. v. Stewart Title Guaranty Co, 19 Cal.4th 26 | UNVERIFIED | 20, 32 | 4 |
| 178 | Quinn v. Coulton, 121 Cal.App.5th 1124 | VERIFIED | 26 | 4 |
| 179 | Williams v. Sacramento River Cats Baseball Club, 40 Cal.App.5th 280 | VERIFIED | 26 | 4 |
| 180 | 2018 WL 1567796 | UNVERIFIED | 26 | 3 |
| 181 | 2024 WL 6473762 | UNVERIFIED | 26 | 3 |
| 182 | Abrego Abrego v. Dow Chemical Co, 443 F.3d 676 | UNVERIFIED | 29 | 3 |
| 183 | Accardi v. Shaughnessy, 347 U.S. 260 | VERIFIED | 19 | 3 |
| 184 | Alfaro v. Superior Ct, 58 Cal.App.5th 371 | UNVERIFIED | 26 | 3 |
| 185 | Ashelman v. Pope, 793 F.2d 1072 | VERIFIED | 33 | 3 |
| 186 | Bily v. Arthur Young, 3 Cal.4th 370 | VERIFIED | 5, 12 | 3 |
| 187 | Board of Pardons v. Allen, 482 U.S. 369 | VERIFIED | 19 | 3 |
| 188 | California v. Acevedo, 500 U.S. 565 | VERIFIED | 32 | 3 |
| 189 | California v. Carney, 471 U.S. 386 | VERIFIED | 32 | 3 |
| 190 | Cardenas v. Cnty. of Tehama, 476 F. Supp. 3d 1055 | UNVERIFIED | 26 | 3 |
| 191 | Conroy v. Regents of, 45 Cal.4th 1244 | UNVERIFIED | 26 | 3 |
| 192 | Franklin v. Murphy, 745 F.2d 1221 | VERIFIED | 7, 18, 24, 32, 33 | 3 |
| 193 | Gantt v. Sentry Insurance, 1 Cal.4th 1083 | VERIFIED | 27 | 3 |
| 194 | Gonzales v. CarMax Auto Superstores, 840 F.3d 644 | VERIFIED | 26 | 3 |
| 195 | In Hertz Corp. v. Friend, 130 S. Ct. 1181 | VERIFIED | 26 | 3 |
| 196 | In re Clark, 5 Cal.4th 750 | VERIFIED | 19 | 3 |
| 197 | In re Marzec, 25 Cal.2d 794 | VERIFIED | 19 | 3 |
| 198 | In re Sturm, 11 Cal.3d 258 | VERIFIED | 19 | 3 |
| 199 | Khan v. CitiMortgage, 975 F. Supp. 2d 1127 | UNVERIFIED | 26 | 3 |
| 200 | Loehr v. Ventura County Community College Dist, 147 Cal.App.3d 1071 | VERIFIED | 14, 20, 32 | 3 |
| 201 | Miller v. Gammie, 335 F.3d 889 | VERIFIED | 33 | 3 |
| 202 | Mireles v. Waco, 502 U.S. 9 | VERIFIED | 7, 32, 33 | 3 |
| 203 | Napear v. Bonneville Int’l Corp, 669 F. Supp. 3d 948 | UNVERIFIED | 26 | 3 |
| 204 | New York v. Class, 475 U.S. 106 | VERIFIED | 32 | 3 |
| 205 | Orosco v. Napolitano, 598 F.3d 222 | VERIFIED | 2, 24, 32 | 3 |
| 206 | Owens v. Huntling, 115 F.2d 160 | VERIFIED | 26 | 3 |
| 207 | Parrino v. FHP, 146 F.3d 699 | UNVERIFIED | 29 | 3 |
| 208 | Quiroz v. Seventh Ave. Ctr, 140 Cal.App.4th 1256 | UNVERIFIED | 26 | 3 |
| 209 | Rubio v. Capital One Bank, 572 F. Supp. 2d 1157 | UNVERIFIED | 26 | 3 |
| 210 | Saleh v. Nike, 562 F. Supp. 3d 503 | UNVERIFIED | 26 | 3 |
| 211 | Shvarts v. Budget Group, 81 Cal.App.4th 1153 | UNVERIFIED | 26 | 3 |
| 212 | Smith v. State Farm Mutual Automobile Ins. Co, 93 Cal.App.4th 700 | UNVERIFIED | 26 | 3 |
| 213 | Soliman v. Philip Morris Inc, 311 F.3d 966 | VERIFIED | 26 | 3 |
| 214 | Station & Auto. Repair Ass’n v. Am. Home Assur. Co, 62 Cal.App.4th 1166 | UNVERIFIED | 26 | 3 |
| 215 | United States v. Knights, 534 U.S. 112 | VERIFIED | 19 | 3 |
| 216 | Urbino v. Orkins Servs. Of Cal., 726 F.3d 1118 | VERIFIED | 26 | 3 |
| 217 | 2012 WL 3101659 | VERIFIED | 29 | 2 |
| 218 | 2013 WL 3205426 | VERIFIED | 29 | 2 |
| 219 | 2015 WL 12681650 | VERIFIED | 29 | 2 |
| 220 | Arizona v. Gant, 556 U.S 26 (2009) | VERIFIED | 32 | 2 |
| 221 | Ashcroft v. Iqbal, 556 U.S. 678 | VERIFIED | 1, 32 | 2 |
| 222 | Ballentine v. Tucker, 17 F.4th 54 | VERIFIED | 32 | 2 |
| 223 | Beck v. Ohio, 79 U.S. 89 | VERIFIED | 32 | 2 |
| 224 | Bunnett v. Regents of University, 35 Cal.App.4th 843 | VERIFIED | 20, 32 | 2 |
| 225 | Burns v. Windsor Ins. Co, 31 F.3d 1092 | VERIFIED | 25 | 2 |
| 226 | Carloss v. County of Alameda, 242 Cal.App.4th 116 | VERIFIED | 20, 32 | 2 |
| 227 | Cervantes v. City of San Diego, 5 F.3d 1273 | VERIFIED | 29 | 2 |
| 228 | Chambers v. Herrera, 78 F.4th 1100 | UNVERIFIED | 1, 32 | 2 |
| 229 | Collins v. Virginia, 17 U.S. 586 | VERIFIED | 32 | 2 |
| 230 | County of Sacramento v. Lewis, 523 U.S. 10 | VERIFIED | 24, 32 | 2 |
| 231 | Daniels-Hall v. Nat’l Educ. Ass’n, 629 F.3d 992 | VERIFIED | 29 | 2 |
| 232 | Epstein v. Washington Energy Co, 83 F.3d 1136 | VERIFIED | 29 | 2 |
| 233 | Goldberg v. Kelly, 391 U.S. 254 | VERIFIED | 24, 32 | 2 |
| 234 | Hartman v. Moore, 541 U.S. 250 | VERIFIED | 24, 32 | 2 |
| 235 | Holt v. Kelly, 20 Cal.3d 560 | VERIFIED | 20, 32 | 2 |
| 236 | Love v. United States, 915 F.2d 1242 | VERIFIED | 29 | 2 |
| 237 | Nanty v. Barrows Co, 660 F.2d 1327 | VERIFIED | 29 | 2 |
| 238 | O'Day v. McDonnell Douglas Helicopter Co, 79 F.3d 756 | VERIFIED | 29 | 2 |
| 239 | Orion Tire Corp. v. Goodyear Tire, 268 F.3d 1133 | VERIFIED | 29 | 2 |
| 240 | Payton v. New York, 445 U.S. 26 | VERIFIED | 32 | 2 |
| 241 | SN Sands Corp. v. City and County, 167 Cal.App.4th 185 | VERIFIED | 20, 32 | 2 |
| 242 | Saleeby v. State Bar, 39 Cal.3d 547 | VERIFIED | 20, 32 | 2 |
| 243 | Serrano v. Francis, 345 F.3d 1071 | VERIFIED | 3, 28 | 2 |
| 244 | Shoyoye v. County of Los Angeles, 203 Cal.App.4th 947 | VERIFIED | 2, 30, 32 | 2 |
| 245 | Sonner v. Premier Nutrition Corporation, 49 F.4th 1300 | VERIFIED | 29 | 2 |
| 246 | Warner Constr. Corp. v. City of Los Angeles, 2 Cal.3d 285 | VERIFIED | 12 | 2 |
| 247 | White v. Ultramar, 21 Cal.4th 563 | UNVERIFIED | 5, 12 | 2 |
| 248 | 2005 WL 2435900 | VERIFIED | 29 | 1 |
| 249 | 805 F. Supp. 2d 932 | VERIFIED | 29 | 1 |
| 250 | Angus v. Shiley, 989 F.2d 142 | VERIFIED | 25 | 1 |
| 251 | Arias v. Residence Inn, 936 F.3d 920 | VERIFIED | 25 | 1 |
| 252 | Bernson v. Browning-Ferris Industries, 7 Cal.4th 926 | VERIFIED | 12 | 1 |
| 253 | Bias v. Moynihan, 508 F.3d 1212 | VERIFIED | 29 | 1 |
| 254 | Caperton v. A.T. Massey Coal Co, 556 U.S. 15 | VERIFIED | 33 | 1 |
| 255 | Cleveland v. Johnson, 209 Cal.App.4th 1315 | VERIFIED | 12 | 1 |
| 256 | Edmo v. Corizon, 935 F.3d 757 | VERIFIED | 28 | 1 |
| 257 | Exxon Mobil Corp. v. Saudi Basic Indus. Corp, 544 U.S. 280 | VERIFIED | 7, 32, 33 | 1 |
| 258 | Florida v. Wells, 495 U.S. 1 | VERIFIED | 32 | 1 |
| 259 | Fox v. Ethicon Endo-Surgery, 35 Cal.4th 797 | VERIFIED | 12 | 1 |
| 260 | Gibson v. Chrysler Corp, 261 F.3d 927 | VERIFIED | 25 | 1 |
| 261 | Goldberg v. CPC Int’l, 678 F.2d 1365 | VERIFIED | 25 | 1 |
| 262 | Griffin v. Green Tree Servicing, 166 F. Supp. 3d 1030 | VERIFIED | 29 | 1 |
| 263 | Guglielmino v. McKee Foods Corp, 506 F.3d 696 | VERIFIED | 25 | 1 |
| 264 | Hagan v. Khoja, 139 S. Ct. 2615 | VERIFIED | 29 | 1 |
| 265 | Helm v. Alderwoods Group, 696 F. Supp. 2d 1057 | VERIFIED | 29 | 1 |
| 266 | Herr v. Nestle U.S.A., 109 Cal.App.4th 779 | VERIFIED | 29 | 1 |
| 267 | Hertz Corp. v. Friend, 559 U.S. 77 | VERIFIED | 25 | 1 |
| 268 | Hunter v. Bryant, 502 U.S. 224 | VERIFIED | 1, 32 | 1 |
| 269 | Jones v. Sutter Health, 499 F. Supp. 3d 704 | VERIFIED | 29 | 1 |
| 270 | Kantor v. Wellesley Galleries, 704 F.2d 1088 | VERIFIED | 25 | 1 |
| 271 | Kougasian v. TMSL, 359 F.3d 1136 | VERIFIED | 7, 32, 33 | 1 |
| 272 | Lewis v. Verizon Commc’ns, 627 F.3d 395 | VERIFIED | 25 | 1 |
| 273 | LiMandri v. Judkins, 52 Cal.App.4th 326 | VERIFIED | 12 | 1 |
| 274 | MGIC Indem. Corp. v. Weisman, 803 F.2d 500 | VERIFIED | 29 | 1 |
| 275 | Mack v. South Bay Beer Distribs, 798 F.2d 1279 | VERIFIED | 29 | 1 |
| 276 | Marks v. Minnesota Mining, 187 Cal.App.3d 1429 | VERIFIED | 12 | 1 |
| 277 | McKell v. Washington Mut., 142 Cal.App.4th 1457 | VERIFIED | 29 | 1 |
| 278 | Mesler v. Bragg Management Co, 39 Cal.3d 290 | VERIFIED | 12 | 1 |
| 279 | Missouri v. McNeely, 569 U.S. 141 | VERIFIED | 32 | 1 |
| 280 | Monroe v. Pape, 365 U.S. 167 | VERIFIED | 7, 32, 33 | 1 |
| 281 | Neilson v. Union Bank, 290 F. Supp. 2d 1101 | VERIFIED | 29 | 1 |
| 282 | Notice of Removal. Savelson v. W. States Bankcard Ass’n, 731 F.2d 1423 | VERIFIED | 25 | 1 |
| 283 | People v. Medina, 12 Cal.3d 484 | VERIFIED | 33 | 1 |
| 284 | People v. Preslie, 70 Cal.App.3d 486 | VERIFIED | 20, 32 | 1 |
| 285 | People v. Torres, 11 Cal.App.4th 977 | VERIFIED | 33 | 1 |
| 286 | Pinard v. Clatskanie Sch. Dist, 467 F.3d 755 | VERIFIED | 24 | 1 |
| 287 | Rabago-Alvarez v. Dart Industries, 55 Cal.App.3d 91 | VERIFIED | 25 | 1 |
| 288 | Ray v. Alad Corp, 19 Cal.3d 22 | VERIFIED | 12 | 1 |
| 289 | Sanchez v. Monumental Life Ins. Co, 102 F.3d 398 | VERIFIED | 25 | 1 |
| 290 | Sav. & Loan Ass’n v. Solimino, 501 U.S. 104 | VERIFIED | 29 | 1 |
| 291 | Simmons v. PCR Technology, 209 F. Supp. 2d 1029 | VERIFIED | 25 | 1 |
| 292 | Smith v. Brown-Forman Distillers Corp, 196 Cal.App.3d 503 | VERIFIED | 25 | 1 |
| 293 | Sonora Diamond Corp. v. Superior Court, 83 Cal.App.4th 523 | VERIFIED | 12 | 1 |
| 294 | State Farm Mut. Auto Ins. Co. v. Dyer, 19 F.3d 514 | VERIFIED | 25 | 1 |
| 295 | Swift v. California, 384 F.3d 28 | VERIFIED | 33 | 1 |
| 296 | Tsao v. Desert Palace, 698 F.3d 1128 | VERIFIED | 28 | 1 |
| 297 | United States Small Bus. Admin. v. Bensal, 853 F.3d 992 | VERIFIED | 29 | 1 |
| 298 | United States v. Reyna-Tapia, 328 F.3d 1114 | VERIFIED | 7, 32, 33 | 1 |
| 299 | United States v. Sanchez-Gomez, 859 F.3d 649 | VERIFIED | 28 | 1 |
| 300 | United States v. Wilson, 631 F.2d 118 | VERIFIED | 29 | 1 |
| 301 | White v. FCI USA, 319 F.3d 672 | VERIFIED | 25 | 1 |
| 302 | Williams v. Superior Court, 5 Cal.4th 337 | VERIFIED | 2, 32 | 1 |

## Other plaintiff filings (closed / archived matters)

| # | Search | Status | Matters | Uses |
|---|---|---|---|---|
| 303 | Aryeh v. Canon Business Solutions, 55 Cal.4th 1185 | VERIFIED | 15 | 15 |
| 304 | Sullivan v. County of Los Angeles, 12 Cal.3d 710 | UNVERIFIED | 15 | 13 |
| 305 | Hughes v. Pair, 46 Cal.4th 1035 | VERIFIED | 5, 15, 16, 30 | 11 |
| 306 | Alcorn v. Anbro Engineering, 2 Cal.3d 493 | UNVERIFIED | 5, 15, 16 | 10 |
| 307 | AIDS Healthcare Foundation v. L.A. County Dept, 197 Cal.App.4th 693 | VERIFIED | 9 | 9 |
| 308 | Rodriguez v. Solis, 1 Cal.App.4th 495 | VERIFIED | 9 | 9 |
| 309 | Rhodes v. Robinson, 408 F.3d 559 | VERIFIED | 3, 18, 30 | 7 |
| 310 | Hotel & Motel Ass'n v. Industrial Welfare Comm'n, 25 Cal.3d 200 | VERIFIED | 9 | 6 |
| 311 | Morris v. Williams, 67 Cal.2d 733 | VERIFIED | 9 | 6 |
| 312 | In re Crow, 4 Cal.3d 613 | UNVERIFIED | 5, 9 | 4 |
| 313 | Monell v. Dept. of Soc. Servs, 436 U.S. 658 | VERIFIED | 9 | 4 |
| 314 | Sosinsky v. Grant, 6 Cal.App.4th 1548 | VERIFIED | 5 | 4 |
| 315 | Wright v. State of California, 122 Cal.App.4th 659 | VERIFIED | 5, 10 | 4 |
| 316 | Brodheim v. Cry, 584 F.3d 1262 | VERIFIED | 3, 18, 30 | 3 |
| 317 | Day v. Sharp, 50 Cal.App.3d 904 | UNVERIFIED | 5 | 3 |
| 318 | England v. Louisiana State Bd, 375 U.S. 411 | VERIFIED | 9 | 3 |
| 319 | Foster v. Sexton, 61 Cal.App.5th 998 | UNVERIFIED | 5 | 3 |
| 320 | In re Faucette, 253 Cal.App.2d 338 | UNVERIFIED | 9 | 3 |
| 321 | In re Stevens, 119 Cal.App.4th 1228 | VERIFIED | 5, 15 | 3 |
| 322 | In re Walters, 15 Cal.3d 738 | UNVERIFIED | 9 | 3 |
| 323 | Lazar v. Superior Court, 12 Cal.4th 631 | VERIFIED | 5, 16, 36 | 3 |
| 324 | Lockley v. Law Office, 91 Cal.App.4th 875 | MISCITED | 5 | 3 |
| 325 | McCorkle v. City of Los Angeles, 70 Cal.2d 252 | VERIFIED | 15 | 3 |
| 326 | Spencer v. Peters, 857 F.3d 789 | VERIFIED | 30 | 3 |
| 327 | Thornton v. Brown, 757 F.3d 834 | VERIFIED | 30 | 3 |
| 328 | Aaronoff v. Martinez-Senftner, 136 Cal.App.4th 910 | UNVERIFIED | 5 | 2 |
| 329 | Bardin v. DaimlerChrysler Corp, 136 Cal.App.4th 1255 | UNVERIFIED | 5 | 2 |
| 330 | Drum v. San Fernando Valley Bar Assn, 182 Cal.App.4th 247 | UNVERIFIED | 5 | 2 |
| 331 | Elsner v. Uveges, 34 Cal.4th 915 | UNVERIFIED | 5 | 2 |
| 332 | Hahn v. Mirda, 147 Cal.App.4th 740 | UNVERIFIED | 5 | 2 |
| 333 | Herrera v. Deutsche Bank National Trust Co, 196 Cal.App.4th 1366 | UNVERIFIED | 5 | 2 |
| 334 | In re Estrada, 47 Cal.App.4th 1688 | UNVERIFIED | 5 | 2 |
| 335 | Joslin v. H.A.S. Ins. Brokerage, 184 Cal.App.3d 369 | VERIFIED | 5 | 2 |
| 336 | Landeros v. Flood, 17 Cal.3d 399 | UNVERIFIED | 5 | 2 |
| 337 | Mangini v. R.J. Reynolds Tobacco Co, 7 Cal.4th 1057 | VERIFIED | 5 | 2 |
| 338 | People v. Woodell, 17 Cal.4th 448 | VERIFIED | 5 | 2 |
| 339 | Ross v. Creel Printing, 100 Cal.App.4th 736 | VERIFIED | 5 | 2 |
| 340 | Silva v. Di Vittorio, 658 F.3d 1090 | VERIFIED | 30 | 2 |
| 341 | Taylor v. Superior Court, 24 Cal.3d 890 | UNVERIFIED | 5 | 2 |
| 342 | Wilkinson v. Dotson, 544 U.S. 74 | VERIFIED | 5 | 2 |
| 343 | 200 Cal.App.4th 1470 | VERIFIED | 5 | 1 |
| 344 | 2025 WL 2916303 | VERIFIED | 3 | 1 |
| 345 | 461 U.S. 731 | VERIFIED | 30 | 1 |
| 346 | Bolkiah v. Superior Ct, 74 Cal.App.4th 984 | VERIFIED | 3 | 1 |
| 347 | California Motor Transport Co. v. Trucking Unlimited, 404 U.S. 508 | VERIFIED | 30 | 1 |
| 348 | Citizens for Sensible Planning v. City of Stockton, 48 Cal.4th 481 | VERIFIED | 5 | 1 |
| 349 | Clark County Sch. Dist. v. Breeden, 532 U.S. 268 | VERIFIED | 30 | 1 |
| 350 | Coszalter v. City of Salem, 320 F.3d 968 | VERIFIED | 30 | 1 |
| 351 | Fremont Indem. Co. v. Fremont General Corp, 148 Cal.App.4th 97 | VERIFIED | 5 | 1 |
| 352 | Friends of Mammoth v. Town of Mammoth Lakes Redevelopment Agency, 82 Cal.App.4th 511 | VERIFIED | 5 | 1 |
| 353 | Gilliam v. L.A. Municipal Court, 97 Cal.App.3d 704 | VERIFIED | 9 | 1 |
| 354 | Heck v. Humphrey, 512 U.S. 477 | VERIFIED | 30 | 1 |
| 355 | In re Arias, 42 Cal.3d 667 | VERIFIED | 9 | 1 |
| 356 | Jones v. Kmart Corp, 17 Cal.4th 329 | VERIFIED | 30 | 1 |
| 357 | Milhouse v. Carlson, 652 F.2d 371 | VERIFIED | 30 | 1 |
| 358 | Moser v. Benefytt, 8 F.4th 872 | VERIFIED | 3 | 1 |
| 359 | Paul v. Davis, 424 U.S. 693 | VERIFIED | 30 | 1 |
| 360 | Potter v. Firestone Tire, 6 Cal.4th 965 | VERIFIED | 30 | 1 |
| 361 | Sheppard v. Morgan Keegan, 218 Cal.App.3d 61 | VERIFIED | 36 | 1 |
| 362 | Stevens v. Superior Court, 75 Cal.App.4th 594 | VERIFIED | 5 | 1 |
| 363 | Swift v. California Department, 116 Cal.App.4th 1365 | VERIFIED | 30 | 1 |
| 364 | Toscano v. Greene Music, 124 Cal.App.4th 685 | VERIFIED | 36 | 1 |
| 365 | Venegas v. County of Los Angeles, 153 Cal.App.4th 1230 | VERIFIED | 30 | 1 |
| 366 | Villiarimo v. Aloha Island Air, 281 F.3d 1054 | VERIFIED | 30 | 1 |
| 367 | Zahrey v. Coffey, 221 F.3d 342 | VERIFIED | 30 | 1 |

## Court / opposing / research only

Flag-glance if a session has leftover views. Do not spend deep-reads here until the plaintiff buckets are empty.

| # | Search | Status | Matters | Uses |
|---|---|---|---|---|
| 368 | Kim v. Westmoore Partners, 201 Cal.App.4th 267 | UNVERIFIED | 12 | 11 |
| 369 | Richardson v. McKnight, 521 U.S. 399 | VERIFIED | 28 | 11 |
| 370 | People v. Thompson, 38 Cal.4th 811 | UNVERIFIED | 20, 24, 32 | 10 |
| 371 | Garber & Assocs. v. Eskandarian, 150 Cal.App.4th 813 | UNVERIFIED | 12 | 9 |
| 372 | Espinoza v. Shiomoto, 10 Cal.App.5th 85 | UNVERIFIED | 20, 24, 32 | 8 |
| 373 | Redfearn v. Trader Joe's Co, 20 Cal.App.5th 989 | UNVERIFIED | 20, 24, 32 | 8 |
| 374 | Aubry v. Tri-City Hosp. Dist, 2 Cal.4th 962 | UNVERIFIED | 5, 20, 24, 32 | 7 |
| 375 | Filarsky v. Delia, 566 U.S. 377 | VERIFIED | 28 | 7 |
| 376 | Griset v. Fair Political Practices Commission, 25 Cal.4th 688 | UNVERIFIED | 20, 32 | 7 |
| 377 | Ramirez v. Cnty. of San Bernardino, 806 F.3d 1002 | UNVERIFIED | 18, 33 | 7 |
| 378 | 896 F.2d 1542 | UNVERIFIED | 33 | 6 |
| 379 | Barnes v. AT, 718 F. Supp. 2d 1167 | UNVERIFIED | 33 | 6 |
| 380 | Del E. Webb Corp. v. Structural Materials Co, 123 Cal.App.3d 593 | UNVERIFIED | 20, 24, 32 | 6 |
| 381 | Foltz v. State Farm Mut. Auto. Ins. Co, 331 F.3d 1122 | VERIFIED | 28, 29 | 6 |
| 382 | Goncharov v. Uber Techs., 19 Cal.App.5th 1157 | UNVERIFIED | 20, 24, 32 | 6 |
| 383 | Jensen v. Lane County, 222 F.3d 570 | VERIFIED | 3, 28 | 6 |
| 384 | Sch. & Hosp. v. Halderman, 465 U.S. 89 | UNVERIFIED | 7, 33 | 6 |
| 385 | Starr v. Baca, 652 F.3d 1202 | UNVERIFIED | 3, 18, 29 | 6 |
| 386 | Will v. Michigan Dept, 491 U.S. 58 | VERIFIED | 1, 32, 33 | 6 |
| 387 | 2024 WL 4163081 | VERIFIED | 7, 8, 32, 33 | 5 |
| 388 | 35 Cal.3d 197 | UNVERIFIED | 5, 20, 32 | 5 |
| 389 | Albright v. Oliver, 510 U.S. 266 | UNVERIFIED | 3, 24 | 5 |
| 390 | Greenup v. Rodman, 42 Cal.3d 822 | UNVERIFIED | 12 | 5 |
| 391 | North Oakland Medical Clinic v. Rogers, 65 Cal.App.4th 824 | UNVERIFIED | 12 | 5 |
| 392 | People v. Sanders, 31 Cal.4th 318 | VERIFIED | 7, 8, 32, 33 | 5 |
| 393 | Wyatt v. Cole, 504 U.S. 158 | VERIFIED | 28 | 5 |
| 394 | Clark v. Am. Honda Motor Co, 528 F. Supp. 3d 1108 | UNVERIFIED | 29 | 4 |
| 395 | County of San Diego v. State of California, 164 Cal.App.4th 580 | UNVERIFIED | 20, 32 | 4 |
| 396 | Felder v. Casey, 487 U.S. 131 | UNVERIFIED | 33 | 4 |
| 397 | Ferdik v. Bonzelet, 963 F.2d 1258 | UNVERIFIED | 33 | 4 |
| 398 | Florer v. Congregation Pidyon Shevuyim, 639 F.3d 916 | UNVERIFIED | 3, 24 | 4 |
| 399 | Franklin v. Fox, 312 F.3d 423 | VERIFIED | 3, 28 | 4 |
| 400 | Halvorsen v. Baird, 146 F.3d 680 | VERIFIED | 28 | 4 |
| 401 | Hamilton v. Shearson-Lehman American Express, 813 F.2d 1532 | UNVERIFIED | 1, 3, 6, 7, 32, 33 | 4 |
| 402 | Hansen v. Black, 885 F.2d 642 | VERIFIED | 3, 18, 24 | 4 |
| 403 | Martinez v. California, 444 U.S. 277 | UNVERIFIED | 33 | 4 |
| 404 | Phillips v. Gen. Motors Corp, 307 F.3d 1206 | MISCITED | 28, 29 | 4 |
| 405 | Sprewell v. Golden State Warriors, 266 F.3d 979 | UNVERIFIED | 29 | 4 |
| 406 | Vitek v. Jones, 445 U.S. 480 | VERIFIED | 28 | 4 |
| 407 | Wyshak v. City Nat'l Bank, 607 F.2d 824 | UNVERIFIED | 33 | 4 |
| 408 | Yvanova v. New Century Mortg. Corp, 62 Cal.4th 919 | UNVERIFIED | 20, 32 | 4 |
| 409 | 2009 WL 980417 | UNVERIFIED | 29 | 3 |
| 410 | 2017 WL 7049527 | UNVERIFIED | 29 | 3 |
| 411 | 2019 WL 4243221 | UNVERIFIED | 29 | 3 |
| 412 | 234 Cal.App.4th 166 | UNVERIFIED | 20, 32 | 3 |
| 413 | Benavidez v. County of San Diego, 993 F.3d 1134 | UNVERIFIED | 32 | 3 |
| 414 | Clark v. Superior Court, 50 Cal.4th 605 | UNVERIFIED | 29 | 3 |
| 415 | Commercial Space Mgmt. Co. v. Boeing Co, 193 F.3d 1074 | UNVERIFIED | 1, 6, 7, 32, 33 | 3 |
| 416 | Crowe v. County of San Diego, 608 F.3d 406 | UNVERIFIED | 1, 32 | 3 |
| 417 | Fantasy Inc. v. Fogerty, 984 F.2d 1524 | UNVERIFIED | 24, 33 | 3 |
| 418 | In re Tobacco Cases II, 240 Cal.App.4th 779 | UNVERIFIED | 29 | 3 |
| 419 | Johnson v. Duffy, 588 F.2d 740 | VERIFIED | 18, 24 | 3 |
| 420 | Kamakana v. City and Cnty, 447 F.3d 1172 | UNVERIFIED | 29 | 3 |
| 421 | Katzberg v. Regents of Univ, 29 Cal.4th 300 | UNVERIFIED | 33 | 3 |
| 422 | People v. Reyes, 195 Cal.App.4th 946 | UNVERIFIED | 1, 2, 7, 8, 32, 33 | 3 |
| 423 | Pinto Lake MHP LLC v. County of Santa Cruz, 56 Cal.App.5th 1006 | UNVERIFIED | 20, 32 | 3 |
| 424 | Somers v. Apple Inc, 729 F.3d 953 | UNVERIFIED | 3, 29 | 3 |
| 425 | Thomas v. Dillard, 818 F.3d 864 | UNVERIFIED | 32 | 3 |
| 426 | U.S. v. Corinthian Colleges, 655 F.3d 984 | UNVERIFIED | 29 | 3 |
| 427 | W. Mining Council v. Watt, 643 F.2d 618 | UNVERIFIED | 7, 29, 33 | 3 |
| 428 | 12 Cal.App.5th 1043 | UNVERIFIED | 20, 32 | 2 |
| 429 | 132 Cal.App.4th 1076 | UNVERIFIED | 20, 32 | 2 |
| 430 | 2009 WL 3517617 | UNVERIFIED | 33 | 2 |
| 431 | 2010 WL 1452853 | UNVERIFIED | 29 | 2 |
| 432 | 2011 WL 5976239 | UNVERIFIED | 29 | 2 |
| 433 | 2011 WL 607087 | UNVERIFIED | 24 | 2 |
| 434 | 2012 WL 1029425 | UNVERIFIED | 33 | 2 |
| 435 | 2015 WL 5264750 | UNVERIFIED | 29 | 2 |
| 436 | 2018 WL 2431473 | UNVERIFIED | 29 | 2 |
| 437 | 2019 WL 6838705 | UNVERIFIED | 29 | 2 |
| 438 | 223 Cal.App.4th 149 | UNVERIFIED | 20, 32 | 2 |
| 439 | 28 Cal.App.5th 923 | UNVERIFIED | 29 | 2 |
| 440 | 368 F.3d 1053 | UNVERIFIED | 29 | 2 |
| 441 | 9 Cal.5th 279 | UNVERIFIED | 29 | 2 |
| 442 | 96 Cal.App.4th 824 | UNVERIFIED | 20, 32 | 2 |
| 443 | Aldaco v. RentGrow, 921 F.3d 685 | UNVERIFIED | 29 | 2 |
| 444 | Allen v. City of Beverly Hills, 911 F.2d 367 | UNVERIFIED | 29 | 2 |
| 445 | Alvarez v. Chevron Corp, 656 F.3d 925 | UNVERIFIED | 29 | 2 |
| 446 | Asgari v. City of Los Angeles, 15 Cal.4th 744 | UNVERIFIED | 2, 5, 32 | 2 |
| 447 | Berger v. California Ins. Guarantee Ass’n, 128 Cal.App.4th 989 | UNVERIFIED | 20, 32 | 2 |
| 448 | Berlinghieri v. DMV, 33 Cal.3d 392 | UNVERIFIED | 8, 33 | 2 |
| 449 | Blatty v. New York Times Co, 42 Cal.3d 1033 | UNVERIFIED | 20, 32 | 2 |
| 450 | Broam v. Bogan, 320 F.3d 1023 | UNVERIFIED | 24 | 2 |
| 451 | CLEMENT v. GLENDALE, 518 F.3d 1090 | VERIFIED | 28 | 2 |
| 452 | Cisneros v. U.D. Registry, 39 Cal.App.4th 548 | UNVERIFIED | 29 | 2 |
| 453 | Cleveland v. Groceryworks.com, 200 F. Supp. 3d 924 | UNVERIFIED | 29 | 2 |
| 454 | Collins v. Thurmond, 41 Cal.App.5th 879 | UNVERIFIED | 20, 32 | 2 |
| 455 | Concha v. London, 62 F.3d 1493 | UNVERIFIED | 1, 7, 32, 33 | 2 |
| 456 | Condit v. Dunne, 225 F.R.D. 100 | MISCITED | 28 | 2 |
| 457 | Consumer Data Indus. Ass’n v. Frey, 495 F. Supp. 3d 10 | UNVERIFIED | 29 | 2 |
| 458 | County of Los Angeles v. City of Los Angeles, 214 Cal.App.4th 643 | UNVERIFIED | 20, 32 | 2 |
| 459 | Cunha v. IntelliCheck, 254 F. Supp. 3d 1124 | UNVERIFIED | 29 | 2 |
| 460 | Eel River v. North Coast Railroad Authority, 3 Cal.5th 677 | UNVERIFIED | 29 | 2 |
| 461 | Gomez v. Toledo, 446 U.S. 635 | UNVERIFIED | 33 | 2 |
| 462 | Hadley v. Kellogg Sales Co, 243 F. Supp. 3d 1074 | UNVERIFIED | 29 | 2 |
| 463 | Hafer v. Melo, 502 U.S. 21 | UNVERIFIED | 33 | 2 |
| 464 | Harris v. Aguayo, 11 Cal.App.5th 1150 | UNVERIFIED | 29 | 2 |
| 465 | Holland v. Morse Diesel Int’l, 86 Cal.App.4th 1443 | UNVERIFIED | 20, 32 | 2 |
| 466 | In re Ferrero Litigation, 794 F. Supp. 2d 1107 | UNVERIFIED | 29 | 2 |
| 467 | In re Gilead Sci. Sec. Litig, 536 F.3d 1049 | UNVERIFIED | 29 | 2 |
| 468 | In re Stac Elecs. Sec. Litig, 89 F.3d 1399 | UNVERIFIED | 29 | 2 |
| 469 | Jones v. Royal Admin. Servs., 887 F.3d 443 | UNVERIFIED | 29 | 2 |
| 470 | Kennedy v. Beaumont Investment, 111 Cal.App.4th 102 | UNVERIFIED | 29 | 2 |
| 471 | Kenneth Mebane Ranches v. Superior Court, 10 Cal.App.4th 276 | UNVERIFIED | 20, 32 | 2 |
| 472 | Korea Supply Co. v. Lockheed Martin Corp, 29 Cal.4th 1134 | UNVERIFIED | 5, 29 | 2 |
| 473 | Madrid v. Perot Sys. Corp, 130 Cal.App.4th 440 | UNVERIFIED | 29 | 2 |
| 474 | Makar-Welbon v. Sony Electrics, 187 F.R.D. 576 | UNVERIFIED | 29 | 2 |
| 475 | Marceau v. Blackfeet Hous. Auth, 540 F.3d 916 | UNVERIFIED | 29 | 2 |
| 476 | Martinez v. Ylst, 951 F.2d 1153 | UNVERIFIED | 7, 33 | 2 |
| 477 | Mendiondo v. Centinela Hosp. Med. Ctr, 521 F.3d 1097 | UNVERIFIED | 29 | 2 |
| 478 | Miller v. Rykoff, 845 F.2d 209 | UNVERIFIED | 29 | 2 |
| 479 | Monterey Coastkeeper v. Central Coast Regional Water Quality Control, 76 Cal.App.5th 1 | UNVERIFIED | 20, 32 | 2 |
| 480 | Moss v. U.S. Secret Serv, 572 F.3d 962 | UNVERIFIED | 29 | 2 |
| 481 | Nelson v. Tucker Ellis, 48 Cal.App.5th 827 | UNVERIFIED | 20, 32 | 2 |
| 482 | Paulsen v. CNF Inc, 559 F.3d 1061 | UNVERIFIED | 24 | 2 |
| 483 | People v. Coronado, 12 Cal.4th 145 | UNVERIFIED | 29 | 2 |
| 484 | People v. Toomey, 157 Cal.App.3d 1 | UNVERIFIED | 29 | 2 |
| 485 | Pintos v. Pacific Creditors Ass’n, 605 F.3d 665 | UNVERIFIED | 29 | 2 |
| 486 | Rhonda S. v. Kaiser Foundation Health Plain, 94 Cal.App.5th 643 | UNVERIFIED | 20, 32 | 2 |
| 487 | Richardson v. McKnight, 117 S. Ct. 2100 | VERIFIED | 28 | 2 |
| 488 | Roberts v. United Healthcare Services, 2 Cal.App.5th 132 | UNVERIFIED | 29 | 2 |
| 489 | Santos v. Crenshaw Mfg., 55 Cal.App.5th 39 | UNVERIFIED | 29 | 2 |
| 490 | Schneider v. California Dep’t, 151 F.3d 1194 | UNVERIFIED | 29 | 2 |
| 491 | Shaeffer v. Califia Farms, 44 Cal.App.5th 1125 | UNVERIFIED | 20, 32 | 2 |
| 492 | State Farm Mut. Auto. Ins. Co. v. Campbell, 538 U.S. 408 | UNVERIFIED | 12 | 2 |
| 493 | State Farm Mut. Auto. Ins. Co. v. Riley, 199 F.R.D. 276 | UNVERIFIED | 33 | 2 |
| 494 | State of California v. Superior Court, 12 Cal.3d 237 | UNVERIFIED | 20, 32 | 2 |
| 495 | Turner v. Duncan, 158 F.3d 449 | UNVERIFIED | 7, 33 | 2 |
| 496 | U.S. v. Holtzman, 762 F.2d 720 | UNVERIFIED | 29 | 2 |
| 497 | Van’t Rood v. Cty. of Santa Clara, 113 Cal.App.4th 549 | UNVERIFIED | 29 | 2 |
| 498 | Vignolo v. Miller, 120 F.3d 1075 | UNVERIFIED | 29 | 2 |
| 499 | Walker v. USAA Cas. Ins. Co, 474 F. Supp. 2d 1168 | UNVERIFIED | 29 | 2 |
| 500 | Wallis v. Spencer, 202 F.3d 1126 | UNVERIFIED | 33 | 2 |
| 501 | Walsh v. Nevada Dept, 471 F.3d 1033 | UNVERIFIED | 29 | 2 |
| 502 | Warren v. Fox Family Worldwide, 328 F.3d 1136 | UNVERIFIED | 29 | 2 |
| 503 | Washington v. CSC Credit Servs. Inc, 199 F.3d 263 | UNVERIFIED | 29 | 2 |
| 504 | Weinstein v. County of Los Angeles, 237 Cal.App.4th 944 | UNVERIFIED | 20, 32 | 2 |
| 505 | Wilder v. Virginia Hosp. Ass'n, 496 U.S. 498 | UNVERIFIED | 24 | 2 |
| 506 | Zetterberg v. State Dept, 43 Cal.App.3d 657 | UNVERIFIED | 20, 32 | 2 |
| 507 | Zivkovic v. S. Cal. Edison Co, 302 F.3d 1080 | UNVERIFIED | 33 | 2 |
| 508 | 148 Cal. App. 4 | UNVERIFIED | 29 | 1 |
| 509 | 148 Cal.App.4th 937 | UNVERIFIED | 29 | 1 |
| 510 | 2009 WL 1684714 | UNVERIFIED | 24 | 1 |
| 511 | 2009 WL 2390824 | UNVERIFIED | 24 | 1 |
| 512 | 2012 WL 13028094 | UNVERIFIED | 29 | 1 |
| 513 | 2012 WL 5279672 | MISCITED | 28 | 1 |
| 514 | 2015 WL 4089844 | UNVERIFIED | 7, 33 | 1 |
| 515 | 2019 WL 4194128 | UNVERIFIED | 7, 33 | 1 |
| 516 | 2025 WL 2636309 | UNVERIFIED | 7, 33 | 1 |
| 517 | 751 F.3d 990 | UNVERIFIED | 29 | 1 |
| 518 | 966 F.2d 470 | UNVERIFIED | 28 | 1 |
| 519 | Abelleira v. District Court, 17 Cal.2d 280 | UNVERIFIED | 8, 33 | 1 |
| 520 | Ash v. Cvetkov, 739 F.2d 493 | UNVERIFIED | 29 | 1 |
| 521 | Ashcroft v. Al-Kidd, 563 U.S. 731 | UNVERIFIED | 24 | 1 |
| 522 | Az. Students’ Ass. v. Ariz. Bd, 824 F.3d 858 | UNVERIFIED | 28 | 1 |
| 523 | Babb v. Superior Court, 3 Cal.3d 841 | UNVERIFIED | 20, 32 | 1 |
| 524 | Band of Mission Indians v. Rose, 893 F.2d 1074 | UNVERIFIED | 29 | 1 |
| 525 | Berryman v. Merit Prop. Mgmt., 152 Cal.App.4th 1544 | UNVERIFIED | 29 | 1 |
| 526 | Biggs v. Terhune, 334 F.3d 910 | VERIFIED | 28 | 1 |
| 527 | Bostock v. Clayton Cnty, 590 U.S. 644 | UNVERIFIED | 24 | 1 |
| 528 | C.f. Polich v. Burlington Northern, 942 F.2d 1467 | UNVERIFIED | 29 | 1 |
| 529 | CV Amalgamated LLC v. City of Chula Vista, 82 Cal.App.5th 265 | UNVERIFIED | 20, 32 | 1 |
| 530 | Cal. Correctional Peace Officers Assn. v. State Personnel Bd, 10 Cal.4th 1133 | UNVERIFIED | 20, 32 | 1 |
| 531 | Canova v. Trustees of Imperial Irrigation District Employee Pension, 150 Cal.App.4th 1487 | UNVERIFIED | 20, 32 | 1 |
| 532 | Cappello v. Walmart Inc, 394 F. Supp. 3d 1015 | UNVERIFIED | 29 | 1 |
| 533 | Carver v. Lehman, 558 F.3d 869 | VERIFIED | 28 | 1 |
| 534 | Castillo v. Marshall, 207 F.3d 15 | UNVERIFIED | 24 | 1 |
| 535 | Cato v. United States, 70 F.3d 1103 | UNVERIFIED | 7, 33 | 1 |
| 536 | City of Escondido v. Emmons, 139 S. Ct. 500 | VERIFIED | 28 | 1 |
| 537 | Cortez v. Purolator Air Filtration Prod. Co, 23 Cal.4th 163 | UNVERIFIED | 29 | 1 |
| 538 | DZ Reserve v. Meta Platforms, 96 F.4th 1223 | UNVERIFIED | 28 | 1 |
| 539 | Daniels v. DMV, 33 Cal.3d 532 | UNVERIFIED | 8, 33 | 1 |
| 540 | Demoran v. Witt, 781 F.2d 155 | UNVERIFIED | 7, 33 | 1 |
| 541 | DiCampli-Mintz v. County of Santa Clara, 55 Cal.4th 983 | UNVERIFIED | 2, 32 | 1 |
| 542 | Doe v. Brown, 177 Cal.App.4th 408 | UNVERIFIED | 29 | 1 |
| 543 | Doe v. California Dep’t, 173 Cal.App.4th 1095 | UNVERIFIED | 29 | 1 |
| 544 | DuBois v. Workers' Comp. Appeals Bd, 5 Cal.4th 382 | UNVERIFIED | 20, 32 | 1 |
| 545 | Escobedo v. Applebees, 787 F.3d 1226 | UNVERIFIED | 7, 33 | 1 |
| 546 | Ethridge v. Harbor House Rest, 861 F.2d 1389 | UNVERIFIED | 29 | 1 |
| 547 | Evans v. City of Berkeley, 38 Cal.4th 1 | UNVERIFIED | 20, 32 | 1 |
| 548 | Felarca v. Birgeneau, 891 F.3d 809 | UNVERIFIED | 24 | 1 |
| 549 | Fristoe v. Reynolds Metals Co, 615 F.2d 1209 | UNVERIFIED | 29 | 1 |
| 550 | Fukuda v. City of Angels, 20 Cal.4th 805 | UNVERIFIED | 20, 32 | 1 |
| 551 | Galzinski v. Somers, 2 Cal.App.5th 1164 | VERIFIED | 20, 32 | 1 |
| 552 | Ghazarian v. Magellan Health, 53 Cal. App. 5 | UNVERIFIED | 29 | 1 |
| 553 | Gross v. CitiMortgage, 33 F.4th 1246 | UNVERIFIED | 29 | 1 |
| 554 | Hansen v. Blue Cross, 891 F.2d 1384 | VERIFIED | 24 | 1 |
| 555 | Hartmann v. California Dep't, 707 F.3d 1114 | UNVERIFIED | 1, 32 | 1 |
| 556 | Heidary v. Yadollahi, 99 Cal.App.4th 857 | UNVERIFIED | 8, 33 | 1 |
| 557 | Hells Canyon Pres. Council v. U.S. Forest Serv, 403 F.3d 683 | UNVERIFIED | 29 | 1 |
| 558 | Holding Key Fact Ace Beverage Co. v. Lockheed Info. Mgmt. Servs, 144 F.3d 1218 | VERIFIED | 28 | 1 |
| 559 | In Danielson v. Inslee, 945 F.3d 1096 | VERIFIED | 28 | 1 |
| 560 | In Minneci v. Pollard, 565 U.S. 118 | VERIFIED | 28 | 1 |
| 561 | In re Castillo, 297 F.3d 940 | UNVERIFIED | 7, 33 | 1 |
| 562 | In re Dynamic Random Access Memory, 28 F.4th 42 | UNVERIFIED | 29 | 1 |
| 563 | In re Google Assistant Priv. Litig, 457 F. Supp. 3d 797 | UNVERIFIED | 29 | 1 |
| 564 | Johnson v. Barr, 79 F.4th 996 | UNVERIFIED | 1, 32 | 1 |
| 565 | Kern County Hospital Authority v. Dept. of Corrections, 91 Cal.App.5th 1313 | UNVERIFIED | 20, 32 | 1 |
| 566 | Kong v. City of Hawaiian Gardens Redevelopment Agency, 108 Cal.App.4th 1028 | UNVERIFIED | 20, 32 | 1 |
| 567 | Krainski v. Nevada, 616 F.3d 963 | UNVERIFIED | 1, 32 | 1 |
| 568 | Kroessler v. CVS Health Corp, 977 F.3d 803 | UNVERIFIED | 29 | 1 |
| 569 | Lazar v. Hertz Corp, 69 Cal.App.4th 1494 | UNVERIFIED | 29 | 1 |
| 570 | Link v. Wabash R.R. Co, 370 U.S. 626 | UNVERIFIED | 29 | 1 |
| 571 | Lippitt v. Raymond James Fin. Servs., 340 F.3d 1033 | UNVERIFIED | 29 | 1 |
| 572 | Longshore v. County of Ventura, 25 Cal.3d 14 | UNVERIFIED | 20, 32 | 1 |
| 573 | Lozano v. AT, 504 F.3d 718 | UNVERIFIED | 29 | 1 |
| 574 | Luca v. Administration of Offender Services Bureau, 15 F.3d 1086 | VERIFIED | 28 | 1 |
| 575 | Mackey v. Board of Trustees, 31 Cal.App.5th 640 | UNVERIFIED | 33 | 1 |
| 576 | Mangindin v. Washington Mut. Bank, 637 F. Supp. 2d 700 | UNVERIFIED | 24 | 1 |
| 577 | Manufacturers Life Ins. Co. v. Superior Court, 10 Cal.4th 257 | UNVERIFIED | 20, 32 | 1 |
| 578 | Manzarek v. St. Paul Fire, 519 F.3d 1025 | VERIFIED | 26 | 1 |
| 579 | Matrix Motor Co. v. Toyota Jidosha Kabushiki Kaisha, 218 F.R.D. 667 | UNVERIFIED | 29 | 1 |
| 580 | McKenney v. Purepac Pharmaceutical Co, 167 Cal.App.4th 72 | UNVERIFIED | 20, 32 | 1 |
| 581 | Miller v. Terramite Corp, 114 F. App'x 536 | UNVERIFIED | 7, 32, 33 | 1 |
| 582 | Minetti v. Port of Seattle, 152 F.3d 1113 | UNVERIFIED | 7, 33 | 1 |
| 583 | Mission Power Engineering Co. v. Continental Casualty Co, 883 F. Supp. 488 | UNVERIFIED | 29 | 1 |
| 584 | Paulus v. Bob Lynch Ford, 139 Cal.App.4th 659 | UNVERIFIED | 29 | 1 |
| 585 | People v. American Contractors Indemnity Co, 33 Cal.4th 653 | UNVERIFIED | 8, 33 | 1 |
| 586 | People v. Leyba, 29 Cal.3d 591 | UNVERIFIED | 2, 32 | 1 |
| 587 | People v. Nelson, 200 Cal.App.4th 1083 | UNVERIFIED | 7, 33 | 1 |
| 588 | Perez v. Mortg. Elec. Registration Sys., 959 F.3d 334 | UNVERIFIED | 29 | 1 |
| 589 | Pierson v. Ray, 386 U.S. 547 | UNVERIFIED | 7, 33 | 1 |
| 590 | Pittman v. State Personnel Bd, 233 Cal.App.2d 26 | UNVERIFIED | 8, 33 | 1 |
| 591 | Pratt v. Sumner, 807 F.2d 817 | VERIFIED | 24 | 1 |
| 592 | Roberts v. McAfee, 660 F.3d 1156 | UNVERIFIED | 1, 32 | 1 |
| 593 | Rochin v. Pat Johnson Manufacturing Co, 67 Cal.App.4th 1228 | UNVERIFIED | 8, 33 | 1 |
| 594 | Romero v. Kitsap Cty, 931 F.2d 624 | UNVERIFIED | 1, 32 | 1 |
| 595 | Sandin v. Conner, 515 U.S. 472 | VERIFIED | 28 | 1 |
| 596 | Schreiber Distrib. Co. v. Serv-Well Furniture Co, 806 F.2d 1393 | UNVERIFIED | 28 | 1 |
| 597 | Sidney-Vinstein v. A.H. Robins Co, 697 F.2d 880 | UNVERIFIED | 24 | 1 |
| 598 | Smart v. Heinze, 347 F.2d 114 | UNVERIFIED | 7, 33 | 1 |
| 599 | Smith v. Adepa, 81 F.4th 994 | UNVERIFIED | 24 | 1 |
| 600 | Smith v. Los Angeles Unified Sch. Dist, 830 F.3d 843 | UNVERIFIED | 29 | 1 |
| 601 | Swarthout v. Cooke, 562 U.S. 216 | VERIFIED | 28 | 1 |
| 602 | Swartz v. KPMG LLP, 476 F.3d 756 | VERIFIED | 26 | 1 |
| 603 | Tribe of Florida v. Florida, 517 U.S. 44 | UNVERIFIED | 33 | 1 |
| 604 | Tripati v. First Nat. Bank, 821 F.2d 1368 | UNVERIFIED | 7, 33 | 1 |
| 605 | United States v. Cope, 527 F.3d 944 | VERIFIED | 28 | 1 |
| 606 | United States v. Gourde, 440 F.3d 1065 | UNVERIFIED | 1, 32 | 1 |
| 607 | United States v. Weber, 451 F.3d 552 | VERIFIED | 28 | 1 |
| 608 | United States v. Williams, 356 F.3d 1045 | VERIFIED | 28 | 1 |
| 609 | Valdez v. Allstate Ins. Co, 372 F.3d 1115 | VERIFIED | 24 | 1 |
| 610 | Von Saher v. Norton Simon Museum, 592 F.3d 954 | UNVERIFIED | 7, 33 | 1 |
| 611 | WYATT v. COLE, 994 F.2d 1113 | VERIFIED | 28 | 1 |
| 612 | Washington v. Harper, 494 U.S. 210 | VERIFIED | 28 | 1 |
| 613 | Williams v. Gerber Prod. Co, 552 F.3d 934 | UNVERIFIED | 29 | 1 |
| 614 | Wilson v. Hewlett- Packard Co, 668 F.3d 1136 | UNVERIFIED | 29 | 1 |
| 615 | Zetz v. Boston Scienti, 398 F. Supp. 3d 700 | UNVERIFIED | 28 | 1 |
| 616 | Britt v. Superior Court, 20 Cal.3d 844 | UNVERIFIED | 5 | 67 |
| 617 | Griswold v. Connecticut, 381 U.S. 479 | UNVERIFIED | 5 | 67 |
| 618 | 47 Cal. App. 214 | UNVERIFIED | 5 | 14 |
| 619 | Watts v. Johnson, 27 Cal.App.5th 734 | UNVERIFIED | 15 | 11 |
| 620 | Younger v. Berkeley City Council, 45 Cal.App.3d 825 | UNVERIFIED | 5 | 9 |
| 621 | Payless Drug v. Superior Court, 54 Cal.App.3d 988 | UNVERIFIED | 5 | 6 |
| 622 | Travelers Insurance Company v. Superior Court, 143 Cal.App.3d 436 | UNVERIFIED | 5 | 6 |
| 623 | 47 Cal.App.4th 214 | UNVERIFIED | 5 | 5 |
| 624 | Coito v. Superior Court, 54 Cal.App.4th 480 | UNVERIFIED | 5 | 4 |
| 625 | Reese v. County of Sacramento, 888 F.3d 1030 | VERIFIED | 5, 14, 16 | 4 |
| 626 | 2019 WL 3806388 | UNVERIFIED | 3 | 3 |
| 627 | Gillan v. City of San Marino, 147 Cal.App.4th 1033 | UNVERIFIED | 15 | 3 |
| 628 | Graham v. Connor, 490 U.S. 386 | UNVERIFIED | 3 | 3 |
| 629 | Gressett v. Superior Court, 185 Cal.App.4th 114 | UNVERIFIED | 15 | 3 |
| 630 | State of California v. Superior Court, 32 Cal.4th 1234 | UNVERIFIED | 15 | 3 |
| 631 | 235 Cal.App.4th 957 | UNVERIFIED | 15 | 2 |
| 632 | Brentwood Acad. v. Tennessee Secondary Sch. Athletic Ass'n, 531 U.S. 288 | UNVERIFIED | 3 | 2 |
| 633 | Brittain v. Hansen, 451 F.3d 982 | UNVERIFIED | 3 | 2 |
| 634 | Caviness v. Horizon Cmty. Learning Ctr., 590 F.3d 806 | UNVERIFIED | 3 | 2 |
| 635 | Coito v. Superior Court, 54 Cal.4th 480 | UNVERIFIED | 5 | 2 |
| 636 | Entler v. Gregoire, 872 F.3d 1031 | UNVERIFIED | 3 | 2 |
| 637 | Envtl. Protection Info. Ctr. v. Dept. of Forestry, 43 Cal. App. 4 | UNVERIFIED | 15 | 2 |
| 638 | Furnace v. Sullivan, 705 F.3d 1021 | VERIFIED | 3 | 2 |
| 639 | Giraldo v. California Dept, 168 Cal.App.4th 231 | UNVERIFIED | 5 | 2 |
| 640 | Goodman v. Kennedy, 18 Cal.3d 335 | UNVERIFIED | 5 | 2 |
| 641 | Gray v. Superior Court, 125 Cal.App.4th 629 | UNVERIFIED | 9 | 2 |
| 642 | Grimes v. State Dep’t, 70 Cal.App.4th 1065 | UNVERIFIED | 15 | 2 |
| 643 | Haines v. Kerner, 404 U.S. 519 | UNVERIFIED | 3 | 2 |
| 644 | Hilton v. Board of Supervisors, 7 Cal.App.3d 708 | UNVERIFIED | 9 | 2 |
| 645 | In re Chaudhary, 172 Cal.App.4th 32 | UNVERIFIED | 9 | 2 |
| 646 | In re E.J, 47 Cal.4th 1258 | UNVERIFIED | 5 | 2 |
| 647 | In re Febbo, 52 Cal.App.5th 1088 | UNVERIFIED | 9 | 2 |
| 648 | In re Gadlin, 31 Cal.App.5th 784 | VERIFIED | 9 | 2 |
| 649 | In re Greg F, 55 Cal.4th 393 | UNVERIFIED | 9 | 2 |
| 650 | In re Lira, 58 Cal.4th 573 | UNVERIFIED | 9 | 2 |
| 651 | In re Ricardo P, 7 Cal.5th 1113 | VERIFIED | 14 | 2 |
| 652 | In re Steier, 152 Cal.App.4th 63 | UNVERIFIED | 9 | 2 |
| 653 | In re Wilson, 30 Cal.3d 438 | UNVERIFIED | 9 | 2 |
| 654 | Ivey v. Bd. of Regents, 673 F.2d 266 | VERIFIED | 3, 18 | 2 |
| 655 | Jay v. Mahaffey, 218 Cal.App.4th 1522 | UNVERIFIED | 9 | 2 |
| 656 | Keyes v. Bowen, 189 Cal.App.4th 647 | UNVERIFIED | 9 | 2 |
| 657 | King v. Atiyeh, 814 F.2d 565 | UNVERIFIED | 3 | 2 |
| 658 | Kirtley v. Rainey, 326 F.3d 1088 | UNVERIFIED | 3 | 2 |
| 659 | L.P. v. County of Santa Clara, 194 Cal.App.4th 1150 | UNVERIFIED | 9 | 2 |
| 660 | Lockett v. Suardini, 526 F.3d 866 | UNVERIFIED | 3 | 2 |
| 661 | Lugar v. Edmondson Oil Co, 457 U.S. 922 | UNVERIFIED | 3 | 2 |
| 662 | Neighbours v. Buzz Oates Enterprises, 217 Cal.App.3d 325 | UNVERIFIED | 9 | 2 |
| 663 | Parthemore v. Col, 221 Cal.App.4th 1372 | UNVERIFIED | 5 | 2 |
| 664 | People v. Douglas M, 220 Cal.App.4th 1068 | UNVERIFIED | 15 | 2 |
| 665 | People v. Picklesimer, 48 Cal.4th 330 | UNVERIFIED | 9 | 2 |
| 666 | People v. Reynoza, 15 Cal.4th 982 | UNVERIFIED | 9 | 2 |
| 667 | Rawson v. Recovery Innovations, 975 F.3d 742 | UNVERIFIED | 3 | 2 |
| 668 | Reichardt v. Hoffman, 52 Cal.App.4th 754 | UNVERIFIED | 9 | 2 |
| 669 | Rialto Citizens v. City of Rialto, 208 Cal.App.4th 899 | UNVERIFIED | 15 | 2 |
| 670 | Sabatasso v. Superior Court, 167 Cal.App.4th 971 | UNVERIFIED | 15 | 2 |
| 671 | Santa Clara County Counsel Attys. Assn. v. Woodside, 7 Cal.4th 525 | UNVERIFIED | 9 | 2 |
| 672 | State of California v. Superior Court, 15 Cal.4th 1055 | UNVERIFIED | 15 | 2 |
| 673 | Teachers’ Ret. Bd. v. Genest, 154 Cal.App.4th 1012 | UNVERIFIED | 9 | 2 |
| 674 | Venegas v. County of Los Angeles, 32 Cal.4th 820 | VERIFIED | 5, 14 | 2 |
| 675 | Weiss v. City of Los Angeles, 2 Cal.App.5th 194 | UNVERIFIED | 15 | 2 |
| 676 | 158 Cal.App.4th 226 | UNVERIFIED | 16 | 1 |
| 677 | 2 Cal.5th 505 | UNVERIFIED | 5 | 1 |
| 678 | 2006 WL 2308442 | UNVERIFIED | 3 | 1 |
| 679 | 2008 WL 11470935 | UNVERIFIED | 3 | 1 |
| 680 | 2009 WL 656285 | UNVERIFIED |  | 1 |
| 681 | 2010 WL 4169304 | UNVERIFIED | 3 | 1 |
| 682 | 2010 WL 445203 | UNVERIFIED | 18 | 1 |
| 683 | 2010 WL 725563 | UNVERIFIED | 3 | 1 |
| 684 | 2011 WL 3439225 | UNVERIFIED |  | 1 |
| 685 | 2015 WL 4879627 | UNVERIFIED | 18 | 1 |
| 686 | 2017 WL 5129885 | UNVERIFIED | 3 | 1 |
| 687 | 2018 WL 2018096 | UNVERIFIED | 18 | 1 |
| 688 | 2018 WL 558658 | UNVERIFIED | 18 | 1 |
| 689 | 2019 WL 3802187 | UNVERIFIED | 3 | 1 |
| 690 | 2020 WL 2027290 | UNVERIFIED | 18 | 1 |
| 691 | 2020 WL 7214292 | UNVERIFIED | 18 | 1 |
| 692 | 2020 WL 8919180 | UNVERIFIED | 18 | 1 |
| 693 | 2023 WL 11920185 | UNVERIFIED | 3 | 1 |
| 694 | 2024 WL 988374 | UNVERIFIED | 18 | 1 |
| 695 | 208 F.R.D. 273 | UNVERIFIED | 3 | 1 |
| 696 | 309 F.3d 662 | VERIFIED | 18 | 1 |
| 697 | 506 F.3d 895 | UNVERIFIED | 3 | 1 |
| 698 | 518 U.S. 727 | UNVERIFIED | 3 | 1 |
| 699 | 551 U.S. 308 | UNVERIFIED | 3 | 1 |
| 700 | 627 F.3d 402 | UNVERIFIED | 3 | 1 |
| 701 | 840 F.2d 685 | UNVERIFIED | 3 | 1 |
| 702 | American Mfrs. Mut. Ins. Co. v. Sullivan, 526 U.S. 40 | UNVERIFIED | 3 | 1 |
| 703 | Arizonans for Official English v. Arizona, 520 U.S. 43 | UNVERIFIED |  | 1 |
| 704 | Ass’n of Radiation Survivors v. Turnage, 115 F.R.D. 543 | UNVERIFIED | 3 | 1 |
| 705 | Auburn Cmty. Envt. v. County of Placer, 215 Cal.App.4th 25 | UNVERIFIED |  | 1 |
| 706 | Austin B. v. Escondido Union School Dist, 149 Cal.App.4th 860 | UNVERIFIED | 5 | 1 |
| 707 | B.B. v. County of Los Angeles, 10 Cal.5th 1 | VERIFIED | 16 | 1 |
| 708 | Balistreri v. Pacifica Police Dep’t, 901 F.2d 696 | UNVERIFIED | 3 | 1 |
| 709 | Beauchene v. Synanon Foundation, 88 Cal.App.3d 342 | UNVERIFIED | 5 | 1 |
| 710 | Blum v. Yaretsky, 457 U.S. 991 | UNVERIFIED | 3 | 1 |
| 711 | Brockmeyer v. May, 383 F.3d 798 | UNVERIFIED | 3 | 1 |
| 712 | Bruce v. YIst, 351 F.3d 1283 | VERIFIED | 18 | 1 |
| 713 | Burchett v. City of Newport Beach, 33 Cal.App.4th 1472 | UNVERIFIED | 3 | 1 |
| 714 | City of Cleburne Texas v. Cleburne Living Center, 473 U.S. 432 | VERIFIED | 18 | 1 |
| 715 | Cohen v. S & S Construction Co, 151 Cal.App.3d 941 | UNVERIFIED | 5 | 1 |
| 716 | Collins v. Womancare, 878 F.2d 1145 | UNVERIFIED | 3 | 1 |
| 717 | Conley v. Gibson, 355 U.S. 41 | VERIFIED | 18 | 1 |
| 718 | Cortez v. Cnty. of Los Angeles, 294 F.3d 1186 | UNVERIFIED |  | 1 |
| 719 | Davis v. Scherer, 468 U.S. 183 | VERIFIED | 18 | 1 |
| 720 | Decker Coal Co. v. Pehringer, 8 F.4th 1123 | UNVERIFIED | 3 | 1 |
| 721 | Deyo v. Kilbourne, 84 Cal.App.3d 771 | UNVERIFIED | 5 | 1 |
| 722 | Doe v. Harris, 772 F.3d 563 | UNVERIFIED | 3 | 1 |
| 723 | Doster v. County of San Diego, 203 Cal.App.3d 257 | UNVERIFIED | 5 | 1 |
| 724 | Du Lac v. Perma Trans Products, 103 Cal.App.3d 937 | UNVERIFIED | 5 | 1 |
| 725 | Edgren v. Regents of University, 158 Cal.App.3d 515 | UNVERIFIED | 5 | 1 |
| 726 | Employment Division v. Smith, 494 U.S. 872 | VERIFIED | 16 | 1 |
| 727 | Engquist v. Oregon Department, 553 U.S. 591 | VERIFIED | 18 | 1 |
| 728 | Evans v. Skolnik, 637 F. App'x 285 | UNVERIFIED | 18 | 1 |
| 729 | Evartt v. Superior Court, 89 Cal.App.3d 795 | UNVERIFIED | 3 | 1 |
| 730 | Faulkner v. ADT Sec. Servs, 706 F.3d 1017 | UNVERIFIED |  | 1 |
| 731 | Flagg Bros. v. Brooks, 436 U.S. 149 | UNVERIFIED | 3 | 1 |
| 732 | Flores v. Von Kleist, 739 F. Supp. 2d 1236 | UNVERIFIED | 3 | 1 |
| 733 | Forsyth v. Humana, 114 F.3d 1467 | UNVERIFIED | 3 | 1 |
| 734 | Frazier v. Dubois, 922 F.2d 560 | VERIFIED | 18 | 1 |
| 735 | Fulton v. City of Philadelphia, 593 U.S. 522 | VERIFIED | 16 | 1 |
| 736 | George v. Smith, 507 F.3d 605 | UNVERIFIED | 3 | 1 |
| 737 | Harris v. Cnty. of Orange, 682 F.3d 1126 | UNVERIFIED |  | 1 |
| 738 | Harris v. Pac. Anchor Transp., 231 Cal.App.4th 103 | UNVERIFIED | 5 | 1 |
| 739 | Hartpence v. Kinetic Concepts, 792 F.3d 1121 | UNVERIFIED | 3 | 1 |
| 740 | Hauter v. Zogarts, 14 Cal.3d 104 | UNVERIFIED | 5 | 1 |
| 741 | Hulsey v. Koehler, 218 Cal.App.3d 1150 | UNVERIFIED | 5 | 1 |
| 742 | In re David, 202 Cal.App.4th 675 | UNVERIFIED | 5 | 1 |
| 743 | Inouye v. Kemna, 504 F.3d 705 | UNVERIFIED | 3 | 1 |
| 744 | Jackson v. Arizona, 885 F.2d 639 | VERIFIED | 18 | 1 |
| 745 | Jackson v. Metropolitan Edison Co, 419 U.S. 345 | UNVERIFIED | 3 | 1 |
| 746 | Johnson v. Ryan, 55 F.4th 1167 | UNVERIFIED | 3 | 1 |
| 747 | Jones v. Cmty. Redev. Agency, 733 F.2d 646 | VERIFIED | 18 | 1 |
| 748 | Jones v. Williams, 297 F.3d 930 | VERIFIED | 18 | 1 |
| 749 | Julian v. Mission Community Hospital, 11 Cal.App.5th 360 | UNVERIFIED | 5 | 1 |
| 750 | Kevin R. v. Superior Court, 191 Cal.App.4th 676 | UNVERIFIED | 5 | 1 |
| 751 | Kwikset Corp. v. Superior Court, 51 Cal.4th 310 | UNVERIFIED | 5 | 1 |
| 752 | Lee v. Katz, 276 F.3d 550 | UNVERIFIED | 3 | 1 |
| 753 | Legg v. Mutual Ben. Health, 184 Cal.App.2d 482 | UNVERIFIED | 5 | 1 |
| 754 | Lopez v. Dept. of Health Services, 939 F.2d 881 | UNVERIFIED | 3 | 1 |
| 755 | Loux v. Rhay, 375 F.2d 55 | UNVERIFIED | 3 | 1 |
| 756 | Macri v. Carson Tahoe Hosp., 247 Cal.App.2d 63 | UNVERIFIED | 3 | 1 |
| 757 | Maguire v. Hibernia Savings, 23 Cal.2d 719 | UNVERIFIED | 5 | 1 |
| 758 | Manhattan Cmty. Access Corp. v. Halleck, 139 S. Ct. 1921 | UNVERIFIED | 3 | 1 |
| 759 | Mann v. Adams, 55 F.2d 639 | UNVERIFIED | 18 | 1 |
| 760 | Marina Tenants Assn. v. Deauville Marina Development Co, 181 Cal.App.3d 122 | UNVERIFIED | 5 | 1 |
| 761 | May v. Enomoto, 633 F.2d 164 | VERIFIED | 18 | 1 |
| 762 | McCollum v. Ca. Dep't, 647 F.3d 870 | VERIFIED | 18 | 1 |
| 763 | McKinney v. De Bord, 507 F.2d 501 | UNVERIFIED | 3 | 1 |
| 764 | Mediterranean Const. Co. v. State Farm Fire, 66 Cal.App.4th 257 | UNVERIFIED | 5 | 1 |
| 765 | Meyer v. Horizon Health Corp, 565 F.3d 1195 | UNVERIFIED | 3 | 1 |
| 766 | Molko v. Holy Spirit Assn, 46 Cal.3d 1092 | UNVERIFIED | 5 | 1 |
| 767 | Mollett v. Netflix, 795 F.3d 1062 | UNVERIFIED |  | 1 |
| 768 | Noland v. Land of, 114 Cal.App.5th 426 | UNVERIFIED | 5 | 1 |
| 769 | Ogo Associates v. City of Torrance, 37 Cal.App.3d 830 | UNVERIFIED | 5 | 1 |
| 770 | People v. Dominguez, 180 Cal.App.4th 1351 | UNVERIFIED | 5 | 1 |
| 771 | People v. Phillips, 75 Cal.App.5th 643 | UNVERIFIED | 5 | 1 |
| 772 | Plantier v. Ramona Municipal Water Dist, 12 Cal.App.5th 856 | UNVERIFIED | 5 | 1 |
| 773 | Porter v. Osborn, 546 F.3d 1131 | UNVERIFIED | 3 | 1 |
| 774 | Ramirez v. Galaza, 334 F.3d 850 | VERIFIED | 18 | 1 |
| 775 | Reinhardt v. Kopcow, 65 F. Supp. 3d 1164 | UNVERIFIED | 3 | 1 |
| 776 | Resnick v. Hayes, 213 F.3d 443 | UNVERIFIED | 3 | 1 |
| 777 | Rizzo v. Goode, 423 U.S. 362 | VERIFIED | 18 | 1 |
| 778 | Rosenbaum v. Washoe County, 663 F.3d 1071 | UNVERIFIED |  | 1 |
| 779 | Rutman Wine Co. v. E. & J. Gallo Winery, 829 F.2d 729 | UNVERIFIED | 3 | 1 |
| 780 | Sandoval v. Pali Institute, 113 Cal.App.5th 616 | UNVERIFIED | 5 | 1 |
| 781 | Scheuer v. Rhodes, 416 U.S. 232 | VERIFIED | 18 | 1 |
| 782 | Schmid v. City and County, 60 Cal.App.5th 470 | UNVERIFIED | 5 | 1 |
| 783 | Sheerer v. Panas, 119 Cal.App.5th 367 | UNVERIFIED | 5 | 1 |
| 784 | Sierra Club v. San Joaquin Local Agency Formation Com, 21 Cal.4th 489 | UNVERIFIED | 5 | 1 |
| 785 | Simmons v. Superior Court, 7 Cal.App.5th 1113 | UNVERIFIED | 5 | 1 |
| 786 | Stephenson v. Argonaut Ins. Co, 125 Cal.App.4th 962 | UNVERIFIED | 5 | 1 |
| 787 | Stevenson v. Superior Court, 16 Cal.4th 880 | UNVERIFIED | 5 | 1 |
| 788 | Sutton v. Providence St. Joseph Med. Ctr, 192 F.3d 826 | UNVERIFIED | 3 | 1 |
| 789 | Tandon v. Newsom, 593 U.S. 61 | VERIFIED | 16 | 1 |
| 790 | Thornton v. City of St. Helens, 425 F.3d 1158 | VERIFIED | 18 | 1 |
| 791 | Topeka & Santa Fe Ry. Co. v. Hercules Inc, 146 F.3d 1071 | UNVERIFIED | 3 | 1 |
| 792 | Upshaw v. Superior Court, 22 Cal.App.5th 489 | UNVERIFIED | 5 | 1 |
| 793 | Vasquez v. Residential Investments, 118 Cal.App.4th 269 | UNVERIFIED | 5 | 1 |
| 794 | Vecchione v. Carlin, 111 Cal.App.3d 351 | UNVERIFIED | 5 | 1 |
| 795 | Village of Arlington Heights v. Metro. Hous. Dev. Corp, 429 U.S. 252 | UNVERIFIED | 3 | 1 |
| 796 | Village of Willowbrook v. Olech, 528 U.S. 562 | VERIFIED | 18 | 1 |
| 797 | Wagner v. City of South Pasadena, 78 Cal.App.4th 943 | UNVERIFIED | 3 | 1 |
| 798 | Washington v. County of Contra Costa, 38 Cal.App.4th 890 | UNVERIFIED | 5 | 1 |
| 799 | Watison v. Carter, 668 F.3d 1108 | VERIFIED | 18 | 1 |
| 800 | Whren v. United States, 517 U.S. 806 | UNVERIFIED | 3 | 1 |
| 801 | Wilhelm v. Rotman, 680 F.3d 1113 | UNVERIFIED | 3 | 1 |
| 802 | Wilkinson v. Austin, 545 U.S. 209 | VERIFIED | 18 | 1 |
| 803 | Wilner v. Sunset Life Ins. Co, 78 Cal.App.4th 952 | UNVERIFIED | 5 | 1 |
| 804 | Wilson v. City of Fountain Valley, 372 F. Supp. 2d 1178 | UNVERIFIED | 3 | 1 |
| 805 | Wittner v. Banner Health, 720 F.3d 770 | UNVERIFIED | 3 | 1 |
| 806 | Wood v. Yordy, 753 F.3d 899 | VERIFIED | 18 | 1 |

## Already KeyCited — skip

UNIFIED memo, 2026-09-19. Recon: `legal-intel/recon/2026-09-19-matter-28-keycite-westlaw.md`. *Chavez* 12 F.4th stays MISCHARACTERIZED.

| Search | Status | Matters |
|---|---|---|
| Swift v. Christian, 384 F.3d 1184 | MISCITED | 7, 30, 32, 33 |
| Chavez v. Robinson, 12 F.4th 978 | MISCHARACTERIZED | 1, 28, 30, 32 |
| Neal v. Shimoda, 131 F.3d 818 | VERIFIED | 28 |
| Kildare v. Saenz, 325 F.3d 1078 | VERIFIED | 28 |
| Taylor v. Sturgell, 553 U.S. 880 | VERIFIED | 7, 32, 33 |
| Allen v. McCurry, 449 U.S. 90 | VERIFIED | 28 |
| Anza v. Ideal Steel Supply, 547 U.S. 451 | VERIFIED | 28 |
| Beazell v. Schrader, 59 Cal.2d 577 | VERIFIED | 28 |
| Berri v. Superior Court, 43 Cal.2d 856 | VERIFIED | 28 |
| Boeken v. Philip Morris USA, 48 Cal.4th 788 | VERIFIED | 28 |
| Cedric Kushner Promotions v. King, 533 U.S. 158 | VERIFIED | 28 |
| Chavez v. Robinson, 817 F.3d 1162 | VERIFIED | 28 |
| Costello v. United States, 365 U.S. 265 | VERIFIED | 28 |
| DKN Holdings LLC v. Faerber, 61 Cal.4th 813 | VERIFIED | 28 |
| Diaz v. Gates, 420 F.3d 897 | VERIFIED | 28 |
| Franklin & Franklin v. 7-Eleven, 85 Cal.App.4th 1168 | VERIFIED | 28 |
| Furnace v. Giurbino, 838 F.3d 1019 | VERIFIED | 28 |
| Goddard v. Security Title, 14 Cal.2d 47 | VERIFIED | 28 |
| Gonzales v. California Dep't of Corr., 739 F.3d 1226 | VERIFIED | 28 |
| Kay v. City of Rancho Palos Verdes, 504 F.3d 803 | VERIFIED | 28 |
| Keidatz v. Albany, 39 Cal.2d 826 | VERIFIED | 28 |
| Migra v. Warren City Sch. Dist., 465 U.S. 75 | VERIFIED | 28 |
| Perez v. City of San Bruno, 27 Cal.3d 875 | VERIFIED | 28 |
| Sartor v. Superior Court, 136 Cal.App.3d 322 | VERIFIED | 28 |
| Semtek Int'l Inc. v. Lockheed Martin, 531 U.S. 497 | VERIFIED | 28 |
| Sullivan v. Delta Air Lines, 15 Cal.4th 288 | VERIFIED | 28 |
| Valvo v. USC, 67 Cal.App.3d 887 | VERIFIED | 28 |

## 20-view session map

| Session | Rows | First search | Last search |
|---|---|---|---|
| 1 | 6–25 (20) | Benavidez v. County of San Diego, 993 F.3d 9 | Jessie v. United States, 79 M.J. 437 |
| 2 | 26–45 (20) | Johnson v. City of Grants Pass, 50 F.4th 787 | Franks v. Delaware, 438 U.S. 154 |
| 3 | 46–65 (20) | In re Thompson, 172 Cal.App.3d 256 | Blank v. Kirwan, 39 Cal.3d 311 |
| 4 | 66–85 (20) | Chism v. Washington State, 661 F.3d 380 | Pratt v. Rowland, 65 F.3d 802 |
| 5 | 86–105 (20) | Bd. of Cnty. Comm'rs v. Umbehr, 518 U.S. 668 | People v. Lent, 15 Cal.3d 481 |
| 6 | 106–125 (20) | Vlandis v. Kline, 412 U.S. 441 | Mendoza v. ADP Screening, 182 Cal.App.4th 1644 |
| 7 | 126–145 (20) | Regents v. Roth, 408 U.S. 564 | 2019 WL 6619348 |
| 8 | 146–165 (20) | Barnett v. Fireman's Fund Ins. Co, 90 Cal.App.4th 500 | Dent v. Nat’l Football League, 902 F.3d 1109 |
| 9 | 166–185 (20) | Fritsch v. Swift Transp. Co, 899 F.3d 785 | Ashelman v. Pope, 793 F.2d 1072 |
| 10 | 186–205 (20) | Bily v. Arthur Young, 3 Cal.4th 370 | Orosco v. Napolitano, 598 F.3d 222 |
| 11 | 206–225 (20) | Owens v. Huntling, 115 F.2d 160 | Burns v. Windsor Ins. Co, 31 F.3d 1092 |
| 12 | 226–245 (20) | Carloss v. County of Alameda, 242 Cal.App.4th 116 | Sonner v. Premier Nutrition Corporation, 49 F.4th 1300 |
| 13 | 246–265 (20) | Warner Constr. Corp. v. City of Los Angeles, 2 Cal.3d 285 | Helm v. Alderwoods Group, 696 F. Supp. 2d 1057 |
| 14 | 266–285 (20) | Herr v. Nestle U.S.A., 109 Cal.App.4th 779 | People v. Torres, 11 Cal.App.4th 977 |
| 15 | 286–305 (20) | Pinard v. Clatskanie Sch. Dist, 467 F.3d 755 | Hughes v. Pair, 46 Cal.4th 1035 |
| 16 | 306–325 (20) | Alcorn v. Anbro Engineering, 2 Cal.3d 493 | McCorkle v. City of Los Angeles, 70 Cal.2d 252 |
| 17 | 326–345 (20) | Spencer v. Peters, 857 F.3d 789 | 461 U.S. 731 |
| 18 | 346–365 (20) | Bolkiah v. Superior Ct, 74 Cal.App.4th 984 | Venegas v. County of Los Angeles, 153 Cal.App.4th 1230 |
| 19 | 366–385 (20) | Villiarimo v. Aloha Island Air, 281 F.3d 1054 | Starr v. Baca, 652 F.3d 1202 |
| 20 | 386–405 (20) | Will v. Michigan Dept, 491 U.S. 58 | Sprewell v. Golden State Warriors, 266 F.3d 979 |
| 21 | 406–425 (20) | Vitek v. Jones, 445 U.S. 480 | Thomas v. Dillard, 818 F.3d 864 |
| 22 | 426–445 (20) | U.S. v. Corinthian Colleges, 655 F.3d 984 | Alvarez v. Chevron Corp, 656 F.3d 925 |
| 23 | 446–465 (20) | Asgari v. City of Los Angeles, 15 Cal.4th 744 | Holland v. Morse Diesel Int’l, 86 Cal.App.4th 1443 |
| 24 | 466–485 (20) | In re Ferrero Litigation, 794 F. Supp. 2d 1107 | Pintos v. Pacific Creditors Ass’n, 605 F.3d 665 |
| 25 | 486–505 (20) | Rhonda S. v. Kaiser Foundation Health Plain, 94 Cal.App.5th  | Wilder v. Virginia Hosp. Ass'n, 496 U.S. 498 |
| 26 | 506–525 (20) | Zetterberg v. State Dept, 43 Cal.App.3d 657 | Berryman v. Merit Prop. Mgmt., 152 Cal.App.4th 1544 |
| 27 | 526–545 (20) | Biggs v. Terhune, 334 F.3d 910 | Escobedo v. Applebees, 787 F.3d 1226 |
| 28 | 546–565 (20) | Ethridge v. Harbor House Rest, 861 F.2d 1389 | Kern County Hospital Authority v. Dept. of Corrections, 91 C |
| 29 | 566–585 (20) | Kong v. City of Hawaiian Gardens Redevelopment Agency, 108 C | People v. American Contractors Indemnity Co, 33 Cal.4th 653 |
| 30 | 586–605 (20) | People v. Leyba, 29 Cal.3d 591 | United States v. Cope, 527 F.3d 944 |
| 31 | 606–625 (20) | United States v. Gourde, 440 F.3d 1065 | Reese v. County of Sacramento, 888 F.3d 1030 |
| 32 | 626–645 (20) | 2019 WL 3806388 | In re Chaudhary, 172 Cal.App.4th 32 |
| 33 | 646–665 (20) | In re E.J, 47 Cal.4th 1258 | People v. Picklesimer, 48 Cal.4th 330 |
| 34 | 666–685 (20) | People v. Reynoza, 15 Cal.4th 982 | 2015 WL 4879627 |
| 35 | 686–705 (20) | 2017 WL 5129885 | Auburn Cmty. Envt. v. County of Placer, 215 Cal.App.4th 25 |
| 36 | 706–725 (20) | Austin B. v. Escondido Union School Dist, 149 Cal.App.4th 86 | Edgren v. Regents of University, 158 Cal.App.3d 515 |
| 37 | 726–745 (20) | Employment Division v. Smith, 494 U.S. 872 | Jackson v. Metropolitan Edison Co, 419 U.S. 345 |
| 38 | 746–765 (20) | Johnson v. Ryan, 55 F.4th 1167 | Meyer v. Horizon Health Corp, 565 F.3d 1195 |
| 39 | 766–785 (20) | Molko v. Holy Spirit Assn, 46 Cal.3d 1092 | Simmons v. Superior Court, 7 Cal.App.5th 1113 |
| 40 | 786–805 (20) | Stephenson v. Argonaut Ins. Co, 125 Cal.App.4th 962 | Wittner v. Banner Health, 720 F.3d 770 |
| 41 | 806–806 (1) | Wood v. Yordy, 753 F.3d 899 | Wood v. Yordy, 753 F.3d 899 |

## Regenerating

```
python3 internal/scripts/build-westlaw-queue.py
```

Does not touch the verification ledger. Feed flags back through a dated recon + a later Round overlay the way Round 12 did.
