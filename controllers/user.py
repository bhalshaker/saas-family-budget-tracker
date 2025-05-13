from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import UserModel
from serializers import UserCreationResponse,CreateUser,UserLogin


async def create_user(user: CreateUser,db: AsyncSession)->UserCreationResponse:
    print(user.model_dump(exclude='plain_password'))
    db_user = UserModel(**user.model_dump(exclude={'plain_password'}))
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    user_response=UserCreationResponse(**db_user.__dict__)
    return user_response

async def user_login(user:UserLogin):
    pass
