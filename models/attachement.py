from sqlalchemy import Column,LargeBinary,UUID,ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel

class AttachementModel(BaseModel):
    __tablename__ = "attachments"
    transaction_id=Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    file_content = Column(LargeBinary, nullable=False)
    transaction=relationship('TransactionModel',back_populates='attachment')