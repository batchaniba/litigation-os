import { useId, useState, type CSSProperties } from "react";

/**
 * Matter prose (key_facts, procedural_status, risk) runs long — the portfolio
 * median is ~280–420 words and the worst records exceed 1,600. Rather than
 * rewrite legal text, clamp it on screen and keep the full record one click
 * away. Nothing is truncated in the DOM, so print, find-in-page, and the
 * Markdown export still see the whole string.
 */

/** Below this length a toggle costs more than it saves — render plain prose. */
export const COLLAPSE_THRESHOLD = 320;

/** Lines shown while collapsed. Roughly the threshold at .detail-copy sizing. */
const DEFAULT_LINES = 4;

interface CollapsibleProseProps {
  text: string;
  /** Accessible name for the toggle: "Show full key facts". */
  label: string;
  className?: string;
  style?: CSSProperties;
  lines?: number;
  threshold?: number;
}

export function CollapsibleProse({
  text,
  label,
  className,
  style,
  lines = DEFAULT_LINES,
  threshold = COLLAPSE_THRESHOLD,
}: CollapsibleProseProps) {
  const [expanded, setExpanded] = useState(false);
  const id = useId();
  const value = (text ?? "").trim();
  const paragraphClass = className ? `detail-copy ${className}` : "detail-copy";

  if (!value) return null;
  if (value.length <= threshold) {
    return <p className={paragraphClass} style={style}>{value}</p>;
  }

  return (
    <div className="collapsible-prose">
      <p
        id={id}
        className={expanded ? paragraphClass : `${paragraphClass} is-clamped`}
        style={expanded ? style : { ...style, WebkitLineClamp: lines }}
      >
        {value}
      </p>
      <button
        type="button"
        className="collapsible-prose-toggle"
        aria-expanded={expanded}
        aria-controls={id}
        onClick={(event) => {
          // Guard against a future caller nesting this inside a clickable
          // region (MatterCard's expand/collapse control is one click away).
          event.stopPropagation();
          setExpanded((open) => !open);
        }}
      >
        {expanded ? "Show less" : `Show full ${label}`}
      </button>
    </div>
  );
}
