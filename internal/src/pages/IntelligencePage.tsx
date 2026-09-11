import { Link } from "react-router";
import {
  getLitigationOS,
  qiRadar,
  recapAdvice,
  shockwaveFromOpinion,
  simulateDomino,
  systemicImportance,
} from "../intelligence";
import { cases, getMatterSummary } from "../data/matters";
import { ROUTES } from "../routes";
import { CoverageNote, DependencyClocks, WarRoomCard } from "../components/intelligence/CommandPanels";

function MatterLink({ number }: { number: number }) {
  const summary = getMatterSummary(number);
  return (
    <Link className="intel-matter-link" to={`${ROUTES.matters}/${number}`}>
      Matter {number}{summary ? ` — ${summary.caption}` : ""}
    </Link>
  );
}

export function IntelligencePage() {
  const os = getLitigationOS();
  const ranking = systemicImportance(cases, os.graph, os.catalog);
  const radar = qiRadar(os.graph, os.catalog);
  const shock = shockwaveFromOpinion(
    {
      title: "Example v. County (watch)",
      court: "CA9",
      issues: ["qualified_immunity"],
      holdings: "A Ninth Circuit opinion narrowing clearly-established law would refresh the Serrato MTD and the anticipated HOPE QI fight.",
    },
    os.catalog,
  );
  const survives = simulateDomino({ kind: "survives_mtd", matter: 24 }, os.graph, os.catalog);
  const rejected = simulateDomino({ kind: "theory_rejected", issue: "pc_290_46" }, os.graph, os.catalog);
  const counsel = os.catalog.attorneys.filter((attorney) => attorney.matters.length > 1);
  const recap = os.catalog.recap.map(recapAdvice);
  const waiting = os.clocks.filter((clock) => clock.status === "waiting_on_trigger");
  const rooms = os.warRooms.slice(0, 4);

  return (
    <article className="intel-page">
      <header className="intel-hero">
        <h1 className="tab-title">Litigation Intelligence</h1>
        <p className="detail-copy detail-copy-secondary">
          CourtListener is the event stream. This page is the command center: a knowledge graph,
          per-matter twins, defense fingerprints, dependency clocks, and war rooms. It reasons about
          legal state. It does not file anything.
        </p>
        <CoverageNote />
      </header>

      <section className="intel-panel" aria-labelledby="overnight-title">
        <h2 id="overnight-title">Overnight brief</h2>
        <p className="intel-kicker">{os.overnight.asOf}</p>
        <p className="detail-copy"><strong>Highest-priority action:</strong> {os.overnight.highestPriority}</p>
        <ul className="intel-list">
          {os.overnight.docketChanges.slice(0, 6).map((row) => <li key={row}>{row}</li>)}
        </ul>
        {os.overnight.precedent.slice(0, 4).map((row) => <p key={row} className="detail-copy">{row}</p>)}
        {os.overnight.citationNotes.map((row) => <p key={row} className="detail-copy intel-defense">{row}</p>)}
      </section>

      <section className="intel-panel" aria-labelledby="systemic-title">
        <h2 id="systemic-title">Systemic importance</h2>
        <p className="detail-copy">
          Not settlement value. A matter can be modest in dollars and still control four other dockets.
        </p>
        <ol className="intel-rank">
          {ranking.slice(0, 8).map((row) => (
            <li key={row.matter}>
              <div className="intel-rank-top">
                <MatterLink number={row.matter} />
                <span className="intel-score">{row.score}</span>
              </div>
              <div className="intel-bar" aria-hidden="true"><span style={{ width: `${row.score}%` }} /></div>
              <p className="intel-reasons">{row.reasons.join(" · ")}</p>
            </li>
          ))}
        </ol>
      </section>

      <section className="intel-panel" aria-labelledby="qi-title">
        <h2 id="qi-title">Qualified immunity radar</h2>
        <p className="detail-copy">
          Active or anticipated QI fights:{" "}
          {radar.matters.map((number) => <MatterLink key={number} number={number} />)}
        </p>
        <p className="detail-copy">Plaintiff-side authorities: {radar.supporting.map((row) => row.label).join("; ")}</p>
        <p className="detail-copy">Adverse / defense authorities: {radar.adverse.map((row) => row.label).join("; ")}</p>
        <p className="detail-copy">Counsel who have raised or are expected to raise it: {radar.attorneys.join("; ")}</p>
      </section>

      <section className="intel-panel" aria-labelledby="counsel-title">
        <h2 id="counsel-title">Opposing-party graph</h2>
        <ul className="intel-list">
          {counsel.map((attorney) => (
            <li key={attorney.id}>
              {attorney.name} ({attorney.firm}) — matters {attorney.matters.join(", ")}
            </li>
          ))}
        </ul>
        {os.catalog.fingerprints.map((profile) => (
          <div key={profile.id} className="intel-fingerprint">
            <h3>{profile.attorney}</h3>
            <p className="detail-copy">Lead defense: {profile.leadDefense}</p>
            <p className="detail-copy">Tactics: {profile.tactics.join(" · ")}</p>
          </div>
        ))}
      </section>

      <section className="intel-panel" aria-labelledby="domino-title">
        <h2 id="domino-title">Portfolio domino</h2>
        <p className="detail-copy"><strong>{survives.hypothesis}</strong></p>
        <ul className="intel-list">
          {survives.effects.slice(0, 8).map((effect) => (
            <li key={`s-${effect.matter}`}>{effect.delta} · Matter {effect.matter} ({effect.impact}) — {effect.reason}</li>
          ))}
        </ul>
        <p className="detail-copy"><strong>{rejected.hypothesis}</strong></p>
        <ul className="intel-list">
          {rejected.effects.map((effect) => (
            <li key={`r-${effect.matter}`}>{effect.delta} · Matter {effect.matter} ({effect.impact}) — {effect.reason}</li>
          ))}
        </ul>
        <div className="detail-label">Precedent shockwave (QI watch)</div>
        <ul className="intel-list">
          {shock.hits.map((hit) => (
            <li key={hit.matter}>Matter {hit.matter} — {hit.impact}: {hit.reason}</li>
          ))}
        </ul>
      </section>

      <section className="intel-panel" aria-labelledby="clocks-title">
        <h2 id="clocks-title">Dependency clocks</h2>
        <p className="detail-copy">
          Serrato&apos;s CMC is not October 15. It is fourteen days after the final order on Dkt. 18.
          Until that order enters, there is no date certain.
        </p>
        <DependencyClocks clocks={waiting} />
      </section>

      <section className="intel-panel" aria-labelledby="recap-title">
        <h2 id="recap-title">RECAP / PACER gate</h2>
        <ul className="intel-list">
          {recap.map((row) => (
            <li key={row.documentId}>
              <span className={`intel-tag ${row.action === "skip" ? "" : row.action === "wait" ? "intel-tag-warn" : "intel-tag-hot"}`}>{row.action}</span>
              {" "}{row.reason}
            </li>
          ))}
        </ul>
      </section>

      <section className="intel-panel" aria-labelledby="war-title">
        <h2 id="war-title">War rooms</h2>
        {rooms.length ? rooms.map((room) => <WarRoomCard key={`${room.matter}-${room.event}`} room={room} />) : (
          <p className="detail-copy">No significant motion/order events matched the live-motion catalog in this pass.</p>
        )}
      </section>
    </article>
  );
}

export default IntelligencePage;
