#!/usr/bin/env node
/**
 * Live citation-source reachability survey. Fetches constructible URLs
 * and search endpoints from a datacenter IP with no JS rendering.
 * Writes JSON evidence to stdout / optional --out path.
 */
import fs from "node:fs";
import { setTimeout as sleep } from "node:timers/promises";

const UA =
  "citation-source-survey/2026-09-19 (+research; headless HTTPS; no JS)";

const CONTROLS = {
  C1: {
    label: "Richardson v. McKnight, 521 U.S. 399 (1997)",
    caption: "Richardson",
    year: "1997",
  },
  C2: {
    label: "Medical Marijuana, Inc. v. Horn, 604 U.S. 593 (2025)",
    caption: "Medical Marijuana",
    year: "2025",
  },
  C3: {
    label: "United States v. Paul, 239 F. App'x 353 (9th Cir. 2007)",
    caption: "Paul",
    year: "2007",
  },
  C4: {
    label: "Goddard v. Security Title Ins. & Guar. Co., 14 Cal.2d 47 (1939)",
    caption: "Goddard",
    year: "1939",
  },
  C5: {
    label: "2016 WL 4761808",
    caption: "4761808",
    year: "2016",
  },
  C6: {
    label: "Dennis v. Evans, No. 24-6244 (4th Cir. Aug. 2, 2024)",
    caption: "Dennis",
    year: "2024",
  },
  C7: {
    label: "Zellerman v. Northbridge Holdings, 999 F.4th 1 (9th Cir. 2024)",
    caption: "Zellerman",
    year: "2024",
  },
  C7b: {
    label: "In re Leman, 66 Cal.App.5th 200 (fabricated)",
    caption: "Leman",
    year: "2020",
  },
};

function classify(status, body, cf) {
  if (status === 0) return "NO";
  if (status === 403 && /cloudflare|cf-ray|just a moment/i.test(`${cf} ${body}`))
    return "CLOUDFLARE-BLOCKED";
  if (status === 403) return "NO";
  if (status >= 200 && status < 400) return "YES";
  return "NO";
}

function snippet(body, n = 240) {
  return String(body || "")
    .replace(/\s+/g, " ")
    .trim()
    .slice(0, n);
}

function hasAny(body, needles) {
  const t = String(body || "");
  return needles.some((n) => t.toLowerCase().includes(String(n).toLowerCase()));
}

async function fetchOnce(url, { method = "GET", headers = {}, body } = {}) {
  const started = Date.now();
  const ctrl = new AbortController();
  const timer = setTimeout(() => ctrl.abort(), 25000);
  try {
    const res = await fetch(url, {
      method,
      headers: { "User-Agent": UA, Accept: "*/*", ...headers },
      body,
      redirect: "follow",
      signal: ctrl.signal,
    });
    const buf = Buffer.from(await res.arrayBuffer());
    const text = buf.subarray(0, 80_000).toString("utf8");
    const cf = res.headers.get("cf-ray") || res.headers.get("server") || "";
    return {
      url,
      method,
      status: res.status,
      finalUrl: res.url,
      contentType: res.headers.get("content-type") || "",
      bytes: buf.length,
      server: cf,
      elapsedMs: Date.now() - started,
      reachable: classify(res.status, text, cf),
      snippet: snippet(text),
      bodyHead: text.slice(0, 4000),
    };
  } catch (err) {
    return {
      url,
      method,
      status: 0,
      finalUrl: url,
      contentType: "",
      bytes: 0,
      server: "",
      elapsedMs: Date.now() - started,
      reachable: "NO",
      snippet: `${err.name}: ${err.message}`,
      bodyHead: "",
      error: `${err.name}: ${err.message}`,
    };
  } finally {
    clearTimeout(timer);
  }
}

