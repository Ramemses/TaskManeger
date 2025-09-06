from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from typing import Annotated
from src.routes.auth import oauth_sheme, http_bearer
from src.core import security as auth_security
from src.scheme import TokenInfo, CreateUser
from src.routes.auth import users_db
from jwt import InvalidTokenError


router = APIRouter(tags=["users"], prefix='/users')



def get_payload(token: str = Depends(oauth_sheme)):
    try:
        payload  = auth_security.decode_jwt(token=token)
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="invalid token error")

    return payload


# def get_payload(creds: Annotated[HTTPAuthorizationCredentials , Depends(http_bearer)]) -> dict:
#     token = creds.credentials

#     try:
#         payload  = auth_security.decode_jwt(token=token)
#     except InvalidTokenError:
#         raise HTTPException(status_code=401, detail="invalid token error")

#     return payload


def get_authed_user(payload: dict = Depends(get_payload)) -> CreateUser:
    
    username = payload.get("sub")   
    if not (user:=users_db.get(username)):
        raise HTTPException(status_code=401, detail="token invalid(user not found)")
        
    return user
    

def get_active_user(user: CreateUser = Depends(get_authed_user)) -> CreateUser:
    if user.is_active:
        return user
    return HTTPException(status_code=403, detail="user inactive")


@router.get("/me")
def get_user(user: CreateUser = Depends(get_active_user)) -> dict:
    return {
        "username": user.username,
        "email": user.email,
    }



