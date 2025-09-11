from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean
from src.core import Base





class User(Base):   
    __tablename__ = "User"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    username: Mapped[str] = mapped_column(String(30))
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)

    tasks: Mapped[list["Task"]] = relationship(back_populates="user")


    def __repr__(self):
        return f"User <id: {self.id:}, username: {self.username}>"
    

