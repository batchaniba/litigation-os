import {
  addCalendarDaysAfter,
  addFrcpMailDays,
  rollBackwardToCourtDay,
  rollForwardToCourtDay,
  subtractCalendarDaysBefore,
  subtractCourtDaysBefore,
  subtractMailCalendarDays,
} from "./dayCount";
import { formatPortfolioDate, toDayKey } from "./format";
import { forumForCourt, holidaySourcesForCourt } from "./holidays";
import { DISCLAIMER, SOURCES } from "./sources";
import type {
  ComputedDeadline,
  ComputeInput,
  ComputeResult,
  CourtKey,
  DayKey,
  RecipeId,
  RuleCitation,
  ServiceMethod,
} from "./types";

const DEFAULT_STATE_COURT: CourtKey = "San Joaquin Sup. Ct.";
const DEFAULT_FEDERAL_COURT: CourtKey = "USDC E.D. Cal.";

export const RECIPE_META: Record<
  RecipeId,
  { label: string; forum: "california" | "federal"; anchorLabel: string; description: string }
> = {
  ca_motion_hearing: {
    label: "California motion hearing (CCP §1005)",
    forum: "california",
    anchorLabel: "Hearing date",
    description: "Moving papers, opposition, and reply counted backward in court days from the hearing.",
  },
  ca_demurrer_hearing: {
    label: "California demurrer hearing",
    forum: "california",
    anchorLabel: "Hearing date",
    description: "Same CCP §1005 briefing schedule; CRC 3.1320(c) requires demurrer notice to comply with §1005.",
  },
  ca_summons_service: {
    label: "California summons served (answer)",
    forum: "california",
    anchorLabel: "Date of service",
    description: "30-day responsive pleading clock under CCP §412.20(a)(3), with CCP §12a weekend/holiday roll.",
  },
  ca_demurrer_meet_confer: {
    label: "Demurrer meet-and-confer (CCP §430.41)",
    forum: "california",
    anchorLabel: "Responsive pleading deadline",
    description: "Meet-and-confer at least 5 calendar days before the responsive-pleading deadline.",
  },
  ca_crc_service_deadline: {
    label: "Complaint service / proof (CRC 3.110)",
    forum: "california",
    anchorLabel: "Complaint filing date",
    description: "60 days from filing to serve and file proof of service.",
  },
  ca_cmc_statement: {
    label: "Case management statement (CRC 3.725)",
    forum: "california",
    anchorLabel: "CMC date",
    description: "CM-110 due 15 calendar days before the case management conference; M&C 30 days before (CRC 3.724).",
  },
  federal_motion_hearing: {
    label: "Federal motion hearing (FRCP 6(c))",
    forum: "federal",
    anchorLabel: "Hearing date",
    description: "Motion/notice 14 days before hearing; opposing affidavit 7 days before hearing.",
  },
  federal_answer_after_service: {
    label: "Federal answer after service (FRCP 12)",
    forum: "federal",
    anchorLabel: "Date of service",
    description: "21 days to answer after service of summons and complaint, computed under FRCP 6(a).",
  },
  federal_response_after_mail_service: {
    label: "Federal response after mail service (+3)",
    forum: "federal",
    anchorLabel: "Date of mail service",
    description: "Illustrates FRCP 6(d): after a 14-day response period expires under 6(a), add 3 days for mail.",
  },
  edcal_lr230c_opposition: {
    label: "E.D. Cal. L.R. 230(c) opposition",
    forum: "federal",
    anchorLabel: "Motion filing date",
    description: "Opposition due 14 calendar days after the motion is filed, then FRCP 6(a) last-day roll.",
  },
  edcal_lr230d_reply: {
    label: "E.D. Cal. L.R. 230(d) reply",
    forum: "federal",
    anchorLabel: "Opposition filing date",
    description: "Reply due 10 calendar days after the opposition is filed, then FRCP 6(a) last-day roll.",
  },
};

function cite(...ids: (keyof typeof SOURCES)[]): RuleCitation[] {
  return ids.map((id) => SOURCES[id]);
}

function deadline(partial: Omit<ComputedDeadline, "displayDate"> & { displayDate?: string }): ComputedDeadline {
  return {
    ...partial,
    displayDate: partial.displayDate ?? formatPortfolioDate(partial.date),
  };
}

