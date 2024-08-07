from __future__ import annotations

import streamlit as st

import genetic_forensic_portal.app.utils.familial_analysis_utils as fam_utils
from genetic_forensic_portal.app.client import gf_api_client as client
from genetic_forensic_portal.app.common import setup
from genetic_forensic_portal.app.common.constants import AUTHENTICATED

st.header("Get Familial Analysis")

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
            analysis = client.get_familial_analysis(uuid)
            st.dataframe(
                analysis.style.map(
                    fam_utils.highlight_exact_matches,
                    subset=[fam_utils.EXACT_MATCH_COLUMN],
                )
            )
        except FileNotFoundError:
            st.error("Analysis not found")
        except Exception as e:
            st.error(e)
