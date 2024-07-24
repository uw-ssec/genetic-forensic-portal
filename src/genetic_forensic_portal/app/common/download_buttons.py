from __future__ import annotations

import logging
from pathlib import Path

import streamlit as st

import genetic_forensic_portal.app.client.gf_api_client as client
from genetic_forensic_portal.app.common.constants import USERNAME

logger = logging.getLogger(__name__)


def scat_analysis_download_button(uuid: str) -> None:
    try:
        analysis_data_path = client.get_scat_analysis_data(uuid)
        if analysis_data_path:
            analysis_file_name = analysis_data_path.split("/")[-1]
            with Path(analysis_data_path).open("rb") as f:
                st.download_button(
                    label="Download SCAT Analysis",
                    data=f.read(),
                    file_name=analysis_file_name,
                    mime="application/zip",
                )
    except FileNotFoundError:
        logger.debug(
            "SCAT analysis data not found: %s for user %s",
            uuid,
            st.session_state[USERNAME],
        )


def voronoi_analysis_download_button(uuid: str) -> None:
    try:
        analysis_data_path = client.get_voronoi_analysis_data(uuid)
        if analysis_data_path:
            analysis_file_name = analysis_data_path.split("/")[-1]
            with Path(analysis_data_path).open("rb") as f:
                st.download_button(
                    label="Download Voronoi Analysis",
                    data=f.read(),
                    file_name=analysis_file_name,
                    mime="application/zip",
                )
    except FileNotFoundError:
        logger.debug(
            "Voronoi analysis data not found: %s for user %s",
            uuid,
            st.session_state[USERNAME],
        )
