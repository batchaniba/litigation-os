// Numbered thematic buckets. This file is the single source of truth for
// matter.json `cluster` integers, the SPA cluster cards, and generated
// README Case Cluster headings. Do not keep a second number→label table.
//
// These integers are not the named cross-matter graph
// (index/clusters.json / crossMatter.json: `chp-nov2024`,
// `megan-law-employment`, …). Named ids are slugs; numbered ids are 1–6.
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

export const NUMBERED_CLUSTER_IDS = new Set(CLUSTERS.map((c) => c.n));

export function numberedClusterById(n) {
  return CLUSTERS.find((c) => c.n === Number(n)) ?? null;
}

export function isNumberedClusterId(n) {
  return NUMBERED_CLUSTER_IDS.has(Number(n));
}

/** Compact "1, 2, 7–8" list for UI meta and README headings. */
export function formatMatterRanges(nums) {
  if (!nums.length) return "—";
  const sorted = [...new Set(nums.map(Number))].sort((a, b) => a - b);
  const ranges = [];
  let start = sorted[0];
  let end = sorted[0];
  for (let i = 1; i < sorted.length; i++) {
    if (sorted[i] === end + 1) {
      end = sorted[i];
    } else {
      ranges.push(start === end ? `${start}` : `${start}–${end}`);
      start = end = sorted[i];
    }
  }
  ranges.push(start === end ? `${start}` : `${start}–${end}`);
  return ranges.join(", ");
}
