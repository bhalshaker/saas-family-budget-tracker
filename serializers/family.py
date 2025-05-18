from pydantic import BaseModel
from .base import BaseRestResponse
from uuid import UUID
from typing import Optional,List

class CreateFamily(BaseModel):
    name: str

class FamilyInfo(BaseModel):
    id: UUID
    name: str
    
class RestFamilyCreationResponse(BaseRestResponse):
    family: Optional[FamilyInfo]=None

class RestGetAllFamiliesResponse(BaseRestResponse):
    families: Optional[List[FamilyInfo]]=None

class RestGetAllUsersInFamilyResponse(BaseRestResponse):
    family: Optional[FamilyInfo] = None
    users: Optional[List[UUID]] = None