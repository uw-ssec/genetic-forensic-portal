from enum import StrEnum


class Action(StrEnum):
    CREATE = "CREATE"
    VIEW = "VIEW"
    DOWNLOAD = "DOWNLOAD"
    LIST_ALL = "LIST_ALL"


class Effect(StrEnum):
    ALLOW = "ALLOW"
    DENY = "DENY"


class EntityType(StrEnum):
    GROUP = "GROUP"
    USER = "USER"


class Permission:
    def __init__(self, entity: str, effect: Effect, actions: list[Action]):
        self.entity = entity
        self.effect = effect
        self.actions = actions


class AnalysisPermissions:
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
