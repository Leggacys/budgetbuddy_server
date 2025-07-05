from quart import jsonify
from app.main_routes import routes
from app.config import (
    ENVIRONMENT, IS_SANDBOX, NORDIGEN_API_URL, 
    SANDBOX_INSTITUTION_ID, REDIRECT_URI
)


@routes.route("/environment", methods=["GET"])
async def get_environment():
    """Get current environment configuration"""
    return jsonify({
        "environment": ENVIRONMENT,
        "sandbox_mode": IS_SANDBOX,
        "api_url": NORDIGEN_API_URL,
        "sandbox_institution_id": SANDBOX_INSTITUTION_ID if IS_SANDBOX else None,
        "redirect_uri": REDIRECT_URI,
        "configuration": {
            "token_refresh_enabled": True,
            "auto_sandbox_institution": IS_SANDBOX,
            "api_endpoints": {
                "token": f"{NORDIGEN_API_URL}/token/new/",
                "refresh": f"{NORDIGEN_API_URL}/token/refresh/",
                "institutions": f"{NORDIGEN_API_URL}/institutions/",
                "requisitions": f"{NORDIGEN_API_URL}/requisitions/",
                "transactions": f"{NORDIGEN_API_URL}/accounts/{{account_id}}/transactions/"
            }
        }
    }), 200


@routes.route("/sandbox/test-institution", methods=["GET"])
async def get_sandbox_institution():
    """Get sandbox institution details for testing"""
    if not IS_SANDBOX:
        return jsonify({
            "error": "Not in sandbox mode"
        }), 400
    
    return jsonify({
        "institution": {
            "id": SANDBOX_INSTITUTION_ID,
            "name": "Sandbox Finance",
            "bic": "SFIN0000",
            "countries": ["GB"],
            "description": "Sandbox institution for testing Nordigen integration",
            "usage": "This institution is automatically used in sandbox mode for all requisitions"
        },
        "test_credentials": {
            "username": "user_good",
            "password": "pass_good",
            "note": "Use these credentials when prompted during bank authentication in sandbox mode"
        }
    }), 200
