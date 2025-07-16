from quart import jsonify, request
from app.main_routes import routes
from app.utils.security.jwt_utils import jwt_manager


@routes.route("/check-token-validity",methods=["POST"])
def check_token_validity():
    try:
        auth_header = request.headers.get("Authorization",'')
        if not auth_header.startswith("Bearer "):
            return jsonify({
                'valid': False,
                'error': 'No token provided'
            }),401
            
        access_token = auth_header.split(" ")[1]
        payload = jwt_manager.verify_token(access_token)
        if payload and payload.get("type") == "access_token":
            return jsonify({
                'valid': True,
                'payload': payload
            }), 200
        else:
            return jsonify({
                'valid': False,
                'error': 'Invalid or expired token'
            }), 401
    
    except Exception as e:
        return jsonify({
            'valid': False,
            'error': str(e)
        }), 500