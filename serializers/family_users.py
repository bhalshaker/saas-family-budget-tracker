from pydantic import BaseModel
from models import FamilyUserRole
from .base import BaseRestResponse
from .family import FamilyInfo
from uuid import UUID
from datetime import datetime
from typing import Optional,List


class FamilyUserInfo(BaseModel):
    id: UUID
    family_id: UUID
    user_id:UUID
    user_role: FamilyUserRole
    joined_at: datetime

class AddUserToFamily(BaseModel):
    user_id: str
    user_role: FamilyUserRole

class RestAddUserToFamilyResponse(BaseRestResponse):
    family_user_info: FamilyUserInfo

class RestGetFamiliesUserBelongsToResponse(BaseRestResponse):
    #families=Optional[List[FamilyInfo]] = None
    family_users: Optional[List[FamilyUserInfo]] = None