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
        result = session.run("MATCH (p:Project) RETURN p")
        
        projects_list = []
        for record in result:
            # 1. On récupère le nœud Neo4j
            project_node = record["p"]
            
            # 2. On transforme les propriétés en un VRAI dictionnaire JSON compatible
            # C'est ici qu'il fallait faire dict(...)
            project_data = dict(project_node.items())
            
            # 3. Optionnel : Convertir les dates Neo4j en chaînes de caractères
            # (Le JSON n'aime pas les objets 'datetime' de Neo4j)
            if 'created_at' in project_data:
                project_data['created_at'] = str(project_data['created_at'])
            if 'deadline' in project_data:
                project_data['deadline'] = str(project_data['deadline'])

            projects_list.append(project_data)
            
        return {"projects": projects_list} # Flask est content maintenant !



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
