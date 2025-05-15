from models import FamilyModel,UserModel
from serializers import UserCreationResponse,FamilyInfo,RestGetAllUsersInFamilyResponse,AddUserToFamily
from sqlalchemy.ext.asyncio import AsyncSession

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
    family = await db.execute(FamilyModel.select().where(FamilyModel.id == family_id))
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

async def add_user_to_family(family_id:str,user_addition: AddUserToFamily,current_user: UserModel,db: AsyncSession):
    pass

async def remove_user_from_family(family_id:str,user_id: str,current_user: UserModel,db: AsyncSession):
    pass

async def get_family_user_belongs_to(user_id:str,current_user: UserModel,db: AsyncSession):
    pass