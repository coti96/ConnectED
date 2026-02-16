from flask import Blueprint, jsonify
from database import db 
from repository.node_repository import NodeRepository


domains_bp = Blueprint('domains', __name__)

repo = NodeRepository(db.get_db())

@domains_bp.route('/domains', methods=['GET'])
def get_domains():
    try:
        domains = repo.get_nodes_by_label("Domain", order_by="name")
        return jsonify({"domains": domains}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
@domains_bp.route("/domains/<domain_id>", methods=["GET"])
def get_domain_by_id(domain_id):
    try:
        domain = repo.get_by_id("Domain", domain_id)

        if not domain:
            return jsonify({"error": "Domain not found"}), 404

        return jsonify(domain), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
