import { useState } from "react";
import { PORTFOLIO } from "../data";
import { GOLD } from "../constants";
import { useTheme } from "../ThemeContext";
import { getPDTMidnight } from "../utils/dateUtils";
import { CLUSTERS } from "./DashboardTab";

const fmt = (n) => "$" + Math.round(n).toLocaleString();

// ---- Status badge → label/color, reusing the exact ribbon colors MattersTab uses ----
const BADGE_LABEL = {
  DEFAULT: "Default judgment sought",
  DISMISSED: "Dismissed",
  ABANDONED: "Abandoned",
  DENIED: "Denied",
  PENDING: "Pending",
  TIMELY: "Timely",
  SERVED: "Served",
};
const STATUS_COLORS = {
  "Live": GOLD,
  "Settled": "#34D399",
  "Served": "#0d9488",
  "Timely": "#0284c7",
  "Default judgment sought": "#16a34a",
  "Denied": "#6b7280",
  "Dismissed": "#dc2626",
  "Abandoned": "#94A3B8",
  "Pending": "#eab308",
};
const STATUS_ORDER = ["Live", "Settled", "Abandoned", "Dismissed", "Denied", "Default judgment sought", "Served", "Timely", "Pending"];

// Settlement isn't tracked as a `badge` field — matters.js marks it with a
// "SETTLED" prefix on `status` instead (the same signal MattersTab's ribbon uses).
const statusLabelOf = (c) => {
  if (c.status?.startsWith("SETTLED")) return "Settled";
  if (c.badge) return BADGE_LABEL[c.badge] || c.badge;
  return "Live";
};

const MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
const MONTH_INDEX = { Jan: 0, Feb: 1, Mar: 2, Apr: 3, May: 4, Jun: 5, Jul: 6, Aug: 7, Sep: 8, Oct: 9, Nov: 10, Dec: 11 };
const monthYearOf = (dateStr) => {
  const yearMatch = dateStr.match(/(\d{4})/);
  const monthMatch = dateStr.match(/^([A-Za-z]{3})/);
  if (!yearMatch) return null;
  const month = monthMatch && MONTH_INDEX[monthMatch[1]] !== undefined ? MONTH_INDEX[monthMatch[1]] : null;
  return { year: +yearMatch[1], month };
};

// ---- Live-computed aggregates (module scope — same pattern as DashboardTab) ----
const totalMatters = PORTFOLIO.cases.length;
const liveMatters = PORTFOLIO.cases.filter(c => !c.archived).length;
const archivedMatters = totalMatters - liveMatters;
// Strip "TBD — anticipated X" placeholder text (Matter 30) down to the actual
// court name, so an anticipated filing doesn't inflate the distinct-court count.
const courtName = (c) => c.replace(/^TBD\s*—\s*anticipated\s*/i, "").trim();
const distinctCourts = new Set(PORTFOLIO.cases.map(c => courtName(c.court))).size;

