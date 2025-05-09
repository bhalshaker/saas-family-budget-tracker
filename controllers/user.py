from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import UserModel
from serializers import UserCreationResponse


async def create_user(user: dict,db: AsyncSession)->UserCreationResponse:
    db_user = UserModel(**user)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    user_response=UserCreationResponse.model_dump(db_user)
    return user_response

