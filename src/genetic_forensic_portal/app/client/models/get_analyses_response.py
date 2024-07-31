from __future__ import annotations

from typing import Any


class GetAnalysesResponse:
    """The model for the response from the genetic forensic portal API when retrieving all analyses for a sample.

    Attributes:
    - `scat`: The SCAT analysis for the sample.
    - `voronoi`: The Voronoi analysis for the sample.
    - `familial`: The familial analysis for the sample.
    """

    def __init__(self, scat: Any = None, voronoi: Any = None, familial: Any = None):
        self.scat = scat
        self.voronoi = voronoi
        self.familial = familial
