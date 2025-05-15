from pydantic import BaseModel

class AddUserToFamily(BaseModel):
    user_id: str
    user_role: str