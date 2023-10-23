import strawberry
from gqlauth.user import arg_mutations as mutations
from users.graphql.types import CustomUserType, FollowRequestType, FollowsType
from users.graphql.resolvers import *

@strawberry.type
class UserMutation:
    register_user: CustomUserType = strawberry.mutation(register_user)
    
    token_auth = mutations.ObtainJSONWebToken.field
    verify_token = mutations.VerifyToken.field

    password_change = mutations.PasswordChange.field
    send_password_reset_email = mutations.SendPasswordResetEmail.field

    follow_request: FollowRequestType = strawberry.mutation(follow_request)
    approve_follow_request: FollowsType = strawberry.mutation(approve_follow_request)
    reject_follow_request: FollowsType = strawberry.mutation(reject_follow_request)

    unfollow: bool = strawberry.mutation(unfollow)
    delete_follower: bool = strawberry.mutation(delete_follower)
    