from flask import Blueprint, jsonify
from app.connectors import adsb

adsb_bp = Blueprint("adsb", __name__, url_prefix="/api/adsb")


@adsb_bp.route("/aircraft", methods=["GET"])
def get_aircraft():
    try:
        aircraft = adsb.get_aircraft()
        return jsonify({"aircraft": aircraft, "count": len(aircraft)})
    except Exception as e:
        return jsonify({"error": str(e), "aircraft": [], "count": 0}), 500
