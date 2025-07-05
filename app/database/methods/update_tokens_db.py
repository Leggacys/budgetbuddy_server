from datetime import datetime, timedelta, timezone
from sqlalchemy import select
from app.database.db import AsyncSessionLocal
from app.database.models.tokens_model import Tokens


async def update_tokens_db(access_token:str , access_token_expires:str, refresh_token:str, refresh_token_expires:str):
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(Tokens))
        token_entry = result.scalars().first()
        if token_entry:
            token_entry.access_token = access_token
            token_entry.access_expires = datetime.now(timezone.utc) + timedelta(seconds=int(access_token_expires))
            token_entry.refresh_token = refresh_token
            token_entry.refresh_expires = datetime.now(timezone.utc) + timedelta(seconds=int(refresh_token_expires))
        else:
            new_entry = Tokens(
                access_token=access_token,
                refresh_token=refresh_token,
                access_expires=datetime.now(timezone.utc) + timedelta(seconds=int(access_token_expires)),
                refresh_expires=datetime.now(timezone.utc) + timedelta(seconds=int(refresh_token_expires))
            )
            db.add(new_entry)
        await db.commit()
    