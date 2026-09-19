# Frederick–Stanzick Playbook

Living two-desk dossier for **Andrew P. Frederick** (Morgan Lewis / Amazon) and **Jasmine J. Stanzick** (Seyfarth / Accurate) in **Newanforbi v. Amazon.com Services, LLC**, 4:26-cv-09249-ASK (N.D. Cal.).

This is the playbook. Identity/role intelligence and lodged comparator briefs live here. It is **not** a related-case disclosure, **not** a brief, and **not** something to send to either firm.

| File | What it is |
|---|---|
| [`PLAYBOOK.md`](PLAYBOOK.md) | Read this. Two-desk comparison, *Carrillo* argument inventory, the seam between the defenses. |
| [`cases.json`](cases.json) | Append-only machine cards. One object per docket. |
| [`sources/`](sources/) | Lodged PACER prints. Not served on the public site. Seeded: *Carrillo v. Vons / Asurint* class-cert set (Dkts. 1, 55–59). |

The same six *Carrillo* PDFs are also cataloged on Matter 29 as comparator inventory (same pattern as *Lerma*) at `/documents/matter-29/carrillo-v-vons/`. Searchable sidecars sit next to those paths. The playbook `sources/` copies are the counsel-research lodge.

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

*Sandoval Carrillo v. The Vons Companies, Inc.*, C.D. Cal. No. **8:25-cv-00191-SRM-KES** (Murillo, J.):

| Dkt | Paper | Date | Why it is here |
|---|---|---|---|
| 1 | Class Action Complaint | Jan. 31, 2025 | Ray Kim pleading — same counsel as *Lerma*; § 290.46(j)(2)(E), Fair Chance, FCRA § 1681b(b)(1), UCL |
| 55 | Motion for Class Certification | Jan. 14, 2026 | 43 Megan's Law / 901 Fair Chance / 43 FCRA class numbers; standardized adverse-action notices |
| 56 | Vons opposition | Feb. 18, 2026 | Employer-side analog (Littler, **not** Frederick): § 290.46(j)(1) "person at risk," adequacy, same-decision |
| 57 | Asurint opposition | Feb. 18, 2026 | **Stanzick signed.** CRA playbook on paper: certification-only § 1681b(b)(1), *Mendoza*, fail-safe class |
| 58 | Reply to Vons | Mar. 25, 2026 | "Use of any"; (j)(1) as a common defense; circular adequacy attack |
| 59 | Reply to Asurint | Mar. 25, 2026 | Notices as common FCRA knowledge proof; no ascertainability in the Ninth Circuit |
