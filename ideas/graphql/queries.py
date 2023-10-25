import strawberry

from typing import List
from gqlauth.user.queries import UserQueries
from ideas.graphql.types import IdeaType, NotificationsType
from ideas.models import Notification, Idea
from ideas.utils import ideas_user_aux
from users.models import Follows
from ideas.graphql.types import VisibilityEnum
from strawberry.types import Info
from django.contrib.auth import get_user_model
from gqlauth.core.utils import get_user

@strawberry.type
class IdeasQuery(UserQueries):
    @strawberry.field
    def my_ideas(info: Info) -> List[IdeaType]:
        user = get_user(info)
        sorted_list = Idea.objects.filter(user=user).order_by('-created_at')
        return sorted_list


    @strawberry.field
    def ideas_user(username: str, info: Info) -> List[IdeaType]:
        return ideas_user_aux(username, info)


    @strawberry.field
    def timeline(self, info: Info) -> List[IdeaType]:
        user = get_user(info)
        following = Follows.objects.filter(follower = user)
        my_ideas = Idea.objects.filter(user = user)
        lista = list(my_ideas)
        for f in following:
            lista += ideas_user_aux(f.followed.username, info)

        sorted_list = Idea.objects.filter(id__in=[idea.id for idea in lista]).order_by('-created_at')
        return sorted_list


    @strawberry.field
    def my_notifications(info: Info) -> List[NotificationsType]:
        user = get_user(info)
        return Notification.objects.filter(user = user)
