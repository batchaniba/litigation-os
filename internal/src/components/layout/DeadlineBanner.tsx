export function DeadlineBanner({ timeLeft, showClock, onToggle, theme }: { timeLeft: any; showClock: boolean; onToggle: () => void; theme: any }) {
  return (
    <section className="legacy-deadline-banner" style={{ background: theme.bannerBg, borderBottom: `1px solid ${timeLeft.urgent ? "#EF444440" : "#C8A84B30"}` }} aria-label="Next portfolio deadline">
      <div className="legacy-deadline-row">
        <div className="legacy-deadline-label">⚖ Deadline Clock</div>
        <div className="sr-only" aria-live="polite" aria-atomic="true">
          {showClock && timeLeft.label ? `Deadline: ${timeLeft.label}. ${timeLeft.days} days, ${timeLeft.hours} hours, ${timeLeft.mins} minutes remaining.` : ""}
        </div>
        {showClock && <div id="deadline-clock-display" className="legacy-deadline-display">
          <div className="legacy-clock-units" aria-hidden="true">
            {[{ value: timeLeft.days, label: "Days" }, { value: timeLeft.hours, label: "Hrs" }, { value: timeLeft.mins, label: "Min" }, { value: timeLeft.secs, label: "Sec" }].map(({ value, label }, index) => (
              <div key={label} className="legacy-clock-unit-wrap">
                {index > 0 && <span className="legacy-clock-colon">:</span>}
                <div className="legacy-clock-unit">
                  <div className={`legacy-clock-value${timeLeft.frozen ? " frozen" : ""}`} style={{ color: timeLeft.frozen || timeLeft.urgent ? "#EF4444" : "white" }}>{String(value).padStart(2, "0")}</div>
                  <div className="legacy-clock-caption">{label}</div>
                </div>
              </div>
            ))}
          </div>
          <div className="legacy-deadline-description">{timeLeft.label}</div>
        </div>}
        <button className="legacy-deadline-toggle" onClick={onToggle} aria-expanded={showClock} aria-controls="deadline-clock-display" style={{ border: theme.clockBtn.border, color: theme.clockBtn.color }}>
          {showClock ? "Hide" : "Show"}
        </button>
      </div>
    </section>
  );
}
