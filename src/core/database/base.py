from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import create_engine
from src.core.config import settings



engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False},
    echo=True,
)



class Base(DeclarativeBase):
    pass