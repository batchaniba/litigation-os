// Shared Cost of Counsel math.
// Hours remain a per-matter judgment (document-type classification in
// docs/LAWYER_FEES_CALCULATOR.md). Cost, cluster rollups, and portfolio
// totals are derived so they cannot drift from the rows.

export const BLENDED_HOURLY_RATE = 280;

export const RATE_RANGE = {
  seniorPartner: [350, 450],
  midAssociate: [250, 350],
  paralegal: [150, 200],
};

/** Fee-tab billing groups. Numbered 3 + 5 stay one rollup (employment + consumer fraud). */
export const FEE_CLUSTER_DEFS = [
  { id: "cluster1", label: "CHP / DUI / DMV", numbered: [1] },
  { id: "cluster2", label: "Parole Retaliation / HOPE", numbered: [2] },
  { id: "cluster3", label: "Consumer Fraud / Employment", numbered: [3, 5] },
  { id: "cluster4", label: "Administrative Writs & Habeas", numbered: [4] },
  { id: "cluster6", label: "Public Accommodation / Unruh", numbered: [6] },
];

export function costFromHours(hours, rate = BLENDED_HOURLY_RATE) {
  return {
    low: Math.round(hours.low * rate),
    mid: Math.round(hours.mid * rate),
    high: Math.round(hours.high * rate),
  };
}

export function withDerivedCost(row, rate = BLENDED_HOURLY_RATE) {
  return { ...row, cost: costFromHours(row.hours, rate) };
}

function roundHours(n) {
  return Math.round(n * 10) / 10;
}

/**
 * @param {Array<{ number: number, cluster?: number, documentsCount: number, totalPagesReal: number, hours: { low: number, mid: number, high: number }, cost: { low: number, mid: number, high: number } }>} rows
 */
export function summarizeLawyerFees(rows, {
  analysisDate,
  trackedMatters,
  methodologyNote,
  rate = BLENDED_HOURLY_RATE,
} = {}) {
  const totalEstimatedHours = { low: 0, mid: 0, high: 0 };
  const totalEstimatedCost = { low: 0, mid: 0, high: 0 };
  let totalDocumentsAnalyzed = 0;
  let totalPagesReal = 0;

  for (const row of rows) {
    totalEstimatedHours.low += row.hours.low;
    totalEstimatedHours.mid += row.hours.mid;
    totalEstimatedHours.high += row.hours.high;
    totalEstimatedCost.low += row.cost.low;
    totalEstimatedCost.mid += row.cost.mid;
    totalEstimatedCost.high += row.cost.high;
    totalDocumentsAnalyzed += row.documentsCount;
    totalPagesReal += row.totalPagesReal;
  }

  const byNumber = new Map(rows.map((row) => [row.number, row]));
  const clustered = new Set();
  const byCluster = {};
  for (const def of FEE_CLUSTER_DEFS) {
    const numbered = new Set(def.numbered);
    const matters = rows
      .filter((row) => numbered.has(Number(row.cluster)))
      .map((row) => row.number)
      .sort((a, b) => a - b);
    for (const n of matters) clustered.add(n);
    const costLow = matters.reduce((s, n) => s + byNumber.get(n).cost.low, 0);
    const costMid = matters.reduce((s, n) => s + byNumber.get(n).cost.mid, 0);
    const costHigh = matters.reduce((s, n) => s + byNumber.get(n).cost.high, 0);
    byCluster[def.id] = {
      label: def.label,
      matters,
      costLow,
      costMid,
      costHigh,
    };
  }

  const unclustered = rows.map((row) => row.number).filter((n) => !clustered.has(n));
  if (unclustered.length) {
    throw new Error(`lawyer fee rows missing a fee-cluster mapping: ${unclustered.join(", ")}`);
  }

  return {
    analysisDate,
    totalMatters: rows.length,
    trackedMatters: trackedMatters ?? rows.length,
    totalDocumentsAnalyzed,
    totalPagesReal,
    methodology: {
      blendedHourlyRate: rate,
      rateRange: RATE_RANGE,
      note: methodologyNote,
    },
    totalEstimatedHours: {
      low: roundHours(totalEstimatedHours.low),
      mid: roundHours(totalEstimatedHours.mid),
      high: roundHours(totalEstimatedHours.high),
    },
    totalEstimatedCost,
    byCluster,
  };
}
