from serializers import RestFamilyCreationResponse, CreateFamily,RestGetAllFamiliesResponse
from serializers import BaseRestResponse,FamilyInfo
from models import UserModel,FamilyModel,FamilyUserModel,FamilyUserRole
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from uuid import UUID
from .authorization import check_user_is_family_owner,check_user_in_family

async def create_family(new_family: CreateFamily,current_user: UserModel,db: AsyncSession)->RestFamilyCreationResponse:
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
        # Flush to assign db_family.id before using it in FamilyUserModel
        await db.flush()
        family_user=FamilyUserModel(user_id=current_user.id, family_id=db_family.id, role=FamilyUserRole.OWNER)
        db.add(family_user)
        await db.commit()
        await db.refresh(db_family)
        await db.refresh(family_user)
        print(db_family.__dict__)
        print(family_user.__dict__)
        created_family=FamilyInfo(**db_family.__dict__)
        print(created_family.__dict__)
        return RestFamilyCreationResponse(code=1,status="SUCCESSFUL",message="Family created successfully",family=created_family)
    except Exception as e:
        print("Family creation error:", e)
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
        families = await db.execute(select(FamilyModel))
        families = families.scalars().all()
        families = [FamilyInfo(**family.__dict__)for family in families]
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
        await check_user_in_family(family_id, current_user.id, db)
        family = await db.execute(select(FamilyModel).where(FamilyModel.id == UUID(family_id)))
        family = family.scalars().first()
        if not family:
            return RestFamilyCreationResponse(code=0,status="FAILED",message="Family not found")
        return RestFamilyCreationResponse(code=1,status="SUCCESSFUL",message="Family retrieved successfully",family=FamilyInfo(**family.__dict__))
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
        await check_user_is_family_owner(family_id, current_user.id, db)
        family = await db.execute(select(FamilyModel).where(FamilyModel.id == UUID(family_id)))
        family = family.scalars().first()
        if not family:
            return RestFamilyCreationResponse(code=0,status="FAILED",message="Family not found")
        await db.flush()
        await db.delete(family)
        await db.commit()
        return RestFamilyCreationResponse(code=1,status="SUCCESSFUL",message="Family deleted successfully")
    except Exception as e:
        return RestFamilyCreationResponse(code=0,status="FAILED",message=f"Failed to delete family: {str(e)}")

async def update_family(family_id: str,updated_family: CreateFamily,current_user:UserModel,db: AsyncSession)->RestFamilyCreationResponse:
    """
    Asynchronously updates a family by its ID.
    Args:
        family_id (str): The ID of the family to update.
        updated_family (CreateFamily): The updated family data.
        current_user (UserModel): The user requesting the update.
        db (AsyncSession): The asynchronous database session for performing database operations.

    Returns:
        RestFamilyCreationResponse: The response object containing the status, message, and updated family details if successful.
    """
    try:
        family = await db.execute(select(FamilyModel).where(FamilyModel.id == UUID(family_id)))
        family = family.scalars().first()
        if not family:
            return RestFamilyCreationResponse(code=0,status="FAILED",message="Family not found")
        await check_user_is_family_owner(family_id, current_user.id, db)
        await db.flush()
        for key, value in updated_family.model_dump().items():
            setattr(family, key, value)
        await db.commit()
        await db.refresh(family)
        return RestFamilyCreationResponse(code=1,status="SUCCESSFUL",message="Family updated successfully",family=FamilyInfo(**family.__dict__))
    except Exception as e:
        return RestFamilyCreationResponse(code=0,status="FAILED",message=f"Failed to update family: {str(e)}")

# Get family by id
async def get_family_by_id(family_id: str, db: AsyncSession) -> FamilyModel:
    """
    Asynchronously retrieves a family by its ID.
    Args:
        family_id (str): The ID of the family to retrieve.
        db (AsyncSession): The asynchronous database session for performing database operations.
    Returns:
        FamilyModel: The family object if found, otherwise None.
    """

    family = await db.execute(select(FamilyModel).where(FamilyModel.id == UUID(family_id)))
    return family.scalars().first() if family else None

# Get family by id
async def get_family_by_id_with_account(family_id: str, db: AsyncSession) -> FamilyModel:
    """
    Asynchronously retrieves a family by its ID.
    Args:
        family_id (str): The ID of the family to retrieve.
        db (AsyncSession): The asynchronous database session for performing database operations.
    Returns:
        FamilyModel: The family object if found, otherwise None.
    """

    family = await db.execute(select(FamilyModel).options(selectinload(FamilyModel.account)).where(FamilyModel.id == UUID(family_id)))
    return family.scalars().first() if family else None

async def get_family_by_id_with_category(family_id: str, db: AsyncSession) -> FamilyModel:
    """
    Asynchronously retrieves a family by its ID.
    Args:
        family_id (str): The ID of the family to retrieve.
        db (AsyncSession): The asynchronous database session for performing database operations.
    Returns:
        FamilyModel: The family object if found, otherwise None.
    """

    family = await db.execute(select(FamilyModel).options(selectinload(FamilyModel.category)).where(FamilyModel.id == UUID(family_id)))
    return family.scalars().first() if family else None

async def get_family_by_id_with_transactions(family_id: str, db: AsyncSession) -> FamilyModel:
    """
    Asynchronously retrieves a family by its ID.
    Args:
        family_id (str): The ID of the family to retrieve.
        db (AsyncSession): The asynchronous database session for performing database operations.
    Returns:
        FamilyModel: The family object if found, otherwise None.
    """

    family = await db.execute(select(FamilyModel).options(selectinload(FamilyModel.transaction)).where(FamilyModel.id == UUID(family_id)))
    return family.scalars().first() if family else None