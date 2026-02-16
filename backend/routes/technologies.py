from flask import Blueprint, jsonify
from database import db  
from repository.node_repository import NodeRepository

technologies_bp = Blueprint('technologies', __name__)

repo = NodeRepository(db.get_db())

@technologies_bp.route('/technologies', methods=['GET'])
def get_technologies():
    try:
        technologies = repo.get_nodes_by_label("Technology", order_by="name")
        return jsonify({"technologies": technologies}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@technologies_bp.route("/technologies/<technology_id>", methods=["GET"])
def get_technology_by_id(technology_id):
    try:
        technology = repo.get_by_id("Technology", technology_id)

        if not technology:
            return jsonify({"error": "technology not found"}), 404

        return jsonify(technology), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500