import { useState } from "react";
import { Link } from "react-router-dom";
import { cases } from "../data/matters";
import { GOLD, BORDER_BLUE } from "../constants";
import { StatusBadge, ClusterBadge, TypeBadge, ArchiveBadge } from "./Badges";
import { ServiceTracker } from "./ServiceTracker";
import { useTheme } from "../ThemeContext";
import { formatMatterPath } from "../utils/formatters";
import { SavedViews } from "./matters/SavedViews";

const MatterCard = ({ matter: c, isOpen, onToggle }) => {
  const theme = useTheme();
  return (
    <div style={{ position: "relative", background: theme.cardBg, borderRadius: 10, border: isOpen ? `1px solid ${GOLD}40` : `1px solid ${theme.cardBorder}`, overflow: "hidden", transition: "border-color 0.3s" }}>
      {c.status && c.status.startsWith("SETTLED") && (
        <div aria-label="Settled" style={{ position: "absolute", top: 14, right: -28, width: 110, background: "#16a34a", color: "#fff", fontSize: 10, fontFamily: "'DM Sans', sans-serif", fontWeight: 800, letterSpacing: 2, textTransform: "uppercase", textAlign: "center", padding: "5px 0", transform: "rotate(45deg)", boxShadow: "0 2px 8px rgba(0,0,0,0.35)", pointerEvents: "none", zIndex: 10 }}>SETTLED</div>
      )}
      {c.badge === "DEFAULT" && (
        <div aria-label="Default" style={{ position: "absolute", top: 14, right: -28, width: 110, background: "#16a34a", color: "#fff", fontSize: 10, fontFamily: "'DM Sans', sans-serif", fontWeight: 800, letterSpacing: 2, textTransform: "uppercase", textAlign: "center", padding: "5px 0", transform: "rotate(45deg)", boxShadow: "0 2px 8px rgba(0,0,0,0.35)", pointerEvents: "none", zIndex: 10 }}>DEFAULT</div>
      )}
      {c.badge === "DISMISSED" && (
        <div aria-label="Dismissed" style={{ position: "absolute", top: 14, right: -28, width: 110, background: "#dc2626", color: "#fff", fontSize: 10, fontFamily: "'DM Sans', sans-serif", fontWeight: 800, letterSpacing: 2, textTransform: "uppercase", textAlign: "center", padding: "5px 0", transform: "rotate(45deg)", boxShadow: "0 2px 8px rgba(0,0,0,0.35)", pointerEvents: "none", zIndex: 10 }}>DISMISSED</div>
      )}
      {c.badge === "ABANDONED" && (
        <div aria-label="Abandoned" style={{ position: "absolute", top: 14, right: -28, width: 110, background: "#FFFFFF", color: "#1a1a1a", border: "1px solid #00000022", fontSize: 10, fontFamily: "'DM Sans', sans-serif", fontWeight: 800, letterSpacing: 2, textTransform: "uppercase", textAlign: "center", padding: "5px 0", transform: "rotate(45deg)", boxShadow: "0 2px 8px rgba(0,0,0,0.35)", pointerEvents: "none", zIndex: 10 }}>ABANDONED</div>
      )}
      {c.badge === "DENIED" && (
        <div aria-label="Denied" style={{ position: "absolute", top: 14, right: -28, width: 110, background: "#6b7280", color: "#fff", fontSize: 10, fontFamily: "'DM Sans', sans-serif", fontWeight: 800, letterSpacing: 2, textTransform: "uppercase", textAlign: "center", padding: "5px 0", transform: "rotate(45deg)", boxShadow: "0 2px 8px rgba(0,0,0,0.35)", pointerEvents: "none", zIndex: 10 }}>DENIED</div>
      )}
      {c.badge === "PENDING" && (
        <div aria-label="Pending" style={{ position: "absolute", top: 14, right: -28, width: 110, background: "#eab308", color: "#1a1a1a", fontSize: 10, fontFamily: "'DM Sans', sans-serif", fontWeight: 800, letterSpacing: 2, textTransform: "uppercase", textAlign: "center", padding: "5px 0", transform: "rotate(45deg)", boxShadow: "0 2px 8px rgba(0,0,0,0.35)", pointerEvents: "none", zIndex: 10 }}>PENDING</div>
      )}
      {c.badge === "TIMELY" && (
        <div aria-label="Timely filed" style={{ position: "absolute", top: 14, right: -28, width: 110, background: "#0284c7", color: "#fff", fontSize: 10, fontFamily: "'DM Sans', sans-serif", fontWeight: 800, letterSpacing: 2, textTransform: "uppercase", textAlign: "center", padding: "5px 0", transform: "rotate(45deg)", boxShadow: "0 2px 8px rgba(0,0,0,0.35)", pointerEvents: "none", zIndex: 10 }}>TIMELY</div>
      )}
      {c.badge === "SERVED" && (
        <div aria-label="Served" style={{ position: "absolute", top: 14, right: -28, width: 110, background: "#0d9488", color: "#fff", fontSize: 10, fontFamily: "'DM Sans', sans-serif", fontWeight: 800, letterSpacing: 2, textTransform: "uppercase", textAlign: "center", padding: "5px 0", transform: "rotate(45deg)", boxShadow: "0 2px 8px rgba(0,0,0,0.35)", pointerEvents: "none", zIndex: 10 }}>SERVED</div>
      )}
      {/* Header row */}
      <button
        onClick={onToggle}
        aria-expanded={isOpen}
        aria-controls={`matter-detail-${c.number}`}
        style={{ width: "100%", padding: "16px 22px", cursor: "pointer", display: "flex", alignItems: "center", gap: 16, flexWrap: "wrap", background: "transparent", border: "none", textAlign: "left", color: "inherit", font: "inherit", lineHeight: "inherit", margin: 0 }}
      >
        <div style={{ width: 36, height: 36, borderRadius: 8, background: theme.navySubtleBg, display: "flex", alignItems: "center", justifyContent: "center", fontFamily: "'DM Sans', sans-serif", fontSize: 14, fontWeight: 700, color: GOLD, flexShrink: 0 }}>{c.number}</div>
        <div style={{ flex: 1, minWidth: 200 }}>
          <div style={{ fontSize: 16, fontWeight: 700, color: theme.heading, marginBottom: 3 }}>{c.caption}</div>
          <div style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 12, color: theme.subtleText }}>{c.case_no} · {c.court}</div>
        </div>
        <div style={{ display: "flex", flexDirection: "column", alignItems: "flex-end", gap: 6 }}>
          <div style={{ display: "flex", gap: 8, alignItems: "center", flexWrap: "wrap" }}>
            <ClusterBadge cluster={c.cluster} />
            <TypeBadge type={c.type} />
            <StatusBadge status={c.status} />
            {c.archived && <ArchiveBadge />}
          </div>
          {c.note && (
            <div style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 12, fontWeight: 600, fontStyle: "italic", color: theme.secondaryText, whiteSpace: "nowrap" }}>
              {c.badge === "PENDING" ? "⏳" : "📌"} {c.note}
            </div>
          )}
        </div>
        <div aria-hidden="true" style={{ color: theme.subtleText, fontSize: 18, transition: "transform 0.3s", transform: isOpen ? "rotate(180deg)" : "rotate(0)" }}>▾</div>
      </button>

      {/* Expanded detail */}
      {isOpen && (
        <div id={`matter-detail-${c.number}`} style={{ padding: "0 22px 22px", borderTop: `1px solid ${theme.cardBorder}` }}>
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 20, paddingTop: 18 }}>
            <div>
              <div style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 10, color: GOLD, fontWeight: 700, letterSpacing: 2, textTransform: "uppercase", marginBottom: 8 }}>Defendants</div>
              <p style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 13, color: theme.secondaryText, lineHeight: 1.6, margin: 0 }}>{c.defendants}</p>
            </div>
            <div>
              <div style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 10, color: GOLD, fontWeight: 700, letterSpacing: 2, textTransform: "uppercase", marginBottom: 8 }}>Judge</div>
              <p style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 13, color: theme.secondaryText, margin: "0 0 12px" }}>{c.judge}</p>
              <div style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 10, color: GOLD, fontWeight: 700, letterSpacing: 2, textTransform: "uppercase", marginBottom: 8 }}>Filed</div>
              <p style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 13, color: theme.secondaryText, margin: 0 }}>{c.filed}</p>
            </div>
          </div>

          <div style={{ marginTop: 18 }}>
            <div style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 10, color: GOLD, fontWeight: 700, letterSpacing: 2, textTransform: "uppercase", marginBottom: 8 }}>Causes of Action</div>
            <div style={{ display: "flex", flexWrap: "wrap", gap: 6 }}>
              {c.causes.map((ca, i) => (
                <span key={i} style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 11, padding: "4px 10px", borderRadius: 4, background: theme.navySubtleBg, color: theme.secondaryText, border: `1px solid ${BORDER_BLUE}30` }}>{ca}</span>
              ))}
            </div>
          </div>

          <div style={{ marginTop: 18 }}>
            <div style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 10, color: GOLD, fontWeight: 700, letterSpacing: 2, textTransform: "uppercase", marginBottom: 8 }}>Key Facts</div>
            <p style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 13, color: theme.mutedText, lineHeight: 1.7, margin: 0 }}>{c.key_facts}</p>
          </div>

          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 20, marginTop: 18 }}>
            <div>
              <div style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 10, color: GOLD, fontWeight: 700, letterSpacing: 2, textTransform: "uppercase", marginBottom: 8 }}>Procedural Status</div>
              <p style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 13, color: theme.mutedText, lineHeight: 1.6, margin: 0 }}>{c.procedural_status}</p>
            </div>
            <div>
              <div style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 10, color: GOLD, fontWeight: 700, letterSpacing: 2, textTransform: "uppercase", marginBottom: 8 }}>Estimated Damages</div>
              <p style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 15, color: "#34D399", fontWeight: 700, margin: "0 0 12px" }}>{c.damages}</p>
              {c.risk && <>
                <div style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 10, color: GOLD, fontWeight: 700, letterSpacing: 2, textTransform: "uppercase", marginBottom: 8 }}>Risk / Defense Notes</div>
                <p style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 12, color: "#F59E0B", lineHeight: 1.6, margin: 0 }}>{c.risk}</p>
              </>}
            </div>
          </div>

          <div style={{ marginTop: 18 }}>
            <div style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 10, color: GOLD, fontWeight: 700, letterSpacing: 2, textTransform: "uppercase", marginBottom: 8 }}>Key Evidence</div>
            <div style={{ display: "flex", flexWrap: "wrap", gap: 6 }}>
              {c.evidence.map((ev, i) => (
                <span key={i} style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 11, padding: "4px 10px", borderRadius: 4, background: theme.clusterPillBg, color: theme.clusterPillColor, border: `1px solid ${theme.clusterPillBorder}` }}>{ev}</span>
              ))}
            </div>
          </div>

          {c.serviceTracking && <ServiceTracker serviceTracking={c.serviceTracking} />}

          <div style={{ marginTop: 20 }}>
            <Link to={formatMatterPath(c.number)} style={{ color: GOLD, fontFamily: "'DM Sans', sans-serif", fontSize: 12, fontWeight: 700, textDecoration: "none" }}>
              Open dedicated matter page →
            </Link>
          </div>
        </div>
      )}
    </div>
  );
};

