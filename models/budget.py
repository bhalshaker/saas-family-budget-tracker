from sqlalchemy import Column,Numeric,DateTime,UUID,ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel
class BudgetModel(BaseModel):
    __tablename__ = "budgets"
    user_id=Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    family_id=Column(UUID(as_uuid=True), ForeignKey('families.id'), nullable=False)
    category_id=Column(UUID(as_uuid=True), ForeignKey('categories.id'), nullable=False)
    amount=Column(Numeric(scale=3),nullable=False)
    start_date=Column(DateTime(),nullable=False)
    end_date=Column(DateTime(),nullable=False)
    user=relationship('UserModel',back_populates='budget')
    family=relationship('FamilyModel',back_populates='budget')
    category=relationship('CategoryModel',back_populates='budget')
    transactions=relationship('BudgetTransactionModel',back_populates='budgets')