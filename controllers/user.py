from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import UserModel
from serializers import UserCreationResponse,CreateUser,UserLogin,RestUserLoginResponse,UserLoginResponse,RestUserCreationResponse,BaseRestResponse,RestGetllAllUsers
from utilities import verify_password,generate_token
from uuid import UUID

async def get_all_users(db: AsyncSession) -> RestGetllAllUsers:
    """
    Asynchronously retrieves all users from the database.
    Args:
        db (AsyncSession): The asynchronous database session used to perform database operations.
    Returns:
        RestGetllAllUsers: A list of UserModel instances representing all users in the database.
    """
    try:
        result = await db.execute(select(UserModel))
        users_results = result.scalars().all()
        users = [UserCreationResponse(**user.__dict__) for user in users_results]
        return RestGetllAllUsers(code=1,status="SUCCESSFUL",message="Users retrieved successfully",users=users)
    except:
        return RestGetllAllUsers(code=0,status="FAILED",message="Failed to retrieve users")

async def get_user(user_id: str, db: AsyncSession) -> RestUserCreationResponse:
    """
    Asynchronously retrieves a user by their ID from the database.
    Args:
        user_id (str): The ID of the user to retrieve.
        db (AsyncSession): The asynchronous database session used to perform database operations.
    Returns:
        RestUserCreationResponse: The response object containing the user's information.
    """
    try:
        db_user = await get_user_by_id(user_id, db)
        if not db_user:
            return RestUserCreationResponse(code=0,status="FAILED",message="User not found")
        user_response = UserCreationResponse(**db_user.__dict__)
        return RestUserCreationResponse(code=1,status="SUCCESSFUL",message="User retrieved successfully",user=user_response)
    except:
        return RestUserCreationResponse(code=0,status="FAILED",message="Failed to retrieve user")
    
async def create_user(user: CreateUser,db: AsyncSession)->RestUserCreationResponse:
    """
    Asynchronously creates a new user in the database.
    Args:
        user (CreateUser): The user data to create, typically including fields like name, email, and password.
        db (AsyncSession): The asynchronous database session used to perform database operations.
    Returns:
        RestUserCreationResponse: The response object containing the created user's information.
    Raises:
        Exception: If the database operation fails.
    Side Effects:
        - Adds a new user record to the database.
        - Commits the transaction and refreshes the user instance.
    """

    db_user = UserModel(**user.model_dump(exclude={'plain_password'}))
    db.add(db_user)
    try:
        await db.commit()
        await db.refresh(db_user)
        user_response=UserCreationResponse(**db_user.__dict__)
        return RestUserCreationResponse(code=1,status="SUCCESSFUL",message="User created successfully",user=user_response)
    except:
        await db.rollback()
        return RestUserCreationResponse(code=0,status="FAILED",message="Failed to create a new user")

async def user_login(user:UserLogin,db:AsyncSession)->RestUserLoginResponse:
    """
    Asynchronously logs in a user by validating their credentials.
    Args:
        user (UserLogin): The user credentials to validate, typically including fields like email and password.
    Returns:
        bool: True if the login is successful, False otherwise.
    """
    try:
        db_user = await get_user_by_email(user.email,db)
        if not db_user:
            return RestUserLoginResponse(code=0,status="Failed to login",message="Make sure you have entered the correct email and password")
        if not await verify_password(user.password, db_user.password):
            return RestUserLoginResponse(0,"Failed to login","Make sure you have entered the correct email and password")
    except:
        return RestUserLoginResponse(code=0,status="Failed to login",message="Make sure you have entered the correct email and password")
    try:
        access_token=generate_token(db_user.id)
        return RestUserLoginResponse(code=1,status="Successfully logged in",message="You have logged in successfully",user_key=UserLoginResponse(**access_token))
    except Exception as e:
        return RestUserLoginResponse(code=0,status="Failed to login",message="Could not generate login token")


async def get_user_by_id(user_id: str, db: AsyncSession) -> UserModel:
    """
    Fetch a user by their ID from the database.
    Args:
        user_id (str): The ID of the user to fetch.
        db (AsyncSession): The database session to use for the query.
    Returns:
        UserModel: The user object if found, None otherwise.
    """
    result= await db.execute(select(UserModel).where(UserModel.id == UUID(user_id)))
    user = result.scalars().first()
    return user

async def get_user_by_email(email: str, db: AsyncSession) -> UserModel:
    """
    Asynchronously retrieves a user from the database by their email address.
    Args:
        email (str): The email address of the user to retrieve.
        db (AsyncSession): The asynchronous database session.
    Returns:
        user: The user object if found, otherwise None.
    """
    result = await db.execute(select(UserModel).where(UserModel.email == email))
    user = result.scalars().first()
    return user

async def update_user(user_id: str, updated_user: CreateUser,current_user: UserModel, db: AsyncSession) -> RestUserCreationResponse:
    """
    Asynchronously updates a user's information in the database.
    Args:
        user_id (str): The ID of the user to update.
        user (UpdateUser): The new user data to update.
        db (AsyncSession): The asynchronous database session.
    Returns:
        UserCreationResponse: The updated user object.
    """
    try:
        db_user = await get_user_by_id(user_id, db)
    except:
        return RestUserCreationResponse(code=0,status="FAILED",message="Failed to get mentioned user")
    if not db_user:
        return RestUserCreationResponse(code=0,status="FAILED",message="User not found")
    if db_user.id != current_user.id:
        return RestUserCreationResponse(code=0,status="FAILED",message="Operation forbidden")
    for key, value in updated_user.model_dump(exclude_unset=True,exclude={'plain_password'}).items():
        setattr(db_user, key, value)
    try:
        await db.commit()
        await db.refresh(db_user)
        user_response = UserCreationResponse(**db_user.__dict__)
        return RestUserCreationResponse(code=1,status="SUCCESSFUL",message="User updated successfully",user=user_response)
    except:
        await db.rollback()
        return RestUserCreationResponse(code=0,status="FAILED",message="Failed to update user")

async def delete_user(user_id: str,current_user:UserModel, db: AsyncSession) -> BaseRestResponse:
    """
    Asynchronously deletes a user from the database.
    Args:
        user_id (str): The ID of the user to delete.
        db (AsyncSession): The asynchronous database session.
    Returns:
        UserCreationResponse: The deleted user object.
    """
    try:
        db_user = await get_user_by_id(user_id, db)
    except:
        return BaseRestResponse(code=0,status="FAILED",message="Failed to get mentioned user")
    if not db_user:
        return BaseRestResponse(code=0,status="FAILED",message="User not found")
    if db_user.id != current_user.id:
        return BaseRestResponse(code=0,status="FAILED",message="Operation forbidden")
    try:
        await db.delete(db_user)
        await db.commit()
        return BaseRestResponse(code=1,status="SUCCESSFUL",message="User deleted successfully")
    except Exception as e:
        await db.rollback()
        return BaseRestResponse(code=0,status="FAILED",message="Failed to delete user")