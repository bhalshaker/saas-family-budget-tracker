from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from controllers import get_current_user
from controllers import ControllerGetAllGoalsOfFamily,ControllerCreateGoalForFamily
from models import UserModel
from serializers import CreateGoal, UpdateGoal,RestGetAllGoalsOfamilyResponse,RestCreatedTransactionResponse,RestGetTransactionResponse,BaseRestResponse

router = APIRouter()

@router.get("/api/v1/families/{family_id}/goals")
async def get_all_goals_of_family(family_id:str, db: AsyncSession = Depends(get_db))->RestGetAllGoalsOfamilyResponse:
    return await ControllerGetAllGoalsOfFamily(family_id=family_id, db=db)

@router.post("/api/v1/families/{family_id}/goals")
async def create_new_goal(family_id:str,new_goal: CreateGoal,current_user:UserModel=Depends(get_current_user), db: AsyncSession = Depends(get_db))->RestCreatedTransactionResponse:
    return await ControllerCreateGoalForFamily(family_id=family_id, new_goal=new_goal, current_user=current_user, db=db)

@router.get("/api/v1/goals/{goal_id}")
async def get_goal(goal_id:str, current_user:UserModel=Depends(get_current_user), db: AsyncSession = Depends(get_db))->RestGetTransactionResponse:
    

@router.put("/api/v1/goals/{goal_id}")
async def update_goal(goal_id:str, updated_goal:UpdateGoal,current_user:UserModel=Depends(get_current_user), db: AsyncSession = Depends(get_db))->RestCreatedTransactionResponse:
    
    
    return await ControllerUpdateTransaction(transaction_id=transaction_id, updated_transaction=update_category, current_user=current_user, db=db)

@router.delete("/api/v1/goals/{transaction_id}")
async def delete_goal(goal_id:str, current_user:UserModel=Depends(get_current_user), db: AsyncSession = Depends(get_db))->BaseRestResponse:
    
    return await ControllerDeleteTransaction(transaction_id=transaction_id, current_user=current_user, db=db)