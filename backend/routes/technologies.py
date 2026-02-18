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
    
# Fields required : 
# "domain_id": "",
# "libelle": ""    
@technologies_bp.route('/technologies', methods=['POST'])
def create_technology():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON"}), 400
        required_fields = ["libelle", "domain_id"]

        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"{field} is required"}), 400

        domain_id = data.pop("domain_id")
        repo = get_repo()
        try:
            technology = repo.create_node_with_relation(
                label="Technology",
                properties=data,
                relation_type="IN_DOMAIN",
                target_label="Domain",
                target_id=domain_id
            )
        except ConstraintError:
            return jsonify({
                "error": "Technology with this libelle already exists"
            }), 409


        if not technology:
            return jsonify({
                "error": "Domain not found"
            }), 404


        return jsonify({
            "technologies": [technology]
        }), 201


    except Exception as e:

        traceback.print_exc()

        return jsonify({
            "error": str(e)
        }), 500 
    
@technologies_bp.route('/technologies/<technology_id>', methods=['PUT'])
def update_technology(technology_id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON"}), 400

        try:
            technology = get_repo().update_node("Technology", technology_id, data)
        except ConstraintError:
            return jsonify({"error": "Technology with this libelle already exists"}), 409

        if not technology:
            return jsonify({"error": "Technology not found"}), 404

        return jsonify({"technologies": [technology]}), 200

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@technologies_bp.route('/technologies/<technology_id>', methods=['DELETE'])
def delete_technology(technology_id):
    
@technologies_bp.route('/technologies/<technology_id>/domains/<domain_id>',methods=['POST'])
def add_technology_to_domain(technology_id, domain_id):

    try:

        repo = get_repo()

        result = repo.add_relation(
            source_label="Technology",
            source_id=technology_id,
            relation_type="IN_DOMAIN",
            target_label="Domain",
            target_id=domain_id
        )


        if not result:

            return jsonify({
                "error": "Technology or Domain not found"
            }), 404


        return jsonify({
            "message": "Technology successfully associated with Domain",
            "relation": result
        }), 201


    except Exception as e:

        traceback.print_exc()

        return jsonify({
            "error": str(e)
        }), 500

    try:
        deleted = get_repo().delete_node("Technology", technology_id)
        if not deleted:
            return jsonify({"error": "Technology not found"}), 404
        return jsonify({"message": "Technology deleted successfully"}), 200

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500