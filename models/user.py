from sqlalchemy import Column,String
from sqlalchemy.orm import relationship

from .base import BaseModel
class UserModel(BaseModel):
    __tablename__ = "users"
    name = Column(String(length=150),nullable=True)
    email = Column(String(255), unique=True, nullable=False)
    password=Column(String(128), nullable=False)
    families=relationship('FamilyUserMode',back_populates='user')
    transaction=relationship('TransactionModel',back_populates='user')
    account=relationship('AccountsModel',back_populates='user')
    category=relationship('CategoryModel',back_populates='user')
    goal=relationship('GoalModel',back_populates='user')
    budget=relationship('BudgetModel',back_populates='user')