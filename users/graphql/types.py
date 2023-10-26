import strawberry
import uuid

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
