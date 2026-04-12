from flask import Blueprint

network_bp = Blueprint("network", __name__, url_prefix="/api/network")


@network_bp.route("/", methods=["GET"])
def get_network():
    # TODO: return presence (Eero) + DNS stats (Pi-hole)
    return {"presence": [], "pihole": {}}


@network_bp.route("/block", methods=["POST"])
def block_domain():
    # TODO: block domain via PiholeConnector
    return {"status": "not implemented"}, 501


@network_bp.route("/unblock", methods=["POST"])
def unblock_domain():
    # TODO: unblock domain via PiholeConnector
    return {"status": "not implemented"}, 501
