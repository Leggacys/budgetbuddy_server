import uuid
import httpx
from quart import jsonify, request
from app.main_routes import routes
from app.config import REDIRECT_URI
from app.nordingen.methods.get_nordingen_access_token import get_nordigen_access_token
from app.env_loader import load_redirect_uri


@routes.route("/create-requisition", methods=["POST"])
async def create_requisition():
    data = await request.get_json()
    institution_id = data.get("institution_id")
    user_email = data.get("email")
    REDIRECT_URI = load_redirect_uri()

    if not institution_id or not user_email:
        return jsonify({"error": "Missing institution_id or email"}), 400

    access_token = await get_nordigen_access_token()

    reference = str(uuid.uuid4())

    payload = {
        "redirect": REDIRECT_URI,
        "institution_id": institution_id,
        "reference": reference,
        "user_language": "EN"
    }

    async with httpx.AsyncClient() as client:
        res = await client.post(
            "https://bankaccountdata.gocardless.com/api/v2/requisitions/",
            headers={"Authorization": f"Bearer {access_token}"},
            json=payload
        )
    
    if res.status_code != 201:
        print(res.text)
        return jsonify({"error": "Failed to create requisition"}), res.status_code

    requisition_data = res.json()
    link = requisition_data.get("link")
    saved_requisition_id = requisition_data.get("id")

    return jsonify({
        "requisition_id": saved_requisition_id,
        "link": link
    }), 201
