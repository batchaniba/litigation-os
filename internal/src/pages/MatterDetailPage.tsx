import type { ReactNode } from "react";
import { Link, useParams } from "react-router";
import { StatusBadge, ClusterBadge, TypeBadge, ArchiveBadge, ProceedingBadge, PhaseBadge } from "../components/Badges";
import { EmptyState, RouteLoading } from "../components/ui/AsyncState";
import { ServiceTracker } from "../components/ServiceTracker";
import { MatterSummary } from "../components/matters/MatterSummary";
import { CollapsibleProse } from "../components/ui/CollapsibleProse";
import { CrossMatterPanel } from "../components/matters/CrossMatterPanel";
import { getMatterSummary } from "../data/matters";
import { useMatter } from "../hooks/useMatter";
import { ROUTES } from "../routes";
import { withBase } from "../utils/paths";
import { clusterForMatter } from "../utils/crossMatter";
import { groupDocuments } from "../utils/documentGroups";
import { matterActivity } from "../utils/matterTimeline";
import { downloadMatterSummary, matterMarkdown } from "../utils/exportMatter";
import { isArchivedMatter } from "../utils/matterLifecycle";
import { effectiveStatusLabel } from "../utils/statusLabel";

interface RailSection {
  id: string;
  label: string;
}

function DetailSection({ id, label, children }: { id?: string; label: string; children: ReactNode }) {
  return <section id={id} className="detail-section"><div className="detail-label">{label}</div>{children}</section>;
}

/** A titled card. Sections stay inside one of these so the page reads as grouped
 *  panels rather than the flat run of labelled prose it used to be. */
function PanelGroup({ id, title, children }: { id: string; title: string; children: ReactNode }) {
  return (
    <section id={id} className="matter-panel" aria-labelledby={`${id}-title`}>
      <h2 id={`${id}-title`} className="matter-panel-title">{title}</h2>
      {children}
    </section>
  );
}

/** Sticky "on this page" nav. Replaces the three anchor links that used to sit
 *  above the title, and only lists sections this matter actually renders. */
function MatterRail({ sections }: { sections: RailSection[] }) {
  return (
    <nav className="matter-rail print-hidden" aria-label="Matter sections">
      <div className="detail-label">On this page</div>
      <ul>
        {sections.map((section) => (
          <li key={section.id}><a href={`#${section.id}`}>{section.label}</a></li>
        ))}
      </ul>
    </nav>
  );
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

  const activity = matterActivity(matter.number, { clocks: matter.clocks });
  const documentGroups = groupDocuments(matter.documents);
  // CrossMatterPanel renders null without a cluster, so the rail has to ask the
  // same question before advertising a link to it.
  const hasCrossMatter = Boolean(clusterForMatter(matter.number));
  const hasExposure = Boolean(matter.damages || matter.risk);

  const sections: RailSection[] = [
    { id: "matter-overview", label: "Overview" },
    { id: "matter-details", label: "The matter" },
    ...(hasExposure ? [{ id: "matter-exposure", label: "Exposure" }] : []),
    ...(hasCrossMatter ? [{ id: "matter-cross", label: "Cross-matter" }] : []),
    { id: "matter-record", label: "Record" },
  ];

  return (
    <div className="matter-page">
      <Link className="back-link matter-page-back" to={ROUTES.matters}>← All matters</Link>
      <MatterRail sections={sections} />

      <article className="matter-page-main">
        <header id="matter-overview" className="matter-hero">
          <div className="matter-hero-top">
            <div className="matter-hero-identity">
              <div className="detail-label">Matter {matter.number}</div>
              <h1 className="matter-detail-title">{matter.caption}</h1>
              <p className="detail-copy detail-copy-subtle">
                {matter.case_no} · {matter.court}
                {matter.courtlistener?.docket_url ? (
                  <>
                    {" · "}
                    <a href={`https://www.courtlistener.com${matter.courtlistener.docket_url}`} target="_blank" rel="noreferrer">
                      CourtListener docket
                    </a>
                  </>
                ) : null}
              </p>
            </div>
            <div className="matter-actions print-hidden">
              <button onClick={() => window.print()}>Print summary</button>
              <button onClick={() => downloadMatterSummary(matter, matterMarkdown(matter, activity.next, activity.recent))}>Export Markdown</button>
            </div>
          </div>
          <div className="matter-detail-badges">
            <ClusterBadge cluster={matter.cluster} />
            <TypeBadge type={matter.type} />
            <ProceedingBadge proceeding={matter.proceeding} />
            <PhaseBadge phase={matter.phase} />
            <StatusBadge status={effectiveStatusLabel(matter, activity)} lifecycle={matter.lifecycle} />
            {isArchivedMatter(matter) && <ArchiveBadge />}
          </div>
          <MatterSummary matter={matter} next={activity.next} recent={activity.recent} />
        </header>

        <PanelGroup id="matter-details" title="The matter">
          <div className="matter-facts">
            <DetailSection label="Defendants"><p className="detail-copy detail-copy-secondary">{matter.defendants}</p></DetailSection>
            <DetailSection label="Court assignment"><p className="detail-copy detail-copy-secondary">{matter.judge}<br />Filed: {matter.filed}</p></DetailSection>
          </div>
          <DetailSection label="Claims"><p className="detail-copy detail-copy-secondary">{matter.claims}</p></DetailSection>
          {(matter.causes ?? []).length ? (
            <DetailSection label="Causes of action">
              <div className="matter-detail-pills">{matter.causes.map((cause) => <span key={cause} className="matter-detail-pill cause">{cause}</span>)}</div>
            </DetailSection>
          ) : null}
          {matter.evidence?.length ? (
            <DetailSection label="Key evidence">
              <div className="matter-detail-pills">{matter.evidence.map((evidence) => <span key={evidence} className="matter-detail-pill evidence">{evidence}</span>)}</div>
            </DetailSection>
          ) : null}
          {matter.key_facts ? <DetailSection label="Key facts"><CollapsibleProse text={matter.key_facts} label="key facts" className="detail-copy-muted" lines={6} /></DetailSection> : null}
          {matter.procedural_status ? <DetailSection label="Procedural status"><CollapsibleProse text={matter.procedural_status} label="procedural status" className="detail-copy-muted" lines={6} /></DetailSection> : null}
        </PanelGroup>

        {hasExposure ? (
          <PanelGroup id="matter-exposure" title="Exposure">
            <DetailSection label="Estimated damages and risk">
              {matter.damages ? <p className="detail-copy matter-detail-damages">{matter.damages}</p> : null}
              {matter.risk ? <CollapsibleProse text={matter.risk} label="risk notes" className="matter-detail-risk" lines={6} /> : null}
            </DetailSection>
          </PanelGroup>
        ) : null}

        <CrossMatterPanel matter={matter.number} />

        <PanelGroup id="matter-record" title="Record">
          {matter.serviceTracking && <ServiceTracker serviceTracking={matter.serviceTracking} />}
          <DetailSection id="matter-documents" label={`Documents (${matter.documents?.length ?? 0})`}>
            {documentGroups.length ? documentGroups.map(([group, documents], index) => (
              <details key={group} className="document-group" open={index === 0}>
                <summary><span>{group}</span><span>{documents.length}</span></summary>
                <div className="document-list">{documents.map((document) => <a key={document.path} href={withBase(document.path)} target="_blank" rel="noreferrer"><span className="document-type">PDF</span><span>{document.label}</span></a>)}</div>
              </details>
            )) : <p className="detail-copy detail-copy-subtle">No documents are linked to this matter.</p>}
          </DetailSection>
        </PanelGroup>
      </article>
    </div>
  );
}
