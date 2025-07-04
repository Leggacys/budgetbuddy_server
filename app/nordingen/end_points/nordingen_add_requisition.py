from quart import jsonify, request
from app.database.db import AsyncSessionLocal
from app.database.models.bank_links_model import BankLink
from app.main_routes import routes
from app.database.methods.get_user_id import get_user_id


@routes.route("/nordingen_add_requisition", methods=["POST"])
async def nordingen_add_requisition():
    data = await request.get_json()
    requisition_id = data.get("requisition_id")
    user_email = data.get("email")
    bank_name = data.get("bank_name")
    bank_id = data.get("bank_id")
    user_id = await get_user_id(user_email)
    

    if not requisition_id or not user_email or not bank_name or not bank_id:
        return jsonify({"error": "Missing required fields"}), 400

    async with AsyncSessionLocal() as db:
        new_linked_bank = BankLink(
            user_id=user_id,
            requisition_id=requisition_id,
            institution_id=bank_id,
            bank_name=bank_name
        )
        db.add(new_linked_bank)
        await db.commit()

    return jsonify({"message": "Bank linked successfully"}), 200  