# Citation-verification source survey

Machine-readable companion (wired / opt-in / gap, plus these control results): `internal/docs/citation_verification_sources.json`.

Live-tested 2026-09-19 from a headless datacenter IP (plain HTTPS, no JavaScript, no credentials except where a 401 proved a token is required). This is infrastructure, not legal advice. It does not verify any portfolio brief.

**Control set used**

| ID | Cite | Role |
|---|---|---|
| C1 | *Richardson v. McKnight*, 521 U.S. 399 (1997) | Positive, canonical, old |
| C2 | *Medical Marijuana, Inc. v. Horn*, 604 U.S. 593 (2025) | Positive, recent SCOTUS / coverage cliff. Official **preliminary-print** pagination (Volume 604 U.S. Part 2, pages 593–649) is already posted at supremecourt.gov. Bound volume has not replaced it. |
| C3 | *United States v. Paul*, 239 F. App'x 353 (9th Cir. 2007) | Positive, unpublished 9th Cir. memorandum in F. App'x |
| C4 | *Goddard v. Security Title Ins. & Guar. Co.*, 14 Cal.2d 47 (1939) | Positive, old California official reporter |
| C5 | `2016 WL 4761808` as specified, plus a known-real comparator `2016 WL 3945692` (*Korenblum v. Citigroup*, which also has 195 F. Supp. 3d 475) | Positive, Westlaw-only / WL-number resolution |
| C6 | *Dennis v. Evans*, No. 24-6244 (4th Cir. Aug. 2, 2024) | Positive, docket-number-only. **Collision:** the same number is also *Estate of Jill Ann Esche v. Bunuel-Jordana* (9th Cir.), *United States v. Velazquez Hernandez* (10th Cir.), and a SCOTUS IFP docket. |
| C7 | *Zellerman v. Northbridge Holdings*, 999 F.4th 1 (9th Cir. 2024) | Negative. Invented this session. Correct in form, nonexistent. |
| C7b | *In re Leman*, 66 Cal.App.5th 200 | Negative. Known fabrication already in this portfolio's gate. |

A source that returns a case for C7 and presents it as a hit is disqualified as a verification source.

Probe script: `internal/scripts/survey-citation-sources.mjs` (re-runnable). Raw status dump from this session is not committed.

---

## Priority 1 — core probe sources

```
SOURCE: CourtListener REST search API (unauthenticated)
URL TESTED: https://www.courtlistener.com/api/rest/v4/search/?q=%22521%20U.S.%20399%22&type=o
           and fielded https://www.courtlistener.com/api/rest/v4/search/?type=o&q=citation%3A%22521%20U.S.%20399%22
REACHABLE FROM A SERVER?: YES
HTTP RESULT: 200 application/json on every control query this session (no 429 in ~20 sequential calls)
ACCESS: free-no-auth
API OR URL PATTERN: GET /api/rest/v4/search/?type=o&q=citation:"{vol} {reporter} {page}"
  Constructible from (reporter, volume, page) as a query, not as a path.
  Bare q="{cite}" is full-text and will return citing cases. Do not use it as a pin probe.
  type=d / type=r search dockets (RECAP). type=o is opinions.
RESPONSE FORMAT: JSON (HTML if a browser Accept header is sent)
RATE LIMIT: Docs state authenticated users 5/min, 50/hour, 125/day (rolling).
  Anonymous search is intentionally left open; no numeric anonymous cap is published.
  Citation-lookup (below) is a separate 60-valid-cites/min throttle and requires a token.
  Weekly maintenance window Thu 21:00–23:59 PT.
COVERAGE: 3,359 jurisdictions in the CL court table. Federal + state + some agencies.
  This session: C1, C2 (including official 604 U.S. 593 on a cluster dated 2026-01-20),
  C3 (F. App'x), C4 (Goddard via caseName), C6 (only the 9th Cir. collision, not the 4th Cir. target).
STAR PAGINATION?: NO in the search JSON. Snippets are unpaginated OCR/plaintext.
  Opinion HTML this session returned HTTP 202 with a 0-byte body — not usable as a pin source
  from this IP/UA. Detail /opinions/ and /clusters/ endpoints 401 without a token.
UNPUBLISHED DISPOSITIONS?: Indexed. C3 resolved to United States v. Paul. status field
  is "Published" even on some memoranda; do not treat status=Published as F.3d/F.4th.
  F. App'x is the reliable unpublished-circuit signal when present.
SUBSEQUENT HISTORY?: citeCount on the cluster is a raw later-cite tally, not KeyCite/Shepard's.
  /api/rest/v4/opinions-cited/ is the citation graph — 401 without a token.
  No overruled / vacated / depublished flag on the search record.
CONTROL RESULTS: C1 FOUND Richardson, citation array includes 521 U.S. 399 (fielded citation: count=1)
  | C2 FOUND Medical Marijuana, Inc. v. Horn, citation=["604 U.S. 593"], download_url is the
    official preliminary-print PDF; an older sibling cluster still has "Citations: None known"
  | C3 FOUND United States v. Paul at 239 F. App'x 353 (citation= parameter, count=1)
  | C4 BARE q="14 Cal.2d 47" returned 81 HITS starting with Boyd v. Freeman (2017) — citing cases,
    not Goddard. Fielded caseName:Goddard DID find Goddard with ['14 Cal. 2d 47'].
    citation=14 Cal. 2d 47 (unquoted) also returned citing cases first (Angell v. Peterson Tractor).
  | C5 2016 WL 4761808 → count=0. 2016 WL 3945692 → Korenblum (also has an F. Supp. 3d cite).
    westlawCite: field is unused (0 hits). No first-class WL index.
  | C6 q=24-6244 type=o → Estate of Jill Ann Esche (9th Cir.), NOT Dennis v. Evans (4th Cir.).
    type=d → 31 dockets. docketNumber:"24-6244" type=o → still only the 9th Cir. case.
  | C7 nothing returned (count=0) | C7b nothing returned (count=0)
LICENSE: /terms/ returned CloudFront 403 from this IP. Bulk-data page (fetched):
  "Our bulk data files are free of known copyright restrictions."
  Opinion text is court-issued. Token: create a free account at courtlistener.com;
  token is on the profile page. Header: Authorization: Token <key>
FAILURE MODE: Bare full-text q= on a real pin returns citing cases and will happily
  hand you the wrong caption. Docket-number search without court_id collides.
  First hit is not unique. Table-page / multi-cluster pins surface as status=300 only
  on the token citation-lookup API, not here.
VERDICT: WIRE IN (tier 1) as the primary *existence* probe — but ONLY with fielded
  citation:"…" plus a caption check, or (better) the token citation-lookup API.
WHY: Reachable, JSON, free, returns empty cleanly on the negative controls, and is
  the only live index that has both 1997 U.S. Reports and 2025 preliminary-print 604 U.S. 593.
```

```
SOURCE: CourtListener citation-lookup API
URL TESTED: POST https://www.courtlistener.com/api/rest/v4/citation-lookup/  (body text=521 U.S. 399, no token)
REACHABLE FROM A SERVER?: YES (endpoint answers)
HTTP RESULT: 401 {"detail":"Authentication credentials were not provided."}
ACCESS: free-with-token
API OR URL PATTERN: POST application/x-www-form-urlencoded
  text={block of text}  OR  volume=&reporter=&page=
  Constructible from (reporter, volume, page). This is the actual pin API.
RESPONSE FORMAT: JSON per citation: status 200 (resolved) / 404 (valid form, no cluster) /
  300 (ambiguous, multiple clusters) / 400 (unknown reporter) / 429 (over 250 cites in one POST)
RATE LIMIT: 60 valid citations/minute; 250 citations/request; 64k char text payload.
  Each lookup also consumes one request from the main user quota (5/min, 50/hr, 125/day default).
  Membership / commercial agreements raise the main quota. One account per project.
COVERAGE: Whatever is in the CL database. Same corpus as search, including F. App'x and recent SCOTUS.
STAR PAGINATION?: NO. Existence/caption only.
UNPUBLISHED DISPOSITIONS?: Resolved if CL has the cluster (C3 is in the corpus).
SUBSEQUENT HISTORY?: None.
CONTROL RESULTS: C1 401 this session (no token in the environment). Not re-probed authenticated.
  Existing portfolio unit tests document the 200/404/300/400 mapping.
  C2–C7: NOT RUN on this endpoint this session (token absent).
LICENSE: Same as CourtListener. Token is free.
FAILURE MODE: 300-ambiguous is the honest multi-disposition signal — if you ignore it and
  take clusters[0], you launder a table-page collision. 404 is clean nothing.
VERDICT: WIRE IN (tier 1) the moment a token exists. This is the primary pin-existence probe.
WHY: The only free API that says "this volume/page is a real cluster" instead of "this string
  appears in some opinion." The 300 status is how you detect table pages.
```

```
SOURCE: CourtListener opinion / cluster / opinions-cited APIs and HTML
URL TESTED: /api/rest/v4/opinions/?id=111730
           /api/rest/v4/clusters/?citation=521%20U.S.%20399
           /api/rest/v4/opinions-cited/?cited_opinion=111730
           /opinion/118137/richardson-v-mcknight/
REACHABLE FROM A SERVER?: YES for the API host; HTML unusable this session
HTTP RESULT: APIs 401 without token. HTML 202, 0 bytes, content-type text/html.
ACCESS: free-with-token (APIs); HTML is theoretically free-no-auth in a browser
API OR URL PATTERN: /opinion/{id}/{slug}/ is not constructible from (reporter, volume, page).
  You get the id from search or citation-lookup first.
RESPONSE FORMAT: JSON / HTML
RATE LIMIT: Main user quota once authenticated.
COVERAGE: Full CL corpus after you have an id.
STAR PAGINATION?: Not demonstrated this session (empty HTML body). Do not assume yes.
UNPUBLISHED DISPOSITIONS?: Same as search.
SUBSEQUENT HISTORY?: opinions-cited is "who cited whom" + depth, not treatment flags.
CONTROL RESULTS: Auth wall. C1–C7 not independently readable from these endpoints this session.
LICENSE: See CourtListener bulk note above.
FAILURE MODE: Treating an empty 202 HTML response as "case missing."
VERDICT: WIRE IN (tier 2) for opinion text and the citation graph AFTER a token is set.
  Do not use the HTML URL as a headless existence probe.
WHY: Detail APIs are the way to pull text and cited-by once you already know the cluster.
```

