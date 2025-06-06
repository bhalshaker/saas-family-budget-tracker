from fastapi import APIRouter, Depends
from serializers import RestFamilyCreationResponse,RestGetAllFamiliesResponse,CreateFamily,BaseRestResponse
from controllers import ControllerCreateFamily,ControllerGetFamily,ControllerGetAllFamilies,ControllerDeleteFamily,ControllerUpdateFamily
from models import UserModel
from controllers import get_current_user
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db

router = APIRouter()


@router.get(path="/api/v1/families/",
            response_model=RestGetAllFamiliesResponse,summary="Get all families",
            description="""Get all families in the system.
            This endpoint allows you to retrieve a list of all families in the system. The families will be returned in the response.""")
async def get_all_families(db: AsyncSession = Depends(get_db))->RestGetAllFamiliesResponse:
    return await ControllerGetAllFamilies(db)

@router.post(path="/api/v1/families/",
             response_model=RestFamilyCreationResponse,summary="Create a new family",
            description="""Create a new family in the system.
            This endpoint allows you to create a new family with the provided details. The family will be created and returned in the response.""")
async def create_family(new_family: CreateFamily,current_user: UserModel = Depends(get_current_user),db: AsyncSession = Depends(get_db))->RestFamilyCreationResponse:
    """
    Creates a new family entry in the database.
    Args:
        new_family (CreateFamily): The data required to create a new family.
        current_user (UserModel, optional): The currently authenticated user, injected by dependency.
        db (AsyncSession, optional): The asynchronous database session, injected by dependency.
    Returns:
        RestFamilyCreationResponse: The response containing the result of the family creation operation.
    """
    
    return await ControllerCreateFamily(new_family=new_family,current_user=current_user,db=db)

@router.get(path="/api/v1/families/{family_id}",
            response_model=RestFamilyCreationResponse,summary="Get family by ID",
            description="""Get family by ID.
            This endpoint allows you to retrieve a family by its ID. The family details will be returned in the response.""")
async def get_family(family_id: str,current_user:UserModel=Depends(get_current_user),db: AsyncSession = Depends(get_db))->RestFamilyCreationResponse:
    """
    Retrieve information about a specific family.
    Args:
        family_id (str): The unique identifier of the family to retrieve.
        current_user (UserModel, optional): The currently authenticated user, injected by dependency.
        db (AsyncSession, optional): The asynchronous database session, injected by dependency.
    Returns:
        RestFamilyCreationResponse: The response object containing the family's details.
    """

    return await ControllerGetFamily(family_id=family_id,current_user=current_user,db=db)

@router.put(path="/api/v1/families/{family_id}",
            response_model=RestFamilyCreationResponse,summary="Update family by ID",
            description="""Update family by ID.
            This endpoint allows you to update a family by its ID. The updated family details will be returned in the response.""")
async def update_family_by_id(family_id: str,updated_family:CreateFamily,current_user:UserModel=Depends(get_current_user),db: AsyncSession = Depends(get_db))->RestFamilyCreationResponse:
    """
    Update a family record by its ID.
    Args:
        family_id (str): The unique identifier of the family to update.
        updated_family (CreateFamily): The data model containing the updated family information.
        current_user (UserModel, optional): The currently authenticated user, injected by dependency.
        db (AsyncSession, optional): The asynchronous database session, injected by dependency.
    Returns:
        RestFamilyCreationResponse: The response containing the updated family information.
    """

    return await ControllerUpdateFamily(family_id=family_id,updated_family=updated_family,current_user=current_user,db=db)

@router.delete(path="/api/v1/families/{family_id}",
            response_model=RestFamilyCreationResponse,summary="Delete family by ID",
            description="""Delete family by ID.
            This endpoint allows you to delete a family by its ID. The family will be removed from the system.""")
async def delete_family(family_id: str,current_user:UserModel=Depends(get_current_user),db: AsyncSession = Depends(get_db))->RestFamilyCreationResponse:
    """
    Deletes a family by its ID.
    Args:
        family_id (str): The unique identifier of the family to delete.
        current_user (UserModel, optional): The currently authenticated user, injected by dependency.
        db (AsyncSession, optional): The asynchronous database session, injected by dependency.
    Returns:
        RestFamilyCreationResponse: The response object indicating the result of the deletion operation.
    """

    return await ControllerDeleteFamily(family_id=family_id,current_user=current_user,db=db)