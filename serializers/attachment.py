from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from .base import BaseRestResponse
from datetime import datetime

class AttachmentInfo(BaseModel):
    id: UUID
    transaction_id: UUID
    upload_date:datetime

class RestCreateAttachmentResponse(BaseRestResponse):
    attachment: Optional[AttachmentInfo]=None

class RestGetAttachmentOfTransactionResponse(RestCreateAttachmentResponse):
    attachtment: Optional[AttachmentInfo]=None