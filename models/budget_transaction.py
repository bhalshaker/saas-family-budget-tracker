from sqlalchemy import Column,Numeric,UUID,ForeignKey
from .base import BaseModel

class BudgetTransaction(BaseModel):
    __tablename__ = "attachments"
    budget_id=Column(UUID(as_uuid=True), ForeignKey('budgets.id'), nullable=False)
    transaction_id=Column(UUID(as_uuid=True), ForeignKey('transactions.id'), nullable=False)
    assigned_amount=Column(Numeric(scale=3),nullable=False)