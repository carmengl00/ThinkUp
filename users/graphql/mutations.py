from django.forms import ValidationError
import strawberry
from base.jwt import create_access_token, create_refresh_token
from users.graphql.inputs import ChangePasswordInput, LoginInput
from users.graphql.types import CustomUserType, FollowRequestType, FollowsType, UserTypeWeb
from users.models import FollowRequest, Follows, CustomUser
from strawberry.types import Info
from users.password_validator import PasswordValidator
from django.contrib.auth import authenticate
from django.utils import timezone

from base.decorators import login_required

@strawberry.type
class UserMutation:

    @strawberry.field
    def register_user(username: str, email: str, password: str) -> CustomUserType:

        password_validator = PasswordValidator(
            passwords=["password", "password1", "password2", "p@ssw0rd", "common_password1", "common_password2"],
        )

        password_validator.validate(password)
        user = CustomUser.objects._create_user(username=username, email=email, password=password)
        return user
    
    @strawberry.mutation
    def login(self, info: Info, input: LoginInput) -> UserTypeWeb:
        user = authenticate(
            request=info.context.request,
            username=input.email,
            password=input.password,
        )
        if not user:
            raise ValueError("Invalid email or password")
        
        access_token = create_access_token(user)
        refresh_token = create_refresh_token(user)
        user.last_login = timezone.now()
        user.save(update_fields=["last_login"])
        return UserTypeWeb(
            user=user,
            token=access_token,
            refresh_token=refresh_token,
        )
    
    
    @strawberry.mutation
    @login_required
    def change_password(self, info: Info, input: ChangePasswordInput) -> CustomUserType:
        print(getattr(info.context.request, "user", None))

        user = info.context.request.user
        print(info.context)
        print(user)
        if not user:
            raise Exception(
                "You must be logged in to change your password.",
            )
        if not user.check_password(input.current_password):
            raise Exception(
                "The current password is incorrect.",
            )
        if (
            input.password
            and input.repeat_password
            and input.password != input.repeat_password
        ):
            raise Exception(
                "The two password fields didn't match.",
            )
        try:
            password_validator = PasswordValidator(
                passwords=["password", "password1", "password2", "p@ssw0rd", "common_password1", "common_password2"],
            )
            password_validator.validate(input.password)
        except ValidationError as e:
            raise Exception(str(e).replace("['", "").replace("']", ""))
        user.set_password(input.password)
        user.save(update_fields=["password"])
        return user

    @strawberry.field
    @login_required
    def follow_request(self, required_username: str, info: Info) -> FollowRequestType:
        requester = info.context.request.user
        required = CustomUser.objects.get(username = required_username)
        return FollowRequest.objects.create_request(requester = requester, required = required)


    @strawberry.field
    @login_required
    def approve_follow_request(self, id: int, info: Info) -> FollowsType:
        user = info.context.request.user
        request = FollowRequest.objects.get(id = id, required = user)
        request.delete()
        return Follows.objects.create(follower = request.requester, followed = request.required)


    @strawberry.field
    @login_required
    def reject_follow_request(self, id: int, info: Info) -> bool:
        user = info.context.request.user
        request = FollowRequest.objects.get(id = id, required = user)
        request.delete()
        return True


    @strawberry.field
    @login_required
    def unfollow(self, username: str, info: Info) -> bool:
        user = info.context.request.user
        followed = CustomUser.objects.get(username = username)
        follow = Follows.objects.filter(follower = user, followed = followed)
        if follow.exists():
            follow.delete()
        else:
            raise ValueError('You are not following this user')
        return True


    @strawberry.field
    @login_required
    def delete_follower(self, username: str, info: Info) -> bool:
        user = info.context.request.user
        follower = CustomUser.objects.get(username = username)
        follow = Follows.objects.filter(follower = follower, followed = user)
        if follow.exists():
            follow.delete()
        else:
            raise ValueError('This user is not following you')
        return True
        