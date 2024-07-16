from __future__ import annotations

import io
from unittest import mock

import pandas as pd
import pytest
import streamlit

import genetic_forensic_portal.app.client.gf_api_client as client
from genetic_forensic_portal.app.client.models.get_analyses_response import (
    GetAnalysesResponse,
)
from genetic_forensic_portal.app.common.constants import (
    ANALYSIS_FAILED_UUID,
    AUTHENTICATED,
    FAMILIAL_FILE_PARSE_ERROR_UUID,
    IN_PROGRESS_UUID,
    NO_METADATA_UUID,
    ROLES,
    SAMPLE_UUID,
    USERNAME,
)
from genetic_forensic_portal.app.utils.validate_input_file import (
    HEADER_MUST_START_WITH_MATCHID,
)
from genetic_forensic_portal.utils.analysis_status import AnalysisStatus

TEST_FILE_DATA = io.BytesIO(b"this is a file")
TEST_METADATA = "this is metadata"

MOCK_STREAMLIT = streamlit
MOCK_STREAMLIT.session_state = {
    AUTHENTICATED: True,
    USERNAME: "test1",
    ROLES: ["admin"],
}

UUIDS_WITH_ACCESS = [
    SAMPLE_UUID,
    NO_METADATA_UUID,
    IN_PROGRESS_UUID,
    ANALYSIS_FAILED_UUID,
    FAMILIAL_FILE_PARSE_ERROR_UUID,
]


def test_upload_file_returns_uuid():
    with mock.patch(
        "genetic_forensic_portal.app.utils.validate_input_file.validate_input_file"
    ):
        response = client.upload_sample_analysis(TEST_FILE_DATA, TEST_METADATA)

        assert response == client.SAMPLE_UUID


def test_upload_nothing_returns_error():
    with (
        mock.patch(
            "genetic_forensic_portal.app.utils.validate_input_file.validate_input_file"
        ),
        pytest.raises(ValueError, match=client.MISSING_DATA_ERROR),
    ):
        client.upload_sample_analysis(None)  # type: ignore[arg-type]


def test_upload_no_metadata_returns_different_uuid():
    with mock.patch(
        "genetic_forensic_portal.app.utils.validate_input_file.validate_input_file"
    ):
        response = client.upload_sample_analysis(TEST_FILE_DATA)

        assert response == client.NO_METADATA_UUID


def test_upload_file_raises_error():
    with (
        mock.patch(
            "genetic_forensic_portal.app.utils.validate_input_file.validate_input_file"
        ) as mock_validate_input_file,
    ):
        mock_validate_input_file.side_effect = ValueError(
            HEADER_MUST_START_WITH_MATCHID
        )
        with pytest.raises(ValueError, match=HEADER_MUST_START_WITH_MATCHID):
            client.upload_sample_analysis(TEST_FILE_DATA, TEST_METADATA)


def test_upload_no_access_returns_error():
    with (
        pytest.raises(PermissionError, match=client.UPLOAD_DENIED_ERROR),
        mock.patch(
            "genetic_forensic_portal.app.client.keycloak_client.check_create_access",
            return_value=False,
        ),
    ):
        client.upload_sample_analysis(TEST_FILE_DATA, TEST_METADATA)


# SCAT Analysis


def test_get_scat_analysis_returns_image_path():
    response = client.get_scat_analysis(client.SAMPLE_UUID)

    assert response == client.SCAT_SAMPLE_IMAGE


def test_get_scat_analysis_returns_image_path_in_progress_uiud():
    response = client.get_scat_analysis(client.IN_PROGRESS_UUID)

    assert response == client.SCAT_SAMPLE_IMAGE


def test_get_scat_analysis_no_metadata_returns_different_image_path():
    response = client.get_scat_analysis(client.NO_METADATA_UUID)

    assert response == client.SCAT_SAMPLE_IMAGE_2


def test_get_scat_analysis_raises_error():
    with (
        pytest.raises(FileNotFoundError),
        mock.patch(
            "genetic_forensic_portal.app.client.keycloak_client.check_view_access",
            return_value=True,
        ),
    ):
        client.get_scat_analysis("not-an-uuid")


def test_get_scat_analysis_no_access_raises_error():
    with (
        pytest.raises(FileNotFoundError),
        mock.patch(
            "genetic_forensic_portal.app.client.keycloak_client.check_view_access",
            return_value=False,
        ),
    ):
        client.get_scat_analysis("not-an-uuid")


def test_get_scat_analysis_raises_error_for_none():
    with pytest.raises(ValueError, match=client.MISSING_UUID_ERROR):
        client.get_scat_analysis(None)  # type: ignore[arg-type]


def test_list_all_analyses_returns_list():
    response = client.list_all_analyses()

    assert response == UUIDS_WITH_ACCESS


