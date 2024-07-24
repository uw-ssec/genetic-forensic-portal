from __future__ import annotations

import streamlit as st

from genetic_forensic_portal.app.client import gf_api_client as client
from genetic_forensic_portal.app.client import keycloak_client as auth_client
from genetic_forensic_portal.app.common import download_buttons, setup
from genetic_forensic_portal.app.common.constants import AUTHENTICATED, ROLES, USERNAME

st.header("Get SCAT Analysis")

setup.initialize()

if st.session_state[AUTHENTICATED]:
    uuid = getattr(st.session_state, "uuid", None)

    analysis_list = client.list_all_analyses()

    uuid = st.selectbox(
        "Select a sample ID",
        analysis_list,
        index=getattr(st.session_state, "index", None),
        placeholder="Select sample ID...",
    )

    if uuid:
        try:
            analysis = client.get_scat_analysis(uuid)
            st.image(analysis, caption="SCAT Analysis")

            if auth_client.check_download_access(
                st.session_state[USERNAME], st.session_state[ROLES], uuid
            ):
                download_buttons.scat_analysis_download_button(uuid)

        except FileNotFoundError:
            st.error("Analysis not found")
