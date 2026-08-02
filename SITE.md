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
| `VITE_CALENDLY_URL` | Calendly event URL — enables inline booking embed |
| `VITE_LEAD_WEBHOOK_URL` | Optional Zapier/Make/HubSpot webhook for quiz + form leads |

Without Calendly configured, `/book` shows a request form and stores a lead draft in `sessionStorage` (and posts to the webhook if set).

## Funnel

1. Hero wake-up → Equity IQ quiz  
2. Quiz score saved to session → Book orientation  
3. Calendly (or fallback form) → Milestone Agreement offline/DocuSign  

## Note on this branch

This branch serves the commercial site from `web/`. The prior litigation portfolio code under `internal/` is unused by the Vite build here and remains for reference until product direction is finalized.
