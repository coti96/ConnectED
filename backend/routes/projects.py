from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.project import ProjectModel

projects_bp = Blueprint('projects', __name__)

@projects_bp.route('/projects', methods=['GET'])
def get_projects():
    try:
        projects = ProjectModel.get_all()
        for p in projects:
            for key in ['created_at', 'deadline']:
                if key in p: p[key] = str(p[key])
        return jsonify({"projects": projects})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@projects_bp.route('/projects', methods=['POST'])
@jwt_required()
def create_project():
    current_user = get_jwt_identity()
    data = request.get_json()
    
    required = ['titre', 'description', 'domaine', 'deadline']
    for field in required:
        if field not in data:
            return jsonify({"error": f"Champ {field} manquant"}), 400
            
    try:
        project_id = ProjectModel.create(data, current_user['email'])
        return jsonify({"message": "Projet créé avec succès", "id": project_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@projects_bp.route('/projects/recommended', methods=['GET'])
@jwt_required()
def get_recommended_projects():
    current_user = get_jwt_identity()
    
    try:
        recommendations = ProjectModel.get_recommended(current_user['email'])
        for p in recommendations:
            for key in ['created_at', 'deadline']:
                if key in p: p[key] = str(p[key])
        return jsonify({"recommendations": recommendations})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
