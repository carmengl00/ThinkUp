import strawberry

from typing import List
from base.graphql.inputs import PaginationInput
from base.graphql.utils import get_paginator
from users.graphql.types import CustomUserType, FollowRequestType, PaginatedCustomUserType
from users.models import CustomUser, FollowRequest, Follows
from strawberry.types import Info
from base.decorators import login_required

@strawberry.type
class UsersQuery:
    @strawberry.field
    def users(self) -> List[CustomUserType]:
        return CustomUser.objects.all()


    @strawberry.field
    @login_required
    def my_follow_request(self, info: Info) -> List[FollowRequestType]:
        user = info.context.request.user
        im_requester = FollowRequest.objects.filter(requester = user)
        im_required = FollowRequest.objects.filter(required = user)
        
        lista = list(im_requester) + list(im_required)

        return lista


    @strawberry.field
    @login_required
    def my_followers(self, info: Info) -> List[CustomUserType]:
        user = info.context.request.user
        followers = Follows.objects.filter(followed = user)
        return [f.follower for f in followers]
        

    @strawberry.field
    @login_required
    def my_followed(self, info: Info) -> List[CustomUserType]:
        user = info.context.request.user
        following = Follows.objects.filter(follower = user)
        return [f.followed for f in following]


    @strawberry.field
    @login_required
    def search_user(self, username: str, info: Info, pagination: PaginationInput) -> PaginatedCustomUserType:
        user = info.context.request.user
        user_list = CustomUser.objects.filter(username__icontains = username).exclude(username = user.username)
        
        return get_paginator(
            user_list, pagination.page_size, pagination.page, PaginatedCustomUserType
        )
