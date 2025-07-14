from quart import jsonify, request
from app.main_routes import routes
from app.utils.security.jwt_utils import jwt_manager


@routes.route("/refresh-token",methods=["POST"])
async def refresh_token():
    try:
    
        data = await request.get_json()
        if not data or 'refresh_token' not in data:
            return {"error": "Missing refresh_token"}, 400
        
        refresh_token = data['refresh_token']
        new_token = jwt_manager.refresh_access_token(refresh_token)
        
        if not new_token:
            return jsonify({
                "message":"Invalid or expired refresh token"
            }) , 401
        
        if new_token:
            return {
                "message": "Token refreshed successfully",
                "tokens": {
                    "access_token": new_token,
                    "token_type": "Bearer",
                    "expires_in": 86000
                }
            }, 200
    except Exception as e:
        return jsonify({
            "error": "An error occurred while refreshing token",
        }), 500