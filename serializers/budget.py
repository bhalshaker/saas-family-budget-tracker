from pydantic import BaseModel
from datetime import datetime
from typing import Optional,List
from uuid import UUID
from serializers import BaseRestResponse

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

class BudgetInfo(BaseModel):
    id:UUID
    family_id:UUID
    user_id:UUID
    category_id: UUID
    amount: float
    start_date: datetime
    end_date: datetime

class RestCreateBudgetResponse(BaseRestResponse):
    budget: BudgetInfo

class RestGetBudgetResponse(BaseRestResponse):
    budget: BudgetInfo

class RestGetAllBudgetsOfamilyResponse(BaseRestResponse):
    budgets: Optional[List[BudgetInfo]]=None