```
SOURCE: CourtListener RECAP / docket search
URL TESTED: https://www.courtlistener.com/api/rest/v4/search/?q=24-6244&type=d
REACHABLE FROM A SERVER?: YES
HTTP RESULT: 200 JSON, count=31 dockets
ACCESS: free-no-auth for search; PACER fetches via RECAP are a separate paid-PACER-pass-through
API OR URL PATTERN: search only (type=d / type=r / type=rd). Not constructible from a reporter pin.
RESPONSE FORMAT: JSON
RATE LIMIT: Same search API.
COVERAGE: Federal PACER-mirror dockets, incomplete. Not a case-law reporter index.
STAR PAGINATION?: NO
UNPUBLISHED DISPOSITIONS?: Docket ≠ opinion. An unpublished memo may sit on the docket
  without a reporter cite.
SUBSEQUENT HISTORY?: Docket entries (mandate, cert denied) if RECAP has them — not a citator.
CONTROL RESULTS: C6 31 docket hits for "24-6244" — collision, not a unique case.
  C1–C5/C7 not applicable as reporter pins.
LICENSE: RECAP documents are court filings; PACER fee rules still apply to *new* PACER pulls.
FAILURE MODE: Docket-number uniqueness is a myth. 31 rows for one number.
VERDICT: WIRE IN (tier 3) only as a docket corroborator when court_id is known.
WHY: Useful for C6-style problems after you already know the court. Useless as a cite verifier.
```

```
SOURCE: Caselaw Access Project — api.case.law (retired live API)
URL TESTED: https://api.case.law/v1/cases/?cite=521%20U.S.%20399
REACHABLE FROM A SERVER?: YES (host answers)
HTTP RESULT: 200 text/html, redirected to https://case.law/docs/  (goodbye/docs page, not JSON)
ACCESS: n/a — live JSON API is retired
API OR URL PATTERN: Former /v1/cases/?cite=… is dead. Do not call it.
RESPONSE FORMAT: HTML documentation stub (JS site)
RATE LIMIT: n/a
COVERAGE: n/a as an API
STAR PAGINATION?: n/a
UNPUBLISHED DISPOSITIONS?: n/a
SUBSEQUENT HISTORY?: n/a
CONTROL RESULTS: C1 redirected to docs. Not a lookup.
LICENSE: n/a
FAILURE MODE: Wrapper code that still hits api.case.law will parse an HTML "success" as a hit.
VERDICT: DO NOT USE
WHY: Sunset 2024-09-05. Harvard's own notice: search and API moved to CourtListener;
  Harvard still hosts static bulk and per-case HTML at static.case.law / case.law.
```

```
SOURCE: Caselaw Access Project — static.case.law (bulk + per-case HTML)
URL TESTED: https://static.case.law/us/521/CasesMetadata.json
           https://static.case.law/us/521/html/0399-01.html
           https://static.case.law/cal-2d/14/CasesMetadata.json
           https://static.case.law/cal-2d/14/html/0047-01.html
           https://static.case.law/f-appx/239/html/0353-01.html
           https://static.case.law/us/604/CasesMetadata.json
           https://static.case.law/f4th/999/CasesMetadata.json
           https://static.case.law/cal-app-5th/66/CasesMetadata.json
           https://static.case.law/ReportersMetadata.json
REACHABLE FROM A SERVER?: YES
HTTP RESULT: 200 JSON/HTML on in-coverage pins. 404 Cloudflare HTML on missing volumes
  (us/604, f4th/ entire slug, cal-app-5th/66).
ACCESS: free-no-auth
API OR URL PATTERN: CONSTRUCTIBLE
  https://static.case.law/{slug}/{volume}/CasesMetadata.json
  https://static.case.law/{slug}/{volume}/html/{page:04d}-01.html
  Bulk zips/tars per volume from the slug index page.
  Slugs confirmed this session: us, cal-2d, cal-4th, cal-5th, cal-app-4th, cal-app-5th,
  f3d, f-appx. f4th slug does not exist.
RESPONSE FORMAT: JSON metadata; HTML casebody; also zip / pdf / tar per volume
RATE LIMIT: None stated. Large JSON (US 521 metadata was 1.4 MB). Be polite.
COVERAGE: ~6.5–6.7 million official-reporter cases, Harvard bound-volume scan.
  Reporter end years from ReportersMetadata.json this session (not "current year"):
    U.S. 1754–2014 (volumes exist through 521+; 604 does not)
    F.3d 1990–2019 (volumes 1–935)
    F. App'x 1996–2018 (volumes 1–714)
    F.4th — ABSENT
    Cal. 2d 1930–1969
    Cal. 4th 1991–2016
    Cal. 5th — only volume 1 on disk
    Cal. App. 4th through 2016
    Cal. App. 5th 2015–2017 — only volumes 1–11 on disk
  This is the coverage cliff. Cal.2d is present (C4 lives). Cal.App.5th volume 66 is not.
STAR PAGINATION?: YES. Official reporter page breaks are HTML anchors:
  <a id="p354" href="#p354" data-label="354" class="page-label">*354</a>
  Richardson snippet this session:
  <a class="page-label">*400  … *401 … *414 (through the opinion)
  Paul (F. App'x) has the same *354 marker. Goddard casebody has data-firstpage="47"
  data-lastpage="56" and in-text page-block ids.
UNPUBLISHED DISPOSITIONS?: F. App'x is indexed (C3 FOUND). California unpublished
  opinions that never entered the official reports are absent. No "unpublished" label
  beyond the reporter series itself.
SUBSEQUENT HISTORY?: None.
CONTROL RESULTS: C1 FOUND Richardson in us/521 metadata + HTML
  | C2 NOT IN CORPUS (us/604 404)
  | C3 FOUND Paul, 239 F. App'x 353–355, memorandum
  | C4 FOUND Goddard, official cite "14 Cal. 2d 47", decided 1939-07-20
  | C5 no WL index
  | C6 no docket index
  | C7 f4th/999 404 (clean miss) | C7b cal-app-5th/66 404 — clean for the fake page,
    but the *volume* is also outside CAP's Cal.App.5th window, so a *real* 66 Cal.App.5th
    cite would 404 too. Do not treat CAP 404 as NOT_FOUND past the cliff.
LICENSE: case.law/terms (page fetched; body is a JS shell). Harvard's posted term,
  confirmed on the LIL transition note and the terms page title/metadata:
  "Harvard makes the caselaw data and metadata on this site (the \"Caselaw Data\")
  available for public use under the CC0 1.0 Public Domain Dedication."
  Community-norm request (not a legal condition): attribute Harvard / CAP; share
  improvements on the same terms. Site prose is CC BY-SA 4.0; code MIT.
FAILURE MODE: 404 on a post-2014/2017/2018 cite looks like "case does not exist."
  It means "Harvard never scanned that bound volume." Also, -01.html is the first
  case starting on that page; a table page can host more than one disposition
  (additional files -02.html etc. — check metadata first_page collisions).
VERDICT: WIRE IN (tier 1) as corroborator + the only free *pin-confirmation* source
  inside its year window. Offline existence store if you download the metadata.
WHY: Constructible URLs, star pagination, CC0, empty/404 on the invented cite,
  and it still has Cal.2d and F. App'x — the two places people assume free sources stop.
```

```
SOURCE: Google Scholar case law
URL TESTED: https://scholar.google.com/scholar?q=521+U.S.+399+Richardson+McKnight&as_sdt=4%2C33
           https://scholar.google.com/scholar_case?case=16084731491774391602
REACHABLE FROM A SERVER?: NO
HTTP RESULT: 403 HTML "We're sorry... your computer or network may be sending automated queries."
ACCESS: free-no-auth in a consumer browser; blocked from this datacenter
API OR URL PATTERN: search only. scholar_case?case={id} is not constructible from a reporter pin
  (the case= id is Scholar's own).
RESPONSE FORMAT: HTML
RATE LIMIT: Bot wall. Unusable for a headless probe.
COVERAGE: Historically strong on published U.S. + state; "How Cited" is a citator-like view.
STAR PAGINATION?: In a browser, Scholar sometimes shows starred reporter pages. NOT confirmed
  this session (blocked). Treat as unknown / MANUAL-ONLY.
UNPUBLISHED DISPOSITIONS?: Partial in a browser (some F. App'x, some WL). Not tested here.
SUBSEQUENT HISTORY?: "How cited" is a later-cite list with crude signals, not Shepard's.
  Blocked this session.
CONTROL RESULTS: C1–C7 COULD NOT REACH (403 bot wall on every Scholar URL)
LICENSE: Google ToS; scraping is forbidden. Do not store their HTML.
FAILURE MODE: If a residential-IP scraper ever gets through, Scholar's ranking will
  surface a citing case. Same trap as bare CL q=.
VERDICT: MANUAL ONLY
WHY: The "How Cited" view is still worth a human pass. It is not wireable from a server in 2026.
```

