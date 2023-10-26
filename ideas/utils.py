from typing import List
from ideas.graphql.types import IdeaType
from ideas.models import Idea
from users.models import CustomUser, Follows
from ideas.graphql.types import VisibilityEnum

def ideas_user_aux(user_authenticated: CustomUser, target_user: CustomUser) -> List[IdeaType]:
    lista = []
    if user_authenticated == target_user:
        lista = Idea.objects.filter(user = target_user)
    elif Follows.objects.filter(follower = user_authenticated, followed = target_user).exists():
        lista = Idea.objects.filter(user = target_user, visibility__in = [VisibilityEnum.PUBLIC, VisibilityEnum.PROTECTED])
    else:
        lista = Idea.objects.filter(user = target_user, visibility = VisibilityEnum.PUBLIC)
    return lista.order_by('-created_at')