import asyncio
import httpx
from app.database.methods.get_token_from_db import get_token_from_db
from app.config import NORDIGEN_API_URL

async def get_all_transactions(requisition_id):
    """Optimized version with parallel account processing"""
    try:
        access_token = await get_token_from_db()
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Get requisition details
            requisition_response = await client.get(
                f"{NORDIGEN_API_URL}/requisitions/{requisition_id}/",
                headers={"Authorization": f"Bearer {access_token}"}
            )
            
            if requisition_response.status_code != 200:
                print(f"❌ Failed to get requisition {requisition_id}")
                return []
            
            requisition_data = requisition_response.json()
            account_ids = requisition_data.get("accounts", [])
            
            if not account_ids:
                print(f"ℹ️ No accounts found for requisition {requisition_id}")
                return []
            
            print(f"📊 Processing {len(account_ids)} accounts for requisition {requisition_id}")
            
            # ✨ PARALLEL ACCOUNT PROCESSING
            async def fetch_account_transactions(account_id):
                try:
                    response = await client.get(
                        f"{NORDIGEN_API_URL}/accounts/{account_id}/transactions/",
                        headers={"Authorization": f"Bearer {access_token}"}
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        transactions = []
                        transactions.extend(data.get("transactions", {}).get("booked", []))
                        transactions.extend(data.get("transactions", {}).get("pending", []))
                        return transactions
                    else:
                        print(f"❌ Failed to get transactions for account {account_id}")
                        return []
                except Exception as e:
                    print(f"❌ Error fetching account {account_id}: {e}")
                    return []
            
            # Process all accounts in parallel
            account_results = await asyncio.gather(
                *[fetch_account_transactions(account_id) for account_id in account_ids],
                return_exceptions=True
            )
            
            # Combine all transactions
            all_transactions = []
            for result in account_results:
                if not isinstance(result, Exception) and result:
                    all_transactions.extend(result)
            
            print(f"✅ Got {len(all_transactions)} total transactions for requisition {requisition_id}")
            return all_transactions
            
    except Exception as e:
        print(f"❌ Error in get_all_transactions for {requisition_id}: {e}")
        return []
