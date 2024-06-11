from __future__ import annotations

from typing import Any


class GetAnalysesResponse:
    def __init__(self, scat: Any = None, voronoi: Any = None, familial: Any = None):
        self.scat = scat
        self.voronoi = voronoi
        self.familial = familial
