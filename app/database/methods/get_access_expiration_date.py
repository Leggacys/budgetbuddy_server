from sqlalchemy import select
from app.database.db import AsyncSessionLocal
from app.database.models.tokens_model import Tokens

async def get_access_expiration_date():
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(Tokens))
        token = result.scalars().first()
        return token.access_expires if token else None