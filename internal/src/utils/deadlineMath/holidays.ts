import { COURT_HOLIDAY_SOURCES, SOURCES } from "./sources";
import type { CourtKey, DayKey, Forum, Holiday } from "./types";

/** California superior-court judicial holidays (2026–2027), from courts.ca.gov + county pages. */
const CA_STATE_HOLIDAYS: Holiday[] = [
  // 2026 — https://courts.ca.gov/about/court-holidays
  { date: "2026-01-01", name: "New Year's Day", sourceId: SOURCES.caHolidays.id },
  { date: "2026-01-19", name: "Dr. Martin Luther King, Jr. Day", sourceId: SOURCES.caHolidays.id },
  { date: "2026-02-12", name: "Lincoln's Birthday", sourceId: SOURCES.caHolidays.id },
  { date: "2026-02-16", name: "President's Day", sourceId: SOURCES.caHolidays.id },
  { date: "2026-03-31", name: "Farmworkers Day", sourceId: SOURCES.caHolidays.id },
  { date: "2026-05-25", name: "Memorial Day", sourceId: SOURCES.caHolidays.id },
  { date: "2026-06-19", name: "Juneteenth", sourceId: SOURCES.caHolidays.id },
  { date: "2026-07-03", name: "Independence Day (observed)", sourceId: SOURCES.caHolidays.id },
  { date: "2026-09-07", name: "Labor Day", sourceId: SOURCES.caHolidays.id },
  { date: "2026-09-25", name: "Native American Day", sourceId: SOURCES.caHolidays.id },
  { date: "2026-11-11", name: "Veterans Day", sourceId: SOURCES.caHolidays.id },
  { date: "2026-11-26", name: "Thanksgiving", sourceId: SOURCES.caHolidays.id },
  { date: "2026-11-27", name: "Day After Thanksgiving", sourceId: SOURCES.caHolidays.id },
  { date: "2026-12-25", name: "Christmas Day", sourceId: SOURCES.caHolidays.id },
  // 2027 — Sacramento Superior / Judicial Council observed dates
  { date: "2027-01-01", name: "New Year's Day", sourceId: SOURCES.sacramentoCourts.id },
  { date: "2027-01-18", name: "Martin Luther King, Jr. Day", sourceId: SOURCES.sacramentoCourts.id },
  { date: "2027-02-12", name: "Lincoln's Birthday", sourceId: SOURCES.sacramentoCourts.id },
  { date: "2027-02-15", name: "Washington's Birthday", sourceId: SOURCES.sacramentoCourts.id },
  { date: "2027-03-31", name: "Farmworkers Day", sourceId: SOURCES.sacramentoCourts.id },
  { date: "2027-05-31", name: "Memorial Day", sourceId: SOURCES.sacramentoCourts.id },
  { date: "2027-06-18", name: "Juneteenth", sourceId: SOURCES.sacramentoCourts.id },
  { date: "2027-07-05", name: "Independence Day (observed)", sourceId: SOURCES.sacramentoCourts.id },
  { date: "2027-09-06", name: "Labor Day", sourceId: SOURCES.sacramentoCourts.id },
  { date: "2027-09-24", name: "Native American Day", sourceId: SOURCES.sacramentoCourts.id },
  { date: "2027-11-11", name: "Veterans Day", sourceId: SOURCES.sacramentoCourts.id },
  { date: "2027-11-25", name: "Thanksgiving", sourceId: SOURCES.sacramentoCourts.id },
  { date: "2027-11-26", name: "Day After Thanksgiving", sourceId: SOURCES.sacramentoCourts.id },
  { date: "2027-12-24", name: "Christmas Day (observed)", sourceId: SOURCES.sacramentoCourts.id },
  { date: "2027-12-31", name: "New Year's Day 2028 (observed)", sourceId: SOURCES.sacramentoCourts.id },
];

