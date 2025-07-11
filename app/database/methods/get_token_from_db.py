from sqlalchemy import select
from app.database.db import AsyncSessionLocal
from app.database.models.tokens_model import Tokens

async def get_token_from_db():
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(Tokens))
        token = result.scalars().first()
        return token.access_token if token else None