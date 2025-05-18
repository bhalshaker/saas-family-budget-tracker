from sqlalchemy import Column,Numeric,UUID,ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel

class BudgetTransactionModel(BaseModel):
    """
    Represents the association between a budget and a transaction in the system.
    Attributes:
        __tablename__ (str): The name of the database table for this model.
        family_id (UUID): The unique identifier of the associated family.
        budget_id (UUID): The unique identifier of the associated budget. 
            Foreign key referencing the 'id' column in the 'budgets' table.
        transaction_id (UUID): The unique identifier of the associated transaction. 
            Foreign key referencing the 'id' column in the 'transactions' table.
        assigned_amount (Decimal): The amount assigned to this transaction within the budget. 
            Stored as a numeric value with a scale of 3.
        transaction (TransactionModel): The relationship to the TransactionModel, 
            representing the transaction associated with this budget.
        budget (BudgetModel): The relationship to the BudgetModel, 
            representing the budget associated with this transaction.
    """

    __tablename__ = "budgets_transactions"
    family_id=Column(UUID(as_uuid=True), ForeignKey('families.id',deferrable=True), nullable=False)
    budget_id=Column(UUID(as_uuid=True), ForeignKey('budgets.id',deferrable=True), nullable=False)
    transaction_id=Column(UUID(as_uuid=True), ForeignKey('transactions.id',deferrable=True), nullable=False)
    assigned_amount=Column(Numeric(scale=3),nullable=False)
    transaction=relationship('TransactionModel',back_populates='budgets')
    budget=relationship('BudgetModel',back_populates='transactions')