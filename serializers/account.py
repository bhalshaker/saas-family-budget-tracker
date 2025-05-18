from pydantic import BaseModel
from models import AccountType
from typing import Optional,List
from .base import BaseRestResponse
from uuid import UUID

class CreateAccount(BaseModel):
    name:str
    type: AccountType

class UpdateAccount(BaseModel):
    name: Optional[str] = None
    type: Optional[AccountType] = None

class AccountInfo(BaseModel):
    id: UUID
    name: str
    type: AccountType

class RestCreateAccountResponse(BaseRestResponse):
    account: Optional[AccountInfo]=None

class RestGetAllAccountsOfamilyResponse(BaseRestResponse):
    accounts: Optional[List[AccountInfo]]=None

class RestGetAccountResponse(BaseRestResponse):
    account: Optional[AccountInfo]=None