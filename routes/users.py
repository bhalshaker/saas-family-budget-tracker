from fastapi import APIRouter, HTTPException,Depends
from serializers import RestUserCreationResponse,CreateUser
from controllers import create_user as ControllerCreateUser,user_login as ControllerUserLogin
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from serializers import UserLogin,RestUserLoginResponse

router = APIRouter()

@router.post(path="/",response_model=RestUserCreationResponse,summary="Create a user",description="This services creates a user")
async def create_user(user:CreateUser,db:AsyncSession=Depends(get_db)):
    created_user=await ControllerCreateUser(user,db)
    return RestUserCreationResponse(code=1,status='SUCCESSFUL',message='User was created successfully',user=created_user)

@router.post("/login", response_model=RestUserLoginResponse)
async def user_login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    """
    Asynchronously logs in a user by validating their credentials.
    Args:
        user (UserLogin): The user credentials to validate, typically including fields like email and password.
    Returns:
       login_response: The response object containing the login status and token if successful.
    """
    login_response = await ControllerUserLogin(user, db)
    return login_response