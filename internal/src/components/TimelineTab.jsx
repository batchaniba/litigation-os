import { lazy, Suspense, useMemo, useState } from "react";
import { timeline } from "../data/timeline";
import { GOLD } from "../constants";
import { getPDTMidnight, parseEventDatePDT } from "../utils/dateUtils";
import { formatMatterRefs } from "../utils/matterRefs.js";
import { useTheme } from "../ThemeContext";

const CalendarTab = lazy(() => import("./CalendarTab").then((module) => ({ default: module.CalendarTab })));

export const TimelineTab = ({ showPastEvents, setShowPastEvents }) => {
  const theme = useTheme();
  const [view, setView] = useState("list");
  const cutoff = useMemo(() => getPDTMidnight(), []);
  const { pastEvents, recentEvents } = useMemo(() => {
    const sorted = [...timeline].sort((a, b) => parseEventDatePDT(a.date) - parseEventDatePDT(b.date));
    return {
      pastEvents: sorted.filter(t => parseEventDatePDT(t.date) < cutoff),
      recentEvents: sorted.filter(t => t.upcoming && parseEventDatePDT(t.date) >= cutoff),
    };
  }, [cutoff]);

  const renderEvent = (t, i) => {
    const typeColors = { filing: "#34D399", hearing: "#F472B6", ruling: "#60A5FA", event: "#94A3B8", milestone: GOLD };
    const col = typeColors[t.type] || "#94A3B8";
    const isUpcoming = t.upcoming && parseEventDatePDT(t.date) >= cutoff;
    return (
      <div key={i} style={{ position: "relative", marginBottom: 20, paddingLeft: 24 }}>
        <div style={{ position: "absolute", left: -26, top: 5, width: 12, height: 12, borderRadius: "50%", background: isUpcoming ? col : theme.bg, border: `2px solid ${col}`, boxShadow: isUpcoming ? `0 0 12px ${col}60` : "none" }} />
        <div style={{ background: isUpcoming ? `${col}10` : theme.cardBg, borderRadius: 8, padding: "12px 18px", border: isUpcoming ? `1px solid ${col}30` : `1px solid ${theme.cardBorder}` }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", gap: 12, flexWrap: "wrap" }}>
            <div>
              <span style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 12, fontWeight: 700, color: col }}>{t.date}</span>
              {isUpcoming && <span style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 10, marginLeft: 8, padding: "1px 6px", borderRadius: 4, background: `${col}20`, color: col, fontWeight: 700 }}>UPCOMING</span>}
            </div>
            <span style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 10, color: theme.subtleText, textTransform: "uppercase", letterSpacing: 1, fontWeight: 600 }}>{t.type}</span>
          </div>
          <p style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 13, color: theme.secondaryText, margin: "6px 0 0", lineHeight: 1.5 }}>{t.event}</p>
          <div style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 11, color: theme.subtleText, marginTop: 4 }}>Matter {formatMatterRefs(t.matters)}</div>
        </div>
      </div>
    );
  };

  return (
    <div>
      <h2 style={{ fontSize: 24, fontWeight: 700, color: theme.heading, marginBottom: 24 }}>Procedural Timeline</h2>

      {/* View controls */}
      <div style={{ display: "flex", gap: 8, marginBottom: 24, flexWrap: "wrap" }}>
        {view === "list" && (
          <button onClick={() => setShowPastEvents(v => !v)} style={{
            padding: "8px 16px", borderRadius: 6, border: `1px solid ${theme.cardBorder}`,
            background: theme.cardBg, color: theme.mutedText, fontFamily: "'DM Sans', sans-serif",
            fontSize: 12, fontWeight: 600, cursor: "pointer", letterSpacing: 0.3
          }}>
            {showPastEvents ? `Hide past events (${pastEvents.length})` : `Show past events (${pastEvents.length})`}
          </button>
        )}
        <button onClick={() => setView(v => (v === "list" ? "calendar" : "list"))} style={{
          padding: "8px 16px", borderRadius: 6, border: `1px solid ${GOLD}66`,
          background: `${GOLD}18`, color: GOLD, fontFamily: "'DM Sans', sans-serif",
          fontSize: 12, fontWeight: 700, cursor: "pointer", letterSpacing: 0.3
        }}>
          {view === "list" ? "Calendar View" : "List View"}
        </button>
      </div>

      {view === "list" ? (
        <div style={{ position: "relative", paddingLeft: 32 }}>
          <div style={{ position: "absolute", left: 11, top: 0, bottom: 0, width: 2, background: `linear-gradient(to bottom, ${GOLD}, ${theme.cardBorder})` }} />
          {showPastEvents && pastEvents.map((t, i) => renderEvent(t, i))}
          {/* Upcoming divider */}
          <div style={{ position: "relative", marginBottom: 24, paddingLeft: 24 }}>
            <div style={{ position: "absolute", left: -30, top: "50%", transform: "translateY(-50%)", width: 20, height: 20, borderRadius: "50%", background: GOLD, border: `2px solid ${GOLD}`, display: "flex", alignItems: "center", justifyContent: "center" }} />
            <div style={{ borderTop: `1px dashed ${GOLD}40`, paddingTop: 8 }}>
              <span style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 11, fontWeight: 700, color: GOLD, letterSpacing: 1, textTransform: "uppercase" }}>Upcoming & Present</span>
            </div>
          </div>
          {recentEvents.map((t, i) => renderEvent(t, i))}
        </div>
      ) : (
        <Suspense fallback={<div className="route-loading" role="status" aria-label="Loading calendar" />}><CalendarTab /></Suspense>
      )}
    </div>
  );
};
