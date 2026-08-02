/** Tunables a non-developer may need to change before/after launch. */

export const SITE = {
  name: "Equity2Bitcoin",
  legalEntity: "Equity2Bitcoin Consulting LLC",
  domain: "equity2bitcoin.com",
  email: "hello@equity2bitcoin.com",
  jurisdiction: "California, USA",
} as const;

/**
 * Replace PLACEHOLDER URLs with real Calendly event links before launch.
 * While a URL still contains "PLACEHOLDER", booking shows a configured fallback.
 */
export const CALENDLY = {
  orientationUrl: (import.meta.env.VITE_CALENDLY_URL as string | undefined)?.trim() ||
    "https://calendly.com/PLACEHOLDER/orientation-20min",
  equityReviewUrl:
    (import.meta.env.VITE_CALENDLY_REVIEW_URL as string | undefined)?.trim() ||
    "https://calendly.com/PLACEHOLDER/equity-profile-review",
} as const;

export function isCalendlyConfigured(url: string): boolean {
  return Boolean(url) && !url.includes("PLACEHOLDER");
}

/** Milestone success fee — charged once at verified loan funding (Phase 3). */
export const MILESTONE_FEE_RATE = 0.3;

/**
 * Static illustrative BTC price for calculator education.
 * Update price and asOf together, or remove the BTC line entirely.
 */
export const BTC_REFERENCE = {
  priceUsd: 95_000,
  asOf: "January 2026",
} as const;

export const CALCULATOR_DEFAULTS = {
  homeValue: 700_000,
  mortgageBalance: 400_000,
  maxLtv: 0.8,
  ltvMin: 0.75,
  ltvMax: 0.85,
  aprPercent: 8.5,
  amortizationYears: 20,
} as const;
