from sqlalchemy import Column,String,Numeric,DateTime
from .base import BaseModel

class Goal(BaseModel):
    __tablename__ = "goals"
    name = Column(String(), nullable=False)
    target_amount=Column(Numeric(scale=3),nullable=True)
    saved_amount=Column(Numeric(scale=3),nullable=True)
    due_date=Column(DateTime(),nullable=True)