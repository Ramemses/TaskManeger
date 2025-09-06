from fastapi import APIRouter, Depends, Form, status
from fastapi.security import HTTPBearer, OAuth2PasswordBearer
from fastapi.exceptions import HTTPException
from src.scheme.user import CreateUser, UserRegister
from src.scheme.token import TokenInfo
from src.core import security as auth_security, settings


router = APIRouter(tags=['authorisation'], prefix='/auth')

http_bearer = HTTPBearer()
oauth_sheme = OAuth2PasswordBearer(tokenUrl="auth/login",)

john = CreateUser(
    username="John",
    password=auth_security.hash_password("qwerty"),
    email="john@example.com",
    is_active=True
)


sam = CreateUser(
    username="Sam",
    password=auth_security.hash_password("secret"),
    email="sam@example.com",
    is_active=True 
)

users_db: dict[str, CreateUser] = {
    john.username: john,
    sam.username: sam,
}




def validate_auth_user(
        username: str = Form(...),
       password: str = Form(...),
       ):
    unauthed_exc = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid username or password")

    if not (user := users_db.get(username, None)):
        raise unauthed_exc
    
    if not (auth_security.verify_password(password=password, hashed_password=user.password)):
        raise unauthed_exc
    
    return user


@router.post('/login', response_model=TokenInfo)
def login(user: CreateUser = Depends(validate_auth_user)):

    payload = {
        "sub": user.username,
        "username": user.username,
        "emial": user.email,
    }

    token = auth_security.create_jwt(payload)

    return TokenInfo(
        access_token=token,
        token_type="Bearer"
    )


def validate_registration():
    ...

@router.post('/registration')
def registration(user: UserRegister= Depends(validate_registration)):
    if user.password1 == user.password2:
        users_db.update({user.username: user})
        return {"succes": True, "status_code": 302, "redirect": "/login"} 
    return {"success": False, "status_code": 422, "description": "Passwords not equal"}

