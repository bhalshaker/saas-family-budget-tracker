from pydantic import BaseModel, computed_field
from datetime import datetime
from typing import Optional,List
from uuid import UUID
from .base import BaseRestResponse

class CreateBudget(BaseModel):
    entry_category_id: str
    entry_account_id:str
    amount: float
    start_date: datetime
    end_date: datetime

    @computed_field
    @property
    def category_id(self) -> Optional[str]:
        if self.entry_category_id:
            return UUID(self.entry_category_id)
        return None
    @computed_field
    @property
    def account_id(self) -> Optional[str]:
        if self.entry_account_id:
            return UUID(self.entry_account_id)
        return None

class UpdateBudget(BaseModel):
    category_id: Optional[str] = None
    account_id: Optional[str] = None
    amount: Optional[float] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class BudgetInfo(BaseModel):
    id:UUID
    family_id:UUID
    user_id:UUID
    category_id: UUID
    account_id: UUID
    amount: float
    start_date: datetime
    end_date: datetime

class RestCreateBudgetResponse(BaseRestResponse):
    budget: Optional[BudgetInfo] = None

class RestGetBudgetResponse(BaseRestResponse):
    budget: Optional[BudgetInfo] = None

class RestGetAllBudgetsOfamilyResponse(BaseRestResponse):
    budgets: Optional[List[BudgetInfo]]=None