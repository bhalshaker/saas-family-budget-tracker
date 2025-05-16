from pydantic import BaseModel
from datetime import datetime
from typing import Optional,List
from models import EntryType
from serializers import BaseRestResponse
from uuid import UUID

class CreateTransaction(BaseModel):
    category_id: UUID
    account_id: UUID
    amount: float
    date: datetime
    description: Optional[str] = None
    type:EntryType

class UpdateTransaction(BaseModel):
    category_id: Optional[UUID] = None
    account_id: Optional[UUID] = None
    amount: Optional[float] = None
    date: Optional[datetime] = None
    description: Optional[str] = None
    type:Optional[EntryType] = None

class TransactionInfo(BaseModel):
    id: UUID
    family_id: UUID
    category_id: UUID
    account_id: UUID
    user_id: UUID
    amount: float
    date: datetime
    description: Optional[str] = None
    type:EntryType

class RestGetAllTransactionsOfamilyResponse(BaseRestResponse):
    transactions: Optional[List[TransactionInfo]]=None

class RestCreatedTransactionResponse(BaseRestResponse):
    transaction: TransactionInfo

class RestGetTransactionResponse(BaseRestResponse):
    transaction: TransactionInfo
