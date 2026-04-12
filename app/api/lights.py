from flask import Blueprint

lights_bp = Blueprint("lights", __name__, url_prefix="/api/lights")


@lights_bp.route("/", methods=["GET"])
def get_lights():
    # TODO: return all lights + state via HueConnector
    return {"lights": []}


@lights_bp.route("/<light_id>", methods=["POST"])
def set_light(light_id):
    # TODO: set light state via HueConnector
    return {"status": "not implemented"}, 501
