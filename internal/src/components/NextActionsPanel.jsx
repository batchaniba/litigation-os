import { useState } from "react";
import { Link } from "react-router";
import { GOLD } from "../constants";
import { useTheme } from "../ThemeContext";
import { queueBands } from "../../scripts/lib/next-actions.mjs";
import { clipEvent, daysLabel } from "../utils/nextActionsView";
import {
  BodyText,
  CardFrame,
  ContextNote,
  ExpandChevron,
  Eyebrow,
  FieldLabel,
  MatterBadge,
  SANS,
  SERIF,
  SectionHeading,
  StatusPill,
} from "./ui/portfolioChrome";

const RED = "#dc2626";
const AMBER = "#d97706";
const BLUE = "#0284c7";
const SLATE = "#64748b";
const GREEN = "#16a34a";

const BAND_COLORS = {
  overdue: RED,
  opposing_overdue: SLATE,
  critical: AMBER,
  soon: BLUE,
  upcoming: SLATE,
};

const ACTOR_PILL = {
  you: { color: GREEN, label: "Your desk" },
  unknown: { color: GREEN, label: "Your desk" },
  opposing: { color: SLATE, label: "Opposing" },
  agency: { color: SLATE, label: "Court / agency" },
  court: { color: SLATE, label: "Court / agency" },
};

function isYours(item) {
  return item.actor === "you" || item.actor === "unknown";
}

export function NextActionsPanel({ queue, mineOnly, onMineOnlyChange }) {
  const theme = useTheme();
  const bands = queueBands(queue.items, {
    today: queue.today,
    horizonDays: queue.horizonDays,
    mineOnly,
  }).map((band) => ({ ...band, color: BAND_COLORS[band.key] ?? SLATE }));
  const populated = bands.filter((band) => band.items.length > 0);
  const gaps = queue.gaps ?? [];
  const undated = (queue.undated ?? []).filter((item) => (mineOnly ? isYours(item) : true));
  const empty = populated.length === 0 && gaps.length === 0 && undated.length === 0;

  return (
    <section aria-labelledby="next-actions-heading" style={{ marginBottom: 36 }}>
      <div
        style={{
          display: "flex",
          flexWrap: "wrap",
          alignItems: "flex-start",
          justifyContent: "space-between",
          gap: 16,
          marginBottom: 28,
        }}
      >
        <div>
          <Eyebrow>Docket queue</Eyebrow>
          <h2
            id="next-actions-heading"
            style={{ fontSize: 28, fontWeight: 700, color: theme.heading, margin: "0 0 6px" }}
          >
            What’s next
          </h2>
          <p
            style={{
              fontFamily: SANS,
              fontSize: 13,
              color: theme.mutedText,
              margin: 0,
              maxWidth: 620,
            }}
          >
            Past due first, then the next {queue.horizonDays} days from today in Pacific time.
            Confirm against the docket before relying on a date.
          </p>
        </div>
        <label
          style={{
            display: "inline-flex",
            alignItems: "center",
            gap: 8,
            fontFamily: SANS,
            fontSize: 12,
            fontWeight: 600,
            color: theme.mutedText,
            cursor: "pointer",
            paddingTop: 6,
          }}
        >
          <input
            type="checkbox"
            checked={mineOnly}
            onChange={(event) => onMineOnlyChange(event.target.checked)}
            style={{ accentColor: GOLD }}
          />
          My desk only
        </label>
      </div>

      <div style={{ display: "flex", gap: 12, flexWrap: "wrap", marginBottom: empty ? 16 : 32 }}>
        {bands.map((band) => (
          <SummaryPill
            key={band.key}
            label={band.label}
            count={band.count}
            color={band.color}
            theme={theme}
          />
        ))}
      </div>

      {empty ? (
        <div
          style={{
            background: theme.cardBg,
            border: `1px solid ${theme.cardBorder}`,
            borderRadius: 10,
            padding: "18px 24px",
            marginBottom: 24,
            fontFamily: SANS,
            fontSize: 13,
            color: theme.mutedText,
            lineHeight: 1.6,
          }}
        >
          Nothing dated in the next {queue.horizonDays} days.
        </div>
      ) : null}

      {populated.map((band) => (
        <BandSection
          key={band.key}
          headingId={`next-actions-band-${band.key}`}
          label={band.label}
          color={band.color}
          count={band.items.length}
        >
          {band.items.map((item) => (
            <ActionCard
              key={`${item.dateKey}-${item.matters[0]}-${item.event.slice(0, 40)}`}
              item={item}
              color={band.color}
              theme={theme}
            />
          ))}
        </BandSection>
      ))}

      {undated.length > 0 ? (
        <BandSection
          headingId="next-actions-band-undated"
          label="Not on one calendar day"
          color={GOLD}
          count={undated.length}
        >
          {undated.map((item) => (
            <ActionCard
              key={`${item.date}-${item.event.slice(0, 40)}`}
              item={item}
              color={GOLD}
              theme={theme}
            />
          ))}
        </BandSection>
      ) : null}

      {gaps.length > 0 ? (
        <BandSection
          headingId="next-actions-band-gaps"
          label="No dated next step"
          color={GOLD}
          count={gaps.length}
          unit="matters"
          intro={
            <p
              style={{
                fontFamily: SANS,
                fontSize: 13,
                color: theme.mutedText,
                margin: "0 0 14px",
                lineHeight: 1.6,
              }}
            >
              Active or pre-filing matters with nothing on the calendar. These are drifting.
            </p>
          }
        >
          {gaps.map((gap) => (
            <GapCard key={gap.number} gap={gap} theme={theme} />
          ))}
        </BandSection>
      ) : null}

      <ContextNote theme={theme} title="On the calendar">
        Dates as recorded in the portfolio, bucketed from the viewer’s current Pacific date.
        Next 3 days is today through +3. This week is the current Sunday–Saturday and includes
        those next-3-days items. Next 30 days includes this week. Each row is listed once,
        most urgent first. Vacated, satisfied, settled, and archived items are omitted.
        Confirm against the docket before relying on a date. Same ranking as{" "}
        <code style={{ fontSize: "0.95em" }}>npm run next</code>.
      </ContextNote>
    </section>
  );
}

