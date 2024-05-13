# src/genetic_forensic_portal/util/status_enum.py
from enum import Enum


class AnalysisStatus(Enum):
    ANALYSIS_SUCCEEDED = "Analysis succeeded"
    ANALYSIS_IN_PROGRESS = "Analysis in progress"
    ANALYSIS_FAILED = "Analysis failed"
