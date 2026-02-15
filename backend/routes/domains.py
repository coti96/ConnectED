from flask import Blueprint, jsonify
from database import db  # On importe notre instance de base de données

# On définit le Blueprint
domains_bp = Blueprint('domains', __name__)

@domains_bp.route('/domains', methods=['GET'])
def get_domains():
    # On récupère le driver via notre Singleton
    driver = db.get_db()
    
    try:
        with driver.session() as session:
            result = session.run("MATCH (d:Domain) RETURN d ORDER BY d.name")
            
            domains_list = []
            for record in result:
                domain_node = record["d"]
                
                # Conversion en dictionnaire simple
                domain_data = dict(domain_node.items())
                
                domain_data['id'] = domain_node.element_id # 
                # Nettoyage des dates pour le JSON
                for key in ['created_at', 'deadline']:
                    if key in domain_data:
                        domain_data[key] = str(domain_data[key])

                domains_list.append(domain_data)
                
            return jsonify({"domains": domains_list}) 
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500