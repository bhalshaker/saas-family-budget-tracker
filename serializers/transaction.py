from pydantic import BaseModel
from datetime import datetime
from typing import Optional,List
from models import EntryType
from serializers import BaseRestResponse

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

class CreatedTransaction(BaseModel):
    pass

class RestGetAllTransactionsOfamilyResponse(BaseRestResponse):
    transactions: Optional[List[CreatedTransaction]]=None

class RestCreatedTransactionResponse(BaseRestResponse):
    transaction: CreatedTransaction

class RestGetTransactionResponse(BaseRestResponse):
    transaction: CreatedTransaction
