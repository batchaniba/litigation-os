# Kabat Chapman & Ozmer LLP — counsel research

Living dossier for **Chadwick L. Williams** and **Nathan D. Chapman**, Randstad's Matter 27 counsel.

| File | What it is |
|---|---|
| [`WILLIAMS_CHAPMAN.md`](WILLIAMS_CHAPMAN.md) | Read this. Identity, roles, Matter 27 posture, case cards, what is *not* a holding. |
| [`cases.json`](cases.json) | Append-only machine cards. One object per docket. |
| [`sources/`](sources/) | Lodged PACER prints and other primary pulls. Not served on the public site. Seeded: *Charter* (D. Conn.), *We Got U* (N.D. Ga.), *Sullivan* (N.D. Ga. docket + Dkts. 1, 5, 8, 14, 16, 19, 25, 29+29-1+29-2+29-3, 30+Ex. A, 32, 33, 34), Williams N.D. Ga. attorney query. |

## How to add the next case

1. Drop the PACER / portal prints under `sources/<court-case-no>-<short-caption>/` with a date in the filename.
2. Add a card to `cases.json` (copy the Charter card; do not invent fields).
3. Add a matching **Case card** section to `WILLIAMS_CHAPMAN.md`.
4. Update the working-pattern bullets only if the new docket actually changes them.
5. Do **not** register those PDFs on Matter 27's `documents[]` list, do **not** add a related-case link, and do **not** email Williams or Chapman about the research.

Identity and role intelligence only. A docket where they appeared for someone else is not a Civil L.R. 3-12 / CRC 3.300 related case unless a court says it is.

## Standing limits

- PACER username/password are never stored here and are never accepted in chat.
- Firm-website bios are **firm-claimed**. CalBar / other-bar lookups are a separate pass.
- Do not quote settlement numbers from Matter 27 into an email to this firm from this folder.
