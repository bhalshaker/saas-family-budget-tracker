from sqlalchemy import Column,String
from .base import BaseModel
class User(BaseModel):
    __tablename__ = "users"
    name = Column(String(length=150),nullable=True)
    email = Column(String(255), unique=True, nullable=False)
    password=Column(String(128), nullable=False)