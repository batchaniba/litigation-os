import { BookingPanel } from "../components/BookingPanel";
import { loadLeadDraft } from "../lib/leads";

export function BookPage() {
  const draft = loadLeadDraft();

  return (
    <main className="section booking" style={{ paddingTop: "calc(var(--nav-h) + 3rem)" }}>
      <div className="container booking-grid">
        <div>
          <p className="eyebrow">Free orientation</p>
          <h1 className="section-title">Let’s map your equity-to-Bitcoin path.</h1>
          <p className="section-lede">
            Thirty focused minutes on feasibility, compliance boundaries, and whether a milestone agreement makes sense.
            You leave with clarity — not a pitch deck hangover.
          </p>
          {draft.quizBand && (
            <div className="score-pill" style={{ marginTop: "1.25rem" }}>
              Equity IQ synced · {draft.quizBand}
              {draft.quizScore != null ? ` (${draft.quizScore})` : ""}
            </div>
          )}
          <p className="compliance-strip">
            Educational consultation only. Not a loan application. Not investment advice. You keep full control of
            every financial decision.
          </p>
        </div>
        <BookingPanel />
      </div>
    </main>
  );
}
