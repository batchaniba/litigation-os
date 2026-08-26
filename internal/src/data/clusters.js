// The five thematic groupings the portfolio is organised around. Lives here
// rather than on DashboardTab because CensusTab needs it too, and importing a
// constant from a component module pulled the whole dashboard — and the damages
// table behind it — into the census chunk.
export const CLUSTERS = [
  { n: 1, label: "CHP Traffic Stop, DUI Arrest & DMV", color: "#60A5FA" },
  { n: 2, label: "Parole Retaliation, HOPE Abuse & Policy 19-03", color: "#A78BFA" },
  { n: 3, label: "Employment Violations", color: "#FBBF24" },
  { n: 4, label: "Administrative Writs & Habeas Corpus", color: "#34D399" },
  { n: 5, label: "Consumer Fraud / Defective Vehicle", color: "#F97316" },
  { n: 6, label: "Public Accommodation / Unruh", color: "#FB7185" },
];

/** Short labels for the matters-list filter chips. */
export const CLUSTER_LABELS = {
  1: "CHP",
  2: "Parole/HOPE",
  3: "Employment",
  4: "Writs",
  5: "Consumer Fraud",
  6: "Unruh / Public Accom.",
};
