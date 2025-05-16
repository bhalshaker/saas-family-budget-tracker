from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from controllers import get_current_user
from models import UserModel
from controllers import ControllerGetAllBudgetsOfFamily,ControllerCreateBudgetForFamily,ControllerUpdateBudget,ControllerDeleteBudget
from serializers.budget import CreateBudget,UpdateBudget,RestGetAllBudgetsOfamilyResponse,RestCreateBudgetResponse

router = APIRouter()

# Get all budgets of a family through family_id (/api/v1/families/{family_id}/budgets)
@router.get(path="/api/v1/families/{family_id}/budgets",response_model=RestGetAllBudgetsOfamilyResponse,summary="Get all budgets of a family through family_id", description="Get all budgets of a family through family_id")
async def get_all_budgets_of_family(family_id: str, db: AsyncSession = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    """
    Get all budgets of a family through family_id
    """
    # Call the controller function to get all budgets of a family
    return await ControllerGetAllBudgetsOfFamily(family_id, db, current_user)

# Create a budget through family_id (/api/v1/families/{family_id}/budgets)
@router.post(path="/api/v1/families/{family_id}/budgets",response_model=RestCreateBudgetResponse,summary="Create a budget through family_id", description="Create a budget through family_id")
async def create_budget(family_id: str, budget: CreateBudget, db: AsyncSession = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    """
    Create a budget through family_id
    """
    # Call the controller function to create a budget
    return await ControllerCreateBudgetForFamily(family_id, budget, db, current_user)

#Update a bduget
@router.put(path="/api/v1/budgets/{budget_id}",response_model=RestCreateBudgetResponse,summary="Update a budget", description="Update a budget")
async def update_budget(budget_id: str, budget: UpdateBudget, db: AsyncSession = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    """
    Update a budget
    """
    # Call the controller function to update a budget
    return await ControllerUpdateBudget(budget_id, budget, db, current_user)

#Delete a budget
@router.delete(path="/api/v1/budgets/{budget_id}",response_model=RestCreateBudgetResponse,summary="Delete a budget", description="Delete a budget")
async def delete_budget(budget_id: str, db: AsyncSession = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    """
    Delete a budget
    """
    # Call the controller function to delete a budget
    return await ControllerDeleteBudget(budget_id, db, current_user)