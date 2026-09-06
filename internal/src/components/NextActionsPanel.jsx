import { Link } from "react-router";
import { clipEvent, daysLabel } from "../utils/nextActionsView";

const BANDS = [
  ["overdue", "Past due"],
  ["critical", "Next 3 days"],
  ["soon", "This week"],
  ["upcoming", "Next 30 days"],
];

const ACTOR_LABEL = {
  you: "your desk",
  unknown: "your desk",
  opposing: "opposing",
  agency: "court / agency",
};

function groupVisible(items, mineOnly) {
  const visible = items.filter((item) => {
    if (item.urgency === "later") return false;
    if (!mineOnly) return true;
    return item.actor === "you" || item.actor === "unknown";
  });
  return BANDS.map(([key, label]) => ({
    key,
    label,
    items: visible.filter((item) => item.urgency === key),
  })).filter((band) => band.items.length > 0);
}

export function NextActionsPanel({ queue, mineOnly, onMineOnlyChange }) {
  const bands = groupVisible(queue.items, mineOnly);
  const gaps = queue.gaps ?? [];
  const undated = (queue.undated ?? []).filter((item) => {
    if (!mineOnly) return true;
    return item.actor === "you" || item.actor === "unknown";
  });

  return (
    <section className="dashboard-panel next-actions" aria-labelledby="next-actions-heading">
      <div className="next-actions-header">
        <h3 id="next-actions-heading" className="dashboard-heading">What’s next</h3>
        <label className="next-actions-filter">
          <input
            type="checkbox"
            checked={mineOnly}
            onChange={(event) => onMineOnlyChange(event.target.checked)}
          />
          My desk only
        </label>
      </div>

      {bands.length === 0 && gaps.length === 0 && undated.length === 0 ? (
        <p className="next-actions-empty">Nothing dated in the next {queue.horizonDays} days.</p>
      ) : null}

      {bands.map((band) => (
        <div key={band.key} className={`next-actions-band is-${band.key}`}>
          <h4 className="next-actions-band-label">{band.label}</h4>
          <ul className="next-actions-list">
            {band.items.map((item) => {
              const matter = item.matters[0];
              const inferred = item.actorSource === "inferred";
              return (
                <li key={`${item.dateKey}-${matter}-${item.event.slice(0, 40)}`} className="next-actions-item">
                  <div className="next-actions-when">
                    <span className="next-actions-date">{item.date}</span>
                    <span className="next-actions-days">{daysLabel(item.daysOut)}</span>
                  </div>
                  <div className="next-actions-body">
                    <p className="next-actions-event" title={item.event}>{clipEvent(item.event)}</p>
                    <div className="next-actions-meta">
                      {matter != null ? (
                        <Link className="next-actions-matter" to={`/matters/${matter}`}>
                          Matter {matter}
                        </Link>
                      ) : null}
                      <span className="next-actions-action">{item.action}</span>
                      <span
                        className={`next-actions-actor is-${item.actor}`}
                        title={inferred ? "Inferred from the event text — verify" : undefined}
                      >
                        {ACTOR_LABEL[item.actor] ?? item.actor}
                        {inferred ? " · inferred" : null}
                      </span>
                    </div>
                  </div>
                </li>
              );
            })}
          </ul>
        </div>
      ))}

      {undated.length > 0 ? (
        <div className="next-actions-band is-undated">
          <h4 className="next-actions-band-label">Not on one calendar day</h4>
          <ul className="next-actions-list">
            {undated.map((item) => (
              <li key={`${item.date}-${item.event.slice(0, 40)}`} className="next-actions-item">
                <div className="next-actions-when">
                  <span className="next-actions-date">{item.date}</span>
                </div>
                <p className="next-actions-event" title={item.event}>{clipEvent(item.event)}</p>
              </li>
            ))}
          </ul>
        </div>
      ) : null}

      {gaps.length > 0 ? (
        <div className="next-actions-gaps">
          <h4 className="dashboard-subheading">No dated next step</h4>
          <p className="next-actions-gaps-copy">
            Active or pre-filing matters with nothing on the calendar. These are drifting.
          </p>
          <ul className="next-actions-gap-list">
            {gaps.map((gap) => (
              <li key={gap.number}>
                <Link className="next-actions-gap" to={`/matters/${gap.number}`}>
                  <span className="dashboard-matter-badge">Matter {gap.number}</span>
                  <span className="next-actions-gap-caption">
                    {gap.caption}
                    {gap.case_no ? ` (${gap.case_no})` : ""}
                  </span>
                  {gap.status_label ? (
                    <span className="next-actions-gap-status">{gap.status_label}</span>
                  ) : null}
                </Link>
              </li>
            ))}
          </ul>
        </div>
      ) : null}

      <p className="next-actions-caveat">
        Dates as recorded in the portfolio. Confirm against the docket before relying on one.
        Same ranking as <code>npm run next</code>.
      </p>
    </section>
  );
}
