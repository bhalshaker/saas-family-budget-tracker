from models import UserModel,GoalModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from serializers import CreateGoal, UpdateGoal, RestCreateGoalResponse, RestGetGoalResponse, RestGetAllGoalsOfamilyResponse, BaseRestResponse
from serializers import GoalInfo
from .authorization import check_user_in_family,check_user_is_family_owner
from .family import get_family_by_id
from uuid import UUID

async def get_all_goals_of_family(family_id: str, current_user: UserModel, db: AsyncSession)->RestGetAllGoalsOfamilyResponse:
    """
    Retrieve all goals associated with a specific family.
    Args:
        family_id (str): The unique identifier of the family.
        current_user (UserModel): The currently authenticated user.
        db (AsyncSession): The asynchronous database session.
    Returns:
        RestGetAllGoalsOfamilyResponse: Response object containing the status, message, and a list of goals for the family.
    Raises:
        HTTPException: If the user is not a member of the family or if the family does not exist.
    """
    # Check if the user is a member of the family
    await check_user_in_family(family_id, current_user.id, db)
    # Get family
    family = await get_family_by_id(family_id, db)
    if not family:
        return BaseRestResponse(code=0, status="FAILED", message="Family not found")
    # Return all goals of the family from the family
    return RestGetAllGoalsOfamilyResponse(code=1, status="SUCCESS", message="Family goals retrieved successfully", goals=[GoalInfo(**goal) for goal in family.goals])

async def create_goal_for_family(family_id: str, new_goal: CreateGoal, current_user: UserModel, db: AsyncSession)-> RestCreateGoalResponse:
    # Check if the user is the owner of the family
    await check_user_is_family_owner(family_id, current_user.id, db)
    # Create new goal
    new_goal = GoalModel(**new_goal.model_dump(), family_id=UUID(family_id), user_id=current_user.id)
    db.add(new_goal)
    try:
        await db.commit()
        await db.refresh(new_goal)
        return RestCreateGoalResponse(code=1, status="SUCCESS", message="Goal created successfully", goal=GoalInfo(**new_goal.model_dump()))
    except Exception as e:
        await db.rollback()
        return BaseRestResponse(code=0, status="FAILED", message=f"Failed to create goal: {str(e)}")

async def retrieve_goal(goal_id: str, current_user: UserModel, db: AsyncSession)->RestGetGoalResponse:
    # Check if the user is a member of the family
    await check_user_in_family(goal_id, current_user.id, db)
    # Get goal
    goal = await get_goal_by_id(goal_id, db)
    if not goal:
        return BaseRestResponse(code=0, status="FAILED", message="Goal not found")
    return RestGetGoalResponse(code=1, status="SUCCESS", message="Goal retrieved successfully", goal=GoalInfo(**goal.model_dump()))

async def update_goal(goal_id: str, updated_goal: UpdateGoal, current_user: UserModel, db: AsyncSession)->RestCreateGoalResponse:
    # Check if the user is the owner of the family
    await check_user_is_family_owner(goal_id, current_user.id, db)
    # Get goal
    goal = await get_goal_by_id(goal_id, db)
    if not goal:
        return BaseRestResponse(code=0, status="FAILED", message="Goal not found")
    # Update goal
    for key, value in updated_goal.model_dump().items():
        if value is not None:
            setattr(goal, key, value)
    db.add(goal)
    try:
        await db.commit()
        await db.refresh(goal)
        return RestCreateGoalResponse(code=1, status="SUCCESS", message="Goal updated successfully", goal=GoalInfo(**goal.model_dump()))
    except Exception as e:
        await db.rollback()
        return BaseRestResponse(code=0, status="FAILED", message=f"Failed to update goal: {str(e)}")

async def delete_goal(goal_id: str, current_user: UserModel, db: AsyncSession)->BaseRestResponse:
    # Check if the user is the owner of the family
    await check_user_is_family_owner(goal_id, current_user.id, db)
    # Get goal
    goal = await get_goal_by_id(goal_id, db)
    if not goal:
        return BaseRestResponse(code=0, status="FAILED", message="Goal not found")
    # Delete goal
    try:
        await db.delete(goal)
        await db.commit()
        return BaseRestResponse(code=1, status="SUCCESS", message="Goal deleted successfully")
    except Exception as e:
        await db.rollback()
        return BaseRestResponse(code=0, status="FAILED", message=f"Failed to delete goal: {str(e)}")

async def get_goal_by_id(goal_id: str, db: AsyncSession)->GoalModel:
    """
    Retrieve a goal by its ID.
    Args:
        goal_id (str): The unique identifier of the goal.
        db (AsyncSession): The asynchronous database session.
    Returns:
        GoalModel: The goal object if found, None otherwise.
    """
    result = await db.execute(select(GoalModel).where(GoalModel.id == goal_id))
    return result.scalars().first()