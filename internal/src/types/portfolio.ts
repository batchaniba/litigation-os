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
  status: string;
  lifecycle: MatterLifecycle;
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
