from fastapi import APIRouter, HTTPException,Depends
from serializers import RestUserCreationResponse,CreateUser
from controllers import create_user as ControllerCreateUser
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db

router = APIRouter()

@router.post(path="/",response_model=RestUserCreationResponse,summary="Create a user",description="This services creates a user")
async def create_user(user:CreateUser,db:AsyncSession=Depends(get_db)):
    created_user=await ControllerCreateUser(user.model_dump(),db)
    return RestUserCreationResponse(code=1,status='SUCCESSFUL',message='User was created successfully',user=created_user)