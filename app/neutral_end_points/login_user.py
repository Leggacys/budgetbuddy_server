from datetime import datetime,timezone
import uuid
from quart import jsonify, request
from app.main_routes import routes
from app.database.db import AsyncSessionLocal
from app.database.models.user_model import User
from app.utils.security.jwt_utils import jwt_manager

GOOGLE_TOKEN_INFO_URL = "https://oauth2.googleapis.com/tokeninfo"

@routes.route("/login", methods=["POST"])
async def login():
    data = await request.get_json()
    
    id_token = data.get("id_token")
    
    if not id_token:
        return jsonify({"error": "ID token is required"}), 400
    
    resp = request.get(GOOGLE_TOKEN_INFO_URL, params={"id_token": id_token})
    if resp.status_code != 200:
        return jsonify({"error": "Invalid ID token"}), 401
    
    token_info = resp.json()
    email = token_info.get("email")
    google_user_id = token_info.get("sub")
    
    if not email or not google_user_id:
        return jsonify({"error": "Invalid token payload"}), 401

    async with AsyncSessionLocal() as db:
        user = await User.find_by_email(db, email)

        if not user:
            new_user = User(
                id = str(uuid.uuid4()),
                email=email,
                created_at=datetime.now(timezone.utc),
            )
            db.add(new_user)
            await db.commit()
            user_id = new_user.id
            message = "New user created and logged in"
    
    access_token = jwt_manager.create_token(email, user_id)
    refresh_token = jwt_manager.create_refresh_token(email, user_id)
    
    return jsonify({
        "message": "Login successful",
        "user": {
            "user_id": str(user.id),
            "email": email
        },
        "tokens": {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer",
            "expires_in": 86400
        }
    }), 200