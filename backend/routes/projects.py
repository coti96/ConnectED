from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.project import ProjectModel
from models.user import UserModel

projects_bp = Blueprint('projects', __name__)

@projects_bp.route('/projects', methods=['GET'])
def get_projects():
    """
    Récupère tous les projets
    ---
    tags:
      - Projects
    responses:
      200:
        description: Liste des projets
    """
    try:
        projects = ProjectModel.get_all()
        return jsonify({"projects": projects})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@projects_bp.route('/projects', methods=['POST', 'OPTIONS'])
@jwt_required()
def create_project():
    """
    Crée un nouveau projet
    ---
    tags:
      - Projects
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            titre:
              type: string
            description:
              type: string
            domaine:
              type: string
            nombre_places:
              type: integer
            deadline:
              type: string
    """
    if request.method == 'OPTIONS':
        return jsonify({}), 200
        
    current_user = get_jwt_identity()
    email = current_user['email'] if isinstance(current_user, dict) else current_user
    user_node = UserModel.find_by_email(email)
    if not user_node:
        return jsonify({"error": "Utilisateur introuvable"}), 404
    
    data = request.get_json()
    
    if 'titre' not in data or 'description' not in data:
        return jsonify({"error": "Champs manquants"}), 400
            
    try:
        project_id = ProjectModel.create(data, email)
        return jsonify({"message": "Projet créé avec succès", "id": project_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@projects_bp.route('/projects/<project_id>', methods=['GET'])
def get_project(project_id):
    """
    Récupère un projet par son ID
    ---
    tags:
      - Projects
    parameters:
      - name: project_id
        in: path
        type: string
        required: true
    """
    try:
        project = ProjectModel.get_by_id(project_id)
        if not project:
            return jsonify({"error": "Projet non trouvé"}), 404
        return jsonify({"project": project})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@projects_bp.route('/projects/recommended', methods=['GET', 'OPTIONS'])
@jwt_required()
def get_recommended_projects():
    """
    Récupère les projets recommandés pour l'utilisateur connecté
    ---
    tags:
      - Projects
    """
    if request.method == 'OPTIONS':
        return jsonify({}), 200
        
    current_user = get_jwt_identity()
    email = current_user['email'] if isinstance(current_user, dict) else current_user
    
    try:
        recommendations = ProjectModel.get_recommended(email)
        return jsonify({"recommendations": recommendations})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
