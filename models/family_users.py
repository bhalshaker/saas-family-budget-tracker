from sqlalchemy import Column,Enum,DateTime,func,UUID,ForeignKey
from .base import BaseModel
import enum

class Role(enum.Enum):
    PARENT = "parent"
    BIG_SIBLING="big sibling"
    CHILD = "child"
    GUEST = "guest"
        

class FamilyUserModel(BaseModel):
    __tablename__ = "families_users"
    user_id=Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    family_id=Column(UUID(as_uuid=True), ForeignKey('families.id'), nullable=False)
    role = Column(Enum(Role, name="role_enum", native_enum=True),nullable=False)
    joined_at=Column(DateTime, default=func.now())