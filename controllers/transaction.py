from models import UserModel
from sqlalchemy.ext.asyncio import AsyncSession
from serializers import CreateTransaction, UpdateTransaction, RestCreateTransactionResponse, RestGetTransactionResponse, RestGetAllTransactionsOfamilyResponse, BaseRestResponse

async def get_all_transactions_of_family(family_id: str, current_user: UserModel, db: AsyncSession)->RestGetAllTransactionsOfamilyResponse:
    pass

async def create_transaction_for_family(family_id: str, new_transaction: CreateTransaction, current_user: UserModel, db: AsyncSession)-> RestCreateTransactionResponse:
    pass

async def retrieve_transaction(transaction_id: str, current_user: UserModel, db: AsyncSession)-> RestGetTransactionResponse:
    pass

async def update_transaction(transaction_id: str, updated_transaction: UpdateTransaction, current_user: UserModel, db: AsyncSession)->RestCreateTransactionResponse:
    pass

async def delete_transaction(transaction_id: str, current_user: UserModel, db: AsyncSession)->BaseRestResponse:
    pass