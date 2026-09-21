// Reverse-proxy /documents/* from the Pages host to the existing doc-api
// Worker. Pages `_redirects` cannot 200-proxy an external domain
// (https://developers.cloudflare.com/pages/configuration/redirects/ — fetched
// 2026-09-21). A Pages Function can fetch() that origin and return the body,
// which is the analogue of vercel.json's /documents/:path* rewrite.

import { DOCUMENTS_WORKER_ORIGIN } from "./documents-origin.mjs";

/**
 * Map a request URL on the Pages host to the Worker URL, preserving path
 * encoding and the query string (`/documents/matter-26/12%28b%29.pdf?x=1`).
 * @param {string} requestUrl
 * @param {string} [origin]
 */
export function documentsProxyUrl(requestUrl, origin = DOCUMENTS_WORKER_ORIGIN) {
  const incoming = new URL(requestUrl);
  if (!incoming.pathname.startsWith("/documents")) {
    throw new Error(`documents proxy expected a /documents path, got ${incoming.pathname}`);
  }
  return new URL(`${incoming.pathname}${incoming.search}`, origin);
}

/**
 * @param {Request} request
 * @param {typeof fetch} [fetchImpl]
 * @param {string} [origin]
 * @returns {Promise<Response>}
 */
export async function proxyDocumentsRequest(
  request,
  fetchImpl = fetch,
  origin = DOCUMENTS_WORKER_ORIGIN,
) {
  const target = documentsProxyUrl(request.url, origin);
  return fetchImpl(new Request(target, request));
}
