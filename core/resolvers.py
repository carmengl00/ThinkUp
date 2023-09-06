from typing import List
from users.models import CustomUser, FollowRequest, Follows
from django.contrib.auth import get_user_model
from gqlauth.models import UserStatus
from ideas.models import Idea
from gqlauth.core.utils import get_user
from strawberry.types import Info

def register_user(username: str, email: str, password: str) -> CustomUser:
    CustomUser = get_user_model()
    user = CustomUser.objects._create_user(username = username, email = email, password = password)

    status: "UserStatus" = getattr(user, "status")
    status.verified = True
    status.save()

    return user

def create_idea(text: str, visibility: str, info: Info) -> Idea:
    user = get_user(info)
    idea = Idea.objects.create(text = text, visibility = visibility, user = user)
    return idea

def update_visibility_idea(id: int, visibility: str, info: Info) -> Idea:
    user = get_user(info)
    idea = Idea.objects.get(id = id, user = user)
    idea.visibility = visibility
    idea.save()
    return idea

def my_ideas(info: Info) -> List[Idea]:
    user = get_user(info)
    return Idea.objects.filter(user = user)

def delete_idea(id: int, info: Info) -> bool:
    user = get_user(info)
    idea = Idea.objects.get(id = id, user = user)
    idea.delete()
    return True

def follow_request(required_username: str, info: Info) -> FollowRequest:
    requester = get_user(info)
    required = get_user_model().objects.get(username = required_username)
    return FollowRequest.objects.create_request(requester = requester, required = required)

def my_follow_request(info: Info) -> List[FollowRequest]:
    user = get_user(info)
    im_requester = FollowRequest.objects.filter(requester = user)
    im_required = FollowRequest.objects.filter(required = user)
    
    lista = list(im_requester) + list(im_required)
    
    return lista