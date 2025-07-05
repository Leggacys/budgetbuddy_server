
from quart import jsonify,request
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
    
    print(f"Fetching transactions for requisitions: {requisition_ids}") 
     
    all_transactions = []

    for requisition_id in requisition_ids:
        try:
            transactions = await get_all_transactions(requisition_id)
            if transactions:
                all_transactions.extend(transactions)
        except Exception as e:
            print(f"❌ Error fetching transactions for requisition {requisition_id}: {e}")

    if not all_transactions:
        return jsonify({"message": "No transactions found"}), 404

    return jsonify({"transactions": all_transactions}), 200
            
    
    
    
                    
       