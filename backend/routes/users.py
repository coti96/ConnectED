from flask import Blueprint, jsonify
from database import db  
from repository.node_repository import get_nodes_by_label


users_bp = Blueprint('users', __name__)

@users_bp.route('/users', methods=['GET'])
def get_users():
    try:
        users = get_nodes_by_label("User", order_by="name")
        return jsonify({"users": users}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500