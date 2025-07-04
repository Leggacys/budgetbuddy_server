import httpx
from app.database.methods.get_token_from_db import get_token_from_db



async def get_banks_list_by_country(country_code: str):
    access_token = await get_token_from_db()
    
    url = "https://bankaccountdata.gocardless.com/api/v2/institutions/"
    params = {"country": country_code}
    

    headers = {
        "Authorization": f"Bearer {access_token}",
        "accept": "application/json"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)

    if response.status_code == 200:
        institutions = response.json()
        print("✅ Institutions:", institutions)
        return institutions
    else:
        print(f"❌ Error fetching institutions: {response.status_code} - {response.text}")
        return None