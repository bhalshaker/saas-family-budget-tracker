from sqlalchemy import Column,String,Numeric,DateTime,UUID,ForeignKey
from .base import BaseModel

class GoalModel(BaseModel):
    __tablename__ = "goals"
    user_id=Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    family_id=Column(UUID(as_uuid=True), ForeignKey('families.id'), nullable=False)
    name = Column(String(), nullable=False)
    target_amount=Column(Numeric(scale=3),nullable=True)
    saved_amount=Column(Numeric(scale=3),nullable=True)
    due_date=Column(DateTime(),nullable=True)