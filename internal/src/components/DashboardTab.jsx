import { PORTFOLIO } from "../data";
import { GOLD, BORDER_BLUE } from "../constants";
import { useTheme } from "../ThemeContext";

const FILED_GREEN = "#34D399";
const UPCOMING_AMBER = "#FBBF24";

const formatCurrency = (n) => "$" + n.toLocaleString();

const totalMatters = PORTFOLIO.cases.length;
const activeMatters = PORTFOLIO.cases.filter(c => !c.archived).length;
const clusterCounts = { 1: 0, 2: 0, 3: 0, 4: 0, 5: 0 };
const clusterNumberLists = { 1: [], 2: [], 3: [], 4: [], 5: [] };
const courtCounts = {};
let federalCount = 0;
let stateCount = 0;
for (const c of PORTFOLIO.cases) {
  if (!c.archived) {
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
  PORTFOLIO.damages_table.reduce((s, r) => s + r.moderate, 0)
);

const CLUSTERS = [
  { n: 1, label: "CHP Traffic Stop, DUI Arrest & DMV", color: "#60A5FA" },
  { n: 2, label: "Parole Retaliation, HOPE Abuse & Policy 19-03", color: "#A78BFA" },
  { n: 3, label: "Employment Violations", color: "#FBBF24" },
  { n: 4, label: "Administrative Writs & Habeas Corpus", color: "#34D399" },
  { n: 5, label: "Consumer Fraud / Defective Vehicle", color: "#F97316" },
];

const PERTINENT_FILINGS = [
  { title: "Newanforbi v. CDCR, et al.", matter: 15, date: "Filed May 13, 2026", dateStatus: "filed" },
  { title: "Newanforbi v. Serrato et al.", matter: 24, date: "Filed Jun 17, 2026", dateStatus: "filed" },
  { title: "Newanforbi v. Federal Express Corporation", matter: 25, date: "Filed Jul 15, 2026", dateStatus: "filed" },
  { title: "Newanforbi v. United Parcel Service, Inc.", matter: 26, date: "Filed Jul 15, 2026", dateStatus: "filed" },
  { title: "Newanforbi v. Randstad, et al.", matter: 27, note: "Case No. 26CV199902 — RK Logistics Denied Jul 21", date: "Filed Jul 20, 2026", dateStatus: "filed" },
  { title: "Newanforbi v. Shannon Smith, LCSW, et al.", matter: 28, note: "Matter 5 Successor — HOPE / Palacios", date: "Mailed Jul 16, 2026", dateStatus: "filed" },
  { title: "Newanforbi v. Amazon.com Services, LLC", matter: 29, date: "Pre-Complaint — BGC Pending", dateStatus: "upcoming" },
  { title: "Newanforbi v. Moua, et al.", matter: 30, date: "Anticipated Sep 16, 2026", dateStatus: "upcoming" },
];

export const DashboardTab = ({ upcomingEvents, setClusterFilter, setActiveTab }) => {
  const theme = useTheme();
  return (
    <div>
      {/* Stats Row */}
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))", gap: 16, marginBottom: 28 }}>
        {[
          { label: "Active Matters", value: activeMatters, sub: `${federalCount} Federal · ${stateCount} State · ${totalMatters} total` },
          { label: "Jurisdictions", value: PORTFOLIO.jurisdictions.length, sub: "Courts across CA" },
          { label: "Aggregate Exposure", value: moderateExposure, sub: "Moderate estimate" },
          { label: "Next Deadline", value: upcomingEvents[0]?.date || "—", sub: upcomingEvents[0]?.event?.slice(0, 35) || "" }
        ].map((s, i) => (
          <div key={i} style={{ background: theme.cardBg, borderRadius: 10, padding: "20px 22px", border: `1px solid ${theme.cardBorder}`, position: "relative", overflow: "hidden" }}>
            <div style={{ position: "absolute", top: 0, left: 0, width: 3, height: "100%", background: GOLD, borderRadius: "10px 0 0 10px" }} />
            <div style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 11, color: theme.subtleText, fontWeight: 600, letterSpacing: 1.5, textTransform: "uppercase", marginBottom: 8 }}>{s.label}</div>
            <div style={{ fontSize: 28, fontWeight: 700, color: theme.heading }}>{s.value}</div>
            <div style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 11, color: theme.subtleText, marginTop: 4 }}>{s.sub}</div>
          </div>
        ))}
      </div>

      {/* Two-column: Upcoming + Clusters */}
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 20, marginBottom: 28 }}>
        {/* Upcoming */}
        <div style={{ background: theme.cardBg, borderRadius: 10, padding: 24, border: `1px solid ${theme.cardBorder}` }}>
          <h3 style={{ fontSize: 18, fontWeight: 700, color: GOLD, margin: "0 0 16px", fontFamily: "'DM Sans', sans-serif", letterSpacing: 0.5 }}>Upcoming Deadlines</h3>
          <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
            {upcomingEvents.map((e, i) => (
              <div key={i} style={{ display: "flex", gap: 14, alignItems: "flex-start" }}>
                <div style={{ minWidth: 90, fontFamily: "'DM Sans', sans-serif", fontSize: 12, fontWeight: 700, color: "#F472B6", paddingTop: 2 }}>{e.date}</div>
                <div>
                  <div style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 13, color: theme.secondaryText }}>{e.event}</div>
                  <div style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 11, color: theme.subtleText, marginTop: 2 }}>Matter {e.matters}</div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Cluster Breakdown */}
        <div style={{ background: theme.cardBg, borderRadius: 10, padding: 24, border: `1px solid ${theme.cardBorder}` }}>
          <h3 style={{ fontSize: 18, fontWeight: 700, color: GOLD, margin: "0 0 16px", fontFamily: "'DM Sans', sans-serif", letterSpacing: 0.5 }}>Case Clusters</h3>
          {CLUSTERS.map(cl => (
            <div
              key={cl.n}
              role="button"
              tabIndex={0}
              style={{ marginBottom: 16, cursor: "pointer" }}
              onClick={() => { setClusterFilter(cl.n); setActiveTab("Matters"); }}
              onKeyDown={e => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); setClusterFilter(cl.n); setActiveTab("Matters"); } }}
              aria-label={`Filter matters by cluster: ${cl.label}`}
            >
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 4 }}>
                <span style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 13, fontWeight: 600, color: theme.secondaryText }}>{cl.label}</span>
                <span style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 12, color: cl.color, fontWeight: 700 }}>{clusterCounts[cl.n]} matters</span>
              </div>
              <div style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 10, color: theme.subtleText, marginBottom: 6 }}>Matters {clusterMattersStr[cl.n]}</div>
              <div style={{ height: 6, background: theme.barTrack, borderRadius: 3, overflow: "hidden" }}>
                <div style={{ height: "100%", width: `${(clusterCounts[cl.n] / totalMatters) * 100}%`, background: cl.color, borderRadius: 3, transition: "width 0.6s ease" }} />
              </div>
            </div>
          ))}
          <div style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 11, color: theme.subtleText, marginTop: 12, fontStyle: "italic" }}>Click a cluster to filter matters →</div>

          {/* Pertinent Filings */}
          <div style={{ marginTop: 24, borderTop: `1px solid ${theme.cardBorder}`, paddingTop: 16 }}>
            <h4 style={{ fontSize: 13, fontWeight: 700, color: GOLD, margin: "0 0 12px", fontFamily: "'DM Sans', sans-serif", letterSpacing: 0.5, textTransform: "uppercase" }}>Pertinent Filings</h4>
            <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
              {PERTINENT_FILINGS.map((f, i) => {
                const dateColor = f.dateStatus === "upcoming" ? UPCOMING_AMBER : FILED_GREEN;
                return (
                  <div key={i} style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "8px 12px", background: theme.deepBg, borderRadius: 6, border: `1px solid ${BORDER_BLUE}25`, gap: 12 }}>
                    <span style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 12, fontWeight: 600, color: theme.secondaryText }}>
                      {f.title}
                      {f.note && (
                        <span style={{ display: "block", fontSize: 10, fontWeight: 500, color: theme.subtleText, marginTop: 1 }}>{f.note}</span>
                      )}
                    </span>
                    <div style={{ display: "flex", flexDirection: "column", alignItems: "flex-end", gap: 3, flexShrink: 0 }}>
                      <span style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 11, fontWeight: 700, color: theme.badgeNumColor, background: theme.badgeNumBg, borderRadius: 4, padding: "2px 8px" }}>Matter {f.matter}</span>
                      {f.date && (
                        <span style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 9.5, fontWeight: 600, color: dateColor, whiteSpace: "nowrap" }}>{f.date}</span>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      </div>

      {/* Milestone: First Settlement */}
      <div style={{ background: `linear-gradient(135deg, ${GOLD}15, ${GOLD}08)`, borderRadius: 10, padding: 24, border: `2px solid ${GOLD}40`, marginBottom: 16 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
          <div style={{ fontSize: 32, lineHeight: 1 }}>💰</div>
          <div>
            <h3 style={{ fontSize: 18, fontWeight: 700, color: GOLD, margin: "0 0 6px", fontFamily: "'DM Sans', sans-serif", letterSpacing: 0.5 }}>First Case to Settle</h3>
            <p style={{ margin: 0, fontFamily: "'DM Sans', sans-serif", fontSize: 13, color: theme.secondaryText, lineHeight: 1.4 }}>
              Matter 22 became the first matter in this portfolio to reach a negotiated settlement — resolved pro se, without counsel, in under seven weeks from filing.
            </p>
          </div>
        </div>
      </div>

      {/* Milestone: First Interstate Case */}
      <div style={{ background: `linear-gradient(135deg, ${GOLD}15, ${GOLD}08)`, borderRadius: 10, padding: 24, border: `2px solid ${GOLD}40`, marginBottom: 28 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
          <div style={{ fontSize: 32, lineHeight: 1 }}>🌎</div>
          <div>
            <h3 style={{ fontSize: 18, fontWeight: 700, color: GOLD, margin: "0 0 6px", fontFamily: "'DM Sans', sans-serif", letterSpacing: 0.5 }}>First Interstate Reaching Case</h3>
            <p style={{ margin: 0, fontFamily: "'DM Sans', sans-serif", fontSize: 13, color: theme.secondaryText, lineHeight: 1.4 }}>
              Matter 22 represents the first litigation matter with interstate service of process. Demand letter sent via Certified Mail to corporate headquarters in Tennessee.
            </p>
          </div>
        </div>
      </div>

      {/* Courts Overview */}
      <div style={{ background: theme.cardBg, borderRadius: 10, padding: 24, border: `1px solid ${theme.cardBorder}` }}>
        <h3 style={{ fontSize: 18, fontWeight: 700, color: GOLD, margin: "0 0 16px", fontFamily: "'DM Sans', sans-serif" }}>Jurisdictional Distribution</h3>
        <div style={{ display: "flex", flexWrap: "wrap", gap: 10 }}>
          {PORTFOLIO.jurisdictions.map(j => (
            <div key={j} style={{ background: theme.navySubtleBg, borderRadius: 8, padding: "12px 18px", border: `1px solid ${BORDER_BLUE}30`, flex: "1 1 180px" }}>
              <div style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 12, color: theme.mutedText, marginBottom: 4 }}>{j}</div>
              <div style={{ fontSize: 24, fontWeight: 700, color: theme.heading }}>{courtCounts[j] || 0}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
