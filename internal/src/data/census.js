// Hand-verified aggregates that can't be reliably derived from the free-text prose
// fields in matters.js (`defendants` is a single narrative string per matter, not a
// structured list, and `causes` labels are worded slightly differently case-to-case
// even when they assert the same underlying theory). Compiled by a four-pass census
// of the full portfolio on July 25, 2026 — re-verify by hand if the underlying
// narrative fields change materially. Everything else on the Census tab (matter
// counts, cluster/status splits, timeline pace, financial exposure, fee value) is
// computed live from the existing data files, not hardcoded here.
export const census = {
  asOf: "July 25, 2026",
  namedDefendants: 33,
  namedInstitutions: 19,
  feeWaiversGranted: 8,
  feeWaiversDenied: 1,
  distinctTheories: 24,
  topTheories: [
    { label: "Negligence / Negligence Per Se", count: 12 },
    { label: "14th Amendment Due Process", count: 11 },
    { label: "Intentional Infliction of Emotional Distress", count: 9 },
    { label: "Unfair Competition, UCL §17200", count: 8 },
    { label: "Bane Act, Civ. Code §52.1", count: 7 },
    { label: "Declaratory Relief", count: 7 },
    { label: "42 U.S.C. §1983 (general)", count: 7 },
    { label: "4th Amendment", count: 6 },
    { label: "PC §290.46(j) Registry Bar", count: 6 },
    { label: "ICRAA, Civ. Code §1786", count: 6 },
    { label: "PC §3008(d)(2) / 15 CCR §3574", count: 5 },
    { label: "Tameny Wrongful Termination / Failure to Hire", count: 5 },
  ],
  // The repeatable claim: PC §290.46(j)(2)(E) applied to six separate employers.
  // Vendor names live only in each matter's key_facts prose, so they're curated
  // here; caption/status for each matter is still pulled live from PORTFOLIO.cases.
  registryBarEmployers: [
    { matter: 22, vendor: "Checkr, Inc." },
    { matter: 23, vendor: "HireRight" },
    { matter: 25, vendor: "First Advantage" },
    { matter: 26, vendor: "First Advantage" },
    { matter: 27, vendor: "InfoMart" },
    { matter: 29, vendor: "Accurate Background" },
  ],
};
