from __future__ import annotations

import streamlit as st

from genetic_forensic_portal.app.client import gf_api_client as client

st.header("Get Voronoi Analysis")

uuid = getattr(st.session_state, "uuid", None)

analysis_list = client.list_all_analyses()

uuid = st.selectbox(
    "Select a sample ID",
    client.list_all_analyses(),
    index=getattr(st.session_state, "index", None),
    placeholder="Select sample ID...",
)


if uuid:
    try:
        analysis = client.get_voronoi_analysis(uuid)
        st.image(analysis, caption="Voronoi Analysis")
    except FileNotFoundError:
        st.error("Analysis not found")
