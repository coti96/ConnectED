from flask import Blueprint, jsonify
from database import db  
from repository.node_repository import NodeRepository


users_bp = Blueprint('users', __name__)

repo = NodeRepository(db.get_db())

@users_bp.route('/users', methods=['GET'])
def get_users():
    try:
        users = repo.get_nodes_by_label("User", order_by="name")
        return jsonify({"users": users}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
@users_bp.route("/users/<user_id>", methods=["GET"])
def get_user_by_id(user_id):
    try:
        user = repo.get_by_id("User", user_id)

        if not user:
            return jsonify({"error": "User not found"}), 404

        return jsonify(user), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@users_bp.route("/users/<user_id>/technologies/<technology_id>",methods=["POST"])
def add_technology_to_user(user_id, technology_id):
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
            return jsonify({
                "error": "User or Technology not found"
            }), 404

        return jsonify({
            "message": "Technology successfully added to User",
            "relation": result
        }), 201

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
