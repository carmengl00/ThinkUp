import strawberry

from typing import List
from gqlauth.user.queries import UserQueries
from base.graphql.inputs import PaginationInput
from base.graphql.utils import get_paginator
from users.graphql.types import CustomUserType, FollowRequestType, PaginatedCustomUserType
from users.models import CustomUser, FollowRequest, Follows
from strawberry.types import Info
from gqlauth.core.utils import get_user

@strawberry.type
class UsersQuery(UserQueries):
    @strawberry.field
    def users(self) -> List[CustomUserType]:
        return CustomUser.objects.all()


    @strawberry.field
    def my_follow_request(info: Info) -> List[FollowRequestType]:
        user = get_user(info)
        im_requester = FollowRequest.objects.filter(requester = user)
        im_required = FollowRequest.objects.filter(required = user)
        
        lista = list(im_requester) + list(im_required)

        return lista


    @strawberry.field
    def my_followers(info: Info) -> List[CustomUserType]:
        user = get_user(info)
        followers = Follows.objects.filter(followed = user)
        return [f.follower for f in followers]
        

    @strawberry.field
    def my_followed(info: Info) -> List[CustomUserType]:
        user = get_user(info)
        following = Follows.objects.filter(follower = user)
        return [f.followed for f in following]


    @strawberry.field
    def search_user(username: str, info: Info, pagination: PaginationInput) -> PaginatedCustomUserType:
        user = get_user(info)
        user_list = CustomUser.objects.filter(username__icontains = username).exclude(username = user.username)

        results = get_paginator(
            user_list, pagination.page_size, pagination.page, PaginatedCustomUserType
        )

        return results
