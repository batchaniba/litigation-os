export const BRAND = {
  name: "Equity2Bitcoin",
  legalName: "Equity2Bitcoin Consulting LLC",
  tagline: "Turning untapped home equity into sovereign opportunity.",
  principle: "Educate first, advise never, and empower always.",
};

export const PHASES = [
  {
    index: "01",
    title: "Equity Profile Review & Education",
    body: "We map your home equity position, walk through HELOC and cash-out options in plain language, and deliver a readiness report so you understand what is actually available.",
    fee: "No fee",
    paid: false,
  },
  {
    index: "02",
    title: "Loan Preparation & Documentation",
    body: "Checklists, document workflows, and underwriting education so you can submit a complete application to a licensed lender — without us brokering or arranging the loan.",
    fee: "No fee",
    paid: false,
  },
  {
    index: "03",
    title: "Loan Approval & Funding",
    body: "When your lender approves and funds the extraction, the milestone is verified. This is the only paid milestone — tied to extraction, never to Bitcoin performance.",
    fee: "30% success fee",
    paid: true,
  },
  {
    index: "04",
    title: "Bitcoin Integration & Custody Education",
    body: "Exchange onboarding, self-custody hygiene, hardware wallet practices, and long-horizon holding education. You execute every transaction yourself.",
    fee: "No fee",
    paid: false,
  },
  {
    index: "05",
    title: "Verification & Documentation",
    body: "Closing packet with third-party verification artifacts and a clear acknowledgment that the engagement was educational and non-custodial.",
    fee: "No fee",
    paid: false,
  },
] as const;

export const FAQS = [
  {
    q: "Do you handle my loan proceeds or Bitcoin?",
    a: "No. Equity2Bitcoin never takes custody of funds, Bitcoin, or loan instruments. You work with licensed lenders and execute Bitcoin purchases and custody decisions independently.",
  },
  {
    q: "Is this investment advice?",
    a: "No. We provide structured education and milestone consulting. We do not make personalized investment recommendations, manage portfolios, or advise on whether Bitcoin is appropriate for your situation.",
  },
  {
    q: "When do I pay?",
    a: "Only after Phase 3 — verified loan approval or funding. The fee is 30% of the equity extracted. Phases 1, 2, 4, and 5 carry no fee.",
  },
  {
    q: "What if my loan is denied?",
    a: "There is no success fee without verified extraction. You still keep the educational work product from earlier phases.",
  },
  {
    q: "Who is this for?",
    a: "Primarily homeowners roughly ages 35–60 with meaningful tappable equity who want a disciplined, compliance-aware path to learn how equity extraction and Bitcoin ownership can fit together — without giving up control.",
  },
  {
    q: "Is Bitcoin volatile? What about rate risk on a HELOC?",
    a: "Yes on both counts. Volatility and borrowing costs are real. Our process emphasizes education, timing awareness, and sober risk acknowledgment — never guarantees of return.",
  },
] as const;

export const QUIZ_QUESTIONS = [
  {
    id: "equity",
    prompt: "Roughly how much tappable equity do you believe you have?",
    options: [
      { label: "Under $100,000", value: "under_100k", score: 1 },
      { label: "$100,000 – $250,000", value: "100_250k", score: 2 },
      { label: "$250,000 – $500,000", value: "250_500k", score: 3 },
      { label: "Over $500,000", value: "over_500k", score: 4 },
    ],
  },
  {
    id: "ownership",
    prompt: "How long have you owned your primary residence?",
    options: [
      { label: "Less than 2 years", value: "lt_2", score: 1 },
      { label: "2 – 5 years", value: "2_5", score: 2 },
      { label: "5 – 10 years", value: "5_10", score: 3 },
      { label: "10+ years", value: "10_plus", score: 4 },
    ],
  },
  {
    id: "goal",
    prompt: "What best describes your interest right now?",
    options: [
      { label: "Just curious — educating myself", value: "curious", score: 2 },
      { label: "Exploring HELOC / cash-out options", value: "heloc", score: 3 },
      { label: "Ready to build a Bitcoin position thoughtfully", value: "btc_ready", score: 4 },
      { label: "Comparing this to other wealth strategies", value: "compare", score: 3 },
    ],
  },
  {
    id: "btc",
    prompt: "How familiar are you with Bitcoin self-custody?",
    options: [
      { label: "New — I need the basics", value: "new", score: 2 },
      { label: "I have bought before, still learning custody", value: "some", score: 3 },
      { label: "Comfortable with exchanges and wallets", value: "comfortable", score: 4 },
      { label: "Advanced / multi-sig curious", value: "advanced", score: 4 },
    ],
  },
  {
    id: "timeline",
    prompt: "When would you want to take a first concrete step?",
    options: [
      { label: "Just researching this year", value: "research", score: 1 },
      { label: "In the next 3 – 6 months", value: "3_6mo", score: 3 },
      { label: "In the next 30 – 90 days", value: "30_90", score: 4 },
      { label: "As soon as I understand the path", value: "asap", score: 4 },
    ],
  },
] as const;

export type QuizAnswers = Record<string, string>;

export function scoreQuiz(answers: QuizAnswers): {
  score: number;
  max: number;
  band: "explore" | "qualified" | "priority";
  label: string;
  summary: string;
} {
  let score = 0;
  let max = 0;
  for (const q of QUIZ_QUESTIONS) {
    max += 4;
    const selected = q.options.find((o) => o.value === answers[q.id]);
    if (selected) score += selected.score;
  }

  if (score >= 16) {
    return {
      score,
      max,
      band: "priority",
      label: "Strong fit for an orientation",
      summary:
        "Your equity position, timeline, and curiosity suggest a high-signal conversation. Book a free orientation and we will walk the milestone path with clear compliance boundaries.",
    };
  }
  if (score >= 11) {
    return {
      score,
      max,
      band: "qualified",
      label: "Good candidate — start with education",
      summary:
        "You are in range for a productive orientation. We will focus on feasibility, lender pathways, and whether this model fits your household — with no pressure to proceed.",
    };
  }
  return {
    score,
    max,
    band: "explore",
    label: "Keep learning — then revisit",
    summary:
      "You may still benefit from the free orientation, especially if equity access or Bitcoin literacy is early-stage. Grab the blueprint and book when timing feels right.",
  };
}

export const CASE_STEPS = [
  { label: "Home value", value: "$700,000" },
  { label: "Remaining mortgage", value: "$400,000" },
  { label: "Extractable equity (example)", value: "$300,000" },
  { label: "Phases 1–2 education & prep", value: "$0" },
  { label: "Phase 3 success fee (30%)", value: "$90,000" },
  { label: "Phases 4–5 Bitcoin education & close", value: "$0" },
] as const;
