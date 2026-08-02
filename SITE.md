# Equity2Bitcoin commercial site

Marketing + conversion site for **Equity2Bitcoin Consulting LLC**.

## Local

```bash
npm install
npm run dev
```

## Launch config

Copy `web/.env.example` to `web/.env` (or set Vercel env vars):

| Variable | Purpose |
|---|---|
| `VITE_CALENDLY_URL` | Calendly orientation event URL — enables inline booking embed |
| `VITE_CALENDLY_REVIEW_URL` | Optional Milestone 1 review event |
| `VITE_LEAD_WEBHOOK_URL` | Optional Zapier/Make/HubSpot webhook for quiz + form leads |

Tunables (fee rate, BTC reference price, calculator defaults) live in `web/src/config/site.ts`.

Without Calendly configured, `/book` shows a request form after the acknowledgment gate (and posts to the webhook if set).

## Funnel

1. Hero wake-up → Equity IQ quiz **or** `/calculator`  
2. `/fit` self-qualification + volatility honesty  
3. Quiz/calc → `/book` acknowledgment gate → Calendly / form  
4. Milestone Agreement offline/DocuSign  

## Substance integrated from Claude’s branch

Kept (functional, not stylistic): LTV-aware tappable equity math, fee-before-BTC netting, carry-cost display, fit page, Why Bitcoin cycles without price targets, booking acknowledgment gate, `LEGAL-REVIEW.md`, equity unit tests.

## Legal

See [`LEGAL-REVIEW.md`](./LEGAL-REVIEW.md) before pointing a live consumer domain at this site.

## Note on this branch

This branch serves the commercial site from `web/`. The prior litigation portfolio code under `internal/` is unused by the Vite build here and remains for reference until product direction is finalized.
