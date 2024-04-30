from __future__ import annotations

import streamlit as st

from genetic_forensic_portal.app.client import gf_api_client as client

st.write("Upload Sample")
with st.form(key="my_form"):
    data = st.file_uploader(
        "Upload Sample Data: ", type=["tsv"], accept_multiple_files=False
    )
    location = st.text_input("Location seized: ")
    submit_button = st.form_submit_button(label="Submit")
    if submit_button:
        st.write("Sample uploaded successfully!")
        st.write("metadata: ", location)
        uuid = client.upload_sample_analysis(data=data, metadata=location)
        st.write("Sample UUID: ", uuid)
