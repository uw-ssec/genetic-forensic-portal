from unittest import mock

import pytest
from keycloak import KeycloakPostError

from genetic_forensic_portal.app.client import keycloak_client


def test_login_successfully():
    with mock.patch(
        "genetic_forensic_portal.app.client.keycloak_client.keycloak_openid"
    ) as mock_keycloak_openid:
        mock_keycloak_openid.token.return_value = {
            "access_token": "access_token",
        }
        assert keycloak_client.login_user("username", "password") == {
            "access_token": "access_token"
        }
        assert mock_keycloak_openid.token.call_count == 1


def test_login_error_throws():
    with mock.patch(
        "genetic_forensic_portal.app.client.keycloak_client.keycloak_openid"
    ) as mock_keycloak_openid:
        mock_keycloak_openid.token.side_effect = KeycloakPostError("Error")
        with pytest.raises(KeycloakPostError):
            keycloak_client.login_user("username", "password")
        assert mock_keycloak_openid.token.call_count == 1


def test_logout_successfully():
    with mock.patch(
        "genetic_forensic_portal.app.client.keycloak_client.keycloak_openid"
    ) as mock_keycloak_openid:
        mock_keycloak_openid.logout.return_value = None
        keycloak_client.logout_user({"refresh_token": "test"})
        assert mock_keycloak_openid.logout.call_count == 1


def test_logout_error_throws():
    with mock.patch(
        "genetic_forensic_portal.app.client.keycloak_client.keycloak_openid"
    ) as mock_keycloak_openid:
        mock_keycloak_openid.logout.side_effect = KeycloakPostError("Error")
        with pytest.raises(KeycloakPostError):
            keycloak_client.logout_user({"refresh_token": "test"})
        assert mock_keycloak_openid.logout.call_count == 1
