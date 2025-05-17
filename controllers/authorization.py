from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import UserModel,FamilyModel,FamilyUserModel,FamilyUserRole
from uuid import UUID

# Check if the user is a member of the family
async def check_user_in_family(family_id: str, user_id: str, db: AsyncSession):
    """
    Check if the user is a member of the family.
    Args:
        family_id (str): The unique identifier of the family.
        user_id (str): The unique identifier of the user.
        db (AsyncSession): The asynchronous database session.
    Returns:
        bool: True if the user is a member of the family, False otherwise.
    Raises:
        HTTPException: 
            - 404 NOT FOUND if the family does not exist.
            - 403 FORBIDDEN if the user is not a member of the family.
    """
    # Check if the family exists
    family = await db.execute(FamilyModel.select().where(FamilyModel.id == UUID(family_id)))
    family = family.scalars().first()
    if not family:
        raise HTTPException(status_code=404, detail="Family not found")

    # Check if the user is a member of the family
    if not any(user.id == UUID(user_id) for user in family.users):
        raise HTTPException(status_code=403, detail="User is not a member of this family")

# Check if the user is the owner of the family
async def check_user_is_family_owner(family_id: str, user_id: str, db: AsyncSession):
    """
    Check if the user is the owner of the family.
    Args:
        family_id (str): The unique identifier of the family.
        user_id (str): The unique identifier of the user.
        db (AsyncSession): The asynchronous database session.
    Returns:
        bool: True if the user is the owner of the family, False otherwise.
    Raises:
        HTTPException: 
            - 404 NOT FOUND if the family does not exist.
            - 403 FORBIDDEN if the user is not the owner of the family.
    """
    # Check if the family exists
    family = await db.execute(FamilyModel.select().where(FamilyModel.id == UUID(family_id)))
    family = family.scalars().first()
    if not family:
        raise HTTPException(status_code=404, detail="Family not found")

    # Check if the user is the owner of the family based on the family_user table
    family_user = await db.execute(FamilyUserModel.select().where(
        FamilyUserModel.family_id == UUID(family_id),
        FamilyUserModel.user_id == UUID(user_id),
        FamilyUserModel.role == FamilyUserRole.OWNER
    ))
    family_user = family_user.scalars().first()
    if not family_user:
        raise HTTPException(status_code=403, detail="User is not the owner of this family")
    
# Check if user has one of the ROLEs mentioned in the array based on the family_user table
async def check_user_has_role(family_id: str, user_id: str, roles: list[FamilyUserRole], db: AsyncSession):
    """
    Check if the user has one of the specified roles in the family.
    Args:
        family_id (str): The unique identifier of the family.
        user_id (str): The unique identifier of the user.
        roles (list[FamilyUserRole]): List of roles to check against.
        db (AsyncSession): The asynchronous database session.
    Returns:
        bool: True if the user has one of the specified roles, False otherwise.
    Raises:
        HTTPException: 
            - 404 NOT FOUND if the family does not exist.
            - 403 FORBIDDEN if the user does not have any of the specified roles in the family.
    """
    # Check if the family exists
    family = await db.execute(FamilyModel.select().where(FamilyModel.id == UUID(family_id)))
    family = family.scalars().first()
    if not family:
        raise HTTPException(status_code=404, detail="Family not found")

    # Check if the user has one of the specified roles in the family based on the family_user table
    family_user = await db.execute(FamilyUserModel.select().where(
        FamilyUserModel.family_id == UUID(family_id),
        FamilyUserModel.user_id == UUID(user_id),
        FamilyUserModel.role.in_(roles)
    ))
    family_user = family_user.scalars().first()
    if not family_user:
        raise HTTPException(status_code=403, detail="User does not have any of the specified roles in this family")