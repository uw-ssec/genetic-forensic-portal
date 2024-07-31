"""Contains utility functions for displaying familial analysis results."""

from __future__ import annotations

import typing

EXACT_MATCH_COLUMN = "Includes exact match(es)"
GREEN_BACKGROUND = "background-color: green"


def highlight_exact_matches(cell: typing.Any) -> str | None:
    if str(cell) == "Y":
        return GREEN_BACKGROUND

    return None
