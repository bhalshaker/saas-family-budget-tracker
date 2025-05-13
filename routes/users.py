from fastapi import APIRouter, HTTPException,Depends
from serializers import RestUserCreationResponse,CreateUser
from controllers import create_user as ControllerCreateUser
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db

router = APIRouter()

@router.post(path="/",response_model=RestUserCreationResponse,summary="Create a user",description="This services creates a user")
async def create_user(user:CreateUser,db:AsyncSession=Depends(get_db)):
    created_user=await ControllerCreateUser(user,db)
    return RestUserCreationResponse(code=1,status='SUCCESSFUL',message='User was created successfully',user=created_user)

@router.post("/login", response_model=UserToken)
def login(user: UserLogin, db: Session = Depends(get_db)):

    # Find the user by username
    db_user = db.query(UserModel).filter(UserModel.username == user.username).first()

    # Check if the user exists and if the password is correct
    if not db_user or not db_user.verify_password(user.password):
        raise HTTPException(status_code=400, detail="Invalid username or password")

    # Generate JWT token
    token = db_user.generate_token()

    # Return token and a success message
    return {"token": token, "message": "Login successful"}