```
SOURCE: Justia
URL TESTED: https://supreme.justia.com/cases/federal/us/521/399/
           https://supreme.justia.com/cases/federal/us/604/593/
           https://supreme.justia.com/cases/federal/us/604/23-365/
           https://law.justia.com/cases/california/supreme-court/2d/14/47.html
           https://law.justia.com/cases/federal/appellate-courts/ca4/24-6244/24-6244-2024-08-02.html
REACHABLE FROM A SERVER?: CLOUDFLARE-BLOCKED
HTTP RESULT: 403 "Just a moment..." Cloudflare challenge on every Justia URL
ACCESS: free-no-auth in a browser (MANUAL-ONLY from a server)
API OR URL PATTERN: Partially constructible in a browser:
  supreme.justia.com/cases/federal/us/{vol}/{page}/
  law.justia.com/cases/california/supreme-court/2d/{vol}/{page}.html
  Recent SCOTUS is often /{vol}/{docket}/ not /{vol}/{page}/ — Justia still showed
  "604 U.S. ___" on the docket slug in third-party fetches, not 604 U.S. 593.
RESPONSE FORMAT: HTML
RATE LIMIT: Cloudflare bot fight
COVERAGE: Broad published + some unpublished federal. Not tested from this IP.
STAR PAGINATION?: Unknown this session (blocked). Historically Justia HTML is
  usually unpaginated. Treat pin cites from Justia as SECONDARY until proven otherwise.
UNPUBLISHED DISPOSITIONS?: Browser copies of circuit memos exist (C6 Dennis is a
  Justia URL). Not labeled as a citator.
SUBSEQUENT HISTORY?: None reliable.
CONTROL RESULTS: C1–C7 COULD NOT REACH from this server (403 CF)
LICENSE: Justia ToS; scraping prohibited. Opinion text is still the court's.
FAILURE MODE: Constructible /{vol}/{page}/ for a recent U.S. Reports page can 404
  in a browser while the docket slug works — looks like "case missing."
VERDICT: MANUAL ONLY
WHY: Useful human mirror. Unusable as a datacenter probe in 2026.
```

```
SOURCE: FindLaw (Thomson Reuters)
URL TESTED: https://caselaw.findlaw.com/court/us-supreme-court/521/399.html
           https://caselaw.findlaw.com/us-supreme-court/96-318.html
           https://caselaw.findlaw.com/court/us-supreme-court/23-365.html
REACHABLE FROM A SERVER?: CLOUDFLARE-BLOCKED
HTTP RESULT: 403 "Just a moment..."
ACCESS: free-no-auth in a browser; MANUAL-ONLY from a server
API OR URL PATTERN: search / slug only; not a stable (reporter, volume, page) constructor
RESPONSE FORMAT: HTML
RATE LIMIT: Cloudflare
COVERAGE: Published federal + state, uneven unpublished. Not tested.
STAR PAGINATION?: Not demonstrated. Treat as SECONDARY.
UNPUBLISHED DISPOSITIONS?: Unreliable.
SUBSEQUENT HISTORY?: None (this is not KeyCite, despite the TR ownership).
CONTROL RESULTS: C1–C3/C2 COULD NOT REACH (403 CF)
LICENSE: Thomson Reuters ToS. Do not scrape.
FAILURE MODE: Dead slugs after TR URL reshuffles look like NOT_FOUND.
VERDICT: MANUAL ONLY
WHY: Cloudflare + unstable slugs. Do not wire.
```

```
SOURCE: Casetext
URL TESTED: https://casetext.com/case/richardson-v-mcknight
           https://casetext.com/search?q=521%20U.S.%20399
REACHABLE FROM A SERVER?: YES (host answers)
HTTP RESULT: 410 Gone. Body: "This service is no longer available, but we appreciate
  you being a part of it. For legal research, please visit [Thomson Reuters legal]."
ACCESS: dead
API OR URL PATTERN: n/a
RESPONSE FORMAT: HTML retirement notice
RATE LIMIT: n/a
COVERAGE: n/a
STAR PAGINATION?: n/a
UNPUBLISHED DISPOSITIONS?: n/a
SUBSEQUENT HISTORY?: SmartCite died with the product.
CONTROL RESULTS: C1 410. C2–C7 not separately meaningful.
LICENSE: n/a
FAILURE MODE: Old bookmarks and "Justia/Casetext/Scholar" runbooks still list it.
VERDICT: DO NOT USE
WHY: Acquired by Thomson Reuters August 2023 ($650M). Standalone platform shut
  April 1, 2025. Every path is 410 as of this fetch (2026-09-19). Successor is
  paid CoCounsel / Westlaw — not a free verification source, and an AI research
  tool besides.
```

```
SOURCE: vLex (case-law.vlex.com)
URL TESTED: https://case-law.vlex.com/vid/richardson-v-mcknight-885568545
           https://case-law.vlex.com/search?q=521+U.S.+399
REACHABLE FROM A SERVER?: YES
HTTP RESULT: 200 HTML. The guessed Richardson vid *redirected to a different case*
  (Franchi v. New Hampton, vid 885568545). Search URL is a JS app shell.
ACCESS: paid / library-login. Some county law libraries offer remote shared logins
  (San Francisco Law Library publishes a library-wide vLex login on its public
  databases page — MANUAL / library credential, not a server probe).
API OR URL PATTERN: search only. vid= slugs are not constructible from a reporter pin.
RESPONSE FORMAT: HTML (JS-heavy)
RATE LIMIT: Unknown
COVERAGE: Large commercial corpus after login. Not verified this session.
STAR PAGINATION?: Unknown. Do not claim yes.
UNPUBLISHED DISPOSITIONS?: Commercial, after login.
SUBSEQUENT HISTORY?: vLex has citation analysis in the paid product. Not free, not tested.
CONTROL RESULTS: C1 URL did not return Richardson — it returned a different case. Disqualifying
  as a constructible verifier. C2–C7 not cleanly testable without an account.
LICENSE: Commercial. Do not scrape.
FAILURE MODE: Opaque numeric vids. A guessed URL silently serves the wrong opinion.
  This is exactly how a fabricated cite gets a "found it online" launder.
VERDICT: DO NOT USE as a headless verifier. MANUAL ONLY via a library login.
WHY: Reachable, but the constructible-URL experiment handed back the wrong case.
```

```
SOURCE: Fastcase / vLex Fastcase
URL TESTED: https://fc7.fastcase.com/
           https://web.fastcase.com/
REACHABLE FROM A SERVER?: YES for fc7 (redirects to gateway.fastcase.com/login).
  web.fastcase.com → fetch failed (COULD NOT REACH).
HTTP RESULT: 200 login SPA ("Fastcase Gateway"). No opinion without credentials.
ACCESS: paid, or bar-members-only as a free membership benefit
  (California Lawyers Association vLex Fastcase Premium — closed to non-bar-members),
  or in-person / published-library-login at some county law libraries
  (SF Law Library lists a shared Fastcase remote login on its public databases page).
API OR URL PATTERN: search only after login. No constructible reporter URL.
RESPONSE FORMAT: HTML SPA
RATE LIMIT: n/a unauthenticated
COVERAGE: National primary law after login. Not tested.
STAR PAGINATION?: Unknown. Treat pins as SECONDARY unless you open the reporter view.
UNPUBLISHED DISPOSITIONS?: After login, yes (commercial).
SUBSEQUENT HISTORY?: "Citation analysis" / Bad Law Bot is not Shepard's. Not tested.
CONTROL RESULTS: C1 login wall. C2–C7 not reached.
LICENSE: Commercial / library license.
FAILURE MODE: Bar-association marketing calls it "the same as Westlaw." It is not KeyCite.
VERDICT: MANUAL ONLY (library or CLA membership). DO NOT USE as a server probe.
WHY: Login wall from this IP. CLA access is bar-members-only.
```

```
SOURCE: CaseMine
URL TESTED: https://www.casemine.com/judgement/us/5914b5c2add7b0493475f8c2
           https://www.casemine.com/search/us?q=Richardson+v+McKnight+521
REACHABLE FROM A SERVER?: NO
HTTP RESULT: 403 Forbidden (plain nginx, 118 bytes — not a Cloudflare interstitial)
ACCESS: free-with-account / paid in a browser; blocked here
API OR URL PATTERN: search / opaque judgement ids. Not constructible from a reporter pin.
RESPONSE FORMAT: HTML
RATE LIMIT: Datacenter 403
COVERAGE: Not tested
STAR PAGINATION?: Not tested
UNPUBLISHED DISPOSITIONS?: Not tested
SUBSEQUENT HISTORY?: "Citing cases" in the product; not tested
CONTROL RESULTS: C1 COULD NOT REACH (403)
LICENSE: CaseMine ToS
FAILURE MODE: Unknown (blocked)
VERDICT: DO NOT USE
WHY: Hard 403 from this IP. No constructible pin URL even if it weren't.
```

```
SOURCE: Anystate / AnyLaw
URL TESTED: https://www.anystate.com/
           https://www.anylaw.com/
REACHABLE FROM A SERVER?: YES
HTTP RESULT: anystate.com 200 — a *state news* site, not case law.
  anylaw.com 200 — "AnyLaw - System Upgrade" placeholder (product gone / parked).
ACCESS: n/a
API OR URL PATTERN: n/a
RESPONSE FORMAT: HTML
RATE LIMIT: n/a
COVERAGE: none
STAR PAGINATION?: n/a
UNPUBLISHED DISPOSITIONS?: n/a
SUBSEQUENT HISTORY?: n/a
CONTROL RESULTS: Not a case-law source. Controls not applicable.
LICENSE: n/a
FAILURE MODE: The name still appears on old "free caselaw" lists.
VERDICT: DO NOT USE
WHY: Anystate is news. AnyLaw is a dead upgrade page as of this fetch.
```

