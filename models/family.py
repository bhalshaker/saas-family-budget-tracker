from sqlalchemy import Column,String
from sqlalchemy.orm import relationship
from .base import BaseModel

class FamilyModel(BaseModel):
    """
    FamilyModel represents the database model for a family entity in the system.
    Attributes:
        __tablename__ (str): The name of the database table associated with this model.
        name (Column): The name of the family, stored as a non-nullable string.
        users (relationship): A relationship to the FamilyUserModel, representing the users associated with the family.
        transaction (relationship): A relationship to the TransactionModel, representing the transactions linked to the family.
        account (relationship): A relationship to the AccountsModel, representing the accounts owned by the family.
        category (relationship): A relationship to the CategoryModel, representing the categories defined for the family.
        goal (relationship): A relationship to the GoalModel, representing the goals set by the family.
        budget (relationship): A relationship to the BudgetModel, representing the budgets associated with the family.
    """
    
    __tablename__ = "families"
    name = Column(String(), nullable=False)
    users=relationship('FamilyUserModel',back_populates='family')
    transaction=relationship('TransactionModel',back_populates='family')
    category=relationship('CategoryModel',back_populates='family')
    goal=relationship('GoalModel',back_populates='family')
    budget=relationship('BudgetModel',back_populates='family')
    account=relationship('AccountModel',back_populates='family')