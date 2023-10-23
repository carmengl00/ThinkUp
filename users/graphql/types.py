import strawberry

@strawberry.type
class CustomUserType:
    id: strawberry.ID
    email: str
    username: str

@strawberry.type
class FollowRequestType:
    id: strawberry.ID
    requester: CustomUserType
    required: CustomUserType

@strawberry.type
class FollowsType:
    follower: CustomUserType
    followed: CustomUserType