function mailExtraDays(method: ServiceMethod | undefined): { days: number; label: string; citations: RuleCitation[] } | null {
  switch (method) {
    case "mail_ca":
      return { days: 5, label: "mail within California (+5 calendar days)", citations: cite("ccp1005", "ccp12c") };
    case "mail_out_of_state":
      return { days: 10, label: "mail out of state (+10 calendar days)", citations: cite("ccp1005", "ccp12c") };
    case "mail_out_of_country":
      return { days: 20, label: "mail outside the United States (+20 calendar days)", citations: cite("ccp1005", "ccp12c") };
    case "overnight":
      return { days: 2, label: "overnight / fax / express (+2 calendar days)", citations: cite("ccp1005", "ccp12c") };
    case "electronic":
      // CCP 1010.6 electronic extensions are court-day based in some contexts; surface personal-service
      // baseline and note electronic rules separately rather than silently applying a wrong add-on.
      return null;
    default:
      return null;
  }
}

function caMotionBriefing(
  hearing: DayKey,
  court: CourtKey,
  serviceMethod: ServiceMethod | undefined,
  demurrer: boolean,
): ComputedDeadline[] {
  const moving = subtractCourtDaysBefore(hearing, 16, court);
  const opposition = subtractCourtDaysBefore(hearing, 9, court);
  const reply = subtractCourtDaysBefore(hearing, 5, court);
  const baseCitations = demurrer ? cite("ccp1005", "ccp12c", "crc31320") : cite("ccp1005", "ccp12c");

  const out: ComputedDeadline[] = [
    deadline({
      id: "moving_papers",
      label: "Moving & supporting papers (file / personal service)",
      date: moving,
      rolled: false,
      citations: baseCitations,
      explanation: `16 court days before ${formatPortfolioDate(hearing)} under CCP §1005(b), counting backward and excluding the hearing day (CCP §12c).`,
    }),
    deadline({
      id: "opposition",
      label: "Opposition papers",
      date: opposition,
      rolled: false,
      citations: baseCitations,
      explanation: `9 court days before ${formatPortfolioDate(hearing)} under CCP §1005(b).`,
    }),
    deadline({
      id: "reply",
      label: "Reply papers",
      date: reply,
      rolled: false,
      citations: baseCitations,
      explanation: `5 court days before ${formatPortfolioDate(hearing)} under CCP §1005(b).`,
    }),
  ];

  const mail = mailExtraDays(serviceMethod);
  if (mail) {
    const served = subtractMailCalendarDays(moving, mail.days, court);
    out.unshift(
      deadline({
        id: "moving_papers_mail_service",
        label: `Moving papers — service by ${mail.label}`,
        date: served.date,
        rawDate: served.rawDate,
        rolled: served.rolled,
        citations: mail.citations,
        explanation: [
          `Personal-service / filing floor is ${formatPortfolioDate(moving)} (16 court days).`,
          `Count back ${mail.days} more calendar days under CCP §1005(b) / §12c(b) → ${formatPortfolioDate(served.rawDate)}.`,
          served.rolled
            ? `That day is a weekend or court holiday, so the service deadline rolls to the prior court day ${formatPortfolioDate(served.date)}.`
            : "That day is a court day, so it is the mail-service deadline.",
          "CCP §1013 does not further extend CCP §1005 motion notice.",
        ].join(" "),
      }),
    );
  } else if (serviceMethod === "electronic") {
    out.unshift(
      deadline({
        id: "moving_papers_electronic_note",
        label: "Moving papers — electronic service",
        date: moving,
        rolled: false,
        citations: cite("ccp1005", "ccp10106", "crc31320"),
        explanation:
          "Electronic service of moving papers is governed by CCP §1010.6 / CRC 2.251 in addition to the 16-court-day CCP §1005 floor. Confirm the applicable electronic-service extension (often 2 court days) for the method used; this engine surfaces the §1005 personal-service floor as the baseline.",
      }),
    );
  }

  return out;
}

