import strawberry
from gqlauth.user import arg_mutations as mutations
from users.graphql.types import CustomUserType, FollowRequestType, FollowsType
from users.models import FollowRequest, Follows, CustomUser
from strawberry.types import Info
from django.contrib.auth import get_user_model
from gqlauth.core.utils import get_user
from users.password_validator import PasswordValidator
from gqlauth.models import UserStatus

@strawberry.type
class UserMutation:

    token_auth = mutations.ObtainJSONWebToken.field
    verify_token = mutations.VerifyToken.field

    password_change = mutations.PasswordChange.field
    send_password_reset_email = mutations.SendPasswordResetEmail.field

    @strawberry.field
    def register_user(username: str, email: str, password: str) -> CustomUserType:
        CustomUser = get_user_model()

        password_validator = PasswordValidator(
            passwords=["password", "password1", "password2", "p@ssw0rd", "common_password1", "common_password2"],
        )

        password_validator.validate(password)

        user = CustomUser.objects._create_user(username=username, email=email, password=password)

        status: "UserStatus" = getattr(user, "status")
        status.verified = True
        status.save()

        return user


    @strawberry.field
    def follow_request(required_username: str, info: Info) -> FollowRequestType:
        requester = get_user(info)
        required = get_user_model().objects.get(username = required_username)
        return FollowRequest.objects.create_request(requester = requester, required = required)


    @strawberry.field
    def approve_follow_request(id: int, info: Info) -> FollowsType:
        user = get_user(info)
        request = FollowRequest.objects.get(id = id, required = user)
        request.delete()
        return Follows.objects.create(follower = request.requester, followed = request.required)


    @strawberry.field
    def reject_follow_request(id: int, info: Info) -> bool:
        user = get_user(info)
        request = FollowRequest.objects.get(id = id, required = user)
        request.delete()
        return True


    @strawberry.field
    def unfollow(username: str, info: Info) -> bool:
        user = get_user(info)
        followed = get_user_model().objects.get(username = username)
        follow = Follows.objects.filter(follower = user, followed = followed)
        if follow.exists():
            follow.delete()
        else:
            raise ValueError('You are not following this user')
        return True


    @strawberry.field
    def delete_follower(username: str, info: Info) -> bool:
        user = get_user(info)
        follower = get_user_model().objects.get(username = username)
        follow = Follows.objects.filter(follower = follower, followed = user)
        if follow.exists():
            follow.delete()
        else:
            raise ValueError('This user is not following you')
        return True
        