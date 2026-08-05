import { useState, useMemo } from "react";
import { timeline } from "../data/timeline";
import { cases } from "../data/matters";
import { GOLD } from "../constants";
import { getPDTMidnight } from "../utils/dateUtils";
import { groupEventsByDay, buildMonthGrid, dayKey, parseMatterNumbers } from "../utils/calendarUtils";
import { Modal } from "./Modal";

const TYPE_COLORS = { filing: "#34D399", hearing: "#F472B6", ruling: "#60A5FA", event: "#94A3B8", milestone: GOLD, deadline: "#EF4444" };
const WEEKDAYS = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
const MONTH_NAMES = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
const MAX_VISIBLE_PER_CELL = 3;

export const CalendarTab = () => {
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

  return (
    <div className="calendar-view">
      {/* Month nav header */}
      <div className="calendar-toolbar">
        <button onClick={() => goToMonth(-1)} aria-label="Previous month" className="calendar-nav-button">‹</button>
        <div className="calendar-month-title">
          {MONTH_NAMES[viewMonth]} {viewYear}
        </div>
        <div className="calendar-toolbar-actions">
          <button onClick={goToday} className="calendar-today-button">Today</button>
          <button onClick={() => goToMonth(1)} aria-label="Next month" className="calendar-nav-button">›</button>
        </div>
      </div>

      {/* Weekday header row */}
      <div className="calendar-grid calendar-weekdays">
        {WEEKDAYS.map(w => (
          <div key={w}>{w}</div>
        ))}
      </div>

      {/* 6x7 day grid */}
      <div className="calendar-grid calendar-days">
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
              className={`calendar-cell${isToday ? " is-today" : ""}${isSelected ? " is-selected" : ""}${cell.inMonth ? "" : " is-outside"}${events.length ? " has-events" : ""}`}
              style={{
                cursor: events.length > 0 ? "pointer" : "default",
              }}
            >
              <div className="calendar-day-number">
                {cell.date.getUTCDate()}
              </div>
              <div className="calendar-event-dots">
                {visible.map((e, i) => (
                  <span key={i} title={e.event} style={{ background: TYPE_COLORS[e.type] || "#94A3B8" }} />
                ))}
              </div>
              {overflow > 0 && (
                <div className="calendar-overflow">+{overflow} more</div>
              )}
            </div>
          );
        })}
      </div>

      {/* Type legend */}
      <div className="calendar-legend">
        {Object.entries(TYPE_COLORS).map(([type, color]) => (
          <div key={type} className="calendar-legend-item">
            <span className="calendar-legend-dot" style={{ background: color }} />
            <span>{type}</span>
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
          <div key={i} className="calendar-modal-event">
            <span className="calendar-event-type" style={{ color: TYPE_COLORS[e.type] }}>{e.type}</span>
            <p>{e.event}</p>
            <div className="calendar-matter-pills">
              {resolveMatters(e.matters).map((m, j) => (
                <span key={j}>
                  {m.label}{m.caption ? ` — ${m.caption}` : ""}
                </span>
              ))}
            </div>
          </div>
        ))}
      </Modal>

      {/* Ungroundable-date events */}
      {ungrounded.length > 0 && (
        <section className="calendar-undated">
          <h3>
            Approximate / Undated Events ({ungrounded.length})
          </h3>
          {ungrounded.map((e, i) => (
            <div key={i} className="calendar-undated-event">
              <span style={{ color: TYPE_COLORS[e.type] }}>{e.date}</span>
              <span>{e.event}</span>
            </div>
          ))}
        </section>
      )}
    </div>
  );
};
