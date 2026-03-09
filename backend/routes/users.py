from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import UserModel

users_bp = Blueprint('users', __name__)

@users_bp.route('/users', methods=['GET'])
def get_users():
    try:
        users_list = UserModel.get_all()
        # Nettoyage
        for user in users_list:
            if 'password_hash' in user: del user['password_hash']
            for key in ['created_at']:
                if key in user: user[key] = str(user[key])
        return jsonify({"users": users_list}) 
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@users_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    current_user = get_jwt_identity()
    # Gestion sécurisée de l'identité (string ou dict)
    email = current_user['email'] if isinstance(current_user, dict) else current_user
    
    try:
        user_data = UserModel.get_profile_with_techs(email)
        if not user_data:
            return jsonify({"error": "Utilisateur non trouvé"}), 404
            
        if 'password_hash' in user_data: del user_data['password_hash']
        for key in ['created_at']:
            if key in user_data: user_data[key] = str(user_data[key])
            
        return jsonify(user_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@users_bp.route('/profile', methods=['PUT', 'OPTIONS'])
def update_profile():
    if request.method == 'OPTIONS':
        return jsonify({}), 200
        
    print("DEBUG: Entering update_profile (JWT CHECK RESTORED)")
    # On restaure la vérification manuelle pour être sûr
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({"error": "No Authorization header"}), 401
            
        print(f"DEBUG: Auth Header present: {auth_header[:20]}...")
        
        # On peut laisser @jwt_required() faire le travail normalement,
        # mais ici je le fais manuellement pour tester
        from flask_jwt_extended import decode_token
        token = auth_header.split(" ")[1]
        decoded = decode_token(token)
        current_user = decoded['sub']
        
        print(f"DEBUG: Decoded user: {current_user}")
        
        email = current_user['email'] if isinstance(current_user, dict) else current_user
        
        data = request.get_json()
        technologies = data.get('technologies')
        
        result = UserModel.update_profile(email, data, technologies)
        return jsonify({"message": "Profil mis à jour avec succès"}), 200
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
