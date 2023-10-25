from typing import List
from ideas.graphql.types import IdeaType
from ideas.models import Idea
from users.models import Follows
from ideas.graphql.types import VisibilityEnum
from strawberry.types import Info
from django.contrib.auth import get_user_model
from gqlauth.core.utils import get_user

def ideas_user_aux(username: str, info: Info) -> List[IdeaType]:
    user = get_user(info)
    followed = get_user_model().objects.get(username = username)
    follow = Follows.objects.filter(follower = user, followed = followed)
    protected_ideas = []
    private_ideas = []
    if follow:
        protected_ideas = Idea.objects.filter(user = followed, visibility = VisibilityEnum.PROTECTED)
    
    if followed == user:
        private_ideas = Idea.objects.filter(user = followed, visibility = VisibilityEnum.PRIVATE)
        protected_ideas = Idea.objects.filter(user = followed, visibility = VisibilityEnum.PROTECTED)
        
    public_ideas = Idea.objects.filter(user = followed, visibility = VisibilityEnum.PUBLIC)
    lista = list(public_ideas) + list(protected_ideas) + list(private_ideas)
    return lista