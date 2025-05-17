from sqlalchemy.future import select
from models import UserModel,AccountModel
from serializers import CreateAccount,AccountInfo
from sqlalchemy.ext.asyncio import AsyncSession
from serializers import RestCreateAccountResponse, RestGetAccountResponse, RestGetAllAccountsOfamilyResponse, BaseRestResponse,UpdateAccount
from .authorization import check_user_in_family,check_user_is_family_owner
from .family import get_family_by_id
from uuid import UUID

async def get_all_family_accounts(family_id: str,current_user:UserModel,db:AsyncSession)->RestGetAllAccountsOfamilyResponse:
    #Check if the user is a member of the family
    await check_user_in_family(family_id, current_user.id, db)
    #Get family
    family = await get_family_by_id(family_id, db)
    if not family:
        return BaseRestResponse(code=0,status="FAILED",message="Family not found")
    #Return all accounts of the family from the family
    return RestGetAllAccountsOfamilyResponse(code=1,status="SUCCESS",message="Family accounts retrieved successfully",accounts=[AccountInfo(**account.__dict__) for account in family.accounts])

async def create_new_account(family_id: str,new_account:CreateAccount, current_user: UserModel, db: AsyncSession)-> RestCreateAccountResponse:
    #Check if the user is the owner of the family
    await check_user_is_family_owner(family_id, current_user.id, db)
    #Check if the family exists
    family = await get_family_by_id(family_id, db)
    if not family:
        return BaseRestResponse(code=0,status="FAILED",message="Family not found")
    #Create new account
    db_account = AccountModel(**new_account.model_dump(),family_id=family.id)
    db.add(db_account)
    try:
        await db.commit()
        await db.refresh(db_account)
        return RestCreateAccountResponse(code=1,status="SUCCESS",message="Account created successfully",account=AccountInfo(**db_account.__dict__))
    except Exception as e:
        await db.rollback()
        return BaseRestResponse(code=0,status="FAILED",message=f"Failed to create account: {str(e)}")

async def delete_account(account_id: str,current_user: UserModel, db: AsyncSession)->BaseRestResponse:
    #Check if the user is the owner of the family
    await check_user_is_family_owner(account_id, current_user.id, db)
    #Check if the account exists
    account = await get_account_by_id(account_id, db)
    if not account:
        return BaseRestResponse(code=0,status="FAILED",message="Account not found")
    #Delete account
    await db.delete(account)
    try:
        await db.commit()
        return BaseRestResponse(code=1,status="SUCCESS",message="Account deleted successfully")
    except Exception as e:
        await db.rollback()
        return BaseRestResponse(code=0,status="FAILED",message=f"Failed to delete account: {str(e)}")

async def update_account(account_id: str,updated_account:UpdateAccount,current_user: UserModel, db: AsyncSession)->RestCreateAccountResponse:
    #Check if the user is the owner of the family
    await check_user_is_family_owner(account_id, current_user.id, db)
    #Check if the account exists
    account = await get_account_by_id(account_id, db)
    if not account:
        return BaseRestResponse(code=0,status="FAILED",message="Account not found")
    #Update account
    for key, value in updated_account.model_dump(exclude_unset=True).items():
        setattr(account, key, value)
    try:
        await db.commit()
        await db.refresh(account)
        return RestCreateAccountResponse(code=1,status="SUCCESS",message="Account updated successfully",account=AccountInfo(**account.__dict__))
    except Exception as e:
        await db.rollback()
        return BaseRestResponse(code=0,status="FAILED",message=f"Failed to update account: {str(e)}")

async def get_account(account_id: str,current_user: UserModel, db: AsyncSession)->RestGetAccountResponse:
    #Check if the user is a member of the family
    await check_user_in_family(account_id, current_user.id, db)
    #Check if the account exists
    account = await get_account_by_id(account_id, db)
    if not account:
        return BaseRestResponse(code=0,status="FAILED",message="Account not found")
    #Return account
    return RestGetAccountResponse(code=1,status="SUCCESS",message="Account retrieved successfully",account=AccountInfo(**account.__dict__))

async def get_account_by_id(account_id: str, db: AsyncSession) -> AccountModel:
    """
    Asynchronously retrieves an account by its ID from the database.
    Args:
        account_id (str): The ID of the account to retrieve.
        db (AsyncSession): The asynchronous database session.
    Returns:
        AccountModel: The account object if found, otherwise None.
    """
    result = await db.execute(select(AccountModel).where(AccountModel.id == UUID(account_id)))
    account = result.scalars().first()
    return account