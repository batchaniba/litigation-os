# Frederick–Stanzick Playbook

Living two-desk dossier for **Andrew P. Frederick** (Morgan Lewis / Amazon) and **Jasmine J. Stanzick** (Seyfarth / Accurate) in **Newanforbi v. Amazon.com Services, LLC**, 4:26-cv-09249-ASK (N.D. Cal.).

This is the playbook. Identity/role intelligence and lodged comparator briefs live here. It is **not** a related-case disclosure, **not** a brief, and **not** something to send to either firm.

| File | What it is |
|---|---|
| [`PLAYBOOK.md`](PLAYBOOK.md) | Read this. Two-desk comparison, *Lerma* (Frederick) and *Carrillo* (Stanzick) argument inventories, the seam. |
| [`cases.json`](cases.json) | Append-only machine cards. One object per docket. |
| [`sources/`](sources/) | Lodged PACER prints. Not served on the public site. Seeded: *Lerma* Frederick MTD packet (Dkts. 24, 24-1, 27, 36); *Carrillo* set (Dkts. 1, 15, 19, 27, 55–59, 62, 64, 64-1). |

*Carrillo* is also cataloged at `/documents/matter-29/carrillo-v-vons/`. The full *Lerma* docket (69 PDFs) already lives at `/documents/matter-29/lerma-v-amazon/` — do not PACER-pull it again. Playbook `sources/` copies are the counsel-research lodge.

## How to add the next case

1. Drop the PACER / portal prints under `sources/<court-case-no>-<short-caption>/` with the docket number in the filename.
2. Add a card to `cases.json` (copy the *Carrillo* card; do not invent fields).
3. Add a matching **Case card** section to `PLAYBOOK.md`.
4. Update the working-pattern bullets only if the new docket actually changes them.
5. If the paper is a statutory/counsel comparator worth fetching later, also catalog it under `/documents/matter-29/<short-caption>/` the way *Lerma* and *Carrillo* are. Do **not** add a Civil L.R. 3-12 related-case link, and do **not** email Frederick or Stanzick about the research.

Identity and role intelligence only. A docket where they appeared for someone else is not a Civil L.R. 3-12 / CRC 3.300 related case unless a court says it is.

## Standing limits

- Do not email Stanzick or Frederick about this research.
- Firm-website bios are **firm-claimed**. Bar lookups are a separate pass.
- Generated dossiers live under `internal/docs/legal-intel/counsel/`; this folder is the analytical layer on top.
- The older pointer at [`../matter29/`](../matter29/) redirects here. Do not keep a second living copy.

## Seeded sources

*Miguel Lerma, Jr. v. Amazon.com Services, LLC*, C.D. Cal. No. **8:22-cv-01727-FWS-JDE** (Slaughter, J.) — **Frederick signed**:

| Dkt | Paper | Date | Why it is here |
|---|---|---|---|
| 24 | Amazon notice of motion (Claims 1 and 5) | Dec. 15, 2022 | Cover. Website-use-only theory in four pages. |
| **24-1** | **Amazon memorandum** | Dec. 15, 2022 | **The winning brief.** Incorporation + court-record sourcing. Fair Chance left standing (n.1). |
| **27** | **Amazon reply** | Feb. 2, 2023 | Field-by-field court-record vs website comparison; NSOR "NO RECORD FOUND"; *Schneider* on unpled facts; *Sonner* concession. |
| 36 | Order granting both MTDs | May 26, 2023 | Already cataloged. Megan's Law / FCRA / UCL dismissed without prejudice. |

*Sandoval Carrillo v. The Vons Companies, Inc.*, C.D. Cal. No. **8:25-cv-00191-SRM-KES** (Murillo, J.):

| Dkt | Paper | Date | Why it is here |
|---|---|---|---|
| 1 | Class Action Complaint | Jan. 31, 2025 | Ray Kim pleading — same counsel as *Lerma*; § 290.46(j)(2)(E), Fair Chance, FCRA § 1681b(b)(1), UCL |
| 55 | Motion for Class Certification | Jan. 14, 2026 | 43 Megan's Law / 901 Fair Chance / 43 FCRA class numbers; standardized adverse-action notices |
| 56 | Vons opposition | Feb. 18, 2026 | Employer-side analog (Littler, **not** Frederick): § 290.46(j)(1) "person at risk," adequacy, same-decision |
| 57 | Asurint opposition | Feb. 18, 2026 | **Stanzick signed.** CRA playbook on paper: certification-only § 1681b(b)(1), *Mendoza*, fail-safe class |
| 58 | Reply to Vons | Mar. 25, 2026 | "Use of any"; (j)(1) as a common defense; circular adequacy attack |
| 59 | Reply to Asurint | Mar. 25, 2026 | Notices as common FCRA knowledge proof; no ascertainability in the Ninth Circuit |
| 15 | Vons answer | Apr. 8, 2025 | Littler employer posture (not Frederick) |
| 19 | Asurint answer | May 30, 2025 | **Stanzick signed.** Answer-stage certification / registry defenses |
| 27 | Stipulated protective order | Sep. 18, 2025 | Joint; Stanzick/Drury on Asurint block |
| 62 | Class-cert hearing transcript | Apr. 15, 2026 | Oral argument; **no written order in lodge** |
| 64 / 64-1 | Vons supplemental RJN + exhibit | Sep. 15, 2026 | Post-hearing Littler RJN (employer analog) |
