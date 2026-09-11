/**
 * Pure filing-text signals. Shared by the TypeScript OS and court:sync (Node).
 * Continuances that mention a motion are not dispositions of that motion.
 */

const DOCKET_RE =
  /\b(?:Dkt\.?|Doc(?:ument)?\.?|ECF(?:\s+No\.?)?|Docket(?:\s+No\.?)?)\s*#?\s*(\d+)\b/gi;

const MOTION_TO_DISMISS =
  /\bmotion\s+to\s+dismiss\b|\b12\s*\(\s*b\s*\)\s*\(\s*6\s*\)|\brule\s*12(?:\(b\))?(?:\(6\))?/i;

const DISPOSITION =
  /\b(?:grant(?:ed|ing)|den(?:y|ied|ying)|overrul(?:ed|ing)|sustain(?:ed|ing)|dismissed\s+with(?:out)?\s+prejudice|motion\s+is\s+(?:granted|denied))\b/i;

const AFTER_FINAL =
  /\bafter\s+the\s+final\s+order\b|\bno\s+date\s+certain\b|\bcontinued\s+(?:from|until|to)\b|\breset(?:ting)?\s+(?:the\s+)?hearing\b|\bbriefing\s+schedule\s+remains\b|\bvacat(?:ed|ing)\s+(?:the\s+)?(?:cmc|conference|deadline)/i;

const STIP_CONTINUE = /\bstipulation\b[\s\S]{0,100}\bcontinu/i;
const GRANT_STIP = /\bgrant(?:ed|ing)\b[\s\S]{0,80}\bstipulation\b/i;
const ORDER_ENTRY =
  /\border\b|clerk.?s notice|findings?\s*(and|&)\s*recommendations?/i;
const COUNSEL = /notice of appearance|appeared for|counsel of record/i;
const SETTLED = /\bsettled\b|notice of settlement|stipulation of dismissal/i;
const TRIGGER_LANGUAGE = /within \d+ days|shall file|deadline|continued.{0,40}after/i;
const ADMISSION_RE = /([^.!?\n]{0,120}(?:does not dispute|do not dispute|acknowledges|concedes)[^.!?\n]+)/gi;
const BODY_MAX = 80_000;

export function clipBody(text) {
  const value = String(text ?? "").trim();
  if (!value) return "";
  return value.length > BODY_MAX ? value.slice(0, BODY_MAX) : value;
}

export function mentionedDockets(text) {
  const ids = new Set();
  const hay = String(text ?? "");
  for (const match of hay.matchAll(DOCKET_RE)) ids.add(Number(match[1]));
  return [...ids];
}

export function isUnfiledPreview(text) {
  const hay = String(text ?? "");
  if (/\bFILED\s+[—-]|^\s*MOTION\b|\bnotice of motion\b/i.test(hay)) return false;
  return /\bmeet(?:ing)?\s+and\s+confer\b|\bpreview(?:ed)?\b|\bunfiled\b|\basked to (?:confer|dismiss)\b|\bgmail\b|\bdrafted \(unfiled\)/i.test(
    hay,
  );
}

export function isFiledMotionEntry(text) {
  const hay = String(text ?? "");
  if (isUnfiledPreview(hay)) return false;
  if (/\b(?:opposition to|reply brief)\b/i.test(hay) && !/\bnotice of motion\b/i.test(hay)) return false;
  if (/\bhearing\b/i.test(hay) && !/\bnotice of motion\b/i.test(hay) && !/\bFILED\b/.test(hay) && !/^\s*MOTION\b/i.test(hay.trim())) {
    return false;
  }
  const looksFiled =
    /^\s*MOTION\b/i.test(hay.trim()) ||
    /\bFILED\b/.test(hay) ||
    /\bnotice of motion\b/i.test(hay) ||
    /\bdefendants? (?:hereby )?move to dismiss\b/i.test(hay) ||
    /\b(?:defendant'?s?|defendants'?)\s+motion to dismiss\b/i.test(hay) ||
    /\bmotion to dismiss\b/i.test(hay);
  if (!looksFiled) return false;
  return isMotionToDismiss(hay) || /\bmotion to strike\b/i.test(hay);
}

export function isMotionToDismiss(text) {
  return MOTION_TO_DISMISS.test(String(text ?? ""));
}

export function isSchedulingNoise(text) {
  const hay = String(text ?? "");
  if (STIP_CONTINUE.test(hay) || GRANT_STIP.test(hay)) return true;
  if (AFTER_FINAL.test(hay) && !/\bgrant(?:ed|ing)\s+in\s+part\b|\bden(?:ied|ying)\s+(?:the\s+)?motion\b/i.test(hay)) {
    return true;
  }
  return false;
}

export function isMeritsDisposition(text) {
  const hay = String(text ?? "");
  if (!DISPOSITION.test(hay)) return false;
  if (isSchedulingNoise(hay)) return false;
  return true;
}

function docketPattern(docket) {
  return `(?:Dkt\\.?|Doc(?:ument)?\\.?|ECF(?:\\s+No\\.?)?|Docket(?:\\s+No\\.?)?)\\s*#?\\s*${docket}\\b`;
}

