from flask import Blueprint, jsonify, request
from neo4j.exceptions import ConstraintError
from database import db  
from repository.node_repository import NodeRepository

technologies_bp = Blueprint('technologies', __name__)

repo = NodeRepository(db.get_db())

def get_repo():
    """Instancie le repo"""
    return NodeRepository(db.get_db())

@technologies_bp.route('/technologies', methods=['GET'])
def get_technologies():
    try:
        technologies = get_repo().get_nodes_by_label("Technology", order_by="name")
        return jsonify({"technologies": technologies}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@technologies_bp.route("/technologies/<technology_id>", methods=["GET"])
def get_technology_by_id(technology_id):
    try:
        technology = get_repo().get_by_id("Technology", technology_id)

        if not technology:
            return jsonify({"error": "technology not found"}), 404

        return jsonify(technology), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
@technologies_bp.route('/technologies', methods=['POST'])
def create_technology():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON"}), 400

        required_fields = ["libelle"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"{field} is required"}), 400

        try:
            technology = get_repo().create_node("Technology", data)
        except ConstraintError:
            return jsonify({"error": "Technology with this libelle already exists"}), 409

        return jsonify({"technologies": [technology]}), 201

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500