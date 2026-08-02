import { Link } from "react-router-dom";
import { BTC_CYCLES, VOLATILITY_STATEMENT } from "../data/content";

export function WhyBitcoinPage() {
  return (
    <main className="section" style={{ paddingTop: "calc(var(--nav-h) + 3rem)" }}>
      <div className="container">
        <p className="eyebrow">Education</p>
        <h1 className="section-title">Why some homeowners look at Bitcoin</h1>
        <p className="section-lede">
          This page describes what has happened. It does not predict what will happen — and you should be sceptical of
          anyone who claims to.
        </p>

        <section className="prose-block">
          <h2>Fixed supply</h2>
          <p>
            Bitcoin’s issuance schedule is fixed in software: 21 million units, ever. Roughly every four years the rate
            of new issuance is cut in half — the “halving.” The argument some homeowners find interesting is a
            symmetry one: real estate is scarce because land and building are constrained; Bitcoin is scarce because
            the protocol enforces it.
          </p>
          <p className="fit-muted">
            That is an argument, not a guarantee. Scarcity says supply cannot expand on demand. It says nothing about
            whether demand will exist at any particular price.
          </p>
        </section>

        <section className="prose-block">
          <h2>The four-year cycle, as it played out</h2>
          <p>
            Every completed cycle so far has had a similar shape: a halving, a run to a new high roughly 12–18 months
            later, then a severe decline. Both halves of that pattern matter.
          </p>
          <div className="cycle-table-wrap">
            <table className="cycle-table">
              <thead>
                <tr>
                  <th>Halving</th>
                  <th>Block reward</th>
                  <th>Subsequent peak</th>
                  <th>Approximate move</th>
                  <th>What came next</th>
                </tr>
              </thead>
              <tbody>
                {BTC_CYCLES.map((c) => (
                  <tr key={c.halving}>
                    <td>{c.halving}</td>
                    <td>{c.reward}</td>
                    <td>{c.peak}</td>
                    <td>{c.move}</td>
                    <td>{c.drawdown}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>

        <section className="calc-meaning" style={{ marginTop: "2.5rem" }}>
          <h3>Volatility acknowledgment</h3>
          <p>{VOLATILITY_STATEMENT}</p>
        </section>

        <div className="fit-cta">
          <Link to="/calculator" className="btn btn-primary">
            See what a draw would cost to carry
          </Link>
          <Link to="/fit" className="btn btn-ghost">
            Is this for you?
          </Link>
        </div>
      </div>
    </main>
  );
}
