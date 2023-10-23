from typing import List
from django.contrib.auth import get_user_model
from gqlauth.core.utils import get_user
from strawberry.types import Info
from users.password_validator import PasswordValidator
from users.models import Follows, FollowRequest, CustomUser
from gqlauth.models import UserStatus

# Queries
def users(self) -> List[CustomUser]:
    return get_user_model().objects.all()

def my_follow_request(info: Info) -> List[FollowRequest]:
    user = get_user(info)
    im_requester = FollowRequest.objects.filter(requester = user)
    im_required = FollowRequest.objects.filter(required = user)
    
    lista = list(im_requester) + list(im_required)

    return lista

def my_followers(info: Info) -> List[CustomUser]:
    user = get_user(info)
    followers = Follows.objects.filter(followed = user)
    return [f.follower for f in followers]
    
def my_followed(info: Info) -> List[CustomUser]:
    user = get_user(info)
    following = Follows.objects.filter(follower = user)
    return [f.followed for f in following]

def search_user(username: str, info: Info) -> List[CustomUser]:
    user = get_user(info)
    return get_user_model().objects.filter(username__icontains = username).exclude(username = user.username)

# Mutations
def register_user(username: str, email: str, password: str) -> CustomUser:
    CustomUser = get_user_model()

    password_validator = PasswordValidator(
        passwords=["password", "password1", "password2", "p@ssw0rd", "common_password1", "common_password2"],
    )

    password_validator.validate(password)

    user = CustomUser.objects._create_user(username=username, email=email, password=password)

    status: "UserStatus" = getattr(user, "status")
    status.verified = True
    status.save()

    return user


def follow_request(required_username: str, info: Info) -> FollowRequest:
    requester = get_user(info)
    required = get_user_model().objects.get(username = required_username)
    return FollowRequest.objects.create_request(requester = requester, required = required)

def approve_follow_request(id: int, info: Info) -> Follows:
    user = get_user(info)
    request = FollowRequest.objects.get(id = id, required = user)
    request.delete()
    return Follows.objects.create(follower = request.requester, followed = request.required)

def reject_follow_request(id: int, info: Info) -> bool:
    user = get_user(info)
    request = FollowRequest.objects.get(id = id, required = user)
    request.delete()
    return True

def unfollow(username: str, info: Info) -> bool:
    user = get_user(info)
    followed = get_user_model().objects.get(username = username)
    follow = Follows.objects.filter(follower = user, followed = followed)
    if follow.exists():
        follow.delete()
    else:
        raise ValueError('You are not following this user')
    return True

def delete_follower(username: str, info: Info) -> bool:
    user = get_user(info)
    follower = get_user_model().objects.get(username = username)
    follow = Follows.objects.filter(follower = follower, followed = user)
    if follow.exists():
        follow.delete()
    else:
        raise ValueError('This user is not following you')
    return True