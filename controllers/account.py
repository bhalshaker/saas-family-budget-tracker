from models import UserModel
from serializers import CreateAccount
from sqlalchemy.ext.asyncio import AsyncSession
from serializers import RestCreateAccountResponse, RestGetAccountResponse, RestGetAllAccountsOfamilyResponse, BaseRestResponse,UpdateAccount

async def get_all_family_accounts(family_id: str,current_user:UserModel,db:AsyncSession)->RestGetAllAccountsOfamilyResponse:
    pass

async def create_new_account(family_id: str,new_account:CreateAccount, current_user: UserModel, db: AsyncSession)-> RestCreateAccountResponse:
    pass

async def delete_account(account_id: str,current_user: UserModel, db: AsyncSession)->BaseRestResponse:
    pass

async def update_account(account_id: str,updated_account:UpdateAccount,current_user: UserModel, db: AsyncSession)->RestCreateAccountResponse:
    pass

async def get_account(account_id: str,current_user: UserModel, db: AsyncSession)->RestGetAccountResponse:
    pass