from models import UserModel
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import StreamingResponse
from fastapi import UploadFile
from serializers import RestCreateAttachmentResponse, RestGetAttachmentOfTransactionResponse, BaseRestResponse

async def get_attachement_of_transaction(transaction_id: str, current_user: UserModel, db: AsyncSession)->RestGetAttachmentOfTransactionResponse:
    pass

async def upload_attachment_for_transaction(transaction_id: str, file: UploadFile, current_user: UserModel, db: AsyncSession)-> RestCreateAttachmentResponse:
    pass

async def retrieve_attachment(attachment_id: str, current_user: UserModel, db: AsyncSession)-> StreamingResponse:
    pass

async def delete_attachment(attachment_id: str, current_user: UserModel, db: AsyncSession)->BaseRestResponse:
    pass