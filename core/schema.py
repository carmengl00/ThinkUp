from typing import List
import strawberry
from .resolvers import *
from gqlauth.user import arg_mutations as mutations
from gqlauth.user.queries import UserQueries
from gqlauth.core.middlewares import JwtSchema

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
class Query(UserQueries):
    @strawberry.field
    def users(self) -> List[CustomUser]:
        return get_user_model().objects.all()

@strawberry.type
class Mutation:
    register_user: CustomUser = strawberry.mutation(register_user)
    
    token_auth = mutations.ObtainJSONWebToken.field
    verify_token = mutations.VerifyToken.field

    password_change = mutations.PasswordChange.field

schema = JwtSchema(query=Query, mutation=Mutation)