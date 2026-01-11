from flask import Flask, jsonify
from flask_cors import CORS
import os


app = Flask(__name__)

# Active CORS pour permettre les requêtes depuis Angular
CORS(app)

# =========================
# Configuration Base de Données
# =========================
DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "connected")
DB_USER = os.getenv("DB_USER", "connected_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "connected_password")


@app.route("/")
def health():
    return jsonify( {
        "status": "Backend running",
        "db_host": DB_HOST})

# Exemple d'endpoint API
@app.route("/api/hello")
def hello():
    return jsonify({"message": "Hello from backend!"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
