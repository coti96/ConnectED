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
    try:
        user_data = UserModel.get_profile_with_techs(current_user['email'])
        if not user_data:
            return jsonify({"error": "Utilisateur non trouvé"}), 404
            
        if 'password_hash' in user_data: del user_data['password_hash']
        for key in ['created_at']:
            if key in user_data: user_data[key] = str(user_data[key])
            
        return jsonify(user_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@users_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    current_user = get_jwt_identity()
    data = request.get_json()
    
    try:
        UserModel.update_profile(current_user['email'], data, data.get('technologies'))
        return jsonify({"message": "Profil mis à jour avec succès"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
