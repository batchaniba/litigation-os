import type { ReactNode } from "react";
import { Link, useParams } from "react-router-dom";
import type { Matter } from "../types/portfolio";
import { StatusBadge, ClusterBadge, TypeBadge, ArchiveBadge, ProceedingBadge, PhaseBadge } from "../components/Badges";
import { EmptyState, RouteLoading } from "../components/ui/AsyncState";
import { ServiceTracker } from "../components/ServiceTracker";
import { MatterSummary } from "../components/matters/MatterSummary";
import { CrossMatterPanel } from "../components/matters/CrossMatterPanel";
import { CoverageTower } from "../components/CoverageTower";
import { coverageForMatter } from "../data/coverage";
import { getMatterSummary } from "../data/matters";
import { useMatter } from "../hooks/useMatter";
import { ROUTES } from "../routes";
import { withBase } from "../utils/paths";
import { groupDocuments } from "../utils/documentGroups";
import { matterActivity } from "../utils/matterTimeline";
import { downloadMatterSummary, matterMarkdown } from "../utils/exportMatter";
import { isArchivedMatter } from "../utils/matterLifecycle";
import { effectiveStatusLabel } from "../utils/statusLabel";

function DetailSection({ label, children }: { label: string; children: ReactNode }) {
  return <section className="detail-section"><div className="detail-label">{label}</div>{children}</section>;
}

/** The strip shows the effective status label; the narrative only earns its own
 *  section when it actually says more than the label already did. For matters
 *  that resolved in one line ("Abandoned — voluntarily dismissed") the two are
 *  the same fact, and printing both just reads as a stutter. */
const STATUS_NARRATIVE_MARGIN = 40;

function hasStatusNarrative(matter: Matter): boolean {
  const narrative = matter.status?.trim() ?? "";
  const label = effectiveStatusLabel(matter);
  return narrative.length > label.length + STATUS_NARRATIVE_MARGIN;
}

export function MatterDetailPage() {
  const { matterNumber } = useParams();
  const number = Number(matterNumber);
  const summary = getMatterSummary(number);
  const { matter, status } = useMatter(summary ? number : null);

  if (!summary) {
    return <EmptyState title="Matter not found" detail={`No portfolio matter uses number ${matterNumber}.`} action={<Link className="back-link" to={ROUTES.matters}>Return to matters</Link>} />;
  }

  if (status === "error") {
    return <EmptyState title="Could not load matter" detail={`Matter ${number} summary exists but the full record failed to load.`} action={<Link className="back-link" to={ROUTES.matters}>Return to matters</Link>} />;
  }

  if (status === "loading" || status === "idle" || !matter) {
    return <RouteLoading label={`Loading matter ${number}`} />;
  }

  const activity = matterActivity(matter.number);
  const documentGroups = groupDocuments(matter.documents);
  const coverage = coverageForMatter(matter.number);

  return (
    <article>
      <Link className="back-link" to={ROUTES.matters}>← All matters</Link>
      <div className="matter-actions print-hidden">
        <a href="#matter-details">Details</a><a href="#matter-cross">Cross-matter</a><a href="#matter-documents">Documents</a>
        <button onClick={() => window.print()}>Print summary</button>
        <button onClick={() => downloadMatterSummary(matter, matterMarkdown(matter, activity.next, activity.recent))}>Export Markdown</button>
      </div>
      <header className="matter-detail-header">
        <div className="detail-label">Matter {matter.number}</div>
        <h1 className="matter-detail-title">{matter.caption}</h1>
        <p className="detail-copy detail-copy-subtle">{matter.case_no} · {matter.court}</p>
        <div className="matter-detail-badges">
          <ClusterBadge cluster={matter.cluster} />
          <TypeBadge type={matter.type} />
          <ProceedingBadge proceeding={matter.proceeding} />
          <PhaseBadge phase={matter.phase} />
          <StatusBadge status={effectiveStatusLabel(matter, activity)} lifecycle={matter.lifecycle} />
          {isArchivedMatter(matter) && <ArchiveBadge />}
        </div>
      </header>

      <MatterSummary matter={matter} next={activity.next} recent={activity.recent} />

      {hasStatusNarrative(matter) && (
        <DetailSection label="Current status">
          <p className="detail-copy detail-copy-muted">{matter.status}</p>
        </DetailSection>
      )}

      {coverage && (
        <DetailSection label="Insurance coverage on file">
          <CoverageTower record={coverage} variant="panel" linkToMatter={false} />
        </DetailSection>
      )}

      <CrossMatterPanel matter={matter.number} />

      <div id="matter-details" className="detail-grid">
        <DetailSection label="Defendants"><p className="detail-copy detail-copy-secondary">{matter.defendants}</p></DetailSection>
        <DetailSection label="Court assignment"><p className="detail-copy detail-copy-secondary">{matter.judge}<br />Filed: {matter.filed}</p></DetailSection>
      </div>
      <DetailSection label="Claims"><p className="detail-copy detail-copy-secondary">{matter.claims}</p></DetailSection>
      <DetailSection label="Key facts"><p className="detail-copy detail-copy-muted">{matter.key_facts}</p></DetailSection>
      <div className="detail-grid">
        <DetailSection label="Procedural status"><p className="detail-copy detail-copy-muted">{matter.procedural_status}</p></DetailSection>
        <DetailSection label="Estimated damages and risk"><p className="detail-copy matter-detail-damages">{matter.damages}</p><p className="detail-copy matter-detail-risk">{matter.risk}</p></DetailSection>
      </div>
      <DetailSection label="Causes of action">
        <div className="matter-detail-pills">{matter.causes.map((cause) => <span key={cause} className="matter-detail-pill cause">{cause}</span>)}</div>
      </DetailSection>
      <DetailSection label="Key evidence">
        <div className="matter-detail-pills">{matter.evidence.map((evidence) => <span key={evidence} className="matter-detail-pill evidence">{evidence}</span>)}</div>
      </DetailSection>
      {matter.serviceTracking && <ServiceTracker serviceTracking={matter.serviceTracking} />}
      <DetailSection label={`Documents (${matter.documents?.length ?? 0})`}>
        <div id="matter-documents" />
        {documentGroups.length ? documentGroups.map(([group, documents], index) => (
          <details key={group} className="document-group" open={index === 0}>
            <summary><span>{group}</span><span>{documents.length}</span></summary>
            <div className="document-list">{documents.map((document) => <a key={document.path} href={withBase(document.path)} target="_blank" rel="noreferrer"><span className="document-type">PDF</span><span>{document.label}</span></a>)}</div>
          </details>
        )) : <p className="detail-copy detail-copy-subtle">No documents are linked to this matter.</p>}
      </DetailSection>
    </article>
  );
}
