# Matter 20 — Filing set as of Oct. 24, 2026 (handoff)

*Newanforbi v. California Highway Patrol*, Alameda Sup. Ct. No. 26CV191136. Motion for peremptory writ of mandate on the surviving First Cause of Action. **Hearing: Jan. 8, 2027, 9:00 a.m., Dept. 25** (Hon. Jenna M. Whitman). **Nothing has been filed or served.**

Related: [Product 14 – Corrected merits exhibit schedule](https://github.com/newanforbi/interactive-litigation-portfolio/blob/research/matter-20-2026-10-24-integrated-writ/internal/private/research/matter-20/13-integrated-writ-reconstruction/14-CORRECTED-MERITS-EXHIBIT-SCHEDULE.md) (commit 7032d96) · [14A – Redaction log](https://github.com/newanforbi/interactive-litigation-portfolio/blob/research/matter-20-2026-10-24-integrated-writ/internal/private/research/matter-20/13-integrated-writ-reconstruction/14A-REDACTION-LOG.md) (commits 3cc5fde, 08cdbdd).

## Folders
- `out/redacted/` is the **public-filing set**. It has 13 PDFs (each about 10 MB or less) plus preview PNGs:
  - Notice of Motion
  - Memorandum of Points and Authorities
  - Declaration (standalone)
  - Declaration with Exhibits A–I (91 pp)
  - Exhibits A–I Appendix (84 pp)
  - Alternative A proposed writ and proposed judgment
  - Alternative B proposed writ and proposed judgment
  - Alternative proposed order setting limited evidentiary proceedings
  - Blank proof of service
  - Motion Packet (33 pp)
  - Motion Packet with Exhibits A–I (117 pp)
- `out/unredacted/` is **CONFIDENTIAL and not for public filing**. It holds the Appendix, the Declaration with Exhibits, and the Packet with Exhibits, each with " - UNREDACTED" in its name.
  - These are identical to the redacted versions except that the appendix pages are not redacted.
  - Every appendix page carries the stamp "UNREDACTED – CONFIDENTIAL – NOT FOR PUBLIC FILING (CRC 1.201)".
  - The declaration's CRC 1.201 text describes the redacted copy and was left unchanged.
  - This folder is committed only because the repo is private.
- `build/` contains the scripts and sources needed to rebuild the set (see below).

## State of the filing set
- **Exhibits (App. ranges):**

  | Exhibit | Contents | App. pages |
  |---|---|---|
  | A | Apr. 20, 2026 denial letter | 001–002 |
  | B | Apr. 9 I-918B package, reconstructed working copy | 003–025 |
  | C | CHP production Ex. 5 (arrest report, DS 367, warrant, etc.) with Bates index | 026–052 |
  | D | CAD incident log | 053–056 |
  | E | CHP 415 activity records | 057–059 |
  | F | Petitioner's 15-page dashcam transcript | 060–075 |
  | G | PC 851.6 certificate | 076–077 |
  | H | CHP/POST correspondence | 078–080 |
  | I | Beat sheet | 081–082 |

  Each range includes its slip sheet.
- **Redactions:**
  - Applied as true raster redactions to App. 019, 023, 028, 031, 032, 039–041, 043–045, 047–049, 051, 054, 055, 070 and 082. Each of those pages was re-rendered at 200 dpi as an image, the boxes were burned in, and an OCR text layer was added.
  - The boxes were tightened to the value's own line on Oct. 24.
  - Text layers, raw streams and 300-dpi OCR were verified with zero hits.
- **Slip sheets:** these are on pleading paper. Each has a black band spanning from the right margin line to the right content edge, with exhibit letter, title, source and App. range. The grey parent-document line sits below the footer rule.
- **Signatures:** the signature image is placed in the Notice (p. 3) and the MPA (p. 15). The source is the repo's `internal/assets/signature/brendan-newanforbi-signature.png` (main).
- **Exhibit F:** the transcript's own `/s/` (App. 075) was intentionally left as is.

## How to rebuild
The scripts expect the following layout. Paths are hard-coded in the scripts, so edit them if your layout differs.
- `/workspace/m20-pleading/`: contains `build.py`, `src/*.md`, `appendix/`, `assets/sig.png` and `out/`.
- `/workspace/m20-merge/iw`: a worktree of this branch, used for source records.
- `/workspace/m20-merge/repo`: a worktree of main. The build needs `internal/scripts/lib/pleading_paper.py` from it.

Steps:
1. Copy `build/*` to `/workspace/m20-pleading/`, and put `compress.py` and `dedup.py` in `/workspace/`. Copy the signature PNG from main to `assets/sig.png`.
2. **Recreate `appendix/redact_ids.local.json`.** It is gitignored and deliberately not committed. It has the keys `IDS` (the identifier strings to box), `OFF` (offense strings to box with a [REDACTED] label), `P32_PREFIX` and `VERIFY_EXTRA` (extra identifiers to verify only).
   - The values are listed by category in 14A. Get the actual strings from the source records.
   - The redaction script will not run without this file.
3. Run `python3 build.py` to build the standalone papers and the packet without exhibits.
4. Run `cd appendix && MODE=all python3 build_appendix.py` (about 4 minutes) to build the Appendix, the Declaration with Exhibits and the Packet with Exhibits.
   - This also writes `appendix/body_unredacted.pdf`. **Never commit it** or any other unredacted intermediate.
5. Compress each output: `python3 /workspace/compress.py in.pdf tmp.pdf && python3 /workspace/dedup.py tmp.pdf && mv tmp.pdf in.pdf`.
6. Verify with `python3 build/verify.py`, run from `out/`. It checks text-layer and raw-stream hits, page counts, sizes and bookmarks.
7. To build the unredacted set, run `python3 appendix/build_unredacted.py`, then compress the outputs. The script writes to `out/unredacted/`.

`crops.py` and `sbs.py` are review aids that make box crops and before/after side-by-sides (FAST=1 mode of `redact.py`).

## Open items
- **Declaration blanks:**
  - execution date and city
  - ¶ 6: no charge was filed (needs confirmation)
  - ¶ 9: how the denial was received
  - ¶ 10: April 9 as-sent comparison
  - ¶ 14: which transcript edition
  - ¶ 16: the complaints
- **Signature lines:** the standalone papers still have blank wet-signature lines.
- **Five exhibit gaps (Product 14 §4):**
  1. Compare the April 9 package as sent.
  2. Authenticate the video and settle which transcript version applies, and cure the Sept. 8 lodging proof-of-service rejection.
  3. Locate the CHP/POST complaint copies (Exhibit H is correspondence only).
  4. Find out what the beat sheet's "On Call" entry means.
  5. Check that the petition index and the Answer's citations conform.
- **Not redacted (decision pending):** the VIN, the search warrant number and the residential address.
- **Not filed or served.** Deadlines run from the Jan. 8, 2027 hearing.
