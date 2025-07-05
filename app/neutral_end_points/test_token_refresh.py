from quart import jsonify
from app.main_routes import routes
from app.jobs.token_validity import token_refresh_job, check_token_validity
from app.nordingen.methods.refresh_token import refresh_token
from app.database.methods.get_access_expiration_date import get_access_expiration_date
from app.database.methods.get_token_from_db import get_token_from_db
from datetime import datetime, timezone


@routes.route("/test_token_refresh", methods=["POST"])
async def test_token_refresh():
    """Test endpoint to manually trigger token refresh and check status"""
    try:
        # Check current token status
        access_token = await get_token_from_db()
        expires_at = await get_access_expiration_date()
        is_valid = await check_token_validity()
        
        status_info = {
            "has_access_token": bool(access_token),
            "expires_at": expires_at.isoformat() if expires_at else None,
            "is_valid": is_valid,
            "current_time": datetime.now(timezone.utc).isoformat()
        }
        
        # Try to refresh the token
        refresh_result = await refresh_token()
        
        # Check status after refresh
        new_access_token = await get_token_from_db()
        new_expires_at = await get_access_expiration_date()
        new_is_valid = await check_token_validity()
        
        return jsonify({
            "message": "Token refresh test completed",
            "refresh_successful": refresh_result,
            "before_refresh": status_info,
            "after_refresh": {
                "has_access_token": bool(new_access_token),
                "expires_at": new_expires_at.isoformat() if new_expires_at else None,
                "is_valid": new_is_valid,
                "current_time": datetime.now(timezone.utc).isoformat()
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            "error": f"Token refresh test failed: {str(e)}"
        }), 500


@routes.route("/token_status", methods=["GET"])
async def token_status():
    """Get current token status without refreshing"""
    try:
        access_token = await get_token_from_db()
        expires_at = await get_access_expiration_date()
        is_valid = await check_token_validity()
        
        return jsonify({
            "has_access_token": bool(access_token),
            "expires_at": expires_at.isoformat() if expires_at else None,
            "is_valid": is_valid,
            "current_time": datetime.now(timezone.utc).isoformat(),
            "token_preview": access_token[:20] + "..." if access_token else None
        }), 200
        
    except Exception as e:
        return jsonify({
            "error": f"Failed to get token status: {str(e)}"
        }), 500
