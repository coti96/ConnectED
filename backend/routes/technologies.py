from flask import Blueprint, jsonify
from database import db  # On importe notre instance de base de données

# On définit le Blueprint
technologies_bp = Blueprint('technologies', __name__)

@technologies_bp.route('/technologies', methods=['GET'])
def get_technologies():
    # On récupère le driver via notre Singleton
    driver = db.get_db()
    
    try:
        with driver.session() as session:
            result = session.run("MATCH (t:Technology) RETURN t ORDER BY t.name")         
            technologies_list = []
            for record in result:
                technology_node = record["t"]             
                # Conversion en dictionnaire simple
                technology_data = dict(technology_node.items())              
                technology_data['id'] = technology_node.element_id # 
                # Nettoyage des dates pour le JSON
                for key in ['created_at', 'deadline']:
                    if key in technology_data:
                        technology_data[key] = str(technology_data[key])
                technologies_list.append(technology_data)             
            return jsonify({"technologies": technologies_list})         
    except Exception as e:
        return jsonify({"error": str(e)}), 500