```
SOURCE: OpenJurist
URL TESTED: https://openjurist.org/521/us/399
           https://openjurist.org/14/cal2d/47
           https://openjurist.org/604/us/593
           https://openjurist.org/239/f-appx/353
           https://openjurist.org/  (homepage)
REACHABLE FROM A SERVER?: Homepage 200. Case URLs CLOUDFLARE-BLOCKED (403 "Just a moment...").
HTTP RESULT: Constructible case paths 403 CF. Home 200 JS/Nuxt shell.
ACCESS: free-no-auth in a browser; MANUAL-ONLY from a server
API OR URL PATTERN: CONSTRUCTIBLE in principle: /{vol}/{reporter-slug}/{page}
RESPONSE FORMAT: HTML
RATE LIMIT: Cloudflare on the URLs that matter
COVERAGE: Mostly older federal. C2 604/593 would be the cliff test — blocked.
STAR PAGINATION?: Historically yes on some pages (reporter scan). Not confirmed this session.
UNPUBLISHED DISPOSITIONS?: F. App'x path exists in the URL scheme; blocked here.
SUBSEQUENT HISTORY?: None
CONTROL RESULTS: C1/C2/C3/C4 case URLs COULD NOT REACH (403 CF)
LICENSE: Site terms; text is court opinions. Do not scrape the CF wall.
FAILURE MODE: A 200 homepage plus a constructible pattern will tempt a wire-in.
  The actual opinion paths are what Cloudflare blocks.
VERDICT: MANUAL ONLY
WHY: The one attractive constructible URL scheme is the one that 403s from a datacenter.
```

```
SOURCE: Cornell LII
URL TESTED: https://www.law.cornell.edu/supct/html/96-318.ZO.html
           https://www.law.cornell.edu/supremecourt/text/521/399
           https://www.law.cornell.edu/supremecourt/text/23-365
REACHABLE FROM A SERVER?: YES
HTTP RESULT: 200 HTML on all three. C1 and C2 returned the opinion text (caption match).
ACCESS: free-no-auth
API OR URL PATTERN: /supremecourt/text/{vol}/{page} works for C1.
  C2 is /supremecourt/text/23-365 (docket), not /604/593.
  Older /supct/html/{docket}.ZO.html still works for C1 (96-318).
  Not a general federal/state constructor. SCOTUS-only for practical purposes.
RESPONSE FORMAT: HTML
RATE LIMIT: None observed
COVERAGE: U.S. Supreme Court. Not F. App'x, not Cal.2d, not WL, not circuit dockets.
STAR PAGINATION?: NO on the two C1 HTML bodies inspected this session
  (no *400, no id="p400", no page-label). C2 is the slip/syllabus HTML, "604 U.S. ___".
  Pins from LII are SECONDARY.
UNPUBLISHED DISPOSITIONS?: No
SUBSEQUENT HISTORY?: No
CONTROL RESULTS: C1 FOUND Richardson | C2 FOUND by docket 23-365, slip pagination only
  | C3 not in scope | C4 not in scope | C5 not in scope | C6 not in scope
  | C7 not in scope (no 999 F.4th page)
LICENSE: LII site compilation is Cornell's; the opinion is a government work.
  Do not copy their editorial apparatus into a filing as if it were the U.S. Reports.
FAILURE MODE: /supremecourt/text/604/593 is not what they used for Horn.
  A constructible (vol, page) for OT 2024 will 404 while the docket slug works.
VERDICT: WIRE IN (tier 3) as a SCOTUS-only text mirror. Not a pin confirmer.
WHY: Datacenter-reachable HTML for C1/C2, empty on the invented federal cite
  because the URL space is SCOTUS-only. No star pages.
```

```
SOURCE: govinfo.gov — US Reports PDFs + USCOURTS collection + API
URL TESTED: https://www.govinfo.gov/content/pkg/USREPORTS-521/pdf/USREPORTS-521-399.pdf
           https://api.govinfo.gov/collections?offset=0&pageSize=20
           https://www.govinfo.gov/app/collection/uscourts
           https://www.govinfo.gov/app/search/{urlencoded q}
           https://www.govinfo.gov/api-signup
           https://www.govinfo.gov/help/uscourts
REACHABLE FROM A SERVER?: YES for content PDFs and help HTML.
  Search/collection *app* URLs are JS shells (200, ~1.7 KB, no results).
  API collections 401 without an api_key.
ACCESS: PDFs free-no-auth. API free-with-token (register at /api-signup, no fee).
API OR URL PATTERN:
  US Reports PDF (CONSTRUCTIBLE): /content/pkg/USREPORTS-{vol}/pdf/USREPORTS-{vol}-{page}.pdf
    C1 returned application/pdf, 253 KB — a real document, not a volume dump.
  USCOURTS opinion PDF: /content/pkg/USCOURTS-{court}_{case}/pdf/USCOURTS-{court}_{case}-{n}.pdf
    Needs court code + case number, not a reporter pin.
  API: https://api.govinfo.gov/…?api_key=  (JSON)
RESPONSE FORMAT: PDF / JSON (API) / empty HTML SPA (browse)
RATE LIMIT: API key required; published per-key limits on the signup page (not scraped as a number here).
COVERAGE:
  US Reports official pagination — historical volumes. C1 yes. C2 volume 604 is a
  preliminary print on supremecourt.gov, not yet a govinfo USREPORTS-604 package this session.
  USCOURTS: "selected" appellate, district, bankruptcy, plus some national courts,
  generally 2004–present, incomplete even inside that window (help page fetched 2026-09-19,
  last-updated 2024-12-03). Not a substitute for F.3d / F. App'x.
STAR PAGINATION?: The USREPORTS PDF *is* the official pagination. That is pin-confirmation
  for U.S. Reports, not a star in HTML. USCOURTS PDFs are slip pagination.
UNPUBLISHED DISPOSITIONS?: Only if that court sent that memo to GPO. Not labeled as F. App'x.
SUBSEQUENT HISTORY?: None
CONTROL RESULTS: C1 FOUND official U.S. Reports PDF | C2 not on this USREPORTS URL scheme yet
  | C3 not constructible | C4 out of scope | C5 out of scope
  | C6 possible via USCOURTS casenumber if that court participates — not fetched as a PDF
  | C7 would 404 on a fake USREPORTS volume (not fetched; no 999 U.S.)
LICENSE: U.S. government works. GPO authenticates USCOURTS files with digital signatures.
  Quote from the help page: "The secure transfer of files to GPO from the AOUSC maintains
  the chain of custody, allowing GPO to authenticate the files with digital signatures."
FAILURE MODE: The /app/search SPA returns 200 with no results to a headless client —
  looks like "govinfo has nothing" when you simply didn't run the API.
  USCOURTS is opt-in by court; absence ≠ nonexistence.
VERDICT: WIRE IN (tier 2) for official U.S. Reports PDF pins (C1-style).
  WIRE IN (tier 3) USCOURTS API after you register a free key, never as a reporter oracle.
WHY: C1 PDF is the bound-volume page. C2 still lives on supremecourt.gov, not govinfo.
```

```
SOURCE: supremecourt.gov (slip opinions, preliminary prints, bound volumes, slip list)
URL TESTED: https://www.supremecourt.gov/opinions/24pdf/23-365_6k47.pdf
           https://www.supremecourt.gov/opinions/24pdf/604us2r23_3e04.pdf
           https://www.supremecourt.gov/opinions/boundvolumes/521bv.pdf
           https://www.supremecourt.gov/opinions/slipopinion/24
REACHABLE FROM A SERVER?: YES
HTTP RESULT: 200 PDF on all three opinion files (slip 306 KB, prelim 411 KB, bound vol 5.3 MB).
  Slip list 200 HTML and names C2 as 604 U.S. 593.
ACCESS: free-no-auth
API OR URL PATTERN: Slip: /opinions/{term}pdf/{docket}_{hash}.pdf — NOT constructible
  from (reporter, volume, page); the hash is opaque.
  Preliminary print: /opinions/{term}pdf/{vol}us{part}r{n}_{hash}.pdf — also opaque.
  Bound volume: /opinions/boundvolumes/{vol}bv.pdf — constructible by volume, not page.
  Slip list HTML: /opinions/slipopinion/{yy}  (yy = OT year, "24" = OT 2024)
RESPONSE FORMAT: PDF / HTML
RATE LIMIT: None observed
COVERAGE: U.S. Supreme Court only. Slips stay posted until replaced by the prelim-style
  file; the slip list says slips remain "until replaced with opinions edited to reflect
  the usual publication style of the United States Reports, including final pagination
  that will carry forward unchanged in the corresponding preliminary prints and the
  bound volumes."
  Practical lag observed on C2 (decided 2025-04-02): by 2026-09-19 the Court has already
  issued the Volume 604 Part 2 preliminary print with pages 593–649. Bound 604 is still
  pending. That is on the order of months for prelim pagination, years for the bound book.
STAR PAGINATION?: The preliminary print and bound PDFs *are* official U.S. Reports pages.
  The slip PDF is slip pages ("Cite as: 604 U. S. ____ (2025)").
UNPUBLISHED DISPOSITIONS?: n/a (SCOTUS merits opinions)
SUBSEQUENT HISTORY?: None on the opinion page
CONTROL RESULTS: C1 bound volume PDF 200 | C2 slip + prelim + slip-list all 200, prelim
  carries 604 U.S. 593 | C3–C7 out of scope
LICENSE: Official Court work product. Public.
FAILURE MODE: Citing the slip page after the prelim has issued. Using the opaque PDF
  filename as if it were a reporter pin.
VERDICT: WIRE IN (tier 1) for current-Term SCOTUS pagination.
  MANUAL/list scrape of /opinions/slipopinion/{yy} to map docket → official cite.
WHY: This is the only free place that currently prints 604 U.S. 593 as official pages.
  CAP does not have volume 604. Several mirrors still say 604 U.S. ___.
```

