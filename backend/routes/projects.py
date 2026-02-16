from flask import Blueprint, jsonify
from database import db  
from repository.node_repository import NodeRepository

projects_bp = Blueprint('projects', __name__)

repo = NodeRepository(db.get_db())

@projects_bp.route('/projects', methods=['GET'])
def get_projects():
    try:
        projects = repo.get_nodes_by_label("Project", order_by="name")
        return jsonify({"projects": projects}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
@projects_bp.route("/projects/<project_id>", methods=["GET"])
def get_project_by_id(project_id):
    try:
        project = repo.get_by_id("Project", project_id)

        if not project:
            return jsonify({"error": "project not found"}), 404

        return jsonify(project), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500