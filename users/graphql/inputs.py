import strawberry

@strawberry.input
class LoginInput:
    email: str
    password: str

@strawberry.input
class ChangePasswordInput:
    current_password: str
    password: str
    repeat_password: str | None