```
SOURCE: Ninth Circuit CDN + opinions page
URL TESTED: https://cdn.ca9.uscourts.gov/datastore/opinions/
           https://cdn.ca9.uscourts.gov/datastore/memoranda/
           https://www.ca9.uscourts.gov/opinions/  → 200, redirected to /decisions/opinions/
           https://cdn.ca9.uscourts.gov/datastore/opinions/2025/09/29/24-6244.pdf
REACHABLE FROM A SERVER?: YES
HTTP RESULT: Directory indexes 200 with 0-byte body (no listing).
  Dated PDF 200 (C6 *collision* case, 9th Cir. Esche, ~278 KB).
  HTML search page 200.
ACCESS: free-no-auth
API OR URL PATTERN: Published:
  https://cdn.ca9.uscourts.gov/datastore/opinions/{YYYY}/{MM}/{DD}/{docket}.pdf
  Memoranda (unpublished):
  https://cdn.ca9.uscourts.gov/datastore/memoranda/{YYYY}/{MM}/{DD}/{docket}.pdf
  NOT constructible from (reporter, volume, page). Needs docket + date.
  Documents on the CDN appear to remain posted (the 2025-09-29 file is still there).
  The HTML search UI is not an API.
RESPONSE FORMAT: PDF / HTML
RATE LIMIT: None observed
COVERAGE: 9th Cir. published opinions + unpublished memoranda the court posts.
  Not F. App'x pagination. Pre-web-era dispositions are absent.
STAR PAGINATION?: NO. Slip PDF pagination. Pins to F.3d / F. App'x from these files
  are SECONDARY unless you also have CAP/West pages.
UNPUBLISHED DISPOSITIONS?: Yes, under /memoranda/. The PDF banner and 9th Cir. R. 36-3
  language is the label. FRAP 32.1 allows citation of post-2006-12-01 unpublished
  federal dispositions; 9th Cir. R. 36-3 still says they are not precedent.
SUBSEQUENT HISTORY?: No
CONTROL RESULTS: C3 not constructible without a date (Paul is 2007; CDN path not guessed).
  C6 constructed path for 24-6244 returned the *9th Cir.* opinion, which is a real file
  and the wrong case for the 4th Cir. control. That is a feature of the collision, not a CDN bug.
  C7 no such docket fetched.
LICENSE: Court-issued. Public.
FAILURE MODE: Docket number + "9th Cir. CDN" without a date/court check.
VERDICT: WIRE IN (tier 2) for 9th Cir. slip/memo PDFs once you have docket+date.
WHY: Headless 200 PDF. No reporter pages. Essential for unpublished 9th Cir. text.
```

```
SOURCE: Fourth Circuit opinions (added because C6 lives here)
URL TESTED: https://www.ca4.uscourts.gov/opinions/246244.u.pdf
           https://www.ca4.uscourts.gov/opinions/
REACHABLE FROM A SERVER?: YES
HTTP RESULT: 200 application/pdf, 106 KB. Search page 200 HTML.
ACCESS: free-no-auth
API OR URL PATTERN: CONSTRUCTIBLE from docket:
  https://www.ca4.uscourts.gov/opinions/{docket_no_hyphens}.u.pdf  (unpublished)
  Published uses a different suffix (not fully mapped this session).
RESPONSE FORMAT: PDF / HTML
RATE LIMIT: None observed
COVERAGE: 4th Cir. The C6 target *Dennis v. Evans* is this file.
STAR PAGINATION?: NO (2-page unpublished per curiam, slip pages)
UNPUBLISHED DISPOSITIONS?: Yes. Filename .u.pdf and the banner "UNPUBLISHED" /
  "Unpublished opinions are not binding precedent in this circuit."
SUBSEQUENT HISTORY?: No
CONTROL RESULTS: C6 FOUND Dennis v. Evans, No. 24-6244, decided Aug. 2, 2024
  | others out of scope
LICENSE: Court-issued. Public.
FAILURE MODE: Same docket number on ca9 CDN is a different case.
VERDICT: WIRE IN (tier 2) for 4th Cir. unpublished PDFs by docket.
WHY: Rare constructible *docket → PDF* pattern that actually worked from this IP.
```

```
SOURCE: California courts — courts.ca.gov opinion archive + appellate case info
URL TESTED: https://www.courts.ca.gov/opinions.htm → 200, landed on https://courts.ca.gov/opinions
           https://www.courts.ca.gov/opinions-slip.htm → 200, published/citable page
           https://www.courts.ca.gov/opinions/unpublishednon-citable-opinions
           https://appellatecases.courtinfo.ca.gov/  (case info; HTML search form)
REACHABLE FROM A SERVER?: YES for the HTML pages. The actual opinion PDFs are linked
  as /opinions/documents/{docket}.PDF (see CL's Boyd v. Freeman download_url).
ACCESS: free-no-auth
API OR URL PATTERN: Not constructible from (Cal.2d volume, page).
  Recent published: courts.ca.gov opinions pages + /opinions/documents/{docket}.PDF
  Unpublished last 60 days: a pull-down list on the unpublished page.
  After 60 days: California Appellate Courts Case Information System
  (search by case number / caption / party). That system is a form, not an API.
  Goddard (1939) is not on the living opinions site.
RESPONSE FORMAT: HTML / PDF
RATE LIMIT: None observed
COVERAGE: Living site = recent CA Supreme Court and Court of Appeal.
  Official-reporter archive for 1939 is CAP / bound Cal.2d, not this site.
STAR PAGINATION?: NO on slip PDFs. Official Cal. / Cal.App. pagination is in the
  bound Official Reports (CAP has the scans through the cliff).
UNPUBLISHED DISPOSITIONS?: Labeled. Rule 8.1115: unpublished CA Court of Appeal /
  appellate-division opinions "must not be cited or relied on" except as the rule
  allows. The site says unpublished opinions from the last 60 days are listed as
  public information; after 60 days they remain in Case Information Search.
  They are not removed from existence; they are removed from the 60-day list.
SUBSEQUENT HISTORY?: Review-granted / depublished is a Supreme Court order, not a
  field on the slip PDF. Rule 8.1115(e): grant of review no longer auto-depublishes
  (post-2016); the COA opinion stays published and citable for potentially persuasive
  value unless the Supreme Court orders otherwise. Rule 8.1125 is the depublication
  request path. Programmatic detection: you must watch the Supreme Court's
  publication/depublication orders and the Official Reports status — no free API
  this session exposed a "depublished=true" flag. Free sources silently omit this.
CONTROL RESULTS: C4 page is the current published list, not Goddard.
  C7b will never appear (fabricated). A real 66 Cal.App.5th case would be on
  Case Information / Official Reports, not necessarily on the 60-day list.
LICENSE: Court-issued. Public.
FAILURE MODE: Treating "not on the 60-day unpublished list" as "does not exist."
  Treating a Cal.App.5th cite as citable without checking publication status.
  Free opinion sites will show unpublished text without an 8.1115 banner.
VERDICT: WIRE IN (tier 2) for recent CA slip PDFs and the 60-day unpublished list.
  MANUAL for depublication / review-granted status.
WHY: Reachable, labeled unpublished, but not a reporter-pin constructor and not a citator.
```

```
SOURCE: Oyez
URL TESTED: https://www.oyez.org/cases/2024/23-365
REACHABLE FROM A SERVER?: YES (200)
HTTP RESULT: 200 JS/Angular shell, {{meta.fullTitle}} placeholders — no opinion text
  without JavaScript.
ACCESS: free-no-auth in a browser
API OR URL PATTERN: /cases/{term}/{docket} — SCOTUS only, docket not reporter
RESPONSE FORMAT: HTML SPA
RATE LIMIT: n/a
COVERAGE: SCOTUS multimedia / summaries
STAR PAGINATION?: NO
UNPUBLISHED DISPOSITIONS?: n/a
SUBSEQUENT HISTORY?: No
CONTROL RESULTS: C2 200 empty-to-a-headless-client
LICENSE: Oyez / Chicago-Kent. Not a primary-source license for U.S. Reports pages.
FAILURE MODE: 200 with no case data looks like a hit in a naive scraper.
VERDICT: DO NOT USE as a verifier. MANUAL ONLY for argument audio.
WHY: JS-required. Wrong job.
```

```
SOURCE: Library of Congress U.S. Reports scan
URL TESTED: https://tile.loc.gov/storage-services/service/ll/usrep/usrep521/usrep521399/usrep521399.pdf
REACHABLE FROM A SERVER?: YES
HTTP RESULT: 200 application/pdf, 749 KB
ACCESS: free-no-auth
API OR URL PATTERN: CONSTRUCTIBLE
  …/service/ll/usrep/usrep{vol}/usrep{vol}{page}/usrep{vol}{page}.pdf
  (page is zero-padded to 3+ digits in this pattern; C1 used 399)
RESPONSE FORMAT: PDF (official U.S. Reports page images)
RATE LIMIT: None observed
COVERAGE: Historical U.S. Reports. C1 yes. C2 volume 604 not expected.
STAR PAGINATION?: The PDF pages *are* the official pagination.
UNPUBLISHED DISPOSITIONS?: No
SUBSEQUENT HISTORY?: No
CONTROL RESULTS: C1 FOUND official volume/page PDF | C2 not in this historical set
LICENSE: Government work / LOC scan. Public.
FAILURE MODE: Pattern is volume-specific; do not invent a 604 path and treat 404 as
  "Horn does not exist."
VERDICT: WIRE IN (tier 2) as a second official-PDF pin confirmer for old U.S. Reports.
WHY: Constructible, datacenter-reachable, official pages. Complements govinfo.
```

---

## Priority 2 — pin cites and star pagination

**2A. Free sources that actually embed reporter page breaks (fetched this session)**

- **CAP static HTML — YES.** Real snippet from `https://static.case.law/us/521/html/0399-01.html`:

  `<a class="page-label">*400`

  and from Paul, `https://static.case.law/f-appx/239/html/0353-01.html`:

  `<a id="p354" href="#p354" data-label="354" data-citation-index="1" class="page-label">*354</a>`

  Also `data-firstpage` / `data-lastpage` on `<section class="casebody">`.

- **Official U.S. Reports PDFs — YES (the pages themselves).**
  govinfo `USREPORTS-521-399.pdf`, LOC `usrep521399.pdf`, SCOTUS bound `521bv.pdf`,
  SCOTUS prelim `604us2r23_3e04.pdf` (pages 593–649).

