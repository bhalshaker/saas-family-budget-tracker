from sqlalchemy import Column,LargeBinary,UUID,ForeignKey,DateTime,func
from sqlalchemy.orm import relationship
from .base import BaseModel

class AttachementModel(BaseModel):
    """
    AttachementModel represents the database model for storing file attachments 
    associated with transactions.
    Attributes:
        __tablename__ (str): The name of the database table, "attachments".
        transaction_id (UUID): A foreign key referencing the ID of a user in the "users" table.
        file_content (LargeBinary): The binary content of the uploaded file.
        upload_date (DateTime): The timestamp when the file was uploaded. Defaults to the current time.
        transaction (relationship): A relationship to the TransactionModel, allowing access to 
            the associated transaction for this attachment.
    """
    
    __tablename__ = "attachments"
    transaction_id=Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    file_content = Column(LargeBinary, nullable=False)
    upload_date=Column(DateTime(),default=func.now(),nullable=False)
    transaction=relationship('TransactionModel',back_populates='attachment')