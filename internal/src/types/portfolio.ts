export type MatterType = "Federal" | "State";
export type MatterVisibility = "active" | "archived";

/** Structured docket posture — prefer this over parsing the prose `status` field. */
export type MatterLifecycle =
  | "active"
  | "pre_filing"
  | "settled"
  | "dismissed"
  | "abandoned"
  | "closed";

/** What kind of proceeding this matter is (drives allowed `phase` values). */
export type MatterProceeding = "state_civil" | "federal_civil" | "mandate" | "habeas";

/**
 * Current procedural stage on that proceeding's track.
 * Prefer this over parsing `status` / `badge` for filters and chips.
 */
export type MatterPhase =
  | "intake"
  | "pre_filing"
  | "service"
  | "pleadings"
  | "responsive_deadline"
  | "stayed"
  | "discovery"
  | "cmc"
  | "dispositive"
  | "trial_set"
  | "default"
  | "judgment"
  | "post_judgment"
  | "terminal"
  | "petition_filed"
  | "demurrer"
  | "hearing"
  | "writ_ruling"
  | "return_awaited"
  | "traverse"
  | "under_submission"
  | "ruling"
  | "screening_ifp"
  | "mtd_briefing"
  | "fr_pending"
  | "district_review";

export interface PortfolioDocument {
  label: string;
  path: string;
  filed?: boolean;
}

export interface ServiceRecord {
  name: string;
  served: boolean;
  date?: string;
  dateServed?: string;
  title?: string;
  location?: string;
  method?: string;
}

/** Light matter record shipped in the shell bundle (no heavy prose). */
export interface MatterSummary {
  number: number;
  caption: string;
  case_no: string;
  court: string;
  claims: string;
  /** Full procedural narrative. Grows over the life of the matter — render it
   *  in a prose section, never in a badge or a fixed-width cell. */
  status: string;
  /** Short current posture (<= 60 chars) for badges, the summary strip, search
   *  results, and the README table. Kept in sync with `status` by hand; the
   *  length cap is enforced in validate-portfolio. */
  status_label: string;
  lifecycle: MatterLifecycle;
  proceeding: MatterProceeding;
  phase: MatterPhase;
  filed: string;
  judge: string;
  cluster: number;
  type: MatterType | string;
  defendants: string;
  causes: string[];
  evidenceCount: number;
  documentCount: number;
  serviceTracking?: ServiceRecord[];
  /** Derived from lifecycle (terminal dispositions). Prefer `lifecycle` / helpers. */
  archived?: boolean;
  badge?: string;
  note?: string;
  /** Known insurance policy limits for a named defendant, e.g. "$1M / $5M". */
  policy_limits?: string;
}

/** Full matter record lazy-loaded from NN.json on expand/detail. */
export interface Matter extends MatterSummary {
  key_facts: string;
  procedural_status: string;
  damages: string;
  risk: string;
  evidence: string[];
  documents?: PortfolioDocument[];
}

export interface DocumentIndexEntry {
  matter: number;
  label: string;
  path: string;
}

export interface TimelineEvent {
  date: string;
  event: string;
  type: string;
  matters: string;
  upcoming?: boolean;
}

export type CrossMatterDirection = "mutual" | "from_depends_on_to" | "to_cites_from";

export type CrossMatterSeverity = "high" | "medium" | "low";

export interface CrossMatterLink {
  id: string;
  from: number;
  to: number;
  direction: CrossMatterDirection;
  severity: CrossMatterSeverity;
  kinds: string[];
  significance: string;
  sources: string[];
}

export interface CrossMatterExposure {
  id: string;
  label: string;
  severity: CrossMatterSeverity;
  status: "open" | "monitoring" | "resolved";
  matters: number[];
  detail: string;
  remedy: string;
}

export interface CrossMatterFoundation {
  id: string;
  label: string;
  matters: number[];
  detail: string;
  document_path?: string;
}

export interface CrossMatterParty {
  name: string;
  role: string;
  defendantIn: number[];
  factualIn: number[];
}

export interface CrossMatterKind {
  label: string;
  description: string;
}

export interface CrossMatterCluster {
  id: string;
  label: string;
  matters: number[];
  thesis: string;
  links: CrossMatterLink[];
  exposures: CrossMatterExposure[];
  foundation: CrossMatterFoundation[];
  parties: CrossMatterParty[];
}

export interface CrossMatterGraph {
  linkKinds: Record<string, CrossMatterKind>;
  clusters: CrossMatterCluster[];
}

/** A peer matter as seen from the perspective of one matter. */
export interface RelatedMatter {
  number: number;
  link: CrossMatterLink;
  kinds: string[];
  relationship: string;
  significance: string;
  severity: CrossMatterSeverity;
  sources: string[];
}
