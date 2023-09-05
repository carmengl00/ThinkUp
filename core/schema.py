from typing import List
import strawberry
from .resolvers import *

@strawberry.type
class Idea:
    id: strawberry.ID
    text: str
    created_at: str
    updated_at: str
    visibility: str
    user_id: int

@strawberry.type
class CustomUser:
    id: strawberry.ID
    email: str
    username: str
    password: str

@strawberry.type
class Query:
    @strawberry.field
    def user(self) -> List[CustomUser]:
        return get_user_model().objects.all()

@strawberry.type
class Mutation:
    register_user: CustomUser = strawberry.mutation(register_user)

schema = strawberry.Schema(query=Query, mutation=Mutation)