# Import necessary libraries 
import uuid
from datetime import datetime, timezone
from sqlalchemy.orm import declarative_base 
from sqlalchemy import Column, DateTime, Integer, func,UUID,Enum
from enum import Enum

Base= declarative_base()

class BaseModel(Base):
    """
    BaseModel is an abstract base class for all database models in the application.
    Attributes:
        id (UUID): The primary key for the model, automatically generated as a UUID.
        created_at (DateTime): The timestamp when the record was created, defaults to the current time.
        modified_at (DateTime): The timestamp when the record was last modified, automatically updated on changes.
    """
    __abstract__ = True
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, default=func.now())
    modified_at = Column(DateTime, default=func.now(), onupdate=func.now())

class EntryType(Enum):
    INCOME = "income"
    EXPENSE = "expense"
    TRANSFER = "transfer"