import os
from dotenv import load_dotenv
import httpx

from app.database.methods.update_tokens_db import update_tokens_db

load_dotenv()

NORDIGEN_SECRET_ID = os.getenv("NORDIGEN_SECRET_ID")
NORDIGEN_SECRET_KEY = os.getenv("NORDIGEN_SECRET_KEY")

async def get_nordigen_access_token():
    url = "https://bankaccountdata.gocardless.com/api/v2/token/new/"
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json={
            "secret_id": NORDIGEN_SECRET_ID,
            "secret_key": NORDIGEN_SECRET_KEY
        })
    
    print(response.json())
    response.raise_for_status()
    await update_tokens_db(response.json().get("access")
                  , response.json().get("access_expires")
                  ,response.json().get("refresh")
                  , response.json().get("refresh_expires"))  
                  
    return response.json()