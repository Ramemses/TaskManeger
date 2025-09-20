from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, ForeignKey
from src.core import Base
from typing import Optional


class Task(Base):
    __tablename__ = "Task"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(30))
    description: Mapped[Optional[str]] = mapped_column(String(512))
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False)

    
    user_id: Mapped[int] = mapped_column(ForeignKey("User.id"))
    user: Mapped["User"] = relationship(back_populates="tasks")


    def __repr__(self):
        return f"id: {self.id}, name: {self.name}, description: {self.description}, is_completed: {self.is_completed}"
