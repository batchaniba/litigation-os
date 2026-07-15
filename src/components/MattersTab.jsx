import { useState } from "react";
import { PORTFOLIO } from "../data";
import { GOLD, BORDER_BLUE } from "../constants";
import { StatusBadge, ClusterBadge, TypeBadge, ArchiveBadge } from "./Badges";
import { ServiceTracker } from "./ServiceTracker";
import { useTheme } from "../ThemeContext";

const MatterCard = ({ matter: c, isOpen, onToggle }) => {
  const theme = useTheme();
  return (
    <div style={{ position: "relative", background: theme.cardBg, borderRadius: 10, border: isOpen ? `1px solid ${GOLD}40` : `1px solid ${theme.cardBorder}`, overflow: "hidden", transition: "border-color 0.3s" }}>
      {c.status && c.status.startsWith("SETTLED") && (
        <div aria-label="Settled" style={{ position: "absolute", top: 14, right: -28, width: 110, background: "#16a34a", color: "#fff", fontSize: 10, fontFamily: "'DM Sans', sans-serif", fontWeight: 800, letterSpacing: 2, textTransform: "uppercase", textAlign: "center", padding: "5px 0", transform: "rotate(45deg)", boxShadow: "0 2px 8px rgba(0,0,0,0.35)", pointerEvents: "none", zIndex: 10 }}>SETTLED</div>
      )}
      {c.badge === "DEFAULT" && (
        <div aria-label="Default" style={{ position: "absolute", top: 14, right: -28, width: 110, background: GOLD, color: "#fff", fontSize: 10, fontFamily: "'DM Sans', sans-serif", fontWeight: 800, letterSpacing: 2, textTransform: "uppercase", textAlign: "center", padding: "5px 0", transform: "rotate(45deg)", boxShadow: "0 2px 8px rgba(0,0,0,0.35)", pointerEvents: "none", zIndex: 10 }}>DEFAULT</div>
      )}
      {c.badge === "DISMISSED" && (
        <div aria-label="Dismissed" style={{ position: "absolute", top: 14, right: -28, width: 110, background: "#dc2626", color: "#fff", fontSize: 10, fontFamily: "'DM Sans', sans-serif", fontWeight: 800, letterSpacing: 2, textTransform: "uppercase", textAlign: "center", padding: "5px 0", transform: "rotate(45deg)", boxShadow: "0 2px 8px rgba(0,0,0,0.35)", pointerEvents: "none", zIndex: 10 }}>DISMISSED</div>
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
        <div style={{ display: "flex", gap: 8, alignItems: "center", flexWrap: "wrap" }}>
          <ClusterBadge cluster={c.cluster} />
          <TypeBadge type={c.type} />
          <StatusBadge status={c.status} />
          {c.archived && <ArchiveBadge />}
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
        </div>
      )}
    </div>
  );
};

export const MattersTab = ({ filteredCases, clusterFilter, setClusterFilter, typeFilter, setTypeFilter, searchQuery, setSearchQuery }) => {
  const theme = useTheme();
  const [expandedMatter, setExpandedMatter] = useState(null);

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
        {[null, 1, 2, 3, 4].map(c => (
          <button key={c ?? "all"} onClick={() => setClusterFilter(c)} style={{
            padding: "8px 14px", borderRadius: 6,
            border: clusterFilter === c ? `1px solid ${GOLD}` : `1px solid ${theme.filterInactiveBorder}`,
            background: clusterFilter === c ? `${GOLD}18` : theme.filterInactiveBg,
            color: clusterFilter === c ? GOLD : theme.filterInactiveColor,
            fontFamily: "'DM Sans', sans-serif", fontSize: 12, fontWeight: 600, cursor: "pointer"
          }}>{c === null ? "All" : c === 1 ? "CHP" : c === 2 ? "Parole/HOPE" : c === 3 ? "Vehicle" : "Writs"}</button>
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
        <span style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 12, color: theme.subtleText, marginLeft: "auto" }}>{filteredCases.length} of {PORTFOLIO.cases.length}</span>
      </div>

      {/* Matter Cards */}
      <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
        {filteredCases.length === 0 ? (
          <div style={{ padding: "40px 24px", textAlign: "center", fontFamily: "'DM Sans', sans-serif", fontSize: 14, color: theme.subtleText }}>
            No matters match your current filters.{" "}
            <button
              onClick={() => { setClusterFilter(null); setTypeFilter(null); setSearchQuery(""); }}
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
