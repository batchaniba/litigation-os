# Matter 25 — Rule 30(b)(6) deposition of FedEx (internal, do not send)

`HOLD - Notice of Rule 30(b)(6) Deposition of FedEx (unsigned, undated).pdf`: a notice with **Schedule A (20 matters)** and a proof of service, on pleading paper. Generator: `internal/scripts/matter25-30b6-notice.py`.

## When
- **After** FedEx's responses to Set One (due about 30–33 days after service) and its document production. The designee should be questioned with the report, the adjudication criteria, and the access logs in hand.
- Target: December 2026 – January 2027, well before the fact-discovery cutoff the Oct. 8 scheduling order sets.
- Give reasonable notice: at least 14 days, and more is better for a corporate designee.

## Before you serve it (Rule 30(b)(6) requires this)
1. **Meet and confer with Kray, live by phone or video** (Judge Riordan requires it), about the matters in Schedule A, the number of designees, date, place, and recording method. Rule 30(b)(6) requires a good-faith conference "before or promptly after" the notice.
2. **Remote deposition:** Zoom needs a stipulation or court order (Rule 30(b)(4)). Ask Kray to stipulate. It saves travel to Irvine or Memphis.
3. **Court reporter:** you arrange and pay for an officer authorized to administer oaths (Rule 28). Budget roughly $1,000–$3,000 for a full day with transcript. Audio-visual recording is optional and costs more. Get quotes first.
4. Then render the served version:
   ```
   python3 internal/scripts/matter25-30b6-notice.py --stamp-signature --date "<service date>" \
     --depo-date "<date>" --depo-time "9:30 a.m. Pacific" \
     --depo-place "By remote videoconference (Zoom) under Fed. R. Civ. P. 30(b)(4), by stipulation" \
     --recording "stenographically by a certified shorthand reporter" \
     --mailed-from "San Jose, California" --also-email
   ```
   Serve on Kray (mail + email the same day). **Do not file.**

## Limits
- Counts as **one** deposition toward the 10-deposition limit (Rule 30(a)(2)(A)(i)), even with several designees.
- Each designee is limited to 1 day of 7 hours (Rule 30(d)(1), Advisory Committee Note).

## What to expect from FedEx
- **Scope objections** to the policy topics (16), the discovery-on-discovery topic (20), and "any time" on prior hires (3). Narrow them at the meet-and-confer rather than drop them.
- **Contention topics** (11, 13, 15) sometimes draw "ask by interrogatory" objections. The interrogatories already ask; the deposition tests the answers with a live witness.
- If the designee isn't prepared on a topic, that is a failure to appear for that topic. Note it on the record and raise it in the meet-and-confer. Don't argue with the witness.

## The matters, by purpose
| Purpose | Matters |
|---|---|
| Right entity (Express vs. Ground) | 1 |
| Registry drove the decision | 5, 6, 7, 8, 9, 10, 12, 18 |
| "Misrepresentation" came later / inconsistent with prior hires | 2, 3, 11 |
| Person-at-risk defense | 13, 14 |
| No legal requirement to screen | 15 |
| Policies and process | 16, 17 |
| Damages | 4 |
| Records integrity | 19, 20 |

Caution: Matters 3 and 11 put your prior applications and answers squarely in play. FedEx will use the same testimony. Prepare for your own deposition before this one.
