from fastapi import FastAPI
from config.config import Settings


app=FastAPI()
#app.include_router(UsersRouter, prefix="/api") 
settings=Settings()