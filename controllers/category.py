from models import UserModel,CategoryModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from serializers import CreateCategory, UpdateCategory, RestCreateCategoryResponse, RestGetCategoryResponse, RestGetAllCategoriesOfamilyResponse, BaseRestResponse
from uuid import UUID
from .authorization import check_user_in_family,check_user_is_family_owner
from .family import get_family_by_id

async def get_all_categories_of_family(family_id:str,current_user:UserModel,db:AsyncSession)->RestGetAllCategoriesOfamilyResponse:
    """
    Retrieve all categories associated with a specific family.
    Args:
        family_id (str): The unique identifier of the family.
        current_user (UserModel): The currently authenticated user.
        db (AsyncSession): The asynchronous database session.
    Returns:
        RestGetAllCategoriesOfamilyResponse: A response object containing the status, message, and a list of categories if successful.
            If the family is not found, returns a response with code 0 and an appropriate message.
    """

    # Check if the user is a member of the family
    await check_user_in_family(family_id, current_user.id, db)
    # Get family
    family = await get_family_by_id(family_id, db)
    if not family:
        return BaseRestResponse(code=0, status="FAILED", message="Family not found")
    # Return all categories of the family from the family
    return RestGetAllCategoriesOfamilyResponse(code=1, status="SUCCESS", message="Family categories retrieved successfully", categories=[CategoryModel(**category) for category in family.categories])

async def create_category_for_family(family_id:str,new_category:CreateCategory,current_user:UserModel,db:AsyncSession)-> RestCreateCategoryResponse:
    """
    Asynchronously creates a new category for a specified family.
    Args:
        family_id (str): The unique identifier of the family for which the category is being created.
        new_category (CreateCategory): The data required to create the new category.
        current_user (UserModel): The user attempting to create the category.
        db (AsyncSession): The asynchronous database session.
    Returns:
        RestCreateCategoryResponse: On success, returns a response containing the created category and a success message.
        BaseRestResponse: On failure, returns a response with an error message and failure status.
    Raises:
        Exception: Rolls back the transaction and returns a failure response if an error occurs during category creation.
    Notes:
        - The function checks if the current user is the owner of the specified family before proceeding.
        - If the family does not exist, a failure response is returned.
    """

    # Check if the user is the owner of the family
    await check_user_is_family_owner(family_id, current_user.id, db)
    # Get family
    family = await get_family_by_id(family_id, db)
    if not family:
        return BaseRestResponse(code=0, status="FAILED", message="Family not found")
    # Create new category
    new_category = CategoryModel(**new_category.model_dump(), family_id=UUID(family.id), user_id=current_user.id)
    db.add(new_category)
    try:
        await db.commit()
        await db.refresh(new_category)
        return RestCreateCategoryResponse(code=1, status="SUCCESS", message="Category created successfully", category=CategoryModel(**new_category.model_dump()))
    except:
        await db.rollback()
        return BaseRestResponse(code=0, status="FAILED", message="Failed to create category")

async def retrieve_category(category_id:str,current_user:UserModel,db:AsyncSession)->RestGetCategoryResponse:
    """
    Retrieve a category by its ID for the current user.
    This function checks if the current user is a member of the family associated with the category,
    retrieves the category from the database, and returns a response object.
    Args:
        category_id (str): The unique identifier of the category to retrieve.
        current_user (UserModel): The user making the request.
        db (AsyncSession): The asynchronous database session.
    Returns:
        RestGetCategoryResponse: A response object containing the status, message, and category data if found.
    """

    # Check if the user is a member of the family
    await check_user_in_family(category_id, current_user.id, db)
    # Get category
    category = await get_category_by_id(category_id, db)
    if not category:
        return BaseRestResponse(code=0, status="FAILED", message="Category not found")
    return RestGetCategoryResponse(code=1, status="SUCCESS", message="Category retrieved successfully", category=CategoryModel(**category.model_dump()))

async def update_category(category_id:str,updated_category:UpdateCategory,current_user:UserModel,db:AsyncSession)->RestCreateCategoryResponse:
    """
    Asynchronously updates an existing category with new data.
    Args:
        category_id (str): The unique identifier of the category to update.
        updated_category (UpdateCategory): The data to update the category with.
        current_user (UserModel): The user performing the update operation.
        db (AsyncSession): The asynchronous database session.
    Returns:
        RestCreateCategoryResponse: A response object indicating the result of the update operation. 
            On success, returns the updated category. On failure, returns an error message.
    Raises:
        Exception: Rolls back the transaction and returns a failure response if an error occurs during the update.
    """

    # Check if the user is the owner of the family
    await check_user_is_family_owner(category_id, current_user.id, db)
    # Get category
    category = await get_category_by_id(category_id, db)
    if not category:
        return BaseRestResponse(code=0, status="FAILED", message="Category not found")
    # Update category
    for key, value in updated_category.model_dump().items():
        setattr(category, key, value)
    db.add(category)
    try:
        await db.commit()
        await db.refresh(category)
        return RestCreateCategoryResponse(code=1, status="SUCCESS", message="Category updated successfully", category=CategoryModel(**category.model_dump()))
    except:
        await db.rollback()
        return BaseRestResponse(code=0, status="FAILED", message="Failed to update category")

async def delete_category(category_id:str,current_user:UserModel,db:AsyncSession)->BaseRestResponse:
    """
    Deletes a category by its ID after verifying the current user is the owner of the associated family.
    Args:
        category_id (str): The unique identifier of the category to be deleted.
        current_user (UserModel): The user attempting to delete the category.
        db (AsyncSession): The asynchronous database session.
    Returns:
        BaseRestResponse: The response object indicating the result of the deletion operation.
            - code=1, status="SUCCESS" if the category was deleted successfully.
            - code=0, status="FAILED" if the category was not found or deletion failed.
    Raises:
        Exception: If there is an error during the deletion process.
    """

    # Check if the user is the owner of the family
    await check_user_is_family_owner(category_id, current_user.id, db)
    # Get category
    category = await get_category_by_id(category_id, db)
    if not category:
        return BaseRestResponse(code=0, status="FAILED", message="Category not found")
    # Delete category
    await db.delete(category)
    try:
        await db.commit()
        return BaseRestResponse(code=1, status="SUCCESS", message="Category deleted successfully")
    except:
        await db.rollback()
        return BaseRestResponse(code=0, status="FAILED", message="Failed to delete category")

async def get_category_by_id(category_id:str,db:AsyncSession)->CategoryModel:
    """
    Get category by ID.
    Args:
        category_id (str): The unique identifier of the category.
        db (AsyncSession): The asynchronous database session.
    Returns:
        CategoryModel: The category model if found, None otherwise.
    """
    category = await db.execute(select(CategoryModel).where(CategoryModel.id == UUID(category_id)))
    return category.scalars().first()