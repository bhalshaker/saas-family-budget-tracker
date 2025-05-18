from pydantic import BaseModel,computed_field
from uuid import UUID
from .base import BaseRestResponse
from typing import Optional, List

class CreateBudgetTransaction(BaseModel):
    entry_budget_id: str
    entry_transaction_id: str
    assigned_amount: float

    @computed_field
    @property
    def budget_id(self) -> Optional[str]:
        if self.entry_budget_id:
            return UUID(self.entry_budget_id)
        return None
    @computed_field
    @property
    def transaction_id(self) -> Optional[str]:
        if self.entry_transaction_id:
            return UUID(self.entry_transaction_id)
        return None

class BudgetTransactionInfo(BaseModel):
    id: UUID
    family_id: UUID
    budget_id: UUID
    transaction_id: UUID
    assigned_amount: float

class RestGetAllBudgetTransactionsOfamilyResponse(BaseRestResponse):
    budget_transactions: Optional[List[BudgetTransactionInfo]] = None

class RestCreateBudgetTransactionResponse(BaseRestResponse):
    budget_transaction: Optional[BudgetTransactionInfo] = None

class RestGetBudgetTransactionResponse(BaseRestResponse):
    budget_transaction: Optional[BudgetTransactionInfo] = None