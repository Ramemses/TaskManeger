from fastapi import APIRouter, Depends, Form, status
from fastapi.security import HTTPBearer, OAuth2PasswordBearer
from fastapi.exceptions import HTTPException
from src.scheme.user import CreateUser, RegistrationUser, UserResponse
from src.scheme.token import TokenInfo
from src.core import security as auth_security, settings
from src.repositories.user import UserServices, get_user_service
from src.models.user import User
from src.services.auth import create_access_token, create_refresh_token
from pydantic import EmailStr


router = APIRouter(tags=['authorisation'], prefix='/auth')

http_bearer = HTTPBearer()
oauth_sheme = OAuth2PasswordBearer(tokenUrl="auth/login",)



def validate_auth_user(
        email: EmailStr = Form(...),
       password: str = Form(...),
       user_services : UserServices = Depends(get_user_service)
       ):
    unauthed_exc = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid email or password")

    user = user_services.get_user_by_email(email)
    if not user:
        raise unauthed_exc
    
    if not (auth_security.verify_password(password=password, hashed_password=user.hashed_password)):
        raise unauthed_exc
    
    return UserResponse(
        id=user.id,          
        username=user.username,
        email=user.email,
        is_active=user.is_active,
        is_superuser=user.is_superuser
    )




@router.post('/login', response_model=TokenInfo)
def login(user: UserResponse = Depends(validate_auth_user)):

    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)

    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token,
    )



def validate_registration_user(user: RegistrationUser = Form(...)) -> CreateUser:
    
        if user.password1 != user.password2:
             raise HTTPException(status_code=422, detail="Passwords not euqal")
    
        return CreateUser(
                username=user.username,
                email=user.email,
                password=auth_security.hash_password(user.password1),
                is_active=True
                )


@router.post('/registration')
def registration(user: CreateUser= Depends(validate_registration_user), 
        user_services: UserServices =Depends(get_user_service)) -> dict:

        
        #Try to create new user
        result = user_services.create_user(user)
        if not result:
             raise HTTPException(
                status_code=400, 
                detail="User with this email address is alredy exist"
            )
        
        return {"succes": True, "status_code": 302, "redirect": "/login"} 
    