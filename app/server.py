from flask import Flask, jsonify, send_from_directory
from app.api.lights import lights_bp
from app.api.locks import locks_bp
from app.api.hvac import hvac_bp
from app.api.appliances import appliances_bp
from app.api.scenes import scenes_bp
from app.api.network import network_bp
from app.api.status import status_bp


def create_app():
    app = Flask(__name__, static_folder="../static")

    app.register_blueprint(lights_bp)
    app.register_blueprint(locks_bp)
    app.register_blueprint(hvac_bp)
    app.register_blueprint(appliances_bp)
    app.register_blueprint(scenes_bp)
    app.register_blueprint(network_bp)
    app.register_blueprint(status_bp)

    @app.route("/")
    def index():
        return send_from_directory(app.static_folder, "index.html")

    @app.route("/health")
    def health():
        return jsonify({"status": "ok"})

    return app
