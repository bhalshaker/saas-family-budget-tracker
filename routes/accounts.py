from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from controllers import get_current_user
from controllers import ControllerGetAllFamilyAccounts,ControllerCreateNewAccount,ControllerGetAccount,ControllerUpdateAccount,ControllerDeleteAccount
from models import UserModel
from serializers import RestGetAllAccountsOfamilyResponse, CreateAccount,UpdateAccount, RestCreateAccountResponse, BaseRestResponse

router = APIRouter()

# Get a list of all accounts belongs to a family
@router.get("/api/v1/families/{family_id}/accounts", response_model=RestGetAllAccountsOfamilyResponse,summary="Get all accounts of a family",description="Get all accounts of a family")
async def get_all_family_accounts(family_id: str, current_user: UserModel = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """
    Get all accounts of a family
    """
    return await ControllerGetAllFamilyAccounts(family_id, current_user, db)

# Post a new account that belongs to a family
@router.post("/api/v1/families//{family_id}/accounts", response_model=RestCreateAccountResponse,summary="Create a new account",description="Create a new account")
async def create_new_account(family_id: str, new_account: CreateAccount, current_user: UserModel = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """
    Create a new account
    """
    return await ControllerCreateNewAccount(family_id, new_account, current_user, db)

# Get a specific account
@router.get("/api/v1/accounts/{account_id}", response_model=ControllerGetAccount,summary="Get a specific account",description="Get a specific account")
async def get_account(account_id: str, current_user: UserModel = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """
    Get a specific account
    """
    return await ControllerGetAccount(account_id, current_user, db)

# Put -- Upadate an account
@router.put("/api/v1/accounts/{account_id}", response_model=RestCreateAccountResponse,summary="Update an account",description="Update an account")
async def update_account(account_id: str, updated_account: UpdateAccount, current_user: UserModel = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """
    Update an account
    """
    return await ControllerUpdateAccount(account_id, updated_account, current_user, db)

# Delete an account
@router.delete("/api/v1/accounts/{account_id}", response_model=BaseRestResponse,summary="Delete an account",description="Delete an account")
async def delete_account(account_id: str, current_user: UserModel = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """
    Delete an account
    """
    return await ControllerDeleteAccount(account_id, current_user, db)