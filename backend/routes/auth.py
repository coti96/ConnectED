from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token
from models.user import UserModel

auth_bp = Blueprint('auth', __name__)
bcrypt = Bcrypt()

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    required = ['email', 'password', 'nom', 'prenom', 'role']
    for field in required:
        if field not in data:
            return jsonify({"error": f"Champ {field} obligatoire"}), 400

    try:
        password_hash = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        user, error = UserModel.create(
            data['email'], password_hash, data['nom'], data['prenom'], data['role']
        )
        
        if error:
            return jsonify({"error": error}), 409
            
        return jsonify({"message": "Utilisateur créé avec succès"}), 201
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    # BYPASS DE TEST
    identity = {
        "email": "student6@mail.com",
        "role": "Etudiante",
        "nom": "Dev",
        "prenom": "Mode"
    }
    access_token = create_access_token(identity=identity["student6@mail.com"])
    return jsonify({
        "message": "Bypass activé",
        "token": access_token,
        "user": identity
    }), 200
    # data = request.get_json()
    # email = data.get('email')
    # password = data.get('password')
    
    # if not email or not password:
    #     return jsonify({"error": "Email et mot de passe requis"}), 400
        
    # try:
    #     user_node = UserModel.find_by_email(email)
        
    #     if not user_node:
    #         return jsonify({"error": "Email ou mot de passe incorrect"}), 401
            
    #     stored_hash = user_node.get('password_hash')
    #     if not stored_hash or not bcrypt.check_password_hash(stored_hash, password):
    #         return jsonify({"error": "Email ou mot de passe incorrect"}), 401
            
    #     identity = {
    #         "email": user_node.get('email'),
    #         "role": user_node.get('role'),
    #         "nom": user_node.get('nom'),
    #         "prenom": user_node.get('prenom')
    #     }
    #     access_token = create_access_token(identity=identity["email"])
        
    #     return jsonify({
    #         "message": "Connexion réussie",
    #         "token": access_token,
    #         "user": identity
    #     }), 200
            
    # except Exception as e:
    #     return jsonify({"error": str(e)}), 500
