import strawberry
from users.graphql.types import CustomUserType

@strawberry.type
class IdeaType:
    id: strawberry.ID
    text: str
    created_at: str
    updated_at: str
    visibility: str
    user_id: int

@strawberry.type
class NotificationsType:
    id: strawberry.ID
    idea: IdeaType
    user: CustomUserType
