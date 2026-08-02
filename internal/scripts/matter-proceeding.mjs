// Shared proceeding/phase helpers for Node scripts (validate, scaffold).

export const MATTER_PROCEEDINGS = ["state_civil", "federal_civil", "mandate", "habeas"];

export const MATTER_PHASES = [
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
  "petition_filed",
  "demurrer",
  "hearing",
  "writ_ruling",
  "return_awaited",
  "traverse",
  "under_submission",
  "ruling",
  "screening_ifp",
  "mtd_briefing",
  "fr_pending",
  "district_review",
];

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
];

export const PHASES_BY_PROCEEDING = {
  state_civil: [...SHARED, "demurrer", "hearing"],
  federal_civil: [...SHARED, "screening_ifp", "mtd_briefing", "fr_pending", "district_review", "hearing"],
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

export function isPhaseAllowed(proceeding, phase) {
  return (PHASES_BY_PROCEEDING[proceeding] ?? []).includes(phase);
}

export function proceedingLabel(proceeding) {
  return (
    {
      state_civil: "State civil",
      federal_civil: "Federal civil",
      mandate: "Mandate / writ",
      habeas: "Habeas",
    }[proceeding] ?? proceeding
  );
}

export function phaseLabel(phase) {
  return (
    {
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
    }[phase] ?? phase
  );
}
