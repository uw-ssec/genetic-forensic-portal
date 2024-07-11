from unittest.mock import patch

from genetic_forensic_portal.app.client import keycloak_client
from genetic_forensic_portal.app.client.models.analysis_permissions import (
    Action,
    AnalysisPermissions,
    Effect,
    EntityType,
    Permission,
)

TEST_USER = "test_user"
TEST_RESOURCE = "test_resource"
TEST_ROLE = "test_role"


# user: T resource: T decision: True
@patch(
    "genetic_forensic_portal.app.client.keycloak_client.MOCK_USER_AUTH_CACHE",
    {
        TEST_USER: {
            Action.VIEW: True,
            Action.DOWNLOAD: True,
            Action.CREATE: True,
            Action.LIST_ALL: True,
        }
    },
)
@patch(
    "genetic_forensic_portal.app.client.keycloak_client.MOCK_RESOURCE_AUTH_CACHE",
    {TEST_RESOURCE + "1": {TEST_USER: {Action.VIEW: True, Action.DOWNLOAD: True}}},
)
def test_user_allowed_resource_allowed_access_allowed():
    assert keycloak_client.check_view_access(TEST_USER, [], TEST_RESOURCE + "1")
    assert keycloak_client.check_download_access(TEST_USER, [], TEST_RESOURCE + "1")
    assert keycloak_client.check_create_access(TEST_USER, [])
    assert keycloak_client.check_list_all_access(TEST_USER, [])


# user: N resource: T decision: True
@patch(
    "genetic_forensic_portal.app.client.keycloak_client.MOCK_USER_AUTH_CACHE",
    {TEST_USER: {Action.VIEW: None, Action.DOWNLOAD: None}},
)
@patch(
    "genetic_forensic_portal.app.client.keycloak_client.MOCK_RESOURCE_AUTH_CACHE",
    {TEST_RESOURCE + "2": {TEST_USER: {Action.VIEW: True, Action.DOWNLOAD: True}}},
)
def test_user_not_defined_resource_allowed_access_allowed():
    assert keycloak_client.check_view_access(TEST_USER, [], TEST_RESOURCE + "2")
    assert keycloak_client.check_download_access(TEST_USER, [], TEST_RESOURCE + "2")


# user: F resource: T decision: False
@patch(
    "genetic_forensic_portal.app.client.keycloak_client.MOCK_USER_AUTH_CACHE",
    {TEST_USER: {Action.VIEW: False, Action.DOWNLOAD: False}},
)
@patch(
    "genetic_forensic_portal.app.client.keycloak_client.MOCK_RESOURCE_AUTH_CACHE",
    {TEST_RESOURCE + "3": {TEST_USER: {Action.VIEW: True, Action.DOWNLOAD: True}}},
)
def test_user_denied_resource_allowed_access_denied():
    assert not keycloak_client.check_view_access(TEST_USER, [], TEST_RESOURCE + "3")
    assert not keycloak_client.check_download_access(TEST_USER, [], TEST_RESOURCE + "3")


# user: T resource: F decision: False
@patch(
    "genetic_forensic_portal.app.client.keycloak_client.MOCK_USER_AUTH_CACHE",
    {TEST_USER: {Action.VIEW: True, Action.DOWNLOAD: True}},
)
@patch(
    "genetic_forensic_portal.app.client.keycloak_client.MOCK_RESOURCE_AUTH_CACHE",
    {TEST_RESOURCE + "4": {TEST_USER: {Action.VIEW: False, Action.DOWNLOAD: False}}},
)
def test_user_allowed_resource_denied_access_denied():
    assert not keycloak_client.check_view_access(TEST_USER, [], TEST_RESOURCE + "4")
    assert not keycloak_client.check_download_access(TEST_USER, [], TEST_RESOURCE + "4")


# user: N resource: F decision: False
@patch(
    "genetic_forensic_portal.app.client.keycloak_client.MOCK_USER_AUTH_CACHE",
    {TEST_USER: {Action.VIEW: None, Action.DOWNLOAD: None}},
)
@patch(
    "genetic_forensic_portal.app.client.keycloak_client.MOCK_RESOURCE_AUTH_CACHE",
    {TEST_RESOURCE + "5": {TEST_USER: {Action.VIEW: False, Action.DOWNLOAD: False}}},
)
def test_user_not_defined_resource_denied_access_denied():
    assert not keycloak_client.check_view_access(TEST_USER, [], TEST_RESOURCE + "5")
    assert not keycloak_client.check_download_access(TEST_USER, [], TEST_RESOURCE + "5")


