from quart import jsonify, request
import httpx
from app.database.db import AsyncSessionLocal
from app.database.models.bank_links_model import BankLink
from app.main_routes import routes
from app.database.methods.get_user_id import get_user_id
from app.database.methods.get_token_from_db import get_token_from_db
from app.config import NORDIGEN_API_URL
from app.utils.security.jwt_utils import require_jwt


@routes.route("/nordigen-add-requisition", methods=["POST"])
@require_jwt
async def nordigen_add_requisition():
    data = await request.get_json()
    requisition_id = data.get("requisition_id")
    user_email = data.get("email")
    bank_name = data.get("bank_name")
    bank_id = data.get("bank_id")
    
    print(f"📨 Received request data:")
    print(f"   - requisition_id: {requisition_id}")
    print(f"   - user_email: {user_email}")
    print(f"   - bank_name: {bank_name}")
    print(f"   - bank_id: {bank_id}")
    
    user_id = await get_user_id(user_email)
    print(f"👤 Found user_id: {user_id}")
    

    if not requisition_id or not user_email or not bank_name or not bank_id:
        return jsonify({"error": "Missing required fields"}), 400

    # Verify the requisition exists and is valid before saving
    try:
        access_token = await get_token_from_db()
        print(f"🔍 Verifying requisition_id: {requisition_id}")
        print(f"🔑 Using access token: {access_token[:20]}..." if access_token else "❌ No access token found")
        
        async with httpx.AsyncClient() as client:
            verify_url = f"{NORDIGEN_API_URL}/requisitions/{requisition_id}/"
            print(f"📡 Making request to: {verify_url}")
            
            verify_response = await client.get(
                verify_url,
                headers={"Authorization": f"Bearer {access_token}"}
            )
            
            print(f"📊 Response status: {verify_response.status_code}")
            print(f"📄 Response body: {verify_response.text}")
            
            if verify_response.status_code != 200:
                return jsonify({
                    "error": "Invalid requisition_id or requisition not found",
                    "debug_info": {
                        "status_code": verify_response.status_code,
                        "response": verify_response.text,
                        "requisition_id": requisition_id,
                        "api_url": verify_url
                    }
                }), 400
            
            requisition_data = verify_response.json()
            actual_institution_id = requisition_data.get("institution_id")
            
            # Verify the institution_id matches
            if actual_institution_id != bank_id:
                return jsonify({"error": f"Institution ID mismatch. Expected {bank_id}, got {actual_institution_id}"}), 400
                
    except Exception as e:
        return jsonify({"error": f"Failed to verify requisition: {str(e)}"}), 500

    # Save to database with proper error handling
    try:
        async with AsyncSessionLocal() as db:
            # Check if requisition_id already exists
            from sqlalchemy import select
            existing_link = await db.execute(
                select(BankLink).where(BankLink.requisition_id == requisition_id)
            )
            if existing_link.scalar_one_or_none():
                return jsonify({
                    "error": "Requisition already linked",
                    "message": f"This requisition ({requisition_id}) has already been linked to an account.",
                    "requisition_id": requisition_id
                }), 409  # Conflict status code
            
            new_linked_bank = BankLink(
                user_id=user_id,
                requisition_id=requisition_id,
                institution_id=bank_id,
                bank_name=bank_name
            )
            db.add(new_linked_bank)
            await db.commit()
    except Exception as db_error:
        return jsonify({"error": f"Database error: {str(db_error)}"}), 500

    return jsonify({"message": "Bank linked successfully", "requisition_id": requisition_id}), 200  