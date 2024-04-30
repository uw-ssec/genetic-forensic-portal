from __future__ import annotations

import pytest

import genetic_forensic_portal.app.client.gf_api_client as client

TEST_FILE_DATA = b"this is a file"
TEST_METADATA = "this is metadata"


def test_upload_file_returns_uuid():
    response = client.upload_sample_analysis(TEST_FILE_DATA, TEST_METADATA)

    assert response == client.SAMPLE_UUID


def test_upload_nothing_returns_error():
    with pytest.raises(ValueError, match=client.MISSING_DATA_ERROR):
        client.upload_sample_analysis(None)  # type: ignore[arg-type]


def test_upload_no_metadata_returns_different_uuid():
    response = client.upload_sample_analysis(TEST_FILE_DATA)

    assert response == client.NO_METADATA_UUID
