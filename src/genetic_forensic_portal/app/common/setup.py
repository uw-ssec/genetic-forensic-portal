from typing import Any

import streamlit as st

from genetic_forensic_portal.app.client import keycloak_client
from genetic_forensic_portal.app.common.constants import (
    AUTHENTICATED,
    ROLES,
    TOKEN,
    USERNAME,
)


def initialize_session_state() -> None:
    if AUTHENTICATED not in st.session_state:
        st.session_state[AUTHENTICATED] = False

    if USERNAME not in st.session_state:
        st.session_state[USERNAME] = None


def login_success(message: str, username: str, token: dict[Any, Any]) -> None:
    st.success(message)
    st.session_state[AUTHENTICATED] = True
    st.session_state[USERNAME] = username
    st.session_state[TOKEN] = token
    st.rerun()


@st.experimental_dialog("Login")  # type: ignore[misc]
def authentication_dialog() -> None:
    with st.form(key="login"):
        username = st.text_input(
            label="Login username",
            placeholder=None,
            help=None,
            disabled=st.session_state[AUTHENTICATED],
        )

        password = st.text_input(
            label="Login password",
            placeholder=None,
            help=None,
            type="password",
            disabled=st.session_state[AUTHENTICATED],
        )

        if st.form_submit_button(
            label="Login",
            disabled=st.session_state[AUTHENTICATED],
            type="primary",
        ):
            try:
                token = keycloak_client.login_user(username, password)

                if len(token) > 0:
                    login_success("Logged in!", username, token)
                else:
                    st.error("Error logging in")
                    st.session_state[AUTHENTICATED] = False
            except Exception as e:
                st.error(e)
                st.session_state[AUTHENTICATED] = False


@st.experimental_dialog("Logout Flow")  # type: ignore[misc]
def authentication_logout() -> None:
    st.write(f"Are you sure you want to logout, {st.session_state[USERNAME]}?")
    if st.button("Confirm Logout"):
        keycloak_client.logout_user(st.session_state[TOKEN])
        st.session_state[AUTHENTICATED] = False
        st.session_state[USERNAME] = None
        st.session_state[ROLES] = None
        st.session_state[TOKEN] = None
        st.rerun()


def create_authentication() -> None:
    if not st.session_state[AUTHENTICATED]:
        if st.button("Login"):
            authentication_dialog()
    else:
        st.write(f"Welcome {st.session_state[USERNAME]}!")
        if st.button("Logout"):
            authentication_logout()


def initialize() -> None:
    initialize_session_state()
    create_authentication()
