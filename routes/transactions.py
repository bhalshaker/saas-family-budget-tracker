from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from controllers import get_current_user,ControllerGetAllTransactionsOfFamily,ControllerCreateTransactionForFamily
from controllers import ControllerRetrieveTransaction,ControllerUpdateTransaction,ControllerDeleteTransaction
from models import UserModel
from serializers import CreateTransaction,UpdateTransaction,BaseRestResponse,RestGetAllTransactionsOfamilyResponse,RestCreatedTransactionResponse,RestGetTransactionResponse

router = APIRouter()

@router.get("/api/v1/families/{family_id}/transactions")
async def get_all_transactions_of_family(family_id:str, db: AsyncSession = Depends(get_db))->RestGetAllTransactionsOfamilyResponse:
    return await ControllerGetAllTransactionsOfFamily(family_id=family_id, db=db)

@router.post("/api/v1/families/{family_id}/transactions")
async def create_new_transaction(family_id:str,new_transaction: CreateTransaction,current_user:UserModel=Depends(get_current_user), db: AsyncSession = Depends(get_db))->RestCreatedTransactionResponse:
    """
    Creates a new transaction for a specified family.
    Args:
        family_id (str): The unique identifier of the family for which the transaction is being created.
        new_transaction (CreateTransaction): The transaction data to be created.
        current_user (UserModel, optional): The currently authenticated user. Automatically injected by dependency.
        db (AsyncSession, optional): The asynchronous database session. Automatically injected by dependency.
    Returns:
        RestCreatedTransactionResponse: The response containing details of the newly created transaction.
    """
    
    return await ControllerCreateTransactionForFamily(family_id=family_id, new_transaction=new_transaction, current_user=current_user, db=db)

@router.get("/api/v1/transactions/{transaction_id}")
async def get_transaction(transaction_id:str, current_user:UserModel=Depends(get_current_user), db: AsyncSession = Depends(get_db))->RestGetTransactionResponse:
    """
    Retrieve a specific transaction by its ID for the current authenticated user.
    Args:
        transaction_id (str): The unique identifier of the transaction to retrieve.
        current_user (UserModel, optional): The currently authenticated user, injected by dependency.
        db (AsyncSession, optional): The asynchronous database session, injected by dependency.
    Returns:
        RestGetTransactionResponse: The response object containing the transaction details.
    """
    
    return await ControllerRetrieveTransaction(transaction_id=transaction_id, current_user=current_user, db=db)

@router.put("/api/v1/transactions/{transaction_id}")
async def update_transaction(transaction_id:str, update_category:UpdateTransaction,current_user:UserModel=Depends(get_current_user), db: AsyncSession = Depends(get_db))->RestCreatedTransactionResponse:
    """
    Update an existing transaction with new data.
    Args:
        transaction_id (str): The unique identifier of the transaction to update.
        update_category (UpdateTransaction): The data to update the transaction with.
        current_user (UserModel, optional): The currently authenticated user. Injected by dependency.
        db (AsyncSession, optional): The database session. Injected by dependency.
    Returns:
        RestCreatedTransactionResponse: The updated transaction response.
    """
    
    return await ControllerUpdateTransaction(transaction_id=transaction_id, updated_transaction=update_category, current_user=current_user, db=db)

@router.delete("/api/v1/transactions/{transaction_id}")
async def delete_transaction(transaction_id:str, current_user:UserModel=Depends(get_current_user), db: AsyncSession = Depends(get_db))->BaseRestResponse:
    """
    Deletes a transaction by its ID for the current authenticated user.
    Args:
        transaction_id (str): The unique identifier of the transaction to delete.
        current_user (UserModel, optional): The currently authenticated user, injected by dependency.
        db (AsyncSession, optional): The asynchronous database session, injected by dependency.
    Returns:
        BaseRestResponse: The response object indicating the result of the delete operation.
    """
    
    return await ControllerDeleteTransaction(transaction_id=transaction_id, current_user=current_user, db=db)