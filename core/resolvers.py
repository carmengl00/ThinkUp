from users.models import CustomUser
from django.contrib.auth import get_user_model
from gqlauth.models import UserStatus

def register_user(username: str, email: str, password: str) -> CustomUser:
    CustomUser = get_user_model()
    user = CustomUser.objects._create_user(username = username, email = email, password = password)

    status: "UserStatus" = getattr(user, "status")
    status.verified = True
    status.save()

    return user