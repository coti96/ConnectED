from flask import Flask, jsonify
import os
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from database import db
from flasgger import Swagger
from datetime import timedelta
import logging
from werkzeug.exceptions import HTTPException

from routes.projects import projects_bp
from routes.users import users_bp
from routes.auth import auth_bp
from routes.applications import applications_bp
from routes.messages import messages_bp
from routes.dashboard import dashboard_bp
from routes.domains import domains_bp
from routes.technologies import technologies_bp
from routes.notifications import notifications_bp
from routes.admin import admin_bp

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.getenv(
    "JWT_SECRET_KEY",
    "this-is-a-very-long-and-secure-secret-key-for-connected-2026-esiee",
)
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=7)

origins_env = os.getenv("CORS_ORIGINS", "http://localhost:4200,http://127.0.0.1:4200")
allowed_origins = [o.strip() for o in origins_env.split(",") if o.strip()]
CORS(
    app,
    resources={r"/*": {"origins": allowed_origins}},
    supports_credentials=True,
    allow_headers=["Content-Type", "Authorization"],
)
jwt = JWTManager(app)
swagger = Swagger(app)
logging.basicConfig(level=logging.INFO)

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

@app.errorhandler(HTTPException)
def http_exception_handler(e):
    return jsonify({
        'ok': False,
        'error': e.name,
        'message': e.description
    }), e.code

@app.errorhandler(Exception)
def unhandled_exception_handler(e):
    logging.exception("Unhandled exception")
    return jsonify({
        'ok': False,
        'error': 'Internal Server Error',
        'message': str(e)
    }), 500

# On autorise Angular (port 4200) à appeler Flask
with app.app_context():
    try:
        db.connect()
    except Exception as e:
        logging.exception("Erreur de connexion initiale")
# Enregistrement des routes
app.register_blueprint(projects_bp)
app.register_blueprint(users_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(applications_bp)
app.register_blueprint(messages_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(domains_bp)
app.register_blueprint(technologies_bp)
app.register_blueprint(notifications_bp)
app.register_blueprint(admin_bp)

@app.route('/api/health')
def index():
    driver = db.get_db()
    with driver.session() as session:
        result = session.run("RETURN 'Connexion backend !' AS message")
        # Renvoyer un objet JSON est plus propre pour une API
        return jsonify({"message": result.single()["message"]})
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
