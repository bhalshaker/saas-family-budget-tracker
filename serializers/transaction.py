from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from models import EntryType

class CreateTransaction(BaseModel):
    category_id: str
    account_id: str
    amount: float
    date: datetime
    description: Optional[str] = None
    type:EntryType

class UpdateTransaction(BaseModel):
    category_id: Optional[str] = None
    account_id: Optional[str] = None
    amount: Optional[float] = None
    date: Optional[datetime] = None
    description: Optional[str] = None
    type:Optional[EntryType] = None