/** Portfolio jurisdiction keys matching portfolioMeta.js court names. */
export type CourtKey =
  | "USDC E.D. Cal."
  | "USDC N.D. Cal."
  | "San Joaquin Sup. Ct."
  | "Alameda Sup. Ct."
  | "Sacramento Sup. Ct."
  | "Santa Clara Sup. Ct.";

export type Forum = "california" | "federal";

export type ServiceMethod =
  | "personal"
  | "mail_ca"
  | "mail_out_of_state"
  | "mail_out_of_country"
  | "overnight"
  | "electronic";

/** YYYY-MM-DD civil date (timezone-agnostic). */
export type DayKey = `${number}-${number}-${number}` | string;

export type Holiday = {
  date: DayKey;
  name: string;
  sourceId: string;
};

export type RuleCitation = {
  id: string;
  label: string;
  /** Official primary-source URL when available. */
  url: string;
  note?: string;
};

export type ComputedDeadline = {
  id: string;
  label: string;
  date: DayKey;
  /** Portfolio display form, e.g. "Aug. 21, 2026". */
  displayDate: string;
  /** Days counted before any weekend/holiday roll. */
  rawDate?: DayKey;
  rolled: boolean;
  citations: RuleCitation[];
  explanation: string;
};

export type RecipeId =
  | "ca_motion_hearing"
  | "ca_demurrer_hearing"
  | "ca_summons_service"
  | "ca_demurrer_meet_confer"
  | "ca_crc_service_deadline"
  | "ca_cmc_statement"
  | "federal_motion_hearing"
  | "federal_answer_after_service"
  | "federal_response_after_mail_service"
  | "edcal_lr230c_opposition"
  | "edcal_lr230d_reply"
  | "ndcal_lr7_motion_filed";

export type ComputeInput = {
  recipe: RecipeId;
  /** Anchor date: hearing, service, or filing depending on recipe. */
  anchorDate: DayKey | Date | string;
  court?: CourtKey;
  serviceMethod?: ServiceMethod;
};

export type ComputeResult = {
  recipe: RecipeId;
  forum: Forum;
  court: CourtKey;
  anchorDate: DayKey;
  anchorDisplay: string;
  deadlines: ComputedDeadline[];
  sources: RuleCitation[];
  disclaimer: string;
};
