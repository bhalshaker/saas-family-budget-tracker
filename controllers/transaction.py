from models import UserModel
from sqlalchemy.ext.asyncio import AsyncSession
from serializers import NewTransaction, UpdatedTransaction

async def get_all_transactions_of_family(family_id: str, current_user: UserModel, db: AsyncSession):
    pass

async def create_transaction_for_family(family_id: str, new_transaction: NewTransaction, current_user: UserModel, db: AsyncSession):
    pass

async def retrieve_transaction(transaction_id: str, current_user: UserModel, db: AsyncSession):
    pass

async def update_transaction(transaction_id: str, updated_transaction: UpdatedTransaction, current_user: UserModel, db: AsyncSession):
    pass

async def delete_transaction(transaction_id: str, current_user: UserModel, db: AsyncSession):
    pass