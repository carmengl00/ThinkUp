import strawberry

from typing import List
from gqlauth.user.queries import UserQueries
from ideas.graphql.types import IdeaType, NotificationsType
from .resolvers import *


@strawberry.type
class IdeasQuery(UserQueries):
    my_ideas: List[IdeaType] = strawberry.field(resolver = my_ideas)
    ideas_user: List[IdeaType] = strawberry.field(resolver = ideas_user)
    timeline: List[IdeaType] = strawberry.field(resolver = timeline)
    notifications: List[NotificationsType] = strawberry.field(resolver = my_notifications)