from sqlalchemy import Column,Numeric,DateTime,UUID,ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel
class BudgetModel(BaseModel):
    """
    BudgetModel represents the budget entity in the application.
    Attributes:
        __tablename__ (str): The name of the database table associated with this model.
        user_id (UUID): Foreign key referencing the ID of the user associated with the budget.
        family_id (UUID): Foreign key referencing the ID of the family associated with the budget.
        category_id (UUID): Foreign key referencing the ID of the category associated with the budget.
        amount (Numeric): The budgeted amount with a precision of up to 3 decimal places.
        start_date (DateTime): The start date of the budget period.
        end_date (DateTime): The end date of the budget period.
        user (UserModel): Relationship to the UserModel, representing the user associated with the budget.
        family (FamilyModel): Relationship to the FamilyModel, representing the family associated with the budget.
        category (CategoryModel): Relationship to the CategoryModel, representing the category associated with the budget.
        transactions (BudgetTransactionModel): Relationship to the BudgetTransactionModel, representing the transactions associated with the budget.
    """

    __tablename__ = "budgets"
    user_id=Column(UUID(as_uuid=True), ForeignKey('users.id',deferrable=True), nullable=False)
    family_id=Column(UUID(as_uuid=True), ForeignKey('families.id',deferrable=True), nullable=False)
    category_id=Column(UUID(as_uuid=True), ForeignKey('categories.id',deferrable=True), nullable=False)
    amount=Column(Numeric(scale=3),nullable=False)
    start_date=Column(DateTime(),nullable=False)
    end_date=Column(DateTime(),nullable=False)
    user=relationship('UserModel',back_populates='budget')
    family=relationship('FamilyModel',back_populates='budget')
    category=relationship('CategoryModel',back_populates='budget')
    transactions=relationship('BudgetTransactionModel',back_populates='budgets')
    account=relationship('AccountModel',back_populates='buget')