import strawberry
from ideas.models import VisibilityType
from users.graphql.types import CustomUserType
import uuid

VisibilityEnum = strawberry.enum(VisibilityType)

@strawberry.type
class IdeaType:
    uuid: uuid.UUID
    text: str
    created_at: str
    updated_at: str
    visibility: VisibilityEnum
    user: CustomUserType

@strawberry.type
class NotificationsType:
    uuid: uuid.UUID
    idea: IdeaType
    user: CustomUserType