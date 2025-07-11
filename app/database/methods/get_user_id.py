from sqlalchemy import select
from app.database.db import AsyncSessionLocal
from app.database.models.user_model import User


async def get_user_id(email:str):
    async with AsyncSessionLocal() as session:
        user = await User.find_by_email(session, email)
        if user:
            return user.id
        return None
    