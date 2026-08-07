import { Link } from "react-router";
import { formatLimit } from "../data/coverage";

export interface CoverageRecord {
  matter: number;
  caption: string;
  caseNo: string;
  court: string;
  carrier: string;
  policyNo: string;
  perIncident: number;
  aggregate: number;
  limitsShort: string;
  insureds: string[];
  source: string;
  leverage: string;
}

/**
 * Insurance policy limits rendered as a stacked tower.
 *
 * The per-incident bar is drawn as its true fraction of the aggregate, so the
 * picture carries the strategy rather than just the number: one incident
 * reaches a fifth of the tower, which is the visual argument for pleading
 * discrete violations rather than a single omnibus claim.
 */
export function CoverageTower({
  record,
  variant = "header",
  linkToMatter = true,
}: {
  record: CoverageRecord;
  variant?: "header" | "panel";
  linkToMatter?: boolean;
}) {
  // This renders in the app-wide header, so a malformed record must degrade
  // rather than throw: a zero/negative per-incident limit would otherwise make
  // the tick count Infinity and take down every page.
  const usableRatio = record.perIncident > 0 && record.aggregate > 0;
  const share = usableRatio ? Math.max(0, Math.min(1, record.perIncident / record.aggregate)) : 1;
  const perIncidentPct = `${(share * 100).toFixed(1)}%`;
  const incidentsToExhaust = usableRatio
    ? Math.min(24, Math.max(1, Math.ceil(record.aggregate / record.perIncident)))
    : 1;

  const caption = (
    <>
      {record.insureds.join(" · ")}
    </>
  );

  const body = (
    <>
      <div className="coverage-tower-label">
        <span aria-hidden="true">🏛️</span> Insured Exposure
      </div>

      <div className="coverage-tower-figures">
        <div className="coverage-tower-figure">
          <span className="coverage-tower-amount">{formatLimit(record.perIncident)}</span>
          <span className="coverage-tower-unit">per incident</span>
        </div>
        <span className="coverage-tower-divider" aria-hidden="true">/</span>
        <div className="coverage-tower-figure">
          <span className="coverage-tower-amount coverage-tower-amount-aggregate">
            {formatLimit(record.aggregate)}
          </span>
          <span className="coverage-tower-unit">aggregate</span>
        </div>
      </div>

      <div
        className="coverage-tower-bar"
        role="img"
        aria-label={`Policy tower: ${formatLimit(record.perIncident)} per incident against a ${formatLimit(
          record.aggregate,
        )} aggregate — ${incidentsToExhaust} separate incidents exhaust the tower.`}
      >
        <div className="coverage-tower-bar-fill" style={{ width: perIncidentPct }} />
        {Array.from({ length: incidentsToExhaust - 1 }, (_, i) => (
          <span
            key={i}
            className="coverage-tower-tick"
            style={{ left: `${((i + 1) / incidentsToExhaust) * 100}%` }}
            aria-hidden="true"
          />
        ))}
      </div>

      <div className="coverage-tower-insureds">{caption}</div>

      {variant === "panel" ? (
        <>
          <div className="coverage-tower-meta">
            {record.carrier} · Policy No. {record.policyNo} · {record.court} {record.caseNo}
          </div>
          <p className="coverage-tower-leverage">{record.leverage}</p>
          <div className="coverage-tower-source">{record.source}</div>
        </>
      ) : (
        <div className="coverage-tower-meta">
          {record.carrier} · Policy No. {record.policyNo}
          <span className="coverage-tower-matter">Matter {record.matter}</span>
        </div>
      )}
    </>
  );

  const className = `coverage-tower coverage-tower-${variant}`;
  const title = `${record.limitsShort} — ${record.carrier} Policy No. ${record.policyNo}, covering ${record.insureds.join(
    " and ",
  )} (Matter ${record.matter})`;

  if (!linkToMatter) {
    return (
      <div className={className} title={title}>
        {body}
      </div>
    );
  }

  return (
    <Link className={className} to={`/matters/${record.matter}`} title={title}>
      {body}
    </Link>
  );
}
