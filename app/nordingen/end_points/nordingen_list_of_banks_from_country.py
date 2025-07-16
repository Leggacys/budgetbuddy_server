from quart import jsonify, request
from app.main_routes import routes
from app.nordingen.methods.list_of_banks_from_country import get_banks_list_by_country
from app.utils.security.jwt_utils import require_jwt


@routes.route("/nordingen-list-of-banks-from-country",methods=["GET"])
@require_jwt
async def list_of_banks_from_country():
    country_code = request.args.get("country_code")
    
    if not country_code:
        return jsonify({"error": "Missing country_code"}), 400

    print(f"Fetching banks for country code: {country_code}")

    banks = await get_banks_list_by_country(country_code)
    
    
    if not banks:
        return jsonify({"error": "Failed to fetch banks"}), 500
    else:
        return jsonify(banks), 200 