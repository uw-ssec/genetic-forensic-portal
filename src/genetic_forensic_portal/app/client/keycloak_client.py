from __future__ import annotations

import os
from typing import Any

from keycloak import KeycloakOpenID

from genetic_forensic_portal.app.common.constants import (
    ANALYSIS_FAILED_UUID,
    FAMILIAL_FILE_PARSE_ERROR_UUID,
    IN_PROGRESS_UUID,
    NO_METADATA_UUID,
    NOT_AUTHORIZED_UUID,
    SAMPLE_UUID,
)

from .models.analysis_permissions import (
    Action,
    AnalysisPermissions,
    Effect,
    EntityType,
    Permission,
)

KEYCLOAK_SERVER_URL = os.environ.get("KEYCLOAK_SERVER_URL", "http://localhost:8080/")

keycloak_openid = KeycloakOpenID(
    server_url=KEYCLOAK_SERVER_URL,
    client_id="gf-portal-login",
    realm_name="gf-portal",
    client_secret_key="hFw4vaDOftBQClhO5XwankvYWGggLKhH",
)


TEST_CENTER = "test-center"
CEFS = "cefs"
ADMIN = "admin"
TEST_USER_1 = "test1"
NO_ACCESS_USER = "noaccess"

CEFS_ALLOW_ALL_ACCESS = Permission(
    entity=CEFS,
    effect=Effect.ALLOW,
    actions=[Action.VIEW, Action.DOWNLOAD],
)

ADMIN_ALLOW_ALL_ACCESS = Permission(
    entity=ADMIN,
    effect=Effect.ALLOW,
    actions=[Action.VIEW, Action.DOWNLOAD],
)

DENY_NO_ACCESS_USER = Permission(
    entity=NO_ACCESS_USER,
    effect=Effect.DENY,
    actions=[Action.VIEW, Action.DOWNLOAD],
)

MOCK_RESOURCE_ACCESS_CONTROL = {
    SAMPLE_UUID: AnalysisPermissions(
        analysis_owner=TEST_CENTER,
        owner_type=EntityType.GROUP,
        role_permissions=[
            CEFS_ALLOW_ALL_ACCESS,
            ADMIN_ALLOW_ALL_ACCESS,
            Permission(
                entity=TEST_CENTER,
                effect=Effect.ALLOW,
                actions=[Action.VIEW, Action.DOWNLOAD],
            ),
        ],
        user_permissions=[DENY_NO_ACCESS_USER],
    ),
    NO_METADATA_UUID: AnalysisPermissions(
        analysis_owner=TEST_USER_1,
        owner_type=EntityType.USER,
        role_permissions=[
            CEFS_ALLOW_ALL_ACCESS,
            ADMIN_ALLOW_ALL_ACCESS,
        ],
        user_permissions=[
            Permission(
                entity=TEST_USER_1,
                effect=Effect.ALLOW,
                actions=[Action.VIEW, Action.DOWNLOAD],
            ),
            DENY_NO_ACCESS_USER,
        ],
    ),
    NOT_AUTHORIZED_UUID: AnalysisPermissions(
        analysis_owner="admin",
        owner_type=EntityType.GROUP,
        role_permissions=[
            Permission(
                entity=CEFS,
                effect=Effect.DENY,
                actions=[Action.VIEW, Action.DOWNLOAD],
            ),
            Permission(
                entity=TEST_CENTER,
                effect=Effect.DENY,
                actions=[Action.VIEW, Action.DOWNLOAD],
            ),
        ],
        user_permissions=[
            DENY_NO_ACCESS_USER,
            Permission(
                entity=TEST_USER_1,
                effect=Effect.DENY,
                actions=[Action.VIEW, Action.DOWNLOAD],
            ),
        ],
    ),
    IN_PROGRESS_UUID: AnalysisPermissions(
        analysis_owner=TEST_CENTER,
        owner_type=EntityType.GROUP,
        role_permissions=[
            CEFS_ALLOW_ALL_ACCESS,
            ADMIN_ALLOW_ALL_ACCESS,
            Permission(
                entity=TEST_CENTER,
                effect=Effect.ALLOW,
                actions=[Action.VIEW, Action.DOWNLOAD],
            ),
        ],
        user_permissions=[
            DENY_NO_ACCESS_USER,
            Permission(
                entity=TEST_USER_1,
                effect=Effect.ALLOW,
                actions=[Action.VIEW, Action.DOWNLOAD],
            ),
        ],
    ),
    ANALYSIS_FAILED_UUID: AnalysisPermissions(
        analysis_owner=TEST_USER_1,
        owner_type=EntityType.USER,
        role_permissions=[
            CEFS_ALLOW_ALL_ACCESS,
            ADMIN_ALLOW_ALL_ACCESS,
            Permission(
                entity=TEST_CENTER,
                effect=Effect.ALLOW,
                actions=[Action.VIEW, Action.DOWNLOAD],
            ),
        ],
        user_permissions=[
            DENY_NO_ACCESS_USER,
            Permission(
                entity=TEST_USER_1,
                effect=Effect.ALLOW,
                actions=[Action.VIEW, Action.DOWNLOAD],
            ),
        ],
    ),
    FAMILIAL_FILE_PARSE_ERROR_UUID: AnalysisPermissions(
        analysis_owner=TEST_USER_1,
        owner_type=EntityType.USER,
        role_permissions=[CEFS_ALLOW_ALL_ACCESS, ADMIN_ALLOW_ALL_ACCESS],
        user_permissions=[
            Permission(
                entity=TEST_USER_1,
                effect=Effect.ALLOW,
                actions=[Action.VIEW, Action.DOWNLOAD],
            ),
        ],
    ),
}

