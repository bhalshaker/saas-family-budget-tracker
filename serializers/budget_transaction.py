from pydantic import BaseModel
from uuid import UUID
from serializers import BaseRestResponse
from typing import Optional, List

class CreateBudgetTransaction(BaseModel):
    budget_id: str
    transaction_id: str
    assigned_amount: float

class BudgetTransactionInfo(BaseModel):
    id: UUID
    budget_id: str
    transaction_id: str
    assigned_amount: float

class RestGetAllBudgetTransactionsOfamilyResponse(BaseRestResponse):
    budget_transactions: Optional[List[BudgetTransactionInfo]] = None

class RestCreateBudgetTransactionResponse(BaseRestResponse):
    budget_transaction: BudgetTransactionInfo

class RestGetBudgetTransactionResponse(BaseRestResponse):
    budget_transaction: BudgetTransactionInfo