**2B. Sources without star pagination (pins from these are SECONDARY)**

CourtListener search JSON and (this session) opinion HTML; Google Scholar (blocked, not demonstrated); Justia / FindLaw / OpenJurist (blocked); Cornell LII HTML for Richardson (no `*400` / `p400`); circuit slip PDFs (CA9 CDN, CA4 `.u.pdf`); courts.ca.gov slips; Oyez; vLex/Fastcase unauthenticated; any AI chatbot.

**2C. When official reporter pagination is not free**

Accepted fallback, in order of honesty:

1. **Vendor-neutral / public-domain cite + paragraph number**, where the court adopted one.
   Typical form: `2024 N.H. 1, ¶ 12`. Jurisdictions that have implemented some form of
   this (formats differ; this is not a Bluebook recitation): Oklahoma, New Mexico,
   Wisconsin, North Dakota, Colorado, Maine, Montana, New Hampshire (neutral form
   added 2024-01-01), South Dakota, Utah, Vermont, Wyoming, plus different schemes in
   Illinois, Louisiana, Mississippi, Ohio, Arkansas. North Carolina adopted and did
   not keep it. **California has not adopted this.** CRC 1.200 still points at the
   California Style Manual or the Bluebook and the Official Reports.
2. **Court-assigned docket + full date + slip page** (FRAP 32.1 unpublished; CA9 memo PDF).
3. **Say in the brief that the pin is to the slip/public-domain copy and is SECONDARY.**

There is no free, complete map from F.3d page 753 back to a paragraph number.
You confirm 753 only if you can see a `*753` or an official PDF page 753.

**2D. Current U.S. Supreme Court Term pagination**

1. Day of decision: slip PDF on `/opinions/slipopinion/{yy}` — cite `604 U.S. ___`.
2. Months later: Reporter of Decisions posts a **preliminary print** PDF with the
   volume/page that will carry into the bound book. C2 already has this
   (`604 U.S. 593`, Volume 604 Part 2, pages 593–649), fetched this session from
   supremecourt.gov. The slip list HTML already prints `604 U.S. 593`.
3. Bound volume: `/opinions/boundvolumes/{vol}bv.pdf` and later LOC/govinfo scans.
   Lag from decision to bound book is still measured in years. Lag from decision to
   *usable official page numbers* is the prelim, which for Horn was posted well
   before this 2026-09-19 survey (decision 2025-04-02).

Do not wait for CAP. CAP's U.S. series ends 2014.

---

## Priority 3 — subsequent history and negative treatment

**3A. Free citator-like tools**

- **CourtListener citation network** (`/opinions-cited/`, plus search `citeCount`, plus quarterly Citations Map bulk CSV): "who cited whom" and a depth count. 401 without a token this session. This is **not** Shepard's. It will not tell you reversed / overruled / vacated / distinguished / criticized. A high citeCount on a reversed case looks like vitality.
- **Google Scholar "How Cited":** MANUAL-ONLY, 403 from this IP. Human-usable later-cite list with crude signals. Still not a treatment citator.
- **vLex / Fastcase citation analysis / Bad Law Bot:** login / bar / library. Not tested. Not Shepard's.
- **No free Shepard's or KeyCite API exists.**

**3B. California unpublished / depublished / review granted**

- CRC **8.1115**: unpublished CA Court of Appeal / appellate-division opinions are not citable except as the rule allows.
- Detection from the citation alone: a *Cal. App. 5th* / *Cal. 5th* official cite is (was) published. An unpublished disposition is typically `2024 WL …` or `No. B######` with no Cal.App. cite, or a courts.ca.gov unpublished PDF.
- **Depublication** is a Supreme Court order (CRC 8.1125). It will not reliably appear as a flag on CAP, CL, Justia, or Scholar. CAP will still serve the scanned Official Reports pages.
- **Grant of review** no longer auto-depublishes (8.1115(e), post-2016). The COA opinion stays published unless the Court says otherwise. Transfer-with-directions-to-vacate can depublish or render "not citable" depending on whether the bound volume has shipped (comment to 8.1115, post-2021).
- Programmatic truth: scrape / watch the Supreme Court's publication and depublication orders, or look it up on Westlaw/Lexis at a library. Free opinion HTML **silently omits** this.

**3C. Federal unpublished — FRAP 32.1**