function computeDeadlines(input: ComputeInput, court: CourtKey): ComputedDeadline[] {
  const anchor = toDayKey(input.anchorDate);

  switch (input.recipe) {
    case "ca_motion_hearing":
      return caMotionBriefing(anchor, court, input.serviceMethod ?? "personal", false);
    case "ca_demurrer_hearing":
      return caMotionBriefing(anchor, court, input.serviceMethod ?? "personal", true);
    case "ca_summons_service": {
      const raw = addCalendarDaysAfter(anchor, 30);
      const rolled = rollForwardToCourtDay(raw, court);
      return [
        deadline({
          id: "responsive_pleading",
          label: "Responsive pleading deadline",
          date: rolled.date,
          rawDate: raw,
          rolled: rolled.rolled,
          citations: cite("ccp41220", "ccp12", "ccp12a"),
          explanation: [
            `30 days after service on ${formatPortfolioDate(anchor)} under CCP §412.20(a)(3) (excluding the day of service per CCP §12) lands on ${formatPortfolioDate(raw)}.`,
            rolled.rolled
              ? `That day is a Saturday, Sunday, or judicial holiday, so CCP §12a extends the deadline to ${formatPortfolioDate(rolled.date)}.`
              : "That day is a court day, so no CCP §12a extension applies.",
          ].join(" "),
        }),
      ];
    }
    case "ca_demurrer_meet_confer": {
      const raw = subtractCalendarDaysBefore(anchor, 5);
      const practical = rollBackwardToCourtDay(raw, court);
      return [
        deadline({
          id: "meet_and_confer",
          label: "Meet-and-confer deadline (statutory)",
          date: raw,
          rolled: false,
          citations: cite("ccp43041", "ccp12"),
          explanation: `CCP §430.41(a)(2) requires meet-and-confer at least 5 days before the ${formatPortfolioDate(anchor)} responsive-pleading deadline → ${formatPortfolioDate(raw)}.`,
        }),
        ...(practical.rolled
          ? [
              deadline({
                id: "meet_and_confer_practical",
                label: "Practical completion target (prior court day)",
                date: practical.date,
                rawDate: raw,
                rolled: true,
                citations: cite("ccp43041"),
                explanation: `${formatPortfolioDate(raw)} falls on a weekend or holiday. Complete the conference by ${formatPortfolioDate(practical.date)} if a weekday call is needed; a weekend conference on ${formatPortfolioDate(raw)} still satisfies the statute if actually held.`,
              }),
            ]
          : []),
      ];
    }
    case "ca_crc_service_deadline": {
      const raw = addCalendarDaysAfter(anchor, 60);
      const rolled = rollForwardToCourtDay(raw, court);
      return [
        deadline({
          id: "service_and_pos",
          label: "Service & proof-of-service filing deadline",
          date: rolled.date,
          rawDate: raw,
          rolled: rolled.rolled,
          citations: cite("crc3110", "ccp12", "ccp12a"),
          explanation: [
            `60 days from filing on ${formatPortfolioDate(anchor)} under CRC 3.110(b) lands on ${formatPortfolioDate(raw)}.`,
            rolled.rolled
              ? `CCP §12a rolls the practical deadline to ${formatPortfolioDate(rolled.date)}.`
              : "No weekend/holiday roll required.",
          ].join(" "),
        }),
      ];
    }
    case "ca_cmc_statement": {
      const statementRaw = subtractCalendarDaysBefore(anchor, 15);
      const statement = rollBackwardToCourtDay(statementRaw, court);
      const mcRaw = subtractCalendarDaysBefore(anchor, 30);
      const mc = rollBackwardToCourtDay(mcRaw, court);
      return [
        deadline({
          id: "cmc_meet_confer",
          label: "CMC meet-and-confer (CRC 3.724)",
          date: mc.date,
          rawDate: mcRaw,
          rolled: mc.rolled,
          citations: cite("crc3724", "ccp12a"),
          explanation: `30 calendar days before ${formatPortfolioDate(anchor)} → ${formatPortfolioDate(mcRaw)}${mc.rolled ? `, rolled to prior court day ${formatPortfolioDate(mc.date)}` : ""}.`,
        }),
        deadline({
          id: "cmc_statement",
          label: "Case management statement (CRC 3.725)",
          date: statement.date,
          rawDate: statementRaw,
          rolled: statement.rolled,
          citations: cite("crc3725", "ccp12a"),
          explanation: `15 calendar days before ${formatPortfolioDate(anchor)} → ${formatPortfolioDate(statementRaw)}${statement.rolled ? `, rolled to prior court day ${formatPortfolioDate(statement.date)}` : ""}.`,
        }),
      ];
    }
    case "federal_motion_hearing": {
      const motionRaw = subtractCalendarDaysBefore(anchor, 14);
      const motion = rollBackwardToCourtDay(motionRaw, court);
      const oppRaw = subtractCalendarDaysBefore(anchor, 7);
      const opp = rollBackwardToCourtDay(oppRaw, court);
      return [
        deadline({
          id: "federal_motion_notice",
          label: "Motion & notice of hearing",
          date: motion.date,
          rawDate: motionRaw,
          rolled: motion.rolled,
          citations: cite("frcp6c", "frcp6"),
          explanation: `FRCP 6(c)(1) requires service at least 14 days before ${formatPortfolioDate(anchor)}. Counting backward lands on ${formatPortfolioDate(motionRaw)}${motion.rolled ? `; FRCP 6(a)(5)/(1)(C) continues to prior court day ${formatPortfolioDate(motion.date)}` : ""}. Local rules may set longer briefing schedules.`,
        }),
        deadline({
          id: "federal_opposing_affidavit",
          label: "Opposing affidavit",
          date: opp.date,
          rawDate: oppRaw,
          rolled: opp.rolled,
          citations: cite("frcp6c", "frcp6"),
          explanation: `FRCP 6(c)(2) requires opposing affidavits at least 7 days before the hearing → ${formatPortfolioDate(opp.date)}. Check the assigned judge's standing order for briefing lengths.`,
        }),
      ];
    }
    case "federal_answer_after_service": {
      const raw = addCalendarDaysAfter(anchor, 21);
      const rolled = rollForwardToCourtDay(raw, court);
      return [
        deadline({
          id: "federal_answer",
          label: "Answer / Rule 12 response",
          date: rolled.date,
          rawDate: raw,
          rolled: rolled.rolled,
          citations: cite("frcp12", "frcp6"),
          explanation: [
            `21 days after service on ${formatPortfolioDate(anchor)} under FRCP 12(a)(1)(A), computed per FRCP 6(a), lands on ${formatPortfolioDate(raw)}.`,
            rolled.rolled
              ? `Last day is a weekend or legal holiday, so the period runs to ${formatPortfolioDate(rolled.date)}.`
              : "Last day is a business day; no extension.",
          ].join(" "),
        }),
      ];
    }
    case "federal_response_after_mail_service": {
      const periodRaw = addCalendarDaysAfter(anchor, 14);
      const period = rollForwardToCourtDay(periodRaw, court);
      const withMail = addFrcpMailDays(period.date, court);
      return [
        deadline({
          id: "federal_period_before_mail",
          label: "Prescribed period (example: 14 days) before mail add-on",
          date: period.date,
          rawDate: periodRaw,
          rolled: period.rolled,
          citations: cite("frcp6"),
          explanation: `FRCP 6(a) period after mail service on ${formatPortfolioDate(anchor)} expires ${formatPortfolioDate(period.date)}.`,
        }),
        deadline({
          id: "federal_period_with_mail",
          label: "Deadline after FRCP 6(d) +3 mail days",
          date: withMail.date,
          rawDate: withMail.afterMail,
          rolled: withMail.rolled,
          citations: cite("frcp6"),
          explanation: `FRCP 6(d) adds 3 days after the 6(a) expiration → ${formatPortfolioDate(withMail.afterMail)}${withMail.date !== withMail.afterMail ? `, then rolls to ${formatPortfolioDate(withMail.date)}` : ""}. Does not apply to CM/ECF electronic service.`,
        }),
      ];
    }
    case "edcal_lr230c_opposition":
      return federalCalendarDeadline({
        anchor,
        days: 14,
        court,
        id: "edcal_opposition",
        label: "Opposition (L.R. 230(c))",
        citations: cite("edcal230", "frcp6"),
        rule: `E.D. Cal. L.R. 230(c) requires opposition no later than 14 days after the motion is filed on ${formatPortfolioDate(anchor)}`,
      });
    case "edcal_lr230d_reply":
      return federalCalendarDeadline({
        anchor,
        days: 10,
        court,
        id: "edcal_reply",
        label: "Reply brief (L.R. 230(d))",
        citations: cite("edcal230", "frcp6"),
        rule: `E.D. Cal. L.R. 230(d) allows a reply no later than 10 days after the opposition is filed on ${formatPortfolioDate(anchor)}`,
      });
    default: {
      const _exhaustive: never = input.recipe;
      throw new Error(`Unknown recipe: ${_exhaustive}`);
    }
  }
}

