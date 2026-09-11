#!/usr/bin/env python3
"""Unit tests for citation-key matching, overlay rules, and web-search filters."""
from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from lib.citation_keys import (  # noqa: E402
    case_name_key,
    names_overlap,
    normalize_authority_key,
    reporter_pin_key,
)


def _load(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / filename)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


overlay = _load("overlay_citation_lookups", "overlay-citation-lookups.py")
lookup = _load("lookup_citations", "lookup-citations.py")


class CitationKeysTest(unittest.TestCase):
    def test_ocr_spacing_shares_a_pin(self):
        a = "Florer v. Congregation Pidyon Shevuyim, N.A, 639 F. 3d 916"
        b = "Florer v. Congregation Pidyon Shevuyim, N.A, 639 F.3d 916"
        self.assertEqual(reporter_pin_key(a), reporter_pin_key(b))
        self.assertEqual(reporter_pin_key(a), "639 f3d 916")
        self.assertEqual(normalize_authority_key(a), normalize_authority_key(b))

    def test_cal_app_spacing(self):
        a = "Quiroz v. Seventh Ave. Ctr, 140 Cal.App. 4th 1256"
        b = "Quiroz v. Seventh Ave. Ctr, 140 Cal. App. 4th 1256"
        self.assertEqual(reporter_pin_key(a), reporter_pin_key(b))
        self.assertEqual(reporter_pin_key(a), "140 calapp4th 1256")

    def test_dismiss_see_prefix(self):
        cite = "Dismiss. See Paulsen v. CNF Inc, 559 F. 3d 1061"
        self.assertTrue(case_name_key(cite).startswith("paulsen"))
        self.assertEqual(reporter_pin_key(cite), "559 f3d 1061")

    def test_westlaw_pin(self):
        self.assertEqual(
            reporter_pin_key("Ruelaz v. Leprino Foods Co, 2025 WL 25549"),
            "wl 25549",
        )

    def test_names_overlap_ocr_vs_table_page(self):
        self.assertTrue(
            names_overlap(
                "Smith v. Adepa, 81 F. 4th 994",
                "Paulette Smith v. Edward Agdeppa, 81 F.4th 994",
            )
        )
        self.assertFalse(
            names_overlap(
                "Collins v. Moore, 81 F.3d 167",
                "United States v. Unrelated, 81 F.3d 167",
            )
        )


class OverlayRulesTest(unittest.TestCase):
    def test_found_unverified_becomes_verified(self):
        lookup_row = {
            "query": "Albright v. Oliver, 510 U.S. 266 (1994)",
            "consensus": "FOUND",
            "matched_name": "Albright v. Oliver",
            "reporter_pin": "510 U.S. 266",
            "sources": [{"source": "courtlistener", "found": True, "url": "https://www.courtlistener.com/x"}],
        }
        row = overlay.overlay_row(lookup_row, {}, {}, {})
        self.assertIsNotNone(row)
        self.assertEqual(row["status"], "VERIFIED")
        self.assertIn("Existence only", row["notes"])
        self.assertIn("Characterization still needs opinion text", row["notes"])

    def test_skips_prior_mischaracterized(self):
        lookup_row = {
            "query": "People v. Rizo, 22 Cal. 4th 681 (2000)",
            "consensus": "FOUND",
            "matched_name": "People v. Rizo",
            "reporter_pin": "22 Cal. 4th 681",
            "sources": [],
        }
        key = normalize_authority_key(lookup_row["query"])
        row = overlay.overlay_row(lookup_row, {key: "MISCHARACTERIZED"}, {}, {})
        self.assertIsNone(row)

    def test_ocr_caption_mismatch_is_verified(self):
        lookup_row = {
            "query": "Smith v. Adepa, 81 F. 4th 994",
            "consensus": "CAPTION_MISMATCH",
            "matched_name": "Paulette Smith v. Edward Agdeppa",
            "reporter_pin": "81 F.4th 994",
            "sources": [{"source": "courtlistener", "found": True, "url": "https://www.courtlistener.com/x"}],
        }
        row = overlay.overlay_row(lookup_row, {}, {}, {})
        self.assertIsNotNone(row)
        self.assertEqual(row["status"], "VERIFIED")
        self.assertIn("official caption", row["notes"])

    def test_wrong_case_at_pin_is_not_overlaid(self):
        lookup_row = {
            "query": "Collins v. Moore, 81 F.3d 167",
            "consensus": "CAPTION_MISMATCH",
            "matched_name": "United States v. Unrelated Table Page",
            "reporter_pin": "81 F.3d 167",
            "sources": [{"source": "courtlistener", "found": True, "url": "https://www.courtlistener.com/x"}],
        }
        self.assertIsNone(overlay.overlay_row(lookup_row, {}, {}, {}))

    def test_web_only_partial_is_not_overlaid(self):
        lookup_row = {
            "query": "Some Case, 1 U.S. 1",
            "consensus": "PARTIAL",
            "matched_name": "Some Case",
            "reporter_pin": "1 U.S. 1",
            "sources": [
                {"source": "web_search", "found": True, "url": "https://www.justia.com/x"},
            ],
        }
        self.assertTrue(overlay.web_only_partial(lookup_row))
        self.assertIsNone(overlay.overlay_row(lookup_row, {}, {}, {}))


class WebFilterTest(unittest.TestCase):
    def test_allowlist_accepts_courtlistener(self):
        self.assertTrue(lookup._host_allowed("https://www.courtlistener.com/opinion/1/x/"))
        self.assertTrue(lookup._host_allowed("https://cdn.ca9.uscourts.gov/datastore/opinions/x.pdf"))
        self.assertFalse(lookup._host_allowed("https://www.ssa.gov/form-521"))
        self.assertFalse(lookup._host_allowed("https://richardsonsports.com/"))

    def test_bing_dest_decode(self):
        # "https://www.courtlistener.com/x" as bing u=a1 base64
        raw = "aHR0cHM6Ly93d3cuY291cnRsaXN0ZW5lci5jb20veA=="
        href = f"https://www.bing.com/ck/a?!&u=a1{raw}&ntb=1"
        self.assertEqual(lookup._decode_bing_dest(href), "https://www.courtlistener.com/x")

    def test_web_alone_is_partial_not_found(self):
        result = lookup.LookupResult(
            query="Richardson v. McKnight, 521 U.S. 399",
            case_name_guess="Richardson v. McKnight",
            reporter_pin="521 U.S. 399",
            wl_pin=None,
        )
        result.sources.append(
            lookup.SourceHit(source="courtlistener", found=False, url=""),
        )
        result.sources.append(
            lookup.SourceHit(source="case.law_static", found=False, url=""),
        )
        result.sources.append(
            lookup.SourceHit(
                source="web_search",
                found=True,
                url="https://www.courtlistener.com/opinion/1/richardson-v-mcknight/",
                case_name="Richardson v. McKnight",
                citations=["521 U.S. 399"],
            ),
        )
        self.assertEqual(lookup.consensus_for(result), "PARTIAL")


if __name__ == "__main__":
    unittest.main()
