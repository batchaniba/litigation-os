import { Link } from "react-router";
import { GOLD } from "../../constants";

export const SANS = "'DM Sans', sans-serif";
export const SERIF = "'Cormorant Garamond', Georgia, serif";

/** GOLD uppercase label used as a page eyebrow or in-card field name. */
export function Eyebrow({ children, color = GOLD, as: Tag = "div", style, ...rest }) {
  return (
    <Tag
      style={{
        fontFamily: SANS,
        fontSize: 10,
        fontWeight: 700,
        letterSpacing: 4,
        textTransform: "uppercase",
        color,
        marginBottom: 8,
        ...style,
      }}
      {...rest}
    >
      {children}
    </Tag>
  );
}

/** Outcomes-style band heading: colored label, count chip, hairline. */
export function SectionHeading({ label, color, count, unit = "items", headingId }) {
  const singular = unit.replace(/s$/, "");
  const noun = count === 1 ? singular : `${singular}s`;
  return (
    <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 14 }}>
      <h3
        id={headingId}
        style={{
          fontFamily: SANS,
          fontSize: 11,
          fontWeight: 700,
          letterSpacing: 3,
          textTransform: "uppercase",
          color,
          margin: 0,
        }}
      >
        {label}
      </h3>
      <div
        style={{
          fontFamily: SANS,
          fontSize: 11,
          fontWeight: 600,
          background: `${color}18`,
          color,
          border: `1px solid ${color}44`,
          borderRadius: 20,
          padding: "2px 10px",
        }}
      >
        {count} {noun}
      </div>
      <div style={{ flex: 1, height: 1, background: `${color}30` }} />
    </div>
  );
}

/** Uppercase status / action / actor pill. */
export function StatusPill({ color, children, title }) {
  return (
    <div
      title={title}
      style={{
        fontFamily: SANS,
        fontSize: 10,
        fontWeight: 700,
        letterSpacing: 2,
        textTransform: "uppercase",
        background: `${color}18`,
        color,
        border: `1px solid ${color}44`,
        borderRadius: 20,
        padding: "4px 14px",
        whiteSpace: "nowrap",
      }}
    >
      {children}
    </div>
  );
}

/** Square matter-number badge; links when `to` is set. */
export function MatterBadge({ matter, color, to, className }) {
  const style = {
    width: 40,
    height: 40,
    borderRadius: 8,
    background: `${color}18`,
    border: `1px solid ${color}44`,
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    fontFamily: SANS,
    fontSize: 14,
    fontWeight: 700,
    color,
    flexShrink: 0,
    textDecoration: "none",
  };
  const label = matter == null ? "—" : String(matter);
  if (to) {
    return (
      <Link className={className} to={to} aria-label={`Matter ${matter}`} style={style}>
        {label}
      </Link>
    );
  }
  return (
    <div className={className} style={style}>
      {label}
    </div>
  );
}

export function ExpandChevron({ open, theme }) {
  return (
    <div
      aria-hidden
      style={{
        color: theme.subtleText,
        fontSize: 18,
        transition: "transform 0.3s",
        transform: open ? "rotate(180deg)" : "rotate(0)",
      }}
    >
      ▾
    </div>
  );
}

export function CardFrame({ theme, open = false, color, as: Tag = "div", style, children, ...rest }) {
  return (
    <Tag
      style={{
        background: theme.cardBg,
        borderRadius: 10,
        border: `1px solid ${open && color ? `${color}60` : theme.cardBorder}`,
        overflow: "hidden",
        transition: "border-color 0.2s",
        ...style,
      }}
      {...rest}
    >
      {children}
    </Tag>
  );
}

/** Gold (or tinted) left-border note used under Opinions / Outcomes lists. */
export function ContextNote({ theme, color = GOLD, title, children }) {
  return (
    <div
      style={{
        background: theme.cardBg,
        border: `1px solid ${color}30`,
        borderRadius: 10,
        padding: "20px 24px",
        borderLeft: `3px solid ${color}`,
      }}
    >
      {title ? (
        <div
          style={{
            fontFamily: SANS,
            fontSize: 10,
            fontWeight: 700,
            letterSpacing: 2,
            textTransform: "uppercase",
            color,
            marginBottom: 10,
          }}
        >
          {title}
        </div>
      ) : null}
      <div
        style={{
          fontFamily: SANS,
          fontSize: 13,
          color: theme.secondaryText,
          lineHeight: 1.8,
          margin: 0,
        }}
      >
        {children}
      </div>
    </div>
  );
}

export function FieldLabel({ children }) {
  return (
    <div
      style={{
        fontFamily: SANS,
        fontSize: 10,
        fontWeight: 700,
        letterSpacing: 2,
        textTransform: "uppercase",
        color: GOLD,
        marginBottom: 6,
      }}
    >
      {children}
    </div>
  );
}

export function BodyText({ theme, title, style, children }) {
  return (
    <p
      title={title}
      style={{
        fontFamily: SANS,
        fontSize: 13,
        color: theme.secondaryText,
        lineHeight: 1.6,
        margin: "0 0 14px",
        ...style,
      }}
    >
      {children}
    </p>
  );
}
