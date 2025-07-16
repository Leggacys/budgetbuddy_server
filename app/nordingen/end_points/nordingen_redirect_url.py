from quart import jsonify, request
from app.main_routes import routes
from app.nordingen.methods.get_requisition import get_requisition
from app.utils.security.jwt_utils import require_jwt

@routes.route("/nordigen-redirect-url", methods=["GET"])
@require_jwt
async def nordigen_redirect_url():
    email = request.args.get("email")
    bank_id = request.args.get("bank_id")
    redirect_url = await get_requisition(bank_id)
    if( not redirect_url):
        return jsonify({"error": "Failed to create requisition"}), 500
    return jsonify({"redirect_url": redirect_url}), 200
    