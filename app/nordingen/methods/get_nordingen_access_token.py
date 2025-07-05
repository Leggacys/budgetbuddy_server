import os
from dotenv import load_dotenv
import httpx

from app.database.methods.update_tokens_db import update_tokens_db
from app.config import NORDIGEN_API_URL, NORDIGEN_SECRET_ID, NORDIGEN_SECRET_KEY

load_dotenv()

async def get_nordigen_access_token():
    url = f"{NORDIGEN_API_URL}/token/new/"
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json={
            "secret_id": NORDIGEN_SECRET_ID,
            "secret_key": NORDIGEN_SECRET_KEY
        })
    
    print("🔑 Token response:", response.json())
    response.raise_for_status()
    await update_tokens_db(response.json().get("access")
                  , response.json().get("access_expires")
                  ,response.json().get("refresh")
                  , response.json().get("refresh_expires"))  
                  
    return response.json()