from flask import Blueprint, jsonify
from database import db  # On importe notre instance de base de données

# On définit le Blueprint
users_bp = Blueprint('users', __name__)

@users_bp.route('/users', methods=['GET'])
def get_users():
    # On récupère le driver via notre Singleton
    driver = db.get_db()
    
    try:
        with driver.session() as session:
            result = session.run("MATCH (u:User) RETURN u")
            
            users_list = []
            for record in result:
                user_node = record["u"]
                
                # Conversion en dictionnaire simple
                user_data = dict(user_node.items())
                
                user_data['id'] = user_node.element_id # 
                # Nettoyage des dates pour le JSON
                for key in ['created_at', 'deadline']:
                    if key in user_data:
                        user_data[key] = str(user_data[key])

                users_list.append(user_data)
                
            return jsonify({"users": users_list}) 
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500