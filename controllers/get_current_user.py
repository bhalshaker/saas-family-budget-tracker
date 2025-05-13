
# dependencies/get_current_user.py
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from models.user import UserModel
from database import get_db
from jwt import DecodeError, ExpiredSignatureError # We import specific exceptions to handle them explicitly
from utilities import decode_token

# We're using the HTTP Bearer scheme for the Authorization header
http_bearer = HTTPBearer()

# This function takes the database session and the JWT token from the request header
def get_current_user(token: Annotated[HTTPAuthorizationCredentials, Depends(http_bearer)], db: Session = Depends(get_db)):
    sub_val = None
    try:
        sub_val = decode_token(token.credentials)
        user = db.query(UserModel).filter(UserModel.id == int(payload.get("sub"))).first()

        # If no user is found, raise an HTTP 401 Unauthorized error
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                 detail="Invalid username or password")
    # Handle decoding errors (invalid token)
    except DecodeError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                             detail=f'Could not decode token: {str(e)}')

    # Handle expired token errors
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                             detail='Token has expired')

    # Return the user if the token is valid
    return user

