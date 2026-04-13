from dotenv import load_dotenv
load_dotenv()

from app.server import create_app  # noqa: E402

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
