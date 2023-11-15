import strawberry
from base.graphql.types import PaginatedQueryType
from ideas.models import VisibilityType
from users.graphql.types import CustomUserType
import uuid

VisibilityEnum = strawberry.enum(VisibilityType)

@strawberry.type
class IdeaType:
    id: uuid.UUID
    text: str
    created_at: str
    updated_at: str
    visibility: VisibilityEnum
    user: CustomUserType

@strawberry.type
class NotificationsType:
    id: uuid.UUID
    idea: IdeaType
    user: CustomUserType

@strawberry.type
class PaginatedIdeaType(PaginatedQueryType):
    edges: list[IdeaType]

@strawberry.type
class PaginatedNotificationType(PaginatedQueryType):
    edges: list[NotificationsType]