import type { Matter, TimelineEvent } from "../../types/portfolio";

function SummaryItem({
  label,
  value,
  accent,
  empty,
}: {
  label: string;
  value: string;
  accent?: boolean;
  empty?: boolean;
}) {
  const classes = ["matter-summary-value"];
  if (accent) classes.push("accent");
  if (empty) classes.push("is-empty");
  return (
    <div className="matter-summary-item">
      <div className="detail-label">{label}</div>
      {/* title carries the untruncated text — cells are line-clamped so one long
          value can't blow out the height of the whole strip. */}
      <div className={classes.join(" ")} title={empty ? undefined : value}>
        {value}
      </div>
    </div>
  );
}

export function MatterSummary({ matter, next, recent }: { matter: Matter; next?: TimelineEvent; recent?: TimelineEvent }) {
  return (
    <section className="matter-summary" aria-label="Matter at a glance">
      <SummaryItem label="Status" value={matter.status_label} accent />
      <SummaryItem
        label="Next action"
        value={next?.event ?? "None scheduled"}
        empty={!next}
      />
      <SummaryItem
        label="Deadline"
        value={next?.date ?? "—"}
        accent={Boolean(next)}
        empty={!next}
      />
      <SummaryItem
        label="Recent development"
        value={recent ? `${recent.date} — ${recent.event}` : "None recorded"}
        empty={!recent}
      />
    </section>
  );
}
