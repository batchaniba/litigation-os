import { useState } from "react";
import { Link } from "react-router";
import { cases } from "../data/matters";
import { CLUSTERS, formatMatterRanges } from "../data/clusters";
import { damages_table } from "../data/damages";
import { jurisdictions } from "../data/portfolioMeta";
import { headline_coverage, formatLimit } from "../data/coverage";
import { formatCurrency } from "../utils/formatters";
import { isArchivedMatter, isOpenLifecycle } from "../utils/matterLifecycle";
import { useNextActions } from "../hooks/useNextActions";
import { NextActionsPanel } from "./NextActionsPanel";
import { timeline } from "../data/timeline";
import syncState from "../data/courtlistener/sync-state.json";

const totalMatters = cases.length;
// "Active Matters" is the open-docket count -- still on the docket, settled
// included (isOpenLifecycle), not the narrower "currently being litigated"
// set. A settled-but-not-yet-dismissed matter (e.g. Matter 22) still belongs
// here; its card carries its own Settled ribbon/badge regardless.
const activeMatters = cases.filter(c => isOpenLifecycle(c.lifecycle) || (!c.lifecycle && !c.archived)).length;
const clusterCounts = Object.fromEntries(CLUSTERS.map((cl) => [cl.n, 0]));
const clusterNumberLists = Object.fromEntries(CLUSTERS.map((cl) => [cl.n, []]));
const courtCounts = {};
let federalCount = 0;
let stateCount = 0;
for (const c of cases) {
  if (!isArchivedMatter(c)) {
    if (c.type === "Federal") federalCount++;
    else if (c.type === "State") stateCount++;
  }
  if (clusterCounts[c.cluster] !== undefined) {
    clusterCounts[c.cluster]++;
    clusterNumberLists[c.cluster].push(c.number);
  }
  courtCounts[c.court] = (courtCounts[c.court] || 0) + 1;
}

const clusterMattersStr = Object.fromEntries(
  CLUSTERS.map((cl) => [cl.n, formatMatterRanges(clusterNumberLists[cl.n])]),
);

const moderateExposure = formatCurrency(
  damages_table.reduce((s, r) => s + r.moderate, 0)
);

export const DashboardTab = ({ setClusterFilter, setActiveTab }) => {
  const { queue, mine } = useNextActions(30);
  const [mineOnly, setMineOnly] = useState(false);
  const nextMine = mine[0];
  // Data freshness: latest verification across timeline events.
  const verifiedDates = timeline.map((e) => e.verified_at).filter(Boolean).sort();
  const dataAsOf = verifiedDates.length ? verifiedDates[verifiedDates.length - 1] : null;
  const clMatters = syncState?.matters ? Object.keys(syncState.matters).length : 0;
  const clStatus = clMatters > 0 ? `${clMatters} dockets` : "paused";

  return (
    <div className="dashboard-view">
      <div className="data-freshness-badge" role="status">
        {dataAsOf ? <span>Portfolio data as of {dataAsOf}</span> : <span>Portfolio data date unknown</span>}
        <span className="freshness-sep">·</span>
        <span className={clMatters > 0 ? "freshness-ok" : "freshness-paused"}>
          CourtListener sync: {clStatus}
        </span>
      </div>
      {/* Stats Row */}
      <div className="dashboard-stats">
        {[
          { label: "Active Matters", value: activeMatters, sub: `${federalCount} Federal · ${stateCount} State · ${totalMatters} total` },
          { label: "Jurisdictions", value: jurisdictions.length, sub: "Courts across CA" },
          { label: "Aggregate Exposure", value: moderateExposure, sub: "Moderate estimate" },
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
