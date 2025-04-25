from sqlalchemy import Column,Enum,DateTime,func
from .base import BaseModel
import enum

class Role(enum.Enum):
    PARENT = "parent"
    BIG_SIBLING="big sibling"
    CHILD = "child"
    GUEST = "guest"
        

class FamilyUser(BaseModel):
    __tablename__ = "families_users"
    role = Column(Enum(Role, name="role_enum", native_enum=True),nullable=False)
    joined_at=Column(DateTime, default=func.now())