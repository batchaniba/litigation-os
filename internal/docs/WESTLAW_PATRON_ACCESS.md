# Westlaw Patron Access via San Diego Law Library

Intel note — verified live 2026-09-19 via a real browser session (sign-in, one test
citation lookup, KeyCite URL mapping, sign-out). This is the only working Westlaw
door for this portfolio. It fills the one gap no free source covers: **KeyCite
treatment flags**.

## The only working entry route

1. `sandiegolawlibrary.org` → "Westlaw Remote for Non-Attorneys" → **"Westlaw Remote
   for Pro Se"** page (`https://sandiegolawlibrary.org/westlaw-remote-for-pro-se/`)
2. Click **"Click Here for Access to Westlaw Remote for Pro Se"**
3. OnePass sign-in for **"Westlaw Patron Access for Pro Se (for non-commercial use)"**
   (URL carries `productid=RPA`, return host `westlawpatronaccess.thomsonreuters.com`)

Do NOT go to `westlaw.com` directly. It redirects to the generic OnePass sign-in
(`productid=CBT`), which accepts the credentials but then demands a **registration
key** the account does not have — because the entitlement is provisioned through the
library, not the profile. Going directly to Westlaw to log in will not work, per the
library's own page.

## Credentials and 2FA

- The saved OnePass username + password (Secure Vault) is accepted at the Patron
  Access sign-in.
- OnePass then requires **SMS 2-step verification** to the phone on file (observed:
  number ending 4442). The code arrives by text; the user relays it.
- New users must complete OnePass registration + email validation + 2FA (cell phone)
  before first use.

## Seat and usage limits (shared pool — everyone, not per-user)

- **2 concurrent seats** for all pro-se patrons. If both are busy: "cannot obtain
  access at this time, try again later." Retry later; do not hover.
- Entry **only** via the library's access link.
- Download/email limit: **20 documents per session, 150/day combined for both seats.**
- Always use **Sign Off** when done to release the seat.

## Citation-funnel hookup verdict: manual spot-checks only, NOT scriptable

A scripted GET-based probe from a bare citation is not feasible:

- The `docGuid` (Westlaw's internal document ID) is **not derivable from the citation
  string** — a script must first perform a JS-driven search to resolve citation →
  docGuid. No simple GET search URL was observed.
- The `docSource` token changes between navigations (per-navigation/session state,
  not a stable per-document token); `ppcid` on the flag link is likewise per-click.
- Host alternates between `next.westlaw.com` and `1.next.westlaw.com`.
- Auth needs the library's special entry link, a live OnePass session, and periodic
  SMS 2FA; concurrency is capped at 2 shared seats.

So: KeyCite treatment checks are **manual browser spot-checks on request**, run in
one batched session after a draft is frozen (see workflow below). Nothing about this
changes the scripted funnel (`internal/scripts/lookup-citations.py`), which keeps
handling existence + pin verification from free sources.

## URL patterns (observed 2026-09-19, Westlaw Edge)

- Document page:
  `https://next.westlaw.com/Document/{docGuid}/View/FullText.html?transitionType=UniqueDocItem&contextData=(sc.Default)&userEnteredCitation={citation}`
- KeyCite negative treatment:
  `https://next.westlaw.com/RelatedInformation/{docGuid}/kcNegativeTreatment.html?originationContext=documentTab&transitionType=NegativeTreatment&contextData=(sc.UserEnteredCitation)&docSource={token}&rulebookMode=false`
- KeyCite citing references:
  `https://1.next.westlaw.com/RelatedInformation/{docGuid}/kcCitingReferences.html?originationContext=negativeTreatment&transitionType=CitingReferences&contextData=(sc.UserEnteredCitation)&docSource={token}&rank=0&rulebookMode=false`
- Flag link target:
  `https://1.next.westlaw.com/Link/RelatedInformation/Flag?documentGuid={docGuid}&transitionType=Document&originationContext=docHeaderFlag&Rank=0&ppcid={token}&contextData=(sc.UserEnteredCitation)`
- The KeyCite flag sits in the document header (colored flag image, clickable) and
  navigates to the negative-treatment view. `kcHistory.html`, `kcFilings.html`, and
  `kcTableOfAuthorities.html` presumably follow the same `RelatedInformation/{docGuid}/`
  pattern (not opened during the probe).

## Efficient verification workflow (post-draft)

1. **Verify once, against the frozen draft.** Cite lists churn mid-draft; earlier
   checks don't stick.
2. **Run the scripted funnel first.** Existence + pin checks are free and instant —
   Westlaw time covers only what the script can't: KeyCite treatment flags, plus any
   cites the script left UNRESOLVED.
3. **Batch into one session.** Pull every citation into a single deduped list before
   signing in, so seat time is pure lookups.
4. **Prioritize load-bearing authorities** (the cases the argument actually stands
   on) for full treatment reads; string-cite passengers get a flag glance.
5. **Exhaust each cite in a single visit.** Document views are the scarce resource
   (20/session), so never spend two sessions on one citation: per cite, do one
   search, note the flag color, open the negative-treatment tab on yellow/red, and
   capture everything then — the full treatment list (courts, dates, treatment types)
   plus the actual passages and quotes for any treatment that could touch the
   proposition cited for. A yellow flag on an unrelated point doesn't sink the cite,
   but record *why* so nobody re-reads it later. Budget the 20 views: flag-glance the
   whole batch first, then spend deep-read views only on flags that could matter
   (standing rule adopted 2026-09-19 after the KeyCite + deep-dive sessions).
6. **Session hygiene:** in through the library link, whole batch in one go, Sign Off
   to free the seat. If both seats are busy, walk away and retry later.
7. **Feed results back** into the matter's verification notes so the next draft
   doesn't re-check the same cases.

See also: the live portfolio KeyCite queue — [`WESTLAW_PORTFOLIO_QUEUE.md`](WESTLAW_PORTFOLIO_QUEUE.md) and the printable [`WESTLAW_PORTFOLIO_QUEUE.pdf`](WESTLAW_PORTFOLIO_QUEUE.pdf) (`python3 internal/scripts/build-westlaw-queue.py && python3 internal/scripts/render-westlaw-queue-pdf.py`).

## Provenance

- Live browser session 2026-09-19 (~02:08–02:15 PDT): library-route sign-in with
  saved OnePass credentials + SMS 2FA, one test lookup, URL-pattern mapping, Sign Off.
- Test lookup `"384 F.3d 1184"` → *Swift v. California*, 9th Cir., Oct. 5, 2004 —
  carries a **KeyCite yellow flag** (some negative treatment; not overruled/reversed).
  Flag does not affect pin/existence use of the cite.
- No charge warnings, no CAPTCHA / bot checks, no rate limiting observed on Patron
  Access. No case content was copied or downloaded — URLs and structural observations
  only.

## See also

- `internal/docs/CITATION_SOURCE_SURVEY.md` — free-source survey; Westlaw is MANUAL ONLY
- `internal/docs/citation_verification_sources.json` — catalog row `westlaw_patron_prose`
- `internal/docs/legal-intel/recon/2026-09-19-matter-28-keycite-westlaw.md` — 27/27 UNIFIED KeyCite
