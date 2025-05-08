from sqlalchemy import Column,String,Numeric,DateTime,UUID,ForeignKey,Enum as EnumSQL,func
from sqlalchemy.orm import relationship
from .base import BaseModel,EntryType
class TransactionModel(BaseModel):
    """
    TransactionModel represents a financial transaction within the family budget tracker system.
    Attributes:
        __tablename__ (str): The name of the database table associated with this model.
        user_id (UUID): Foreign key referencing the ID of the user who created the transaction.
        family_id (UUID): Foreign key referencing the ID of the family associated with the transaction.
        account_id (UUID): Foreign key referencing the ID of the account involved in the transaction.
        category_id (UUID): Foreign key referencing the ID of the category for the transaction.
        amount (Numeric): The monetary value of the transaction, with a scale of 3 decimal places.
        date (DateTime): The timestamp of when the transaction occurred. Defaults to the current time.
        description (str): An optional description or note about the transaction.
        transaction_type (Enum): The type of transaction (e.g., income, expense) based on the EntryType enum.
        attachment (AttachmentModel): A one-to-one relationship with the AttachmentModel, representing any associated file.
        user (UserModel): A relationship to the UserModel, representing the user who created the transaction.
        family (FamilyModel): A relationship to the FamilyModel, representing the family associated with the transaction.
        account (AccountModel): A relationship to the AccountModel, representing the account involved in the transaction.
        category (CategoryModel): A relationship to the CategoryModel, representing the category of the transaction.
        budgets (list[BudgetTransactionModel]): A relationship to BudgetTransactionModel, representing budget allocations for the transaction.
    """

    __tablename__ = "transactions"
    user_id=Column(UUID(as_uuid=True), ForeignKey('users.id',deferrable=True), nullable=False)
    family_id=Column(UUID(as_uuid=True), ForeignKey('families.id'),deferrable=True, nullable=False)
    account_id=Column(UUID(as_uuid=True), ForeignKey('accounts.id',deferrable=True), nullable=False)
    category_id=Column(UUID(as_uuid=True), ForeignKey('categories.id',deferrable=True), nullable=False)
    amount=Column(Numeric(scale=3),nullable=False)
    date=Column(DateTime(),default=func.now(),nullable=False)
    description=Column(String(),nullable=True)
    transaction_type=Column(EnumSQL(EntryType, name="entry_type", native_enum=True),nullable=False)
    attachment=relationship('AttachmentModel',back_populates='transaction',uselist=False)
    user=relationship('UserModel',back_populates='transaction')
    family=relationship('FamilyModel',back_populates='transaction')
    account=relationship('AccountModel',back_populates='transaction')
    category=relationship('CategoryModel',back_populates='transaction')
    budgets=relationship('BudgetTransactionModel',back_populates='transaction')