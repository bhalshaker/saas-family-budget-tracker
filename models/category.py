from sqlalchemy import Column,String,Enum,UUID,ForeignKey
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