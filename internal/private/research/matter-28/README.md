# Matter 28 - Cisneros hearing preparation

**Newanforbi v. Smith et al., N.D. Cal. 3:26-cv-07504-LJC**  
Research branch: `research/matter-28-cisneros-hearing-2026-10-25`  
Prepared October 25, 2026, America/Los_Angeles. Private working analysis; nothing here has been filed, served, or adopted by the Court.

## Start here

1. [Hearing command sheet](10-hearing-prep/00-HEARING-COMMAND-SHEET.md): objectives, appearance logistics, essential record checks, and requested rulings.
2. [Argument and record map](09-evidence-map/RECORD-TO-ARGUMENT-MAP.md): complaint paragraphs, motion/opposition/reply pages, adverse points, and missing proof.
3. [Oral argument](10-hearing-prep/01-ORAL-ARGUMENT.md): short opening, modular answers, and closing request.
4. [Judge-question drill](10-hearing-prep/02-JUDGE-QUESTIONS.md): difficult questions with concise proposed answers and supporting locators.
5. [Amendment proffer](10-hearing-prep/03-AMENDMENT-PROFFER.md): specific cures to identify if the Court finds pleading defects; no invented facts or automatic concessions.
6. [CMC and protective-order plan](10-hearing-prep/04-CMC-AND-PROTECTIVE-ORDER.md): the existing scheduling proposals, practical discovery sequence, and prior-production issue.
7. [Rehearsal and outcome checklist](10-hearing-prep/05-REHEARSAL-AND-OUTCOMES.md): preparation order, hearing notes, and next steps for each ruling.
8. [Verified hearing facts](10-hearing-prep/06-VERIFIED-HEARING-FACTS.md): setting, in-person rule, tentative-ruling procedure (there is none), chambers-contact rules, morning-of checklist.
9. [Reply rebuttal matrix](10-hearing-prep/07-REPLY-REBUTTAL-MATRIX.md): each ECF 30 argument, a short spoken answer, locators, and what not to say.
10. [Timeline](09-evidence-map/TIMELINE.md): sourced chronology through the hearing and the post-ruling deadlines.
11. [Citation table](09-merits-analysis/CITATION-TABLE.md): every reported case in the motion, reply, and opposition, existence-checked; two unverified.
12. [Authority verification](09-merits-analysis/AUTHORITY-LEDGER.md) and [record conflicts](08-audit/GAPS-AND-CONFLICTS.md): what has actually been checked and what remains open.

## Hearing identity

The live repository clock `28-hearing-mtd` and ECF 29 set the combined **motion-to-dismiss hearing and initial CMC for Tuesday, October 27, 2026, 10:30 a.m. Pacific, Courtroom G, 15th Floor, San Francisco**. The preserved ECF 29 was signed October 6 and filed October 8. A later order or clerk notice controls if one exists; this collection is not a PACER docket refresh.

The Court's current linked civil standing order is dated **February 17, 2026**. It expressly makes motion hearings in person unless otherwise ordered. The ordinary Thursday Zoom CMC schedule does not convert this specially combined Tuesday hearing to Zoom. Verify the current docket and any remote-appearance ruling. See [current rules review](06-source-snapshots/CURRENT-COURT-RULES-REVIEW.md).

## Three substantive corrections

- **The signed state demurrer order is not labeled exhaustion-only.** Its operative language sustains the demurrer without leave because the FAC fails to allege facts sufficient to state any cause of action. The reasons must be established from the actual state record before making a narrower characterization. The absence of an express dismissal remains a separate argument, now opposed by defendants' substance-over-form cases and docket screenshot.
- **Use the complaint's actual count order:** I = Smith individual capacity; II = HOPE entity liability; III = Bane Act; IV = fraud/negligent misrepresentation; V = RICO. `claims.json` reverses the first two labels. The snapshot is preserved without changing the live graph.
- **Correct the regulatory pinpoints:** section 3574(d) addresses completion before parole discharge; (e) separates treatment review from discharge/electronic monitoring; the introductory text of (f) requires written, jointly signed good-cause retention determinations and delivery within 30 days. Subdivision (f)(1) is the LS/CMI factor, not the general procedural rule.

## Relationship to the Matter 20 branch

This room follows `research/matter-20-2026-10-24/internal/private/research/matter-20`: preserved sources, independent graph snapshots, extracted text, audit/provenance, a record-to-argument map, and separately authored analysis. It starts from **main at eaacea3e448e8296ca7747b5765b4ccb5d15cb4b**, rather than importing Matter 20's unrelated case edits.

| Directory | Purpose |
|---|---|
| `00-user-inputs/` | Exact instruction and scope |
| `01-portfolio-records/` | Complaint, federal motion/reply record, orders, CMS, disclosures |
| `02-prior-proceeding/` | Signed San Joaquin order and two preserved FAC versions |
| `03-discovery-production/` | Restricted-production locator and use boundary; no duplicated confidential production |
| `04-drafts-and-working-papers/` | October 14 proposed protective order and service certificate |
| `05-prior-analysis/` | Historical discovery and judge/citation memoranda, preserved without adopting their claims |
| `06-source-snapshots/` | Matter 28 graph siblings, current rules review, source retrieval results |
| `07-source-text/` | Complaint/motion/order text and existing opposition/reply/PO sidecars |
| `08-audit/` | Source aliases, inventory, hashes, verification report, and retrieval gaps |
| `09-evidence-map/` | Pleading-to-argument matrix |
| `09-merits-analysis/` | Bounded authority checks and adverse-authority analysis |
| `10-hearing-prep/` | Actual hearing preparation and rehearsal materials |

The manifest distinguishes Git blob identity from registered SHA-256 and independently verified SHA-256. Copying an existing Git blob preserves exact bytes; it does not represent independent PDF review of every copied page. The complaint is a historically filed-designated copy with a blank case-number line, not a newly recovered ECF-stamped original. The reply identifies the opposition as ECF 23; that identification is attributed to the reply until a stamped opposition or current docket is checked.

## Working rules

Keep allegations, evidence, judicial findings, historical analysis, and proposed amendments distinct. Cite existing complaint paragraphs when defending Rule 12 sufficiency. New evidence is not an amendment, and oral argument is not testimony. A protective order does not automatically authorize reuse of discovery restricted by another court's order.

All live docket/calendar/public registry/R2 data remain in their original homes. Do not publish, register, or deploy this room. Private location alone does not establish a legal privilege. No settlement figure is proposed here.
