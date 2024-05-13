from __future__ import annotations

import logging
from pathlib import Path

import pandas as pd

from genetic_forensic_portal.utils.analysis_status import AnalysisStatus

logger = logging.getLogger(__name__)


MISSING_DATA_ERROR = "data is required"
MISSING_UUID_ERROR = "uuid is required"
FAMILIAL_TSV_ERROR = (
    "Error reading familial matching results. Please contact system administrator."
)

SAMPLE_UUID = "this-is-a-uuid"
NO_METADATA_UUID = "this-is-a-differentuuid"
NOT_FOUND_UUID = "not-found-uuid"
NOT_AUTHORIZED_UUID = "not-authorized-uuid"
IN_PROGRESS_UUID = "in-progress-uuid"
ANALYSIS_FAILED_UUID = "failed-uuid"
FAMILIAL_FILE_PARSE_ERROR_UUID = "familial-parse-error-uuid"

UUID_LIST = [
    SAMPLE_UUID,
    NO_METADATA_UUID,
    NOT_FOUND_UUID,
    NOT_AUTHORIZED_UUID,
    IN_PROGRESS_UUID,
    ANALYSIS_FAILED_UUID,
    FAMILIAL_FILE_PARSE_ERROR_UUID,
]

SAMPLE_PATH = Path(__file__).parents[2] / "resources"  # equivalent to ../../resources

SAMPLE_IMAGE_PATH = SAMPLE_PATH / "sample_images"
SCAT_SAMPLE_IMAGE = str(SAMPLE_IMAGE_PATH / "tan001_scat.png")
SCAT_SAMPLE_IMAGE_2 = str(SAMPLE_IMAGE_PATH / "tan002_scat.png")

# Add Voronoi sample image paths
VORONOI_SAMPLE_IMAGE = str(SAMPLE_IMAGE_PATH / "tan001_voronoi.png")
VORONOI_SAMPLE_IMAGE_2 = str(SAMPLE_IMAGE_PATH / "tan002_voronoi.png")

SAMPLE_DATA_PATH = SAMPLE_PATH / "sample_data"
FAMILIAL_SAMPLE_DATA = str(SAMPLE_DATA_PATH / "sample_familial_matches.tsv")
FAMILIAL_SAMPLE_DATA_2 = str(SAMPLE_DATA_PATH / "sample_familial_matches1.tsv")
FAMILIAL_SAMPLE_DATA_ERRORS = str(
    SAMPLE_DATA_PATH / "sample_familial_matches_errors.tsv"
)


def upload_sample_analysis(data: bytes, metadata: str | None = None) -> str:
    """Uploads a sample analysis from the web portal to the API

    Args:
        data (bytes): The data to upload
        metadata (str | None): The metadata to upload"""
    # This is a placeholder. Eventually, the real API call will be here
    # and we can return its response

    if data is None:
        raise ValueError(MISSING_DATA_ERROR)

    sample_identifier = SAMPLE_UUID

    if metadata is None:
        sample_identifier = NO_METADATA_UUID

    return sample_identifier


def get_scat_analysis(sample_id: str) -> str:
    """Gets the SCAT analysis for a sample

    Args:
        sample_id (str): The sample ID to get the SCAT analysis for"""
    # This is a placeholder. Eventually, the real API call will be here
    # and we can return its response

    if sample_id is None:
        raise ValueError(MISSING_UUID_ERROR)

    analysis = None

    if sample_id == SAMPLE_UUID:
        analysis = SCAT_SAMPLE_IMAGE
    elif sample_id == NO_METADATA_UUID:
        analysis = SCAT_SAMPLE_IMAGE_2
    elif sample_id == IN_PROGRESS_UUID:
        analysis = SCAT_SAMPLE_IMAGE  # This can be any image that represents an in-progress state

    if analysis is None:
        raise FileNotFoundError

    return analysis


def get_voronoi_analysis(sample_id: str) -> str:
    """Gets the Voronoi analysis for a sample

    Args:
        sample_id (str): The sample ID to get the Voronoi analysis for"""
    # This is a placeholder. Eventually, the real API call will be here
    # and we can return its response
    if sample_id is None:
        raise ValueError(MISSING_UUID_ERROR)

    analysis = None

    if sample_id == SAMPLE_UUID:
        analysis = VORONOI_SAMPLE_IMAGE
    elif sample_id == NO_METADATA_UUID:
        analysis = VORONOI_SAMPLE_IMAGE_2

    if analysis is None:
        raise FileNotFoundError

    return analysis


def get_familial_analysis(sample_id: str) -> pd.DataFrame:
    """Retrieves the familial analysis for a sample

    Args:
        sample_id (str): The sample ID to get the familial analysis for"""
    # This is a placeholder. Eventually, the real API call will be here
    # and we can return its response
    if sample_id is None:
        raise ValueError(MISSING_UUID_ERROR)

    analysis_path = None

    if sample_id == SAMPLE_UUID:
        analysis_path = FAMILIAL_SAMPLE_DATA
    elif sample_id == NO_METADATA_UUID:
        analysis_path = FAMILIAL_SAMPLE_DATA_2
    elif sample_id == FAMILIAL_FILE_PARSE_ERROR_UUID:
        analysis_path = FAMILIAL_SAMPLE_DATA_ERRORS

    if analysis_path is None:
        raise FileNotFoundError

    try:
        return pd.read_csv(analysis_path, sep="\t", skiprows=1)
    except Exception:
        logger.exception("Error loading familial results")
        raise RuntimeError(FAMILIAL_TSV_ERROR) from None


def list_analyses() -> list[str]:
    """Lists UUIDs for all SCAT analyses

    Returns:
        list[str]: A list of all SCAT analyses"""
    # This is a placeholder. Eventually, the real API call will be here
    # and we can return its response

    return UUID_LIST


def get_analysis_status(sample_id: str) -> str:
    """
    Retrieves the status of the analysis based on the given UUID.

    Args:
        sample_id (str): The UUID of the analysis to retrieve the status for.

    Returns:
        str: The human-readable status of the analysis.

    """
    if sample_id is None:
        raise ValueError(MISSING_UUID_ERROR)

    if sample_id in [SAMPLE_UUID, NO_METADATA_UUID]:
        return AnalysisStatus.ANALYSIS_SUCCEEDED.value
    if sample_id == IN_PROGRESS_UUID:
        return AnalysisStatus.ANALYSIS_IN_PROGRESS.value
    if sample_id == ANALYSIS_FAILED_UUID:
        return AnalysisStatus.ANALYSIS_FAILED.value

    error_message = "No analysis found for the given UUID"
    raise FileNotFoundError(error_message)
