from flask import Blueprint, jsonify, request
from database import db  
from repository.node_repository import NodeRepository
import traceback

users_bp = Blueprint('users', __name__)
repo = NodeRepository(db.get_db())

def get_repo():
    """Instancie le repo"""
    return NodeRepository(db.get_db())

@users_bp.route('/users', methods=['GET'])
def get_users():
    """
    Récupère tous les utilisateurs.
    ---
    tags:
      - Users
    responses:
      200:
        description: Liste de tous les utilisateurs
        schema:
          type: object
          properties:
            users:
              type: array
              items:
                type: object
      500:
        description: Erreur serveur
    """
    try:
        users = get_repo().get_nodes_by_label("User", order_by="name")
        return jsonify({"users": users}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@users_bp.route("/users/<user_id>", methods=["GET"])
def get_user_by_id(user_id):
    """
    Récupère un utilisateur par son ID.
    ---
    tags:
      - Users
    parameters:
      - name: user_id
        in: path
        type: string
        required: true
        description: ID de l'utilisateur
    responses:
      200:
        description: Utilisateur trouvé
        schema:
          type: object
      404:
        description: Utilisateur non trouvé
      500:
        description: Erreur serveur
    """
    try:
        user = get_repo().get_by_id("User", user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        return jsonify(user), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@users_bp.route("/users/<user_id>/technologies/<technology_id>", methods=["POST"])
def add_technology_to_user(user_id, technology_id):
    """
    Associe une technologie existante à un utilisateur.
    ---
    tags:
      - Users
    parameters:
      - name: user_id
        in: path
        type: string
        required: true
        description: ID de l'utilisateur
      - name: technology_id
        in: path
        type: string
        required: true
        description: ID de la technologie à ajouter
    responses:
      201:
        description: Technologie ajoutée avec succès à l'utilisateur
      404:
        description: Utilisateur ou technologie non trouvée
      500:
        description: Erreur serveur
    """
    try:
        repo = get_repo()
        result = repo.add_relation(
            source_label="User",
            source_id=user_id,
            relation_type="HAS_TECHNOLOGY",
            target_label="Technology",
            target_id=technology_id
        )
        if not result:
            return jsonify({"error": "User or Technology not found"}), 404
        return jsonify({"message": "Technology successfully added to User", "relation": result}), 201
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
