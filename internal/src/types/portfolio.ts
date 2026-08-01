export type MatterType = "Federal" | "State";
export type MatterVisibility = "active" | "archived";

export interface PortfolioDocument {
  label: string;
  path: string;
  filed?: boolean;
}

export interface ServiceRecord {
  name: string;
  served: boolean;
  date?: string;
  method?: string;
}

export interface Matter {
  number: number;
  caption: string;
  case_no: string;
  court: string;
  claims: string;
  status: string;
  filed: string;
  judge: string;
  cluster: number;
  type: MatterType | string;
  defendants: string;
  key_facts: string;
  procedural_status: string;
  damages: string;
  risk: string;
  causes: string[];
  evidence: string[];
  documents?: PortfolioDocument[];
  serviceTracking?: ServiceRecord[];
  archived?: boolean;
  badge?: string;
  note?: string;
}

export interface TimelineEvent {
  date: string;
  event: string;
  type: string;
  matters: string;
  upcoming?: boolean;
}
