from flask import Blueprint, jsonify
from database import db  
from repository.node_repository import get_nodes_by_label


technologies_bp = Blueprint('technologies', __name__)

@technologies_bp.route('/technologies', methods=['GET'])
def get_technologies():
    try:
        technologies = get_nodes_by_label("Technology", order_by="name")
        return jsonify({"technologies": technologies}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500