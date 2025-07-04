from sqlalchemy import select
from app.database.db import AsyncSessionLocal
from app.database.models.user_model import User


async def get_user_id(email:str):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.email == email))
        user = result.scalars().first()
        if user:
            return user.id
        return None
    