from quart import Blueprint




routes = Blueprint('routes', __name__)


import app.nordingen.end_points.create_requisition
import app.nordingen.end_points.list_of_banks_from_country
import app.nordingen.end_points.nordingen_redirect_url
import app.nordingen.end_points.nordingen_add_requisition
import app.neutral_end_points.login_user
import app.nordingen.end_points.get_transactions