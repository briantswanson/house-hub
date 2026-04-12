from flask import Blueprint

scenes_bp = Blueprint("scenes", __name__, url_prefix="/api/scenes")


@scenes_bp.route("/<name>", methods=["POST"])
def run_scene(name):
    # TODO: run named scene via scenes/definitions.py
    return {"status": "not implemented"}, 501
