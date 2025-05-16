from pydantic import BaseModel
from serializers import BaseRestResponse,UserCreationResponse
from uuid import UUID
from typing import Optional,List

class CreateFamily(BaseModel):
    name: str

class FamilyInfo(BaseModel):
    id: UUID
    name: str

class CreatedFamily(FamilyInfo):
    owner: UserCreationResponse
    
class RestFamilyCreationResponse(BaseRestResponse):
    family: CreateFamily

class RestGetAllFamiliesResponse(BaseRestResponse):
    families: Optional[List[CreatedFamily]]

class RestGetAllUsersInFamilyResponse(BaseRestResponse):
    family: Optional[FamilyInfo] = None
    users: Optional[List[UserCreationResponse]] = None