import { useState } from "react";
import { Link } from "react-router";
import { cases } from "../data/matters";
import { CLUSTERS, formatMatterRanges } from "../data/clusters";
import { damages_table } from "../data/damages";
import { jurisdictions } from "../data/portfolioMeta";
import { headline_coverage, formatLimit } from "../data/coverage";
import { formatCurrency } from "../utils/formatters";
import { useNextActions } from "../hooks/useNextActions";
import { NextActionsPanel } from "./NextActionsPanel";
import syncState from "../data/courtlistener/sync-state.json";
import indexMeta from "../data/index/matters.json";
import {
  countCourts,
  isActiveExposureRow,
  litigatingMatters,
  preFilingMatters,
  sumExposure,
} from "../utils/portfolioStats";

const totalMatters = cases.length;
const litigating = litigatingMatters(cases);
const preFiling = preFilingMatters(cases);
const activeMatters = litigating.length;
const byNumber = new Map(cases.map((c) => [Number(c.number), c]));
const liveDamages = damages_table.filter((row) => isActiveExposureRow(row, byNumber));
const clusterCounts = Object.fromEntries(CLUSTERS.map((cl) => [cl.n, 0]));
const clusterNumberLists = Object.fromEntries(CLUSTERS.map((cl) => [cl.n, []]));
const courtCounts = countCourts(cases, jurisdictions);
let federalCount = 0;
let stateCount = 0;
for (const c of litigating) {
  if (c.type === "Federal") federalCount++;
  else if (c.type === "State") stateCount++;
}
for (const c of cases) {
  if (clusterCounts[c.cluster] !== undefined) {
    clusterCounts[c.cluster]++;
    clusterNumberLists[c.cluster].push(c.number);
  }
}

const clusterMattersStr = Object.fromEntries(
  CLUSTERS.map((cl) => [cl.n, formatMatterRanges(clusterNumberLists[cl.n])]),
);

const moderateExposure = formatCurrency(sumExposure(liveDamages, "moderate"));

export const DashboardTab = ({ setClusterFilter, setActiveTab }) => {
  const { queue, nextMine } = useNextActions(30);
  const [mineOnly, setMineOnly] = useState(false);
  const dataAsOf = indexMeta?.today || null;
  const clEntries = Object.values(syncState?.matters ?? {});
  const clMatters = clEntries.length;
  const clLast = clEntries
    .map((row) => row?.last_synced_at)
    .filter(Boolean)
    .sort()
    .at(-1);
  const clLastDay = typeof clLast === "string" ? clLast.slice(0, 10) : null;
  const clStatus = clMatters > 0
    ? `${clMatters} dockets${clLastDay ? `, last ${clLastDay}` : ""}`
    : "not run";

  return (
    <div className="dashboard-view">
      <div className="data-freshness-badge" role="status">
        {dataAsOf ? <span>Portfolio clocks as of {dataAsOf}</span> : <span>Portfolio data date unknown</span>}
        <span className="freshness-sep">·</span>
        <span className={clLastDay ? "freshness-paused" : "freshness-paused"}>
          CourtListener sync: {clStatus}
        </span>
      </div>
      {/* Stats Row */}
      <div className="dashboard-stats">
        {[
          { label: "Active Matters", value: activeMatters, sub: `${federalCount} Federal · ${stateCount} State · ${preFiling.length} pre-filing · ${totalMatters} tracked` },
          { label: "Jurisdictions", value: jurisdictions.length, sub: "Courts across CA" },
          { label: "Aggregate Exposure", value: moderateExposure, sub: "Live moderate (excludes settled)" },
          { label: "Next on your desk", value: nextMine?.date || "—", sub: nextMine ? `M${nextMine.matters[0]} · ${nextMine.action}` : "Nothing dated" }
        ].map((s, i) => (
          <div key={i} className="dashboard-stat-card">
            <div className="dashboard-stat-label">{s.label}</div>
            <div className="dashboard-stat-value">{s.value}</div>
            <div className="dashboard-stat-sub">{s.sub}</div>
          </div>
        ))}
        {headline_coverage && (
          <Link
            to={`/matters/${headline_coverage.matter}`}
            className="dashboard-stat-card dashboard-stat-card-coverage"
            title={`${headline_coverage.carrier} Policy No. ${headline_coverage.policyNo} — ${headline_coverage.insureds.join(" and ")}`}
          >
            <div className="dashboard-stat-label">Insured Exposure</div>
            <div className="dashboard-stat-value">
              {formatLimit(headline_coverage.perIncident)} <span className="dashboard-stat-slash">/</span>{" "}
              {formatLimit(headline_coverage.aggregate)}
            </div>
            <div className="dashboard-stat-sub">
              {headline_coverage.insureds.join(" · ")} — Matter {headline_coverage.matter}
            </div>
          </Link>
        )}
      </div>

      <NextActionsPanel queue={queue} mineOnly={mineOnly} onMineOnlyChange={setMineOnly} />

      {/* Two-column: Clusters + courts */}
      <div className="grid-2 dashboard-primary-grid">
        <section className="dashboard-panel">
          <h3 className="dashboard-heading">Case Clusters</h3>
          {CLUSTERS.map(cl => (
            <button
              key={cl.n}
              className="dashboard-cluster"
              type="button"
              onClick={() => { setClusterFilter(cl.n); setActiveTab("Matters"); }}
              aria-label={`Filter matters by cluster: ${cl.label}`}
            >
              <div className="dashboard-cluster-header">
                <span>{cl.label}</span>
                <span style={{ color: cl.color }}>{clusterCounts[cl.n] || 0} matters</span>
              </div>
              <div className="dashboard-cluster-meta">Matters {clusterMattersStr[cl.n] || "—"}</div>
              <div className="dashboard-cluster-track">
                <div className="dashboard-cluster-bar" style={{ width: `${((clusterCounts[cl.n] || 0) / totalMatters) * 100}%`, background: cl.color }} />
              </div>
            </button>
          ))}
          <div className="dashboard-cluster-hint">Click a cluster to filter matters →</div>
        </section>

        <section className="dashboard-panel">
          <h3 className="dashboard-heading">Jurisdictional Distribution</h3>
          <div className="dashboard-jurisdictions">
            {jurisdictions.map(j => (
              <div key={j} className="dashboard-jurisdiction">
                <div className="dashboard-jurisdiction-name">{j}</div>
                <div className="dashboard-jurisdiction-count">{courtCounts[j] || 0}</div>
              </div>
            ))}
          </div>
        </section>
      </div>

      {/* Milestone: First Settlement */}
      <div className="dashboard-milestone">
        <div className="dashboard-milestone-inner">
          <div className="dashboard-milestone-icon">💰</div>
          <div>
            <h3 className="dashboard-heading compact">First Case to Settle</h3>
            <p className="dashboard-milestone-copy">
              Matter 22 became the first matter in this portfolio to reach a negotiated settlement — resolved pro se, without counsel, in under seven weeks from filing.
            </p>
          </div>
        </div>
      </div>

      {/* Milestone: First Interstate Case */}
      <div className="dashboard-milestone dashboard-milestone-last">
        <div className="dashboard-milestone-inner">
          <div className="dashboard-milestone-icon">🌎</div>
          <div>
            <h3 className="dashboard-heading compact">First Interstate Reaching Case</h3>
            <p className="dashboard-milestone-copy">
              Matter 22 represents the first litigation matter with interstate service of process. Demand letter sent via Certified Mail to corporate headquarters in Tennessee.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};