function SummaryPill({ label, count, color, theme }) {
  return (
    <div
      style={{
        background: theme.cardBg,
        border: `1px solid ${color}44`,
        borderRadius: 10,
        padding: "16px 24px",
        borderTop: `3px solid ${color}`,
      }}
    >
      <div
        style={{
          fontFamily: SANS,
          fontSize: 9,
          fontWeight: 700,
          letterSpacing: 3,
          textTransform: "uppercase",
          color,
          marginBottom: 6,
        }}
      >
        {label}
      </div>
      <div
        style={{
          fontFamily: SERIF,
          fontSize: 32,
          fontWeight: 700,
          color: theme.heading,
          lineHeight: 1,
        }}
      >
        {count}
      </div>
    </div>
  );
}

function BandSection({ headingId, label, color, count, unit, intro, children }) {
  return (
    <div style={{ marginBottom: 32 }}>
      <SectionHeading label={label} color={color} count={count} unit={unit} headingId={headingId} />
      {intro}
      <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>{children}</div>
    </div>
  );
}

function ActionCard({ item, color, theme }) {
  const [open, setOpen] = useState(false);
  const matter = item.matters?.[0];
  const inferred = item.actorSource === "inferred";
  const actor = ACTOR_PILL[item.actor] ?? { color: SLATE, label: item.actor };
  const compact = String(item.event ?? "").replace(/\s+/g, " ").trim();
  const clipped = clipEvent(item.event);
  const actorTitle = inferred ? "Inferred from the event text — verify" : undefined;
  const actorText = inferred ? `${actor.label} · inferred` : actor.label;

  return (
    <CardFrame theme={theme} open={open} color={color}>
      <div style={{ display: "flex", alignItems: "stretch" }}>
        <div style={{ display: "flex", alignItems: "center", padding: "18px 0 18px 24px" }}>
          <MatterBadge
            className="next-actions-matter"
            matter={matter}
            color={color}
            to={matter != null ? `/matters/${matter}` : undefined}
          />
        </div>
        <button
          type="button"
          className="next-actions-expand"
          onClick={() => setOpen((value) => !value)}
          aria-expanded={open}
          style={{
            flex: 1,
            minWidth: 0,
            padding: "18px 24px 18px 18px",
            cursor: "pointer",
            display: "flex",
            alignItems: "center",
            gap: 18,
            flexWrap: "wrap",
            background: "transparent",
            border: "none",
            textAlign: "left",
            color: "inherit",
            font: "inherit",
            lineHeight: "inherit",
          }}
        >
          <div style={{ flex: 1, minWidth: 200 }}>
            <div
              style={{
                fontFamily: SANS,
                fontSize: 14,
                fontWeight: 600,
                lineHeight: 1.45,
                color: theme.heading,
                marginBottom: 3,
              }}
            >
              {clipped}
            </div>
            <div style={{ fontFamily: SANS, fontSize: 12, color: theme.subtleText }}>
              {item.daysOut != null ? daysLabel(item.daysOut) : "Not a single calendar day"}
            </div>
          </div>
          <StatusPill color={color}>{item.action}</StatusPill>
          <StatusPill color={actor.color} title={actorTitle}>
            {actorText}
          </StatusPill>
          <div
            style={{
              fontFamily: SANS,
              fontSize: 12,
              color: theme.mutedText,
              whiteSpace: "nowrap",
            }}
          >
            {item.date}
          </div>
          <ExpandChevron open={open} theme={theme} />
        </button>
      </div>

      {open ? (
        <div style={{ padding: "0 24px 24px", borderTop: `1px solid ${theme.cardBorder}` }}>
          <div style={{ paddingTop: 18 }}>
            <FieldLabel>Event</FieldLabel>
            <BodyText theme={theme} style={{ lineHeight: 1.7 }}>{compact}</BodyText>
            {inferred ? (
              <>
                <FieldLabel>Actor</FieldLabel>
                <BodyText theme={theme}>
                  {actor.label}. Inferred from the event text — verify.
                </BodyText>
              </>
            ) : null}
            {item.source ? (
              <>
                <FieldLabel>Source</FieldLabel>
                <BodyText theme={theme}>
                  <a
                    href={item.source}
                    target="_blank"
                    rel="noreferrer"
                    style={{ color: GOLD, fontWeight: 600, textDecoration: "none" }}
                  >
                    source PDF
                  </a>
                </BodyText>
              </>
            ) : null}
            {item.verified_at ? (
              <>
                <FieldLabel>Verified</FieldLabel>
                <BodyText
                  theme={theme}
                  title={`Source: ${item.source_type || "unknown"} · Confidence: ${item.confidence || "unknown"}`}
                >
                  verified {item.verified_at}
                </BodyText>
              </>
            ) : null}
            {item.precedentPeers?.length ? (
              <>
                <FieldLabel>Also</FieldLabel>
                <BodyText theme={theme}>
                  {item.precedentPeers.map((peer, index) => (
                    <span key={peer}>
                      {index > 0 ? ", " : null}
                      <Link
                        to={`/matters/${peer}`}
                        style={{ color: GOLD, fontWeight: 700, textDecoration: "none" }}
                      >
                        M{peer}
                      </Link>
                    </span>
                  ))}
                </BodyText>
              </>
            ) : null}
          </div>
        </div>
      ) : null}
    </CardFrame>
  );
}

function GapCard({ gap, theme }) {
  return (
    <CardFrame
      as={Link}
      to={`/matters/${gap.number}`}
      className="next-actions-gap"
      aria-label={`Matter ${gap.number}${gap.caption ? `: ${gap.caption}` : ""}`}
      theme={theme}
      color={GOLD}
      style={{
        display: "flex",
        alignItems: "center",
        gap: 18,
        flexWrap: "wrap",
        padding: "18px 24px",
        textDecoration: "none",
        color: "inherit",
      }}
    >
      <MatterBadge matter={gap.number} color={GOLD} />
      <div style={{ flex: 1, minWidth: 200 }}>
        <div
          style={{
            fontFamily: SANS,
            fontSize: 14,
            fontWeight: 600,
            lineHeight: 1.45,
            color: theme.heading,
            marginBottom: 3,
          }}
        >
          {gap.caption}
        </div>
        <div style={{ fontFamily: SANS, fontSize: 12, color: theme.subtleText }}>
          {gap.case_no || "No case number yet"}
        </div>
      </div>
      {gap.status_label ? <StatusPill color={GOLD}>{gap.status_label}</StatusPill> : null}
    </CardFrame>
  );
}
