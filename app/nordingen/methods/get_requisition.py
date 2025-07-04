import uuid
import httpx
from app.database.methods.get_token_from_db import get_token_from_db
from app.env_loader import load_nordingen_production_url, load_redirect_uri


async def get_requisition(institution_id: str):
    reference = f"user-{uuid.uuid4()}"
    url ="https://bankaccountdata.gocardless.com/api/v2/requisitions/"
    redirectUrl= load_redirect_uri()
    access_token = await get_token_from_db()
    headers = {
        "Authorization": f"Bearer {access_token}",
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    
    ##TODO change institution id on production
    data = {
        "redirect": redirectUrl,
        "institution_id": "SANDBOXFINANCE_SFIN0000",
        "reference": reference,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=data)
        if response.status_code != 201:
            print("Error creating requisition:", response.text)
            return None
        else:
            print("Requisition created successfully:", response.json())
            requisition = response.json()
            redirect_url = requisition.get("link")
            return redirect_url

    