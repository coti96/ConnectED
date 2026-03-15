from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt
from models.user import UserModel
from utils.roles import normalize_role

users_bp = Blueprint('users', __name__)
bcrypt = Bcrypt()

@users_bp.route('/users', methods=['GET'])
def get_users():
    """
    Récupère tous les utilisateurs
    ---
    tags:
      - Users
    """
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
    """
    Récupère le profil de l'utilisateur connecté
    ---
    tags:
      - Users
    """
    current_user = get_jwt_identity()
    # Gestion sécurisée de l'identité (string ou dict)
    email = current_user['email'] if isinstance(current_user, dict) else current_user
    
    try:
        user_data = UserModel.get_profile_with_techs(email)
        if not user_data:
            return jsonify({"error": "Utilisateur non trouvé"}), 404
            
        if 'password_hash' in user_data: del user_data['password_hash']
        if 'role' in user_data:
            user_data['role'] = normalize_role(user_data.get('role'))
        for key in ['created_at']:
            if key in user_data: user_data[key] = str(user_data[key])
            
        return jsonify(user_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@users_bp.route('/profile', methods=['PUT', 'OPTIONS'])
@jwt_required()
def update_profile():
    """
    Met à jour le profil de l'utilisateur connecté
    ---
    tags:
      - Users
    """
    if request.method == 'OPTIONS':
        return jsonify({}), 200

    current_user = get_jwt_identity()
    email = current_user['email'] if isinstance(current_user, dict) else current_user
    data = request.get_json() or {}
    technologies = data.get('technologies')
    UserModel.update_profile(email, data, technologies)
    return jsonify({"message": "Profil mis à jour avec succès"}), 200


@users_bp.route('/profile/password', methods=['PUT', 'OPTIONS'])
@jwt_required()
def update_password():
    if request.method == 'OPTIONS':
        return jsonify({}), 200

    current_user = get_jwt_identity()
    email = current_user['email'] if isinstance(current_user, dict) else current_user

    data = request.get_json() or {}
    current_password = data.get("current_password")
    new_password = data.get("new_password")
    if not current_password or not new_password:
        return jsonify({"error": "Champs manquants"}), 400
    if len(str(new_password)) < 6:
        return jsonify({"error": "Mot de passe trop court"}), 400

    user_node = UserModel.find_by_email(email)
    if not user_node:
        return jsonify({"error": "Utilisateur introuvable"}), 404

    stored_hash = user_node.get("password_hash")
    if not stored_hash or not bcrypt.check_password_hash(stored_hash, current_password):
        return jsonify({"error": "Mot de passe actuel incorrect"}), 401

    new_hash = bcrypt.generate_password_hash(new_password).decode("utf-8")
    ok = UserModel.update_password(email, new_hash)
    if not ok:
        return jsonify({"error": "Impossible de mettre à jour"}), 500
    return jsonify({"message": "Mot de passe mis à jour"}), 200
