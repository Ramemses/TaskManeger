from src.core import security as auth_security, settings
from src.scheme import UserResponse
from datetime import timedelta
from src.core.config import settings


TOKEN_TYPE_FIELD = "type"
ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"


def create_token(payload: dict, resfresh_token_expire_days: timedelta | None = None):
    
    token = auth_security.create_jwt(payload, expire_timedelta_days=resfresh_token_expire_days)
    return token


def create_access_token(user: UserResponse):
    
    payload = {
        "sub": str(user.id),
        "isa": user.is_active,
        "iss": user.is_superuser,
        TOKEN_TYPE_FIELD: ACCESS_TOKEN_TYPE,
    }

    return create_token(payload)


def create_refresh_token(user: UserResponse):
    payload = {
        "sub": str(user.id),
        TOKEN_TYPE_FIELD: REFRESH_TOKEN_TYPE,
    }

    return create_token(
            payload=payload,    
            resfresh_token_expire_days=timedelta(days=settings.auth_jwt.refresh_token_expire_days),   
        )


def reload_access_token():
    pass


