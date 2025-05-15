from pydantic import BaseModel
from models import EntryType
from typing import Optional

class CreateCategory(BaseModel):
    name: str
    type: EntryType


class UpdateCategory(BaseModel):
    name: Optional[str] = None
    type: Optional[EntryType] = None