def test_list_analyses_returns_response_object():
    response = client.list_analyses()

    assert response.analyses == UUIDS_WITH_ACCESS[: client.DEFAULT_LIST_PAGE_SIZE]
    assert response.start_token == 0
    assert (
        response.next_token == client.DEFAULT_LIST_PAGE_SIZE + 2
    )  # 2 UUIDs are not accessible and thus omitted from results


def test_list_analyses_with_start_returns_correct_page():
    response = client.list_analyses(client.DEFAULT_LIST_PAGE_SIZE)

    assert (
        response.analyses
        == UUIDS_WITH_ACCESS[
            client.DEFAULT_LIST_PAGE_SIZE - 1 : client.DEFAULT_LIST_PAGE_SIZE * 2 - 1
        ]
    )
    assert response.start_token == client.DEFAULT_LIST_PAGE_SIZE
    assert response.next_token is None


def test_list_analyses_with_early_returns_page_with_correct_size():
    start_token = 1
    response = client.list_analyses(start_token)

    expected_end = start_token + client.DEFAULT_LIST_PAGE_SIZE + 2

    assert (
        response.analyses
        == UUIDS_WITH_ACCESS[start_token : start_token + client.DEFAULT_LIST_PAGE_SIZE]
    )
    assert len(response.analyses) == client.DEFAULT_LIST_PAGE_SIZE
    assert response.start_token == start_token
    assert response.next_token == expected_end


def test_list_analyses_with_out_of_bounds_start_returns_empty_list():
    response = client.list_analyses(100)

    assert response.analyses == []
    assert response.start_token == 0
    assert response.next_token is None


# Voronoi Analysis


def test_get_voronoi_analysis_returns_image_path():
    response = client.get_voronoi_analysis(client.SAMPLE_UUID)

    assert response == client.VORONOI_SAMPLE_IMAGE


def test_get_voronoi_analysis_no_metadata_returns_different_image_path():
    response = client.get_voronoi_analysis(client.NO_METADATA_UUID)

    assert response == client.VORONOI_SAMPLE_IMAGE_2


def test_get_voronoi_analysis_raises_error():
    with (
        pytest.raises(FileNotFoundError),
        mock.patch(
            "genetic_forensic_portal.app.client.keycloak_client.check_view_access",
            return_value=True,
        ),
    ):
        client.get_voronoi_analysis("not-an-uuid")


def test_get_voronoi_analysis_no_access_raises_error():
    with (
        pytest.raises(FileNotFoundError),
        mock.patch(
            "genetic_forensic_portal.app.client.keycloak_client.check_view_access",
            return_value=False,
        ),
    ):
        client.get_voronoi_analysis("not-an-uuid")


def test_get_voronoi_analysis_raises_error_for_none():
    with pytest.raises(ValueError, match=client.MISSING_UUID_ERROR):
        client.get_voronoi_analysis(None)  # type: ignore[arg-type]


# Tests for the get_analysis_status function
def test_get_analysis_status_succeeded():
    response = client.get_analysis_status(client.SAMPLE_UUID)
    assert response == AnalysisStatus.ANALYSIS_SUCCEEDED


def test_get_analysis_status_in_progress():
    response = client.get_analysis_status(client.IN_PROGRESS_UUID)
    assert response == AnalysisStatus.ANALYSIS_IN_PROGRESS


def test_get_analysis_status_failed():
    response = client.get_analysis_status(client.ANALYSIS_FAILED_UUID)
    assert response == AnalysisStatus.ANALYSIS_FAILED


def test_get_analysis_status_not_found():
    with (
        pytest.raises(FileNotFoundError),
        mock.patch(
            "genetic_forensic_portal.app.client.keycloak_client.check_view_access",
            return_value=True,
        ),
    ):
        client.get_analysis_status("unknown-uuid")


def test_get_analysis_status_no_access_raises_error():
    with (
        pytest.raises(FileNotFoundError),
        mock.patch(
            "genetic_forensic_portal.app.client.keycloak_client.check_view_access",
            return_value=False,
        ),
    ):
        client.get_analysis_status("not-an-uuid")


def test_get_analysis_status_no_uuid_provided():
    with pytest.raises(ValueError, match=client.MISSING_UUID_ERROR):
        client.get_analysis_status(None)  # type: ignore[arg-type]


# Familial Analysis


def test_get_familial_analysis_returns_image_path():
    response = client.get_familial_analysis(client.SAMPLE_UUID)

    pd.testing.assert_frame_equal(
        response, pd.read_csv(client.FAMILIAL_SAMPLE_DATA, sep="\t", skiprows=1)
    )


def test_get_familial_analysis_no_metadata_returns_different_image_path():
    response = client.get_familial_analysis(client.NO_METADATA_UUID)

    pd.testing.assert_frame_equal(
        response, pd.read_csv(client.FAMILIAL_SAMPLE_DATA_2, sep="\t", skiprows=1)
    )


