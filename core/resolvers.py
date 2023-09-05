from typing import List
from users.models import CustomUser
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