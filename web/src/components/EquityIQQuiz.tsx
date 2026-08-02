import { useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { QUIZ_QUESTIONS, scoreQuiz, type QuizAnswers } from "../data/content";
import { saveLeadDraft } from "../lib/leads";

export function EquityIQQuiz() {
  const [step, setStep] = useState(0);
  const [answers, setAnswers] = useState<QuizAnswers>({});
  const [selected, setSelected] = useState<string | null>(null);

  const finished = step >= QUIZ_QUESTIONS.length;
  const question = QUIZ_QUESTIONS[step];
  const result = useMemo(() => (finished ? scoreQuiz(answers) : null), [answers, finished]);

  function choose(value: string) {
    setSelected(value);
  }

  function next() {
    if (!question || !selected) return;
    const nextAnswers = { ...answers, [question.id]: selected };
    setAnswers(nextAnswers);
    setSelected(null);

    if (step + 1 >= QUIZ_QUESTIONS.length) {
      const scored = scoreQuiz(nextAnswers);
      saveLeadDraft({
        source: "equity-iq",
        quizAnswers: nextAnswers,
        quizBand: scored.band,
        quizScore: scored.score,
      });
      setStep(step + 1);
      return;
    }
    setStep(step + 1);
  }

  function back() {
    if (step === 0) return;
    setStep((s) => s - 1);
    const prev = QUIZ_QUESTIONS[step - 1];
    setSelected(answers[prev.id] ?? null);
  }

  function reset() {
    setStep(0);
    setAnswers({});
    setSelected(null);
  }

  return (
    <div className="quiz-panel" aria-live="polite">
      {!finished && (
        <>
          <div className="quiz-progress" aria-hidden="true">
            {QUIZ_QUESTIONS.map((q, i) => (
              <i key={q.id} className={i <= step ? "is-done" : undefined} />
            ))}
          </div>
          <div className="quiz-question">{question.prompt}</div>
          <div className="quiz-options" role="radiogroup" aria-label={question.prompt}>
            {question.options.map((option) => (
              <button
                key={option.value}
                type="button"
                role="radio"
                aria-checked={selected === option.value}
                className={`quiz-option${selected === option.value ? " is-selected" : ""}`}
                onClick={() => choose(option.value)}
              >
                {option.label}
              </button>
            ))}
          </div>
          <div className="quiz-nav">
            <button type="button" className="btn btn-ghost" onClick={back} disabled={step === 0}>
              Back
            </button>
            <button type="button" className="btn btn-primary" onClick={next} disabled={!selected}>
              {step === QUIZ_QUESTIONS.length - 1 ? "See my Equity IQ" : "Continue"}
            </button>
          </div>
        </>
      )}

      {finished && result && (
        <div className="quiz-result">
          <div className="score-pill">
            Equity IQ {result.score}/{result.max} · {result.label}
          </div>
          <h3>{result.label}</h3>
          <p>{result.summary}</p>
          <div style={{ display: "flex", flexWrap: "wrap", gap: "0.75rem" }}>
            <Link to="/book" className="btn btn-primary">
              Book free orientation
            </Link>
            <button type="button" className="btn btn-ghost" onClick={reset}>
              Retake quiz
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
