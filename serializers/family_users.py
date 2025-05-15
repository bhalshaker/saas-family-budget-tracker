from pydantic import BaseModel
from models import FamilyUserRole

class AddUserToFamily(BaseModel):
    user_id: str
    user_role: FamilyUserRole