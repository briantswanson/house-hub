from flask import Blueprint

hvac_bp = Blueprint("hvac", __name__, url_prefix="/api/hvac")


@hvac_bp.route("/", methods=["GET"])
def get_hvac():
    # TODO: return HVAC state via SensiboConnector
    return {"units": []}


@hvac_bp.route("/<unit_id>", methods=["POST"])
def set_hvac(unit_id):
    # TODO: set mode/temp/fan via SensiboConnector
    return {"status": "not implemented"}, 501
