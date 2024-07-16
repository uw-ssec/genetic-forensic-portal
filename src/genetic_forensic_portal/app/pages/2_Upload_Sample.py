from __future__ import annotations

import streamlit as st

from genetic_forensic_portal.app.client import gf_api_client as client
from genetic_forensic_portal.app.common import setup
from genetic_forensic_portal.app.common.constants import AUTHENTICATED

st.title("Upload Sample")

setup.initialize()

if st.session_state[AUTHENTICATED]:
    with st.form(key="my_form"):
        data = st.file_uploader(
            "Upload Sample Data: ", type=["tsv"], accept_multiple_files=False
        )
        location = st.text_input("Location seized: ")
        submit_button = st.form_submit_button(label="Submit")
        if submit_button:
            try:
                uuid = client.upload_sample_analysis(data=data, metadata=location)
                st.write("Sample uploaded successfully!")
                st.write("metadata: ", location)
                st.write("Sample UUID: ", uuid)
            except Exception as e:
                st.write("Error uploading sample: ", e)
