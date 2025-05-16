from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from controllers import get_current_user
from models import UserModel
from serializers import UpdateCategory,BaseRestResponse,RestGetAllCategoriesOfamilyResponse,RestGetCategoryResponse,RestCreateCategoryResponse

router = APIRouter()

@router.get("/api/v1/families/{family_id}/categories")
async def get_all_categories_of_family(family_id:str, db: AsyncSession = Depends(get_db))->RestGetAllCategoriesOfamilyResponse:
    pass

@router.post("/api/v1/families/{family_id}/categories")
async def create_new_category(family_id:str, current_user:UserModel=Depends(get_current_user),db: AsyncSession = Depends(get_db))->RestCreateCategoryResponse:
    pass

@router.get("/api/v1/categories/{category_id}")
async def get_category(category_id:str, current_user:UserModel=Depends(get_current_user), db: AsyncSession = Depends(get_db))->RestGetCategoryResponse:
    pass

@router.put("/api/v1/categories/{category_id}")
async def update_category(category_id:str, update_category:UpdateCategory,current_user:UserModel=Depends(get_current_user), db: AsyncSession = Depends(get_db))->RestCreateCategoryResponse:
    pass

@router.delete("/api/v1/categories/{category_id}")
async def delete_category(category_id:str, current_user:UserModel=Depends(get_current_user), db: AsyncSession = Depends(get_db))->BaseRestResponse:
    pass
