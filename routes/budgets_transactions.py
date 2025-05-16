from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from controllers import get_current_user
from models import UserModel
from serializers import CreateBudgetTransaction, RestGetAllBudgetTransactionsOfamilyResponse, RestCreateBudgetTransactionResponse, RestGetBudgetTransactionResponse, BaseRestResponse
from controllers import ControllerGetAllBudgetTransactionsOfFamily, ControllerAddBudgetTransactionForFamily, ControllerRetrieveBudgetTransaction, ControllerDeleteBudgetTransaction

router = APIRouter()

#GET all budget transactions of a family
@router.get(path="/api/v1/families/{family_id}/budget_transactions", response_model=RestGetAllBudgetTransactionsOfamilyResponse, summary="Get all budget transactions of a family", description="Retrieve all budget transactions associated with a specific family.")
async def get_all_budget_transactions_of_family(family_id: str, current_user: UserModel = Depends(get_current_user), db: AsyncSession = Depends(get_db)) -> RestGetAllBudgetTransactionsOfamilyResponse:
    """
    Retrieve all budget transactions associated with a specific family.
    Args:
        family_id (str): The unique identifier of the family whose budget transactions are to be retrieved.
        current_user (UserModel, optional): The currently authenticated user, injected by dependency. Defaults to Depends(get_current_user).
        db (AsyncSession, optional): The asynchronous database session, injected by dependency. Defaults to Depends(get_db).
    Returns:
        RestGetAllBudgetTransactionsOfamilyResponse: The response object containing all budget transactions for the specified family.
    """

    return await ControllerGetAllBudgetTransactionsOfFamily(family_id=family_id, current_user=current_user, db=db)

#POST a new budget transaction for a family
@router.post(path="/api/v1/families/{family_id}/budget_transactions", response_model=RestCreateBudgetTransactionResponse, summary="Create a new budget transaction", description="Create a new budget transaction for a specified family.")
async def create_budget_transaction(family_id: str, new_budget_transaction: CreateBudgetTransaction, current_user: UserModel = Depends(get_current_user), db: AsyncSession = Depends(get_db)) -> RestCreateBudgetTransactionResponse:
    """
    Creates a new budget transaction for a specified family.
    Args:
        family_id (str): The unique identifier of the family for which the transaction is being created.
        new_budget_transaction (CreateBudgetTransaction): The data for the new budget transaction.
        current_user (UserModel, optional): The currently authenticated user. Automatically provided by dependency injection.
        db (AsyncSession, optional): The asynchronous database session. Automatically provided by dependency injection.
    Returns:
        RestCreateBudgetTransactionResponse: The response containing the details of the created budget transaction.
    """

    return await ControllerAddBudgetTransactionForFamily(family_id=family_id, new_budget_transaction=new_budget_transaction, current_user=current_user, db=db)

# GET a specific budget transaction
@router.get(path="/api/v1/budget_transactions/{budget_transaction_id}", response_model=RestGetBudgetTransactionResponse, summary="Get a budget transaction", description="Retrieve a specific budget transaction by its ID.")
async def get_budget_transaction(budget_transaction_id: str, current_user: UserModel = Depends(get_current_user), db: AsyncSession = Depends(get_db)) -> RestGetBudgetTransactionResponse:
    """
    Retrieve a specific budget transaction by its ID.
    Args:
        budget_transaction_id (str): The unique identifier of the budget transaction to retrieve.
        current_user (UserModel, optional): The currently authenticated user, injected by dependency.
        db (AsyncSession, optional): The asynchronous database session, injected by dependency.
    Returns:
        RestGetBudgetTransactionResponse: The response object containing the requested budget transaction details.
    """

    return await ControllerRetrieveBudgetTransaction(budget_transaction_id=budget_transaction_id, current_user=current_user, db=db)

#DELETE a specific budget transaction
@router.delete(path="/api/v1/budget_transactions/{budget_transaction_id}", response_model=BaseRestResponse, summary="Delete a budget transaction", description="Delete a specific budget transaction by its ID.")
async def delete_budget_transaction(budget_transaction_id: str, current_user: UserModel = Depends(get_current_user), db: AsyncSession = Depends(get_db)) -> BaseRestResponse:
    """
    Deletes a budget transaction by its ID.
    Args:
        budget_transaction_id (str): The unique identifier of the budget transaction to delete.
        current_user (UserModel, optional): The currently authenticated user, injected by dependency.
        db (AsyncSession, optional): The asynchronous database session, injected by dependency.
    Returns:
        BaseRestResponse: The response object indicating the result of the delete operation.
    """

    return await ControllerDeleteBudgetTransaction(budget_transaction_id=budget_transaction_id, current_user=current_user, db=db)