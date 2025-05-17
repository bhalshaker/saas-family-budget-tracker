from models import UserModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from serializers import CreateCategory, UpdateCategory, RestCreateCategoryResponse, RestGetCategoryResponse, RestGetAllCategoriesOfamilyResponse, BaseRestResponse

async def get_all_categories_of_family(family_id:str,current_user:UserModel,db:AsyncSession)->RestGetAllCategoriesOfamilyResponse:
    pass

async def create_category_for_family(family_id:str,new_category:CreateCategory,current_user:UserModel,db:AsyncSession)-> RestCreateCategoryResponse:
    pass

async def retrieve_category(category_id:str,current_user:UserModel,db:AsyncSession)->RestGetCategoryResponse:
    pass

async def update_category(category_id:str,updated_category:UpdateCategory,current_user:UserModel,db:AsyncSession)->RestCreateCategoryResponse:
    pass

async def delete_category(category_id:str,current_user:UserModel,db:AsyncSession)->BaseRestResponse:
    pass