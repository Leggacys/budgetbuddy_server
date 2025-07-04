import requests
from app.database.methods import update_tokens_db
from app.database.methods.get_refresh_token import get_refresh_token_from_db

async def refresh_token():
    refresh_token = await get_refresh_token_from_db()
    
    response = requests.post(
    "https://ob.nordigen.com/api/v2/token/refresh/",
    json={"refresh": refresh_token}
)

    if response.status_code == 200:
        tokens = response.json()
        print("Tokens refreshed successfully:", tokens)
        update_tokens_db(
            tokens["access"],
            tokens["access_expires"],
            tokens["refresh"],
            tokens["refresh_expires"]
        )
        return True
        
    else:
        print("Failed to refresh token:", response.text)
        return False