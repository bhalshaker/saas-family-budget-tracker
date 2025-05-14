from serializers import RestFamilyCreationResponse, CreateFamily,CreatedFamily,UserCreationResponse,RestGetAllFamiliesResponse
from models import UserModel,FamilyModel,FamilyUserModel,FamilyUserRole
from sqlalchemy.ext.asyncio import AsyncSession

async def create_family(new_family: CreateFamily,
                        current_user: UserModel,
                        db: AsyncSession)->RestFamilyCreationResponse:
    """
    Asynchronously creates a new family and associates the current user as the owner.
    Args:
        new_family (CreateFamily): The data required to create a new family.
        current_user (UserModel): The user initiating the family creation, who will be set as the owner.
        db (AsyncSession): The asynchronous database session for performing database operations.
    Returns:
        RestFamilyCreationResponse: The response object containing the status, message, and created family details if successful.
    """    
    db_family = FamilyModel(**new_family.model_dump())
    db.add(db_family)
    try:
        await db.commit()
        await db.refresh(db_family)
        family_user=FamilyUserModel(user_id=current_user.id,family_id=db_family.id,role=FamilyUserRole.OWNER)
        db.add(family_user)
        await db.commit()
        await db.refresh(family_user)
        created_family=CreatedFamily(**db_family.__dict__,owner=UserCreationResponse(**current_user.__dict__))
        return RestFamilyCreationResponse(code=1,status="SUCCESSFUL",message="Family created successfully",family=created_family)
    except:
        await db.rollback()
        return RestFamilyCreationResponse(code=0,status="FAILED",message="Failed to create a new family")
    
async def get_all_families(db: AsyncSession)->RestGetAllFamiliesResponse:
    """
    Asynchronously retrieves all families from the database.
    Args:
        db (AsyncSession): The asynchronous database session for performing database operations.
    Returns:
        RestFamilyCreationResponse: The response object containing the status, message, and list of all families if successful.
    """
    try:
        families = await db.execute(FamilyModel.select())
        families = families.scalars().all()
        families = [
            CreatedFamily(
            **family.__dict__,
            owner=UserCreationResponse(
                **next(
                (
                    family_user.__dict__
                    for family_user in family.users
                    if family_user.role == FamilyUserRole.OWNER
                ),
                {}
                )
            )
            )
            for family in families
        ]
        return RestGetAllFamiliesResponse(code=1,status="SUCCESSFUL",message="Families retrieved successfully",families=families)
    except Exception as e:
        return RestGetAllFamiliesResponse(code=0,status="FAILED",message=f"Failed to retrieve families: {str(e)}")

async def get_family(family_id: str,current_user:UserModel,db: AsyncSession)->RestFamilyCreationResponse:
    """
    Asynchronously retrieves a family by its ID.
    Args:
        family_id (str): The ID of the family to retrieve.
        current_user (UserModel): The user requesting the family information.
        db (AsyncSession): The asynchronous database session for performing database operations.
    Returns:
        RestFamilyCreationResponse: The response object containing the status, message, and family details if successful.
    """
    try:
        family = await db.execute(FamilyModel.select().where(FamilyModel.id == family_id))
        family = family.scalars().first()
        if not family:
            return RestFamilyCreationResponse(code=0,status="FAILED",message="Family not found")
        if not any(family_user.user_id == current_user.id for family_user in family.users):
            return RestFamilyCreationResponse(code=0,status="FAILED",message="User is not a member of this family")
        return RestFamilyCreationResponse(code=1,status="SUCCESSFUL",message="Family retrieved successfully",family=CreatedFamily(**family.__dict__))
    except Exception as e:
        return RestFamilyCreationResponse(code=0,status="FAILED",message=f"Failed to retrieve family: {str(e)}")

async def delete_family(family_id: str,current_user:UserModel,db: AsyncSession)->RestFamilyCreationResponse:
    """
    Asynchronously deletes a family by its ID.
    Args:
        family_id (str): The ID of the family to delete.
        current_user (UserModel): The user requesting the deletion.
        db (AsyncSession): The asynchronous database session for performing database operations.
    Returns:
        RestFamilyCreationResponse: The response object containing the status and message of the deletion operation.
    """
    try:
        family = await db.execute(FamilyModel.select().where(FamilyModel.id == family_id))
        family = family.scalars().first()
        if not family:
            return RestFamilyCreationResponse(code=0,status="FAILED",message="Family not found")
        if not any(family_user.user_id == current_user.id and family_user.role == FamilyUserRole.OWNER for family_user in family.users):
            return RestFamilyCreationResponse(code=0, status="FAILED", message="User is not the owner of this family")
        await db.delete(family)
        await db.commit()
        return RestFamilyCreationResponse(code=1,status="SUCCESSFUL",message="Family deleted successfully")
    except Exception as e:
        return RestFamilyCreationResponse(code=0,status="FAILED",message=f"Failed to delete family: {str(e)}")

async def update_family(family_id: str,
                        current_user:UserModel,
                        db: AsyncSession,
                        updated_family: CreateFamily)->RestFamilyCreationResponse:
    """
    Asynchronously updates a family by its ID.
    Args:
        family_id (str): The ID of the family to update.
        current_user (UserModel): The user requesting the update.
        db (AsyncSession): The asynchronous database session for performing database operations.
        updated_family (CreateFamily): The updated family data.
    Returns:
        RestFamilyCreationResponse: The response object containing the status, message, and updated family details if successful.
    """
    try:
        family = await db.execute(FamilyModel.select().where(FamilyModel.id == family_id))
        family = family.scalars().first()
        if not family:
            return RestFamilyCreationResponse(code=0,status="FAILED",message="Family not found")
        if not any(family_user.user_id == current_user.id and family_user.role == FamilyUserRole.OWNER for family_user in family.users):
            return RestFamilyCreationResponse(code=0,status="FAILED",message="User is not the owner of this family")
        for key, value in updated_family.model_dump().items():
            setattr(family, key, value)
        await db.commit()
        await db.refresh(family)
        return RestFamilyCreationResponse(code=1,status="SUCCESSFUL",message="Family updated successfully",family=CreatedFamily(**family.__dict__))
    except Exception as e:
        return RestFamilyCreationResponse(code=0,status="FAILED",message=f"Failed to update family: {str(e)}")