export function DeadlineBanner({ timeLeft, showClock, onToggle, theme }: { timeLeft: any; showClock: boolean; onToggle: () => void; theme: any }) {
  const countdown = `${String(timeLeft.days).padStart(2, "0")}d ${String(timeLeft.hours).padStart(2, "0")}h ${String(timeLeft.mins).padStart(2, "0")}m`;
  return (
    <section className="deadline-banner" style={{ background: theme.bannerBg }} aria-label="Next portfolio deadline">
      <div className="app-container deadline-row">
        <span className="deadline-label">⚖ Deadline Clock</span>
        {showClock && <span className="deadline-value" style={{ color: timeLeft.urgent ? "#ef4444" : theme.secondaryText }}>{countdown} · {timeLeft.label}</span>}
        <button className="deadline-toggle" onClick={onToggle} aria-expanded={showClock} style={{ border: theme.clockBtn.border, color: theme.clockBtn.color }}>{showClock ? "Hide" : "Show"}</button>
      </div>
    </section>
  );
}