const TARGETS = [
  // CourtListener
  {
    source: "CourtListener search API (unauth)",
    control: "C1",
    url: "https://www.courtlistener.com/api/rest/v4/search/?q=%22521%20U.S.%20399%22&type=o",
  },
  {
    source: "CourtListener search API (unauth)",
    control: "C2",
    url: "https://www.courtlistener.com/api/rest/v4/search/?q=%22604%20U.S.%20593%22&type=o",
  },
  {
    source: "CourtListener search API (unauth) name",
    control: "C2",
    url: "https://www.courtlistener.com/api/rest/v4/search/?q=%22Medical%20Marijuana%22%20Horn&type=o",
  },
  {
    source: "CourtListener search API (unauth)",
    control: "C3",
    url: "https://www.courtlistener.com/api/rest/v4/search/?q=%22239%20F.%20App%27x%20353%22&type=o",
  },
  {
    source: "CourtListener search API (unauth) fappx reporter",
    control: "C3",
    url: "https://www.courtlistener.com/api/rest/v4/search/?citation=239%20F.%20App%27x%20353&type=o",
  },
  {
    source: "CourtListener search API (unauth)",
    control: "C4",
    url: "https://www.courtlistener.com/api/rest/v4/search/?q=%2214%20Cal.2d%2047%22&type=o",
  },
  {
    source: "CourtListener search API (unauth)",
    control: "C5",
    url: "https://www.courtlistener.com/api/rest/v4/search/?q=2016%20WL%204761808&type=o",
  },
  {
    source: "CourtListener search API (unauth)",
    control: "C6",
    url: "https://www.courtlistener.com/api/rest/v4/search/?q=24-6244&type=o",
  },
  {
    source: "CourtListener search API (unauth)",
    control: "C7",
    url: "https://www.courtlistener.com/api/rest/v4/search/?q=%22999%20F.4th%201%22&type=o",
  },
  {
    source: "CourtListener search API (unauth)",
    control: "C7b",
    url: "https://www.courtlistener.com/api/rest/v4/search/?q=%2266%20Cal.%20App.%205th%20200%22&type=o",
  },
  {
    source: "CourtListener citation-lookup (unauth POST)",
    control: "C1",
    url: "https://www.courtlistener.com/api/rest/v4/citation-lookup/",
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: "text=521 U.S. 399",
  },
  {
    source: "CourtListener opinion HTML",
    control: "C1",
    url: "https://www.courtlistener.com/opinion/118137/richardson-v-mcknight/",
  },
  {
    source: "CourtListener opinion HTML",
    control: "C2",
    url: "https://www.courtlistener.com/opinion/10371243/medical-marijuana-inc-v-horn/",
  },
  {
    source: "CourtListener opinions API (unauth)",
    control: "C1",
    url: "https://www.courtlistener.com/api/rest/v4/opinions/?id=111730",
  },
  {
    source: "CourtListener clusters API (unauth)",
    control: "C1",
    url: "https://www.courtlistener.com/api/rest/v4/clusters/?citation=521%20U.S.%20399",
  },

  // CAP
  {
    source: "CAP api.case.law",
    control: "C1",
    url: "https://api.case.law/v1/cases/?cite=521%20U.S.%20399",
  },
  {
    source: "CAP case.law home",
    control: "meta",
    url: "https://case.law/",
  },
  {
    source: "CAP case.law docs",
    control: "meta",
    url: "https://case.law/docs/",
  },
  {
    source: "CAP static CasesMetadata US 521",
    control: "C1",
    url: "https://static.case.law/us/521/CasesMetadata.json",
  },
  {
    source: "CAP static HTML US 521/399",
    control: "C1",
    url: "https://static.case.law/us/521/html/0399-01.html",
  },
  {
    source: "CAP static US 604 metadata",
    control: "C2",
    url: "https://static.case.law/us/604/CasesMetadata.json",
  },
  {
    source: "CAP static HTML US 604/593",
    control: "C2",
    url: "https://static.case.law/us/604/html/0593-01.html",
  },
  {
    source: "CAP static reporters index",
    control: "meta",
    url: "https://static.case.law/ReportersMetadata.json",
  },
  {
    source: "CAP static f-appx?",
    control: "C3",
    url: "https://static.case.law/f-appx/239/CasesMetadata.json",
  },
  {
    source: "CAP static fed-appx?",
    control: "C3",
    url: "https://static.case.law/fed-appx/239/CasesMetadata.json",
  },
  {
    source: "CAP static f-appx HTML",
    control: "C3",
    url: "https://static.case.law/f-appx/239/html/0353-01.html",
  },
  {
    source: "CAP static cal-2d metadata",
    control: "C4",
    url: "https://static.case.law/cal-2d/14/CasesMetadata.json",
  },
  {
    source: "CAP static HTML cal-2d 14/47",
    control: "C4",
    url: "https://static.case.law/cal-2d/14/html/0047-01.html",
  },
  {
    source: "CAP static f4th 999",
    control: "C7",
    url: "https://static.case.law/f4th/999/CasesMetadata.json",
  },
  {
    source: "CAP static cal-app-5th 66",
    control: "C7b",
    url: "https://static.case.law/cal-app-5th/66/CasesMetadata.json",
  },

  // Google Scholar
  {
    source: "Google Scholar cases",
    control: "C1",
    url: "https://scholar.google.com/scholar_case?case=16084731491774391602",
  },
  {
    source: "Google Scholar search",
    control: "C1",
    url: "https://scholar.google.com/scholar?q=521+U.S.+399+Richardson+McKnight&as_sdt=4%2C33",
  },

  // Justia
  {
    source: "Justia SCOTUS constructible",
    control: "C1",
    url: "https://supreme.justia.com/cases/federal/us/521/399/",
  },
  {
    source: "Justia SCOTUS 604/593",
    control: "C2",
    url: "https://supreme.justia.com/cases/federal/us/604/593/",
  },
  {
    source: "Justia SCOTUS 604 docket slug",
    control: "C2",
    url: "https://supreme.justia.com/cases/federal/us/604/23-365/",
  },
  {
    source: "Justia Cal constructible",
    control: "C4",
    url: "https://law.justia.com/cases/california/supreme-court/2d/14/47.html",
  },
  {
    source: "Justia CA4 docket",
    control: "C6",
    url: "https://law.justia.com/cases/federal/appellate-courts/ca4/24-6244/24-6244-2024-08-02.html",
  },
  {
    source: "Justia search",
    control: "C3",
    url: "https://law.justia.com/search?query=239+F.+Appx+353",
  },

  // FindLaw
  {
    source: "FindLaw SCOTUS",
    control: "C1",
    url: "https://caselaw.findlaw.com/court/us-supreme-court/521/399.html",
  },
  {
    source: "FindLaw SCOTUS alt",
    control: "C1",
    url: "https://caselaw.findlaw.com/us-supreme-court/96-318.html",
  },
  {
    source: "FindLaw search",
    control: "C1",
    url: "https://caselaw.findlaw.com/summary/search/?query=richardson+v+mcknight+521",
  },

  // Casetext / vLex / Fastcase / CaseMine / OpenJurist
  {
    source: "Casetext",
    control: "C1",
    url: "https://casetext.com/case/richardson-v-mcknight",
  },
  {
    source: "Casetext search",
    control: "C1",
    url: "https://casetext.com/search?q=521%20U.S.%20399",
  },
  {
    source: "vLex case-law",
    control: "C1",
    url: "https://case-law.vlex.com/vid/richardson-v-mcknight-885568545",
  },
  {
    source: "vLex search",
    control: "C1",
    url: "https://case-law.vlex.com/search?q=521+U.S.+399",
  },
  {
    source: "Fastcase",
    control: "C1",
    url: "https://fc7.fastcase.com/",
  },
  {
    source: "Fastcase web",
    control: "C1",
    url: "https://web.fastcase.com/",
  },
  {
    source: "CaseMine",
    control: "C1",
    url: "https://www.casemine.com/judgement/us/5914b5c2add7b0493475f8c2",
  },
  {
    source: "CaseMine search",
    control: "C1",
    url: "https://www.casemine.com/search/us?q=Richardson+v+McKnight+521",
  },
  {
    source: "OpenJurist constructible",
    control: "C1",
    url: "https://openjurist.org/521/us/399",
  },
  {
    source: "OpenJurist C4",
    control: "C4",
    url: "https://openjurist.org/14/cal2d/47",
  },
  {
    source: "OpenJurist C2",
    control: "C2",
    url: "https://openjurist.org/604/us/593",
  },

  // Cornell LII
  {
    source: "Cornell LII constructible",
    control: "C1",
    url: "https://www.law.cornell.edu/supct/html/96-318.ZO.html",
  },
  {
    source: "Cornell LII text",
    control: "C1",
    url: "https://www.law.cornell.edu/supremecourt/text/521/399",
  },
  {
    source: "Cornell LII C2",
    control: "C2",
    url: "https://www.law.cornell.edu/supremecourt/text/23-365",
  },

  // govinfo
  {
    source: "govinfo USREPORTS 521/399",
    control: "C1",
    url: "https://www.govinfo.gov/content/pkg/USREPORTS-521/pdf/USREPORTS-521-399.pdf",
  },
  {
    source: "govinfo USCOURTS API collections",
    control: "meta",
    url: "https://api.govinfo.gov/collections?offset=0&pageSize=20",
  },
  {
    source: "govinfo USCOURTS collection",
    control: "meta",
    url: "https://www.govinfo.gov/app/collection/uscourts",
  },
  {
    source: "govinfo search C1",
    control: "C1",
    url: "https://www.govinfo.gov/app/search/%7B%22query%22%3A%22521%20U.S.%20399%20Richardson%22%2C%22offset%22%3A0%7D",
  },

  // Official courts
  {
    source: "supremecourt.gov slip C2",
    control: "C2",
    url: "https://www.supremecourt.gov/opinions/24pdf/23-365_6k47.pdf",
  },
  {
    source: "supremecourt.gov prelim C2",
    control: "C2",
    url: "https://www.supremecourt.gov/opinions/24pdf/604us2r23_3e04.pdf",
  },
  {
    source: "supremecourt.gov bound 521",
    control: "C1",
    url: "https://www.supremecourt.gov/opinions/boundvolumes/521bv.pdf",
  },
  {
    source: "supremecourt.gov slip list OT24",
    control: "C2",
    url: "https://www.supremecourt.gov/opinions/slipopinion/24",
  },
  {
    source: "CA9 opinions index",
    control: "meta",
    url: "https://cdn.ca9.uscourts.gov/datastore/opinions/",
  },
  {
    source: "CA9 memoranda index",
    control: "meta",
    url: "https://cdn.ca9.uscourts.gov/datastore/memoranda/",
  },
  {
    source: "CA9 published search page",
    control: "meta",
    url: "https://www.ca9.uscourts.gov/opinions/",
  },
  {
    source: "courts.ca.gov opinions",
    control: "meta",
    url: "https://www.courts.ca.gov/opinions.htm",
  },
  {
    source: "courts.ca.gov published search",
    control: "C4",
    url: "https://www.courts.ca.gov/opinions-slip.htm",
  },

  // Other
  {
    source: "Oyez C2",
    control: "C2",
    url: "https://www.oyez.org/cases/2024/23-365",
  },
  {
    source: "Library of Congress Congress.gov? skip",
    control: "meta",
    url: "https://tile.loc.gov/storage-services/service/ll/usrep/usrep521/usrep521399/usrep521399.pdf",
  },
  {
    source: "Google Scholar How Cited page shape",
    control: "C1",
    url: "https://scholar.google.com/scholar?q=related:richardson+mcknight+521&as_sdt=2006",
  },
  {
    source: "FindLaw C2",
    control: "C2",
    url: "https://caselaw.findlaw.com/court/us-supreme-court/23-365.html",
  },
  {
    source: "Justia F.Appx guess",
    control: "C3",
    url: "https://law.justia.com/cases/federal/appellate-courts/ca9/239-f-appx-353/",
  },
  {
    source: "OpenJurist F.Appx",
    control: "C3",
    url: "https://openjurist.org/239/f-appx/353",
  },
  {
    source: "CourtListener search WL known real",
    control: "C5",
    url: "https://www.courtlistener.com/api/rest/v4/search/?q=%22WL%204761808%22",
  },
  {
    source: "CourtListener docket search 24-6244",
    control: "C6",
    url: "https://www.courtlistener.com/api/rest/v4/search/?q=24-6244&type=d",
  },
];

async function main() {
  const outPath = process.argv.includes("--out")
    ? process.argv[process.argv.indexOf("--out") + 1]
    : null;
  const results = [];
  for (const t of TARGETS) {
    const r = await fetchOnce(t.url, {
      method: t.method,
      headers: t.headers,
      body: t.body,
    });
    const body = r.bodyHead || "";
    results.push({
      source: t.source,
      control: t.control,
      controlLabel: CONTROLS[t.control]?.label || t.control,
      ...r,
      captionHit: t.control !== "meta" && CONTROLS[t.control]
        ? hasAny(body, [
            CONTROLS[t.control].caption,
            CONTROLS[t.control].year,
          ])
        : null,
    });
    process.stderr.write(
      `${String(r.status).padStart(3)} ${r.reachable.padEnd(20)} ${t.control} ${t.source}\n`,
    );
    await sleep(150);
  }
  const payload = {
    generated: new Date().toISOString(),
    ua: UA,
    controls: CONTROLS,
    results,
  };
  const json = JSON.stringify(payload, null, 2);
  if (outPath) fs.writeFileSync(outPath, json);
  else process.stdout.write(json);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
