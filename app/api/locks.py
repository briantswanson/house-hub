from flask import Blueprint

locks_bp = Blueprint("locks", __name__, url_prefix="/api/locks")


@locks_bp.route("/", methods=["GET"])
def get_locks():
    # TODO: return lock state via SmartThingsConnector
    return {"locks": []}


@locks_bp.route("/<lock_id>", methods=["POST"])
def set_lock(lock_id):
    # TODO: lock or unlock via SmartThingsConnector
    return {"status": "not implemented"}, 501
