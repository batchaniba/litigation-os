import type { CourtKey, RuleCitation } from "./types";

/** Primary-source citations for computation rules and court calendars. */
export const SOURCES = {
  ccp12: {
    id: "ccp12",
    label: "CCP §12",
    url: "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CCP&sectionNum=12.",
    note: "Exclude the first day; include the last day when computing time.",
  },
  ccp12a: {
    id: "ccp12a",
    label: "CCP §12a",
    url: "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CCP&sectionNum=12a.",
    note: "If the last day falls on a Saturday or holiday, extend to the next non-holiday day.",
  },
  ccp12c: {
    id: "ccp12c",
    label: "CCP §12c",
    url: "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CCP&sectionNum=12c.",
    note: "Count backward from the hearing date, excluding the hearing day; service add-ons count further backward.",
  },
  ccp135: {
    id: "ccp135",
    label: "CCP §135",
    url: "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CCP&sectionNum=135.",
    note: "Defines judicial holidays observed by California courts.",
  },
  ccp1005: {
    id: "ccp1005",
    label: "CCP §1005(b)",
    url: "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CCP&sectionNum=1005.",
    note: "Moving papers 16 court days; opposition 9 court days; reply 5 court days before hearing. Mail within California adds 5 calendar days to moving-paper notice.",
  },
  ccp41220: {
    id: "ccp41220",
    label: "CCP §412.20(a)(3)",
    url: "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CCP&sectionNum=412.20.",
    note: "Defendant must respond within 30 days after summons is served.",
  },
  ccp43041: {
    id: "ccp43041",
    label: "CCP §430.41(a)(2)",
    url: "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CCP&sectionNum=430.41.",
    note: "Meet-and-confer at least 5 days before the responsive-pleading deadline if demurring.",
  },
  ccp10106: {
    id: "ccp10106",
    label: "CCP §1010.6",
    url: "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CCP&sectionNum=1010.6.",
    note: "Electronic service timing; demurrer notice also references this via CRC 3.1320(c).",
  },
  crc111: {
    id: "crc111",
    label: "CRC 1.11",
    url: "https://courts.ca.gov/cms/rules/index/one/rule1_11",
    note: "Judicial holiday on Saturday observed Friday; on Sunday observed Monday.",
  },
  crc3110: {
    id: "crc3110",
    label: "CRC 3.110(b)",
    url: "https://courts.ca.gov/cms/rules/index/three/rule3_110",
    note: "Complaint must be served and proof of service filed within 60 days of filing.",
  },
  crc3724: {
    id: "crc3724",
    label: "CRC 3.724",
    url: "https://courts.ca.gov/cms/rules/index/three/rule3_724",
    note: "Meet-and-confer no later than 30 calendar days before the initial case management conference.",
  },
  crc3725: {
    id: "crc3725",
    label: "CRC 3.725",
    url: "https://courts.ca.gov/cms/rules/index/three/rule3_725",
    note: "Case management statement due no later than 15 calendar days before the CMC.",
  },
  crc31320: {
    id: "crc31320",
    label: "CRC 3.1320(c)–(d)",
    url: "https://courts.ca.gov/cms/rules/index/three/rule3_1320",
    note: "Demurrer notice of hearing must comply with CCP §1005; hearing generally within 35 days of demurrer filing.",
  },
  frcp6: {
    id: "frcp6",
    label: "FRCP 6",
    url: "https://www.law.cornell.edu/rules/frcp/rule_6",
    note: "Federal day-counting, legal holidays, and +3 days after mail service under Rule 6(d).",
  },
  frcp6c: {
    id: "frcp6c",
    label: "FRCP 6(c)",
    url: "https://www.law.cornell.edu/rules/frcp/rule_6",
    note: "Written motion and notice at least 14 days before hearing; opposing affidavit at least 7 days before hearing.",
  },
  frcp12: {
    id: "frcp12",
    label: "FRCP 12(a)(1)(A)",
    url: "https://www.law.cornell.edu/rules/frcp/rule_12",
    note: "Answer due within 21 days after being served with the summons and complaint.",
  },
  caHolidays: {
    id: "caHolidays",
    label: "California Courts — Court Holidays 2026",
    url: "https://courts.ca.gov/about/court-holidays",
    note: "Statewide judicial holiday schedule published by the Judicial Branch.",
  },
  sjCourts: {
    id: "sjCourts",
    label: "San Joaquin Superior Court — Holidays",
    url: "https://www.sjcourts.org/court-hours-and-holidays",
  },
  alamedaCourts: {
    id: "alamedaCourts",
    label: "Alameda Superior Court — Holidays",
    url: "https://www.alameda.courts.ca.gov/general-information/holidays",
  },
  sacramentoCourts: {
    id: "sacramentoCourts",
    label: "Sacramento Superior Court — Holidays",
    url: "https://www.saccourt.ca.gov/general/holidays.aspx",
  },
  santaClaraCourts: {
    id: "santaClaraCourts",
    label: "Santa Clara Superior Court — Holidays",
    url: "https://santaclara.courts.ca.gov/general-information/court-holidays",
  },
  caedHolidays: {
    id: "caedHolidays",
    label: "USDC E.D. Cal. — Court Holidays",
    url: "https://www.caed.uscourts.gov/caednew/index.cfm/clerks-office/court-holidays/",
    note: "Includes Chief Judge closures (day after Thanksgiving, Christmas Eve, New Year's Eve).",
  },
  candHolidays: {
    id: "candHolidays",
    label: "USDC N.D. Cal. — Court Holidays",
    url: "https://cand.uscourts.gov/about/court/locations-hours/court-holidays",
  },
} as const satisfies Record<string, RuleCitation>;

export const COURT_HOLIDAY_SOURCES: Record<CourtKey, RuleCitation[]> = {
  "San Joaquin Sup. Ct.": [SOURCES.caHolidays, SOURCES.sjCourts, SOURCES.crc111],
  "Alameda Sup. Ct.": [SOURCES.caHolidays, SOURCES.alamedaCourts, SOURCES.crc111],
  "Sacramento Sup. Ct.": [SOURCES.caHolidays, SOURCES.sacramentoCourts, SOURCES.crc111],
  "Santa Clara Sup. Ct.": [SOURCES.caHolidays, SOURCES.santaClaraCourts, SOURCES.crc111],
  "USDC E.D. Cal.": [SOURCES.caedHolidays, SOURCES.frcp6],
  "USDC N.D. Cal.": [SOURCES.candHolidays, SOURCES.frcp6],
};

export const DISCLAIMER =
  "Computed dates are aids derived from the cited rules and published court holiday calendars. Local rules, court orders, stipulations, and e-filing cutoffs can change the operative deadline. Verify every date against the docket and governing order before relying on it.";
