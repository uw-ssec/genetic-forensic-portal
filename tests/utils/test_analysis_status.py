from genetic_forensic_portal.utils.analysis_status import AnalysisStatus


def test_ordering():
    """Test the ordering of the AnalysisStatus enum.
    Order should be
    ANALYSIS_SUCCEEDED < ANALYSIS_IN_PROGRESS < ANALYSIS_FAILED < ANALYSIS_NOT_FOUND < ANALYSIS_ERROR
    """
    # less than
    assert AnalysisStatus.ANALYSIS_SUCCEEDED < AnalysisStatus.ANALYSIS_IN_PROGRESS
    assert AnalysisStatus.ANALYSIS_IN_PROGRESS < AnalysisStatus.ANALYSIS_FAILED
    assert AnalysisStatus.ANALYSIS_FAILED < AnalysisStatus.ANALYSIS_NOT_FOUND
    assert AnalysisStatus.ANALYSIS_NOT_FOUND < AnalysisStatus.ANALYSIS_ERROR

    # greater than
    assert AnalysisStatus.ANALYSIS_ERROR > AnalysisStatus.ANALYSIS_NOT_FOUND
    assert AnalysisStatus.ANALYSIS_NOT_FOUND > AnalysisStatus.ANALYSIS_FAILED
    assert AnalysisStatus.ANALYSIS_FAILED > AnalysisStatus.ANALYSIS_IN_PROGRESS
    assert AnalysisStatus.ANALYSIS_IN_PROGRESS > AnalysisStatus.ANALYSIS_SUCCEEDED


def test_ordering_with_arbitrary_strings_uses_string_ordering():
    assert AnalysisStatus.ANALYSIS_SUCCEEDED < "ZZZZZZZ"
    assert AnalysisStatus.ANALYSIS_SUCCEEDED > "AAAAAAA"
