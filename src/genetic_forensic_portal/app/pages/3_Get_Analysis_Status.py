from __future__ import annotations

import streamlit as st

from genetic_forensic_portal.app.client import gf_api_client as client
from genetic_forensic_portal.app.common import setup
from genetic_forensic_portal.app.common.constants import AUTHENTICATED

st.title("Get Analysis Status")

setup.initialize()

if st.session_state[AUTHENTICATED]:
    uuid = st.selectbox(
        "Select a sample ID",
        client.list_all_analyses(),
        index=None,
        placeholder="Select sample ID...",
    )

    if uuid:
        try:
            status = client.get_analysis_status(uuid).value
            st.success(f"Current status of the analysis: {status}")
        except ValueError as ve:
            st.error(f"Invalid input: {ve}")
        except FileNotFoundError:
            st.error("Analysis not found for the given UUID")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
