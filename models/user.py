from sqlalchemy import Column,String
from sqlalchemy.orm import relationship

from .base import BaseModel
class UserModel(BaseModel):
    """
    UserModel represents the user entity in the database.
    Attributes:
        __tablename__ (str): The name of the database table associated with this model.
        name (Column): The name of the user, stored as a string with a maximum length of 150 characters. Nullable.
        email (Column): The email address of the user, stored as a unique string with a maximum length of 255 characters. Cannot be null.
        password (Column): The hashed password of the user, stored as a string with a maximum length of 18 characters. Cannot be null.
        families (relationship): A relationship to the FamilyUserMode model, representing the families associated with the user.
        transaction (relationship): A relationship to the TransactionModel, representing the transactions associated with the user.
        account (relationship): A relationship to the AccountsModel, representing the accounts associated with the user.
        category (relationship): A relationship to the CategoryModel, representing the categories associated with the user.
        goal (relationship): A relationship to the GoalModel, representing the goals associated with the user.
        budget (relationship): A relationship to the BudgetModel, representing the budgets associated with the user.
    """

    __tablename__ = "users"
    name = Column(String(length=150),nullable=True)
    email = Column(String(255), unique=True, nullable=False)
    password=Column(String(18), nullable=False)
    families=relationship('FamilyUserModel',back_populates='user')
    transaction=relationship('TransactionModel',back_populates='user')
    account=relationship('AccountModel', back_populates='user')
    category=relationship('CategoryModel', back_populates='user')
    goal=relationship('GoalModel', back_populates='user')
    budget=relationship('BudgetModel', back_populates='user')