from flask import Blueprint

appliances_bp = Blueprint("appliances", __name__, url_prefix="/api/appliances")


@appliances_bp.route("/", methods=["GET"])
def get_appliances():
    # TODO: return appliance states via SmartThingsConnector
    return {"appliances": []}
