# Matter 37 — Home Depot valuation formula (November 1, 2026)

Case: Ngwa Nforbi v. Home Depot U.S.A., Inc., No. 2:26-cv-03310-TLN-AC (E.D. Cal.).
Operative complaint filed September 18, 2026: single cause of action under
Penal Code § 290.46(j)(2)(E), (j)(4)(A). Service complete October 14, 2026
(U.S. Marshal on CSC, Sacramento; USM-285 return, Dkt. 8, filed October 19, 2026).
Answer or Rule 12 motion due November 4, 2026.

This note is a repo-internal working paper for other models. It is NOT website
content and does NOT change damages.json (which still carries the older
post-favorable-MTD settlement range). The user directed on November 1, 2026
that the repo's older numbers be set aside and the formula run afresh.

## Inputs

- W (weekly wage) = $560/week — USER-SUPPLIED November 1, 2026.
- D (distress) = $150,000 — USER-SUPPLIED November 1, 2026.
- Loss start: on or about August 2024 (Tracy warehouse/distribution/fulfillment
  role, 5395 Hopkins Rd; accepted, onboarding began, background check, then
  ghosted; no independent reason communicated).
- Back-pay window: August 2024 → assumed August 2027 trial = 152–156 weeks
  (midpoint 154). The August 2027 trial date is an ANALOGY to the FedEx
  removal-paper shape, NOT a scheduled Home Depot trial date. Home Depot has
  no trial date set.
- Front-pay window: 104 weeks after trial (FedEx shape).
- Benefits: 15% of wages (the Matter 29 working figure).
- Framework: canonical v1 — C = back + front + benefits (15%) + distress;
  Loaded = 3 × C; Opening = 1.33 × Loaded; Target = 32–53% of Loaded.
  Discounted-front variant per framework v2: 4% real discount, weekly payments.

## Back pay

- Midpoint: 154 weeks × $560 = $86,240 gross; $99,176 with 15% benefits.
- Range across 152–156 weeks: $85,120–$87,360 gross ($97,888–$100,464 with benefits).

## Front pay

- Gross (FedEx shape): 104 weeks × $560 = $58,240; $66,976 with 15% benefits.
- Discounted (v2, 4% real, weekly payments over 104 weeks): present-value
  factor 99.91 → $55,951 gross; $64,343 with 15% benefits. The discount only
  shaves about 4% off gross.
- CEILING, not net: before the v2 tenure adjustment for a never-commenced
  at-will role (hire-probability × tenure-survival, unquantified) and before
  any mitigation offset.

## Totals (midpoint, gross front)

- Wages: $86,240 (back) + $58,240 (front) = $144,480
- Benefits (15%): $21,672
- Distress: $150,000
- C = $316,152 (range $314,864–$317,440 across back 152–156 weeks;
  discounted-front C = $313,519)
- Loaded (3 × C) = $948,456
- Framework opening (1.33 × Loaded) = $1,261,446
- Framework target (32–53% of Loaded) = $303,506–$502,682

## Caveats other models must carry with these numbers

1. GROSS before mitigation. Interim earnings are unknown, and the base resume
   shows continuous HD Supply (Pleasanton) warehouse employment from April 2023
   to the present, straight through the Home Depot loss period — the same
   mitigation mechanics as Delta Hotels in Matter 29, likely offsetting
   back-pay wage loss heavily. Net wage loss may be far below the gross legs.
2. Distress is ~47% of C. Distress corroboration does the heavy lifting here,
   as in Matter 29. Do not present C as wage-driven.
3. WAGE PROVENANCE GAP. The filed complaint ¶54 pointedly refuses to invent an
   hourly wage, weekly-hours figure, or employment duration unsupported by the
   record, and no Home Depot offer letter, pay record, or wage statement is in
   the file. W = $560/week is user-supplied, NOT record-established. Do not
   cite it as documented, and do not put demand math built on W in front of
   Home Depot until W has a documentary source — Home Depot will quote ¶54
   back.
4. The framework opening (~$1.26M) is arithmetic, not the user's demand. The
   user's anchor demand is $550,000, which sits just above the framework target
   band's top ($502,682) and well below formula opening — the same
   below-formula posture as Matter 29's $335,000 against its ~$445,368 formula
   demand.
5. Statutory footing: § 290.46(j)(4)(A) authorizes actual damages plus additional
   damages up to 3× actuals plus exemplary damages. Actuals $316,152 + 3×
   additional alone is ~$1.26M before exemplary damages, so the framework
   opening sits within the statute's own multiples, not above them.
6. Rounding rule for outward use: cite $1.25 million, not $1,261,446, and frame
   through the statute (actuals + statutory additional), not through the
   multiplier chain (3× then 1.33×), which reads as stacked markups.

## Machine-readable summary

- matter: 37; case: 2:26-cv-03310-TLN-AC; W: 560; D: 150000
- back_weeks_mid: 154; back_gross: 86240; front_weeks: 104; front_gross: 58240
- wages: 144480; benefits_15pct: 21672; C: 316152; loaded: 948456
- framework_opening: 1261446; framework_target_lo: 303506; framework_target_hi: 502682
- anchor_demand: 550000; front_pay_discounted_pv: 55951; front_pay_discounted_with_benefits: 64343
- status: gross_before_mitigation; trial_date_analogy_only; wage_provenance_gap
