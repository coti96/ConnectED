from flask import Blueprint, jsonify, request
from neo4j.exceptions import ConstraintError
from database import db 
from repository.node_repository import NodeRepository


domains_bp = Blueprint('domains', __name__)

def get_repo():
    return NodeRepository(db.get_db())

@domains_bp.route('/domains', methods=['GET'])
def get_domains():
    try:
        domains = get_repo().get_nodes_by_label("Domain", order_by="name")
        return jsonify({"domains": domains}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
@domains_bp.route("/domains/<domain_id>", methods=["GET"])
def get_domain_by_id(domain_id):
    try:
        domain = get_repo().get_by_id("Domain", domain_id)
        if not domain:
            return jsonify({"error": "Domain not found"}), 404
        return jsonify(domain), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@domains_bp.route('/domains', methods=['POST'])
def create_domain():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON"}), 400

        required_fields = ["libelle"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"{field} is required"}), 400

        try:
            domain = get_repo().create_node("Domain", data)
        except ConstraintError:
            return jsonify({"error": "Domain with this libelle already exists"}), 409

        return jsonify({"domains": [domain]}), 201

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
    
    
@domains_bp.route('/domains/<domain_id>', methods=['PUT'])
def update_domain(domain_id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON"}), 400

        try:
            domain = get_repo().update_node("Domain", domain_id, data)
        except ConstraintError:
            return jsonify({"error": "Domain with this libelle already exists"}), 409

        if not domain:
            return jsonify({"error": "Domain not found"}), 404

        return jsonify({"domains": [domain]}), 200

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@domains_bp.route('/domains/<domain_id>', methods=['DELETE'])
def delete_domain(domain_id):
    try:
        deleted = get_repo().delete_node("Domain", domain_id)
        if not deleted:
            return jsonify({"error": "Domain not found"}), 404
        return jsonify({"message": "Domain deleted successfully"}), 200

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500