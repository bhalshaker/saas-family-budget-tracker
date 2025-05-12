from pydantic import BaseModel
from dotenv import dotenv_values

class Config(BaseModel):
    db_host:str
    db_port:str
    db_user:str
    db_password:str
    db_name:str
    token_secret:str

config_env=dotenv_values(".env")

config=Config(**config_env)