from pydantic import BaseModel
from typing import Optional,List
from datetime import datetime
from uuid import UUID
from serializers import BaseRestResponse

class CreateGoal(BaseModel):
    name:str
    target_amount: float
    saved_amount: Optional[float] = 0.0
    due_date: datetime

class UpdateGoal(BaseModel):
    name: Optional[str] = None
    target_amount: Optional[float] = None
    saved_amount: Optional[float] = None
    due_date: Optional[datetime] = None

class GoalInfo(BaseModel):
    id: UUID
    family_id: UUID
    user_id: UUID
    name: str
    target_amount: float
    saved_amount: float
    due_date: datetime

class RestGetAllGoalsOfamilyResponse(BaseRestResponse):
    goals: Optional[List[GoalInfo]]=None

class RestCreateGoalResponse(BaseRestResponse):
    goal:GoalInfo

class RestGetGoalResponse(BaseRestResponse):
    goal:GoalInfo
