from quart import jsonify, request
import httpx
from app.main_routes import routes
from app.database.methods.get_token_from_db import get_token_from_db
from app.config import NORDIGEN_API_URL


@routes.route("/debug/test-requisition", methods=["POST"])
async def test_requisition_debug():
    """Debug endpoint to test requisition verification"""
    data = await request.get_json()
    requisition_id = data.get("requisition_id")
    
    if not requisition_id:
        return jsonify({"error": "Missing requisition_id"}), 400
    
    try:
        # Get access token
        access_token = await get_token_from_db()
        
        debug_info = {
            "requisition_id": requisition_id,
            "has_access_token": bool(access_token),
            "access_token_preview": access_token[:20] + "..." if access_token else None,
            "api_url": NORDIGEN_API_URL
        }
        
        if not access_token:
            return jsonify({
                "error": "No access token found",
                "debug_info": debug_info
            }), 500
        
        # Test the API call
        async with httpx.AsyncClient() as client:
            verify_url = f"{NORDIGEN_API_URL}/requisitions/{requisition_id}/"
            
            verify_response = await client.get(
                verify_url,
                headers={"Authorization": f"Bearer {access_token}"}
            )
            
            debug_info.update({
                "request_url": verify_url,
                "response_status": verify_response.status_code,
                "response_headers": dict(verify_response.headers),
                "response_body": verify_response.text
            })
            
            try:
                response_json = verify_response.json()
                debug_info["response_json"] = response_json
            except:
                debug_info["response_json"] = "Failed to parse JSON"
            
            return jsonify({
                "message": "Debug test completed",
                "success": verify_response.status_code == 200,
                "debug_info": debug_info
            }), 200
            
    except Exception as e:
        return jsonify({
            "error": f"Exception occurred: {str(e)}",
            "debug_info": debug_info if 'debug_info' in locals() else {}
        }), 500


@routes.route("/debug/token-info", methods=["GET"])
async def token_info_debug():
    """Debug endpoint to check token status"""
    try:
        access_token = await get_token_from_db()
        
        return jsonify({
            "has_token": bool(access_token),
            "token_preview": access_token[:20] + "..." if access_token else None,
            "api_url": NORDIGEN_API_URL
        }), 200
        
    except Exception as e:
        return jsonify({
            "error": f"Failed to get token info: {str(e)}"
        }), 500
