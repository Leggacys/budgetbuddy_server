
from sqlalchemy import select
from app.database.db import AsyncSessionLocal
from app.database.models.bank_links_model import BankLink
from app.database.models.user_model import User


async def get_requisition(email: str):
    async with AsyncSessionLocal() as session:
        user = await User.find_by_email(session, email)
        if not user:
            return []
        result = await session.execute(select(BankLink).where(BankLink.user_id == user.id))
        bank_links = result.scalars().all()
        return [link.requisition_id for link in bank_links]