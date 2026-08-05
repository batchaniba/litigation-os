import { GOLD } from "../constants";
import { phaseLabel, proceedingLabel } from "../utils/matterProceeding";

const LIFECYCLE_STYLE = {
  active: { color: "#34D399", bg: "rgba(52,211,153,0.12)" },
  pre_filing: { color: GOLD, bg: "rgba(200,168,75,0.12)" },
  settled: { color: "#16a34a", bg: "rgba(22,163,74,0.12)" },
  dismissed: { color: "#F87171", bg: "rgba(248,113,113,0.12)" },
  abandoned: { color: "#94A3B8", bg: "rgba(148,163,184,0.15)" },
  closed: { color: "#6B7280", bg: "rgba(107,114,128,0.15)" },
};

const PHASE_STYLE = {
  stayed: { color: "#FBBF24", border: "#FBBF2440" },
  demurrer: { color: "#F472B6", border: "#F472B640" },
  fr_pending: { color: "#F472B6", border: "#F472B640" },
  district_review: { color: "#F472B6", border: "#F472B640" },
  mtd_briefing: { color: "#F472B6", border: "#F472B640" },
  under_submission: { color: "#A78BFA", border: "#A78BFA40" },
  responsive_deadline: { color: "#0d9488", border: "#0d948840" },
  service: { color: "#0d9488", border: "#0d948840" },
  default: { color: "#16a34a", border: "#16a34a40" },
  screening_ifp: { color: GOLD, border: `${GOLD}40` },
  pre_filing: { color: "#eab308", border: "#eab30840" },
  cmc: { color: "#60A5FA", border: "#60A5FA40" },
  hearing: { color: "#60A5FA", border: "#60A5FA40" },
};

export const StatusBadge = ({ status, lifecycle }) => {
  let color = "#6B7280";
  let bg = "rgba(107,114,128,0.15)";
  if (lifecycle && LIFECYCLE_STYLE[lifecycle]) {
    ({ color, bg } = LIFECYCLE_STYLE[lifecycle]);
  } else if (typeof status === "string") {
    if (status.includes("Filed") || status.includes("Active")) { color = "#34D399"; bg = "rgba(52,211,153,0.12)"; }
    if (status.includes("Gov. Claim") || status.includes("45-day")) { color = GOLD; bg = "rgba(200,168,75,0.12)"; }
    if (status.includes("MTD") || status.includes("Hearing")) { color = "#F472B6"; bg = "rgba(244,114,182,0.12)"; }
    if (status.includes("DISMISSED")) { color = "#F87171"; bg = "rgba(248,113,113,0.12)"; }
  }
  const label = typeof status === "string" ? status : "";
  return <span style={{ fontSize: 11, padding: "3px 10px", borderRadius: 20, color, background: bg, fontWeight: 600, whiteSpace: "nowrap", letterSpacing: 0.3 }}>{label.length > 40 ? label.slice(0, 38) + "…" : label}</span>;
};

export const ClusterBadge = ({ cluster }) => {
  const labels = { 1: "CHP Stop", 2: "Parole/HOPE", 3: "Employment", 4: "Writs/Habeas", 5: "Consumer Fraud" };
  const colors = { 1: "#60A5FA", 2: "#A78BFA", 3: "#FBBF24", 4: "#34D399", 5: "#F97316" };
  return <span style={{ fontSize: 10, padding: "2px 8px", borderRadius: 4, color: colors[cluster], border: `1px solid ${colors[cluster]}40`, fontWeight: 700, letterSpacing: 1, textTransform: "uppercase" }}>{labels[cluster]}</span>;
};

export const TypeBadge = ({ type }) => (
  <span style={{ fontSize: 10, padding: "2px 8px", borderRadius: 4, color: type === "Federal" ? "#38BDF8" : "#FB923C", border: `1px solid ${type === "Federal" ? "#38BDF840" : "#FB923C40"}`, fontWeight: 600 }}>{type}</span>
);

export const ArchiveBadge = () => (
  <span style={{ fontSize: 10, padding: "2px 8px", borderRadius: 4, color: "#94A3B8", border: "1px solid #94A3B840", fontWeight: 700, letterSpacing: 1, textTransform: "uppercase" }}>Archive</span>
);

export const ProceedingBadge = ({ proceeding }) => {
  if (!proceeding) return null;
  return (
    <span style={{ fontSize: 10, padding: "2px 8px", borderRadius: 4, color: "#94A3B8", border: "1px solid #94A3B840", fontWeight: 600 }}>
      {proceedingLabel(proceeding)}
    </span>
  );
};

export const PolicyLimitsBadge = ({ limits }) => {
  if (!limits) return null;
  return (
    <span
      title={`Known insurance policy limits: ${limits} (per incident / aggregate)`}
      style={{ fontSize: 10, padding: "2px 8px", borderRadius: 4, color: "#34D399", border: "1px solid #34D39940", fontWeight: 700, letterSpacing: 0.4 }}
    >
      🏷️ {limits}
    </span>
  );
};

export const PhaseBadge = ({ phase }) => {
  if (!phase || phase === "terminal") return null;
  const style = PHASE_STYLE[phase] || { color: "#94A3B8", border: "#94A3B840" };
  return (
    <span style={{ fontSize: 10, padding: "2px 8px", borderRadius: 4, color: style.color, border: `1px solid ${style.border}`, fontWeight: 700, letterSpacing: 0.4, textTransform: "uppercase" }}>
      {phaseLabel(phase)}
    </span>
  );
};