- FRAP 32.1: a court may not forbid citation of unpublished federal opinions issued **on or after 2007-01-01** (rule effective 2006-12-01). Local rules may still say they are not precedent (9th Cir. R. 36-3; 4th Cir. banner on C6).
- From the citation alone:
  - `F.3d` / `F.4th` → published.
  - `F. App'x` → unpublished (West's Federal Appendix).
  - `2024 WL …` or `No. 24-6244` with no F.3d/F.4th → unpublished unless you find a reporter pin.
- Reliable labels this session: CAP F. App'x series; CA4 `.u.pdf` + "UNPUBLISHED" banner; CA9 `/memoranda/` + R. 36-3 footer; courts.ca.gov "Unpublished/Non-Citable" page. CL `status=Published` is **not** reliable for this distinction.

**3D. Free negative-treatment flags**

**No free flag from a server.** CourtListener's graph is a reading list, not a treatment flag.

**As of 2026-09-19 Plaintiff has KeyCite in a browser** via Westlaw Patron Access for Pro Se. That is the workaround: open the case, read Negative Treatment / History / Citing References (or search `kc {cite}`). Still not something a script can call.

---

## Priority 4 — free access to the paid citators

In-person findings below were fetched from the libraries' own pages this session unless marked otherwise. Hours move; call before a trip.

**4A. California county law libraries (Northern / Central priority)**

These are **public** law libraries. You do not need to be a lawyer. You usually need a **free library card** (issued in person) to log into the research computers.

| Library | What they actually offer | Hours (as posted 2026-09-19) | Appointment? | Print / email |
|---|---|---|---|---|
| **Alameda County Law Library**, 125 12th St, Oakland | **Westlaw** (50-state + federal + KeyCite + Rutter/Witkin) and **Lexis Advance** (incl. **Shepard's**) on research computers. Bloomberg Law on one dedicated terminal (card; some download features disabled). CEB OnLaw, HeinOnline, NCLC, Gale forms, Nolo remote. Lexis Digital Library ebooks remote with card. | Mon–Fri 9:00–4:00; doors lock 15 min early | No appointment stated for computers. Card required. Research computers up to 3 hours/day (2 hours Bloomberg). | Email, USB, or print **$0.25/page** |
| **San Francisco Law Library**, 1145 Market St, 4th Fl | **Westlaw** and **Lexis+** (unreported cases, Shepard's) on library computers. Bloomberg, CEB, Hein, Trellis, VitalLaw on site. **Remote Fastcase and remote vLex** via library-published shared logins on the public databases page. Lexis Digital Library + Nolo remote. | Mon–Fri 9:00–5:00 | No appointment stated | Printers/scanners on site; citator products are the on-site terminals |
| **Sacramento County Public Law Library**, 609 9th St | **Lexis+ with Shepard's**, CEB OnLaw, HeinOnline, Trellis, Matthew Bender digital, NCLC. (Westlaw was **not** listed on the databases page fetched this session — Lexis/Shepard's is the citator they advertise.) 12 public legal-research PCs, no time limit; wifi; librarians will not give legal advice. | Mon–Fri 9:00–5:00 | No appointment for terminals | Publisher licenses block most remote use |
| **Santa Clara County Law Library**, 360 N First St, San Jose | **WestlawNext** (KeyCite; email/download limited) and **Lexis Advance** (Shepard's; email/download/print allowed) **terminals only**. | Mon–Fri 9:00–5:00 (page fetched via search) | Not stated | Westlaw download restricted; Lexis more permissive |
| **Fresno County Law Library** | **WestlawNext + KeyCite** on site. CEB OnLaw, HeinOnline, Nolo. **Cannot save** from library computers; **print $0.15/page only**. | Confirm before travel (databases page fetched; hours not on that page) | Not stated | Print only; no save |
| **Witkin State Law Library** (California State Library), 914 Capitol Mall, Sacramento | **Westlaw on-site only.** CEB OnLaw on-site. HeinOnline remote for people who qualify for a State Library card (state employees / certain officials — **not a general public remote Westlaw grant**). Public may use reading-room terminals. | Mon–Fri 9:30–4:30 | Walk-in reading room | On-site |

**Remote Westlaw Patron Access for Pro Se — now in Plaintiff's hands (2026-09-19).** Screenshots reached the live `next.westlaw.com` home after the Thomson Reuters click-wrap on `ess.thomsonreuters.com`. This is the library remote pilot (Riverside and San Diego publish it; enter through that library's link, not a bare Westlaw URL). Shared seats (often 2). Sign Off when done. Personal pro se use only. **Do not put the OnePass in chat or in the pipeline.** Contra Costa, San Joaquin, Stanislaus, San Mateo, Marin, Solano, Yolo, Placer, Kern, Monterey, Butte still follow the on-site Westlaw/Lexis pattern unless they join the same pilot.

**4B. Federal courthouse public terminals and court libraries**

- **ND Cal clerk's offices** (San Francisco, Oakland, San Jose): public PACER terminals during clerk hours — docket lookup / print. This is **PACER, not Westlaw**.
- **ND Cal court library** (Phillip Burton, 18th Floor, 415-436-8130): **limited public access; open to members of the bar admitted in ND Cal.** That is **bar-members-only** for the typical visitor. Appointment culture; staffing shortages.
- **ED Cal Anthony M. Kennedy Library**, Matsui Courthouse, 501 I St, Suite I-400, Sacramento, 916-930-4155: **by appointment**, open to members of the bar **and pro se litigants with an active Eastern District of California case** (Local Rule 120). Not a walk-in Westlaw lab for the general public.
- **ED Cal Fresno** (Coyle Courthouse, 2500 Tulare, Suite 2401, 559-499-5615): court library exists; confirm current public/pro se rules before travel.
- **PACER fees:** courthouse public terminals are the place a pro se litigant views and prints docket PDFs without running a personal PACER meter. They do not replace KeyCite.

**4C. Remote programs open to non-lawyers vs bar-only**

| Program | Open to a pro se non-lawyer? |
|---|---|
| County law library **on-site** Westlaw / Lexis / Shepard's / KeyCite | **Yes**, with a free library card |
| SF Law Library **remote Fastcase / vLex** (shared library login on the public page) | **Yes** (library credential, not a personal research account) |
| Alameda / SF **Lexis Digital Library ebooks** remote | **Yes**, with that library's card. Follow-links into live Lexis usually still need the paid/on-site session. |
| California Lawyers Association **vLex Fastcase Premium** | **No — bar / CLA members only** |
| Fastcase as a state-bar member benefit generally | **No — bar members only** |
| California State Library remote databases | **Mostly state employees / officials.** Westlaw is on-site only. |
| University / law-school Westlaw or Lexis | **Closed to the public** (student/faculty licenses) |
| **Westlaw Patron Access for Pro Se** (library remote pilot; OnePass) | **Yes — Plaintiff has this as of 2026-09-19.** Personal non-commercial use. Not a server source. |
| LII / CourtListener / CAP | Yes, already free; not a citator |
| PACER fee exemption | Separate application; not a citator |

---

## Priority 5 — bulk data, licenses, parsers

**5A. Bulk downloads that let you answer "does this cite exist?" offline**

| Source | What | Format | Cadence / size | URL pattern |
|---|---|---|---|---|
| **CAP static.case.law** | Per-reporter, per-volume CasesMetadata.json + HTML + zip/tar/PDF | JSON + HTML + archives | Static snapshot; not updated past the end-year cliff | `https://static.case.law/{slug}/{vol}/CasesMetadata.json` and the volume index |
| **CourtListener bulk** | Courts, dockets, opinion clusters, opinions (full text), **Citations Map**, parentheticals, judges | PostgreSQL `COPY` CSV, UTF-8, header row. Snapshots, not deltas. | Quarterly (last day of Mar/Jun/Sep/Dec, 03:00 PT) | Browse via the bulk-data page; files stream to `s3://com-courtlistener-storage/` (this session `https://storage.courtlistener.com/` listed the bucket). Schema SQL dumped alongside. |
| **CL embeddings** | Semantic-search vectors | ~2 TB | Nightly inventory | `aws s3 sync s3://com-courtlistener-storage/embeddings/opinions/ . --no-sign-request` (FLP notes ~$200 egress cost to them) |
| **Hugging Face `free-law/Caselaw_Access_Project`** | CAP-derived | Parquet / dataset | Mirror of the CAP dump | Hosted dataset; accept conditions. Not fetched byte-for-byte this session. |
| **LOC / govinfo US Reports** | Official page-image PDFs | PDF | Historical | Constructible paths above |

Practical offline existence store: download CAP `CasesMetadata.json` for the reporters you cite (small enough to keep) **plus** a periodic CL citations/clusters CSV if you have the disk. CAP alone will false-negative everything after ~2014–2018.

**5B. License terms (quoted, not summarized)**

- **CAP** (Harvard, terms page / LIL announcement): *"Harvard makes the caselaw data and metadata on this site (the \"Caselaw Data\") available for public use under the CC0 1.0 Public Domain Dedication."* CC0 waives copyright to the extent Harvard can. Harvard *"makes no representations or warranties of any kind concerning the status of any data included in the Caselaw Data that is generated by third parties."* Community norms request attribution and share-alike; those are requests, not the license.
- **CourtListener bulk** (help page fetched this session): *"Our bulk data files are free of known copyright restrictions."*
- **U.S. Reports / slip opinions / circuit PDFs:** court-issued government works. Quoting them in a filing is what the documents are for.
- **Google / Justia / vLex / Fastcase HTML:** their *website* ToS forbids scraping and redistribution of *their* compilation. The underlying opinion is still the court's. Do not warehouse their HTML.
- **Filing a brief:** you may quote the opinion. You may not paste a vendor headnote as if the court wrote it.

**5C. Citation parsers (maintenance as of this session)**

| Library | Status | F. App'x | Cal.2d–Cal.5th / Cal.App. | Bare WL |
|---|---|---|---|---|
| **eyecite** (Free Law Project, Python) | **Maintained.** PyPI **v2.7.8**, 2026-07-01. Requires `reporters-db>=3.2.53`, Python ≥3.10. Powers CL's own extractor. | Yes (reporters-db edition `F. App'x` / `Fed. Appx.`) | Yes (Cal. 2d / 3d / 4th / 5th, Cal. App. series). Compact/OCR variants still produce edge misses (FLP issue #304: spaced abbreviations). | Extracts proprietary `WL` strings as citations; **does not resolve them to a case.** |
| **reporters-db** | **Maintained** (eyecite's dependency). Nearly every American reporter abbreviation. | Yes | Yes | WL is a database cite, not a reporter edition |
| **eyecite-ts** (community TS port) | Active 2026 releases (v0.21.6–v0.27.0 in May 2026) adding `FedAppx` / `Cal.2d` normalization. Not the FLP canonical. | Yes (recently fixed) | Yes (recently fixed) | Same limit as eyecite |
| **courts-db** | Maintained alongside eyecite | n/a (courts, not reporters) | n/a | n/a |

eyecite's job is **normalize "975 F. 3d 742" → (F.3d, 975, 742)**. It will happily parse `999 F.4th 1` and `2016 WL 4761808` into well-formed objects. **Parsing is not verification.** C7 is why.

---

## Priority 6 — failure modes

**6A. Confident wrong answers (the brief-killing ones)**

1. **CourtListener bare `q=` full-text** — C4 `q="14 Cal.2d 47"` returned **81 opinions**, first hit *Boyd v. Freeman* (2017). A pipeline that takes `results[0].caseName` will file the wrong case.
2. **CourtListener `citation=` / unquoted citation parameter** — same trap; first hit on `citation=14 Cal. 2d 47` was *Angell v. Peterson Tractor*.
3. **CourtListener docket search without `court_id`** — C6 `24-6244` → 31 dockets / the 9th Cir. Esche opinion, not the 4th Cir. Dennis memo.
4. **vLex guessed `vid` URL** — 200 OK, **wrong opinion** (Franchi, not Richardson).
5. **Oyez / govinfo /app/search / Fastcase gateway / CAP api.case.law** — HTTP 200 with an empty or goodbye page. A status-code-only checker records FOUND.
6. **CAP `html/{page}-01.html` on a table page** — first disposition on that page, not necessarily yours. Check `CasesMetadata.json` for multiple objects with the same `first_page`.
7. **CAP 404 past the cliff** — looks like NOT_FOUND for a real 2020 Cal.App.5th or any F.4th.
8. **CL `status=Published`** — not the same as "published in F.3d."
9. **Justia / Scholar "did you mean"** — not tested from this IP (blocked), but that is the classic laundering path in a browser.

**6B. One volume/page, several dispositions**

- CAP: multiple metadata rows sharing `first_page`; extra HTML files `{page}-02.html`.
- CourtListener **citation-lookup status 300** + `clusters[]` — this is the machine signal. Search API will just return several hits with the same cite, or several hits that *mention* the cite.
- Always require **caption token overlap** (and docket, if present) before FOUND.
- Never auto-accept `clusters[0]`.

**6C. Widely recommended, now dead / degraded / acquired (dated)**

| Thing | What happened |
|---|---|
| **Casetext** | Acquired by Thomson Reuters 2023-08-17. Standalone killed **2025-04-01**. **410 Gone** on 2026-09-19. SmartCite is gone. |
| **CAP live API + search** (`api.case.law`, case.law search) | Restrictions lifted 2024-03; **API/search sunset 2024-09-05**. Static bulk remains. Corpus search is CourtListener. |
| **AnyLaw** | "System Upgrade" placeholder, 2026-09-19. |
| **Anystate.com as caselaw** | It is a news site. |
| **Google Scholar as an API** | Datacenter 403. Not new, still true. |
| **Justia / FindLaw / OpenJurist as scrapable** | Cloudflare 403 from this IP, 2026-09-19. |
| **Fastcase 7 standalone** | Merging into **vLex Fastcase** through 2025–2026. `fc7.fastcase.com` is a login gateway. Bar-member benefit, not a public API. |
| **old.case.law** | Was kept only until September 2024 per the LIL post. Do not bookmark it as current. |
| **CiteGeist daily/monthly CL dumps / old JSON bulk** | Removed in CL bulk v3 (see FLP issues #285 / #1983). Quarterly CSV only. |

---

## The four lists

### (1) Ranked pipeline

Use this order. Stop when the stopping rule fires. Existence ≠ holding.

0. **Parse** with eyecite / reporters-db → `(reporter, volume, page)` or `WL` or `docket`. If eyecite cannot parse it, do not call it verified.

1. **Primary existence probe — CourtListener citation-lookup** (token).
   POST `volume` / `reporter` / `page` (or `text=`).
   - `200` + caption overlap → FOUND (existence only).
   - `404` → NOT_FOUND candidate (go to step 2 before you believe it).
   - `300` → **stop, do not pick a cluster.** Human / caption disambiguation.
   - `400` → unknown reporter, not a case miss.
   - If no token: fielded search `type=o&q=citation:"{vol} {reporter} {page}"` and require the **result `citation` array** to contain that pin **and** caption overlap. `count=0` → NOT_FOUND candidate. `count>1` with matching pins → treat as 300.

2. **Corroborator — CAP static** if the reporter/year is inside the cliff (U.S. ≤2014, F.3d ≤~2019, F. App'x ≤~2018, Cal.2d all, Cal.App.5th only vols 1–11, no F.4th).
   GET `CasesMetadata.json`, find `first_page == page` and caption overlap.
   - Hit → existence corroborated.
   - Miss **inside** the window → strong NOT_FOUND.
   - Miss **outside** the window → ignore CAP.

3. **Pin-confirmation** (only after FOUND):
   - CAP HTML `class="page-label">*{pin}` or `data-label="{pin}"` → pin CONFIRMED.
   - Else official PDF page (SCOTUS prelim/bound, govinfo USREPORTS, LOC usrep) → pin CONFIRMED for U.S. Reports.
   - Else vendor-neutral ¶ number from the issuing court → pin CONFIRMED in that system only.
   - Else slip PDF page → mark pin **SECONDARY** and say so.
   - **Never** confirm a pin from CL search snippets, LII HTML, or a circuit slip against an F.3d/F. App'x cite.

4. **Recent SCOTUS overlay:** scrape `/opinions/slipopinion/{yy}` for docket → `604 U.S. 593`-style official cite. Prefer the prelim PDF over the slip.

5. **Docket-only (C6):** require `court_id` (or circuit). Construct the court's own PDF if the pattern is known (CA4 `{docket}.u.pdf`; CA9 needs date). Never search a bare `24-6244`.

6. **WL-only (C5):** server **stop.** No free source this session resolved a bare WL number. **Manual:** look it up on Westlaw Patron Access for Pro Se (this account). If you also have a docket+court+date, fetch the court's PDF as well.

7. **Negative control / fabrication:** if step 1 is 404/count=0 and step 2 (in-window) misses → NOT_FOUND. Do not run a fuzzy name search "to be helpful." A Westlaw miss on a well-formed cite is strong NOT_FOUND.

8. **Treatment:** do not ask the *server* pipeline. **Manual:** KeyCite on this Westlaw account (Negative Treatment / History / `kc {cite}`). CL's graph is still only a reading list.

### (2) Every source that could not be reached (and what was tried)

| Target | Tried | Result |
|---|---|---|
| CourtListener citation-lookup (authenticated) | POST without token | 401 — token unset in this environment |
| CourtListener /opinions/, /clusters/, /opinions-cited/ | GET unauth | 401 |
| CourtListener /terms/ | GET | CloudFront 403 |
| CourtListener opinion HTML | GET /opinion/118137/… and Horn | 202, 0-byte body |
| Google Scholar search + scholar_case + related | GET | 403 bot wall |
| Justia (6 constructible URLs) | GET | Cloudflare 403 |
| FindLaw (3 URLs) | GET | Cloudflare 403 |
| OpenJurist case paths (4 URLs) | GET | Cloudflare 403 (homepage 200) |
| CaseMine (2 URLs) | GET | 403 nginx |
| web.fastcase.com | GET | fetch failed |
| CAP api.case.law JSON | GET | 200 HTML redirect to docs — API gone |
| govinfo API /collections | GET no key | 401 API_KEY_MISSING |
| govinfo /app/search and /app/collection/uscourts | GET | 200 empty JS shell |
| Oyez case page | GET | 200 empty Angular shell |
| CA9 CDN directory indexes | GET | 200, 0 bytes (no listing) |
| Casetext | GET | 410 Gone |
| AnyLaw | GET | "System Upgrade" |
| Westlaw Patron Access for Pro Se from this server | not attempted (login + license; Plaintiff reached it in a phone browser) | — |
| Lexis / Shepard's | not attempted (on-site library) | — |
| Authenticated Fastcase / vLex opinion text | login wall | — |

### (3) The honest gaps

Jobs that **cannot** be done for free from a headless server:

| Job | Cannot do | Realistic workaround |
|---|---|---|
| Confirm a **pin** to F.3d / F.4th / Cal.5th / Cal.App.5th after CAP's cliff | No free star pages for post-2018/2019 bound volumes **from a server** | **This Westlaw account** (reporter view / star pages). Or cite the **slip / vendor-neutral ¶** and mark the reporter pin SECONDARY |
| Resolve a **bare WL number** with no reporter parallel | C5 `2016 WL 4761808` → nothing on free sources. `westlawCite:` on CL is empty. | **This Westlaw account.** If you also have a docket+court+date, fetch the court's PDF as a parallel |
| **Negative treatment** (reversed, overruled, vacated, depublished) | No free flag from a server | **KeyCite on this Westlaw account.** Shepard's remains available on-site at Alameda / SF / Santa Clara / Sac / Witkin. CL's graph is still not a citator |
| **California depublication / review-granted / "not citable"** | Free sites serve the old text with no banner | **KeyCite History** on this Westlaw account, plus the Supreme Court orders. Do not cite unpublished CA opinions (CRC 8.1115) just because CL/CAP/Justia showed the PDF |
| **Google Scholar How Cited** from a server | 403 | Manual browser on a residential IP, or skip |
| **Justia / FindLaw / OpenJurist** as probes | Cloudflare | Manual only |
| **Current-Term official U.S. Reports page** before the prelim issues | Only slip pages exist | Cite `___ U.S. ___` + docket, or wait for the prelim PDF on supremecourt.gov |
| **Unique resolution of a docket number without a court** | Structurally impossible | Always pair number + court + date |
| **Authenticated CL citation-lookup in this environment** | No token present | Set `COURTLISTENER_TOKEN` (free). Until then, fielded `citation:"…"` search is the fallback |

### (4) Traps — sources that will confidently hand back a wrong case

1. **CourtListener unauthenticated full-text search** (`q="14 Cal.2d 47"`) — 81 citing cases, wrong first caption.
2. **Any pipeline that accepts `results[0]`** without matching the `citation` array and the caption.
3. **Docket-number search** (`24-6244`) — four real cases, this session's opinion hit was the wrong circuit.
4. **vLex `/vid/{guess}`** — 200, different case.
5. **CAP `{page}-01.html` without metadata** — table-page / multi-disposition collision.
6. **CAP 404 after ~2014–2018** — real cases look fabricated.
7. **HTTP 200 empty shells** (Oyez, govinfo app, Fastcase gateway, retired `api.case.law`).
8. **Casetext bookmarks** — 410, or a Thomson Reuters AI product if someone "just follows the redirect."
9. **Scholar / Justia "similar cases" in a browser** — not demonstrated here because they blocked the server; still the classic laundering UI. Never treat a fuzzy suggestion as FOUND.
10. **eyecite / any parser** — will normalize C7 into a perfect triple. Parser output is not a source hit.

---

```
SOURCE: Westlaw Patron Access for Pro Se (Thomson Reuters library remote pilot)
URL TESTED: Not fetched from this server. Plaintiff screenshots 2026-09-19:
           ess.thomsonreuters.com landing ("WESTLAW PATRON ACCESS FOR PRO SE
           (for non-commercial use)" + Access Westlaw);
           next.westlaw.com click-wrap; next.westlaw.com home after agree.
REACHABLE FROM A SERVER?: NO — login + JS + library-issued OnePass
HTTP RESULT: Not attempted from the datacenter (would be a license and
  credential violation). Plaintiff's phone session reached the live home page.
ACCESS: in-person-only at most county libraries; this product is the *remote*
  exception for self-represented litigants via a participating library link
  (Riverside and San Diego publish the same pilot; other counties may).
  Not a personal paid subscription. Not bar-membership-gated.
API OR URL PATTERN: search only after login. No constructible reporter URL
  for a headless probe. Re-enter through the *library* remote link, not a
  bookmarked next.westlaw.com.
RESPONSE FORMAT: HTML SPA (next.westlaw.com)
RATE LIMIT: Shared seats — commonly 2 concurrent users per library. Sign Off
  or the seat holds ~7–15 minutes. San Diego publishes 20 downloads/session
  and 150/day across both seats; after that, print only.
COVERAGE: Remote package = primary state and federal law (cases, statutes,
  regulations, trial-court orders). Home page this session showed Cases,
  Topics & Key Numbers, Trial Court Orders, Statutes & Court Rules,
  Regulations, Administrative Decisions, Practical Law, Secondary Sources,
  FormFinder, Briefs, Jury Verdicts, Dockets. On-site Westlaw at the same
  libraries has more secondary sources than the remote pilot.
STAR PAGINATION?: YES on Westlaw case views (star pages / official reporter
  pagination). Not screenshotted this session — confirm on the first case
  opened. Pins taken from Westlaw reporter view are the accepted confirmation
  when CAP has no *page-label.
UNPUBLISHED DISPOSITIONS?: Yes. This is how a bare WL number (C5) gets resolved.
  F. App'x and unreported orders are in the cases collection.
SUBSEQUENT HISTORY?: **KeyCite** — Negative Treatment / History / Citing
  References tabs on the case. Type `kc {cite}` in the search box. This is
  the only real citator now in Plaintiff's hands. Not an API.
CONTROL RESULTS: C1–C7 not run on this account this session.
  First manual jobs: KeyCite the live authorities; resolve 2016 WL 4761808;
  confirm any F.3d/F.4th/Cal.App.5th pin past CAP's cliff.
LICENSE: Click-wrap affirmed on screen (quoted): personal pro se use only;
  not on behalf of a firm, company, government, or nonprofit; no competitive
  analysis or benchmarking; agree to Patron Access for Pro Se terms.
  That matches this portfolio. It does not authorize automation, sharing the
  OnePass, or feeding the account into a probe script.
FAILURE MODE: Going directly to westlaw.com / next.westlaw.com next time
  (library pages say the remote link is required). Treating a KeyCite "cited
  by" count as a holding. Pasting credentials into chat.
VERDICT: MANUAL ONLY
WHY: This is the missing citator and the WL-number resolver. It must stay
  in a logged-in browser. Do not wire it.
```

*Generated 2026-09-19; Westlaw Patron Access for Pro Se added the same day from Plaintiff's screenshots. Re-run `node internal/scripts/survey-citation-sources.mjs` before trusting reachability; Cloudflare and 410s move.*
