from models import UserModel
from sqlalchemy.ext.asyncio import AsyncSession
from serializers import CreateBudget, UpdateBudget, RestCreateBudgetResponse, RestGetBudgetResponse, RestGetAllBudgetsOfamilyResponse, BaseRestResponse

async def get_all_budgets_of_family(family_id: str, current_user: UserModel, db: AsyncSession)->RestGetAllBudgetsOfamilyResponse:
    pass

async def create_budget_for_family(family_id: str, new_budget: CreateBudget, current_user: UserModel, db: AsyncSession)-> RestCreateBudgetResponse:
    pass

async def retrieve_budget(budget_id: str, current_user: UserModel, db: AsyncSession)->RestGetBudgetResponse:
    pass

async def update_budget(budget_id: str, updated_budget: UpdateBudget, current_user: UserModel, db: AsyncSession)->RestCreateBudgetResponse:
    pass

async def delete_budget(budget_id: str, current_user: UserModel, db: AsyncSession)->BaseRestResponse:
    pass