const judgeName = (j) => j.split(/[,/(]/)[0].trim();
const distinctJudges = new Set(
  PORTFOLIO.cases.filter(c => c.judge?.startsWith("Hon.")).map(c => judgeName(c.judge))
).size;
const assignedMatters = PORTFOLIO.cases.filter(c => c.judge?.startsWith("Hon.")).length;

const totalDocuments = PORTFOLIO.cases.reduce((s, c) => s + (c.documents?.length || 0), 0);
const totalEvidence = PORTFOLIO.cases.reduce((s, c) => s + (c.evidence?.length || 0), 0);
const totalCauses = PORTFOLIO.cases.reduce((s, c) => s + (c.causes?.length || 0), 0);

const statusCounts = {};
for (const c of PORTFOLIO.cases) {
  const label = statusLabelOf(c);
  statusCounts[label] = (statusCounts[label] || 0) + 1;
}
const statusRows = STATUS_ORDER
  .filter(s => statusCounts[s])
  .map(s => ({ label: s, count: statusCounts[s], color: STATUS_COLORS[s] || GOLD }));
const maxStatus = Math.max(...statusRows.map(r => r.count));

const clusterCounts = {};
for (const c of PORTFOLIO.cases) clusterCounts[c.cluster] = (clusterCounts[c.cluster] || 0) + 1;
const clusterRows = CLUSTERS
  .map(cl => ({ ...cl, count: clusterCounts[cl.n] || 0 }))
  .sort((a, b) => b.count - a.count);
const maxCluster = Math.max(...clusterRows.map(r => r.count));

const monthlyAll = Array(12).fill(0);
const monthlyFilings = Array(12).fill(0);
let filingSpanMin = null, filingSpanMax = null;
for (const t of PORTFOLIO.timeline) {
  const my = monthYearOf(t.date);
  if (!my) continue;
  if (t.type === "filing") {
    const key = my.year * 12 + (my.month ?? 0);
    if (filingSpanMin === null || key < filingSpanMin) filingSpanMin = key;
    if (filingSpanMax === null || key > filingSpanMax) filingSpanMax = key;
  }
  if (my.year === 2026 && my.month !== null) {
    monthlyAll[my.month]++;
    if (t.type === "filing") monthlyFilings[my.month]++;
  }
}
const busiestMonthIdx = monthlyAll.indexOf(Math.max(...monthlyAll));
const filingSpanLabel = filingSpanMin !== null
  ? `${MONTHS[filingSpanMin % 12]} ${Math.floor(filingSpanMin / 12)} – ${MONTHS[filingSpanMax % 12]} ${Math.floor(filingSpanMax / 12)}`
  : "—";

const exposure = PORTFOLIO.outcomes.portfolio_exposure;
const settledDeals = PORTFOLIO.outcomes.realized.filter(r => r.type === "settlement");
const settledTotal = settledDeals.reduce((s, r) => s + r.amount, 0);
const demandsTotal = PORTFOLIO.outcomes.active_demands.reduce((s, d) => s + d.demand_amount, 0);
const demandsResponded = PORTFOLIO.outcomes.active_demands.filter(
  d => d.response_status !== "no response" && d.response_status !== "pending"
).length;

const feeSummary = PORTFOLIO.lawyer_fees_summary;
const feeClusters = Object.values(feeSummary.byCluster);
const maxFeeCost = Math.max(...feeClusters.map(c => c.costHigh));

const casesByNumber = Object.fromEntries(PORTFOLIO.cases.map(c => [c.number, c]));

const thStyle = (theme) => ({
  fontFamily: "'DM Sans', sans-serif", fontSize: 10, fontWeight: 700,
  color: theme.subtleText, textTransform: "uppercase", letterSpacing: 1,
  padding: "0 10px 8px 0", whiteSpace: "nowrap",
});
const tdStyle = (theme) => ({
  fontFamily: "'DM Sans', sans-serif", fontSize: 12,
  padding: "9px 10px 9px 0", borderTop: `1px solid ${theme.cardBorder}`,
});

function StatTile({ label, value, sub, theme }) {
  return (
    <div style={{ background: theme.cardBg, borderRadius: 10, padding: "18px 20px", border: `1px solid ${theme.cardBorder}`, position: "relative", overflow: "hidden" }}>
      <div style={{ position: "absolute", top: 0, left: 0, width: 3, height: "100%", background: GOLD, borderRadius: "10px 0 0 10px" }} />
      <div style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 10.5, color: theme.subtleText, fontWeight: 600, letterSpacing: 1.2, textTransform: "uppercase", marginBottom: 8 }}>{label}</div>
      <div style={{ fontSize: 24, fontWeight: 700, color: theme.heading }}>{value}</div>
      {sub && <div style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 11, color: theme.subtleText, marginTop: 4 }}>{sub}</div>}
    </div>
  );
}

function Bar({ pct, color, theme, height = 7 }) {
  return (
    <div style={{ height, background: theme.barTrack, borderRadius: height / 2, overflow: "hidden" }}>
      <div style={{ height: "100%", width: `${pct}%`, background: color, borderRadius: height / 2, transition: "width 0.6s ease" }} />
    </div>
  );
}

