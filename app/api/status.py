from flask import Blueprint, jsonify

status_bp = Blueprint("status", __name__, url_prefix="/api/status")


@status_bp.route("/", methods=["GET"])
def get_status():
    # TODO: return full home snapshot across all connectors
    return jsonify({"lights": [], "locks": [], "hvac": [], "appliances": [], "network": {}})
