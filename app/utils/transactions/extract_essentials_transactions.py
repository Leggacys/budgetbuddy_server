import json
from app.utils.transactions.get_category_romania import get_category_romanian

async def extract_essentials_transactions(data:str):
    full_data = json.loads(data)    
    transactions_list = []
    if isinstance(full_data,dict):
        if 'transactions' in full_data:
            trans = full_data['transactions']
            if isinstance(trans, dict):
                transactions_list.extend(trans.get('booked', []))
                transactions_list.extend(trans.get('pending', []))
            else:
                transactions_list=trans
        else:
            return "[]"
    else:
        transactions_list = full_data
        
    essentials = []
    
    for t in transactions_list:
        company = t.get("creditorName",'') or t.get("debtorName", '')
        description = t.get("remittanceInformationUnstructured", '') or t.get("remittanceInformationStructured", '')
        amount = t.get("transactionAmount", {}).get("amount", '') or t.get("transactionAmount", '')
        
        category = await get_category_romanian(company, description, amount) 
        
        essentials.append({
            "id": t.get("transactionId", ''),
            "amount": amount,
            "description": description,
            "company": company,
            "category": category
        })
        
    return json.dumps(essentials, indent=2)
    