from sqlalchemy import Column,String,Numeric,DateTime
from .base import BaseModel
class Transaction(BaseModel):
    __tablename__ = "transactions"
    amount=Column(Numeric(scale=3),nullable=False)
    #currency TODO: In the future
    date=Column(DateTime(),nullable=False)
    description=Column(String(),nullable=True)
    #transaction_type TODO: Evaluate whether this has to be defined in table or Enum