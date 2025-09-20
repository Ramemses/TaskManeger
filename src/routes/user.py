from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPAuthorizationCredentials

from src.routes.auth import oauth_sheme, http_bearer
from src.core import security as auth_security
from src.scheme import TokenInfo, UserResponse
from src.repositories.user import UserServices, get_user_service

from jwt import InvalidTokenError
from datetime import datetime, timedelta
from typing import Annotated



router = APIRouter(tags=["users"], prefix='/users')



# def get_payload(token: str = Depends(oauth_sheme)):
#     try:
#         payload  = auth_security.decode_jwt(token=token)
#     except InvalidTokenError as e:
#         raise HTTPException(status_code=401, detail=f"invalid token error {e}")

#     return payload


def get_payload(creds: Annotated[HTTPAuthorizationCredentials , Depends(http_bearer)]) -> dict:
    token = creds.credentials
    try:
        payload  = auth_security.decode_jwt(token=token)
    except InvalidTokenError as e:
        raise HTTPException(status_code=401, detail=f"invalid token error {e}")
        
    

    return payload


# def validate_access_token_expire(payload: dict = Depends(get_payload)):
    
#     print("Sex 2")
#     if "exp" in payload:
#         current_timestamp = datetime.utcnow().timestamp()
#         if payload["exp"] < current_timestamp:
#             raise HTTPException(status_code=401, detail="Invalid token (access token expire is limited)")
#     else:
#         raise HTTPException(status_code=401, detail="Invalid token (token has no expire)")   
    # return payload

def get_authed_user(payload: dict = Depends(get_payload),
    user_services: UserServices=Depends(get_user_service)) -> UserResponse:
    
    id = int(payload.get("sub"))   
    if not (user:=user_services.get_user_by_id(id)):
        raise HTTPException(status_code=401, detail="token invalid(user not found)")
        
    return UserResponse(
        id = user.id,
        username=user.username,
        email=user.email,
        is_active=user.is_active,
        is_superuser=user.is_superuser
    )
    

def get_active_user(user: UserResponse = Depends(get_authed_user)) -> UserResponse:
    if user.is_active:
        return user
    return HTTPException(status_code=403, detail="user inactive")


@router.get("/me")
def get_user(user: UserResponse = Depends(get_active_user)) -> dict:
    return {
        "username": user.username,
        "email": user.email,
        "is_active": user.is_active,
        "is_superuser": user.is_superuser,
    }



