from sqlalchemy import Column,String,Enum
from .base import BaseModel

class CategoryType(Enum):
    INCOME = "income"
    EXPENSE = "expense"
class Category(BaseModel):
    __tablename__ = "categories"
    name = Column(String, nullable=False)
    type= Column(Enum(CategoryType, name="category_type_enum", native_enum=True),nullable=False)