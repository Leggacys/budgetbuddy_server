import asyncio
from datetime import datetime, timezone
from app.database.methods.get_access_expiration_date import get_access_expiration_date
from app.nordingen.methods.refresh_token import refresh_token
from app.database.methods.get_token_from_db import get_token_from_db
from app.nordingen.methods.get_nordingen_access_token import get_nordigen_access_token 

    

async def check_token_validity():
        now = datetime.now(timezone.utc)
        expires_in = await get_access_expiration_date()
        print(f"Current time: {now}, Token expires at: {expires_in}")
        if now >= expires_in:
            return False
        return True    
    
    
async def check_token_in_database():
        token_entry = await get_token_from_db()
        if token_entry:
            return True
        else:
            return False


async def token_refresh_job():
    result = await check_token_in_database()
    if result is False:
        print("🚀 Start getting token process...")
        result = await get_nordigen_access_token()
        return
    else:
        print("🔎 Token found in database, checking validity...")
    
    result = await check_token_validity()
    
    if result == True:
        print("✅ Token is still valid, no need to refresh.")
    else:
        print("⏰ Token is expired, refreshing...")
        await refresh_token()
        
    while True:
        now = datetime.now(timezone.utc)
        expires_in = await get_access_expiration_date()
        if not expires_in:
            print("❗ No expiration date found, refreshing token now...")
            await refresh_token()
            continue
        
        wait_seconds = (expires_in - now).total_seconds()
        if wait_seconds > 0:
            print(f"⏳ Waiting {wait_seconds} seconds until token refresh...")
            await asyncio.sleep(wait_seconds)
        else:
            print("🔄 Token expired, refreshing...")
            await refresh_token()
        
    
        
    
      
            
        
    
    
    
        