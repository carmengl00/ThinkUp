import strawberry

from gqlauth.core.utils import get_user
from strawberry.types import Info
from ideas.graphql.types import IdeaType
from .resolvers import *

@strawberry.type
class IdeasMutation:
    create_idea: IdeaType = strawberry.mutation(resolver = create_idea)
    update_visibility_idea: IdeaType = strawberry.mutation(resolver = update_visibility_idea)
    delete_idea: bool = strawberry.mutation(resolver = delete_idea)