from datetime import datetime,timezone
import uuid
from quart import jsonify, request
from sqlalchemy import select
from app.main_routes import routes
from app.database.db import AsyncSessionLocal
from app.database.models.user_model import User
from app.utils.email_encryption import email_encryption


@routes.route("/login", methods=["POST"])
async def login():
    data = await request.get_json()
    
    # Check if email is provided
    if not data or 'email' not in data:
        return jsonify({"error": "Email is required"}), 400
    
    email = data['email']
    
    # Check if email is empty
    if not email or email.strip() == "":
        return jsonify({"error": "Email cannot be empty"}), 400

    async with AsyncSessionLocal() as db:
        user = await User.find_by_email(db, email)

        if user:
            response = {
                "message": "User found",
                "user_id": user.id,
                "email": user.email
            }
        else:
            new_user = User(
                id = str(uuid.uuid4()),
                email=email,
                created_at=datetime.now(timezone.utc),
            )
            db.add(new_user)
            await db.commit()
            response = {
                "message": "User not found, new user created",
                "user_id": new_user.id,
                "email": new_user.email
            }

    return jsonify(response), 200