function federalCalendarDeadline(opts: {
  anchor: DayKey;
  days: number;
  court: CourtKey;
  id: string;
  label: string;
  citations: RuleCitation[];
  rule: string;
}): ComputedDeadline[] {
  const raw = addCalendarDaysAfter(opts.anchor, opts.days);
  const rolled = rollForwardToCourtDay(raw, opts.court);
  return [
    deadline({
      id: opts.id,
      label: opts.label,
      date: rolled.date,
      rawDate: raw,
      rolled: rolled.rolled,
      citations: opts.citations,
      explanation: [
        `${opts.rule}, computed under FRCP 6(a) (exclude the trigger day, count every intervening day) → ${formatPortfolioDate(raw)}.`,
        rolled.rolled
          ? `That day is a Saturday, Sunday, or legal holiday, so FRCP 6(a)(1)(C) continues the period to ${formatPortfolioDate(rolled.date)}.`
          : "That day is a court day, so no FRCP 6(a) last-day extension applies.",
      ].join(" "),
    }),
  ];
}

function defaultCourtForRecipe(recipe: RecipeId, court?: CourtKey): CourtKey {
  if (court) return court;
  return RECIPE_META[recipe].forum === "federal" ? DEFAULT_FEDERAL_COURT : DEFAULT_STATE_COURT;
}