/** Standard federal legal holidays for N.D. Cal. (FRCP 6(a)(6) + cand.uscourts.gov). */
const FEDERAL_BASE_HOLIDAYS: Holiday[] = [
  { date: "2026-01-01", name: "New Year's Day", sourceId: SOURCES.candHolidays.id },
  { date: "2026-01-19", name: "Birthday of Martin Luther King, Jr.", sourceId: SOURCES.candHolidays.id },
  { date: "2026-02-16", name: "Washington's Birthday", sourceId: SOURCES.candHolidays.id },
  { date: "2026-05-25", name: "Memorial Day", sourceId: SOURCES.candHolidays.id },
  { date: "2026-06-19", name: "Juneteenth National Independence Day", sourceId: SOURCES.candHolidays.id },
  { date: "2026-07-03", name: "Independence Day (observed)", sourceId: SOURCES.candHolidays.id },
  { date: "2026-09-07", name: "Labor Day", sourceId: SOURCES.candHolidays.id },
  { date: "2026-10-12", name: "Columbus Day", sourceId: SOURCES.candHolidays.id },
  { date: "2026-11-11", name: "Veterans Day", sourceId: SOURCES.candHolidays.id },
  { date: "2026-11-26", name: "Thanksgiving Day", sourceId: SOURCES.candHolidays.id },
  { date: "2026-12-25", name: "Christmas Day", sourceId: SOURCES.candHolidays.id },
  { date: "2027-01-01", name: "New Year's Day", sourceId: SOURCES.candHolidays.id },
  { date: "2027-01-18", name: "Birthday of Martin Luther King, Jr.", sourceId: SOURCES.candHolidays.id },
  { date: "2027-02-15", name: "Washington's Birthday", sourceId: SOURCES.candHolidays.id },
  { date: "2027-05-31", name: "Memorial Day", sourceId: SOURCES.candHolidays.id },
  { date: "2027-06-18", name: "Juneteenth National Independence Day", sourceId: SOURCES.candHolidays.id },
  { date: "2027-07-05", name: "Independence Day (observed)", sourceId: SOURCES.candHolidays.id },
  { date: "2027-09-06", name: "Labor Day", sourceId: SOURCES.candHolidays.id },
  { date: "2027-10-11", name: "Columbus Day", sourceId: SOURCES.candHolidays.id },
  { date: "2027-11-11", name: "Veterans Day", sourceId: SOURCES.candHolidays.id },
  { date: "2027-11-25", name: "Thanksgiving Day", sourceId: SOURCES.candHolidays.id },
  { date: "2027-12-24", name: "Christmas Day (observed)", sourceId: SOURCES.candHolidays.id },
];

/**
 * E.D. Cal. publishes the federal set plus Chief Judge closures
 * (day after Thanksgiving, Christmas Eve, New Year's Eve) for 2026.
 */
const CAED_EXTRA_HOLIDAYS: Holiday[] = [
  { date: "2026-11-27", name: "Day after Thanksgiving Day (Chief Judge order)", sourceId: SOURCES.caedHolidays.id },
  { date: "2026-12-24", name: "Christmas Eve (Chief Judge order)", sourceId: SOURCES.caedHolidays.id },
  { date: "2026-12-31", name: "New Year's Eve (Chief Judge order)", sourceId: SOURCES.caedHolidays.id },
];

const byCourt: Record<CourtKey, Holiday[]> = {
  "San Joaquin Sup. Ct.": CA_STATE_HOLIDAYS,
  "Alameda Sup. Ct.": CA_STATE_HOLIDAYS,
  "Sacramento Sup. Ct.": CA_STATE_HOLIDAYS,
  "Santa Clara Sup. Ct.": CA_STATE_HOLIDAYS,
  "USDC N.D. Cal.": FEDERAL_BASE_HOLIDAYS,
  "USDC E.D. Cal.": [...FEDERAL_BASE_HOLIDAYS, ...CAED_EXTRA_HOLIDAYS],
};

export const STATE_COURTS: CourtKey[] = [
  "San Joaquin Sup. Ct.",
  "Alameda Sup. Ct.",
  "Sacramento Sup. Ct.",
  "Santa Clara Sup. Ct.",
];

export const FEDERAL_COURTS: CourtKey[] = ["USDC E.D. Cal.", "USDC N.D. Cal."];

export function forumForCourt(court: CourtKey): Forum {
  return FEDERAL_COURTS.includes(court) ? "federal" : "california";
}

export function holidaysForCourt(court: CourtKey): Holiday[] {
  return byCourt[court] ?? CA_STATE_HOLIDAYS;
}

export function holidaySet(court: CourtKey): Set<DayKey> {
  return new Set(holidaysForCourt(court).map((h) => h.date));
}

export function isWeekend(day: DayKey): boolean {
  const dow = utcWeekday(day);
  return dow === 0 || dow === 6;
}

export function isCourtHoliday(day: DayKey, court: CourtKey): boolean {
  return holidaySet(court).has(day);
}

/** Non-court day: Saturday, Sunday, or published court holiday. */
export function isNonCourtDay(day: DayKey, court: CourtKey): boolean {
  return isWeekend(day) || isCourtHoliday(day, court);
}

export function isCourtDay(day: DayKey, court: CourtKey): boolean {
  return !isNonCourtDay(day, court);
}

export function holidaySourcesForCourt(court: CourtKey) {
  return COURT_HOLIDAY_SOURCES[court];
}

function utcWeekday(day: DayKey): number {
  const [y, m, d] = day.split("-").map(Number);
  return new Date(Date.UTC(y, m - 1, d)).getUTCDay();
}
