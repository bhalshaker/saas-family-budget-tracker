from sqlalchemy import Column,ForeignKey,UUID,String,Enum as EnumSQL
from sqlalchemy.orm import relationship
from .base import BaseModel
from enum import Enum

class AccountType(Enum):
    INCOME = 'Income'
    EXPENSE = 'Expense'
    ASSET = 'Asset'
    LIABILITY = 'Liability'

class AccountModel(BaseModel):
    """
    AccountModel represents an account entity in the family budget tracker system.
    Attributes:
        __tablename__ (str): The name of the database table associated with this model.
        user_id (UUID): Foreign key referencing the ID of the user who owns the account.
        family_id (UUID): Foreign key referencing the ID of the family associated with the account.
        name (str): The name of the account.
        type (AccountType): The type of the account, represented as an enumeration.
        user (UserModel): Relationship to the UserModel, representing the user who owns the account.
        family (FamilyModel): Relationship to the FamilyModel, representing the family associated with the account.
    """

    __tablename__ = "accounts"
    user_id=Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    family_id=Column(UUID(as_uuid=True), ForeignKey('families.id'), nullable=False)
    name = Column(String, nullable=False)
    type= Column(EnumSQL(AccountType, name="account_type", native_enum=True),nullable=False)
    user=relationship('UserModel',back_populates='account')
    family=relationship('FamilyModel',back_populates='account')
    budget=relationship('BudgetModel',back_populates='account')
    transaction=relationship('TransactionModel',back_populates='account')