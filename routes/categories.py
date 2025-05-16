from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from controllers import get_current_user,ControllerGetAllCategoriesOfFamily,ControllerCreateCategoryForFamily,ControllerRetrieveCategory,ControllerUpdateCategory,ControllerDeleteCategory
from models import UserModel
from serializers import UpdateCategory,BaseRestResponse,RestGetAllCategoriesOfamilyResponse,RestGetCategoryResponse,RestCreateCategoryResponse

router = APIRouter()

# Get (/api/v1/families/{family_id}/categories) all categories of a family
@router.get("/api/v1/families/{family_id}/categories",response_model=RestGetAllCategoriesOfamilyResponse,summary="Get all categories of a family",description="Get all categories of a family")
async def get_all_family_categories(family_id: str,current_user:UserModel=Depends(get_current_user),db:AsyncSession=Depends(get_db))->RestGetAllCategoriesOfamilyResponse:
    """
    Get all categories of a family
    """
    return await ControllerGetAllCategoriesOfFamily(family_id,current_user,db)

# Create (/api/v1/families/{family_id}/categories) a new category
@router.post("/api/v1/families/{family_id}/categories",response_model=RestCreateCategoryResponse,summary="Create a new category",description="Create a new category")
async def create_new_category(family_id: str,new_category:UpdateCategory,current_user:UserModel=Depends(get_current_user),db:AsyncSession=Depends(get_db))->RestCreateCategoryResponse:
    """
    Create a new category
    """
    return await ControllerCreateCategoryForFamily(family_id,new_category,current_user,db)

# Get (/api/v1/categories/{category_id}) get a category
@router.get("/api/v1/categories/{category_id}",response_model=RestGetCategoryResponse,summary="Get a category",description="Get a category")
async def get_category(category_id: str,current_user:UserModel=Depends(get_current_user),db:AsyncSession=Depends(get_db))->RestGetCategoryResponse:
    """
    Get a category
    """
    return await ControllerRetrieveCategory(category_id,current_user,db)

# Update (/api/v1/categories/{category_id}) update a category
@router.put("/api/v1/categories/{category_id}",response_model=RestCreateCategoryResponse,summary="Update a category",description="Update a category")
async def update_category(category_id: str,updated_category:UpdateCategory,current_user:UserModel=Depends(get_current_user),db:AsyncSession=Depends(get_db))->RestCreateCategoryResponse:
    """
    Update a category
    """
    return await ControllerUpdateCategory(category_id,updated_category,current_user,db)

# Delete (/api/v1/categories/{category_id}) delete a category
@router.delete("/api/v1/categories/{category_id}",response_model=BaseRestResponse,summary="Delete a category",description="Delete a category")
async def delete_category(category_id: str,current_user:UserModel=Depends(get_current_user),db:AsyncSession=Depends(get_db))->BaseRestResponse:
    """
    Delete a category
    """
    return await ControllerDeleteCategory(category_id,current_user,db)