MOCK_USER_ACCESS_CONTROL = {
    TEST_USER_1: Permission(
        entity=TEST_USER_1,
        effect=Effect.ALLOW,
        actions=[Action.VIEW, Action.DOWNLOAD, Action.CREATE],
    ),
    NO_ACCESS_USER: Permission(
        entity=TEST_USER_1,
        effect=Effect.DENY,
        actions=[Action.VIEW, Action.DOWNLOAD, Action.CREATE, Action.LIST_ALL],
    ),
}

MOCK_GROUP_ACCESS_CONTROL = {
    CEFS: Permission(
        entity=CEFS,
        effect=Effect.ALLOW,
        actions=[Action.VIEW, Action.DOWNLOAD, Action.CREATE, Action.LIST_ALL],
    ),
    TEST_CENTER: Permission(
        entity=TEST_CENTER,
        effect=Effect.ALLOW,
        actions=[Action.VIEW, Action.DOWNLOAD, Action.CREATE],
    ),
}

# format: {analysis_id: {user: {action: decision}}}
MOCK_RESOURCE_AUTH_CACHE: dict[str, dict[str, dict[Action, bool]]] = {}

# format: {username: {action: decision}}
MOCK_USER_AUTH_CACHE: dict[str, dict[Action, bool | None]] = {}


def login_user(username: str, password: str) -> Any:
    return keycloak_openid.token(username, password)


def get_user_roles(token: dict[Any, Any]) -> Any:
    return keycloak_openid.introspect(token["access_token"])["realm_access"]["roles"]


def logout_user(token: dict[Any, Any]) -> None:
    keycloak_openid.logout(token["refresh_token"])


def update_auth_cache(
    analysis_id: str, user: str, action: Action, decision: bool
) -> None:
    if analysis_id not in MOCK_RESOURCE_AUTH_CACHE:
        MOCK_RESOURCE_AUTH_CACHE[analysis_id] = {}

    if user not in MOCK_RESOURCE_AUTH_CACHE[analysis_id]:
        MOCK_RESOURCE_AUTH_CACHE[analysis_id][user] = {}

    MOCK_RESOURCE_AUTH_CACHE[analysis_id][user][action] = decision


def check_user_access(user: str, roles: list[str], action: Action) -> bool | None:
    # check if the decision has been "cached"
    if user in MOCK_USER_AUTH_CACHE and action in MOCK_USER_AUTH_CACHE[user]:
        return MOCK_USER_AUTH_CACHE[user][action]

    # if not, check the permissions the regular way and update the cache
    # this simulates calling to the auth server to check permissions
    permissions = MOCK_USER_ACCESS_CONTROL.get(user)

    decision = None

    for role in roles:
        role_permissions = MOCK_GROUP_ACCESS_CONTROL.get(role)
        if role_permissions is not None and action in role_permissions.actions:
            if role_permissions.effect == Effect.ALLOW:
                decision = True
            elif role_permissions.effect == Effect.DENY:
                decision = False

    if permissions is not None and action in permissions.actions:
        # user allow takes precedence over group deny
        if permissions.effect == Effect.ALLOW:
            decision = True
        elif permissions.effect == Effect.DENY:
            decision = False

    MOCK_USER_AUTH_CACHE[user] = {action: decision}
    return decision


def check_resource_access(
    user: str, roles: list[str], action: Action, analysis_id: str
) -> bool:
    # check if the decision has been "cached"
    if (
        analysis_id in MOCK_RESOURCE_AUTH_CACHE
        and user in MOCK_RESOURCE_AUTH_CACHE[analysis_id]
        and action in MOCK_RESOURCE_AUTH_CACHE[analysis_id][user]
    ):
        return MOCK_RESOURCE_AUTH_CACHE[analysis_id][user][action]

    # if not, check the permissions the regular way and update the cache
    # this simulates calling to the auth server to check permissions
    permissions = MOCK_RESOURCE_ACCESS_CONTROL.get(analysis_id)

    # implicit deny for resources that do not exist
    if permissions is None:
        update_auth_cache(analysis_id, user, action, False)
        return False

    # implicit allow for resource owners
    if permissions.analysis_owner == user:
        update_auth_cache(analysis_id, user, action, True)
        return True

    decision = False
    for role_permission in permissions.role_permissions:
        if role_permission.entity in roles and action in role_permission.actions:
            if role_permission.effect == Effect.ALLOW:
                decision = True
            # group deny takes precedence over user allow
            elif role_permission.effect == Effect.DENY:
                update_auth_cache(analysis_id, user, action, False)
                return False

    for user_permission in permissions.user_permissions:
        if user_permission.entity == user and action in user_permission.actions:
            if user_permission.effect == Effect.ALLOW:
                decision = True
            # user deny takes precedence over group allow
            elif user_permission.effect == Effect.DENY:
                update_auth_cache(analysis_id, user, action, False)
                return False

    update_auth_cache(analysis_id, user, action, decision)
    return decision


def check_view_access(user: str, roles: list[str], analysis_id: str) -> bool:
    resource_access = check_resource_access(user, roles, Action.VIEW, analysis_id)
    user_access = check_user_access(user, roles, Action.VIEW)

    return resource_access and (user_access is None or user_access)


def check_download_access(user: str, roles: list[str], analysis_id: str) -> bool:
    resource_access = check_resource_access(user, roles, Action.DOWNLOAD, analysis_id)
    user_access = check_user_access(user, roles, Action.DOWNLOAD)

    return resource_access and (user_access is None or user_access)


def check_create_access(user: str, roles: list[str]) -> bool:
    user_access = check_user_access(user, roles, Action.CREATE)
    if user_access is not None:
        return user_access
    return False


def check_list_all_access(user: str, roles: list[str]) -> bool:
    user_access = check_user_access(user, roles, Action.LIST_ALL)
    if user_access is not None:
        return user_access
    return False
