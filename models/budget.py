from sqlalchemy import Column,Numeric,DateTime,UUID,ForeignKey
from .base import BaseModel
class BudgetModel(BaseModel):
    __tablename__ = "budgets"
    user_id=Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    family_id=Column(UUID(as_uuid=True), ForeignKey('families.id'), nullable=False)
    category_id=Column(UUID(as_uuid=True), ForeignKey('categories.id'), nullable=False)
    amount=Column(Numeric(scale=3),nullable=False)
    #currency TODO: In the future
    start_date=Column(DateTime(),nullable=False)
    end_date=Column(DateTime(),nullable=False)
    #transaction_type TODO: Evaluate whether this has to be defined in table or Enum