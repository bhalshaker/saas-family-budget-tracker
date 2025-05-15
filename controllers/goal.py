from models import UserModel
from sqlalchemy.ext.asyncio import AsyncSession
from  serializers import CreateGoal, UpdateGoal

async def get_all_goals_of_family(family_id: str, current_user: UserModel, db: AsyncSession):
    pass

async def create_goal_for_family(family_id: str, new_goal: CreateGoal, current_user: UserModel, db: AsyncSession):
    pass

async def retrieve_goal(goal_id: str, current_user: UserModel, db: AsyncSession):
    pass

async def update_goal(goal_id: str, updated_goal: UpdateGoal, current_user: UserModel, db: AsyncSession):
    pass

async def delete_goal(goal_id: str, current_user: UserModel, db: AsyncSession):
    pass