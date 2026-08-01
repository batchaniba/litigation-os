export const ROUTES = {
  dashboard: "/",
  matters: "/matters",
  timeline: "/timeline",
  damages: "/damages",
  theories: "/theories",
  costOfCounsel: "/cost-of-counsel",
  outcomes: "/outcomes",
  judicialOpinions: "/judicial-opinions",
  notableQuotes: "/notable-quotes",
} as const;

export const NAV_ITEMS = [
  { label: "Dashboard", path: ROUTES.dashboard, end: true },
  { label: "Matters", path: ROUTES.matters, end: false },
  { label: "Timeline", path: ROUTES.timeline, end: false },
  { label: "Damages", path: ROUTES.damages, end: false },
  { label: "Theories", path: ROUTES.theories, end: false },
  { label: "Cost of Counsel", path: ROUTES.costOfCounsel, end: false },
  { label: "Profit", path: ROUTES.outcomes, end: false },
  { label: "Judicial Opinions", path: ROUTES.judicialOpinions, end: false },
  { label: "Notable Quotes", path: ROUTES.notableQuotes, end: false },
] as const;

export const routeForTab = (tab: string) =>
  NAV_ITEMS.find((item) => item.label === tab)?.path ?? ROUTES.dashboard;
