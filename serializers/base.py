from pydantic import BaseModel,ConfigDict


class BaseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class BaseRestResponse(BaseModel):
    code:int
    status:str
    message:str