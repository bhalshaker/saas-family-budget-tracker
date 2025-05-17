from models import UserModel,BudgetTransactionModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from serializers import CreateBudgetTransaction, RestGetAllBudgetTransactionsOfamilyResponse, RestCreateBudgetTransactionResponse, RestGetBudgetTransactionResponse, BaseRestResponse
from serializers import BudgetTransactionInfo
from uuid import UUID
from .authorization import check_user_in_family,check_user_is_family_owner
from .family import get_family_by_id

async def get_all_budget_transactions_of_family(family_id: str, current_user: UserModel, db: AsyncSession)->RestGetAllBudgetTransactionsOfamilyResponse:
    """
    Retrieve all budget transactions associated with a specific family.
    Args:
        family_id (str): The unique identifier of the family.
        current_user (UserModel): The currently authenticated user.
        db (AsyncSession): The asynchronous database session.
    Returns:
        RestGetAllBudgetTransactionsOfamilyResponse: Response object containing the status, message, and a list of budget transactions for the family.
    Raises:
        HTTPException: If the user is not a member of the family or if the family does not exist.
    """

    # Check if the user is a member of the family
    await check_user_in_family(family_id, current_user.id, db)
    # Get family
    family = await get_family_by_id(family_id, db)
    if not family:
        return BaseRestResponse(code=0, status="FAILED", message="Family not found")
    # Return all budget transactions of the family from the family
    return RestGetAllBudgetTransactionsOfamilyResponse(code=1, status="SUCCESS", message="Family budget transactions retrieved successfully", budget_transactions=[BudgetTransactionInfo(**budget_transaction) for budget_transaction in family.budget_transactions])

async def add_budget_transaction_for_family(family_id: str, new_budget_transaction: CreateBudgetTransaction, current_user: UserModel, db: AsyncSession)-> RestCreateBudgetTransactionResponse:
    """
    Asynchronously adds a new budget transaction for a specified family.
    Args:
        family_id (str): The unique identifier of the family.
        new_budget_transaction (CreateBudgetTransaction): The data for the new budget transaction to be created.
        current_user (UserModel): The user performing the operation.
        db (AsyncSession): The asynchronous database session.
    Returns:
        RestCreateBudgetTransactionResponse: A response object containing the status and details of the created budget transaction, or an error message if the operation fails.
    Raises:
        Exception: If the database operation fails, an exception is caught and a failure response is returned.
    Notes:
        - Checks if the current user is a member of the specified family before proceeding.
        - Rolls back the transaction if any error occurs during the commit.
    """

    # Check if the user is a member of the family
    await check_user_in_family(family_id, current_user.id, db)
    # Get family
    family = await get_family_by_id(family_id, db)
    if not family:
        return BaseRestResponse(code=0, status="FAILED", message="Family not found")
    # Create new budget transaction
    new_budget_transaction = BudgetTransactionModel(**new_budget_transaction.model_dump(), family_id=UUID(family.id), user_id=current_user.id)
    db.add(new_budget_transaction)
    try:
        await db.commit()
        await db.refresh(new_budget_transaction)
        return RestCreateBudgetTransactionResponse(code=1, status="SUCCESS", message="Budget transaction created successfully", budget_transaction=BudgetTransactionInfo(**new_budget_transaction.model_dump()))
    except:
        await db.rollback()
        return BaseRestResponse(code=0, status="FAILED", message="Failed to create budget transaction")

async def retrieve_budget_transaction(budget_transaction_id: str, current_user: UserModel, db: AsyncSession)->RestGetBudgetTransactionResponse:
    """
    Retrieve a budget transaction by its ID.
    Args:
        budget_transaction_id (str): The unique identifier of the budget transaction.
        current_user (UserModel): The currently authenticated user.
        db (AsyncSession): The asynchronous database session.
    Returns:
        RestGetBudgetTransactionResponse: Response object containing the status, message, and details of the retrieved budget transaction.
    Raises:
        HTTPException: If the user is not a member of the family or if the budget transaction does not exist.
    """

    # Check if the user is a member of the family
    await check_user_in_family(budget_transaction_id, current_user.id, db)
    # Get budget transaction
    budget_transaction = await get_budget_transaction_by_id(budget_transaction_id, db)
    if not budget_transaction:
        return BaseRestResponse(code=0, status="FAILED", message="Budget transaction not found")
    return RestGetBudgetTransactionResponse(code=1, status="SUCCESS", message="Budget transaction retrieved successfully", budget_transaction=BudgetTransactionInfo(**budget_transaction.model_dump()))

async def delete_budget_transaction(budget_transaction_id: str, current_user: UserModel, db: AsyncSession)->BaseRestResponse:
    """
    Asynchronously deletes a budget transaction if the current user is the owner of the associated family.
    Args:
        budget_transaction_id (str): The unique identifier of the budget transaction to be deleted.
        current_user (UserModel): The user attempting to delete the budget transaction.
        db (AsyncSession): The asynchronous database session.
    Returns:
        BaseRestResponse: A response object indicating the result of the deletion operation.
            - If the budget transaction does not exist, returns a response with code 0 and status "FAILED".
            - If the deletion is successful, returns a response with code 1 and status "SUCCESS".
            - If an error occurs during deletion, returns a response with code 0 and status "FAILED" along with the error message.
    Raises:
        Exception: If the user is not the owner of the family, an exception may be raised by `check_user_is_family_owner`.
    """

    # Check if the user is the owner member of the family
    await check_user_is_family_owner(budget_transaction_id, current_user.id, db)
    # Get budget transaction
    budget_transaction = await get_budget_transaction_by_id(budget_transaction_id, db)
    if not budget_transaction:
        return BaseRestResponse(code=0, status="FAILED", message="Budget transaction not found")
    # Delete budget transaction
    await db.delete(budget_transaction)
    try:
        await db.commit()
        return BaseRestResponse(code=1, status="SUCCESS", message="Budget transaction deleted successfully")
    except:
        await db.rollback()
        return BaseRestResponse(code=0, status="FAILED", message="Failed to delete budget transaction")

async def get_budget_transaction_by_id(budget_transaction_id: str, db: AsyncSession)->BudgetTransactionModel:
    """
    Retrieve a budget transaction by its ID.
    Args:
        budget_transaction_id (str): The unique identifier of the budget transaction.
        db (AsyncSession): The asynchronous database session.
    Returns:
        BudgetTransactionModel: The budget transaction object if found, None otherwise.
    """
    result = await db.execute(select(BudgetTransactionModel).where(BudgetTransactionModel.id == UUID(budget_transaction_id)))
    return result.scalars().first()