# user: F resource: F decision: False
@patch(
    "genetic_forensic_portal.app.client.keycloak_client.MOCK_USER_AUTH_CACHE",
    {TEST_USER: {Action.VIEW: False, Action.DOWNLOAD: False}},
)
@patch(
    "genetic_forensic_portal.app.client.keycloak_client.MOCK_RESOURCE_AUTH_CACHE",
    {TEST_RESOURCE + "6": {TEST_USER: {Action.VIEW: False, Action.DOWNLOAD: False}}},
)
def test_user_denied_resource_denied_access_denied():
    assert not keycloak_client.check_view_access(TEST_USER, [], TEST_RESOURCE + "6")
    assert not keycloak_client.check_download_access(TEST_USER, [], TEST_RESOURCE + "6")


@patch(
    "genetic_forensic_portal.app.client.keycloak_client.MOCK_GROUP_ACCESS_CONTROL",
    {TEST_ROLE: Permission(TEST_ROLE, Effect.ALLOW, [Action.VIEW, Action.DOWNLOAD])},
)
@patch(
    "genetic_forensic_portal.app.client.keycloak_client.MOCK_RESOURCE_ACCESS_CONTROL",
    {
        TEST_RESOURCE + "7": AnalysisPermissions(
            analysis_owner="other_group",
            owner_type=EntityType.GROUP,
            role_permissions=[
                Permission(TEST_ROLE, Effect.ALLOW, [Action.VIEW, Action.DOWNLOAD])
            ],
            user_permissions=[],
        )
    },
)
def test_role_allow_user_none_resource_allow_access_allow():
    assert keycloak_client.check_view_access(
        TEST_USER, [TEST_ROLE], TEST_RESOURCE + "7"
    )
    assert keycloak_client.check_download_access(
        TEST_USER, [TEST_ROLE], TEST_RESOURCE + "7"
    )


@patch(
    "genetic_forensic_portal.app.client.keycloak_client.MOCK_GROUP_ACCESS_CONTROL",
    {TEST_ROLE: Permission(TEST_ROLE, Effect.DENY, [Action.VIEW, Action.DOWNLOAD])},
)
@patch(
    "genetic_forensic_portal.app.client.keycloak_client.MOCK_RESOURCE_ACCESS_CONTROL",
    {
        TEST_RESOURCE + "8": AnalysisPermissions(
            analysis_owner="other_group",
            owner_type=EntityType.GROUP,
            role_permissions=[],
            user_permissions=[],
        )
    },
)
def test_role_deny_user_none_resource_none_access_deny():
    assert not keycloak_client.check_view_access(
        TEST_USER, [TEST_ROLE], TEST_RESOURCE + "8"
    )
    assert not keycloak_client.check_download_access(
        TEST_USER, [TEST_ROLE], TEST_RESOURCE + "8"
    )


@patch(
    "genetic_forensic_portal.app.client.keycloak_client.MOCK_USER_ACCESS_CONTROL",
    {TEST_USER: Permission(TEST_USER, Effect.DENY, [Action.VIEW, Action.DOWNLOAD])},
)
@patch(
    "genetic_forensic_portal.app.client.keycloak_client.MOCK_RESOURCE_ACCESS_CONTROL",
    {
        TEST_RESOURCE + "9": AnalysisPermissions(
            analysis_owner="other_group",
            owner_type=EntityType.GROUP,
            role_permissions=[],
            user_permissions=[],
        )
    },
)
def test_role_none_user_deny_resource_allow_access_deny():
    assert not keycloak_client.check_view_access(
        TEST_USER, [TEST_ROLE], TEST_RESOURCE + "9"
    )
    assert not keycloak_client.check_download_access(
        TEST_USER, [TEST_ROLE], TEST_RESOURCE + "9"
    )


@patch(
    "genetic_forensic_portal.app.client.keycloak_client.MOCK_RESOURCE_ACCESS_CONTROL",
    {
        TEST_RESOURCE + "10": AnalysisPermissions(
            analysis_owner="other_group",
            owner_type=EntityType.GROUP,
            role_permissions=[
                Permission(TEST_ROLE, Effect.DENY, [Action.VIEW, Action.DOWNLOAD])
            ],
            user_permissions=[],
        )
    },
)
def test_role_allow_user_none_resource_role_deny_access_deny():
    assert not keycloak_client.check_view_access(
        TEST_USER, [TEST_ROLE], TEST_RESOURCE + "10"
    )
    assert not keycloak_client.check_download_access(
        TEST_USER, [TEST_ROLE], TEST_RESOURCE + "10"
    )


@patch(
    "genetic_forensic_portal.app.client.keycloak_client.MOCK_USER_AUTH_CACHE",
    {
        TEST_USER: {
            Action.VIEW: True,
            Action.DOWNLOAD: True,
            Action.CREATE: None,
            Action.LIST_ALL: None,
        }
    },
)
def test_user_none_access_deny():
    assert not keycloak_client.check_create_access(TEST_USER, [])
    assert not keycloak_client.check_list_all_access(TEST_USER, [])
