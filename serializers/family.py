from pydantic import BaseModel
from serializers import BaseRestResponse,UserCreationResponse
from uuid import UUID

class CreateFamily(BaseModel):
    name: str

class CreatedFamily(BaseModel):
    id: UUID
    name: str
    owner: UserCreationResponse
    
class RestFamilyCreationResponse(BaseRestResponse):
    family: CreateFamily

class RestGetAllFamiliesResponse(BaseRestResponse):
    families: list[CreatedFamily]