from pydantic import BaseModel
from models import AccountType
from typing import Optional,List
from .base import BaseRestResponse

class CreateAccount(BaseModel):
    name:str
    type: AccountType
    balance: Optional[float] = 0.0

class UpdateAccount(BaseModel):
    name: Optional[str] = None
    type: Optional[AccountType] = None
    balance: Optional[float] = None

class AccountInfo(BaseModel):
    id: str
    name: str
    type: AccountType
    balance: float

class RestCreateAccountResponse(BaseRestResponse):
    account: AccountInfo

class RestGetAllAccountsOfamilyResponse(BaseRestResponse):
    accounts: Optional[List[AccountInfo]]=None

class RestGetAccountResponse(BaseRestResponse):
    account: Optional[AccountInfo]=None