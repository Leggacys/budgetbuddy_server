import asyncio
from datetime import datetime, timezone
from app.database.methods.get_access_expiration_date import get_access_expiration_date
from app.nordingen.methods.refresh_token import refresh_token
from app.database.methods.get_token_from_db import get_token_from_db
from app.nordingen.methods.get_nordingen_access_token import get_nordigen_access_token 

    

async def check_token_validity():
    try:
        now = datetime.now(timezone.utc)
        expires_in = await get_access_expiration_date()
        print(f"Current time: {now}, Token expires at: {expires_in}")
        if not expires_in:
            return False
        if now >= expires_in:
            return False
        return True
    except Exception as e:
        print(f"❌ Error checking token validity: {e}")
        return False    
    
    
async def check_token_in_database():
        token_entry = await get_token_from_db()
        if token_entry:
            return True
        else:
            return False


async def token_refresh_job():
    try:
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
            refresh_result = await refresh_token()
            if refresh_result:
                print("✅ Token refreshed successfully")
            else:
                print("❌ Failed to refresh token, getting new token...")
                await get_nordigen_access_token()
                
    except Exception as e:
        print(f"❌ Error in token refresh job: {e}")
        try:
            print("🚀 Attempting to get new token...")
            await get_nordigen_access_token()
        except Exception as e2:
            print(f"❌ Failed to get new token: {e2}")