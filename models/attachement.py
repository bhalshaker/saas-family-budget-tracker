from sqlalchemy import Column,LargeBinary
from .base import BaseModel

class Attachement(BaseModel):
    __tablename__ = "attachments"
    file_content = Column(LargeBinary, nullable=False)