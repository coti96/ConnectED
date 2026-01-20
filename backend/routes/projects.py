from flask import Blueprint, jsonify
from database import db  # On importe notre instance de base de données

# On définit le Blueprint
projects_bp = Blueprint('projects', __name__)

@projects_bp.route('/projects', methods=['GET'])
def get_projects():
    # On récupère le driver via notre Singleton
    driver = db.get_db()
    
    try:
        with driver.session() as session:
            result = session.run("MATCH (p:Project) RETURN p")
            
            projects_list = []
            for record in result:
                project_node = record["p"]
                
                # Conversion en dictionnaire simple
                project_data = dict(project_node.items())
                
                # Ajout de l'ID interne Neo4j (souvent utile pour le front)
                project_data['id'] = project_node.element_id # 
                # Nettoyage des dates pour le JSON
                for key in ['created_at', 'deadline']:
                    if key in project_data:
                        project_data[key] = str(project_data[key])

                projects_list.append(project_data)
                
            return jsonify({"projects": projects_list}) 
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500