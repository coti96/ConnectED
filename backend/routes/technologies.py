from flask import Blueprint, jsonify, request
from neo4j.exceptions import ConstraintError
from database import db  
from repository.node_repository import NodeRepository
import traceback

technologies_bp = Blueprint('technologies', __name__)
repo = NodeRepository(db.get_db())

def get_repo():
    """Instancie le repo"""
    return NodeRepository(db.get_db())

@technologies_bp.route('/technologies', methods=['GET'])
def get_technologies():
    """
    Récupère toutes les technologies.
    ---
    tags:
      - Technologies
    responses:
      200:
        description: Liste de toutes les technologies
        schema:
          type: object
          properties:
            technologies:
              type: array
              items:
                type: object
      500:
        description: Erreur serveur
    """
    try:
        technologies = get_repo().get_nodes_by_label("Technology", order_by="name")
        return jsonify({"technologies": technologies}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@technologies_bp.route("/technologies/<technology_id>", methods=["GET"])
def get_technology_by_id(technology_id):
    """
    Récupère une technologie par son ID.
    ---
    tags:
      - Technologies
    parameters:
      - name: technology_id
        in: path
        type: string
        required: true
        description: ID de la technologie
    responses:
      200:
        description: Technologie trouvée
        schema:
          type: object
      404:
        description: Technologie non trouvée
      500:
        description: Erreur serveur
    """
    try:
        technology = get_repo().get_by_id("Technology", technology_id)
        if not technology:
            return jsonify({"error": "technology not found"}), 404
        return jsonify(technology), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------------------------
# GET Technologies FILTER BY
# --------------------------- 
@technologies_bp.route('/technologies/filter', methods=['GET'])
def filter_technologies():
    """
    Filtre les technologies selon différents critères
    ---
    tags:
      - Technologies
    parameters:
      - name: libelle
        in: query
        type: string
        required: false
        description: Filtrer par nom de la technologie
      - name: domain_id
        in: query
        type: string
        required: false
        description: Filtrer par domaine
      - name: used_in_project_id
        in: query
        type: string
        required: false
        description: Filtrer par projets utilisant cette technologie
    responses:
      200:
        description: Liste des technologies correspondant aux filtres
        schema:
          type: object
          properties:
            technologies:
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
      500:
        description: Erreur serveur
    """
    try:
        repo = get_repo()
        query_params = request.args
        technologies = repo.get_technologies_filtered(
            libelle=query_params.get("libelle"),
            domain_id=query_params.get("domain_id"),
            used_in_project_id=query_params.get("used_in_project_id")
        )
        return jsonify({"technologies": technologies}), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@technologies_bp.route('/technologies', methods=['POST'])
def create_technology():
    """
    Crée une nouvelle technologie et l'associe à un domaine.
    ---
    tags:
      - Technologies
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - libelle
            - domain_id
          properties:
            libelle:
              type: string
              description: Nom de la technologie
            domain_id:
              type: string
              description: ID du domaine associé
    responses:
      201:
        description: Technologie créée avec succès
      400:
        description: JSON invalide ou champs manquants
      404:
        description: Domaine introuvable
      409:
        description: Technologie avec ce libelle existe déjà
      500:
        description: Erreur serveur
    """
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
            return jsonify({"error": "Technology with this libelle already exists"}), 409

        if not technology:
            return jsonify({"error": "Domain not found"}), 404

        return jsonify({"technologies": [technology]}), 201
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@technologies_bp.route('/technologies/<technology_id>', methods=['PUT'])
def update_technology(technology_id):
    """
    Met à jour une technologie existante.
    ---
    tags:
      - Technologies
    parameters:
      - name: technology_id
        in: path
        type: string
        required: true
        description: ID de la technologie à mettre à jour
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            libelle:
              type: string
    responses:
      200:
        description: Technologie mise à jour
      400:
        description: JSON invalide
      404:
        description: Technologie non trouvée
      409:
        description: Technologie avec ce libelle existe déjà
      500:
        description: Erreur serveur
    """
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
    """
    Supprime une technologie existante.
    ---
    tags:
      - Technologies
    parameters:
      - name: technology_id
        in: path
        type: string
        required: true
        description: ID de la technologie à supprimer
    responses:
      200:
        description: Technologie supprimée avec succès
      404:
        description: Technologie non trouvée
      500:
        description: Erreur serveur
    """
    try:
        deleted = get_repo().delete_node("Technology", technology_id)
        if not deleted:
            return jsonify({"error": "Technology not found"}), 404
        return jsonify({"message": "Technology deleted successfully"}), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@technologies_bp.route("/technologies/<technology_id>/domains/<domain_id>", methods=["POST"])
def add_technology_to_domain(technology_id, domain_id):
    """
    Associe une technologie existante à un domaine existant.
    ---
    tags:
      - Technologies
    parameters:
      - name: technology_id
        in: path
        type: string
        required: true
        description: ID de la technologie
      - name: domain_id
        in: path
        type: string
        required: true
        description: ID du domaine
    responses:
      201:
        description: Relation créée avec succès
      404:
        description: Technologie ou domaine introuvable
      500:
        description: Erreur serveur
    """
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
            return jsonify({"error": "Technology or Domain not found"}), 404
        return jsonify({"message": "Technology successfully associated with Domain","relation": result}), 201
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
