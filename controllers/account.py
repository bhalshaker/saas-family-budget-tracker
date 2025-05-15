from models import UserModel
from serializers import CreateAccount
from sqlalchemy.ext.asyncio import AsyncSession

async def get_all_family_accounts(family_id: str,current_user:UserModel,db:AsyncSession):
    pass

async def create_new_account(family_id: str,new_account:CreateAccount, current_user: UserModel, db: AsyncSession):
    pass

async def delete_account(account_id: str,current_user: UserModel, db: AsyncSession):
    pass

async def update_account(account_id: str,updated_account:CreateAccount,current_user: UserModel, db: AsyncSession):
    pass

async def get_account(account_id: str,current_user: UserModel, db: AsyncSession):
    pass