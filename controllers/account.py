from sqlalchemy.future import select
from models import UserModel,AccountModel
from serializers import CreateAccount,AccountInfo
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from serializers import RestCreateAccountResponse, RestGetAccountResponse, RestGetAllAccountsOfamilyResponse, BaseRestResponse,UpdateAccount
from .authorization import check_user_in_family,check_user_is_family_owner
from .family import get_family_by_id_with_account
from uuid import UUID

async def get_all_family_accounts(family_id: str,current_user:UserModel,db:AsyncSession)->RestGetAllAccountsOfamilyResponse:
    """
    Retrieve all accounts associated with a specific family.
    Args:
        family_id (str): The unique identifier of the family.
        current_user (UserModel): The user making the request.
        db (AsyncSession): The asynchronous database session.
    Returns:
        RestGetAllAccountsOfamilyResponse: A response object containing the status, message, and a list of family accounts.
            If the family is not found, returns a response with code 0 and status "FAILED".
            On success, returns code 1, status "SUCCESS", and the list of accounts.
    Raises:
        Exception: If the user is not a member of the specified family.
    """

    #Check if the user is a member of the family
    await check_user_in_family(family_id, current_user.id, db)
    #Get family
    family = await get_family_by_id_with_account(family_id, db)
    if not family:
        return BaseRestResponse(code=0,status="FAILED",message="Family not found")
    #Return all accounts of the family from the family
    return RestGetAllAccountsOfamilyResponse(code=1,status="SUCCESS",message="Family accounts retrieved successfully",accounts=[AccountInfo(**account.__dict__) for account in family.account])

async def create_new_account(family_id: str,new_account:CreateAccount, current_user: UserModel, db: AsyncSession)-> RestCreateAccountResponse:
    """
    Creates a new account for a given family.
    This function checks if the current user is the owner of the specified family,
    verifies the existence of the family, and then creates a new account associated
    with that family. If the account creation is successful, it returns a success
    response with the account information; otherwise, it returns a failure response.
    Args:
        family_id (str): The ID of the family for which the account is to be created.
        new_account (CreateAccount): The data required to create a new account.
        current_user (UserModel): The user attempting to create the account.
        db (AsyncSession): The asynchronous database session.
    Returns:
        RestCreateAccountResponse: A response object containing the result of the account creation operation.
    """

    #Check if the user is the owner of the family
    await check_user_is_family_owner(family_id, current_user.id, db)
    #Check if the family exists
    family = await get_family_by_id_with_account(family_id, db)
    if not family:
        return BaseRestResponse(code=0,status="FAILED",message="Family not found")
    #Create new account
    db_account = AccountModel(**new_account.model_dump(),family_id=family.id,user_id=current_user.id)
    print(db_account)
    db.add(db_account)
    try:
        await db.commit()
        await db.refresh(db_account)
        return RestCreateAccountResponse(code=1,status="SUCCESS",message="Account created successfully",account=AccountInfo(**db_account.__dict__))
    except Exception as e:
        await db.rollback()
        return RestCreateAccountResponse(code=0,status="FAILED",message=f"Failed to create account: {str(e)}")

async def delete_account(account_id: str,current_user: UserModel, db: AsyncSession)->BaseRestResponse:
    """
    Asynchronously deletes an account if the current user is the owner of the associated family.
    Args:
        account_id (str): The unique identifier of the account to be deleted.
        current_user (UserModel): The user attempting to delete the account.
        db (AsyncSession): The asynchronous database session.
    Returns:
        BaseRestResponse: A response object indicating the result of the deletion operation.
            - If the account does not exist, returns a response with code 0 and status "FAILED".
            - If the deletion is successful, returns a response with code 1 and status "SUCCESS".
            - If an error occurs during deletion, returns a response with code 0 and status "FAILED" along with the error message.
    Raises:
        Exception: If the user is not the owner of the family, an exception may be raised by `check_user_is_family_owner`.
    """

    #Check if the user is the owner of the family
    account = await get_account_by_id(account_id, db)
    if not account:
        return BaseRestResponse(code=0,status="FAILED",message="Account not found")
    await check_user_is_family_owner(str(account.family_id), current_user.id, db)
    #Delete account
    await db.delete(account)
    try:
        await db.commit()
        return BaseRestResponse(code=1,status="SUCCESS",message="Account deleted successfully")
    except Exception as e:
        await db.rollback()
        return BaseRestResponse(code=0,status="FAILED",message=f"Failed to delete account: {str(e)}")

async def update_account(account_id: str,updated_account:UpdateAccount,current_user: UserModel, db: AsyncSession)->RestCreateAccountResponse:
    """
    Updates an existing account with new information.
    Args:
        account_id (str): The unique identifier of the account to update.
        updated_account (UpdateAccount): The data containing updated account fields.
        current_user (UserModel): The user performing the update operation.
        db (AsyncSession): The asynchronous database session.
    Returns:
        RestCreateAccountResponse: A response object containing the status and details of the update operation.
    Raises:
        Exception: If the update operation fails due to a database error or other unexpected issues.
    Notes:
        - Checks if the current user is the owner of the family associated with the account.
        - Verifies the existence of the account before attempting an update.
        - Only updates fields provided in `updated_account` (fields not set are ignored).
    """

    #Check if the user is the owner of the family
    account = await get_account_by_id(account_id, db)
    if not account:
        return BaseRestResponse(code=0,status="FAILED",message="Account not found")
    await check_user_is_family_owner(str(account.family_id), current_user.id, db)
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
    """
    Retrieve account information for a given account ID, ensuring the current user is a member of the associated family.
    Args:
        account_id (str): The unique identifier of the account to retrieve.
        current_user (UserModel): The currently authenticated user making the request.
        db (AsyncSession): The asynchronous database session for performing queries.
    Returns:
        RestGetAccountResponse: A response object containing the account information if found and accessible,
        or an error message if the account does not exist or the user is not authorized.
    Raises:
        HTTPException: If the user is not a member of the family associated with the account.
    """

    #Check if the user is a member of the family
    account = await get_account_by_id(account_id, db)
    if not account:
        return BaseRestResponse(code=0,status="FAILED",message="Account not found")
    await check_user_in_family(str(account.family_id), current_user.id, db)
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