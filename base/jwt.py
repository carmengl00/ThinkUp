from core import settings
from datetime import timedelta, datetime
from typing import Any

import jwt

from users.models import CustomUser

JWT_ACCESS_TYPE = "access"
JWT_REFRESH_TYPE = "refresh"

def jwt_base_payload(exp_delta: timedelta | None) -> dict[str, Any]:
    utc_now = datetime.utcnow()
    payload = {"iat": utc_now}
    if exp_delta:
        payload["exp"] = utc_now + exp_delta
    return payload

def jwt_user_payload(
    user: CustomUser,
    token_type: str,
    exp_delta: timedelta | None,
) -> dict[str, Any]:
    payload = jwt_base_payload(exp_delta)
    payload.update(
        {
            "token": user.jwt_token_key,
            "email": user.email,
            "type": token_type,
            "user_id": str(user.id),
        }
    )
    return payload

def jwt_encode(payload: dict[str, Any]) -> str:
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

def jwt_decode(token: dict[str, Any], verify_expiration=True) -> str:
    return jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=["HS256"],
        options={"verify_exp": verify_expiration},
    )

def create_access_token(
    user: CustomUser, access_token_expires=settings.JWT_EXPIRE, override_ttl=None
) -> str:
    payload = jwt_user_payload(
        user,
        JWT_ACCESS_TYPE,
        settings.JWT_TTL_ACCESS_TIMEDELTA
        if access_token_expires and not override_ttl
        else override_ttl,
    )
    return jwt_encode(payload)


def create_refresh_token(
    user: CustomUser,
) -> str:
    payload = jwt_user_payload(
        user, JWT_REFRESH_TYPE, settings.JWT_TTL_REFRESH_TIMEDELTA
    )
    return jwt_encode(payload)
