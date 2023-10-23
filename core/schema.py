import strawberry
from gqlauth.core.middlewares import JwtSchema
#import mutations and queries from ideas and users
from users.graphql.mutations import UserMutation
from ideas.graphql.mutations import IdeasMutation
from users.graphql.queries import UsersQuery
from ideas.graphql.queries import IdeasQuery

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
    

schema = JwtSchema(query=Query, mutation=Mutation)