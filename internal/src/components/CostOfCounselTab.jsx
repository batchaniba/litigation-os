import { useState } from "react";
import { damages_table } from "../data/damages";
import { lawyer_fees, lawyer_fees_summary } from "../data/lawyerFees";
import { GOLD } from "../constants";
import { useTheme } from "../ThemeContext";
import { formatCurrency } from "../utils/formatters";

const fmt = (n) => formatCurrency(Math.round(n));
const VIEWS = ["low", "mid", "high"];
const VIEW_LABEL = { low: "Conservative", mid: "Mid-Point", high: "High-End" };

const summary = lawyer_fees_summary;
const PORTFOLIO_DAMAGES_TOTALS = damages_table.reduce(
  (acc, d) => {
    acc.conservative += d.conservative;
    acc.moderate += d.moderate;
    acc.aggressive += d.aggressive;
    return acc;
  },
  { conservative: 0, moderate: 0, aggressive: 0 }
);

const MAX_MATTER_COST = Math.max(...lawyer_fees.map((m) => m.cost.high));

const thStyle = (theme) => ({
  fontFamily: "'DM Sans', sans-serif", fontSize: 10, fontWeight: 700,
  color: theme.subtleText, textTransform: "uppercase", letterSpacing: 1,
  padding: "0 8px 8px 0", whiteSpace: "nowrap",
});

const tdStyle = (theme) => ({
  fontFamily: "'DM Sans', sans-serif", fontSize: 12,
  padding: "6px 8px 6px 0",
});

function FeeMatterCard({ m, view, expanded, onToggle, theme }) {
  const total = m.cost[view];
  const pct = (total / MAX_MATTER_COST) * 100;

  return (
    <div style={{
      background: theme.cardBg, borderRadius: 10,
      border: `1px solid ${expanded ? GOLD + "60" : theme.cardBorder}`,
      overflow: "hidden", transition: "border-color 0.2s",
    }}>
      <button onClick={onToggle} style={{
        width: "100%", background: "none", border: "none", cursor: "pointer",
        padding: "16px 20px", textAlign: "left", color: "inherit", font: "inherit",
      }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", gap: 12, flexWrap: "wrap" }}>
          <div style={{ flex: 1, minWidth: 0 }}>
            <div style={{ display: "flex", alignItems: "center", gap: 8, flexWrap: "wrap", marginBottom: 3 }}>
              <span style={{
                fontFamily: "'DM Sans', sans-serif", fontSize: 10, fontWeight: 700,
                background: `${GOLD}22`, color: GOLD, padding: "2px 7px", borderRadius: 4, letterSpacing: 1, flexShrink: 0,
              }}>M{m.number}</span>
              <span style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 13, fontWeight: 600, color: theme.secondaryText }}>{m.caption}</span>
            </div>
            <div style={{ display: "flex", gap: 8, flexWrap: "wrap", alignItems: "center" }}>
              <span style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 10, color: theme.subtleText }}>{m.court}</span>
              <span style={{ color: theme.subtleText, fontSize: 10 }}>·</span>
              <span style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 10, color: theme.subtleText }}>{m.documentsCount} docs · {m.totalPagesReal} real pages</span>
            </div>
          </div>
          <div style={{ display: "flex", alignItems: "center", gap: 12, flexShrink: 0 }}>
            <div style={{ textAlign: "right" }}>
              <div style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 18, fontWeight: 700, color: "#34D399" }}>{fmt(total)}</div>
              <div style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 10, color: theme.subtleText }}>{m.hours[view].toFixed(1)} hrs</div>
            </div>
            <span style={{
              fontFamily: "'DM Sans', sans-serif", fontSize: 14, color: theme.subtleText,
              transition: "transform 0.2s", display: "inline-block", transform: expanded ? "rotate(180deg)" : "none",
            }}>▾</span>
          </div>
        </div>
        <div style={{ height: 4, background: theme.barTrack, borderRadius: 2, overflow: "hidden", marginTop: 10 }}>
          <div style={{ height: "100%", width: `${pct}%`, background: `linear-gradient(90deg, ${GOLD}, #34D399)`, borderRadius: 2, transition: "width 0.5s ease" }} />
        </div>
      </button>

      {expanded && (
        <div style={{ borderTop: `1px solid ${theme.cardBorder}`, padding: "16px 20px 20px" }}>
          <div style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 11, color: GOLD, marginBottom: 10, letterSpacing: 0.5 }}>{m.type}</div>
          <div style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 11, color: theme.subtleText, marginBottom: 12 }}>{m.status}</div>
          <div style={{ background: theme.deepBg, borderRadius: 6, padding: "10px 12px" }}>
            <div style={{
              fontFamily: "'DM Sans', sans-serif", fontSize: 9, fontWeight: 700,
              color: GOLD, letterSpacing: 1.5, textTransform: "uppercase", marginBottom: 5,
            }}>Basis for Estimate</div>
            <div style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 11, color: theme.subtleText, lineHeight: 1.5 }}>{m.notes}</div>
          </div>
        </div>
      )}
    </div>
  );
}

