from fastapi import APIRouter, HTTPException,Depends
from serializers import RestUserCreationResponse,CreateUser,RestGetllAllUsers
from controllers import ControllerCreateUser,ControllerUserLogin,get_current_user,ControllerUpdateUser,ControllerDeleteUser,ControllerGetAllUsers,ControllerGetUser
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from serializers import UserLogin,RestUserLoginResponse,UserUpdate,BaseRestResponse,UserCreationResponse
from models import UserModel

router = APIRouter()


@router.get(path="/api/v1/users/me",response_model=RestUserCreationResponse,summary="Get current user",description="This services gets the current user")
async def get_current_user_info(current_user: UserModel = Depends(get_current_user))->RestUserCreationResponse:
    """
    Retrieves the current authenticated user's information.
    Args:
        current_user (UserModel, optional): The currently authenticated user, injected via dependency.
    Returns:
        RestUserCreationResponse: The response object containing the current user's information.
    """
    return RestUserCreationResponse(code=1,status="SUCCESSFUL",message="User retrieved successfully",user=current_user)

@router.get(path="/api/v1/users/",response_model=RestGetllAllUsers,summary="Get all users",description="This services gets all users")
async def get_all_users(db:AsyncSession=Depends(get_db)):
    """
    Asynchronously retrieves all users from the database.
    Args:
        db (AsyncSession, optional): The asynchronous database session, injected by dependency.
    Returns:
        RestUserCreationResponse: The result of the ControllerGetAllUsers function, which handles the retrieval logic.
    """

    return await ControllerGetAllUsers(db)

@router.post(path="/api/v1/users/",response_model=RestUserCreationResponse,summary="Create a user",description="This services creates a user")
async def create_user(user:CreateUser,db:AsyncSession=Depends(get_db))->RestUserCreationResponse:
    """
    Asynchronously creates a new user in the database.
    Args:
        user (CreateUser): The user data to create a new user.
        db (AsyncSession, optional): The asynchronous database session, injected by dependency.
    Returns:
        RestUserCreationResponse: The result of the user creation process, as returned by ControllerCreateUser.
    """

    created_user_retults=await ControllerCreateUser(user,db)
    return created_user_retults

@router.post("/api/v1/users/login", response_model=RestUserLoginResponse,summary="Login a user",description="This services logs in a user")
async def user_login(user: UserLogin, db: AsyncSession = Depends(get_db))->RestUserLoginResponse:
    """
    Asynchronously logs in a user by validating their credentials.
    Args:
        user (UserLogin): The user credentials to validate, typically including fields like email and password.
    Returns:
       login_response: The response object containing the login status and token if successful.
    """

    login_response = await ControllerUserLogin(user, db)
    return login_response

@router.get(path="/api/v1/users/{user_id}",response_model=RestUserCreationResponse,summary="Get a user",description="This services gets a user")
async def get_user(user_id:str,db:AsyncSession=Depends(get_db)):
    """
    Asynchronously retrieves a user by their ID from the database.
    Args:
        user_id (str): The ID of the user to retrieve.
        db (AsyncSession, optional): The asynchronous database session, injected by dependency.
    Returns:
        RestUserCreationResponse: The result of the ControllerGetUser function, which handles the retrieval logic.
    """

    return await ControllerGetUser(user_id,db)

@router.put(path="/api/v1/users/{user_id}",response_model=RestUserCreationResponse,summary="Update a user",description="This services updates a user")
async def update_user(user_id:str,updated_user:UserUpdate,current_user: UserModel = Depends(get_current_user),db:AsyncSession=Depends(get_db))->RestUserCreationResponse:
    """
    Asynchronously updates a user's information.
    Args:
        user_id (str): The unique identifier of the user to update.
        updated_user (UserUpdate): The data containing updated user information.
        current_user (UserModel, optional): The currently authenticated user, injected via dependency.
        db (AsyncSession, optional): The asynchronous database session, injected via dependency.
    Returns:
        RestUserCreationResponse The result of the ControllerUpdateUser function, which handles the update logic.
    """
    
    return await ControllerUpdateUser(user_id,updated_user,current_user,db)

@router.delete(path="/api/v1/users/{user_id}",response_model=BaseRestResponse,summary="Delete a user",description="This services deletes users without transactions")
async def delete_user(user_id:str,current_user: UserModel = Depends(get_current_user),db:AsyncSession=Depends(get_db))->BaseRestResponse:
    """
    Deletes a user by their user ID.
    Args:
        user_id (str): The unique identifier of the user to be deleted.
        current_user (UserModel, optional): The currently authenticated user, injected via dependency.
        db (AsyncSession, optional): The asynchronous database session, injected via dependency.
    Returns:
        BaseRestResponse: The result of the user deletion operation, as handled by ControllerUpdateUser.
    """

    return await ControllerDeleteUser(user_id,current_user,db)