from __future__ import annotations

import streamlit as st

from genetic_forensic_portal.app.client import gf_api_client as client
from genetic_forensic_portal.utils.analysis_status import AnalysisStatus


def try_get_analysis(uuid: str) -> AnalysisStatus:
    try:
        return client.get_analysis_status(uuid)
    except FileNotFoundError:
        return AnalysisStatus.ANALYSIS_NOT_FOUND
    except Exception:
        return AnalysisStatus.ANALYSIS_ERROR


st.session_state.sorted_results = getattr(st.session_state, "sorted_results", [])
st.session_state.analysis_start = getattr(st.session_state, "analysis_start", 0)
st.session_state.analysis_next = getattr(st.session_state, "analysis_next", None)


def update_session_state(uuid: str, index: int) -> None:
    st.session_state.uuid = uuid
    st.session_state.index = index


def retrieve_analyses(start: int = 0) -> list[str]:
    if (
        len(st.session_state.sorted_results) == 0
        or st.session_state.analysis_next is not None
    ):
        analyses_list = client.list_analyses(start)
        st.session_state.analysis_start = analyses_list.start_token
        st.session_state.analysis_next = analyses_list.next_token
        return analyses_list.analyses
    return []


def retrieve_and_sort_analyses(start: int = 0) -> None:
    analyses = retrieve_analyses(start)
    statuses = [try_get_analysis(analysis) for analysis in analyses]
    results = list(
        zip(range(start, start + len(analyses)), analyses, statuses, strict=True)
    )
    full_results = st.session_state.sorted_results + results
    st.session_state.sorted_results = sorted(full_results, key=lambda x: x[2])


st.header("List Analyses")

if len(st.session_state.sorted_results) == 0:
    retrieve_and_sort_analyses()


st.write(f"Showing {len(st.session_state.sorted_results)} analyses.")

if st.session_state.analysis_next is not None:
    st.write("More analyses can be shown. Load them?")
    st.button(
        "Load more",
        on_click=lambda: retrieve_and_sort_analyses(
            start=st.session_state.analysis_next
        ),
    )


ana_col, status_col, scat_col, vor_col, fam_col = st.columns([1, 0.7, 0.5, 0.5, 0.5])
ana_col.write("**Analysis ID**")
status_col.write("**Status**")
scat_col.write("**SCAT Analysis**")
vor_col.write("**Voronoi Analysis**")
fam_col.write("**Familial Analysis**")


for index, analysis, status in st.session_state.sorted_results:
    ana_col, status_col, scat_col, vor_col, fam_col = st.columns(
        [1, 0.7, 0.5, 0.5, 0.5]
    )
    ana_col.write(analysis)
    status_col.write(status.value)
    with scat_col:
        if st.button(key=f"SCAT {analysis}", label="SCAT", use_container_width=True):
            update_session_state(analysis, index)
            st.switch_page("pages/4_Get_SCAT_Analysis.py")
    with vor_col:
        if st.button(
            key=f"Voronoi {analysis}", label="Voronoi", use_container_width=True
        ):
            update_session_state(analysis, index)
            st.switch_page("pages/5_Get_Voronoi_Analysis.py")
    with fam_col:
        if st.button(
            key=f"Familial {analysis}", label="Familial", use_container_width=True
        ):
            update_session_state(analysis, index)
            st.switch_page("pages/6_Get_Familial_Analysis.py")
