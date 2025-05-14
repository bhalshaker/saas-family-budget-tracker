from pydantic import EmailStr,computed_field,BaseModel
from serializers import BaseResponse,BaseRestResponse
from utilities import hash_a_password
from datetime import datetime
from typing import Optional
from uuid import UUID


class CreateUser(BaseModel):
    name:str
    email:EmailStr
    plain_password:str

    @computed_field
    @property
    def password(self) -> str:
        return hash_a_password(self.plain_password)

class UserUpdate(BaseModel):
    name: Optional[str] = None
    plain_password: Optional[bool] = None

    @computed_field
    @property
    def password(self) -> Optional[str]:
        if self.plain_password:
            return hash_a_password(self.plain_password)
        return None

class UserCreationResponse(BaseResponse):
    id: UUID
    name:str
    email:str

class RestUserCreationResponse(BaseRestResponse):
    user:UserCreationResponse = None

class UserLogin(BaseModel):
    email: str
    password: str

class UserLoginResponse(BaseResponse):
    issued_at: datetime
    expires_at: datetime
    apikey: str
    @computed_field
    @property
    def authorization(self) -> str:
        return f"Bearer {self.apikey}"

class RestUserLoginResponse(BaseRestResponse):
    user_key: UserLoginResponse = None

class RestGetllAllUsers(BaseRestResponse):
    users: list[UserCreationResponse]