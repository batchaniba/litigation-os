import { Link } from "react-router";
import { getMatterSummary } from "../data/matters";
import { ROUTES } from "../routes";
import {
  CROSS_MATTER_CLUSTERS,
  authorityChain,
  kindsBetween,
  linkKindDescription,
  linkKindLabel,
  linkDegree,
  openExposures,
  relationshipFor,
} from "../utils/crossMatter";

function MatterLabel({ number }: { number: number }) {
  const summary = getMatterSummary(number);
  return (
    <Link className="xm-matter-link" to={`${ROUTES.matters}/${number}`}>
      <span className="xm-matter-number">Matter {number}</span>
      {summary && <span className="xm-matter-caption">{summary.caption}</span>}
      {summary && <span className="xm-matter-court">{summary.court}</span>}
    </Link>
  );
}

export function CrossMatterTab() {
  return (
    <article className="xm-tab">
      <header className="xm-tab-header">
        <h1 className="tab-title">Cross-Matter Significance</h1>
        <p className="detail-copy detail-copy-secondary">
          Where one factual record drives several dockets at once, the relationships between matters
          carry as much weight as the matters themselves. This view maps those relationships, the
          authority that travels between them, and the exposure the overlap creates.
        </p>
      </header>

      {CROSS_MATTER_CLUSTERS.map((cluster) => {
        const exposures = openExposures(cluster);
        const chain = authorityChain(cluster);
        return (
          <section key={cluster.id} className="xm-cluster">
            <div className="detail-label">Cluster</div>
            <h2 className="xm-cluster-title">{cluster.label}</h2>
            <p className="detail-copy detail-copy-secondary xm-thesis">{cluster.thesis}</p>

            <div className="xm-stats">
              <div className="xm-stat">
                <span className="xm-stat-value">{cluster.matters.length}</span>
                <span className="xm-stat-label">Matters</span>
              </div>
              <div className="xm-stat">
                <span className="xm-stat-value">{cluster.links.length}</span>
                <span className="xm-stat-label">Documented links</span>
              </div>
              <div className="xm-stat">
                <span className="xm-stat-value">{exposures.length}</span>
                <span className="xm-stat-label">Open exposures</span>
              </div>
              <div className="xm-stat">
                <span className="xm-stat-value">{cluster.foundation.length}</span>
                <span className="xm-stat-label">Shared proof items</span>
              </div>
            </div>

            <div className="xm-subhead">Relationship matrix</div>
            <div className="xm-matrix-scroll">
              <table className="xm-matrix">
                <caption className="xm-matrix-caption">
                  Each cell lists every documented relationship between the row matter and the column
                  matter.
                </caption>
                <thead>
                  <tr>
                    <th scope="col">Matter</th>
                    {cluster.matters.map((number) => (
                      <th key={number} scope="col">
                        {number}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {cluster.matters.map((row) => (
                    <tr key={row}>
                      <th scope="row">
                        <MatterLabel number={row} />
                        <span className="xm-degree">{linkDegree(row)} links</span>
                      </th>
                      {cluster.matters.map((column) => {
                        if (row === column) {
                          return (
                            <td key={column} className="xm-cell xm-cell-self" aria-label="same matter">
                              —
                            </td>
                          );
                        }
                        const kinds = kindsBetween(row, column);
                        if (kinds.length === 0) {
                          return (
                            <td key={column} className="xm-cell xm-cell-empty">
                              <span className="xm-none">no link</span>
                            </td>
                          );
                        }
                        return (
                          <td key={column} className="xm-cell">
                            {kinds.map((kind) => (
                              <span key={kind} className={`xm-kind xm-kind-${kind}`}>
                                {linkKindLabel(kind)}
                              </span>
                            ))}
                          </td>
                        );
                      })}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            <div className="xm-subhead">Authority chain</div>
            <ol className="xm-chain">
              {chain.map((link) => (
                <li key={link.id} className={`xm-chain-item xm-sev-${link.severity}`}>
                  <div className="xm-chain-head">
                    <span className="xm-chain-route">
                      Matter {link.from} → Matter {link.to}
                    </span>
                    <span className="xm-relationship">{relationshipFor(link, link.from)}</span>
                  </div>
                  <div className="xm-kinds">
                    {link.kinds.map((kind) => (
                      <span key={kind} className={`xm-kind xm-kind-${kind}`}>
                        {linkKindLabel(kind)}
                      </span>
                    ))}
                  </div>
                  <p className="detail-copy detail-copy-muted">{link.significance}</p>
                  <ul className="xm-sources">
                    {link.sources.map((source) => (
                      <li key={source}>{source}</li>
                    ))}
                  </ul>
                </li>
              ))}
            </ol>

            <div className="xm-subhead">Open exposure across the cluster</div>
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

            <div className="xm-subhead">Shared evidentiary foundation</div>
            <ul className="xm-foundation-list xm-foundation-wide">
              {cluster.foundation.map((item) => (
                <li key={item.id}>
                  <span className="xm-foundation-label">{item.label}</span>
                  <span className="xm-foundation-count">
                    Matters {item.matters.join(", ")}
                  </span>
                  <p className="detail-copy detail-copy-muted">{item.detail}</p>
                </li>
              ))}
            </ul>

            <div className="xm-subhead">Overlapping parties</div>
            <div className="xm-matrix-scroll">
              <table className="xm-matrix xm-party-table">
                <thead>
                  <tr>
                    <th scope="col">Party</th>
                    <th scope="col">Role</th>
                    <th scope="col">Named defendant in</th>
                    <th scope="col">Factual role in</th>
                  </tr>
                </thead>
                <tbody>
                  {cluster.parties.map((party) => (
                    <tr key={party.name}>
                      <th scope="row">{party.name}</th>
                      <td>{party.role}</td>
                      <td>{party.defendantIn.length ? party.defendantIn.join(", ") : "—"}</td>
                      <td>{party.factualIn.length ? party.factualIn.join(", ") : "—"}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            <div className="xm-subhead">Legend</div>
            <dl className="xm-legend">
              {Array.from(new Set(cluster.links.flatMap((link) => link.kinds))).map((kind) => (
                <div key={kind} className="xm-legend-item">
                  <dt>
                    <span className={`xm-kind xm-kind-${kind}`}>{linkKindLabel(kind)}</span>
                  </dt>
                  <dd className="detail-copy detail-copy-muted">{linkKindDescription(kind)}</dd>
                </div>
              ))}
            </dl>
          </section>
        );
      })}
    </article>
  );
}
