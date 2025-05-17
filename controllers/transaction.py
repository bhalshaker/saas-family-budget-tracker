from models import UserModel,TransactionModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from serializers import CreateTransaction, UpdateTransaction, RestCreatedTransactionResponse, RestGetTransactionResponse, RestGetAllTransactionsOfamilyResponse, BaseRestResponse
from serializers import TransactionInfo
from .authorization import check_user_in_family, check_user_is_family_owner
from .family import get_family_by_id
from uuid import UUID

async def get_all_transactions_of_family(family_id: str, current_user: UserModel, db: AsyncSession)->RestGetAllTransactionsOfamilyResponse:
    """
    Retrieve all transactions associated with a specific family.
    Args:
        family_id (str): The unique identifier of the family.
        current_user (UserModel): The currently authenticated user.
        db (AsyncSession): The asynchronous database session.
    Returns:
        RestGetAllTransactionsOfamilyResponse: A response object containing the status, message, and a list of transactions for the specified family.
    Raises:
        HTTPException: If the user is not a member of the family or if the family does not exist.
    Notes:
        - The function first checks if the current user is a member of the specified family.
        - If the family exists, it retrieves and returns all transactions associated with the family.
    """

    # Check if the user is a member of the family
    await check_user_in_family(family_id, current_user.id, db)
    # Get family
    family = await get_family_by_id(family_id, db)
    if not family:
        return BaseRestResponse(code=0, status="FAILED", message="Family not found")
    # Return all transactions of the family from the family
    return RestGetAllTransactionsOfamilyResponse(code=1, status="SUCCESS", message="Family transactions retrieved successfully", transactions=[TransactionInfo(**transaction) for transaction in family.transactions])

async def create_transaction_for_family(family_id: str, new_transaction: CreateTransaction, current_user: UserModel, db: AsyncSession)-> RestCreatedTransactionResponse:
    """
    Creates a new transaction for a specified family if the current user is the family owner.
    Args:
        family_id (str): The UUID of the family for which the transaction is being created.
        new_transaction (CreateTransaction): The transaction data to be created.
        current_user (UserModel): The user attempting to create the transaction.
        db (AsyncSession): The asynchronous database session.
    Returns:
        RestCreatedTransactionResponse: Response containing the created transaction info on success.
        BaseRestResponse: Response with error message on failure.
    Raises:
        Exception: If the transaction creation fails or the user is not a member of th family.
    """

    # Check if the user is a member of the family
    await check_user_in_family(family_id, current_user.id, db)
    # Create new transaction
    new_transaction = TransactionModel(**new_transaction.model_dump(), family_id=UUID(family_id), user_id=current_user.id)
    db.add(new_transaction)
    try:
        await db.commit()
        await db.refresh(new_transaction)
        return RestCreatedTransactionResponse(code=1, status="SUCCESS", message="Transaction created successfully", transaction=TransactionInfo(**new_transaction.model_dump()))
    except Exception as e:
        await db.rollback()
        return BaseRestResponse(code=0, status="FAILED", message=f"Failed to create transaction: {str(e)}")

async def retrieve_transaction(transaction_id: str, current_user: UserModel, db: AsyncSession)-> RestGetTransactionResponse:
    """
    Retrieve a transaction by its ID for the current user.
    This function checks if the current user is a member of the family associated with the transaction,
    retrieves the transaction from the database, and returns a response containing the transaction details.
    Args:
        transaction_id (str): The unique identifier of the transaction to retrieve.
        current_user (UserModel): The user requesting the transaction.
        db (AsyncSession): The asynchronous database session.
    Returns:
        RestGetTransactionResponse: A response object containing the transaction details if found,
        or an error message if the transaction does not exist or the user is not authorized.
    """

    # Check if the user is a member of the family
    await check_user_in_family(transaction_id, current_user.id, db)
    # Get transaction
    transaction = await get_transaction_by_id(transaction_id, db)
    if not transaction:
        return BaseRestResponse(code=0, status="FAILED", message="Transaction not found")
    return RestGetTransactionResponse(code=1, status="SUCCESS", message="Transaction retrieved successfully", transaction=TransactionInfo(**transaction.model_dump()))

async def update_transaction(transaction_id: str, updated_transaction: UpdateTransaction, current_user: UserModel, db: AsyncSession)->RestCreatedTransactionResponse:
    """
    Update an existing transaction for the current user.
    Args:
        transaction_id (str): The unique identifier of the transaction to update.
        updated_transaction (UpdateTransaction): The data object containing updated transaction fields.
        current_user (UserModel): The user performing the update operation.
        db (AsyncSession): The asynchronous database session.
    Returns:
        RestCreatedTransactionResponse: On success, returns a response with the updated transaction information.
        BaseRestResponse: On failure, returns a response with an error message.
    Raises:
        Exception: If the database update fails, an exception is caught and a failure response is returned.
    Notes:
        - Checks if the current user is the owner of the family associated with the transaction.
        - If the transaction does not exist, returns a failure response.
        - Updates the transaction fields with the provided data.
        - Commits the changes to the database and refreshes the transaction instance.
    """

    # Check if the user is the owner of the family
    await check_user_is_family_owner(transaction_id, current_user.id, db)
    # Get transaction
    transaction = await get_transaction_by_id(transaction_id, db)
    if not transaction:
        return BaseRestResponse(code=0, status="FAILED", message="Transaction not found")
    # Update transaction
    for key, value in updated_transaction.model_dump().items():
        setattr(transaction, key, value)
    try:
        await db.commit()
        await db.refresh(transaction)
        return RestCreatedTransactionResponse(code=1, status="SUCCESS", message="Transaction updated successfully", transaction=TransactionInfo(**transaction.model_dump()))
    except Exception as e:
        await db.rollback()
        return BaseRestResponse(code=0, status="FAILED", message=f"Failed to update transaction: {str(e)}")

async def delete_transaction(transaction_id: str, current_user: UserModel, db: AsyncSession)->BaseRestResponse:
    """
    Deletes a transaction by its ID after verifying the current user is the owner of the family.
    Args:
        transaction_id (str): The unique identifier of the transaction to delete.
        current_user (UserModel): The user attempting to delete the transaction.
        db (AsyncSession): The asynchronous database session.
    Returns:
        BaseRestResponse: The response object indicating the result of the deletion operation.
            - code=1, status="SUCCESS" if the transaction was deleted successfully.
            - code=0, status="FAILED" if the transaction was not found or deletion failed.
    Raises:
        Exception: If an error occurs during the database commit operation.
    """

    # Check if the user is the owner of the family
    await check_user_is_family_owner(transaction_id, current_user.id, db)
    # Get transaction
    transaction = await get_transaction_by_id(transaction_id, db)
    if not transaction:
        return BaseRestResponse(code=0, status="FAILED", message="Transaction not found")
    # Delete transaction
    await db.delete(transaction)
    try:
        await db.commit()
        return BaseRestResponse(code=1, status="SUCCESS", message="Transaction deleted successfully")
    except Exception as e:
        await db.rollback()
        return BaseRestResponse(code=0, status="FAILED", message=f"Failed to delete transaction: {str(e)}")

async def get_transaction_by_id(transaction_id: str, db: AsyncSession)->TransactionModel:
    """
    Retrieve a transaction by its ID.
    Args:
        transaction_id (str): The unique identifier of the transaction.
        db (AsyncSession): The asynchronous database session.
    Returns:
        TransactionModel: The transaction object if found, None otherwise.
    """
    result = await db.execute(select(TransactionModel).where(TransactionModel.id == UUID(transaction_id)))
    return result.scalars().first()