export const CensusTab = ({ setActiveTab, setClusterFilter, setStatusFilter, setSearchQuery, damagesView, setDamagesView, setShowPastEvents }) => {
  const theme = useTheme();
  const [velocityMode, setVelocityMode] = useState("all");
  const monthly = velocityMode === "all" ? monthlyAll : monthlyFilings;
  const maxMonthly = Math.max(...monthly, 1);
  const today = getPDTMidnight();
  const todayMonthIdx = today.getUTCFullYear() === 2026 ? today.getUTCMonth() : null;

  // Always set every filter explicitly (never leave a stale cluster/search from a
  // previous drill-through in place) so each click lands on exactly what it promised.
  const goToMatters = (opts = {}) => {
    setStatusFilter?.("all");
    setClusterFilter?.(opts.cluster ?? null);
    setSearchQuery?.(opts.search ?? "");
    setActiveTab("Matters");
  };

  return (
    <div>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline", marginBottom: 6, flexWrap: "wrap", gap: 8 }}>
        <h2 style={{ fontSize: 24, fontWeight: 700, color: theme.heading, margin: 0 }}>Portfolio Census</h2>
        <span style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 11, color: theme.subtleText }}>Curated figures as of {PORTFOLIO.census.asOf} · everything else computed live</span>
      </div>
      <p style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 13, color: theme.subtleText, maxWidth: 760, margin: "0 0 24px", lineHeight: 1.6 }}>
        A statistical accounting of the entire docket — scale, pace, legal theories, and financial exposure — in one place. Click any bar or row to jump to the underlying matters.
      </p>

      {/* KPI grid */}
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(190px, 1fr))", gap: 14, marginBottom: 28 }}>
        <StatTile theme={theme} label="Matters Tracked" value={totalMatters} sub={`${liveMatters} live · ${archivedMatters} closed/archived`} />
        <StatTile theme={theme} label="Active Filing Span" value={filingSpanLabel} sub="earliest → latest complaint filed" />
        <StatTile theme={theme} label="Court Systems" value={distinctCourts} sub={`${PORTFOLIO.jurisdictions.length} jurisdictions listed`} />
        <StatTile theme={theme} label="Judicial Officers" value={distinctJudges} sub={`assigned in ${assignedMatters} of ${totalMatters} matters`} />
        <StatTile theme={theme} label="Named Defendants" value={PORTFOLIO.census.namedDefendants} sub={`~${PORTFOLIO.census.namedInstitutions} institutions, DOES excluded`} />
        <StatTile theme={theme} label="Causes of Action" value={totalCauses} sub={`${PORTFOLIO.census.distinctTheories} distinct theories`} />
        <StatTile theme={theme} label="Documents + Evidence" value={(totalDocuments + totalEvidence).toLocaleString()} sub={`${totalDocuments} docs · ${totalEvidence} evidence items logged`} />
        <StatTile theme={theme} label="Fee Waivers" value={PORTFOLIO.census.feeWaiversGranted} sub={`granted · ${PORTFOLIO.census.feeWaiversDenied} denied`} />
      </div>

      {/* Status + Cluster */}
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 20, marginBottom: 24 }}>
        <div style={{ background: theme.cardBg, borderRadius: 10, padding: 24, border: `1px solid ${theme.cardBorder}` }}>
          <h3 style={{ fontSize: 16, fontWeight: 700, color: GOLD, margin: "0 0 4px", fontFamily: "'DM Sans', sans-serif", letterSpacing: 0.5 }}>Docket Status</h3>
          <div style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 11, color: theme.subtleText, marginBottom: 16 }}>{totalMatters} matters, by current procedural status</div>
          {statusRows.map(r => (
            <div
              key={r.label} role="button" tabIndex={0}
              onClick={() => goToMatters()}
              onKeyDown={e => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); goToMatters(); } }}
              aria-label={`View matters — status: ${r.label}`}
              style={{ marginBottom: 14, cursor: "pointer" }}
            >
              <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 5 }}>
                <span style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 12.5, fontWeight: 600, color: theme.secondaryText }}>{r.label}</span>
                <span style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 12, color: r.color, fontWeight: 700 }}>{r.count}</span>
              </div>
              <Bar pct={(r.count / maxStatus) * 100} color={r.color} theme={theme} />
            </div>
          ))}
          <div style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 11, color: theme.subtleText, marginTop: 4, fontStyle: "italic" }}>Click a status to open Matters →</div>
        </div>

        <div style={{ background: theme.cardBg, borderRadius: 10, padding: 24, border: `1px solid ${theme.cardBorder}` }}>
          <h3 style={{ fontSize: 16, fontWeight: 700, color: GOLD, margin: "0 0 4px", fontFamily: "'DM Sans', sans-serif", letterSpacing: 0.5 }}>Subject-Matter Clusters</h3>
          <div style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 11, color: theme.subtleText, marginBottom: 16 }}>Five recurring fact patterns account for the whole docket</div>
          {clusterRows.map(cl => (
            <div
              key={cl.n} role="button" tabIndex={0}
              onClick={() => goToMatters({ cluster: cl.n })}
              onKeyDown={e => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); goToMatters({ cluster: cl.n }); } }}
              aria-label={`Filter matters by cluster: ${cl.label}`}
              style={{ marginBottom: 14, cursor: "pointer" }}
            >
              <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 5 }}>
                <span style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 12.5, fontWeight: 600, color: theme.secondaryText }}>{cl.label}</span>
                <span style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 12, color: cl.color, fontWeight: 700 }}>{cl.count}</span>
              </div>
              <Bar pct={(cl.count / maxCluster) * 100} color={cl.color} theme={theme} />
            </div>
          ))}
          <div style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 11, color: theme.subtleText, marginTop: 4, fontStyle: "italic" }}>Click a cluster to open Matters →</div>
        </div>
      </div>

      {/* Filing velocity */}
      <div style={{ background: theme.cardBg, borderRadius: 10, padding: 24, border: `1px solid ${theme.cardBorder}`, marginBottom: 24 }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", flexWrap: "wrap", gap: 12, marginBottom: 4 }}>
          <h3 style={{ fontSize: 16, fontWeight: 700, color: GOLD, margin: 0, fontFamily: "'DM Sans', sans-serif", letterSpacing: 0.5 }}>Filing Velocity, 2026</h3>
          <div style={{ display: "flex", gap: 6 }}>
            {[{ k: "all", l: "All Events" }, { k: "filing", l: "Filings Only" }].map(({ k, l }) => (
              <button key={k} onClick={() => setVelocityMode(k)} aria-pressed={velocityMode === k} style={{
                padding: "6px 12px", borderRadius: 6,
                border: velocityMode === k ? `1px solid ${GOLD}` : `1px solid ${theme.filterInactiveBorder}`,
                background: velocityMode === k ? `${GOLD}18` : theme.filterInactiveBg,
                color: velocityMode === k ? GOLD : theme.filterInactiveColor,
                fontFamily: "'DM Sans', sans-serif", fontSize: 11, fontWeight: 600, cursor: "pointer",
              }}>{l}</button>
            ))}
          </div>
        </div>
        <div style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 11, color: theme.subtleText, marginBottom: 18 }}>
          Busiest month: <strong style={{ color: theme.secondaryText }}>{MONTHS[busiestMonthIdx]} 2026</strong> ({monthlyAll[busiestMonthIdx]} logged events) · click a bar to open Timeline
        </div>
        <div style={{ display: "flex", alignItems: "flex-end", gap: 8, height: 140 }}>
          {monthly.map((v, i) => {
            const isPast = todayMonthIdx === null ? true : i <= todayMonthIdx;
            const isToday = i === todayMonthIdx;
            return (
              <div
                key={i} role="button" tabIndex={0}
                onClick={() => { setShowPastEvents?.(isPast); setActiveTab("Timeline"); }}
                onKeyDown={e => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); setShowPastEvents?.(isPast); setActiveTab("Timeline"); } }}
                aria-label={`${MONTHS[i]} 2026: ${v} ${velocityMode === "all" ? "events" : "filings"}`}
                style={{ flex: 1, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "flex-end", height: "100%", cursor: "pointer" }}
              >
                <div style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 10, fontWeight: 700, color: theme.subtleText, marginBottom: 3, visibility: v ? "visible" : "hidden" }}>{v}</div>
                <div style={{
                  width: "100%", height: `${Math.max((v / maxMonthly) * 100, v > 0 ? 4 : 1)}%`,
                  background: isToday ? GOLD : `linear-gradient(180deg, ${GOLD}, #34D399)`,
                  opacity: isPast ? 1 : 0.4,
                  borderRadius: "4px 4px 0 0", transition: "height 0.5s ease", minHeight: 2,
                }} />
                <div style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 10.5, color: isToday ? GOLD : theme.subtleText, fontWeight: isToday ? 700 : 500, marginTop: 6 }}>{MONTHS[i]}</div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Top theories */}
      <div style={{ background: theme.cardBg, borderRadius: 10, padding: 24, border: `1px solid ${theme.cardBorder}`, marginBottom: 24 }}>
        <h3 style={{ fontSize: 16, fontWeight: 700, color: GOLD, margin: "0 0 4px", fontFamily: "'DM Sans', sans-serif", letterSpacing: 0.5 }}>Most-Asserted Legal Theories</h3>
        <div style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 11, color: theme.subtleText, marginBottom: 16 }}>
          {totalCauses} causes of action pled across {totalMatters} matters, {PORTFOLIO.census.distinctTheories} distinct theories — top {PORTFOLIO.census.topTheories.length} shown
        </div>
        {PORTFOLIO.census.topTheories.map(t => (
          <div key={t.label} style={{ marginBottom: 10 }}>
            <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 4 }}>
              <span style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 12.5, color: theme.secondaryText }}>{t.label}</span>
              <span style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 12, color: GOLD, fontWeight: 700 }}>{t.count}</span>
            </div>
            <Bar pct={(t.count / PORTFOLIO.census.topTheories[0].count) * 100} color={GOLD} theme={theme} height={6} />
          </div>
        ))}
      </div>

      {/* The repeatable claim */}
      <div style={{ background: theme.cardBg, borderRadius: 10, padding: 24, border: `1px solid ${theme.cardBorder}`, marginBottom: 24 }}>
        <h3 style={{ fontSize: 16, fontWeight: 700, color: GOLD, margin: "0 0 4px", fontFamily: "'DM Sans', sans-serif", letterSpacing: 0.5 }}>The Repeatable Claim: PC §290.46(j)(2)(E)</h3>
        <div style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 11, color: theme.subtleText, marginBottom: 16, maxWidth: 700, lineHeight: 1.6 }}>
          One statute — barring use of the sex-offender registry in employment decisions — applied to six separate employers after the first produced a settlement. Click a row to open that matter.
        </div>
        <div style={{ overflowX: "auto" }}>
          <table style={{ width: "100%", borderCollapse: "collapse" }}>
            <thead>
              <tr>
                <th style={{ ...thStyle(theme), textAlign: "left" }}>Matter</th>
                <th style={{ ...thStyle(theme), textAlign: "left" }}>Employer</th>
                <th style={{ ...thStyle(theme), textAlign: "left" }}>Screening Vendor</th>
                <th style={{ ...thStyle(theme), textAlign: "left" }}>Status</th>
              </tr>
            </thead>
            <tbody>
              {PORTFOLIO.census.registryBarEmployers.map(({ matter, vendor }) => {
                const c = casesByNumber[matter];
                if (!c) return null;
                const statusLabel = statusLabelOf(c);
                const statusColor = STATUS_COLORS[statusLabel] || theme.subtleText;
                return (
                  <tr
                    key={matter} role="button" tabIndex={0}
                    onClick={() => goToMatters({ search: c.caption.replace(/^Newanforbi v\.\s*/, "") })}
                    onKeyDown={e => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); goToMatters({ search: c.caption.replace(/^Newanforbi v\.\s*/, "") }); } }}
                    style={{ cursor: "pointer" }}
                  >
                    <td style={tdStyle(theme)}><span style={{ color: GOLD, fontWeight: 700 }}>M{matter}</span></td>
                    <td style={{ ...tdStyle(theme), color: theme.secondaryText }}>{c.caption.replace(/^Newanforbi v\.\s*/, "")}</td>
                    <td style={{ ...tdStyle(theme), color: theme.subtleText }}>{vendor}</td>
                    <td style={{ ...tdStyle(theme), color: statusColor, fontWeight: 600 }}>{statusLabel}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>

      {/* Financial exposure */}
      <div style={{ background: theme.cardBg, borderRadius: 10, padding: 24, border: `1px solid ${theme.cardBorder}`, marginBottom: 24 }}>
        <h3 style={{ fontSize: 16, fontWeight: 700, color: GOLD, margin: "0 0 4px", fontFamily: "'DM Sans', sans-serif", letterSpacing: 0.5 }}>Financial Exposure</h3>
        <div style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 11, color: theme.subtleText, marginBottom: 16 }}>De-duplicated across the whole portfolio — shared economic events counted once</div>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 12, marginBottom: 18 }}>
          {["conservative", "moderate", "aggressive"].map(v => {
            const isActive = v === damagesView;
            return (
              <button key={v} onClick={() => setDamagesView?.(v)} aria-pressed={isActive} style={{
                background: isActive ? theme.damagesActiveBg : theme.damagesInactiveBg,
                borderRadius: 8, padding: "14px 16px",
                border: isActive ? `1px solid ${GOLD}40` : `1px solid ${theme.cardBorder}`,
                cursor: "pointer", textAlign: "center", color: "inherit", font: "inherit", transition: "all 0.2s",
              }}>
                <div style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 10, color: isActive ? GOLD : theme.subtleText, fontWeight: 700, letterSpacing: 1, textTransform: "uppercase", marginBottom: 6 }}>{v}</div>
                <div style={{ fontSize: 22, fontWeight: 700, color: isActive ? theme.aggregateCardText : theme.mutedText }}>{fmt(exposure[v])}{v === "aggressive" && "+"}</div>
              </button>
            );
          })}
        </div>
        <div style={{ display: "flex", justifyContent: "flex-end", marginBottom: 18 }}>
          <button onClick={() => setActiveTab("Damages")} style={{
            background: "none", border: `1px solid ${theme.cardBorder}`, borderRadius: 6, padding: "6px 12px",
            color: GOLD, fontFamily: "'DM Sans', sans-serif", fontSize: 11, fontWeight: 600, cursor: "pointer",
          }}>Full breakdown →</button>
        </div>
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 14 }}>
          <div style={{ background: theme.deepBg, borderRadius: 8, padding: "14px 16px" }}>
            <div style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 9, fontWeight: 700, color: "#34D399", letterSpacing: 1.5, textTransform: "uppercase", marginBottom: 6 }}>Realized</div>
            <div style={{ fontSize: 20, fontWeight: 700, color: theme.heading }}>{fmt(settledTotal)}</div>
            <div style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 11, color: theme.subtleText, marginTop: 3 }}>{settledDeals.length} settlement{settledDeals.length !== 1 ? "s" : ""} to date</div>
          </div>
          <div style={{ background: theme.deepBg, borderRadius: 8, padding: "14px 16px" }}>
            <div style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 9, fontWeight: 700, color: GOLD, letterSpacing: 1.5, textTransform: "uppercase", marginBottom: 6 }}>Outstanding Demands</div>
            <div style={{ fontSize: 20, fontWeight: 700, color: theme.heading }}>{fmt(demandsTotal)}</div>
            <div style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 11, color: theme.subtleText, marginTop: 3 }}>{demandsResponded} of {PORTFOLIO.outcomes.active_demands.length} defendants responded</div>
          </div>
        </div>
      </div>

      {/* Fee value avoided */}
      <div style={{ background: theme.aggregateCardBg, borderRadius: 10, padding: 24, border: `1px solid ${GOLD}30` }}>
        <h3 style={{ fontSize: 16, fontWeight: 700, color: GOLD, margin: "0 0 4px", fontFamily: "'DM Sans', sans-serif", letterSpacing: 0.5 }}>Value of the Work Itself</h3>
        <div style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 11, color: theme.subtleText, marginBottom: 16 }}>
          {feeSummary.totalDocumentsAnalyzed} real PDFs, {feeSummary.totalPagesReal.toLocaleString()} pages, priced at a blended ${feeSummary.methodology.blendedHourlyRate}/hr had counsel been retained
        </div>
        <div style={{ fontSize: 34, fontWeight: 700, color: theme.aggregateCardText, marginBottom: 4 }}>
          {fmt(feeSummary.totalEstimatedCost.low)}–{fmt(feeSummary.totalEstimatedCost.high)}
        </div>
        <div style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 11, color: theme.subtleText, marginBottom: 18 }}>
          ~{feeSummary.totalEstimatedHours.low.toLocaleString()}–{feeSummary.totalEstimatedHours.high.toLocaleString()} hours of attorney work, delivered pro se
        </div>
        <div style={{ display: "flex", flexDirection: "column", gap: 10, marginBottom: 14 }}>
          {feeClusters.map(c => (
            <div key={c.label}>
              <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 4 }}>
                <span style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 12.5, color: theme.secondaryText }}>{c.label}</span>
                <span style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 12, color: "#34D399", fontWeight: 700 }}>{fmt(c.costLow)}–{fmt(c.costHigh)}</span>
              </div>
              <Bar pct={(c.costHigh / maxFeeCost) * 100} color="#34D399" theme={theme} height={6} />
            </div>
          ))}
        </div>
        <div style={{ display: "flex", justifyContent: "flex-end" }}>
          <button onClick={() => setActiveTab("Cost of Counsel")} style={{
            background: "none", border: `1px solid ${GOLD}40`, borderRadius: 6, padding: "6px 12px",
            color: GOLD, fontFamily: "'DM Sans', sans-serif", fontSize: 11, fontWeight: 600, cursor: "pointer",
          }}>Full breakdown →</button>
        </div>
      </div>
    </div>
  );
};
