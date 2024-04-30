from __future__ import annotations

MISSING_DATA_ERROR = "data is required"
SAMPLE_UUID = "this-is-a-uuid"
NO_METADATA_UUID = "this-is-a-differentuuid"


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
