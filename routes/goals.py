from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from controllers import get_current_user
from controllers import ControllerGetAllGoalsOfFamily,ControllerCreateGoalForFamily,ControllerUpdateGoal, ControllerDeleteGoal,ControllerRetrieveGoal
from models import UserModel
from serializers import CreateGoal, UpdateGoal,RestGetAllGoalsOfamilyResponse,RestCreateGoalResponse,RestGetGoalResponse,BaseRestResponse

router = APIRouter()

# Get all goals of a family
@router.get(path="/api/v1/families/{family_id}/goals",response_model=RestGetAllGoalsOfamilyResponse,summary="Get all goals of a family",description="Retrieve all financial goals associated with a specific family.")
async def get_all_goals_of_family(family_id:str, db: AsyncSession = Depends(get_db))->RestGetAllGoalsOfamilyResponse:
    """
    Retrieve all goals associated with a specific family.
    Args:
        family_id (str): The unique identifier of the family whose goals are to be retrieved.
        db (AsyncSession, optional): The asynchronous database session dependency.
    Returns:
        RestGetAllGoalsOfamilyResponse: The response object containing all goals for the specified family.
    """
    
    return await ControllerGetAllGoalsOfFamily(family_id=family_id, db=db)

#Create a new goal for a family
@router.post(path="/api/v1/families/{family_id}/goals",response_model=RestCreateGoalResponse,summary="Create a new goal",description="Create a new financial goal for a specified family.")
async def create_new_goal(family_id:str,new_goal: CreateGoal,current_user:UserModel=Depends(get_current_user), db: AsyncSession = Depends(get_db))->RestCreateGoalResponse:
    """
    Creates a new financial goal for a specified family.
    Args:
        family_id (str): The unique identifier of the family for which the goal is being created.
        new_goal (CreateGoal): The data model containing information about the new goal to be created.
        current_user (UserModel, optional): The currently authenticated user, injected by dependency.
        db (AsyncSession, optional): The asynchronous database session, injected by dependency.
    Returns:
        RestCreateGoalResponse: The response object containing details of the created goal transaction.
    """

    return await ControllerCreateGoalForFamily(family_id=family_id, new_goal=new_goal, current_user=current_user, db=db)

#Retrieve a goal
@router.get(path="/api/v1/goals/{goal_id}",response_model=RestGetGoalResponse,summary="Get a goal",description="Retrieve a specific goal by its ID.")
async def get_goal(goal_id:str, current_user:UserModel=Depends(get_current_user), db: AsyncSession = Depends(get_db))->RestGetGoalResponse:
    """
    Retrieve a specific goal by its ID for the current authenticated user.
    Args:
        goal_id (str): The unique identifier of the goal to retrieve.
        current_user (UserModel, optional): The currently authenticated user, injected by dependency.
        db (AsyncSession, optional): The asynchronous database session, injected by dependency.
    Returns:
        RestGetGoalResponse: The response object containing the retrieved goal details.
    """

    return await ControllerRetrieveGoal(goal_id=goal_id, current_user=current_user, db=db)
    

@router.put(path="/api/v1/goals/{goal_id}",response_model=RestCreateGoalResponse,summary="Update a goal",description="Update an existing goal by its ID.")
async def update_goal(goal_id:str, updated_goal:UpdateGoal,current_user:UserModel=Depends(get_current_user), db: AsyncSession = Depends(get_db))->RestCreateGoalResponse:
    """
    Update an existing goal with new data.
    Args:
        goal_id (str): The unique identifier of the goal to update.
        updated_goal (UpdateGoal): The updated goal data.
        current_user (UserModel, optional): The currently authenticated user. Automatically injected by dependency.
        db (AsyncSession, optional): The database session. Automatically injected by dependency.
    Returns:
        RestCreateGoalResponse: The response containing the updated goal information.
    """

    return await ControllerUpdateGoal(goal_id=goal_id, updated_goal=updated_goal, current_user=current_user, db=db)

@router.delete(path="/api/v1/goals/{goal_id}",response_model=BaseRestResponse,summary="Delete a goal",description="Delete a goal by its ID.")
async def delete_goal(goal_id:str, current_user:UserModel=Depends(get_current_user), db: AsyncSession = Depends(get_db))->BaseRestResponse:
    """
    Deletes a goal specified by its ID for the current authenticated user.
    Args:
        goal_id (str): The unique identifier of the goal to be deleted.
        current_user (UserModel, optional): The currently authenticated user, injected by dependency.
        db (AsyncSession, optional): The asynchronous database session, injected by dependency.
    Returns:
        BaseRestResponse: The response object indicating the result of the delete operation.
    """

    return await ControllerDeleteGoal(goal_id=goal_id, current_user=current_user, db=db)