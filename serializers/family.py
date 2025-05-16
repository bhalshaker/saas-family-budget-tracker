from pydantic import BaseModel
from serializers import BaseRestResponse,UserCreationResponse
from uuid import UUID

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
    families: list[CreatedFamily]

class RestGetAllUsersInFamilyResponse(BaseRestResponse):
    family: FamilyInfo = None
    users: list[UserCreationResponse] = None