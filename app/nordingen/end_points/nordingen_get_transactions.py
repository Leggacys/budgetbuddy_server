import asyncio
from quart import jsonify, request
from app.main_routes import routes
from app.database.methods.get_requisition_db import get_requisition
from app.nordingen.methods.get_all_transactions import get_all_transactions


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
    
    # Combine all results
    all_transactions = []
    failed_requisitions = []
    
    for i, result in enumerate(transaction_results):
        if isinstance(result, Exception):
            failed_requisitions.append(requisition_ids[i])
            print(f"❌ Failed to process requisition {requisition_ids[i]}: {result}")
        elif result:
            all_transactions.extend(result)
    
    # Sort transactions by date (newest first)
    all_transactions.sort(key=lambda x: x.get('bookingDate', ''), reverse=True)
    
    print(f"⚡ Processed {len(requisition_ids)} requisitions in {processing_time}s")
    
    response_data = {
        "transactions": all_transactions,
        "total_count": len(all_transactions),
        "requisitions_processed": len(requisition_ids),
        "failed_requisitions": len(failed_requisitions),
        "processing_time_seconds": processing_time
    }
    
    if failed_requisitions:
        response_data["warning"] = f"Failed to fetch transactions from {len(failed_requisitions)} bank(s)"
    
    if not all_transactions:
        return jsonify({"message": "No transactions found", **response_data}), 404

    return jsonify(response_data), 200





