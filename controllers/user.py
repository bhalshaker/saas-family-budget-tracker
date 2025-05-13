from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import UserModel
from serializers import UserCreationResponse,CreateUser,UserLogin,RestUserLoginResponse,UserLoginResponse
from utilities import verify_password,generate_token


async def create_user(user: CreateUser,db: AsyncSession)->UserCreationResponse:
    """
    Asynchronously creates a new user in the database.
    Args:
        user (CreateUser): The user data to create, typically including fields like name, email, and password.
        db (AsyncSession): The asynchronous database session used to perform database operations.
    Returns:
        UserCreationResponse: The response object containing the created user's information.
    Raises:
        Exception: If the database operation fails.
    Side Effects:
        - Adds a new user record to the database.
        - Commits the transaction and refreshes the user instance.
    """

    db_user = UserModel(**user.model_dump(exclude={'plain_password'}))
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    user_response=UserCreationResponse(**db_user.__dict__)
    return user_response

async def user_login(user:UserLogin,db:AsyncSession)->RestUserLoginResponse:
    """
    Asynchronously logs in a user by validating their credentials.
    Args:
        user (UserLogin): The user credentials to validate, typically including fields like email and password.
    Returns:
        bool: True if the login is successful, False otherwise.
    """
    
    db_user = await get_user_by_email(user.email)
    if not db_user:
        return RestUserLoginResponse(0,"Failed to login","Make sure you have entered the correct email and password",None)
    if not await verify_password(user.password, db_user.password):
        return False
    try:
        token=generate_token(db_user.id)
        return RestUserLoginResponse(1,"Successfully logged in","You have logged in successfully",UserLoginResponse(token))
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
    user= await db.execute(select(UserModel).where(UserModel.id == user_id)).scalars().first()
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
    user=await db.execute(select(UserModel).where(UserModel.email == email)).scalars().first()
    return user