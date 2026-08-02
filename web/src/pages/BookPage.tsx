import { useState } from "react";
import { Link } from "react-router-dom";
import { BookingPanel } from "../components/BookingPanel";
import { loadLeadDraft } from "../lib/leads";

export function BookPage() {
  const draft = loadLeadDraft();
  const [acknowledged, setAcknowledged] = useState(false);

  return (
    <main className="section booking" style={{ paddingTop: "calc(var(--nav-h) + 3rem)" }}>
      <div className="container booking-grid">
        <div>
          <p className="eyebrow">Free orientation · ~20 minutes</p>
          <h1 className="section-title">Let’s map your equity-to-Bitcoin path.</h1>
          <p className="section-lede">
            Feasibility, the milestone fee in your numbers, and whether this path deserves another step. If we think
            this is wrong for you, we will say so on the call.
          </p>
          {draft.quizBand && (
            <div className="score-pill" style={{ marginTop: "1.25rem" }}>
              Equity IQ synced · {draft.quizBand}
              {draft.quizScore != null ? ` (${draft.quizScore})` : ""}
            </div>
          )}

          <ul className="book-list">
            <li>Your equity position and what a lender might realistically advance</li>
            <li>The five milestones and where the single fee falls</li>
            <li>What the monthly obligation would actually be</li>
            <li>Risks stated plainly — including the ones that end the conversation</li>
            <li>Whether you should be talking to a licensed fiduciary instead</li>
          </ul>

          <p className="compliance-strip">
            Come prepared if you can: approximate home value and mortgage balance. The{" "}
            <Link to="/calculator">calculator</Link> takes two minutes and stays in your browser.
          </p>
        </div>

        <div>
          <div className="book-ack">
            <p>
              <strong>Before you book, please acknowledge:</strong>
            </p>
            <ul>
              <li>
                This call is educational — not investment advice, not a recommendation, and not an offer of credit.
              </li>
              <li>
                Equity2Bitcoin Consulting LLC is not a registered investment adviser, mortgage broker, lender, or money
                transmitter, and will not take custody of your funds or digital assets.
              </li>
              <li>
                Borrowing against your home puts your property at risk. Bitcoin is highly volatile and has declined more
                than 80% in past market cycles.
              </li>
              <li>You should consult your own attorney, accountant, and licensed financial professional before acting.</li>
            </ul>
            <label className="book-checkbox">
              <input
                type="checkbox"
                checked={acknowledged}
                onChange={(e) => setAcknowledged(e.target.checked)}
              />
              <span>I have read and understand the above.</span>
            </label>
          </div>

          {acknowledged ? (
            <BookingPanel />
          ) : (
            <div className="book-gate">
              <p>Tick the acknowledgment above to load the scheduler.</p>
            </div>
          )}
        </div>
      </div>
    </main>
  );
}
