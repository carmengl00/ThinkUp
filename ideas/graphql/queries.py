import strawberry

from typing import List
from gqlauth.user.queries import UserQueries
from base.graphql.inputs import PaginationInput
from base.graphql.utils import get_paginator
from ideas.graphql.types import IdeaType, NotificationsType, PaginatedIdeaType
from ideas.models import Notification, Idea
from ideas.utils import ideas_user_aux
from users.models import CustomUser, Follows
from strawberry.types import Info
from gqlauth.core.utils import get_user
from uuid import UUID

@strawberry.type
class IdeasQuery(UserQueries):
    @strawberry.field
    def my_ideas(info: Info, pagination: PaginationInput) -> PaginatedIdeaType:
        user = get_user(info)
        sorted_list = Idea.objects.filter(user=user).order_by('-created_at')

        results = get_paginator(
            sorted_list, pagination.page_size, pagination.page, PaginatedIdeaType
        )

        return results


    @strawberry.field
    def ideas_user(uuid: UUID, info: Info, pagination: PaginationInput) -> PaginatedIdeaType:
        user_authenticated = get_user(info)
        target_user = CustomUser.objects.get(uuid = uuid)

        lista = ideas_user_aux(user_authenticated, target_user)

        results = get_paginator(
            lista, pagination.page_size, pagination.page, PaginatedIdeaType
        )

        return results


    @strawberry.field
    def timeline(self, info: Info, pagination: PaginationInput) -> PaginatedIdeaType:
        user = get_user(info)
        following = Follows.objects.filter(follower = user)
        my_ideas = Idea.objects.filter(user = user)
        lista = list(my_ideas)
        for f in following:
            lista += ideas_user_aux(user, f.followed)

        sorted_list = Idea.objects.filter(id__in=[idea.id for idea in lista]).order_by('-created_at')

        results = get_paginator(
            sorted_list, pagination.page_size, pagination.page, PaginatedIdeaType
        )

        return results


    @strawberry.field
    def my_notifications(info: Info) -> List[NotificationsType]:
        user = get_user(info)
        return Notification.objects.filter(user = user)