def test_get_familial_analysis_raises_error():
    with (
        pytest.raises(FileNotFoundError),
        mock.patch(
            "genetic_forensic_portal.app.client.keycloak_client.check_view_access",
            return_value=True,
        ),
    ):
        client.get_familial_analysis("not-an-uuid")


def test_get_familial_analysis_no_access_raises_error():
    with (
        pytest.raises(FileNotFoundError),
        mock.patch(
            "genetic_forensic_portal.app.client.keycloak_client.check_view_access",
            return_value=False,
        ),
    ):
        client.get_familial_analysis("not-an-uuid")


def test_get_familial_analysis_raises_error_for_none():
    with pytest.raises(ValueError, match=client.MISSING_UUID_ERROR):
        client.get_familial_analysis(None)  # type: ignore[arg-type]


def test_get_familial_analysis_with_erroring_file_raises():
    with pytest.raises(RuntimeError, match=client.FAMILIAL_TSV_ERROR):
        client.get_familial_analysis(client.FAMILIAL_FILE_PARSE_ERROR_UUID)


# Tests for the get_all_analyses function

# Mock data for testing
mock_scat_image = "scat_image_path"
mock_voronoi_image = "voronoi_image_path"
mock_familial_data = pd.DataFrame(
    {"Column1": ["Data1", "Data2"], "Column2": ["Data3", "Data4"]}
)


@pytest.fixture()
def mock_functions(mocker):
    def _mock_functions(mock_scat=None, mock_voronoi=None, mock_familial=None):
        mocker.patch(
            "genetic_forensic_portal.app.client.gf_api_client.get_scat_analysis",
            side_effect=mock_scat,
        )
        mocker.patch(
            "genetic_forensic_portal.app.client.gf_api_client.get_voronoi_analysis",
            side_effect=mock_voronoi,
        )
        mocker.patch(
            "genetic_forensic_portal.app.client.gf_api_client.get_familial_analysis",
            side_effect=mock_familial,
        )

    return _mock_functions


# Mock functions with exceptions to trigger the except blocks
def mock_scat(sample_id):
    if sample_id in ["missing-scat-uuid", "all-missing-uuid"]:
        raise FileNotFoundError
    return mock_scat_image


def mock_voronoi(sample_id):
    if sample_id in ["missing-voronoi-uuid", "all-missing-uuid"]:
        raise FileNotFoundError
    return mock_voronoi_image


def mock_familial(sample_id):
    if sample_id in ["missing-familial-uuid", "all-missing-uuid"]:
        raise Exception
    return mock_familial_data


@pytest.mark.parametrize(
    ("uuid", "mock_scat", "mock_voronoi", "mock_familial", "expected_results"),
    [
        (
            client.SAMPLE_UUID,
            mock_scat,
            mock_voronoi,
            mock_familial,
            GetAnalysesResponse(
                scat=mock_scat_image,
                voronoi=mock_voronoi_image,
                familial=mock_familial_data,
            ),
        ),
        (
            "missing-scat-uuid",
            mock_scat,
            mock_voronoi,
            mock_familial,
            GetAnalysesResponse(
                scat=None,
                voronoi=mock_voronoi_image,
                familial=mock_familial_data,
            ),
        ),
        (
            "missing-voronoi-uuid",
            mock_scat,
            mock_voronoi,
            mock_familial,
            GetAnalysesResponse(
                scat=mock_scat_image,
                voronoi=None,
                familial=mock_familial_data,
            ),
        ),
        (
            "missing-familial-uuid",
            mock_scat,
            mock_voronoi,
            mock_familial,
            GetAnalysesResponse(
                scat=mock_scat_image,
                voronoi=mock_voronoi_image,
                familial=None,
            ),
        ),
        (
            "all-missing-uuid",
            mock_scat,
            mock_voronoi,
            mock_familial,
            GetAnalysesResponse(
                scat=None,
                voronoi=None,
                familial=None,
            ),
        ),
    ],
)
def test_get_all_analyses(
    mock_functions, uuid, mock_scat, mock_voronoi, mock_familial, expected_results
):
    """Test different scenarios for get_all_analyses."""
    mock_functions(
        mock_scat=mock_scat, mock_voronoi=mock_voronoi, mock_familial=mock_familial
    )
    results = client.get_all_analyses(uuid)

    assert (
        results.scat == expected_results.scat
    ), f"SCAT analysis mismatch for UUID: {uuid}"
    assert (
        results.voronoi == expected_results.voronoi
    ), f"Voronoi analysis mismatch for UUID: {uuid}"
    if isinstance(results.familial, pd.DataFrame) and isinstance(
        expected_results.familial, pd.DataFrame
    ):
        assert results.familial.equals(
            expected_results.familial
        ), f"Familial analysis mismatch for UUID: {uuid}"
    else:
        assert (
            results.familial == expected_results.familial
        ), f"Familial analysis mismatch for UUID: {uuid}"
