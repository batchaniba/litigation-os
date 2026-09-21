// Cloudflare Pages Function: same-origin /documents/:path* → doc-api Worker.
//
// Why a Function and not `_redirects`: Pages 200-proxy is same-origin only.
// https://developers.cloudflare.com/pages/configuration/redirects/
// ("Proxying will only support relative URLs on your site. You cannot proxy
// external domains.") Fetched 2026-09-21.
//
// File-based route: functions/documents/[[path]].js matches /documents and
// any depth under it. https://developers.cloudflare.com/pages/functions/routing/
//
// _routes.json (generated into internal/public/, copied to dist/) includes
// only /documents/* so static SPA assets stay on the unlimited free tier.

import { proxyDocumentsRequest } from "../../internal/scripts/lib/pages-documents-proxy.mjs";

export async function onRequest(context) {
  return proxyDocumentsRequest(context.request);
}
