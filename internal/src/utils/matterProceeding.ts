import type {
  MatterPhase,
  MatterProceeding,
  MatterSummary,
} from "../types/portfolio";

export const MATTER_PROCEEDINGS = [
  "state_civil",
  "federal_civil",
  "mandate",
  "habeas",
] as const;

/** Phases shared across tracks, plus track-specific stages. */
export const MATTER_PHASES = [
  // shared / early
  "intake",
  "pre_filing",
  "service",
  "pleadings",
  "responsive_deadline",
  "stayed",
  "discovery",
  "cmc",
  "dispositive",
  "trial_set",
  "default",
  "judgment",
  "post_judgment",
  "terminal",
  // mandate / habeas petition track
  "petition_filed",
  "demurrer",
  "hearing",
  "writ_ruling",
  "return_awaited",
  "traverse",
  "under_submission",
  "ruling",
  // federal civil
  "screening_ifp",
  "mtd_briefing",
  "fr_pending",
  "district_review",
] as const;

const SHARED = [
  "intake",
  "pre_filing",
  "service",
  "pleadings",
  "responsive_deadline",
  "stayed",
  "discovery",
  "cmc",
  "dispositive",
  "trial_set",
  "default",
  "judgment",
  "post_judgment",
  "terminal",
] as const satisfies readonly MatterPhase[];

export const PHASES_BY_PROCEEDING: Record<MatterProceeding, readonly MatterPhase[]> = {
  state_civil: [...SHARED, "demurrer", "hearing"],
  federal_civil: [
    ...SHARED,
    "screening_ifp",
    "mtd_briefing",
    "fr_pending",
    "district_review",
    "hearing",
  ],
  mandate: [
    "intake",
    "pre_filing",
    "petition_filed",
    "service",
    "demurrer",
    "hearing",
    "under_submission",
    "writ_ruling",
    "stayed",
    "terminal",
  ],
  habeas: [
    "intake",
    "pre_filing",
    "petition_filed",
    "return_awaited",
    "traverse",
    "under_submission",
    "ruling",
    "hearing",
    "stayed",
    "terminal",
  ],
};

export function isPhaseAllowed(proceeding: MatterProceeding, phase: MatterPhase): boolean {
  return (PHASES_BY_PROCEEDING[proceeding] ?? []).includes(phase);
}

export function proceedingLabel(proceeding: MatterProceeding): string {
  switch (proceeding) {
    case "state_civil":
      return "State civil";
    case "federal_civil":
      return "Federal civil";
    case "mandate":
      return "Mandate / writ";
    case "habeas":
      return "Habeas";
    default:
      return proceeding;
  }
}

export function phaseLabel(phase: MatterPhase): string {
  const labels: Record<MatterPhase, string> = {
    intake: "Intake",
    pre_filing: "Pre-filing",
    service: "Service",
    pleadings: "Pleadings",
    responsive_deadline: "Responsive deadline",
    stayed: "Stayed",
    discovery: "Discovery",
    cmc: "Case management",
    dispositive: "Dispositive motion",
    trial_set: "Trial set",
    default: "Default / prove-up",
    judgment: "Judgment",
    post_judgment: "Post-judgment",
    terminal: "Terminal",
    petition_filed: "Petition filed",
    demurrer: "Demurrer",
    hearing: "Hearing",
    writ_ruling: "Writ ruling",
    return_awaited: "Return awaited",
    traverse: "Traverse",
    under_submission: "Under submission",
    ruling: "Ruling",
    screening_ifp: "IFP / screening",
    mtd_briefing: "MTD briefing",
    fr_pending: "F&R pending",
    district_review: "District judge review",
  };
  return labels[phase] ?? phase;
}

/** Prefer structured phase for UI chips; fall back to legacy badge. */
export function phaseOrBadgeLabel(matter: Pick<MatterSummary, "phase" | "badge">): string | null {
  if (matter.phase && matter.phase !== "terminal") return phaseLabel(matter.phase);
  if (matter.badge) return matter.badge;
  return null;
}
