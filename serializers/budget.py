from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CreateBudget(BaseModel):
    category_id: str
    name: str
    amount: float
    start_date: datetime
    end_date: datetime

class UpdateBudget(BaseModel):
    category_id: Optional[str] = None
    name: Optional[str] = None
    amount: Optional[float] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None