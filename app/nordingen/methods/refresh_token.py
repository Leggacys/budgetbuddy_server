import httpx
from app.database.methods.update_tokens_db import update_tokens_db
from app.database.methods.get_refresh_token import get_refresh_token_from_db
from app.config import NORDIGEN_API_URL

async def refresh_token():
    refresh_token = await get_refresh_token_from_db()
    
    if not refresh_token:
        print("❌ No refresh token found in database")
        return False
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{NORDIGEN_API_URL}/token/refresh/",
            json={"refresh": refresh_token}
        )

    if response.status_code == 200:
        tokens = response.json()
        print("✅ Tokens refreshed successfully:", tokens)
        await update_tokens_db(
            tokens["access"],
            tokens["access_expires"],
            tokens["refresh"],
            tokens["refresh_expires"]
        )
        return True
        
    else:
        print("❌ Failed to refresh token:", response.text)
        return False