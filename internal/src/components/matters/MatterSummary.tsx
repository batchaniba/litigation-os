import type { Matter, TimelineEvent } from "../../types/portfolio";
import { useTheme } from "../../ThemeContext";

function SummaryItem({ label, value, accent }: { label: string; value: string; accent?: boolean }) {
  const theme = useTheme();
  return <div className="matter-summary-item"><div className="detail-label">{label}</div><div style={{ color: accent ? "var(--gold)" : theme.secondaryText }}>{value}</div></div>;
}

export function MatterSummary({ matter, next, recent }: { matter: Matter; next?: TimelineEvent; recent?: TimelineEvent }) {
  const theme = useTheme();
  return (
    <section className="matter-summary" aria-label="Matter at a glance" style={{ background: theme.cardBg, borderColor: theme.cardBorder }}>
      <SummaryItem label="Status" value={matter.status} accent />
      <SummaryItem label="Next action" value={next?.event ?? "No upcoming action recorded"} />
      <SummaryItem label="Deadline" value={next?.date ?? "None recorded"} accent={Boolean(next)} />
      <SummaryItem label="Recent development" value={recent ? `${recent.date} — ${recent.event}` : "No recent development recorded"} />
    </section>
  );
}
