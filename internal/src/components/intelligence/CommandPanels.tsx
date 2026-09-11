import { Link } from "react-router";
import { COVERAGE_DISCLAIMER, type ClaimMatrix, type LitigationTwin, type PendingClock, type WarRoom } from "../../intelligence/types";
import { coverageReport } from "../../intelligence/coverage";
import { ROUTES } from "../../routes";

function pct(value: number): string {
  return `${Math.round(value * 100)}%`;
}

function statusClass(status: string): string {
  if (status === "active" || status === "live" || status === "HIGH") return "intel-tag intel-tag-hot";
  if (status === "anticipated" || status === "waiting_on_trigger" || status === "MEDIUM") return "intel-tag intel-tag-warn";
  return "intel-tag";
}

export function CoverageNote() {
  return <p className="intel-disclaimer">{COVERAGE_DISCLAIMER}</p>;
}

export function LitigationTwinPanel({ twin }: { twin: LitigationTwin }) {
  return (
    <div className="intel-twin">
      <p className="intel-kicker">Litigation Twin — controlling questions, not a scoreboard</p>
      <div className="intel-twin-grid">
        <div>
          <div className="detail-label">Stage</div>
          <p className="detail-copy">{twin.stage.replaceAll("_", " ")}</p>
        </div>
        <div>
          <div className="detail-label">Live motions</div>
          <ul className="intel-list">
            {twin.live_motions.length ? twin.live_motions.map((motion) => (
              <li key={motion.id}>
                <span className={statusClass(motion.status)}>{motion.status}</span> {motion.label}
                {motion.hearing ? ` · hearing ${motion.hearing}` : ""}
              </li>
            )) : <li>None on file.</li>}
          </ul>
        </div>
      </div>
      <div className="detail-label">Open issues</div>
      <ul className="intel-issue-list">
        {twin.open_issues.map((issue) => (
          <li key={issue.id}>
            <span className={statusClass(issue.status)}>{issue.status}</span>
            <span>{issue.id.replaceAll("_", " ")}</span>
          </li>
        ))}
      </ul>
      <div className="intel-coverage-row" aria-label="Record coverage">
        <div><span>Evidence</span><strong>{pct(twin.evidence_coverage)}</strong></div>
        <div><span>Pleading</span><strong>{pct(twin.pleading_coverage)}</strong></div>
        <div><span>Procedural risk</span><strong>{pct(twin.procedural_risk)}</strong></div>
        <div><span>Discovery leverage</span><strong>{pct(twin.discovery_leverage)}</strong></div>
      </div>
      {twin.weakest_element && (
        <p className="detail-copy">
          Weakest covered element: <strong>{twin.weakest_element}</strong>
          {twin.best_next_evidence ? ` · Best next evidence: ${twin.best_next_evidence}` : ""}
        </p>
      )}
      <CoverageNote />
    </div>
  );
}

export function ClaimMatrixPanel({ matrices }: { matrices: ClaimMatrix[] }) {
  if (!matrices.length) return null;
  return (
    <div className="intel-matrices">
      {matrices.map((matrix) => {
        const report = coverageReport(matrix);
        return (
          <div key={matrix.claim_id} className="intel-matrix">
            <div className="intel-matrix-head">
              <h3>{matrix.claim}</h3>
              <span>{pct(report.coverage)} coverage</span>
            </div>
            <ul className="intel-element-list">
              {matrix.elements.map((element) => (
                <li key={element.id}>
                  <div className="intel-element-top">
                    <strong>{element.label}</strong>
                    <span>{pct(report.elements.find((row) => row.id === element.id)?.coverage ?? 0)}</span>
                  </div>
                  {element.allegation && <p>{element.allegation}</p>}
                  {element.defense && <p className="intel-defense">Defense: {element.defense}</p>}
                </li>
              ))}
            </ul>
            {report.weakest && (
              <p className="detail-copy">Weakest element: {report.weakest}{report.best_next_evidence ? ` · next evidence: ${report.best_next_evidence}` : ""}</p>
            )}
          </div>
        );
      })}
    </div>
  );
}

export function DependencyClocks({ clocks }: { clocks: PendingClock[] }) {
  if (!clocks.length) return null;
  return (
    <ul className="intel-list">
      {clocks.map((clock) => (
        <li key={clock.id}>
          <span className={statusClass(clock.status)}>{clock.status.replaceAll("_", " ")}</span>
          {" "}{clock.label}
          {clock.displayDate ? ` — ${clock.displayDate}` : clock.waitingOn ? ` — waiting on: ${clock.waitingOn}` : ""}
        </li>
      ))}
    </ul>
  );
}

export function WarRoomCard({ room }: { room: WarRoom }) {
  return (
    <article className="intel-war-room">
      <p className="intel-kicker">War Room — Matter {room.matter}{room.docket != null ? ` / Dkt. ${room.docket}` : ""}</p>
      <h3>{room.event}</h3>
      <p className="detail-copy">{room.immediate}</p>
      <div className="detail-label">Defense attacks</div>
      <ul className="intel-issue-list">
        {room.attacks.map((attack) => (
          <li key={attack.issue}>
            <span className={statusClass(attack.level)}>{attack.level}</span>
            <span>{attack.issue.replaceAll("_", " ")}</span>
          </li>
        ))}
      </ul>
      <p className="detail-copy">
        New authorities: {room.newAuthorities.length}. In CiteProof: {room.authoritiesInCiteProof.length}.
        Weak or overstated: {room.weakOrMiscited.length}. Cross-matter:{" "}
        {room.crossMatters.map((number) => (
          <Link key={number} to={`${ROUTES.matters}/${number}`}> {number}</Link>
        ))}
      </p>
      <div className="detail-label">Recommended sequence</div>
      <ol className="intel-sequence">
        {room.sequence.map((step) => <li key={step}>{step}</li>)}
      </ol>
    </article>
  );
}
