import strawberry
import uuid

from base.graphql.types import PaginatedQueryType

@strawberry.type
class CustomUserType:
    id: uuid.UUID
    email: str
    username: str

@strawberry.type
class FollowRequestType:
    id: uuid.UUID
    requester: CustomUserType
    required: CustomUserType

@strawberry.type
class FollowsType:
    id: uuid.UUID
    follower: CustomUserType
    followed: CustomUserType

@strawberry.type
class PaginatedCustomUserType(PaginatedQueryType):
    edges: list[CustomUserType]

@strawberry.type
class UserTypeWeb:
    user: CustomUserType
    token: str
    refresh_token: str