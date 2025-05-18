from pydantic import BaseModel
from models import EntryType
from typing import Optional,List
from .base import BaseRestResponse
from uuid import UUID

class CreateCategory(BaseModel):
    name: str
    type: EntryType


class UpdateCategory(BaseModel):
    name: Optional[str] = None
    type: Optional[EntryType] = None

class CreatedCategory(BaseModel):
    id: UUID
    name: str
    type: EntryType
    family_id: UUID

class  RestCreateCategoryResponse(BaseRestResponse):
    category: Optional[CreatedCategory]=None

class RestGetCategoryResponse(BaseRestResponse):
    category: Optional[CreatedCategory]=None

class RestGetAllCategoriesOfamilyResponse(BaseRestResponse):
    categories: Optional[List[CreatedCategory]]=None