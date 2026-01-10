from flask import Flask, jsonify
from flask_cors import CORS


app = Flask(__name__)

# Active CORS pour permettre les requêtes depuis Angular
CORS(app)

@app.route("/")
def health():
    return jsonify({"status": "Backend running"})

# Exemple d'endpoint API
@app.route("/api/hello")
def hello():
    return jsonify({"message": "Hello from backend!"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
