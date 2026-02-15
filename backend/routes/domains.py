from flask import Blueprint, jsonify
from database import db 
from node_repository import get_nodes_by_label

# On définit le Blueprint
domains_bp = Blueprint('domains', __name__)

@domains_bp.route('/domains', methods=['GET'])
def get_domains():
    try:
        domains = get_nodes_by_label("Domain", order_by="name")
        return jsonify({"domains": domains}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500