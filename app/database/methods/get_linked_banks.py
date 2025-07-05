from sqlalchemy import select
from app.database.db import AsyncSessionLocal
from app.database.models.bank_links_model import BankLink


async def get_linked_banks_from_db():
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(BankLink))
        bank_links = result.scalars().all()
        return [bank_link.bank_id for bank_link in bank_links] if bank_links else []