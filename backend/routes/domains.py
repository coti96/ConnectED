from flask import Blueprint, jsonify, request
from neo4j.exceptions import ConstraintError
from database import db 
from repository.node_repository import NodeRepository
import traceback

domains_bp = Blueprint('domains', __name__)

def get_repo():
    return NodeRepository(db.get_db())

# ---------------------------
# GET all domains
# ---------------------------
@domains_bp.route('/domains', methods=['GET'])
def get_domains():
    """
    Récupère tous les domains
    ---
    tags:
      - Domains
    responses:
      200:
        description: Liste des domains
        schema:
          type: object
          properties:
            domains:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: string
                  libelle:
                    type: string
                  created_at:
                    type: string
                  updated_at:
                    type: string
      500:
        description: Erreur serveur
    """
    try:
        domains = get_repo().get_nodes_by_label("Domain", order_by="name")
        return jsonify({"domains": domains}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------------------------
# GET domain by ID
# ---------------------------
@domains_bp.route("/domains/<domain_id>", methods=["GET"])
def get_domain_by_id(domain_id):
    """
    Récupère un domain par son ID
    ---
    tags:
      - Domains
    parameters:
      - name: domain_id
        in: path
        type: string
        required: true
        description: ID du domain
    responses:
      200:
        description: Domain trouvé
        schema:
          type: object
          properties:
            id:
              type: string
            libelle:
              type: string
            created_at:
              type: string
            updated_at:
              type: string
      404:
        description: Domain non trouvé
      500:
        description: Erreur serveur
    """
    try:
        domain = get_repo().get_by_id("Domain", domain_id)
        if not domain:
            return jsonify({"error": "Domain not found"}), 404
        return jsonify(domain), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------------------------
# POST create domain
# ---------------------------
@domains_bp.route('/domains', methods=['POST'])
def create_domain():
    """
    Crée un nouveau domain
    ---
    tags:
      - Domains
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - libelle
          properties:
            libelle:
              type: string
              description: Nom du domain
    responses:
      201:
        description: Domain créé
        schema:
          type: object
          properties:
            domains:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: string
                  libelle:
                    type: string
                  created_at:
                    type: string
      400:
        description: JSON invalide ou champ manquant
      409:
        description: Domain déjà existant
      500:
        description: Erreur serveur
    """
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

# ---------------------------
# PUT update domain
# ---------------------------
@domains_bp.route('/domains/<domain_id>', methods=['PUT'])
def update_domain(domain_id):
    """
    Met à jour un domain existant
    ---
    tags:
      - Domains
    parameters:
      - name: domain_id
        in: path
        type: string
        required: true
        description: ID du domain
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            libelle:
              type: string
    responses:
      200:
        description: Domain mis à jour
        schema:
          type: object
          properties:
            domains:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: string
                  libelle:
                    type: string
                  created_at:
                    type: string
                  updated_at:
                    type: string
      400:
        description: JSON invalide
      404:
        description: Domain non trouvé
      409:
        description: Domain déjà existant
      500:
        description: Erreur serveur
    """
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

# ---------------------------
# DELETE domain
# ---------------------------
@domains_bp.route('/domains/<domain_id>', methods=['DELETE'])
def delete_domain(domain_id):
    """
    Supprime un domain existant
    ---
    tags:
      - Domains
    parameters:
      - name: domain_id
        in: path
        type: string
        required: true
        description: ID du domain
    responses:
      200:
        description: Domain supprimé
      404:
        description: Domain non trouvé
      500:
        description: Erreur serveur
    """
    try:
        deleted = get_repo().delete_node("Domain", domain_id)
        if not deleted:
            return jsonify({"error": "Domain not found"}), 404
        return jsonify({"message": "Domain deleted successfully"}), 200

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
