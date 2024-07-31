"""Contains the models for the permissions that can be assigned to users and groups for a given analysis and action."""

from enum import StrEnum


class Action(StrEnum):
    """The actions that can be performed on an analysis."""

    CREATE = "CREATE"
    VIEW = "VIEW"
    DOWNLOAD = "DOWNLOAD"
    LIST_ALL = "LIST_ALL"


class Effect(StrEnum):
    """The effect of a permission. Can be ALLOW or DENY."""

    ALLOW = "ALLOW"
    DENY = "DENY"


class EntityType(StrEnum):
    """The type of entity that owns the analysis. Can be GROUP or USER."""

    GROUP = "GROUP"
    USER = "USER"


class Permission:
    """A permission that can be assigned to a user or group for a given action."""

    def __init__(self, entity: str, effect: Effect, actions: list[Action]):
        self.entity = entity
        self.effect = effect
        self.actions = actions


class AnalysisPermissions:
    """The permissions that can be assigned to users and groups for a given analysis."""

    def __init__(
        self,
        analysis_owner: str,
        owner_type: EntityType,
        role_permissions: list[Permission] | None = None,
        user_permissions: list[Permission] | None = None,
    ):
        self.analysis_owner = analysis_owner
        self.owner_type = owner_type
        self.role_permissions = role_permissions if role_permissions else []
        self.user_permissions = user_permissions if user_permissions else []
