import strawberry
#import mutations and queries from ideas and users
from users.graphql.mutations import UserMutation
from ideas.graphql.mutations import IdeasMutation
from users.graphql.queries import UsersQuery
from ideas.graphql.queries import IdeasQuery
from base.middleware import AuthenticationMiddleware

@strawberry.type
class Query(
    UsersQuery,
    IdeasQuery,
):
    pass

@strawberry.type
class Mutation(
    UserMutation,
    IdeasMutation,
):
    pass
    
extensions = [
    AuthenticationMiddleware,
]

schema = strawberry.Schema(query=Query, mutation=Mutation, extensions=extensions)