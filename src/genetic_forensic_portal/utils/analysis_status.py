# src/genetic_forensic_portal/util/status_enum.py
from __future__ import annotations

from enum import StrEnum


class AnalysisStatus(StrEnum):
    ANALYSIS_SUCCEEDED = "Analysis succeeded"
    ANALYSIS_IN_PROGRESS = "Analysis in progress"
    ANALYSIS_FAILED = "Analysis failed"
    ANALYSIS_NOT_FOUND = "NOT FOUND"
    ANALYSIS_ERROR = "ERROR"

    def _get_ordering(self: AnalysisStatus) -> dict[str, int]:
        return {name: idx for idx, name in enumerate(self.__class__)}

    def __lt__(self: AnalysisStatus, other: str) -> bool:
        ordering = self._get_ordering()
        if other not in ordering:
            return super().__lt__(other)
        return ordering[self] < ordering[other]

    def __gt__(self: AnalysisStatus, other: str) -> bool:
        ordering = self._get_ordering()
        if other not in ordering:
            return super().__gt__(other)
        return ordering[self] > ordering[other]
