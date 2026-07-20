// Prefixes a root-absolute public asset path (e.g. "/logo-dark.png") with
// Vite's configured base path, so links and images resolve correctly both
// on Vercel (served from "/") and GitHub Pages (served from a project
// subpath, e.g. "/interactive-litigation-portfolio/").
export const withBase = (path) => import.meta.env.BASE_URL.replace(/\/$/, "") + path;
