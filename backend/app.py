from flask import Flask, jsonify
import os
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from database import db
from flasgger import Swagger
from datetime import timedelta

from routes.projects import projects_bp
from routes.users import users_bp
from routes.auth import auth_bp
from routes.applications import applications_bp
from routes.messages import messages_bp
from routes.dashboard import dashboard_bp
from routes.domains import domains_bp
from routes.technologies import technologies_bp

app = Flask(__name__)
# On change la clé secrète pour une version plus longue (32+ octets) pour éviter les warnings JWT
app.config['JWT_SECRET_KEY'] = 'this-is-a-very-long-and-secure-secret-key-for-connected-2026-esiee'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=7)
CORS(
    app,
    resources={r"/*": {"origins": ["http://localhost:4200", "http://127.0.0.1:4200"]}},
    supports_credentials=True,
    allow_headers=["Content-Type", "Authorization"],
)
jwt = JWTManager(app)
swagger = Swagger(app)

@jwt.unauthorized_loader
def unauthorized_response(callback):
    return jsonify({
        'ok': False,
        'message': 'Missing Authorization Header'
    }), 401

@jwt.invalid_token_loader
def invalid_token_callback(reason):
    return jsonify({
        'ok': False,
        'message': 'Invalid Token',
        'detail': reason
    }), 422

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({
        'ok': False,
        'message': 'Token has expired'
    }), 401

# On autorise Angular (port 4200) à appeler Flask
with app.app_context():
    try:
        db.connect()
    except Exception as e:
        print(f" Erreur de connexion initiale : {e}")
# Enregistrement des routes
app.register_blueprint(projects_bp)
app.register_blueprint(users_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(applications_bp)
app.register_blueprint(messages_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(domains_bp)
app.register_blueprint(technologies_bp)

@app.route('/api/health')
def index():
    driver = db.get_db()
    with driver.session() as session:
        result = session.run("RETURN 'Connexion backend !' AS message")
        # Renvoyer un objet JSON est plus propre pour une API
        return jsonify({"message": result.single()["message"]})
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
