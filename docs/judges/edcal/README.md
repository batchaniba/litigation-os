# E.D. Cal. judge profiles (Sacramento)

> Internal research notes, current as of 2026-10-29. Do not cite these notes, the downloaded PDFs, or any repo path in court papers. Cite the court's own orders and rules instead.
>
> Every claim below links to a source in the per-judge `summary.md` or to a source listed here. Anything not found says **not found**, and anything unconfirmed says **unverified**. No settlement figures or private data are included.

## Judges

| Judge | Role | Suffix | Profile |
|---|---|---|---|
| Dena Coggins | District Judge | DC | [coggins/summary.md](coggins/summary.md) |
| Daniel J. Calabretta | District Judge | DJC | [calabretta/summary.md](calabretta/summary.md) |
| Dale A. Drozd | District Judge | DAD | [drozd/summary.md](drozd/summary.md) |
| Troy L. Nunley | District Judge | TLN | [nunley/summary.md](nunley/summary.md) |
| Chi Soo Kim | Magistrate Judge | CSK | [kim/summary.md](kim/summary.md) |
| Jeremy D. Peterson | Magistrate Judge | JDP | [peterson/summary.md](peterson/summary.md) |
| Allison Claire | Magistrate Judge | AC | [claire/summary.md](claire/summary.md) |
| Sean C. Riordan | Magistrate Judge | SCR | [riordan/summary.md](riordan/summary.md) |
| Carolyn K. Delaney | Chief Magistrate Judge | CKD | [delaney/summary.md](delaney/summary.md) |

## Case-to-judge list

Judge assignments come from the case-number suffixes in the repo (`internal/src/data/matters/*/matter.json`) and were cross-checked against the public dockets cited in each profile.

### Active cases

| Matter | Case | District Judge | Magistrate Judge | Status (repo, as of Oct 28, 2026) |
|---|---|---|---|---|
| M25 FedEx | 2:26-cv-02881-DAD-SCR | Drozd | Riordan | Removed case in discovery. The Oct 8 status conference outcome is **unverified**. |
| M26 UPS | 2:26-cv-02847-DAD-CKD | Drozd | Delaney | MTD under submission since Sep 24 (Dkt 15). F&R pending. |
| M36 AT&T | 2:26-cv-03314-DJC-AC | Calabretta | Claire | IFP granted and screening passed Oct 14. **USM packet due Oct 29, 2026.** |
| M37 Home Depot | 2:26-cv-03310 (public sources) | Nunley (public sources) | **unverified** | The repo shows this as unfiled, but public listings show a case. **Reconcile on PACER.** |
| M38 Swift | 2:26-cv-03312-DC-SCR | Coggins | Riordan | IFP denied without prejudice Oct 5. **Renewed AO 239 or fee was due Oct 26, 2026**; neither appears in the repo. |
| M39 Best Buy | 2:26-cv-03315-DC-CKD | Coggins | Delaney | Fee paid Oct 27 per user report (receipt not ingested). Service is next. |

### Closed cases

| Matter | Case suffix | District Judge | Magistrate Judge |
|---|---|---|---|
| M01 | DC-CSK | Coggins | Kim |
| M03 | DJC-JDP | Calabretta | Peterson |
| M06 HOPE | TLN-AC | Nunley | Claire |
| M07 | DC-CSK | Coggins | Kim |
| M11 Macomber | **TBD in repo** | unverified | unverified |
| M13 | DC-SCR | Coggins | Riordan |
| M17 | DAD-SCR | Drozd | Riordan |
| M18 | DJC-CSK | Calabretta | Kim |
| M21 | DC-CKD | Coggins | Delaney |

- M07 was refiled in N.D. Cal. as M33 (3:26-cv-08272). That case is outside this folder.
- M21's judge field in the repo says TBD; the assignment above comes from its case suffix.

