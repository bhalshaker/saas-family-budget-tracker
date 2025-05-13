from pydantic import EmailStr,computed_field,BaseModel
from serializers import BaseResponse,BaseRestResponse
from utilities import hash_a_password


class CreateUser(BaseModel):
    name:str
    email:EmailStr
    plain_password:str

    @computed_field
    @property
    def password(self) -> str:
        return hash_a_password(self.plain_password)

class UserCreationResponse(BaseResponse):
    name:str
    email:str

class RestUserCreationResponse(BaseRestResponse):
    user:UserCreationResponse = None

class UserLogin(BaseModel):
    email: str
    password: str

class UserLoginResponse(BaseResponse):
    access_token: str

class RestUserLoginResponse(BaseRestResponse):
    user: UserLoginResponse = None