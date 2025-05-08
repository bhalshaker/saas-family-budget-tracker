from sqlalchemy import Column,Enum as EnumSQL,DateTime,func,UUID,ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel
import enum

class Role(enum.Enum):
    PARENT = "parent"
    BIG_SIBLING="big sibling"
    CHILD = "child"
    GUEST = "guest"
        

class FamilyUserModel(BaseModel):
    """
    FamilyUserModel represents the association between users and families in the system.
    Attributes:
        __tablename__ (str): The name of the database table, "families_users".
        user_id (UUID): Foreign key referencing the ID of a user in the "users" table. Cannot be null.
        family_id (UUID): Foreign key referencing the ID of a family in the "families" table. Cannot be null.
        role (Enum): The role of the user within the family, defined by the Role enumeration. Cannot be null.
        joined_at (DateTime): The timestamp when the user joined the family. Defaults to the current time.
        user (relationship): A SQLAlchemy relationship to the UserModel, representing the user associated with this record.
        family (relationship): A SQLAlchemy relationship to the FamilyModel, representing the family associated with this record.
    """

    __tablename__ = "families_users"
    user_id=Column(UUID(as_uuid=True), ForeignKey('users.id',deferrable=True), nullable=False)
    family_id=Column(UUID(as_uuid=True), ForeignKey('families.id',deferrable=True), nullable=False)
    role = Column(EnumSQL(Role, name="role_enum", native_enum=True),nullable=False)
    joined_at=Column(DateTime, default=func.now())
    user=relationship('UserModel',back_populates='families')
    family=relationship('FamilyModel',back_populates='users')