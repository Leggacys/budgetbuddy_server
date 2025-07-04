from datetime import datetime,timezone
import uuid
from quart import jsonify, request
from sqlalchemy import select
from app.main_routes import routes
from app.database.db import AsyncSessionLocal
from app.database.models.user_model import User


@routes.route("/login", methods=["POST"])
async def login():
    data = await request.get_json()
    email = data['email']

    async with AsyncSessionLocal() as db:
        result = await db.execute(select(User).filter_by(email=email))
        user = result.scalars().first()

        if user:
            response = {
                "message": "User found",
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
                "email": new_user.email
            }

    return jsonify(response), 200