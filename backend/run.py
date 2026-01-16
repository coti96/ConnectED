from flask import Flask, jsonify
import os
from neo4j import GraphDatabase


app = Flask(__name__)

# Récupération des variables Docker
uri = os.getenv("DB_URI", "bolt://db:7687")
user = os.getenv("DB_USER", "neo4j")
password = os.getenv("DB_PASSWORD", "connected_password")

# Initialisation du driver Neo4j
driver = GraphDatabase.driver(uri, auth=(user, password))

@app.route('/projects')
def get_projects():
    with driver.session() as session:
        # Une requête Cypher simple
        result = session.run("MATCH (p:Project) RETURN p LIMIT 10")
        projects = [record["p"].items() for record in result]
        return {"projects": projects}



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
