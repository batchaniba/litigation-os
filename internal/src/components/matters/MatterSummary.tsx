import type { Matter, TimelineEvent } from "../../types/portfolio";
import { effectiveStatusLabel } from "../../utils/statusLabel";

function SummaryItem({ label, value, accent }: { label: string; value: string; accent?: boolean }) {
  return (
    <div className="matter-summary-item">
      <div className="detail-label">{label}</div>
      <div className={accent ? "matter-summary-value accent" : "matter-summary-value"}>{value}</div>
    </div>
  );
}

export function MatterSummary({ matter, next, recent }: { matter: Matter; next?: TimelineEvent; recent?: TimelineEvent }) {
  const statusLabel = effectiveStatusLabel(matter, { next, recent });
  return (
    <section className="matter-summary" aria-label="Matter at a glance">
      <SummaryItem label="Status" value={statusLabel} accent />
      <SummaryItem label="Next action" value={next?.event ?? "No upcoming action recorded"} />
      <SummaryItem label="Deadline" value={next?.date ?? "None recorded"} accent={Boolean(next)} />
      <SummaryItem label="Recent development" value={recent ? `${recent.date} — ${recent.event}` : "No recent development recorded"} />
    </section>
  );
}
