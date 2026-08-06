import { Link } from "react-router-dom";
import { getMatterSummary } from "../../data/matters";
import { ROUTES } from "../../routes";
import {
  clusterForMatter,
  exposuresForMatter,
  foundationForMatter,
  linkKindLabel,
  partiesForMatter,
  relatedMatters,
} from "../../utils/crossMatter";

interface CrossMatterPanelProps {
  matter: number;
}

export function CrossMatterPanel({ matter }: CrossMatterPanelProps) {
  const cluster = clusterForMatter(matter);
  if (!cluster) return null;

  const peers = relatedMatters(matter);
  const exposures = exposuresForMatter(matter);
  const foundation = foundationForMatter(matter);
  const parties = partiesForMatter(matter);

  return (
    <section className="detail-section xm-panel" id="matter-cross">
      <div className="detail-label">Cross-matter significance</div>
      <p className="detail-copy detail-copy-secondary xm-cluster-line">
        Part of <Link to={ROUTES.crossMatter}>{cluster.label}</Link> — {cluster.matters.length} matters,{" "}
        {peers.length} direct links from this docket.
      </p>

      <div className="xm-subhead">Linked matters</div>
      <ul className="xm-peer-list">
        {peers.map((peer) => {
          const summary = getMatterSummary(peer.number);
          return (
            <li key={peer.number} className={`xm-peer xm-sev-${peer.severity}`}>
              <div className="xm-peer-head">
                <Link className="xm-peer-title" to={`${ROUTES.matters}/${peer.number}`}>
                  Matter {peer.number}
                  {summary ? ` — ${summary.caption}` : ""}
                </Link>
                <span className="xm-relationship">{peer.relationship}</span>
              </div>
              <div className="xm-kinds">
                {peer.kinds.map((kind) => (
                  <span key={kind} className={`xm-kind xm-kind-${kind}`}>
                    {linkKindLabel(kind)}
                  </span>
                ))}
              </div>
              {peer.significance.split("\n\n").map((paragraph) => (
                <p key={paragraph.slice(0, 32)} className="detail-copy detail-copy-muted">
                  {paragraph}
                </p>
              ))}
              <ul className="xm-sources">
                {peer.sources.map((source) => (
                  <li key={source}>{source}</li>
                ))}
              </ul>
            </li>
          );
        })}
      </ul>

      {exposures.length > 0 && (
        <>
          <div className="xm-subhead">Open cross-matter exposure</div>
          <ul className="xm-exposure-list">
            {exposures.map((exposure) => (
              <li key={exposure.id} className={`xm-exposure xm-sev-${exposure.severity}`}>
                <div className="xm-exposure-head">
                  <span className="xm-exposure-label">{exposure.label}</span>
                  <span className={`xm-status xm-status-${exposure.status}`}>{exposure.status}</span>
                </div>
                <p className="detail-copy detail-copy-muted">{exposure.detail}</p>
                <p className="detail-copy xm-remedy">
                  <strong>Remedy:</strong> {exposure.remedy}
                </p>
                <div className="xm-exposure-matters">
                  {exposure.matters.map((number) => (
                    <Link key={number} className="xm-matter-chip" to={`${ROUTES.matters}/${number}`}>
                      Matter {number}
                    </Link>
                  ))}
                </div>
              </li>
            ))}
          </ul>
        </>
      )}

      <div className="xm-grid">
        <div>
          <div className="xm-subhead">Shared evidentiary foundation</div>
          <ul className="xm-foundation-list">
            {foundation.map((item) => (
              <li key={item.id}>
                <span className="xm-foundation-label">{item.label}</span>
                <span className="xm-foundation-count">
                  {item.matters.length} matter{item.matters.length === 1 ? "" : "s"}
                </span>
                <p className="detail-copy detail-copy-muted">{item.detail}</p>
              </li>
            ))}
          </ul>
        </div>
        <div>
          <div className="xm-subhead">Overlapping parties</div>
          <ul className="xm-party-list">
            {parties.map((party) => (
              <li key={party.name}>
                <span className="xm-party-name">{party.name}</span>
                <p className="detail-copy detail-copy-muted">{party.role}</p>
                <p className="detail-copy detail-copy-subtle">
                  Defendant in: {party.defendantIn.length ? party.defendantIn.join(", ") : "none"} ·
                  Factual role in: {party.factualIn.length ? party.factualIn.join(", ") : "none"}
                </p>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </section>
  );
}
