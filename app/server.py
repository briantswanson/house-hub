from flask import Flask, jsonify


def create_app():
    app = Flask(__name__, static_folder="../static")

    @app.route("/health")
    def health():
        return jsonify({"status": "ok"})

    return app
