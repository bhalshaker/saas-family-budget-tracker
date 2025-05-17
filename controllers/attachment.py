from models import UserModel,AttachmentModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi.responses import StreamingResponse
from fastapi import UploadFile
from serializers import RestCreateAttachmentResponse, RestGetAttachmentOfTransactionResponse, BaseRestResponse
from serializers import AttachmentInfo
from .authorization import check_user_in_family, check_user_is_family_owner
from .family import get_family_by_id
from .transaction import get_transaction_by_id
from uuid import UUID

async def get_attachement_of_transaction(transaction_id: str, current_user: UserModel, db: AsyncSession)->RestGetAttachmentOfTransactionResponse:
    # Check if the transaction exists
    transaction = await get_transaction_by_id(transaction_id, db)
    if not transaction:
        return BaseRestResponse(code=0, status="FAILED", message="Transaction not found")
    # Check if the user is a member of the family based on the transaction
    await check_user_in_family(str(transaction.family_id), current_user.id, db)
    # Get the attachment associated with the transaction
    attachment = await get_attachment_by_id(transaction.attachment_id, db)
    if not attachment:
        return BaseRestResponse(code=0, status="FAILED", message="Attachment not found")
    return RestGetAttachmentOfTransactionResponse(code=1, status="SUCCESS", message="Attachment retrieved successfully", attachment=AttachmentInfo(**attachment.model_dump()))

async def upload_attachment_for_transaction(transaction_id: str, file: UploadFile, current_user: UserModel, db: AsyncSession)-> RestCreateAttachmentResponse:
    # Check if the transaction exists
    transaction = await get_transaction_by_id(transaction_id, db)
    if not transaction:
        return BaseRestResponse(code=0, status="FAILED", message="Transaction not found")
    # Check if the user is a member of the family based on the transaction
    await check_user_in_family(str(transaction.family_id), current_user.id, db)
    # Create new attachment
    new_attachment = AttachmentModel(**file.model_dump(), transaction_id=UUID(transaction_id), user_id=current_user.id)
    db.add(new_attachment)
    try:
        await db.commit()
        await db.refresh(new_attachment)
        return RestCreateAttachmentResponse(code=1, status="SUCCESS", message="Attachment created successfully", attachment=AttachmentInfo(**new_attachment.model_dump()))
    except Exception as e:
        await db.rollback()
        return BaseRestResponse(code=0, status="FAILED", message=f"Failed to create attachment: {str(e)}")

async def retrieve_attachment(attachment_id: str, current_user: UserModel, db: AsyncSession)-> StreamingResponse:
    #Check if the attachment exists
    attachment = await get_attachment_by_id(attachment_id, db)
    if not attachment:
        return BaseRestResponse(code=0, status="FAILED", message="Attachment not found")
    # Check if the user is a member of the family based on the attachment transaction
    await check_user_in_family(str(attachment.transaction.family_id), current_user.id, db)
    # Create a streaming response for the attachment
    response = StreamingResponse(
        iter([attachment.file_content]),
        media_type="application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename={attachment.id}"}
    )
    return response

async def delete_attachment(attachment_id: str, current_user: UserModel, db: AsyncSession)->BaseRestResponse:
    # Check if the attachment exists
    attachment = await get_attachment_by_id(attachment_id, db)
    if not attachment:
        return BaseRestResponse(code=0, status="FAILED", message="Attachment not found")
    # Check if the user is a the owner of the family based on the attachment transaction
    await check_user_is_family_owner(str(attachment.transaction.family_id), current_user.id, db)
    # Delete the attachment
    try:
        await db.delete(attachment)
        await db.commit()
        return BaseRestResponse(code=1, status="SUCCESS", message="Attachment deleted successfully")
    except Exception as e:
        await db.rollback()
        return BaseRestResponse(code=0, status="FAILED", message=f"Failed to delete attachment: {str(e)}")

async def get_attachment_by_id(attachment_id: str, db: AsyncSession)->AttachmentModel:
    """
    Retrieve an attachment by its ID from the database.
    Args:
        attachment_id (str): The unique identifier of the attachment.
        db (AsyncSession): The asynchronous database session.
    Returns:
        AttachmentModel: The attachment object if found, otherwise None.
    """
    result = await db.execute(select(AttachmentModel).where(AttachmentModel.id == attachment_id))
    return result.scalars().first()