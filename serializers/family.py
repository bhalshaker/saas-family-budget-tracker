from pydantic import BaseModel
from .base import BaseRestResponse
from .user import UserCreationResponse
from uuid import UUID
from typing import Optional,List

class CreateFamily(BaseModel):
    name: str

class FamilyInfo(BaseModel):
    id: UUID
    name: str
    
class RestFamilyCreationResponse(BaseRestResponse):
    family: FamilyInfo

class RestGetAllFamiliesResponse(BaseRestResponse):
    families: Optional[List[FamilyInfo]]

class RestGetAllUsersInFamilyResponse(BaseRestResponse):
    family: Optional[FamilyInfo] = None
    users: Optional[List[UUID]] = None