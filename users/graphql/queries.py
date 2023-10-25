import strawberry

from typing import List
from gqlauth.user.queries import UserQueries
from users.graphql.types import CustomUserType, FollowRequestType
from users.models import FollowRequest, Follows
from strawberry.types import Info
from django.contrib.auth import get_user_model
from gqlauth.core.utils import get_user

@strawberry.type
class UsersQuery(UserQueries):
    @strawberry.field
    def users(self) -> List[CustomUserType]:
        return get_user_model().objects.all()


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
    def search_user(username: str, info: Info) -> List[CustomUserType]:
        user = get_user(info)
        return get_user_model().objects.filter(username__icontains = username).exclude(username = user.username)
