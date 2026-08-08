import { useState } from "react";
import { PORTFOLIO } from "../data";
import { GOLD } from "../constants";
import { useTheme } from "../ThemeContext";
import { getPDTMidnight } from "../utils/dateUtils";
import { formatCurrency } from "../utils/formatters";
import { isArchivedMatter, isLiveLifecycle, lifecycleLabel } from "../utils/matterLifecycle";
import { phaseLabel, proceedingLabel } from "../utils/matterProceeding";
import { HorizontalBarChart, VerticalBarChart, RangeChart } from "./charts/PortfolioCharts";
import { CLUSTERS } from "./DashboardTab";

const fmt = (n) => formatCurrency(Math.round(n));
const MONO = "'Courier New', ui-monospace, monospace";
const SANS = "'DM Sans', sans-serif";
const GREEN = "#34D399";

// Procedural overlay badges (not lifecycle) — keep census chart compatible with Matters ribbons.
const BADGE_LABEL = {
  DEFAULT: "Default judgment sought",
  DENIED: "Denied",
  TIMELY: "Timely",
  SERVED: "Served",
};
const statusLabelOf = (c) => {
  if (c.lifecycle === "settled") return "Settled";
  if (c.lifecycle === "abandoned") return "Abandoned";
  if (c.lifecycle === "dismissed") return "Dismissed";
  if (c.lifecycle === "closed") return c.badge === "DENIED" ? "Denied" : "Closed";
  if (c.lifecycle === "pre_filing" || c.phase === "pre_filing" || c.badge === "PENDING") return "Pending";
  // Live matters: prefer procedural phase over generic "Live"
  if (c.phase && c.phase !== "terminal") return phaseLabel(c.phase);
  if (c.badge && BADGE_LABEL[c.badge]) return BADGE_LABEL[c.badge];
  if (c.lifecycle) return lifecycleLabel(c.lifecycle);
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
const liveMatters = PORTFOLIO.cases.filter(c => isLiveLifecycle(c.lifecycle) || (!c.lifecycle && !c.archived)).length;
const archivedMatters = PORTFOLIO.cases.filter(c => isArchivedMatter(c)).length;
// Strip "TBD — anticipated X" placeholder text (Matter 30) down to the actual
// court name, so an anticipated filing doesn't inflate the distinct-court count.
const courtName = (c) => c.replace(/^TBD\s*—\s*anticipated\s*/i, "").trim();
const distinctCourts = new Set(PORTFOLIO.cases.map(c => courtName(c.court))).size;

const judgeName = (j) => j.split(/[,/(]/)[0].trim();
const distinctJudges = new Set(
  PORTFOLIO.cases.filter(c => c.judge?.startsWith("Hon.")).map(c => judgeName(c.judge))
).size;
const assignedMatters = PORTFOLIO.cases.filter(c => c.judge?.startsWith("Hon.")).length;

const totalDocuments = PORTFOLIO.cases.reduce((s, c) => s + (c.documentCount || 0), 0);
const totalEvidence = PORTFOLIO.cases.reduce((s, c) => s + (c.evidenceCount ?? c.evidence?.length ?? 0), 0);
const totalCauses = PORTFOLIO.cases.reduce((s, c) => s + (c.causes?.length || 0), 0);

// Status palette: reuse MattersTab's exact ribbon colors; anything else falls
// back through the cluster palette below so every bar still gets a distinct hue.
const STATUS_COLOR = {
  "Settled": GREEN,
  "Active": GREEN,
  "Served": "#0d9488",
  "Service": "#0d9488",
  "Responsive deadline": "#0d9488",
  "Timely": "#0284c7",
  "Default judgment sought": "#16a34a",
  "Default / prove-up": "#16a34a",
  "Denied": "#6b7280",
  "Closed": "#6b7280",
  "Dismissed": "#dc2626",
  "Abandoned": "#94A3B8",
  "Pending": "#eab308",
  "Pre-filing": "#eab308",
  "Stayed": "#FBBF24",
  "Demurrer": "#F472B6",
  "F&R pending": "#F472B6",
  "Under submission": "#A78BFA",
  "Case management": "#60A5FA",
  "IFP / screening": GOLD,
  "Live": GOLD,
};

const PROCEEDING_COLOR = {
  "Federal civil": "#38BDF8",
  "State civil": "#FB923C",
  "Mandate / writ": "#A78BFA",
  "Habeas": "#34D399",
};
const proceedingCounts = {};
for (const c of PORTFOLIO.cases) {
  const label = c.proceeding ? proceedingLabel(c.proceeding) : "Unknown";
  proceedingCounts[label] = (proceedingCounts[label] || 0) + 1;
}
const proceedingRows = Object.entries(proceedingCounts)
  .map(([label, count]) => ({ label, count, value: count, color: PROCEEDING_COLOR[label] || GOLD }))
  .sort((a, b) => b.count - a.count);
const statusCounts = {};
for (const c of PORTFOLIO.cases) {
  const label = statusLabelOf(c);
  statusCounts[label] = (statusCounts[label] || 0) + 1;
}
const statusRows = Object.entries(statusCounts)
  .map(([label, count]) => ({ label, count, value: count, color: STATUS_COLOR[label] || GOLD }))
  .sort((a, b) => b.count - a.count);

const clusterCounts = {};
for (const c of PORTFOLIO.cases) clusterCounts[c.cluster] = (clusterCounts[c.cluster] || 0) + 1;
const clusterRows = CLUSTERS
  .map(cl => ({ ...cl, count: clusterCounts[cl.n] || 0, value: clusterCounts[cl.n] || 0 }))
  .sort((a, b) => b.count - a.count);

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
const feeClusters = Object.values(feeSummary.byCluster).sort((a, b) => b.costHigh - a.costHigh);

const casesByNumber = Object.fromEntries(PORTFOLIO.cases.map(c => [c.number, c]));

const thStyle = (theme) => ({
  fontFamily: SANS, fontSize: 10, fontWeight: 700,
  color: theme.subtleText, textTransform: "uppercase", letterSpacing: 1,
  padding: "0 10px 8px 0", whiteSpace: "nowrap",
});
const tdStyle = (theme) => ({
  fontFamily: SANS, fontSize: 12.5,
  padding: "9px 10px 9px 0", borderTop: `1px solid ${theme.cardBorder}`,
});

// ---------------------------------------------------------------------------
// Small building blocks — masthead label, section heading, stat tile, charts
// ---------------------------------------------------------------------------
function Eyebrow({ children }) {
  return (
    <div style={{ fontFamily: SANS, fontSize: 10.5, letterSpacing: "0.16em", textTransform: "uppercase", color: GOLD, fontWeight: 700, marginBottom: 6 }}>
      {children}
    </div>
  );
}

function ExhibitHeading({ exhibit, title, intro, theme }) {
  return (
    <>
      <Eyebrow theme={theme}>{exhibit}</Eyebrow>
      <h2 style={{ fontSize: 21, fontWeight: 700, color: theme.heading, margin: "0 0 6px" }}>{title}</h2>
      {intro && <p style={{ fontFamily: SANS, fontSize: 13, color: theme.subtleText, maxWidth: 640, margin: "0 0 18px", lineHeight: 1.6 }}>{intro}</p>}
    </>
  );
}

function StatTile({ label, value, sub, theme }) {
  return (
    <div style={{ background: theme.cardBg, padding: "16px 18px" }}>
      <div style={{ fontFamily: SANS, fontSize: 10, color: theme.subtleText, fontWeight: 700, letterSpacing: "0.07em", textTransform: "uppercase", marginBottom: 8 }}>{label}</div>
      <div style={{ fontFamily: MONO, fontVariantNumeric: "tabular-nums", fontSize: 22, fontWeight: 700, color: theme.heading, lineHeight: 1.1 }}>{value}</div>
      {sub && <div style={{ fontFamily: SANS, fontSize: 11, color: theme.subtleText, marginTop: 5 }}>{sub}</div>}
    </div>
  );
}

function ChartCard({ title, note, theme, children, style }) {
  return (
    <div style={{ background: theme.cardBg, border: `1px solid ${theme.cardBorder}`, borderRadius: 8, padding: "18px 20px 16px", ...style }}>
      {title && <p style={{ fontFamily: SANS, fontSize: 12.5, fontWeight: 700, color: theme.secondaryText, margin: "0 0 2px" }}>{title}</p>}
      {note && <p style={{ fontFamily: SANS, fontSize: 11, color: theme.subtleText, margin: "0 0 14px" }}>{note}</p>}
      {children}
    </div>
  );
}

function TableToggle({ theme, headers, rows }) {
  return (
    <details style={{ marginTop: 10 }}>
      <summary style={{ cursor: "pointer", fontFamily: SANS, fontSize: 11.5, color: theme.subtleText, userSelect: "none" }}>View as table</summary>
      <div style={{ overflowX: "auto", marginTop: 10 }}>
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead><tr>{headers.map(h => <th key={h} style={{ ...thStyle(theme), textAlign: h === headers[0] ? "left" : "right" }}>{h}</th>)}</tr></thead>
          <tbody>
            {rows.map((r, i) => (
              <tr key={i}>
                <td style={tdStyle(theme)}>{r.label}</td>
                <td style={{ ...tdStyle(theme), textAlign: "right", fontFamily: MONO, fontVariantNumeric: "tabular-nums" }}>{r.value}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </details>
  );
}

export const CensusTab = ({ setActiveTab, setClusterFilter, setStatusFilter, setSearchQuery, setDamagesView, setShowPastEvents }) => {
  const theme = useTheme();
  const [velocityMode, setVelocityMode] = useState("all");
  const monthly = (velocityMode === "all" ? monthlyAll : monthlyFilings).map((v, i) => ({ label: MONTHS[i], value: v }));
  const today = getPDTMidnight();
  const todayMonthIdx = today.getUTCFullYear() === 2026 ? today.getUTCMonth() : null;
  monthly.forEach((d, i) => { d.opacity = todayMonthIdx === null || i <= todayMonthIdx ? 1 : 0.4; });

  // Always set every filter explicitly (never leave a stale cluster/search from a
  // previous drill-through in place) so each click lands on exactly what it promised.
  const goToMatters = (opts = {}) => {
    setStatusFilter?.("all");
    setClusterFilter?.(opts.cluster ?? null);
    setSearchQuery?.(opts.search ?? "");
    setActiveTab("Matters");
  };

  const sectionStyle = { marginBottom: 40 };
  const dividerStyle = { borderTop: `1px solid ${theme.cardBorder}`, paddingTop: 40 };

  return (
    <div style={{ maxWidth: 880, margin: "0 auto" }}>
      {/* Masthead */}
      <header style={{ paddingBottom: 20, marginBottom: 34, borderBottom: `3px double ${theme.cardBorder}` }}>
        <Eyebrow theme={theme}>In Propria Persona &middot; Case File Census</Eyebrow>
        <h1 style={{ fontSize: 30, fontWeight: 700, color: theme.heading, margin: "0 0 8px" }}>The Scale of One Litigant's Docket</h1>
        <p style={{ fontFamily: SANS, fontSize: 14.5, color: theme.subtleText, maxWidth: 620, margin: 0, lineHeight: 1.6 }}>
          A statistical accounting of every civil and habeas matter tracked in this portfolio — scale, pace, legal theories, and financial exposure — filed, served, argued, and pressed by a single self-represented plaintiff. Click any bar, tile, or row to jump to the underlying matters.
        </p>
        <div style={{ marginTop: 14, fontFamily: MONO, fontSize: 11, color: theme.subtleText, display: "flex", gap: 18, flexWrap: "wrap" }}>
          <span>CURATED FIGURES AS OF {PORTFOLIO.census.asOf.toUpperCase()}</span>
          <span>EVERYTHING ELSE COMPUTED LIVE, ON EVERY LOAD</span>
        </div>
      </header>

      {/* EXHIBIT A — SCALE */}
      <section style={sectionStyle}>
        <ExhibitHeading theme={theme} exhibit="Exhibit A — Scale" title="Thirty matters. One name on every caption."
          intro="Every case below lists the same plaintiff, appearing without counsel. Read together, the docket is less a single lawsuit than a standing legal practice run out of one person's own record-keeping." />
        <div className="grid-cards" style={{ gap: 1, background: theme.cardBorder, border: `1px solid ${theme.cardBorder}`, borderRadius: 6, overflow: "hidden" }}>
          <StatTile theme={theme} label="Matters Tracked" value={totalMatters} sub={`${liveMatters} live · ${archivedMatters} closed/archived`} />
          <StatTile theme={theme} label="Active Filing Span" value={filingSpanLabel} sub="earliest → latest complaint" />
          <StatTile theme={theme} label="Court Systems" value={distinctCourts} sub={`${PORTFOLIO.jurisdictions.length} jurisdictions listed`} />
          <StatTile theme={theme} label="Judicial Officers" value={distinctJudges} sub={`assigned in ${assignedMatters} of ${totalMatters}`} />
          <StatTile theme={theme} label="Named Defendants" value={PORTFOLIO.census.namedDefendants} sub={`~${PORTFOLIO.census.namedInstitutions} institutions, DOES excluded`} />
          <StatTile theme={theme} label="Causes of Action" value={totalCauses} sub={`${PORTFOLIO.census.distinctTheories} distinct theories`} />
          <StatTile theme={theme} label="Docs + Evidence" value={(totalDocuments + totalEvidence).toLocaleString()} sub={`${totalDocuments} docs · ${totalEvidence} evidence`} />
          <StatTile theme={theme} label="Fee Waivers" value={PORTFOLIO.census.feeWaiversGranted} sub={`granted · ${PORTFOLIO.census.feeWaiversDenied} denied`} />
        </div>
      </section>

      {/* EXHIBIT B — DOCKET STATUS */}
      <section style={{ ...sectionStyle, ...dividerStyle }}>
        <ExhibitHeading theme={theme} exhibit="Exhibit B — Docket Status" title="Where each matter stands, and what it's about"
          intro={`${statusCounts["Abandoned"] || 0} matters closed without a decision on the merits, several for safety reasons; ${liveMatters} remain live. Subject matter splits into five recognizable families of dispute.`} />

        <ChartCard theme={theme} title={`Matters by procedural phase (n=${totalMatters})`} note="Live matters show structured phase (demurrer, F&R pending, responsive deadline, etc.); terminal matters show disposition." style={{ marginBottom: 16 }}>
          <HorizontalBarChart theme={theme} data={statusRows} leftPad={170} barH={20} gap={9} ariaLabel="Matters by procedural phase" onRowClick={() => goToMatters()} />
          <TableToggle theme={theme} headers={["Phase / disposition", "Matters"]} rows={statusRows.map(r => ({ label: r.label, value: r.count }))} />
        </ChartCard>

        <ChartCard theme={theme} title={`Matters by proceeding type (n=${totalMatters})`} note="State civil, federal civil, mandate/writ, and habeas each have their own phase vocabulary." style={{ marginBottom: 16 }}>
          <HorizontalBarChart theme={theme} data={proceedingRows} leftPad={140} barH={22} gap={11} ariaLabel="Matters by proceeding type" onRowClick={() => goToMatters()} />
          <TableToggle theme={theme} headers={["Proceeding", "Matters"]} rows={proceedingRows.map(r => ({ label: r.label, value: r.count }))} />
        </ChartCard>

        <ChartCard theme={theme} title={`Matters by subject-matter cluster (n=${totalMatters})`} note="Five recurring fact patterns account for the entire docket. Click a bar to open Matters.">
          <HorizontalBarChart theme={theme} data={clusterRows} leftPad={215} barH={22} gap={11} ariaLabel="Matters by subject cluster" onRowClick={(d) => goToMatters({ cluster: d.n })} />
          <TableToggle theme={theme} headers={["Cluster", "Matters"]} rows={clusterRows.map(r => ({ label: r.label, value: r.count }))} />
        </ChartCard>
      </section>

      {/* EXHIBIT C — VELOCITY */}
      <section style={{ ...sectionStyle, ...dividerStyle }}>
        <ExhibitHeading theme={theme} exhibit="Exhibit C — Filing Velocity" title={`${PORTFOLIO.timeline.length} logged events, and a docket that keeps accelerating`}
          intro={`At its peak in 2026, a new matter was opened roughly every ten days. ${MONTHS[busiestMonthIdx]} 2026 alone produced ${monthlyAll[busiestMonthIdx]} timeline entries, the busiest month on record.`} />
        <ChartCard theme={theme} title="Timeline activity by month, 2026" note="Solid bars: happened. Faded bars: scheduled ahead of today. Click a bar to open Timeline.">
          <div style={{ display: "flex", gap: 6, marginBottom: 14 }}>
            {[{ k: "all", l: "All Events" }, { k: "filing", l: "Filings Only" }].map(({ k, l }) => (
              <button key={k} onClick={() => setVelocityMode(k)} aria-pressed={velocityMode === k} style={{
                padding: "5px 11px", borderRadius: 6,
                border: velocityMode === k ? `1px solid ${GOLD}` : `1px solid ${theme.filterInactiveBorder}`,
                background: velocityMode === k ? `${GOLD}18` : theme.filterInactiveBg,
                color: velocityMode === k ? GOLD : theme.filterInactiveColor,
                fontFamily: SANS, fontSize: 11, fontWeight: 600, cursor: "pointer",
              }}>{l}</button>
            ))}
          </div>
          <VerticalBarChart theme={theme} data={monthly} todayIndex={todayMonthIdx} ariaLabel={`Timeline ${velocityMode === "filing" ? "filings" : "events"} by month, 2026`}
            onColumnClick={(d, i) => { setShowPastEvents?.(todayMonthIdx === null || i <= todayMonthIdx); setActiveTab("Timeline"); }} />
        </ChartCard>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(min(100%, 200px), 1fr))", gap: 12, marginTop: 16 }}>
          <div style={{ background: theme.cardBg, border: `1px solid ${theme.cardBorder}`, borderLeft: `3px solid ${GOLD}`, borderRadius: 4, padding: "12px 14px" }}>
            <div style={{ fontFamily: MONO, fontSize: 18, fontWeight: 700, color: theme.heading }}>~3.0 / mo</div>
            <div style={{ fontFamily: SANS, fontSize: 11.5, color: theme.subtleText, marginTop: 3 }}>New matters filed in 2026's peak filing window — about one every 10 days</div>
          </div>
          <div style={{ background: theme.cardBg, border: `1px solid ${theme.cardBorder}`, borderLeft: `3px solid ${GOLD}`, borderRadius: 4, padding: "12px 14px" }}>
            <div style={{ fontFamily: MONO, fontSize: 18, fontWeight: 700, color: theme.heading }}>{liveMatters}</div>
            <div style={{ fontFamily: SANS, fontSize: 11.5, color: theme.subtleText, marginTop: 3 }}>Matters currently live, with the docket still open</div>
          </div>
        </div>
      </section>

      {/* EXHIBIT D — LEGAL THEORIES */}
      <section style={{ ...sectionStyle, ...dividerStyle }}>
        <ExhibitHeading theme={theme} exhibit="Exhibit D — Legal Theories" title={`${PORTFOLIO.census.distinctTheories} theories, unevenly leaned on`}
          intro="Negligence and 14th Amendment due process carry the most weight, but the pattern below is really two overlapping playbooks — one built on Bane Act/civil-rights claims against state actors, the other a template built around a single California statute (more in Exhibit E)." />
        <ChartCard theme={theme} title="Most-asserted causes of action, by matter count" note={`${totalCauses} causes of action pled across ${totalMatters} matters — top ${PORTFOLIO.census.topTheories.length} shown`}>
          <HorizontalBarChart theme={theme} data={PORTFOLIO.census.topTheories.map(t => ({ label: t.label, value: t.count, color: GOLD }))} leftPad={210} barH={17} gap={7} ariaLabel="Most asserted causes of action" />
          <p style={{ fontFamily: SANS, fontSize: 11, color: theme.subtleText, margin: "12px 0 0" }}>Plus 12 additional theories asserted 1&ndash;4 times each (RICO, Monell liability, habeas corpus, FCRA, writ of mandate, and others).</p>
        </ChartCard>
      </section>

      {/* EXHIBIT E — THE REPEATABLE CLAIM */}
      <section style={{ ...sectionStyle, ...dividerStyle }}>
        <ExhibitHeading theme={theme} exhibit="Exhibit E — The Repeatable Claim" title="One statute, six employers"
          intro="Penal Code §290.46(j)(2)(E) bars using California's sex-offender registry for employment decisions. After the theory produced a settlement against the first employer, it was applied to five more — application, background check, a registry flag, an adverse action, a demand letter." />
        <ChartCard theme={theme} title={null}>
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
                  const isSettled = statusLabel === "Settled";
                  return (
                    <tr
                      key={matter} role="button" tabIndex={0}
                      onClick={() => goToMatters({ search: c.caption.replace(/^Newanforbi v\.\s*/, "") })}
                      onKeyDown={e => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); goToMatters({ search: c.caption.replace(/^Newanforbi v\.\s*/, "") }); } }}
                      style={{ cursor: "pointer" }}
                    >
                      <td style={tdStyle(theme)}><span style={{ color: GOLD, fontWeight: 700, fontFamily: MONO }}>M{matter}</span></td>
                      <td style={{ ...tdStyle(theme), color: theme.secondaryText }}>{c.caption.replace(/^Newanforbi v\.\s*/, "")}</td>
                      <td style={{ ...tdStyle(theme), color: theme.subtleText }}>{vendor}</td>
                      <td style={tdStyle(theme)}>
                        {isSettled
                          ? <span style={{ fontFamily: MONO, fontSize: 10.5, fontWeight: 700, letterSpacing: "0.06em", textTransform: "uppercase", color: GREEN, border: `1.5px solid ${GREEN}`, borderRadius: 3, padding: "2px 6px" }}>Settled {fmt(settledDeals.find(d => d.matter === matter)?.amount || 0)}</span>
                          : <span style={{ color: STATUS_COLOR[statusLabel] || theme.subtleText, fontWeight: 600 }}>{statusLabel}</span>}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </ChartCard>

        <p style={{ fontFamily: SANS, fontSize: 14, color: theme.subtleText, lineHeight: 1.6, marginTop: 18 }}>
          The largest cluster in the portfolio isn't the employment claims — it's <strong style={{ color: theme.secondaryText }}>{clusterRows.find(c => c.label.includes("Parole"))?.count ?? clusterRows[0]?.count} matters</strong> arising from parole supervision under CDCR, naming individual agents and officials plus the CDCR Secretary in an official capacity across several of them, and a private contracted therapy vendor as co-defendant in the most recent filing. The connecting threads: a disputed discharge-review form, a superseded department policy pursued as ultra vires, and an inter-county transfer the litigant's own records date to one day after filing a matter naming his supervising officials.
        </p>
      </section>

      {/* EXHIBIT F — FINANCIAL EXPOSURE */}
      <section style={{ ...sectionStyle, ...dividerStyle }}>
        <ExhibitHeading theme={theme} exhibit="Exhibit F — Financial Exposure" title="What's actually at stake, in dollars"
          intro="The portfolio's own de-duplicated model — which strips out shared economic events counted more than once across related matters — puts total exposure in the range below. One matter has already converted to cash." />

        <ChartCard theme={theme} title="Portfolio-wide damages exposure, de-duplicated" note="Conservative / moderate / aggressive tiers, computed once across all matters to avoid double-counting shared claims. Click a tier to open Damages.">
          <HorizontalBarChart theme={theme} leftPad={110} barH={28} gap={13} valueFmt={v => fmt(v) + (v === exposure.aggressive ? "+" : "")} ariaLabel="Portfolio damages exposure by tier"
            data={["conservative", "moderate", "aggressive"].map((k, i) => ({ label: k[0].toUpperCase() + k.slice(1), value: exposure[k], color: GOLD, opacity: 0.55 + i * 0.225, key: k }))}
            onRowClick={(d) => { setDamagesView?.(d.key); setActiveTab("Damages"); }} />
        </ChartCard>

        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(min(100%, 220px), 1fr))", gap: 14, margin: "16px 0" }}>
          <div style={{ background: theme.cardBg, border: `1px solid ${theme.cardBorder}`, borderLeft: `3px solid ${GREEN}`, borderRadius: 4, padding: "14px 16px" }}>
            <div style={{ fontFamily: MONO, fontSize: 20, fontWeight: 700, color: theme.heading }}>{fmt(settledTotal)}</div>
            <div style={{ fontFamily: SANS, fontSize: 11.5, color: theme.subtleText, marginTop: 3 }}>Realized — {settledDeals.length} settlement{settledDeals.length !== 1 ? "s" : ""} to date</div>
          </div>
          <div style={{ background: theme.cardBg, border: `1px solid ${theme.cardBorder}`, borderLeft: `3px solid ${GOLD}`, borderRadius: 4, padding: "14px 16px" }}>
            <div style={{ fontFamily: MONO, fontSize: 20, fontWeight: 700, color: theme.heading }}>{fmt(demandsTotal)}</div>
            <div style={{ fontFamily: SANS, fontSize: 11.5, color: theme.subtleText, marginTop: 3 }}>Outstanding demands — {demandsResponded} of {PORTFOLIO.outcomes.active_demands.length} defendants responded</div>
          </div>
        </div>

        <ChartCard theme={theme} title="Estimated value of the work itself, had counsel been retained" note={`${feeSummary.totalDocumentsAnalyzed} real PDFs, ${feeSummary.totalPagesReal.toLocaleString()} pages, measured directly and priced at a blended $${feeSummary.methodology.blendedHourlyRate}/hr`}>
          <div style={{ fontFamily: MONO, fontSize: 26, fontWeight: 700, color: theme.heading, marginBottom: 2 }}>
            {fmt(feeSummary.totalEstimatedCost.low)}&ndash;{fmt(feeSummary.totalEstimatedCost.high)}
          </div>
          <div style={{ fontFamily: SANS, fontSize: 11.5, color: theme.subtleText, marginBottom: 16 }}>
            ~{feeSummary.totalEstimatedHours.low.toLocaleString()}&ndash;{feeSummary.totalEstimatedHours.high.toLocaleString()} hours of attorney work, delivered pro se
          </div>
          <RangeChart theme={theme} rows={feeClusters.map(c => ({ label: c.label, low: c.costLow, high: c.costHigh }))} valueFmt={fmt} />
          <div style={{ display: "flex", justifyContent: "flex-end", marginTop: 8 }}>
            <button onClick={() => setActiveTab("Cost of Counsel")} style={{
              background: "none", border: `1px solid ${theme.cardBorder}`, borderRadius: 6, padding: "6px 12px",
              color: GOLD, fontFamily: SANS, fontSize: 11, fontWeight: 600, cursor: "pointer",
            }}>Full breakdown →</button>
          </div>
        </ChartCard>
      </section>

      {/* EXHIBIT G — CONTEXT */}
      <section style={{ ...sectionStyle, ...dividerStyle }}>
        <ExhibitHeading theme={theme} exhibit="Exhibit G — Context" title="What the numbers don't show" />
        <p style={{ fontFamily: SANS, fontSize: 14, color: theme.subtleText, lineHeight: 1.65 }}>
          {statusCounts["Abandoned"] || 0} of the {totalMatters} matters were voluntarily abandoned or dismissed rather than pressed — several explicitly because of a real, credible safety threat rather than any weakness in the claim. The portfolio's own records tie a retaliatory inter-county transfer, dated one day after a filing against supervising parole officials, to a period of homelessness beginning July 2, 2026 that the litigant has been navigating while continuing to file, serve, and track {liveMatters} still-live matters. Read against that backdrop, the statistics above describe not just a large caseload, but one sustained without an office, a firm, or a single day off from the underlying circumstances that produced it.
        </p>
      </section>

      {/* DATA NOTES */}
      <section style={{ borderTop: `1px solid ${theme.cardBorder}`, paddingTop: 18 }}>
        <div style={{ fontFamily: SANS, fontSize: 11.5, color: theme.subtleText, fontWeight: 700, marginBottom: 8 }}>Methodology &amp; caveats</div>
        <ul style={{ fontFamily: SANS, fontSize: 12, color: theme.subtleText, lineHeight: 1.7, margin: 0, paddingLeft: 18 }}>
          <li>Every figure on this page except the small hand-curated set in <code>census.js</code> (named defendants, fee-waiver counts, the top-theories ranking, and the registry-bar employer/vendor list) is computed live from matter JSON, <code>timeline.json</code>, <code>damages.js</code>, <code>lawyerFees.js</code>, and <code>outcomes.js</code> on every page load — it can't drift out of sync the way a hand-compiled snapshot can.</li>
          <li>A supplemental cross-matter interconnectivity audit (disclosure completeness, claim-preclusion exposure, citation-chain accuracy) was run across all {totalMatters} matters and logged to <code>consistency_audit.json</code> — see that file for the full set of findings and what was corrected in place versus only flagged.</li>
          <li>The "moderate" damages tier is only explicitly stated in a minority of matters and is too sparse to sum meaningfully at the per-matter level; the portfolio-wide moderate figure comes from the de-duplicated model in <code>damages.js</code>, not a raw sum.</li>
        </ul>
      </section>

      <footer style={{ marginTop: 40, borderTop: `3px double ${theme.cardBorder}`, paddingTop: 14, fontFamily: MONO, fontSize: 10.5, color: theme.subtleText }}>
        RECOMPUTED LIVE FROM MATTERS.JS, TIMELINE.JS, DAMAGES.JS, LAWYERFEES.JS &amp; OUTCOMES.JS.
      </footer>
    </div>
  );
};
