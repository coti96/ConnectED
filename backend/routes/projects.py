from flask import Blueprint, jsonify
from database import db  
from node_repository import get_nodes_by_label

projects_bp = Blueprint('projects', __name__)

@projects_bp.route('/projects', methods=['GET'])
def get_projects():
    try:
        projects = get_nodes_by_label("Project", order_by="name")
        return jsonify({"projects": projects}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500