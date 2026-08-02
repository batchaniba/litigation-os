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

export const VOLATILITY_STATEMENT =
  "Bitcoin is highly volatile. Drawdowns of 50% happen regularly. Declines of 80% or more have occurred in every market cycle to date. Any strategy that borrows against your home to acquire it places a fixed, secured obligation against an asset that can lose most of its value — and your home is the collateral. Nothing on this site should be read as a prediction that Bitcoin will rise.";

export const GOOD_FIT = [
  "You own your home and have meaningful equity beyond the cushion lenders typically require you to keep.",
  "You can comfortably service an additional monthly payment from current income — without counting on Bitcoin going up.",
  "You have a long horizon and will not need this capital back within four to six years.",
  "You want to understand the mechanics yourself rather than hand decisions to someone else.",
  "You already know Bitcoin can fall 50%+ and have decided that is a risk you can live with.",
];

export const POOR_FIT = [
  "You would need to sell Bitcoin to make the loan payment.",
  "Your income is unstable, or the new payment would stretch your monthly budget.",
  "You might need the equity soon for renovation, tuition, medical costs, or near-term retirement.",
  "You are behind on your mortgage, or your equity cushion is already thin.",
  "You want someone to tell you Bitcoin will go up. We will not.",
  "A 50–80% drawdown would cause you real financial or personal distress.",
];

export const FAQS = [
  {
    q: "What exactly am I paying for?",
    a: "Education, documentation support, and milestone verification across five phases. You are not paying for a loan, for Bitcoin, or for advice about whether to buy it.",
  },
  {
    q: "Do you handle my loan proceeds or Bitcoin?",
    a: "No. Never. You apply to a licensed lender directly. You buy Bitcoin yourself. You hold your own keys. Nothing passes through us.",
  },
  {
    q: "Do you arrange the loan?",
    a: "No. We are not mortgage brokers or loan originators. We teach what lenders look for and help you assemble a complete package. Choosing the lender and accepting terms are yours.",
  },
  {
    q: "How much is the fee, and when do I pay?",
    a: "30% of the equity you extract, charged once at Phase 3 — after verified loan approval and funding. Phases 1, 2, 4, and 5 carry no fee. On a $200,000 draw the fee is $60,000.",
  },
  {
    q: "So less than I borrow actually reaches Bitcoin?",
    a: "Correct — and this is the most important thing to understand before going further. If you draw $200,000, the fee is $60,000 and $140,000 reaches Bitcoin, but you owe payments on the full $200,000. The calculator shows that subtraction explicitly.",
  },
  {
    q: "What if my loan is denied?",
    a: "There is no success fee without verified extraction. Phases 1 and 2 are free, so a denial costs you time, not a milestone invoice.",
  },
  {
    q: "What happens if Bitcoin falls after I buy?",
    a: "You still owe your lender every dollar, on schedule, and your home secures it. This strategy is only appropriate if you can service the loan from income regardless of what Bitcoin does.",
  },
  {
    q: "Could I lose my home?",
    a: "A HELOC or cash-out refinance is secured by your home. If you cannot make payments, the lender has recourse against the property, up to and including foreclosure. That deserves stating plainly because proceeds are going into a volatile asset.",
  },
  {
    q: "Are returns guaranteed or projected?",
    a: "Neither. We do not publish return projections. Historical cycle material describes what happened, not what will. Past performance says nothing reliable about the future.",
  },
  {
    q: "Are you a registered investment adviser?",
    a: "No. We do not manage assets or make personalized recommendations about whether Bitcoin belongs in your portfolio. Our services are educational. For tailored advice, speak with a licensed fiduciary.",
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
        "Your equity position, timeline, and curiosity suggest a high-signal conversation. Book a free orientation and we will walk the milestone path with clear compliance boundaries — including whether this is wrong for you.",
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
      "You may still benefit from the free orientation, especially if equity access or Bitcoin literacy is early-stage. Run the calculator and book when timing feels right.",
  };
}

export const BTC_CYCLES = [
  {
    halving: "November 2012",
    reward: "50 → 25 BTC",
    peak: "Late 2013",
    move: "Roughly $12 to roughly $1,100",
    drawdown: "Followed by an ~85% decline into 2015",
  },
  {
    halving: "July 2016",
    reward: "25 → 12.5 BTC",
    peak: "December 2017",
    move: "Roughly $650 to nearly $20,000",
    drawdown: "Followed by an ~84% decline into 2018",
  },
  {
    halving: "May 2020",
    reward: "12.5 → 6.25 BTC",
    peak: "November 2021",
    move: "Roughly $8,500 to above $67,000",
    drawdown: "Followed by a ~77% decline into 2022",
  },
  {
    halving: "April 2024",
    reward: "6.25 → 3.125 BTC",
    peak: "Ongoing",
    move: "Outcome not yet known",
    drawdown: "Unknown — the cycle has not completed",
  },
] as const;
