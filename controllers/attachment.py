from models import UserModel
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import StreamingResponse
from fastapi import UploadFile

async def get_all_attachements_of_transaction(transaction_id: str, current_user: UserModel, db: AsyncSession):
    pass

async def upload_attachment_for_transaction(transaction_id: str, file: UploadFile, current_user: UserModel, db: AsyncSession):
    pass

async def retrieve_attachment(attachment_id: str, current_user: UserModel, db: AsyncSession)-> StreamingResponse:
    pass

async def delete_attachment(attachment_id: str, current_user: UserModel, db: AsyncSession):
    pass