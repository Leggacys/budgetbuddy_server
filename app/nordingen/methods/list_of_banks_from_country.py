import httpx
from app.database.methods.get_token_from_db import get_token_from_db
from app.config import NORDIGEN_API_URL, IS_SANDBOX, SANDBOX_INSTITUTION_ID



async def get_banks_list_by_country(country_code: str):
    access_token = await get_token_from_db()
    
    url = f"{NORDIGEN_API_URL}/institutions/"
    params = {"country": country_code}
    

    headers = {
        "Authorization": f"Bearer {access_token}",
        "accept": "application/json"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)

    if response.status_code == 200:
        institutions = response.json()
        
        # In sandbox mode, add/prioritize the sandbox institution
        if IS_SANDBOX:
            sandbox_institution = {
                "id": SANDBOX_INSTITUTION_ID,
                "name": "Sandbox Finance",
                "bic": "SFIN0000",
                "transaction_total_days": "90",
                "countries": ["GB"],
                "logo": "https://cdn.gocardless.com/bank_icons/sandbox_finance.png"
            }
            # Add sandbox institution at the beginning
            institutions.insert(0, sandbox_institution)
            print("🏖️ Added sandbox institution to list")
        
        return institutions
    else:
        print(f"❌ Error fetching institutions: {response.status_code} - {response.text}")
        return None