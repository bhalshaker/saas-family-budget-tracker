from sqlalchemy import Column,Numeric,DateTime
from .base import BaseModel
class Budget(BaseModel):
    __tablename__ = "budgets"
    amount=Column(Numeric(scale=3),nullable=False)
    #currency TODO: In the future
    start_date=Column(DateTime(),nullable=False)
    end_date=Column(DateTime(),nullable=False)
    #transaction_type TODO: Evaluate whether this has to be defined in table or Enum