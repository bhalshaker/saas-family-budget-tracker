from sqlalchemy import Column,LargeBinary,UUID,ForeignKey
from .base import BaseModel

class Attachement(BaseModel):
    __tablename__ = "attachments"
    transaction_id=Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    file_content = Column(LargeBinary, nullable=False)