from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CreateGoal(BaseModel):
    name:str
    target_amount: float
    saved_amount: Optional[float] = 0.0
    due_date: datetime

class UpdateGoal(BaseModel):
    name: Optional[str] = None
    target_amount: Optional[float] = None
    saved_amount: Optional[float] = None
    due_date: Optional[datetime] = None