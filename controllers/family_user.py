from models import FamilyModel,UserModel,FamilyUserModel,FamilyUserRole
from serializers import UserCreationResponse,FamilyInfo,RestGetAllUsersInFamilyResponse,AddUserToFamily,RestAddUserToFamilyResponse,BaseRestResponse,RestGetFamiliesUserBelongsToResponse
from sqlalchemy.ext.asyncio import AsyncSession
from .authorization import check_user_is_family_owner
from uuid import UUID

async def get_all_users_in_family(family_id: str,current_user: UserModel, db: AsyncSession) -> RestGetAllUsersInFamilyResponse:
    """
    Retrieve all users belonging to a specified family if the current user is a member.
    Args:
        family_id (str): The unique identifier of the family.
        current_user (UserModel): The user making the request.
        db (AsyncSession): The asynchronous database session.
    Returns:
        RestGetAllUsersInFamilyResponse: 
            - If the family does not exist, returns a response with code 0 and status "FAILED".
            - If the current user is not a member of the family, returns a response with code 0 and status "UNAUTHORIZED".
            - If successful, returns a response with code 1, status "SUCCESS", family information, and a list of users in the family.
    """

    #Check if user id really belongs to a family
    family = await db.execute(FamilyModel.select().where(FamilyModel.id == UUID(family_id)))
    family = family.scalars().first()
    if not family:
        return RestGetAllUsersInFamilyResponse(code=0,status="FAILED", message="Family not found")
    #Check if usser in the familiy
    if not any (user.id == current_user.id for user in family.users):
        return RestGetAllUsersInFamilyResponse(code=0, status="UNAUTHORIZED",message="You are not a memeber of this family")
    else:
        return RestGetAllUsersInFamilyResponse(code=1, status="SUCCESS", message="User is in the family",
                                               family=FamilyInfo(**family.model_dmup()),
                                               users=[UserCreationResponse(**user.__dict__) for user in family.users])

async def add_user_to_family(family_id:str,user_addition: AddUserToFamily,current_user: UserModel,db: AsyncSession)->RestAddUserToFamilyResponse:
    """
    Asynchronously adds a user to a family if the current user is the family owner.
    Args:
        family_id (str): The unique identifier of the family.
        user_addition (AddUserToFamily): The data required to add a user to the family, including user ID and role.
        current_user (UserModel): The currently authenticated user attempting to add another user.
        db (AsyncSession): The asynchronous database session.
    Returns:
        RestAddUserToFamilyResponse: A response object indicating the result of the operation, including success or failure status, and relevant data if successful.
    Raises:
        None explicitly, but may return a failed response if:
            - The current user is not the family owner.
            - The family does not exist.
            - The user is already in the family.
            - The user to be added does not exist.
            - There is a database error during the addition process.
    """

    #Check if the current user is the owner of the family
    await check_user_is_family_owner(family_id, current_user.id, db)
    #Check if the user to be added is already in the family
    family = await db.execute(FamilyModel.select().where(FamilyModel.id == UUID(family_id)))
    family = family.scalars().first()
    if not family:
        return BaseRestResponse(code=0, status="FAILED", message="Family not found")
    if any(user.id == user_addition.user_id for user in family.users):
        return BaseRestResponse(code=0, status="FAILED", message="User already in the family")
    #Check if the user to be added exists
    user = await db.execute(UserModel.select().where(UserModel.id == UUID(user_addition.user_id)))
    user = user.scalars().first()
    if not user:
        return BaseRestResponse(code=0, status="FAILED", message="User not found")
    #Add the user to the family
    family_user = FamilyUserModel(family_id=family_id, user_id=user_addition.user_id, role=user_addition.role)
    db.add(family_user)
    try:
        await db.commit()
        await db.refresh(family_user)
        return RestAddUserToFamilyResponse(code=1, status="SUCCESS", message="User added to family",
                                       family=FamilyInfo(**family.model_dump()),
                                       user=UserCreationResponse(**user.__dict__))
    except:
        return BaseRestResponse(code=0, status="FAILED", message="Failed to add user to family")

async def remove_user_from_family(family_id:str,user_id: str,current_user: UserModel,db: AsyncSession)->BaseRestResponse:
    """
    Removes a user from a family, if the current user is the owner.
    Args:
        family_id (str): The ID of the family from which the user will be removed.
        user_id (str): The ID of the user to remove from the family.
        current_user (UserModel): The user performing the removal operation.
        db (AsyncSession): The asynchronous database session.
    Returns:
        BaseRestResponse: The result of the operation, indicating success or failure.
    Raises:
        Exception: If the current user is not the owner of the family.
    Notes:
        - The owner of the family cannot be removed.
        - If the user is not found in the family, a failure response is returned.
        - Commits the transaction if the removal is successful.
    """

    #check if the current user is the owner of the family
    await check_user_is_family_owner(family_id, current_user.id, db)
    #Remove the user from the family_user table if the user already exists and is not the owner
    family_user = await db.execute(FamilyUserModel.select().where(FamilyUserModel.family_id == family_id, FamilyUserModel.user_id == UUID(user_id)))
    family_user = family_user.scalars().first()
    if not family_user:
        return BaseRestResponse(code=0, status="FAILED", message="User not found in family")
    if family_user.role == FamilyUserRole.OWNER:
        return BaseRestResponse(code=0, status="FAILED", message="Cannot remove the owner of the family")
    db.delete(family_user)
    try:
        await db.commit()
        return BaseRestResponse(code=1, status="SUCCESS", message="User removed from family")
    except:
        return BaseRestResponse(code=0, status="FAILED", message="Failed to remove user from family")

async def get_families_user_belongs_to(user_id:str,current_user: UserModel,db: AsyncSession)->RestGetFamiliesUserBelongsToResponse:
    """
    Retrieve the list of families that a user belongs to.
    Args:
        user_id (str): The ID of the user whose families are to be retrieved.
        current_user (UserModel): The currently authenticated user.
        db (AsyncSession): The asynchronous database session.
    Returns:
        RestGetFamiliesUserBelongsToResponse: A response object containing the status, message, and a list of families the user belongs to.
    Raises:
        None
    Notes:
        - Only allows access if the requested user_id matches the current authenticated user's ID.
        - Returns a failure response if the user is not authorized to view the families.
    """

    #check if the current user id is the same as the user id
    if current_user.id != UUID(user_id):
        return RestGetFamiliesUserBelongsToResponse(code=0, status="FAILED", message="You are not authorized to view this user's families")
    #Generate rest respone of all families the user belongs to based on current_user.families
    return RestGetFamiliesUserBelongsToResponse(code=1, status="SUCCESS", message="User belongs to the following families",
                                                families=[FamilyInfo(**family.model_dump()) for family in current_user.families]) 
