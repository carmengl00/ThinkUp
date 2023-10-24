import strawberry
from ideas.models import VisibilityType
from users.graphql.types import CustomUserType

VisibilityEnum = strawberry.enum(VisibilityType)

@strawberry.type
class IdeaType:
    id: strawberry.ID
    text: str
    created_at: str
    updated_at: str
    visibility: VisibilityEnum
    user: CustomUserType

@strawberry.type
class NotificationsType:
    id: strawberry.ID
    idea: IdeaType
    user: CustomUserType
