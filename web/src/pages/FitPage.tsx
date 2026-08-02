import { Link } from "react-router-dom";
import { GOOD_FIT, POOR_FIT } from "../data/content";

export function FitPage() {
  return (
    <main className="section" style={{ paddingTop: "calc(var(--nav-h) + 3rem)" }}>
      <div className="container">
        <p className="eyebrow">Qualification</p>
        <h1 className="section-title">Is this for you? Often the answer is no.</h1>
        <p className="section-lede">
          We would rather lose a prospect here than have someone discover halfway through that this was never a fit.
          Read both columns honestly. The second matters more.
        </p>

        <div className="fit-grid">
          <div>
            <h2>This may be worth exploring if…</h2>
            <ul>
              {GOOD_FIT.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          </div>
          <div className="fit-poor">
            <h2>This is not for you if…</h2>
            <ul>
              {POOR_FIT.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          </div>
        </div>

        <section className="fit-test">
          <p className="eyebrow">The test that matters</p>
          <h2>One question decides most of this</h2>
          <p>
            Could you make the loan payment every month for the next five years if your Bitcoin position fell 80% and
            stayed there?
          </p>
          <p>
            If yes — from income, without selling anything, without strain — you may be in the population this could
            suit. If no, “probably,” or “it depends on Bitcoin,” the answer is no. Borrowing against your home creates
            a fixed obligation. Bitcoin provides no income to service it.
          </p>
          <p className="fit-muted">We will ask you this on the call. We want the true answer, not the right one.</p>
        </section>

        <section className="fit-advisers">
          <h2>Discuss with your own advisers first</h2>
          <ul>
            <li>
              <strong>Tax treatment of the interest.</strong> Deductibility depends on how borrowed funds are used.
              Ask a CPA before assuming a deduction.
            </li>
            <li>
              <strong>Your existing first mortgage.</strong> A cash-out refinance may replace a low fixed rate; a
              HELOC as a second lien can preserve it.
            </li>
            <li>
              <strong>Rate structure.</strong> Most HELOCs are variable. Model what happens if rates rise.
            </li>
            <li>
              <strong>Draw period mechanics.</strong> Interest-only periods often end with a sharp payment step-up.
            </li>
            <li>
              <strong>Alternatives.</strong> Paying higher-interest debt, funding retirement accounts, or leaving
              equity alone are all real options with merit.
            </li>
          </ul>
        </section>

        <div className="fit-cta">
          <Link to="/book" className="btn btn-primary">
            If you are still a yes, book orientation
          </Link>
          <Link to="/calculator" className="btn btn-ghost">
            Run the calculator first
          </Link>
        </div>
      </div>
    </main>
  );
}
