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


if __name__ == "__main__":
    unittest.main()