## District context
- **Judicial emergency.** The court says it has only six active district judgeships and about 2,400 immigration habeas petitions filed in three months of 2026. That is second in the nation, behind W.D. Tex., which has 13 judgeships. The court reports a 400% increase over 2025 and significant delays in other cases. Source: https://www.caed.uscourts.gov/caednew/index.cfm/news/judicial-emergency/
- **Caseload.** For the 12 months ending Sep 30, 2025, E.D. Cal. had **887 weighted filings per judgeship** (782 of them civil). The national figure was 534, and C.D. Cal. was 759. Source: Table X-1A, https://www.uscourts.gov/sites/default/files/document/jb_x1a_0930.2025.pdf
- **Pro se referral.** In Sacramento, every action where all plaintiffs or all defendants are pro se is referred to the magistrate judge, including dispositive motions. The magistrate judge issues F&Rs and the district judge rules on them. Source: L.R. 302(c)(21), Local Rules eff. Feb 23, 2026, https://www.caed.uscourts.gov/caednew/assets/File/EDCA%20LOCAL%20RULES%20EFF_%2002-23-26.pdf (the "LR" source below).
- **F&R objections** are due within 14 days, and replies to objections within 14 days after that (LR 304(b), (d)). Review of a non-dispositive magistrate-judge order must be sought within 14 days (LR 303(c)).
- **Motion timing.** Notice at least 35 days before the hearing (LR 230(b)). Opposition within 14 days after the motion is filed (LR 230(c)). Reply within 10 days after the opposition (LR 230(d)). The court may decide on the papers without a hearing (LR 230(g)); most judges here do so often.
- **Discovery.** Motions require meet and confer and a joint statement 14 days before the hearing, with 21 days' notice (LR 251). Each judge's own procedures are summarized in the profiles.
- **Pro se rules.**
  - Pro se parties are bound by the rules, and an address change must be filed within 30 days (LR 183).
  - Pro se parties cannot e-file without the judge's permission (LR 133(b)(2)).
  - Court pro se page: https://www.caed.uscourts.gov/caednew/index.cfm/cmecf-e-filing/representing-yourself-pro-se-litigant/
- **Consent.**
  - Magistrate-judge jurisdiction requires every party's consent (28 U.S.C. § 636(c); LR 305).
  - There are no adverse consequences for withholding consent, and judges are told only if all parties consent. Source: https://www.caed.uscourts.gov/caednew/index.cfm/judges/consent-to-proceed-before-a-magistrate-judge/
  - An **Opt-Out Civil Consent** program began Feb 1, 2026. Source: https://www.caed.uscourts.gov/caednew/index.cfm/news/opt-out-consent/
  - Judge Claire's standing order says magistrate-judge trial calendars are "generally less congested."
- **IFP screening.** "Notwithstanding any filing fee … that may have been paid, the court shall dismiss the case at any time" if it is frivolous or malicious, fails to state a claim, or seeks money from an immune defendant. Source: 28 U.S.C. § 1915(e)(2), https://www.law.cornell.edu/uscode/text/28/1915
- **Leave to amend for pro se.** The sample orders apply Lopez v. Smith, 203 F.3d 1122 (9th Cir. 2000) (en banc): leave is granted unless amendment would be futile. Futility dismissals without leave do occur (Claire/Olson, Riordan/Chiu, Delaney/Walker, Kim, Peterson; see the profiles).

## Comparison table

| Judge | Page limits (motion and opposition / reply) | Hearing day and mode | Courtesy copies | Proposed-order email | Discovery | F&R or screening timing observed |
|---|---|---|---|---|---|---|
| Coggins (DJ) | 25 / 15 | 1st and 3rd Fridays 1:30 pm, in person | TRO only | DCorders@ | Goes to the MJ | Adopted F&Rs 3 weeks to 4 months later; M01 F&R unruled ~116 days, M07 ~61 days |
| Calabretta (DJ) | 25 / 15 | Thursdays 1:30 pm, in person; remote disfavored | not found | DJCorders@ (TRO and PI only) | Goes to the MJ; meet-and-confer certification or summary denial | Adopted F&Rs 22 to 71 days later |
| Drozd (DJ) | 25 / 15 | 1st and 3rd Mondays 1:30 pm, Zoom only | None except TRO | dadorders@ | Goes to the MJ | Adopted F&Rs 64 days to ~4 months later |
| Nunley (DJ) | 20 / 10 (extra pages requested 14 days ahead) | Thursdays 2:00 pm; phone appearance requested 7 court days ahead | None | tlnorders@ | Caption "DISCOVERY MATTER"; goes to the MJ | Adopted F&Rs 29 to 91 days later |
| Kim (MJ) | 20 / 10 | Tuesdays 10:00 am, in person | see profile | CSKorders@ | 2-page joint letter for informal conference | M07 F&R 49 days after FAC; M01 F&R ~3.5 months after MTD reply |
| Peterson (MJ) | see profile | Thursdays 10:00 am, generally Zoom | None | jdporders@ | Pre-motion Zoom conference; 3-page briefs, no attachments | M03 MTD granted with 14 days to amend |
| Claire (MJ) | 20 / 10 (or stricken) | Wednesdays 10:00 am, in person; pro se preference given "significant weight" | Only discovery joint statements (mandatory, tabbed) | acorders@ | Joint statement 25 pages; email conferral insufficient; 2-page letter for informal conference | M36 screened 26 days after filing |
| Riordan (MJ) | 20 / 10 | Thursdays 10:00 am, in person; remote on hardship, requested 10 days ahead | not found | SCRorders@ | Joint statement 20 pages; 2-page letter 48 hours before informal conference | M38 IFP ruling 17 days after filing |
| Delaney (MJ) | 30 / 10 | Wednesdays 10:00 am, Zoom | None "until further notice" | ckdorders@ | Voice-to-voice conferral; 2-page letter 24 hours before informal conference | Screening in 3 to 7 days in samples; M26 MTD pending since Sep 24 |

