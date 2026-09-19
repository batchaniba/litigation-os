#!/usr/bin/env python3
"""Unit tests for CourtListener citation-lookup status mapping (no network)."""
from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("lookup_citations", SCRIPTS / "lookup-citations.py")
lookup = importlib.util.module_from_spec(spec)
sys.modules["lookup_citations"] = lookup
spec.loader.exec_module(lookup)


class CitationLookupHitTest(unittest.TestCase):
    def test_200_found(self):
        rows = [
            {
                "citation": "521 U.S. 399",
                "normalized_citations": ["521 U.S. 399"],
                "status": 200,
                "clusters": [
                    {
                        "case_name": "Richardson v. McKnight",
                        "absolute_url": "/opinion/118142/richardson-v-mcknight/",
                        "citations": ["521 U.S. 399"],
                    }
                ],
            }
        ]
        hit = lookup.citation_lookup_hit(
            rows,
            "Richardson v. McKnight, 521 U.S. 399 (1997)",
            "Richardson v. McKnight",
            http_status=200,
            url=lookup.CL_CITATION_LOOKUP,
        )
        self.assertTrue(hit.found)
        self.assertEqual(hit.case_name, "Richardson v. McKnight")
        self.assertIn("status=200", hit.notes)

    def test_404_not_found(self):
        rows = [{"citation": "66 Cal. App. 5th 200", "status": 404, "clusters": [], "error_message": "no cluster"}]
        hit = lookup.citation_lookup_hit(
            rows,
            "In re Leman, 66 Cal.App.5th 200",
            "In re Leman",
            http_status=200,
            url=lookup.CL_CITATION_LOOKUP,
        )
        self.assertFalse(hit.found)
        self.assertIn("no cluster", hit.notes)

    def test_400_bad_reporter(self):
        rows = [{"citation": "1 Fake. Rptr. 1", "status": 400, "clusters": [], "error_message": "unknown reporter"}]
        hit = lookup.citation_lookup_hit(
            rows, "Nope, 1 Fake. Rptr. 1", "Nope", http_status=200, url=lookup.CL_CITATION_LOOKUP
        )
        self.assertFalse(hit.found)
        self.assertIn("unknown reporter", hit.notes)

    def test_300_ambiguous_picks_name_overlap(self):
        rows = [
            {
                "citation": "384 F.3d 1184",
                "status": 300,
                "clusters": [
                    {"case_name": "Unrelated v. Other", "absolute_url": "/opinion/1/x/", "citations": ["384 F.3d 1184"]},
                    {
                        "case_name": "Swift v. California",
                        "absolute_url": "/opinion/2/swift/",
                        "citations": ["384 F.3d 1184"],
                    },
                ],
            }
        ]
        hit = lookup.citation_lookup_hit(
            rows,
            "Swift v. California, 384 F.3d 1184",
            "Swift v. California",
            http_status=200,
            url=lookup.CL_CITATION_LOOKUP,
        )
        self.assertTrue(hit.found)
        self.assertEqual(hit.case_name, "Swift v. California")
        self.assertIn("ambiguous", hit.notes)

    def test_token_prefers_COURTLISTENER_TOKEN(self):
        lookup._citation_lookup_disabled = False
        self.assertEqual(lookup.CL_TOKEN_ENV, "COURTLISTENER_TOKEN")
        self.assertEqual(lookup.CL_TOKEN_ENV_ALT, "COURTLISTENER_API_TOKEN")


