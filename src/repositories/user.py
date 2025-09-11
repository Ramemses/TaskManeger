from fastapi import Depends

from sqlalchemy import func
from sqlalchemy.orm import Session
from src.core.database.dependency import get_db
from src.models.user import User
from src.scheme.user import UserUpdate, CreateUser



class UserServices():

    def __init__(self, db: Session):
        self.db = db

    def get_max_user_id(self):
        max_id = self.db.query(func.max(User.id)).scalar()
        return max_id or 0  
    

    def get_user_by_id(self, user_id: int) -> User | None:        
        user = self.db.get(User, user_id)
        if user is None:
            print(f"User with id = {user_id} not found")
            return None
        return user


    def get_user_by_email(self, user_email: str) -> User | None:
        user = self.db.query(User).filter(User.email == user_email).first()
        if user is None:
            print(f"User with id = {user_email} not found")
            return None
        return user

    
    def create_user(self, user_data: CreateUser) -> User | None:
        if self.get_user_by_email(user_data.email):
            return False

        user = User(
            email=user_data.email,
            username=user_data.username,
            hashed_password=user_data.password,
            is_active=True,
            is_superuser=False
        )
        
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return True
        

    def update_user(self, user_id: int, user_data: UserUpdate):

        user =self.get_user_by_id(user_id)
        if not user:
            return False  

        if user_data.email:
            user.email = user_data.email
        if user_data.password:
            user.hashed_password = user_data.password
        if user_data.username:
            user.username = user_data.username
    
        self.db.commit()

        return True
        

    def delete_user(self, user_id: int):
        
        user  = self.get_user_by_id(user_id)

        if not user:
            return False
        
        self.db.delete(user)
        self.db.commit()


    def get_all_users(self):
        users =  self.db.query(User).all()

        return users
    



def get_user_service(db: Session = Depends(get_db)):
    return UserServices(db)