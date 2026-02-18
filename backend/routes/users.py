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
    
@users_bp.route('/users/filter', methods=['GET'])
def filter_users():
    """
    Filtre les utilisateurs selon différents critères
    ---
    tags:
      - Users
    parameters:
      - name: name
        in: query
        type: string
        required: false
        description: Filtrer par nom de l'utilisateur
      - name: technology_id
        in: query
        type: string
        required: false
        description: Filtrer par technologies possédées
      - name: project_id
        in: query
        type: string
        required: false
        description: Filtrer par projets associés à l'utilisateur
    responses:
      200:
        description: Liste des utilisateurs correspondant aux filtres
        schema:
          type: object
          properties:
            users:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: string
                  name:
                    type: string
                  email:
                    type: string
                  created_at:
                    type: string
      500:
        description: Erreur serveur
    """
    try:
        repo = get_repo()
        query_params = request.args
        users = repo.get_users_filtered(
            name=query_params.get("name"),
            technology_id=query_params.get("technology_id"),
            project_id=query_params.get("project_id")
        )
        return jsonify({"users": users}), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

# ---------------------------
# POST : Ajouter une tech existante a un utilisateur existant
# --------------------------- 
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
    
@users_bp.route('/users/<user_id>/recommended_projects', methods=['GET'])
def get_recommended_projects(user_id):
    """
    Retourne une liste de projets recommandés pour un utilisateur
    ---
    tags:
      - Users
      - Recommendations
    parameters:
      - name: user_id
        in: path
        type: string
        required: true
        description: ID de l'utilisateur
      - name: domain_id
        in: query
        type: string
        required: false
        description: Filtrer les projets par domaine
      - name: localisation
        in: query
        type: string
        required: false
        description: Filtrer les projets par localisation
      - name: max_results
        in: query
        type: integer
        required: false
        description: Nombre maximum de projets retournés (par défaut 10)
    responses:
      200:
        description: Liste des projets recommandés
        schema:
          type: object
          properties:
            recommended_projects:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: string
                  titre:
                    type: string
                  description:
                    type: string
                  localisation:
                    type: string
                  nombre_places:
                    type: integer
                  statut:
                    type: string
                  created_at:
                    type: string
      404:
        description: Utilisateur non trouvé
      500:
        description: Erreur serveur
    """
    try:
        repo = get_repo()
        params = request.args
        recommended_projects = repo.get_recommended_projects(
            user_id=user_id,
            domain_id=params.get("domain_id"),
            localisation=params.get("localisation"),
            max_results=int(params.get("max_results", 10))
        )
        if not recommended_projects:
            return jsonify({"message": "No recommended projects found"}), 200

        return jsonify({"recommended_projects": recommended_projects}), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

