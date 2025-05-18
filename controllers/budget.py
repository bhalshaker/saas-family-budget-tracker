from models import UserModel,BudgetModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from serializers import CreateBudget, UpdateBudget, RestCreateBudgetResponse, RestGetBudgetResponse, RestGetAllBudgetsOfamilyResponse, BaseRestResponse,BudgetInfo
from uuid import UUID
from .authorization import check_user_in_family,check_user_is_family_owner
from .family import get_family_by_id,get_family_by_id_with_budget
 

async def get_all_budgets_of_family(family_id: str, current_user: UserModel, db: AsyncSession)->RestGetAllBudgetsOfamilyResponse:
    # Check if the user is a member of the family
    await check_user_in_family(family_id, current_user.id, db)
    # Get family
    family = await get_family_by_id_with_budget(family_id, db)
    if not family:
        return RestGetAllBudgetsOfamilyResponse(code=0, status="FAILED", message="Family not found")
    # Return all budgets of the family from the family
    return RestGetAllBudgetsOfamilyResponse(code=1, status="SUCCESS", message="Family budgets retrieved successfully", budgets=[BudgetInfo(**budget.__dict__) for budget in family.budget])

async def create_budget_for_family(family_id: str, new_budget: CreateBudget, current_user: UserModel, db: AsyncSession)-> RestCreateBudgetResponse:
    # Check if the user is the owner of the family
    await check_user_is_family_owner(family_id, current_user.id, db)
    # Get family
    family = await get_family_by_id(family_id, db)
    if not family:
        return RestCreateBudgetResponse(code=0, status="FAILED", message="Family not found")
    # Create new budget
    new_budget = BudgetModel(**new_budget.model_dump(exclude={"entry_category_id", "entry_account_id"}), family_id=family.id, user_id=current_user.id)
    db.add(new_budget)
    try:
        await db.commit()
        await db.refresh(new_budget)
        return RestCreateBudgetResponse(code=1, status="SUCCESS", message="Budget created successfully", budget=BudgetInfo(**new_budget.__dict__))
    except Exception as e:
        print(f"Error creating budget: {e}")
        await db.rollback()
        return RestCreateBudgetResponse(code=0, status="FAILED", message="Failed to create budget")

async def retrieve_budget(budget_id: str, current_user: UserModel, db: AsyncSession)->RestGetBudgetResponse:
    # Get budget
    budget = await get_budget_by_id(budget_id, db)
    if not budget:
        return RestGetBudgetResponse(code=0, status="FAILED", message="Budget not found")
    # Check if the user is a member of the family
    await check_user_in_family(str(budget.family_id), current_user.id, db)
    
    return RestGetBudgetResponse(code=1, status="SUCCESS", message="Budget retrieved successfully", budget=BudgetInfo(**budget.__dict__))

async def update_budget(budget_id: str, updated_budget: UpdateBudget, current_user: UserModel, db: AsyncSession)->RestCreateBudgetResponse:
    # Get budget
    budget = await get_budget_by_id(budget_id, db)
    if not budget:
        return RestCreateBudgetResponse(code=0, status="FAILED", message="Budget not found")
    # Check if the user is the owner of the family
    await check_user_is_family_owner(str(budget.family_id), current_user.id, db)
    # Update budget
    for key, value in updated_budget.model_dump(exclude={"entry_category_id", "entry_account_id"}).items():
        if value is not None:
            setattr(budget, key, value)
    db.add(budget)
    try:
        await db.commit()
        await db.refresh(budget)
        return RestCreateBudgetResponse(code=1, status="SUCCESS", message="Budget updated successfully", budget=BudgetInfo(**budget.__dict__))
    except:
        await db.rollback()
        return RestCreateBudgetResponse(code=0, status="FAILED", message="Failed to update budget")

async def delete_budget(budget_id: str, current_user: UserModel, db: AsyncSession)->BaseRestResponse:
    # Get budget
    budget = await get_budget_by_id(budget_id, db)
    if not budget:
        return BaseRestResponse(code=0, status="FAILED", message="Budget not found")
    # Check if the user is the owner of the family
    await check_user_is_family_owner(str(budget.family_id), current_user.id, db)
    
    # Delete budget
    await db.delete(budget)
    try:
        await db.commit()
        return BaseRestResponse(code=1, status="SUCCESS", message="Budget deleted successfully")
    except:
        await db.rollback()
        return BaseRestResponse(code=0, status="FAILED", message="Failed to delete budget")

async def get_budget_by_id(budget_id: str, db: AsyncSession) -> BudgetModel:
    """
    Retrieve a budget by its ID from the database.

    Args:
        budget_id (str): The ID of the budget to retrieve.
        db (AsyncSession): The database session.

    Returns:
        BudgetModel: The retrieved budget object.

    Raises:
        Exception: If the budget is not found.
    """
    result = await db.execute(select(BudgetModel).where(BudgetModel.id == UUID(budget_id)))
    budget = result.scalars().first()
    return budget