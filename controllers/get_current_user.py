from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from models.user import UserModel
from database import get_db
from jwt import DecodeError, ExpiredSignatureError
from utilities import decode_token
from .user import get_user_by_id as ControllerGetUserById

http_bearer = HTTPBearer()

async def get_current_user(token: Annotated[HTTPAuthorizationCredentials, Depends(http_bearer)], db: AsyncSession = Depends(get_db))->UserModel:
    """
    Retrieves the current authenticated user based on the provided JWT token.
    Args:
        token (Annotated[HTTPAuthorizationCredentials, Depends(http_bearer)]): The HTTP bearer token credentials extracted from the request.
        db (AsyncSession, optional): SQLAlchemy database session dependency.
    Returns:
        UserModel: The user model instance corresponding to the authenticated user.
    Raises:
        HTTPException: 
            - 403 FORBIDDEN if the token cannot be decoded or has expired.
            - 401 UNAUTHORIZED if the user does not exist.
            - 403 FORBIDDEN if there is an error retrieving the user from the database.
    """

    sub_val = None
    try:
        sub_val = decode_token(token.credentials)
        if sub_val:
            try:
                user = await ControllerGetUserById(sub_val, db)
                if not user:
                    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                 detail="Invalid username or password")
                return user
            except Exception as e:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                 detail=f'Could not retrieve user: {str(e)}')
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                             detail='System Failed to Authenticate token')
    except DecodeError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                             detail=f'Could not decode token: {str(e)}')
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                             detail='Token has expired')