class ExtraProbeHelpersTest(unittest.TestCase):
    def test_ca9_strips_no_prefix_and_companion(self):
        self.assertEqual(lookup.ca9_strip_docket("No. 13-35356"), "13-35356")
        self.assertEqual(lookup.ca9_strip_docket("No. 13-35356, 13-35355"), "13-35356")
        self.assertEqual(lookup.ca9_strip_docket("24-6244"), "24-6244")

    def test_ca9_candidates_opinions_then_memoranda(self):
        pairs = lookup.ca9_pdf_candidates("No. 12-35294", "2015", "11", "23")
        self.assertEqual(
            [k for k, _ in pairs],
            ["opinions", "memoranda"],
        )
        self.assertTrue(pairs[0][1].endswith("/datastore/opinions/2015/11/23/12-35294.pdf"))
        self.assertTrue(pairs[1][1].endswith("/datastore/memoranda/2015/11/23/12-35294.pdf"))
        self.assertNotIn("No.", pairs[0][1])

    def test_govinfo_skips_unbound_us_and_builds_uscourts_query(self):
        self.assertTrue(lookup.is_unbound_us("Medical Marijuana v. Horn, 604 U.S. ___"))
        self.assertIsNone(lookup.govinfo_query_for("Medical Marijuana v. Horn, 604 U.S. ___"))
        self.assertEqual(
            lookup.govinfo_query_for("ASARCO, LLC v. Union Pac. R.R. Co., 765 F.3d 999"),
            'collection:(USCOURTS) "765 F.3d 999"',
        )
        payload = lookup.govinfo_search_payload('collection:(USCOURTS) "765 F.3d 999"')
        self.assertEqual(payload["offsetMark"], "*")
        self.assertTrue(payload["historical"])

    def test_govinfo_name_match_rejects_first_unrelated_hit(self):
        rows = [
            {"collectionCode": "USCOURTS", "title": "Smith v. Jones", "packageId": "USCOURTS-waed-1"},
            {
                "collectionCode": "USCOURTS",
                "title": "Richardson v. McKnight",
                "packageId": "USCOURTS-scotus-96-318",
                "download": {"pdfLink": "https://example.test/richardson.pdf"},
            },
        ]
        cite = "Richardson v. McKnight, 521 U.S. 399"
        hit = lookup.govinfo_pick_named_hit(rows, cite)
        self.assertIsNotNone(hit)
        self.assertEqual(hit["packageId"], "USCOURTS-scotus-96-318")
        self.assertIsNone(lookup.govinfo_pick_named_hit(rows[:1], cite))

    def test_probe_govinfo_unbound_does_not_call_network(self):
        hit = lookup.probe_govinfo("Medical Marijuana v. Horn, 604 U.S. ___ (2025)")
        self.assertFalse(hit.found)
        self.assertIn("supremecourt.gov", hit.notes)

    def test_probe_govinfo_get_shaped_message_is_not_found(self):
        def fake_post(url, payload, headers=None):
            return 200, "application/json", b'{"message": "Use POST"}'

        orig = lookup.http_post_json
        lookup.http_post_json = fake_post
        try:
            hit = lookup.probe_govinfo("ASARCO, LLC v. Union Pac. R.R. Co., 765 F.3d 999")
        finally:
            lookup.http_post_json = orig
        self.assertFalse(hit.found)
        self.assertIn("GET-shaped", hit.notes)

    def test_extra_probes_do_not_vote_in_consensus(self):
        result = lookup.LookupResult(
            query="ASARCO, LLC v. Union Pac. R.R. Co., 765 F.3d 999",
            case_name_guess="ASARCO, LLC v. Union Pac. R.R. Co.",
            reporter_pin="765 F.3d 999",
            wl_pin=None,
            sources=[
                lookup.SourceHit(source="govinfo", found=True, case_name="ASARCO, LLC v. Union Pacific"),
                lookup.SourceHit(source="ca9_cdn", found=True, case_name="ASARCO, LLC v. Union Pacific"),
            ],
        )
        lookup.consensus_for(result)
        # Extra probes must not produce FOUND *or* a finished negative.
        self.assertEqual(result.consensus, "UNRESOLVED")


class ConsensusAndReporterMapTest(unittest.TestCase):
    def test_parses_cal_2d_and_f_appx(self):
        goddard = lookup.parse_reporter("Goddard, 14 Cal.2d 47")
        self.assertIsNotNone(goddard)
        self.assertEqual(goddard["slug"], "cal-2d")
        self.assertEqual(goddard["pin"], "14 Cal. 2d 47")
        paul = lookup.parse_reporter("United States v. Paul, 239 F. App'x 353")
        self.assertIsNotNone(paul)
        self.assertEqual(paul["slug"], "f-appx")
        self.assertEqual(paul["pin"], "239 F. App'x 353")

    def test_pin_404_without_skipped_live_sources_is_not_found(self):
        result = lookup.LookupResult(
            query="In re Leman, 66 Cal.App.5th 200",
            case_name_guess="In re Leman",
            reporter_pin="66 Cal. App. 5th 200",
            wl_pin=None,
            sources=[
                lookup.SourceHit(
                    source="courtlistener_citation",
                    found=False,
                    notes="Citation-lookup 404 for 66 Cal. App. 5th 200",
                ),
                lookup.SourceHit(
                    source="case.law_static",
                    found=False,
                    notes="No case with first_page=200 in CAP volume cal-app-5th/66",
                ),
                lookup.SourceHit(
                    source="courtlistener",
                    found=False,
                    notes="No cite/name match in queries",
                ),
                lookup.SourceHit(
                    source="cl_bulk_offline",
                    found=False,
                    notes="skipped: bulk SQLite index not built",
                ),
            ],
        )
        lookup.consensus_for(result)
        self.assertEqual(result.consensus, "NOT_FOUND")

    def test_skipped_citation_lookup_is_unresolved(self):
        result = lookup.LookupResult(
            query="In re Leman, 66 Cal.App.5th 200",
            case_name_guess="In re Leman",
            reporter_pin="66 Cal. App. 5th 200",
            wl_pin=None,
            sources=[
                lookup.SourceHit(
                    source="courtlistener_citation",
                    found=False,
                    notes="skipped (citation-lookup disabled or no COURTLISTENER_TOKEN)",
                ),
                lookup.SourceHit(
                    source="case.law_static",
                    found=False,
                    notes="Volume metadata unavailable for cal-app-5th/66",
                ),
            ],
        )
        lookup.consensus_for(result)
        self.assertEqual(result.consensus, "UNRESOLVED")

    def test_name_only_hits_cap_at_partial(self):
        result = lookup.LookupResult(
            query="Some Invented Caption",
            case_name_guess="Some Invented Caption",
            reporter_pin=None,
            wl_pin=None,
            sources=[
                lookup.SourceHit(
                    source="courtlistener",
                    found=True,
                    case_name="Some Invented Caption",
                    name_only=True,
                    notes="NAME-ONLY (no pin behind this hit)",
                ),
            ],
        )
        lookup.consensus_for(result)
        self.assertEqual(result.consensus, "PARTIAL")

    def test_bulk_without_db_is_skipped_not_not_found(self):
        lookup._bulk_db_ok = None
        hit = lookup.probe_bulk_offline("Richardson v. McKnight, 521 U.S. 399")
        self.assertFalse(hit.found)
        self.assertIn("skipped", hit.notes.lower())
        self.assertNotIn("NOT_FOUND", hit.notes)


if __name__ == "__main__":
    unittest.main()
