import { cases } from "../data/matters";
import { damages_table } from "../data/damages";
import { jurisdictions } from "../data/portfolioMeta";
import { formatCurrency } from "../utils/formatters";
import { isArchivedMatter, isLiveLifecycle } from "../utils/matterLifecycle";

const FILED_GREEN = "#34D399";
const UPCOMING_AMBER = "#FBBF24";

const totalMatters = cases.length;
const activeMatters = cases.filter(c => isLiveLifecycle(c.lifecycle) || (!c.lifecycle && !c.archived)).length;
const clusterCounts = { 1: 0, 2: 0, 3: 0, 4: 0, 5: 0 };
const clusterNumberLists = { 1: [], 2: [], 3: [], 4: [], 5: [] };
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

const formatRanges = (nums) => {
  if (!nums.length) return "—";
  const sorted = [...nums].sort((a, b) => a - b);
  const ranges = [];
  let start = sorted[0], end = sorted[0];
  for (let i = 1; i < sorted.length; i++) {
    if (sorted[i] === end + 1) { end = sorted[i]; }
    else { ranges.push(start === end ? `${start}` : `${start}–${end}`); start = end = sorted[i]; }
  }
  ranges.push(start === end ? `${start}` : `${start}–${end}`);
  return ranges.join(", ");
};
const clusterMattersStr = {
  1: formatRanges(clusterNumberLists[1]),
  2: formatRanges(clusterNumberLists[2]),
  3: formatRanges(clusterNumberLists[3]),
  4: formatRanges(clusterNumberLists[4]),
  5: formatRanges(clusterNumberLists[5]),
};

const moderateExposure = formatCurrency(
  damages_table.reduce((s, r) => s + r.moderate, 0)
);

export const CLUSTERS = [
  { n: 1, label: "CHP Traffic Stop, DUI Arrest & DMV", color: "#60A5FA" },
  { n: 2, label: "Parole Retaliation, HOPE Abuse & Policy 19-03", color: "#A78BFA" },
  { n: 3, label: "Employment Violations", color: "#FBBF24" },
  { n: 4, label: "Administrative Writs & Habeas Corpus", color: "#34D399" },
  { n: 5, label: "Consumer Fraud / Defective Vehicle", color: "#F97316" },
];

const PERTINENT_FILINGS = [
  { title: "Newanforbi v. Serrato et al.", matter: 24, date: "Filed Jun 17, 2026", dateStatus: "filed" },
  { title: "Newanforbi v. Federal Express Corporation", matter: 25, note: "Served Jul 24, 2026 — Ct Corporation System (Jaqueline Mejia)", date: "Filed Jul 15, 2026", dateStatus: "filed" },
  { title: "Newanforbi v. United Parcel Service, Inc.", matter: 26, note: "Served Jul 22, 2026 — Josh Swindell, Authorized Agent", date: "Filed Jul 15, 2026", dateStatus: "filed" },
  { title: "Newanforbi v. Randstad, et al.", matter: 27, note: "SERVED Jul 30, 2026 — Josh Swindell (Randstad & RK)", date: "Filed Jul 20, 2026", dateStatus: "filed" },
  { title: "Newanforbi v. Shannon Smith, LCSW, et al.", matter: 28, note: "Case No. 3:26-cv-07504 — Hon. Lisa J. Cisneros", date: "Filed Jul 20, 2026", dateStatus: "filed" },
  { title: "Newanforbi v. Amazon.com Services, LLC", matter: 29, date: "Pre-Complaint — BGC Pending", dateStatus: "upcoming" },
  { title: "Newanforbi v. First Advantage LLC", matter: 31, note: "Identified via portfolio gap analysis — vendor for Matters 25 & 26", date: "Not Yet Filed", dateStatus: "upcoming" },
];

export const DashboardTab = ({ upcomingEvents, setClusterFilter, setActiveTab }) => {
  return (
    <div className="dashboard-view">
      {/* Stats Row */}
      <div className="dashboard-stats">
        {[
          { label: "Active Matters", value: activeMatters, sub: `${federalCount} Federal · ${stateCount} State · ${totalMatters} total` },
          { label: "Jurisdictions", value: jurisdictions.length, sub: "Courts across CA" },
          { label: "Aggregate Exposure", value: moderateExposure, sub: "Moderate estimate" },
          { label: "Next Deadline", value: upcomingEvents[0]?.date || "—", sub: upcomingEvents[0]?.event?.slice(0, 35) || "" }
        ].map((s, i) => (
          <div key={i} className="dashboard-stat-card">
            <div className="dashboard-stat-label">{s.label}</div>
            <div className="dashboard-stat-value">{s.value}</div>
            <div className="dashboard-stat-sub">{s.sub}</div>
          </div>
        ))}
      </div>

      {/* Two-column: Upcoming + Clusters */}
      <div className="grid-2 dashboard-primary-grid">
        {/* Upcoming */}
        <section className="dashboard-panel">
          <h3 className="dashboard-heading">Upcoming Deadlines</h3>
          <div className="dashboard-deadlines">
            {upcomingEvents.map((e, i) => (
              <div key={i} className="dashboard-deadline">
                <div className="dashboard-deadline-date">{e.date}</div>
                <div>
                  <div className="dashboard-deadline-event">{e.event}</div>
                  <div className="dashboard-deadline-matter">Matter {e.matters}</div>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* Cluster Breakdown */}
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
                <span style={{ color: cl.color }}>{clusterCounts[cl.n]} matters</span>
              </div>
              <div className="dashboard-cluster-meta">Matters {clusterMattersStr[cl.n]}</div>
              <div className="dashboard-cluster-track">
                <div className="dashboard-cluster-bar" style={{ width: `${(clusterCounts[cl.n] / totalMatters) * 100}%`, background: cl.color }} />
              </div>
            </button>
          ))}
          <div className="dashboard-cluster-hint">Click a cluster to filter matters →</div>

          {/* Pertinent Filings */}
          <div className="dashboard-filings">
            <h4 className="dashboard-subheading">Pertinent Filings</h4>
            <div className="dashboard-filing-list">
              {PERTINENT_FILINGS.map((f, i) => {
                const dateColor = f.dateStatus === "upcoming" ? UPCOMING_AMBER : FILED_GREEN;
                return (
                  <div key={i} className="dashboard-filing">
                    <span className="dashboard-filing-title">
                      {f.title}
                      {f.note && (
                        <span className="dashboard-filing-note">{f.note}</span>
                      )}
                    </span>
                    <div className="dashboard-filing-meta">
                      <span className="dashboard-matter-badge">Matter {f.matter}</span>
                      {f.date && (
                        <span className="dashboard-filing-date" style={{ color: dateColor }}>{f.date}</span>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
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

      {/* Courts Overview */}
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
  );
};