export const MattersTab = ({ filteredCases, statusFilter, setStatusFilter, clusterFilter, setClusterFilter, typeFilter, setTypeFilter, searchQuery, setSearchQuery, sortKey, setSortKey }) => {
  const theme = useTheme();
  const [expandedMatter, setExpandedMatter] = useState(null);
  const activeCount = cases.filter(c => !c.archived).length;

  return (
    <div>
      {/* Filters */}
      <div style={{ display: "flex", gap: 10, flexWrap: "wrap", marginBottom: 20, alignItems: "center" }}>
        <input
          value={searchQuery}
          onChange={e => setSearchQuery(e.target.value)}
          placeholder="Search matters…"
          aria-label="Search matters by caption, case number, or keywords"
          style={{ flex: "1 1 200px", padding: "10px 16px", borderRadius: 8, border: `1px solid ${theme.cardBorder}`, background: theme.inputBg, color: theme.inputColor, fontFamily: "'DM Sans', sans-serif", fontSize: 13, outline: "none" }}
        />
        {["active", "upcoming", "archived", "all"].map(s => (
          <button key={s} onClick={() => setStatusFilter(s)} aria-pressed={statusFilter === s} style={{
            padding: "8px 14px", borderRadius: 6,
            border: statusFilter === s ? `1px solid ${GOLD}` : `1px solid ${theme.filterInactiveBorder}`,
            background: statusFilter === s ? `${GOLD}18` : theme.filterInactiveBg,
            color: statusFilter === s ? GOLD : theme.filterInactiveColor,
            fontFamily: "'DM Sans', sans-serif", fontSize: 12, fontWeight: 600, cursor: "pointer"
          }}>{s === "active" ? `Active (${activeCount})` : s === "upcoming" ? "Upcoming" : s === "archived" ? "Archived" : "All"}</button>
        ))}
        <span style={{ color: theme.subtleText, fontFamily: "'DM Sans', sans-serif", fontSize: 12 }}>|</span>
        {[null, 1, 2, 3, 4, 5].map(c => (
          <button key={c ?? "all"} onClick={() => setClusterFilter(c)} style={{
            padding: "8px 14px", borderRadius: 6,
            border: clusterFilter === c ? `1px solid ${GOLD}` : `1px solid ${theme.filterInactiveBorder}`,
            background: clusterFilter === c ? `${GOLD}18` : theme.filterInactiveBg,
            color: clusterFilter === c ? GOLD : theme.filterInactiveColor,
            fontFamily: "'DM Sans', sans-serif", fontSize: 12, fontWeight: 600, cursor: "pointer"
          }}>{c === null ? "All" : c === 1 ? "CHP" : c === 2 ? "Parole/HOPE" : c === 3 ? "Employment" : c === 4 ? "Writs" : "Consumer Fraud"}</button>
        ))}
        <span style={{ color: theme.subtleText, fontFamily: "'DM Sans', sans-serif", fontSize: 12 }}>|</span>
        {[null, "Federal", "State"].map(t => (
          <button key={t ?? "all"} onClick={() => setTypeFilter(t)} style={{
            padding: "8px 14px", borderRadius: 6,
            border: typeFilter === t ? `1px solid ${GOLD}` : `1px solid ${theme.filterInactiveBorder}`,
            background: typeFilter === t ? `${GOLD}18` : theme.filterInactiveBg,
            color: typeFilter === t ? GOLD : theme.filterInactiveColor,
            fontFamily: "'DM Sans', sans-serif", fontSize: 12, fontWeight: 600, cursor: "pointer"
          }}>{t ?? "All"}</button>
        ))}
        <span style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 12, color: theme.subtleText, marginLeft: "auto" }}>{filteredCases.length} of {cases.length}</span>
      </div>

      <div className="matter-view-controls">
        <SavedViews
          current={{ status: statusFilter, cluster: clusterFilter, type: typeFilter, query: searchQuery, sort: sortKey }}
          onApply={(view) => { setStatusFilter(view.status); setClusterFilter(view.cluster); setTypeFilter(view.type); setSearchQuery(view.query); setSortKey(view.sort); }}
        />
        <label className="sort-control" style={{ color: theme.subtleText }}>Sort by
          <select value={sortKey} onChange={(event) => setSortKey(event.target.value)} style={{ background: theme.inputBg, borderColor: theme.cardBorder, color: theme.inputColor }}>
            <option value="number">Matter number</option><option value="filed">Newest filing</option><option value="deadline">Next deadline</option><option value="exposure">Moderate exposure</option><option value="court">Court</option><option value="status">Status</option>
          </select>
        </label>
      </div>

      <div style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 11, fontStyle: "italic", color: theme.subtleText, marginBottom: 16 }}>
        Matters marked <strong style={{ color: "#6b7280", fontStyle: "normal" }}>ABANDONED</strong> were voluntarily abandoned due to real, credible safety threats.
        Matters marked ⏳ <strong style={{ color: "#eab308", fontStyle: "normal" }}>PENDING</strong> are prepared but not yet filed, contingent on external timing.
      </div>

      {/* Matter Cards */}
      <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
        {filteredCases.length === 0 ? (
          <div style={{ padding: "40px 24px", textAlign: "center", fontFamily: "'DM Sans', sans-serif", fontSize: 14, color: theme.subtleText }}>
            No matters match your current filters.{" "}
            <button
              onClick={() => { setStatusFilter("active"); setClusterFilter(null); setTypeFilter(null); setSearchQuery(""); setSortKey("number"); }}
              style={{ background: "none", border: "none", color: GOLD, cursor: "pointer", fontFamily: "'DM Sans', sans-serif", fontSize: 14, textDecoration: "underline", padding: 0 }}
            >
              Clear all filters
            </button>
          </div>
        ) : (
          filteredCases.map(c => (
            <MatterCard
              key={c.number}
              matter={c}
              isOpen={expandedMatter === c.number}
              onToggle={() => setExpandedMatter(expandedMatter === c.number ? null : c.number)}
            />
          ))
        )}
      </div>
    </div>
  );
};