All email addresses above are @caed.uscourts.gov. F&R rejection or modification rates: **not found** for any judge.

## Per-judge filing checklist

General rules for every filing:
- Use the full case number with both judges' initials.
- File on paper or by the court's pro se method unless e-filing permission has been granted (LR 133(b)(2)).
- Keep the address current (LR 183).
- Never cite the repo or these notes.

**Coggins**
- 25/15 page limits in 12-pt type; ask for more pages 7 days ahead.
- Redline any amended pleading.
- Proposed orders only for administrative, ex parte, or TRO matters, in Word to DCorders@.
- Ex parte relief is "rarely appropriate."
- Object to F&Rs within 14 days.

**Calabretta**
- 25/15 page limits.
- Include the meet-and-confer certification where required.
- Give "specific, concrete reasons" for extensions.
- No proposed orders except TRO or PI.
- Plan to appear in person.

**Drozd**
- 25/15 page limits in Times New Roman 12; no supplemental briefs.
- Expect Zoom hearings or submission on the papers.
- TRO needs a courtesy copy plus a proposed order to dadorders@.
- Expect a long F&R review time.

**Nunley**
- 20/10 page limits; ask for more pages 14 days ahead.
- Request a phone appearance 7 court days ahead.
- Do not contact chambers.
- A stipulation alone is not good cause.

**Kim**
- 20/10 page limits; no sur-replies.
- Request a Zoom appearance 7 days ahead.
- Pro se parties should not email chambers.
- Expect IFP scrutiny at screening.

**Peterson**
- Confer by phone or video, not email, then request a Zoom discovery conference.
- 3-page informal briefs with no attachments.
- Meet any amendment deadline; he set 14 days in M03.

**Claire (M36)**
- File the USM packet and Notice of Submission by Oct 29, 2026.
- Follow the Initial Scheduling Order (Dkt 5).
- 20/10 page limits.
- Tell the CRD your hearing-mode preference at least 1 week ahead.
- Discovery: talk-based conferral, a 25-page joint statement 14 days before the hearing, and a tabbed courtesy copy.

**Riordan (M25, M38)**
- M38: renewed AO 239 or fee (overdue since Oct 26; check the docket for an OSC).
- 20/10 page limits; internally paginated exhibits.
- Request a remote appearance in writing 10 days ahead, citing hardship.
- Proposed orders to SCRorders@ with the subject "proposed order [case no.]".

**Delaney (M26, M39)**
- M26: watch for the F&R, then object within 14 days (LR 304(b)).
- M39: serve under FRCP 4.
- 30/10 page limits.
- Discovery: voice-to-voice conferral, and a 2-page letter to ckdorders@ 24 hours ahead.

## Unverified or not found
1. M37 Home Depot: the repo says unfiled, but public sources show 2:26-cv-03310 before Nunley. The magistrate judge is unknown, and a search-engine claim naming Riordan is unsupported.
2. M11 Macomber: the case number and judges are TBD in the repo.
3. M21: the repo judge field says TBD; the assignment comes from the case suffix only.
4. M26: the repo docket lists the MTD as Dkt 7, but the status says "Live MTD is Dkt. 9." The outcome of the reassignment request is unverified.
5. M25: the Oct 8 status conference outcome.
6. Nunley's HTML standing order has no revision date; a snapshot is saved in `nunley/`.
7. Claire's telephonic discovery policy has no revision date.
8. CourtListener returned HTTP 403, so its data was not used.
9. F&R adoption, rejection, and modification rates were not found for any judge.
