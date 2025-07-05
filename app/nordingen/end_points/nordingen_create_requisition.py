import uuid
import httpx
from quart import jsonify, request
from app.main_routes import routes
from app.config import REDIRECT_URI, NORDIGEN_API_URL, IS_SANDBOX, SANDBOX_INSTITUTION_ID
from app.nordingen.methods.get_nordingen_access_token import get_nordigen_access_token
from app.env_loader import load_redirect_uri

print("🔄 Loading nordigen_create_requisition.py - Route: /nordingen-create-requisition")

@routes.route("/nordingen-create-requisition", methods=["POST"])
async def create_requisition():
    data = await request.get_json()
    institution_id = data.get("institution_id")
    user_email = data.get("email")
    REDIRECT_URI = load_redirect_uri()

    if not institution_id or not user_email:
        return jsonify({"error": "Missing institution_id or email"}), 400

    # In sandbox mode, force use of sandbox institution
    if IS_SANDBOX:
        institution_id = SANDBOX_INSTITUTION_ID
        print(f"🏖️ Sandbox mode: Using institution {institution_id}")

    # Get access token - use the token from database instead of creating new one
    from app.database.methods.get_token_from_db import get_token_from_db
    access_token = await get_token_from_db()
    
    if not access_token:
        print("❌ No access token found, getting new one...")
        token_response = await get_nordigen_access_token()
        access_token = token_response.get("access")

    reference = str(uuid.uuid4())

    payload = {
        "redirect": REDIRECT_URI,
        "institution_id": institution_id,
        "reference": reference,
        "user_language": "EN"
    }

    async with httpx.AsyncClient() as client:
        res = await client.post(
            f"{NORDIGEN_API_URL}/requisitions/",
            headers={"Authorization": f"Bearer {access_token}"},
            json=payload
        )
    
    if res.status_code != 201:
        print("❌ Failed to create requisition:", res.text)
        return jsonify({"error": "Failed to create requisition"}), res.status_code

    requisition_data = res.json()
    link = requisition_data.get("link")
    saved_requisition_id = requisition_data.get("id")

    return jsonify({
        "requisition_id": saved_requisition_id,
        "link": link,
        "institution_id": institution_id,
        "sandbox_mode": IS_SANDBOX,
        "message": "Requisition created successfully. Use this requisition_id to save in your database after user completes authentication."
    }), 201
