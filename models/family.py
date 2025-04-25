from sqlalchemy import Column,String
from sqlalchemy.orm import relationship
from .base import BaseModel

class FamilyModel(BaseModel):
    __tablename__ = "families"
    family_name = Column(String(), nullable=False)
    users=relationship('FamilyUserModel',back_populates='family')
    transaction=relationship('TransactionModel',back_populates='family')
    account=relationship('AccountsModel',back_populates='family')
    category=relationship('CategoryModel',back_populates='family')
    goal=relationship('GoalModel',back_populates='family')
    budget=relationship('BudgetModel',back_populates='family')