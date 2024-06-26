from __future__ import annotations

import os
from typing import Any

from keycloak import KeycloakOpenID

KEYCLOAK_SERVER_URL = os.environ.get("KEYCLOAK_SERVER_URL", "http://localhost:8080/")

keycloak_openid = KeycloakOpenID(
    server_url=KEYCLOAK_SERVER_URL,
    client_id="gf-portal-login",
    realm_name="gf-portal",
)


def login_user(username: str, password: str) -> Any:
    return keycloak_openid.token(username, password)


def logout_user(token: dict[Any, Any]) -> None:
    keycloak_openid.logout(token["refresh_token"])
