from flask import Blueprint, jsonify, request  
from neo4j.exceptions import ConstraintError   
from database import db
from repository.node_repository import NodeRepository
import traceback  # ✅ manquait (utilisé dans create_project)

projects_bp = Blueprint('projects', __name__)


def get_repo():
    """
    Instancie le repo à chaque appel 
    """
    return NodeRepository(db.get_db())


@projects_bp.route('/projects', methods=['GET'])
def get_projects():
    try:
        projects = get_repo().get_nodes_by_label("Project", order_by="titre")
        return jsonify({"projects": projects}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@projects_bp.route("/projects/<project_id>", methods=["GET"])
def get_project_by_id(project_id):
    try:
        project = get_repo().get_by_id("Project", project_id)
        if not project:
            return jsonify({"error": "Project not found"}), 404  # ✅ majuscule cohérente
        return jsonify(project), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@projects_bp.route('/projects', methods=['POST'])
def create_project():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON"}), 400

        required_fields = ["titre", "description", "localisation", "nombre_places", "statut"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"{field} is required"}), 400

        try:
            data["nombre_places"] = int(data["nombre_places"])
        except (ValueError, TypeError):  
            return jsonify({"error": "nombre_places must be an integer"}), 400

        try:
            project = get_repo().create_node("Project", data)
        except ConstraintError:
            return jsonify({"error": "Project with this titre already exists"}), 409  

        return jsonify({"projects": [project]}), 201

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500