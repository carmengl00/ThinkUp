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
class FollowRequest:
    id: strawberry.ID
    requester: CustomUser
    required: CustomUser
    status: str

@strawberry.type
class Follows:
    follower: CustomUser
    followed: CustomUser

@strawberry.type
class Notifications:
    id: strawberry.ID
    idea: Idea
    user: CustomUser

@strawberry.type
class Query(UserQueries):
    @strawberry.field
    def users(self) -> List[CustomUser]:
        return get_user_model().objects.all()
    
    my_ideas: List[Idea] = strawberry.field(my_ideas)
    
    my_follow_request: List[FollowRequest] = strawberry.field(my_follow_request)
    my_followers: List[CustomUser] = strawberry.field(my_followers)
    my_followed: List[CustomUser] = strawberry.field(my_followed)
    search_user: List[CustomUser] = strawberry.field(search_user)
    
    ideas_user: List[Idea] = strawberry.field(ideas_user)
    timeline: List[Idea] = strawberry.field(timeline)

    my_notifications: List[Notifications] = strawberry.field(my_notifications)
    

@strawberry.type
class Mutation:
    register_user: CustomUser = strawberry.mutation(register_user)
    
    token_auth = mutations.ObtainJSONWebToken.field
    verify_token = mutations.VerifyToken.field

    password_change = mutations.PasswordChange.field
    send_password_reset_email = mutations.SendPasswordResetEmail.field

    create_idea: Idea = strawberry.mutation(create_idea)
    update_visibility_idea: Idea = strawberry.mutation(update_visibility_idea)
    delete_idea: bool = strawberry.mutation(delete_idea)

    follow_request: FollowRequest = strawberry.mutation(follow_request)
    approve_follow_request: Follows = strawberry.mutation(approve_follow_request)
    reject_follow_request: bool = strawberry.mutation(reject_follow_request)
    unfollow: bool = strawberry.mutation(unfollow)
    delete_follower: bool = strawberry.mutation(delete_follower)
    

schema = JwtSchema(query=Query, mutation=Mutation)