import strawberry
import uuid

from base.graphql.types import PaginatedQueryType

@strawberry.type
class CustomUserType:
    uuid: uuid.UUID
    email: str
    username: str

@strawberry.type
class FollowRequestType:
    uuid: uuid.UUID
    requester: CustomUserType
    required: CustomUserType

@strawberry.type
class FollowsType:
    uuid: uuid.UUID
    follower: CustomUserType
    followed: CustomUserType

@strawberry.type
class PaginatedCustomUserType(PaginatedQueryType):
    edges: list[CustomUserType]