function sourcesFor(recipe: RecipeId, court: CourtKey): RuleCitation[] {
  const holidaySources = holidaySourcesForCourt(court);
  const ruleSources: RuleCitation[] = (() => {
    switch (recipe) {
      case "ca_motion_hearing":
        return cite("ccp1005", "ccp12", "ccp12a", "ccp12c");
      case "ca_demurrer_hearing":
        return cite("ccp1005", "ccp12c", "crc31320");
      case "ca_summons_service":
        return cite("ccp41220", "ccp12", "ccp12a");
      case "ca_demurrer_meet_confer":
        return cite("ccp43041");
      case "ca_crc_service_deadline":
        return cite("crc3110", "ccp12a");
      case "ca_cmc_statement":
        return cite("crc3724", "crc3725");
      case "federal_motion_hearing":
        return cite("frcp6c", "frcp6");
      case "federal_answer_after_service":
        return cite("frcp12", "frcp6");
      case "federal_response_after_mail_service":
        return cite("frcp6");
      case "edcal_lr230c_opposition":
      case "edcal_lr230d_reply":
        return cite("edcal230", "frcp6");
      default:
        return [];
    }
  })();
  const seen = new Set<string>();
  return [...ruleSources, ...holidaySources].filter((s) => {
    if (seen.has(s.id)) return false;
    seen.add(s.id);
    return true;
  });
}

/** Compute derived deadlines for a triggering event. Pure and timezone-safe (day keys). */
export function computeDeadlinesFromEvent(input: ComputeInput): ComputeResult {
  const court = defaultCourtForRecipe(input.recipe, input.court);
  const anchorDate = toDayKey(input.anchorDate);
  const forum = forumForCourt(court);
  const expectedForum = RECIPE_META[input.recipe].forum;
  if (forum !== expectedForum) {
    throw new Error(
      `Recipe ${input.recipe} is a ${expectedForum} rule set, but court ${court} is ${forum}. Pick a matching court.`,
    );
  }

  return {
    recipe: input.recipe,
    forum,
    court,
    anchorDate,
    anchorDisplay: formatPortfolioDate(anchorDate),
    deadlines: computeDeadlines(input, court),
    sources: sourcesFor(input.recipe, court),
    disclaimer: DISCLAIMER,
  };
}

/** Convenience: demurrer hearing → opposition / reply / moving papers with citations. */
export function computeDemurrerBriefing(
  hearingDate: DayKey | Date | string,
  options: { court?: CourtKey; serviceMethod?: ServiceMethod } = {},
): ComputeResult {
  return computeDeadlinesFromEvent({
    recipe: "ca_demurrer_hearing",
    anchorDate: hearingDate,
    court: options.court ?? DEFAULT_STATE_COURT,
    serviceMethod: options.serviceMethod ?? "mail_ca",
  });
}
