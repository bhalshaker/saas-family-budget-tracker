from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from controllers import get_current_user
from models import UserModel
from serializers import RestGetAllUsersInFamilyResponse,RestAddUserToFamilyResponse,AddUserToFamily,BaseRestResponse,RestGetFamiliesUserBelongsToResponse
from controllers import ControllerGetAllUsersInFamily,ControllerAddUserToFamily,ControllerRemoveUserFromFamily,ControllerGetFamiliesUserBelongsTo

router = APIRouter()

# Get /api/v1/families/{family_id}/users to list all users in a family
@router.get(path="/api/v1/families/{family_id}/users", response_model=RestGetAllUsersInFamilyResponse, summary="Get all users in a family", description="This service gets all users in a family")
async def get_all_users_in_family(family_id: str, current_user: UserModel = Depends(get_current_user), db: AsyncSession = Depends(get_db)) -> RestGetAllUsersInFamilyResponse:
    """
    Asynchronously retrieves all users in a specified family.
    Args:
        family_id (str): The ID of the family to retrieve users from.
        current_user (UserModel, optional): The currently authenticated user, injected via dependency.
        db (AsyncSession, optional): The asynchronous database session, injected by dependency.
    Returns:
        RestGetAllUsersInFamilyResponse: The response object containing the family and user information.
    """
    return await ControllerGetAllUsersInFamily(family_id, current_user, db)

# Post /api/v1/families/{family_id}/users to add a user to a family
@router.post(path="/api/v1/families/{family_id}/users", response_model=RestAddUserToFamilyResponse, summary="Add a user to a family", description="This service adds a user to a family")
async def add_user_to_family(family_id: str, user_addition: AddUserToFamily, current_user: UserModel = Depends(get_current_user), db: AsyncSession = Depends(get_db)) -> RestAddUserToFamilyResponse:
    """
    Asynchronously adds a user to a specified family.
    Args:
        family_id (str): The ID of the family to add the user to.
        user_addition (AddUserToFamily): The user information to be added to the family.
        current_user (UserModel, optional): The currently authenticated user, injected via dependency.
        db (AsyncSession, optional): The asynchronous database session, injected by dependency.
    Returns:
        RestAddUserToFamilyResponse: The response object containing the status of the addition operation.
    """
    return await ControllerAddUserToFamily(family_id, user_addition, current_user, db)

# Delete /api/v1/families/{family_id}/users/{user_id} to remove a user from a family
@router.delete(path="/api/v1/families/{family_id}/users/{user_id}", response_model=BaseRestResponse, summary="Remove a user from a family", description="This service removes a user from a family")
async def remove_user_from_family(family_id: str, user_id: str, current_user: UserModel = Depends(get_current_user), db: AsyncSession = Depends(get_db)) -> BaseRestResponse:
    """
    Asynchronously removes a user from a specified family.
    Args:
        family_id (str): The ID of the family to remove the user from.
        user_id (str): The ID of the user to be removed.
        current_user (UserModel, optional): The currently authenticated user, injected via dependency.
        db (AsyncSession, optional): The asynchronous database session, injected by dependency.
    Returns:
        BaseRestResponse: The response object containing the status of the removal operation.
    """
    return await ControllerRemoveUserFromFamily(family_id, user_id, current_user, db)

# Get /api/v1/users/families to get all families a user belongs to
@router.get(path="/api/v1/users/{user_id}/families", response_model=RestGetFamiliesUserBelongsToResponse, summary="Get all families a user belongs to", description="This service gets all families a user belongs to")
async def get_families_user_belongs_to(user_id: str, current_user: UserModel = Depends(get_current_user), db: AsyncSession = Depends(get_db)) -> RestGetFamiliesUserBelongsToResponse:
    """
    Asynchronously retrieves all families a specified user belongs to.
    Args:
        user_id (str): The ID of the user to retrieve families for.
        current_user (UserModel, optional): The currently authenticated user, injected via dependency.
        db (AsyncSession, optional): The asynchronous database session, injected by dependency.
    Returns:
        RestGetAllUsersInFamilyResponse: The response object containing the family information.
    """
    return await ControllerGetFamiliesUserBelongsTo(user_id, current_user, db)