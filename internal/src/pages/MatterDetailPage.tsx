import type { ReactNode } from "react";
import { Link, useParams } from "react-router-dom";
import { StatusBadge, ClusterBadge, TypeBadge, ArchiveBadge } from "../components/Badges";
import { EmptyState } from "../components/ui/AsyncState";
import { ServiceTracker } from "../components/ServiceTracker";
import { GOLD } from "../constants";
import { cases } from "../data/matters";
import { ROUTES } from "../routes";
import { useTheme } from "../ThemeContext";
import type { Matter } from "../types/portfolio";
import { withBase } from "../utils/paths";

function DetailSection({ label, children }: { label: string; children: ReactNode }) {
  return <section className="detail-section"><div className="detail-label">{label}</div>{children}</section>;
}

export function MatterDetailPage() {
  const { matterNumber } = useParams();
  const theme = useTheme();
  const matter = cases.find((item) => item.number === Number(matterNumber)) as Matter | undefined;

  if (!matter) {
    return <EmptyState title="Matter not found" detail={`No portfolio matter uses number ${matterNumber}.`} action={<Link className="back-link" to={ROUTES.matters}>Return to matters</Link>} />;
  }

  return (
    <article>
      <Link className="back-link" to={ROUTES.matters}>← All matters</Link>
      <header style={{ margin: "22px 0", paddingBottom: 20, borderBottom: `1px solid ${theme.cardBorder}` }}>
        <div className="detail-label">Matter {matter.number}</div>
        <h1 style={{ color: theme.heading, fontSize: 32, margin: "0 0 8px" }}>{matter.caption}</h1>
        <p className="detail-copy" style={{ color: theme.subtleText }}>{matter.case_no} · {matter.court}</p>
        <div style={{ display: "flex", gap: 8, flexWrap: "wrap", marginTop: 14 }}>
          <ClusterBadge cluster={matter.cluster} />
          <TypeBadge type={matter.type} />
          <StatusBadge status={matter.status} />
          {matter.archived && <ArchiveBadge />}
        </div>
      </header>

      <div className="detail-grid">
        <DetailSection label="Defendants"><p className="detail-copy" style={{ color: theme.secondaryText }}>{matter.defendants}</p></DetailSection>
        <DetailSection label="Court assignment"><p className="detail-copy" style={{ color: theme.secondaryText }}>{matter.judge}<br />Filed: {matter.filed}</p></DetailSection>
      </div>
      <DetailSection label="Claims"><p className="detail-copy" style={{ color: theme.secondaryText }}>{matter.claims}</p></DetailSection>
      <DetailSection label="Key facts"><p className="detail-copy" style={{ color: theme.mutedText }}>{matter.key_facts}</p></DetailSection>
      <div className="detail-grid">
        <DetailSection label="Procedural status"><p className="detail-copy" style={{ color: theme.mutedText }}>{matter.procedural_status}</p></DetailSection>
        <DetailSection label="Estimated damages and risk"><p className="detail-copy" style={{ color: "#34d399", fontWeight: 700 }}>{matter.damages}</p><p className="detail-copy" style={{ color: "#f59e0b", marginTop: 10 }}>{matter.risk}</p></DetailSection>
      </div>
      <DetailSection label="Causes of action">
        <div style={{ display: "flex", flexWrap: "wrap", gap: 7 }}>{matter.causes.map((cause) => <span key={cause} style={{ background: theme.navySubtleBg, borderRadius: 4, color: theme.secondaryText, fontFamily: "var(--font-sans)", fontSize: 11, padding: "5px 10px" }}>{cause}</span>)}</div>
      </DetailSection>
      <DetailSection label="Key evidence">
        <div style={{ display: "flex", flexWrap: "wrap", gap: 7 }}>{matter.evidence.map((evidence) => <span key={evidence} style={{ background: theme.clusterPillBg, border: `1px solid ${theme.clusterPillBorder}`, borderRadius: 4, color: theme.clusterPillColor, fontFamily: "var(--font-sans)", fontSize: 11, padding: "5px 10px" }}>{evidence}</span>)}</div>
      </DetailSection>
      {matter.serviceTracking && <ServiceTracker serviceTracking={matter.serviceTracking} />}
      <DetailSection label={`Documents (${matter.documents?.length ?? 0})`}>
        {matter.documents?.length ? (
          <div style={{ display: "grid", gap: 8 }}>
            {matter.documents.map((document) => (
              <a key={document.path} href={withBase(document.path)} target="_blank" rel="noreferrer" style={{ background: theme.cardBg, border: `1px solid ${theme.cardBorder}`, borderRadius: 7, color: theme.secondaryText, fontFamily: "var(--font-sans)", fontSize: 12, padding: "10px 12px", textDecoration: "none" }}>
                <span style={{ color: GOLD, marginRight: 8 }}>PDF</span>{document.label}
              </a>
            ))}
          </div>
        ) : <p className="detail-copy" style={{ color: theme.subtleText }}>No documents are linked to this matter.</p>}
      </DetailSection>
    </article>
  );
}
