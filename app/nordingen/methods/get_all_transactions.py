import httpx
from app.database.methods.get_token_from_db import get_token_from_db

BASE_URL = "https://bankaccountdata.gocardless.com/api/v2"

async def get_all_transactions(requisition_id: str):
    access_token = await get_token_from_db()
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json"
    }

    async with httpx.AsyncClient() as client:
        
        requisition_url = f"{BASE_URL}/requisitions/{requisition_id}/"
        req_response = await client.get(requisition_url, headers=headers)
        req_response.raise_for_status()
        requisition_data = req_response.json()
        account_ids = requisition_data.get("accounts", [])

        if not account_ids:
            print("❌ No accounts linked to this requisition.")
            return []

        all_transactions = []
        
        for account_id in account_ids:
            transactions_url = f"{BASE_URL}/accounts/{account_id}/transactions/"
            tx_response = await client.get(transactions_url, headers=headers)
            tx_response.raise_for_status()
            tx_data = tx_response.json()

            booked = tx_data.get("transactions", {}).get("booked", [])
            pending = tx_data.get("transactions", {}).get("pending", [])

            all_transactions.extend(booked)
            all_transactions.extend(pending)

        print(f"✅ Total transactions fetched: {len(all_transactions)}")
        return all_transactions
