// ==========================================================
// Known insurance coverage backing portfolio defendants.
//
// This is the single source of truth for policy limits. The matter JSON
// carries a short `policy_limits` string for its badge; validate-portfolio
// cross-checks that string against `limitsShort` here so the two can't drift.
//
// Why this matters enough to be its own module: policy limits are the only
// figure in the portfolio that is *collectable on sight*. Damages estimates
// are argued; a policy tower is a number the carrier has already agreed to
// pay up to. It anchors every settlement conversation, so it belongs in the
// shell bundle where the header can reach it without loading a matter file.
// ==========================================================

/**
 * @typedef {Object} CoverageRecord
 * @property {number} matter        Portfolio matter number.
 * @property {string} caption       Matter caption.
 * @property {string} caseNo        Case number.
 * @property {string} court         Court shorthand.
 * @property {string} carrier       Insurance carrier.
 * @property {string} policyNo      Policy number as produced in discovery.
 * @property {number} perIncident   Per-incident limit, in dollars.
 * @property {number} aggregate     Aggregate limit, in dollars.
 * @property {string} limitsShort   Display string; must match matter.policy_limits.
 * @property {string[]} insureds    Defendants the tower covers.
 * @property {string} source        Where the policy came from.
 * @property {string} leverage      Why the number matters, in one sentence.
 */

/** @type {CoverageRecord[]} */
export const insurance_coverage = [
  {
    matter: 28,
    caption: "Newanforbi v. Shannon Smith, LCSW, CEO, et al.",
    caseNo: "3:26-cv-07504",
    court: "USDC N.D. Cal.",
    carrier: "Philadelphia Indemnity",
    policyNo: "067968",
    perIncident: 1_000_000,
    aggregate: 5_000_000,
    limitsShort: "$1M / $5M",
    insureds: ["HOPE Psychotherapy, Inc.", "Shannon Smith, LCSW"],
    source: "Produced in Matter 5 discovery (Bates HOPE_000001–542)",
    leverage:
      "A carrier-funded floor that does not depend on either defendant's balance sheet — and Shannon Smith's individual-capacity exposure sits outside the corporate tower, creating personal settlement pressure on top of it.",
  },
];

/** Coverage record for a matter, or undefined when none is on file. */
export function coverageForMatter(number) {
  return insurance_coverage.find((record) => record.matter === Number(number));
}

/** The record to feature in portfolio-wide chrome (largest aggregate tower). */
export const headline_coverage = insurance_coverage.reduce(
  (largest, record) => (!largest || record.aggregate > largest.aggregate ? record : largest),
  null,
);

/** Compact dollar label: 1_000_000 -> "$1M". */
export function formatLimit(dollars) {
  if (dollars >= 1_000_000) {
    const millions = dollars / 1_000_000;
    return `$${Number.isInteger(millions) ? millions : millions.toFixed(1)}M`;
  }
  if (dollars >= 1_000) return `$${Math.round(dollars / 1_000)}K`;
  return `$${dollars}`;
}
