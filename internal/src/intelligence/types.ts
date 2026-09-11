/** Coverage percentages measure filled record slots, not the chance of a ruling. */
export const COVERAGE_DISCLAIMER =
  "Percentages measure record coverage — allegation, evidence, authority, and defense slots filled — not the probability of a ruling.";

export type NodeKind =
  | "Matter"
  | "Claim"
  | "Element"
  | "Fact"
  | "Evidence"
  | "Document"
  | "DocketEntry"
  | "Authority"
  | "Judge"
  | "Attorney"
  | "Firm"
  | "Defendant"
  | "Agency"
  | "Deadline"
  | "Argument"
  | "Admission"
  | "CourtOrder"
  | "Issue";

export type EdgeKind =
  | "assigned_to"
  | "represents"
  | "employed_by"
  | "cites"
  | "cited_by"
  | "same_issue"
  | "same_counsel"
  | "same_judge"
  | "depends_on"
  | "supports"
  | "contradicts"
  | "raises"
  | "defends"
  | "contains"
  | "triggers"
  | "derived_from"
  | "filed_in"
  | "party_to"
  | "authority_dependency"
  | "persuasive_for";

export type LitigationEventType =
  | "DOCKET_ENTRY_ADDED"
  | "MOTION_FILED"
  | "ORDER_ENTERED"
  | "COUNSEL_APPEARED"
  | "DEADLINE_TRIGGERED"
  | "NEW_PRECEDENT"
  | "CITATION_OVERRULED"
  | "DOCUMENT_ADDED"
  | "ARGUMENT_CHANGED"
  | "CASE_SETTLED"
  | "ISSUE_ACTIVATED";

export type IssueStatus = "anticipated" | "active" | "dormant" | "resolved";
export type ImpactLevel = "HIGH" | "MEDIUM" | "LOW";
export type ClockStatus = "date_certain" | "waiting_on_trigger" | "fired" | "vacated";
export type MotionStatus = "anticipated" | "live" | "submitted" | "decided";

export interface GraphNode {
  id: string;
  kind: NodeKind;
  label: string;
  matter?: number;
  issues?: string[];
  attrs?: Record<string, string | number | boolean | null>;
}

export interface GraphEdge {
  id: string;
  kind: EdgeKind;
  from: string;
  to: string;
  matter?: number;
  label?: string;
}

export interface KnowledgeGraph {
  nodes: GraphNode[];
  edges: GraphEdge[];
  byId: Record<string, GraphNode>;
}

export interface LitigationEvent {
  id: string;
  type: LitigationEventType;
  at: string;
  matter?: number;
  docket?: number;
  summary: string;
  issues?: string[];
  authorities?: string[];
  actor?: string;
  payload?: Record<string, unknown>;
}

export interface OpenIssue {
  id: string;
  status: IssueStatus;
  source?: string;
}

export interface LiveMotion {
  id: string;
  docket?: number;
  label: string;
  status: MotionStatus;
  hearing?: string;
  issues: string[];
}

export interface PendingClock {
  id: string;
  matter: number;
  label: string;
  status: ClockStatus;
  date?: string | null;
  displayDate?: string | null;
  waitingOn?: string;
  derivedFrom?: string;
}

export interface LitigationTwin {
  matter: number;
  stage: string;
  live_motions: LiveMotion[];
  pending_clocks: PendingClock[];
  open_issues: OpenIssue[];
  /** Record-coverage scores, not win probabilities. */
  evidence_coverage: number;
  pleading_coverage: number;
  procedural_risk: number;
  discovery_leverage: number;
  controlling_questions: string[];
  weakest_element?: string;
  best_next_evidence?: string;
}

export interface ClaimElement {
  id: string;
  label: string;
  issue?: string;
  allegation?: string;
  evidence: string[];
  authority: string[];
  defense?: string;
  next_evidence?: string;
}

export interface ClaimMatrix {
  matter: number;
  claim_id: string;
  claim: string;
  elements: ClaimElement[];
}

export interface FactProposition {
  id: string;
  fact: string;
  sources: string[];
  supports: number[];
  contradicted_by: string[];
  issues?: string[];
}

export interface ArgumentSnapshot {
  id: string;
  matter: number;
  filing: string;
  date: string;
  arguments: string[];
  authorities: string[];
  admissions: string[];
}

export interface ArgumentDiff {
  matter: number;
  prior: string;
  current: string;
  added: string[];
  abandoned: string[];
  modified: string[];
  newAuthorities: string[];
  droppedAuthorities: string[];
  factualAdmissions: string[];
}

