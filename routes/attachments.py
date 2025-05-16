from fastapi import APIRouter, Depends,UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from controllers import get_current_user,ControllerGetAttachementOfTransaction,ControllerUploadAttachmentForTransaction,ControllerRetrieveAttachment,ControllerDeleteAttachment
from models import UserModel
from serializers import RestGetAttachmentOfTransactionResponse,RestCreateAttachmentResponse,BaseRestResponse

router = APIRouter()

# Get an attachment of a transaction /api/v1/transactions/{transaction_id}/attachments
@router.get(path="/api/v1/transactions/{transaction_id}/attachments",response_model=RestGetAttachmentOfTransactionResponse, description="Get an attachment of a transaction",summary="Get an attachment of a transaction")
async def get_attachment_of_transaction(transaction_id: str, current_user: UserModel = Depends(get_current_user), db: AsyncSession = Depends(get_db)) -> RestGetAttachmentOfTransactionResponse:
    """
    Get an attachment of a transaction.
    
    Args:
        transaction_id (str): The ID of the transaction.
        current_user (UserModel, optional): The currently authenticated user. Automatically injected by dependency.
        db (AsyncSession, optional): The asynchronous database session. Automatically injected by dependency.
    
    Returns:
        RestGetAttachmentOfTransactionResponse: The response containing the attachment information.
    """
    return await ControllerGetAttachementOfTransaction(transaction_id=transaction_id, current_user=current_user, db=db)

# Upload an attachment for a transaction /api/v1/transactions/{transaction_id}/attachments using fastapi UploadFile class
@router.post(path="/api/v1/transactions/{transaction_id}/attachments",response_model=RestCreateAttachmentResponse, description="Upload an attachment for a transaction",summary="Upload an attachment for a transaction")
async def upload_attachment_for_transaction(transaction_id: str, file: UploadFile, current_user: UserModel = Depends(get_current_user), db: AsyncSession = Depends(get_db)) -> RestCreateAttachmentResponse:
    """
    Upload an attachment for a transaction.
    
    Args:
        transaction_id (str): The ID of the transaction.
        file (UploadFile): The file to be uploaded.
        current_user (UserModel, optional): The currently authenticated user. Automatically injected by dependency.
        db (AsyncSession, optional): The asynchronous database session. Automatically injected by dependency.
    
    Returns:
        RestGetAttachmentOfTransactionResponse: The response containing the attachment information.
    """
    return await ControllerUploadAttachmentForTransaction(transaction_id=transaction_id, file=file,current_user=current_user, db=db)

# Retrieve an attachment /api/v1/attachments/{attachment_id} as StreamingResponse
@router.get(path="/api/v1/attachments/{attachment_id}",description="Retrieve an attachment",summary="Retrieve an attachment")
async def retrieve_attachment(attachment_id: str, current_user: UserModel = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """
    Retrieve an attachment.
    
    Args:
        attachment_id (str): The ID of the attachment.
        current_user (UserModel, optional): The currently authenticated user. Automatically injected by dependency.
        db (AsyncSession, optional): The asynchronous database session. Automatically injected by dependency.
    
    Returns:
        StreamingResponse: The response containing the attachment file.
    """
    return await ControllerRetrieveAttachment(attachment_id=attachment_id, current_user=current_user, db=db)

# Delete an attachment /api/v1/attachments/{attachment_id}
@router.delete(path="/api/v1/attachments/{attachment_id}",response_model=BaseRestResponse,description="Delete an attachment",summary="Delete an attachment")
async def delete_attachment(attachment_id: str, current_user: UserModel = Depends(get_current_user), db: AsyncSession = Depends(get_db)) -> BaseRestResponse:
    """
    Delete an attachment.
    
    Args:
        attachment_id (str): The ID of the attachment.
        current_user (UserModel, optional): The currently authenticated user. Automatically injected by dependency.
        db (AsyncSession, optional): The asynchronous database session. Automatically injected by dependency.
    
    Returns:
        BaseRestResponse: The response indicating the result of the deletion.
    """
    return await ControllerDeleteAttachment(attachment_id=attachment_id, current_user=current_user, db=db)