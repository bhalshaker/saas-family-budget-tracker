from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import UserModel
from serializers import UserCreationResponse,CreateUser,UserLogin,RestUserLoginResponse,UserLoginResponse,RestUserCreationResponse
from utilities import verify_password,generate_token
from uuid import UUID


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
    except Exception as e:
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
            return RestUserLoginResponse(0,"Failed to login","Make sure you have entered the correct email and password",None)
        if not await verify_password(user.password, db_user.password):
            return RestUserLoginResponse(0,"Failed to login","Make sure you have entered the correct email and password",None)
    except Exception as e:
        return RestUserLoginResponse(0,"Failed to login","Could not generate login token",None)
    try:
        access_token=generate_token(db_user.id)
        return RestUserLoginResponse(code=1,status="Successfully logged in",message="You have logged in successfully",user_key=UserLoginResponse(**access_token))
    except Exception as e:
        return RestUserLoginResponse(0,"Failed to login","Could not generate login token",None)


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

async def update_user(user_id: str, user: CreateUser, db: AsyncSession) -> UserCreationResponse:
    """
    Asynchronously updates a user's information in the database.
    Args:
        user_id (str): The ID of the user to update.
        user (UpdateUser): The new user data to update.
        db (AsyncSession): The asynchronous database session.
    Returns:
        UserCreationResponse: The updated user object.
    """
    db_user = await get_user_by_id(user_id, db)
    if not db_user:
        raise Exception("User not found")
    for key, value in user.model_dump(exclude={'plain_password'}).items():
        setattr(db_user, key, value)
    await db.commit()
    await db.refresh(db_user)
    return UserCreationResponse(**db_user.__dict__)