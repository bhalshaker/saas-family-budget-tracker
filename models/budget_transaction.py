from sqlalchemy import Column,Numeric
from .base import BaseModel

class BudgetTransaction(BaseModel):
    __tablename__ = "attachments"
    assigned_amount=Column(Numeric(scale=3),nullable=False)