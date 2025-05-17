from models import UserModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from serializers import CreateBudgetTransaction, RestGetAllBudgetTransactionsOfamilyResponse, RestCreateBudgetTransactionResponse, RestGetBudgetTransactionResponse, BaseRestResponse

async def get_all_budget_transactions_of_family(family_id: str, current_user: UserModel, db: AsyncSession)->RestGetAllBudgetTransactionsOfamilyResponse:
    pass

async def add_budget_transaction_for_family(family_id: str, new_budget_transaction: CreateBudgetTransaction, current_user: UserModel, db: AsyncSession)-> RestCreateBudgetTransactionResponse:
    pass

async def retrieve_budget_transaction(budget_transaction_id: str, current_user: UserModel, db: AsyncSession)->RestGetBudgetTransactionResponse:
    pass

async def delete_budget_transaction(budget_transaction_id: str, current_user: UserModel, db: AsyncSession)->BaseRestResponse:
    pass