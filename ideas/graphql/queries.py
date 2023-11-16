import strawberry

from typing import List
from base.graphql.inputs import PaginationInput
from base.graphql.utils import get_paginator
from ideas.graphql.types import PaginatedIdeaType, PaginatedNotificationType
from ideas.models import Notification, Idea
from ideas.utils import ideas_user_aux
from users.models import CustomUser, Follows
from strawberry.types import Info
from uuid import UUID
from base.decorators import login_required

@strawberry.type
class IdeasQuery:
    @strawberry.field
    @login_required
    def my_ideas(self, info: Info, pagination: PaginationInput) -> PaginatedIdeaType:
        user = info.context.request.user
        sorted_list = Idea.objects.filter(user=user).order_by('-created_at')

        return get_paginator(
            sorted_list, pagination.page_size, pagination.page, PaginatedIdeaType
        )


    @strawberry.field
    @login_required
    def ideas_user(self, id: UUID, info: Info, pagination: PaginationInput) -> PaginatedIdeaType:
        user_authenticated = info.context.request.user
        target_user = CustomUser.objects.get(id = id)

        lista = ideas_user_aux(user_authenticated, target_user)

        return get_paginator(
            lista, pagination.page_size, pagination.page, PaginatedIdeaType
        )


    @strawberry.field
    @login_required
    def timeline(self, info: Info, pagination: PaginationInput) -> PaginatedIdeaType:
        user = info.context.request.user
        following = Follows.objects.filter(follower = user)
        my_ideas = Idea.objects.filter(user = user)
        lista = list(my_ideas)
        for f in following:
            lista += ideas_user_aux(user, f.followed)

        sorted_list = Idea.objects.filter(id__in=[idea.id for idea in lista]).order_by('-created_at')

        return get_paginator(
            sorted_list, pagination.page_size, pagination.page, PaginatedIdeaType
        )


    @strawberry.field
    @login_required
    def my_notifications(self, info: Info, pagination: PaginationInput) -> PaginatedNotificationType:
        user = info.context.request.user
        lista = Notification.objects.filter(user = user)

        return get_paginator(
            lista, pagination.page_size, pagination.page, PaginatedNotificationType
        )

    @strawberry.field
    def stash3(self):
        return "stash3"
    
    @strawberry.field
    def mensaje_commit(self):
        return "mensaje_commit"
    