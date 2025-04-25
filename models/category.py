from sqlalchemy import Column,String,Enum,UUID,ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel

class CategoryType(Enum):
    INCOME = "income"
    EXPENSE = "expense"
class CategoryModel(BaseModel):
    __tablename__ = "categories"
    user_id=Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    family_id=Column(UUID(as_uuid=True), ForeignKey('families.id'), nullable=False)
    name = Column(String, nullable=False)
    type= Column(Enum(CategoryType, name="category_type_enum", native_enum=True),nullable=False)
    user=relationship('UserModel',back_populates='category')
    family=relationship('FamilyModel',back_populates='category')