import strawberry

from typing import List
from gqlauth.user.queries import UserQueries
from users.graphql.types import CustomUserType, FollowRequestType
from users.graphql.resolvers import *

@strawberry.type
class UsersQuery(UserQueries):
    users: List[CustomUserType] = strawberry.field(resolver = users)
    my_follow_request: List[FollowRequestType] = strawberry.field(resolver = my_follow_request)
    my_followers: List[CustomUserType] = strawberry.field(resolver = my_followers)
    my_followed: List[CustomUserType] = strawberry.field(resolver = my_followed)
    search_user: List[CustomUserType] = strawberry.field(resolver = search_user)
