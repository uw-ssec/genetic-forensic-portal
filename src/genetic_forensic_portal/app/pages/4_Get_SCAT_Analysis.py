from __future__ import annotations

import streamlit as st

from genetic_forensic_portal.app.client import gf_api_client as client

st.header("Get SCAT Analysis")

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
    except FileNotFoundError:
        st.error("Analysis not found")
