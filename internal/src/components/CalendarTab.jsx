import { useState, useMemo } from "react";
import { timeline } from "../data/timeline";
import { cases } from "../data/matters";
import { GOLD } from "../constants";
import { getPDTMidnight } from "../utils/dateUtils";
import { groupEventsByDay, buildMonthGrid, dayKey, parseMatterNumbers } from "../utils/calendarUtils";
import { useTheme } from "../ThemeContext";
import { Modal } from "./Modal";

const TYPE_COLORS = { filing: "#34D399", hearing: "#F472B6", ruling: "#60A5FA", event: "#94A3B8", milestone: GOLD, deadline: "#EF4444" };
const WEEKDAYS = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
const MONTH_NAMES = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
const MAX_VISIBLE_PER_CELL = 3;

export const CalendarTab = () => {
  const theme = useTheme();
  const today = useMemo(() => getPDTMidnight(), []);
  const todayKey = useMemo(() => dayKey(today), [today]);

  const [viewYear, setViewYear] = useState(today.getUTCFullYear());
  const [viewMonth, setViewMonth] = useState(today.getUTCMonth());
  const [selectedKey, setSelectedKey] = useState(null);

  const { byDay, ungrounded } = useMemo(() => groupEventsByDay(timeline), []);
  const cells = useMemo(() => buildMonthGrid(viewYear, viewMonth), [viewYear, viewMonth]);

  const goToMonth = (delta) => {
    let m = viewMonth + delta, y = viewYear;
    if (m < 0) { m = 11; y -= 1; } else if (m > 11) { m = 0; y += 1; }
    setViewMonth(m); setViewYear(y);
  };
  const goToday = () => { setViewYear(today.getUTCFullYear()); setViewMonth(today.getUTCMonth()); };

  const selectedEvents = byDay.get(selectedKey) || [];

  const resolveMatters = (mattersStr) => {
    const { all, numbers, label } = parseMatterNumbers(mattersStr);
    if (all || numbers.length === 0) return [{ label }];
    return numbers.map(n => {
      const c = cases.find(cs => cs.number === n);
      return { label: `Matter ${n}`, caption: c?.caption };
    });
  };

  const navBtnStyle = {
    width: 32, height: 32, borderRadius: 6, border: `1px solid ${theme.cardBorder}`,
    background: theme.cardBg, color: theme.secondaryText, fontSize: 16, cursor: "pointer",
    display: "flex", alignItems: "center", justifyContent: "center", lineHeight: 1,
  };

  return (
    <div>
      {/* Month nav header */}
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 16 }}>
        <button onClick={() => goToMonth(-1)} aria-label="Previous month" style={navBtnStyle}>‹</button>
        <div style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 16, fontWeight: 700, color: theme.heading }}>
          {MONTH_NAMES[viewMonth]} {viewYear}
        </div>
        <div style={{ display: "flex", gap: 8 }}>
          <button onClick={goToday} style={{
            padding: "0 14px", height: 32, borderRadius: 6, border: `1px solid ${GOLD}66`,
            background: `${GOLD}18`, color: GOLD, fontFamily: "'DM Sans', sans-serif",
            fontSize: 12, fontWeight: 700, cursor: "pointer", letterSpacing: 0.3,
          }}>Today</button>
          <button onClick={() => goToMonth(1)} aria-label="Next month" style={navBtnStyle}>›</button>
        </div>
      </div>

      {/* Weekday header row */}
      <div style={{ display: "grid", gridTemplateColumns: "repeat(7, 1fr)", marginBottom: 4 }}>
        {WEEKDAYS.map(w => (
          <div key={w} style={{ textAlign: "center", fontFamily: "'DM Sans', sans-serif", fontSize: 10, fontWeight: 700, color: theme.subtleText, letterSpacing: 1, textTransform: "uppercase", padding: "4px 0" }}>{w}</div>
        ))}
      </div>

      {/* 6x7 day grid */}
      <div style={{ display: "grid", gridTemplateColumns: "repeat(7, 1fr)", gap: 4, marginBottom: 24 }}>
        {cells.map(cell => {
          const events = byDay.get(cell.key) || [];
          const isToday = cell.key === todayKey;
          const isSelected = cell.key === selectedKey;
          const visible = events.slice(0, MAX_VISIBLE_PER_CELL);
          const overflow = events.length - visible.length;
          return (
            <div
              key={cell.key}
              role="button"
              tabIndex={0}
              aria-current={isToday ? "date" : undefined}
              aria-label={`${MONTH_NAMES[cell.date.getUTCMonth()]} ${cell.date.getUTCDate()}, ${cell.date.getUTCFullYear()}${events.length ? `, ${events.length} event(s)` : ""}`}
              onClick={() => { if (events.length > 0) setSelectedKey(cell.key); }}
              onKeyDown={e => { if ((e.key === "Enter" || e.key === " ") && events.length > 0) { e.preventDefault(); setSelectedKey(cell.key); } }}
              style={{
                minHeight: 84, padding: "6px 8px", borderRadius: 6, cursor: events.length > 0 ? "pointer" : "default",
                opacity: cell.inMonth ? 1 : 0.4,
                background: isSelected ? `${GOLD}15` : theme.cardBg,
                border: isToday ? `2px solid ${GOLD}` : `1px solid ${theme.cardBorder}`,
              }}
            >
              <div style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 12, fontWeight: isToday ? 700 : 500, color: isToday ? GOLD : theme.secondaryText }}>
                {cell.date.getUTCDate()}
              </div>
              <div style={{ display: "flex", flexWrap: "wrap", gap: 3, marginTop: 4 }}>
                {visible.map((e, i) => (
                  <span key={i} title={e.event} style={{ width: 6, height: 6, borderRadius: "50%", background: TYPE_COLORS[e.type] || "#94A3B8" }} />
                ))}
              </div>
              {overflow > 0 && (
                <div style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 9, color: theme.subtleText, marginTop: 2 }}>+{overflow} more</div>
              )}
            </div>
          );
        })}
      </div>

      {/* Type legend */}
      <div style={{ display: "flex", gap: 16, flexWrap: "wrap", marginBottom: 24 }}>
        {Object.entries(TYPE_COLORS).map(([type, color]) => (
          <div key={type} style={{ display: "flex", alignItems: "center", gap: 6 }}>
            <span style={{ width: 8, height: 8, borderRadius: "50%", background: color }} />
            <span style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 11, color: theme.subtleText, textTransform: "capitalize" }}>{type}</span>
          </div>
        ))}
      </div>

      {/* Day-detail modal */}
      <Modal
        isOpen={selectedKey !== null}
        onClose={() => setSelectedKey(null)}
        title={selectedKey ? `${selectedKey}${selectedKey === todayKey ? " (Today)" : ""}` : ""}
      >
        {selectedEvents.map((e, i) => (
          <div key={i} style={{ marginBottom: i === selectedEvents.length - 1 ? 0 : 14 }}>
            <span style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 10, fontWeight: 700, color: TYPE_COLORS[e.type] || theme.subtleText, textTransform: "uppercase", letterSpacing: 1 }}>{e.type}</span>
            <p style={{ margin: "4px 0", fontFamily: "'DM Sans', sans-serif", fontSize: 13, color: theme.secondaryText, lineHeight: 1.5 }}>{e.event}</p>
            <div style={{ display: "flex", flexWrap: "wrap", gap: 6 }}>
              {resolveMatters(e.matters).map((m, j) => (
                <span key={j} style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 11, color: theme.badgeNumColor, background: theme.badgeNumBg, borderRadius: 4, padding: "2px 8px" }}>
                  {m.label}{m.caption ? ` — ${m.caption}` : ""}
                </span>
              ))}
            </div>
          </div>
        ))}
      </Modal>

      {/* Ungroundable-date events */}
      {ungrounded.length > 0 && (
        <div style={{ background: theme.cardBg, borderRadius: 10, padding: 20, border: `1px solid ${theme.cardBorder}` }}>
          <h3 style={{ fontSize: 13, fontWeight: 700, color: theme.subtleText, margin: "0 0 12px", fontFamily: "'DM Sans', sans-serif", textTransform: "uppercase", letterSpacing: 1 }}>
            Approximate / Undated Events ({ungrounded.length})
          </h3>
          {ungrounded.map((e, i) => (
            <div key={i} style={{ marginBottom: 10 }}>
              <span style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 12, fontWeight: 700, color: TYPE_COLORS[e.type] || theme.subtleText }}>{e.date}</span>
              <span style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 12, color: theme.secondaryText, marginLeft: 8 }}>{e.event}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
