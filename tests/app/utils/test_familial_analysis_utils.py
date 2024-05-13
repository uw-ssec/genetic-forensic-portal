from __future__ import annotations

import genetic_forensic_portal.app.utils.familial_analysis_utils as fam_utils


def test_highlight_exact_matches_match_returns_green():
    assert fam_utils.highlight_exact_matches("Y") == fam_utils.GREEN_BACKGROUND


def test_highlight_exact_matches_no_match_returns_none():
    assert fam_utils.highlight_exact_matches("not Y") is None


def test_highlight_exact_matches_numeric_values_no_error():
    assert fam_utils.highlight_exact_matches(12) is None
