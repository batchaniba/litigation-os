import { cases } from "./matters";
import { timeline } from "./timeline";
import { theories } from "./theories";
import { damages_table, matter_damages } from "./damages";
import { lawyer_fees, lawyer_fees_summary } from "./lawyerFees";
import { outcomes } from "./outcomes";
import { census } from "./census";

export const PORTFOLIO = {
  plaintiff: "Brendan Ngehsi Newanforbi",
  representation: "Pro Se / In Propria Persona",
  contact: { address: "1090 S Milpitas Blvd, Unit #304, Milpitas, CA 95035" },
  prepared_date: "May 6, 2026",
  jurisdictions: ["USDC E.D. Cal.", "USDC N.D. Cal.", "San Joaquin Sup. Ct.", "Alameda Sup. Ct.", "Sacramento Sup. Ct.", "Santa Clara Sup. Ct."],
  cases,
  timeline,
  theories,
  damages_table,
  matter_damages,
  lawyer_fees,
  lawyer_fees_summary,
  outcomes,
  census,
};
