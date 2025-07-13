import asyncio
import json
from quart import jsonify, request
from app.main_routes import routes
from app.database.methods.get_requisition_db import get_requisition
from app.nordingen.methods.get_all_transactions import get_all_transactions
from app.utils.transactions.extract_essentials_transactions import extract_essentials_transactions


@routes.route("/nordingen-get-transactions", methods=["GET"])
async def get_transactions():
    email = request.args.get("email")
    if not email:
        return jsonify({"error": "Missing email"}), 400

    requisition_ids = await get_requisition(email)
    if not requisition_ids:
        return jsonify({"error": "No requisitions found"}), 404
    
    print(f"🔄 Fetching transactions for {len(requisition_ids)} requisitions in parallel...")
    
    # ✨ PARALLEL PROCESSING - This is the key optimization!
    async def fetch_transactions_for_requisition(requisition_id):
        try:
            print(f"📡 Starting fetch for requisition: {requisition_id}")
            transactions = await get_all_transactions(requisition_id)
            print(f"✅ Completed fetch for requisition: {requisition_id} - Got {len(transactions) if transactions else 0} transactions")
            return transactions or []
        except Exception as e:
            print(f"❌ Error fetching transactions for requisition {requisition_id}: {e}")
            return []
    
    # Execute all requests concurrently
    start_time = asyncio.get_event_loop().time()
    
    transaction_results = await asyncio.gather(
        *[fetch_transactions_for_requisition(req_id) for req_id in requisition_ids],
        return_exceptions=True
    )
    
    end_time = asyncio.get_event_loop().time()
    processing_time = round(end_time - start_time, 2)
    
    # Combine all results into raw JSON
    all_transactions_raw = []
    failed_requisitions = []
    
    for i, result in enumerate(transaction_results):
        if isinstance(result, Exception):
            failed_requisitions.append(requisition_ids[i])
            print(f"❌ Failed to process requisition {requisition_ids[i]}: {result}")
        elif result:
            all_transactions_raw.extend(result)
    
    # 🚀 Use your new extraction function to get clean, categorized data
    if all_transactions_raw:
        print(f"🏷️ Processing {len(all_transactions_raw)} transactions with Romanian categorization...")
        
        # Convert raw transactions to JSON string for your function
        raw_transactions_json = json.dumps(all_transactions_raw)
        
        # Extract essentials with Romanian categories
        essentials_json = await extract_essentials_transactions(raw_transactions_json)
        essentials_data = json.loads(essentials_json)
        
        # Sort by amount (highest first) or by date if you prefer
        essentials_data.sort(key=lambda x: abs(float(x.get('amount', 0)) if x.get('amount') else 0), reverse=True)
        
        print(f"✅ Processed and categorized {len(essentials_data)} transactions")
        
        # Generate category summary
        category_summary = {}
        total_spent = 0
        total_income = 0
        
        for transaction in essentials_data:
            category = transaction.get('category', 'Unknown')
            amount = float(transaction.get('amount', 0)) if transaction.get('amount') else 0
            
            # Update category summary
            if category not in category_summary:
                category_summary[category] = {
                    "count": 0,
                    "total_amount": 0,
                    "transactions": []
                }
            
            category_summary[category]["count"] += 1
            category_summary[category]["total_amount"] += abs(amount)
            category_summary[category]["transactions"].append({
                "company": transaction.get("company"),
                "amount": transaction.get("amount")
            })
            
            # Track income vs expenses
            if amount > 0:
                total_income += amount
            else:
                total_spent += abs(amount)
        
        response_data = {
            "total_count": len(essentials_data),
            "requisitions_processed": len(requisition_ids),
            "failed_requisitions": len(failed_requisitions),
            "processing_time_seconds": processing_time,
            
            # 🆕 Your new enhanced data
            "summary": {
                "total_income": round(total_income, 2),
                "total_spent": round(total_spent, 2),
                "net_amount": round(total_income - total_spent, 2),
                "categories_found": len(category_summary)
            },
            
            "categories": category_summary,
            
            "top_categories": sorted(
                [{"category": cat, "amount": data["total_amount"], "count": data["count"]} 
                 for cat, data in category_summary.items()],
                key=lambda x: x["amount"], 
                reverse=True
            )[:5]
        }
        
    else:
        # No transactions found
        response_data = {
            "transactions": [],
            "total_count": 0,
            "raw_count": 0,
            "requisitions_processed": len(requisition_ids),
            "failed_requisitions": len(failed_requisitions),
            "processing_time_seconds": processing_time,
            "summary": {
                "total_income": 0,
                "total_spent": 0,
                "net_amount": 0,
                "categories_found": 0
            },
            "categories": {},
            "top_categories": []
        }
    
    if failed_requisitions:
        response_data["warning"] = f"Failed to fetch transactions from {len(failed_requisitions)} bank(s)"
    
    if not essentials_data if all_transactions_raw else True:
        return jsonify({"message": "No transactions found", **response_data}), 404

    return jsonify(response_data), 200





