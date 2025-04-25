from sqlalchemy import Column,String,Enum,UUID,ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel,EntryType
class CategoryModel(BaseModel):
    __tablename__ = "categories"
    user_id=Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    family_id=Column(UUID(as_uuid=True), ForeignKey('families.id'), nullable=False)
    name = Column(String, nullable=False)
    type= Column(Enum(EntryType, name="entry_type", native_enum=True),nullable=False)
    user=relationship('UserModel',back_populates='category')
    family=relationship('FamilyModel',back_populates='category')