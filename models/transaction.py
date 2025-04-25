from sqlalchemy import Column,String,Numeric,DateTime,UUID,ForeignKey
from .base import BaseModel
class TransactionModel(BaseModel):
    __tablename__ = "transactions"
    user_id=Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    family_id=Column(UUID(as_uuid=True), ForeignKey('families.id'), nullable=False)
    account_id=Column(UUID(as_uuid=True), ForeignKey('accounts.id'), nullable=False)
    category_id=Column(UUID(as_uuid=True), ForeignKey('categories.id'), nullable=False)
    amount=Column(Numeric(scale=3),nullable=False)
    #currency TODO: In the future
    date=Column(DateTime(),nullable=False)
    description=Column(String(),nullable=True)
    #transaction_type TODO: Evaluate whether this has to be defined in table or Enum