export const CostOfCounselTab = () => {
  const theme = useTheme();
  const [view, setView] = useState("mid");
  const [expandedMatter, setExpandedMatter] = useState(null);

  const sortedMatters = [...lawyer_fees].sort((a, b) => b.cost[view] - a.cost[view]);
  const total = summary.totalEstimatedCost[view];
  const totalHours = summary.totalEstimatedHours[view];

  const damagesComparisonBasis = PORTFOLIO_DAMAGES_TOTALS.moderate;
  const ratioPct = ((total / damagesComparisonBasis) * 100).toFixed(0);

  return (
    <div>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 20, flexWrap: "wrap", gap: 12 }}>
        <div>
          <h2 style={{ fontSize: 24, fontWeight: 700, color: theme.heading, margin: 0 }}>Cost of Counsel</h2>
          <div style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 11, color: theme.subtleText, marginTop: 4 }}>
            What retained counsel would have billed to draft every pleading in this portfolio
          </div>
        </div>
        <div style={{ display: "flex", gap: 6, flexWrap: "wrap" }}>
          {VIEWS.map((v) => (
            <button key={v} onClick={() => setView(v)} style={{
              padding: "7px 14px", borderRadius: 6,
              border: view === v ? `1px solid ${GOLD}` : `1px solid ${theme.filterInactiveBorder}`,
              background: view === v ? `${GOLD}18` : theme.filterInactiveBg,
              color: view === v ? GOLD : theme.filterInactiveColor,
              fontFamily: "'DM Sans', sans-serif", fontSize: 11, fontWeight: 600, cursor: "pointer",
            }}>{VIEW_LABEL[v]}</button>
          ))}
        </div>
      </div>

      {/* Aggregate card */}
      <div style={{ background: theme.aggregateCardBg, borderRadius: 12, padding: 28, border: `1px solid ${GOLD}30`, marginBottom: 24, textAlign: "center" }}>
        <div style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 11, color: GOLD, fontWeight: 700, letterSpacing: 3, textTransform: "uppercase", marginBottom: 8 }}>
          Estimated Lawyer Fees — {summary.totalMatters} Matters — {VIEW_LABEL[view]}
        </div>
        <div style={{ fontSize: 48, fontWeight: 700, color: theme.aggregateCardText }}>{fmt(total)}</div>
        <div style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 11, color: theme.subtleText, marginTop: 8 }}>
          {totalHours.toFixed(0)} hours at a $280/hr blended rate · {summary.totalDocumentsAnalyzed} documents, {summary.totalPagesReal.toLocaleString()} real pages measured with pdfinfo
        </div>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 14, marginBottom: 24 }}>
        {VIEWS.map((v) => {
          const t = summary.totalEstimatedCost[v];
          const isActive = v === view;
          return (
            <button key={v} onClick={() => setView(v)} aria-pressed={isActive} style={{
              width: "100%", background: isActive ? theme.damagesActiveBg : theme.damagesInactiveBg,
              borderRadius: 10, padding: 20,
              border: isActive ? `1px solid ${GOLD}40` : `1px solid ${theme.cardBorder}`,
              cursor: "pointer", textAlign: "center", transition: "all 0.3s", color: "inherit", font: "inherit", margin: 0,
            }}>
              <div style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 11, color: isActive ? GOLD : theme.subtleText, fontWeight: 700, letterSpacing: 1, textTransform: "uppercase", marginBottom: 8 }}>{VIEW_LABEL[v]}</div>
              <div style={{ fontSize: 26, fontWeight: 700, color: isActive ? theme.aggregateCardText : theme.mutedText }}>{fmt(t)}</div>
            </button>
          );
        })}
      </div>

      {/* Damages comparison */}
      <div style={{ background: theme.cardBg, borderRadius: 10, border: `1px solid ${theme.cardBorder}`, padding: "18px 22px", marginBottom: 24 }}>
        <div style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 11, fontWeight: 700, color: GOLD, letterSpacing: 2, textTransform: "uppercase", marginBottom: 10 }}>
          Fees vs. Damages Exposure
        </div>
        <div style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 12, color: theme.secondaryText, lineHeight: 1.7 }}>
          At the {VIEW_LABEL[view].toLowerCase()} fee estimate ({fmt(total)}), hiring counsel across all {summary.totalMatters} matters
          would have consumed roughly <strong style={{ color: "#34D399" }}>{ratioPct}%</strong> of the portfolio's moderate-scenario
          damages exposure ({fmt(damagesComparisonBasis)}). Pro se representation preserves that difference in full, minus the
          litigant's own time.
        </div>
      </div>

      {/* Cluster breakdown */}
      <div style={{ display: "flex", flexDirection: "column", gap: 8, marginBottom: 24 }}>
        {Object.values(summary.byCluster).map((c, i) => {
          const val = view === "low" ? c.costLow : view === "high" ? c.costHigh : c.costMid;
          const pct = (val / summary.totalEstimatedCost[view]) * 100;
          return (
            <div key={i} style={{ background: theme.cardBg, borderRadius: 8, padding: "16px 20px", border: `1px solid ${theme.cardBorder}` }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 8 }}>
                <div>
                  <span style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 13, fontWeight: 600, color: theme.secondaryText }}>{c.label}</span>
                  <span style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 11, color: theme.subtleText, marginLeft: 10 }}>Matters {c.matters.join(", ")}</span>
                </div>
                <span style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 16, fontWeight: 700, color: "#34D399" }}>{fmt(val)}</span>
              </div>
              <div style={{ height: 5, background: theme.barTrack, borderRadius: 3, overflow: "hidden" }}>
                <div style={{ height: "100%", width: `${pct}%`, background: `linear-gradient(90deg, ${GOLD}, #34D399)`, borderRadius: 3, transition: "width 0.6s ease" }} />
              </div>
            </div>
          );
        })}
      </div>

      {/* Per-matter cards */}
      <div style={{ display: "flex", flexDirection: "column", gap: 8, marginBottom: 20 }}>
        {sortedMatters.map((m) => (
          <FeeMatterCard
            key={m.number}
            m={m}
            view={view}
            expanded={expandedMatter === m.number}
            onToggle={() => setExpandedMatter(expandedMatter === m.number ? null : m.number)}
            theme={theme}
          />
        ))}
      </div>

      {/* Ranked summary table */}
      <div style={{ background: theme.cardBg, borderRadius: 10, border: `1px solid ${theme.cardBorder}`, padding: "16px 20px" }}>
        <div style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 11, fontWeight: 700, color: GOLD, letterSpacing: 2, textTransform: "uppercase", marginBottom: 14 }}>
          Ranked by Estimated Cost — {VIEW_LABEL[view]}
        </div>
        <div style={{ overflowX: "auto" }}>
          <table style={{ width: "100%", borderCollapse: "collapse" }}>
            <thead>
              <tr>
                <th style={{ ...thStyle(theme), textAlign: "left" }}>#</th>
                <th style={{ ...thStyle(theme), textAlign: "left" }}>Matter</th>
                <th style={{ ...thStyle(theme), textAlign: "right" }}>Pages</th>
                <th style={{ ...thStyle(theme), textAlign: "right" }}>Hours</th>
                <th style={{ ...thStyle(theme), textAlign: "right" }}>Cost</th>
              </tr>
            </thead>
            <tbody>
              {sortedMatters.map((m, i) => (
                <tr key={m.number}>
                  <td style={{ ...tdStyle(theme), color: theme.subtleText }}>{i + 1}</td>
                  <td style={{ ...tdStyle(theme), color: theme.secondaryText }}>
                    <span style={{ color: GOLD, fontWeight: 700, marginRight: 8 }}>M{m.number}</span>{m.caption}
                  </td>
                  <td style={{ ...tdStyle(theme), textAlign: "right", color: "#94A3B8" }}>{m.totalPagesReal}</td>
                  <td style={{ ...tdStyle(theme), textAlign: "right", color: "#94A3B8" }}>{m.hours[view].toFixed(1)}</td>
                  <td style={{ ...tdStyle(theme), textAlign: "right", color: "#34D399", fontWeight: 700 }}>{fmt(m.cost[view])}</td>
                </tr>
              ))}
              <tr>
                <td colSpan={2} style={{ ...tdStyle(theme), borderTop: `1px solid ${theme.cardBorder}`, fontWeight: 700, color: theme.secondaryText, paddingTop: 10 }}>Total</td>
                <td style={{ ...tdStyle(theme), borderTop: `1px solid ${theme.cardBorder}`, textAlign: "right", fontWeight: 700, color: "#94A3B8", paddingTop: 10 }}>{summary.totalPagesReal.toLocaleString()}</td>
                <td style={{ ...tdStyle(theme), borderTop: `1px solid ${theme.cardBorder}`, textAlign: "right", fontWeight: 700, color: "#94A3B8", paddingTop: 10 }}>{totalHours.toFixed(0)}</td>
                <td style={{ ...tdStyle(theme), borderTop: `1px solid ${theme.cardBorder}`, textAlign: "right", fontWeight: 700, color: "#34D399", paddingTop: 10 }}>{fmt(total)}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
