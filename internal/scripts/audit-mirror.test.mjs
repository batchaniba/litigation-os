import { describe, expect, it } from "vitest";
import { diffMirror } from "./audit-mirror.mjs";

const m = (number, extra = {}) => ({ number, caption: `M${number}`, lifecycle: "active", ...extra });
const c = (matter_number, date, title, status = "open") => ({ matter_number, date, title, status });
const d = (sha256, path) => ({ sha256, path });

describe("diffMirror", () => {
  it("is ok when D1 equals the projection", () => {
    const p = { matters: [m(1)], clocks: [c(1, "2026-10-13", "Opp")], documents: [d("a", "/x.pdf")] };
    expect(diffMirror(p, p).ok).toBe(true);
  });

  it("reports every class of drift", () => {
    const expected = {
      matters: [m(28, { status_label: "reply Oct. 13" }), m(42)],
      clocks: [c(29, "2026-10-13", "Opposition due"), c(26, "2026-10-07", "HEARING", "vacated")],
      documents: [d("pub", "/documents/matter-28/filed.pdf")],
    };
    const live = {
      matters: [m(28, { status_label: "answer Sep. 21" })],
      clocks: [c(26, "2026-10-07", "HEARING", "open"), c(33, "2026-11-05", "old CMS")],
      documents: [d("pub", "/documents/matter-28/filed.pdf"), d("priv", "/documents/matter-12/CC Auth.pdf"), d("orphan", "/x")],
    };
    const r = diffMirror(expected, live, new Set(["pub", "priv"]));
    expect(r.ok).toBe(false);
    expect(r.drift.matters.missing_in_d1).toEqual([42]);
    expect(r.drift.matters.field_mismatches).toEqual([
      { matter: 28, field: "status_label", repo: "reply Oct. 13", d1: "answer Sep. 21" },
    ]);
    expect(r.drift.clocks.missing_in_d1.map((x) => x.title)).toEqual(["Opposition due"]);
    expect(r.drift.clocks.extra_in_d1.map((x) => x.title)).toEqual(["old CMS"]);
    expect(r.drift.clocks.status_mismatches).toEqual([
      { matter: 26, date: "2026-10-07", title: "HEARING", repo: "vacated", d1: "open" },
    ]);
    expect(r.drift.documents.d1_only_not_public.map((x) => x.sha256)).toEqual(["priv"]);
    expect(r.drift.documents.d1_only_unknown_to_repo.map((x) => x.sha256)).toEqual(["orphan"]);
  });

  it("matches D1 rows lacking a matter number or an R2 object instead of calling them missing", () => {
    const expected = { matters: [], clocks: [], documents: [d("form", "/documents/_form-library/x.pdf"), d("hope", "/documents/matter-05/h.pdf"), d("gone", "/y.pdf")] };
    const live = {
      matters: [],
      clocks: [],
      documents: [],
      d1Documents: [
        { sha256: "form", path: "/documents/_form-library/x.pdf", matter_number: null },
        { sha256: "hope", path: "/documents/matter-05/h.pdf", matter_number: 5 },
      ],
      r2Missing: new Set(["hope"]),
    };
    const r = diffMirror(expected, live);
    expect(r.drift.documents.missing_in_d1.map((x) => x.sha256)).toEqual(["gone"]);
    expect(r.drift.documents.in_d1_no_r2_object.map((x) => x.sha256)).toEqual(["hope"]);
    expect(r.info.documents_in_d1_no_matter_number).toBe(1);
    expect(r.drift.documents.d1_only).toEqual([]);
  });
});
