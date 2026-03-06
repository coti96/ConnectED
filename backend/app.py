from flask import Flask, jsonify
import os
from flask_cors import CORS
from neo4j import GraphDatabase
from database import db
from routes.projects import projects_bp
from routes.users import users_bp

app = Flask(__name__)
CORS(app)
# On autorise Angular (port 4200) à appeler Flask
with app.app_context():
    try:
        db.connect()
    except Exception as e:
        print(f" Erreur de connexion initiale : {e}")
# À l'arrêt du serveur
@app.teardown_appcontext
def shutdown_session(exception=None):
    db.close()   
# Enregistrement des routes
app.register_blueprint(projects_bp)
app.register_blueprint(users_bp)

@app.route('/api/health')
def index():
    driver = db.get_db()
    with driver.session() as session:
        result = session.run("RETURN 'Connexion backend !' AS message")
        # Renvoyer un objet JSON est plus propre pour une API
        return jsonify({"message": result.single()["message"]})
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