function dispositionNearDocket(text, docket) {
  if (docket == null || !Number.isInteger(Number(docket))) return false;
  const hay = String(text ?? "");
  const docketPat = docketPattern(docket);
  const verb = "(?:grant(?:ed|ing)|den(?:y|ied|ying)|overrul(?:ed|ing)|sustain(?:ed|ing)|dismissed\\s+with(?:out)?\\s+prejudice)";
  const part = "(?:grant(?:ed|ing)\\s+in\\s+part|den(?:ied|ying)\\s+in\\s+part)";
  return (
    new RegExp(`${verb}.{0,180}${docketPat}`, "i").test(hay) ||
    new RegExp(`${docketPat}.{0,180}${verb}`, "i").test(hay) ||
    new RegExp(`${part}.{0,180}${docketPat}`, "i").test(hay) ||
    new RegExp(`${docketPat}.{0,180}${part}`, "i").test(hay)
  );
}

/**
 * True when this order disposes of the identified motion (usually an MTD).
 * Dkt. 25 continuing a CMC "until after the final order on Dkt. 18" is not a disposition.
 * A clerk notice resetting the hearing on Dkt. 18 is not a disposition.
 */
export function matchesMotionDisposition(text, { motionDocket = null, entryNumber = null } = {}) {
  const hay = String(text ?? "");
  if (!isMeritsDisposition(hay)) return false;
  if (motionDocket != null && dispositionNearDocket(hay, motionDocket)) return true;
  if (!isMotionToDismiss(hay)) return false;
  const docks = mentionedDockets(hay);
  if (motionDocket != null && docks.includes(motionDocket)) return true;
  if (docks.length === 0) return true;
  if (entryNumber != null && docks.every((id) => id === entryNumber)) return true;
  return false;
}

export function issuesInText(text, issues) {
  const lower = String(text ?? "").toLowerCase();
  return (issues ?? [])
    .filter((issue) => (issue.keywords ?? []).some((keyword) => lower.includes(String(keyword).toLowerCase())))
    .map((issue) => issue.id);
}

export function triggerIdFromText(text, recipes, { matter, entryNumber } = {}) {
  const hay = String(text ?? "");
  for (const recipe of recipes ?? []) {
    if (matter != null && recipe.matter !== matter) continue;
    const motionDocket = recipe.trigger?.motionDocket ?? null;
    if (matchesMotionDisposition(hay, { motionDocket, entryNumber })) {
      return recipe.trigger?.id ?? null;
    }
  }
  return null;
}

export function classifyDocketText(text) {
  const hay = String(text ?? "");
  if (SETTLED.test(hay)) return "CASE_SETTLED";
  if (COUNSEL.test(hay)) return "COUNSEL_APPEARED";
  const isOrder = ORDER_ENTRY.test(hay);
  const noticeOfMotion = /\bnotice of motion\b/i.test(hay) || /^\s*MOTION\b/i.test(hay.trim());
  if (isOrder && !noticeOfMotion) return "ORDER_ENTERED";
  if (isFiledMotionEntry(hay)) return "MOTION_FILED";
  if (isOrder) return "ORDER_ENTERED";
  if (TRIGGER_LANGUAGE.test(hay)) return "DEADLINE_TRIGGERED";
  return "DOCKET_ENTRY_ADDED";
}

function haystack(text) {
  return String(text ?? "")
    .toLowerCase()
    .replace(/\s+/g, " ");
}

export function extractAuthorities(text, authorities) {
  const hay = haystack(text);
  const collapsed = hay.replace(/\s+v\.?\s+/g, " ");
  return (authorities ?? [])
    .filter((authority) => {
      const label = String(authority.label ?? "").toLowerCase();
      const cite = String(authority.citation ?? "")
        .toLowerCase()
        .replace(/[().]/g, " ")
        .replace(/\s+/g, " ")
        .trim();
      const idWords = String(authority.id ?? "").replaceAll("-", " ");
      if (label && hay.includes(label)) return true;
      if (idWords.length > 4 && hay.includes(idWords)) return true;
      const noV = label.replace(/\s+v\.?\s+/g, " ");
      if (noV.length > 6 && collapsed.includes(noV)) return true;
      if (cite.length > 8 && hay.includes(cite.slice(0, 24))) return true;
      return false;
    })
    .map((authority) => authority.id);
}

export function extractAdmissions(text) {
  const found = [];
  for (const match of String(text ?? "").matchAll(ADMISSION_RE)) {
    const line = match[1]?.replace(/\s+/g, " ").trim();
    if (line) found.push(line);
  }
  return [...new Set(found)];
}

export function extractFiling(text, catalog) {
  const issues = issuesInText(text, catalog?.issues);
  const authorities = extractAuthorities(text, catalog?.authorities);
  return {
    issues,
    authorities,
    arguments: issues,
    admissions: extractAdmissions(text),
  };
}

export function enrichEventRecord(event, catalog) {
  const body = typeof event.payload?.body === "string" ? event.payload.body : "";
  const text = [event.summary, body].filter(Boolean).join("\n");
  const docket =
    event.docket ??
    (Number.isInteger(Number(event.payload?.docket)) ? Number(event.payload.docket) : mentionedDockets(text)[0]);
  const extracted = event.type === "MOTION_FILED" ? extractFiling(text, catalog) : null;
  const issues = event.issues?.length ? event.issues : extracted?.issues ?? issuesInText(text, catalog?.issues);
  const payload = { ...(event.payload ?? {}) };
  if (extracted) {
    payload.authorities = extracted.authorities;
    payload.admissions = extracted.admissions;
    payload.arguments = extracted.arguments;
  }
  if (event.type === "ORDER_ENTERED") {
    const triggerId = triggerIdFromText(text, catalog?.dependencies, {
      matter: event.matter,
      entryNumber: docket ?? null,
    });
    if (triggerId) payload.triggerId = triggerId;
  }
  return { ...event, docket, issues, payload };
}
