// Public Worker origin that serves /documents/:path* from R2.
// Vercel rewrites here; Cloudflare Pages cannot (Pages `_redirects` 200
// proxy is same-origin only — see developers.cloudflare.com/pages/configuration/redirects/).
// Pages uses functions/documents/[[path]].js instead. Keep this module tiny
// so the Pages Function can import it without pulling git/R2 helpers.

export const DOCUMENTS_WORKER_ORIGIN =
  "https://litigation-doc-api.ss8sxswwkt.workers.dev";

export const DOCUMENTS_ORIGIN = `${DOCUMENTS_WORKER_ORIGIN}/documents`;

/** @deprecated alias — Pages no longer serves the library. */
export const PAGES_DOCUMENTS_ORIGIN = DOCUMENTS_ORIGIN;
