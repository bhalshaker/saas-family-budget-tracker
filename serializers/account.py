from pydantic import BaseModel
from models import AccountType
from typing import Optional

class CreateAccount(BaseModel):
    name:str
    type: AccountType
    balance: Optional[float] = 0.0

class UpdateAccount(BaseModel):
    name: Optional[str] = None
    type: Optional[AccountType] = None
    balance: Optional[float] = None