export interface DeadlineRecipe {
  id: string;
  matter: number;
  label: string;
  court?: string;
  trigger: {
    id: string;
    description: string;
    fired?: boolean;
    firedOn?: string | null;
  };
  offset: {
    days: number;
    unit: "calendar" | "court";
    direction: "after" | "before";
    roll?: "forward" | "backward" | "none";
  };
  dependents?: Array<{
    id: string;
    label: string;
    days: number;
    unit: "calendar" | "court";
    direction: "after" | "before";
    roll?: "forward" | "backward" | "none";
  }>;
}

export interface WarRoom {
  matter: number;
  event: string;
  docket?: number;
  immediate: string;
  attacks: Array<{ issue: string; level: ImpactLevel; note?: string }>;
  newAuthorities: string[];
  authoritiesInCiteProof: string[];
  weakOrMiscited: string[];
  newFacts: string[];
  contradictions: string[];
  crossMatters: number[];
  sequence: string[];
}

export interface ShockwaveHit {
  matter: number;
  impact: ImpactLevel;
  reason: string;
  documents: string[];
}

export interface ShockwaveReport {
  opinion: string;
  court: string;
  issues: string[];
  holdings?: string;
  hits: ShockwaveHit[];
  propositionsToUpdate: string[];
}

export interface SystemicScore {
  matter: number;
  score: number;
  reasons: string[];
}

export interface DominoResult {
  hypothesis: string;
  effects: Array<{ matter: number; delta: string; impact: ImpactLevel; reason: string }>;
}

export interface FingerprintProfile {
  id: string;
  attorney: string;
  firm?: string;
  matters: number[];
  recapMattersLocated?: number;
  motionsRetrieved?: number;
  leadDefense?: string;
  frequentAuthorities: string[];
  typicalMtdLength?: string;
  repeatedArguments: string[];
  tactics: string[];
  settlementTiming?: string;
}

export interface FingerprintMatch {
  attorneyId: string;
  score: number;
  resembled: string[];
  priorOutcomes: { granted: number; denied: number; mixed: number };
  vulnerableProposition?: string;
}

export interface JudgeDoctrineMap {
  id: string;
  judge: string;
  court: string;
  doctrines: Array<{
    id: string;
    label: string;
    notes: string;
    orders: string[];
  }>;
  researchOrder: string[];
}

export interface CiteProofAudit {
  authorityId: string;
  exists: boolean;
  propositionFound?: boolean | null;
  reversed: boolean;
  criticized: boolean;
  binding: boolean;
  court?: string;
  posture?: string;
  parentheticalOverstates?: boolean | null;
  notes: string[];
}

export interface RecapAdvice {
  documentId: string;
  action: "retrieve" | "wait" | "skip";
  reason: string;
  strategicValue: ImpactLevel;
  inRecap: boolean;
  prayerPending: boolean;
}

export interface OvernightBrief {
  asOf: string;
  docketChanges: string[];
  precedent: string[];
  citationNotes: string[];
  plaintiffDeadlines: string[];
  highestPriority: string;
}

export interface IssueCatalogEntry {
  id: string;
  label: string;
  doctrines: string[];
  statutes: string[];
  likelyDefense: boolean;
  keywords: string[];
}

export interface AuthorityCatalogEntry {
  id: string;
  label: string;
  court: string;
  citation: string;
  issues: string[];
  supports: "plaintiff" | "defense" | "mixed";
  reversed: boolean;
  criticized: boolean;
  bindingIn: string[];
  posture?: string;
  citedBy: string[];
  cites: string[];
  proposition?: string;
}

export interface RecapWatchEntry {
  id: string;
  label: string;
  matter?: number;
  inRecap: boolean;
  prayerPending: boolean;
  strategicValue: ImpactLevel;
  why: string;
}

export interface LiveMotionSeed {
  id: string;
  matter: number;
  docket?: number;
  label: string;
  status: MotionStatus;
  hearing?: string;
  issues: string[];
}

export interface IntelligenceCatalog {
  issues: IssueCatalogEntry[];
  authorities: AuthorityCatalogEntry[];
  matrices: ClaimMatrix[];
  facts: FactProposition[];
  arguments: ArgumentSnapshot[];
  dependencies: DeadlineRecipe[];
  fingerprints: FingerprintProfile[];
  judges: JudgeDoctrineMap[];
  attorneys: Array<{
    id: string;
    name: string;
    firm: string;
    matters: number[];
    issues: string[];
  }>;
  firms: Array<{ id: string; name: string; attorneys: string[] }>;
  recap: RecapWatchEntry[];
  motions: LiveMotionSeed[];
  citeproof: Record<string, Partial<CiteProofAudit>>;
}
