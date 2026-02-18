from flask import Blueprint, jsonify, request  
from neo4j.exceptions import ConstraintError   
from database import db
from repository.node_repository import NodeRepository
import traceback 

projects_bp = Blueprint('projects', __name__)

def get_repo():
    """
    Instancie le repo à chaque appel 
    """
    return NodeRepository(db.get_db())

# ---------------------------
# GET all projects
# ---------------------------
@projects_bp.route('/projects', methods=['GET'])
def get_projects():
    """
    Récupère tous les projets
    ---
    tags:
      - Projects
    responses:
      200:
        description: Liste des projets
        schema:
          type: object
          properties:
            projects:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: string
                  titre:
                    type: string
                  description:
                    type: string
                  localisation:
                    type: string
                  nombre_places:
                    type: integer
                  statut:
                    type: string
                  created_at:
                    type: string
                  updated_at:
                    type: string
      500:
        description: Erreur serveur
    """
    try:
        projects = get_repo().get_nodes_by_label("Project", order_by="titre")
        return jsonify({"projects": projects}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------------------------
# GET project by ID
# ---------------------------
@projects_bp.route("/projects/<project_id>", methods=["GET"])
def get_project_by_id(project_id):
    """
    Récupère un projet par son ID
    ---
    tags:
      - Projects
    parameters:
      - name: project_id
        in: path
        type: string
        required: true
        description: ID du projet
    responses:
      200:
        description: Projet trouvé
        schema:
          type: object
          properties:
            id:
              type: string
            titre:
              type: string
            description:
              type: string
            localisation:
              type: string
            nombre_places:
              type: integer
            statut:
              type: string
            created_at:
              type: string
            updated_at:
              type: string
      404:
        description: Projet non trouvé
      500:
        description: Erreur serveur
    """
    try:
        project = get_repo().get_by_id("Project", project_id)
        if not project:
            return jsonify({"error": "Project not found"}), 404 
        return jsonify(project), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------------------------
# POST create project
# ---------------------------
@projects_bp.route('/projects', methods=['POST'])
def create_project():
    """
    Crée un nouveau projet
    ---
    tags:
      - Projects
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - titre
            - description
            - localisation
            - nombre_places
            - statut
          properties:
            titre:
              type: string
            description:
              type: string
            localisation:
              type: string
            nombre_places:
              type: integer
            statut:
              type: string
    responses:
      201:
        description: Projet créé
        schema:
          type: object
          properties:
            projects:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: string
                  titre:
                    type: string
                  description:
                    type: string
                  localisation:
                    type: string
                  nombre_places:
                    type: integer
                  statut:
                    type: string
                  created_at:
                    type: string
      400:
        description: JSON invalide ou champ manquant
      409:
        description: Projet déjà existant
      500:
        description: Erreur serveur
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON"}), 400

        required_fields = ["titre", "description", "localisation", "nombre_places", "statut"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"{field} is required"}), 400

        try:
            data["nombre_places"] = int(data["nombre_places"])
        except (ValueError, TypeError):  
            return jsonify({"error": "nombre_places must be an integer"}), 400

        try:
            project = get_repo().create_node("Project", data)
        except ConstraintError:
            return jsonify({"error": "Project with this titre already exists"}), 409  

        return jsonify({"projects": [project]}), 201

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

# ---------------------------
# POST add domain to project
# ---------------------------
@projects_bp.route("/projects/<project_id>/domains/<domain_id>", methods=["POST"])
def add_domain_to_project(project_id, domain_id):
    """
    Ajoute un domaine à un projet
    ---
    tags:
      - Projects
    parameters:
      - name: project_id
        in: path
        type: string
        required: true
        description: ID du projet
      - name: domain_id
        in: path
        type: string
        required: true
        description: ID du domaine
    responses:
      201:
        description: Domaine ajouté au projet
        schema:
          type: object
          properties:
            message:
              type: string
            relation:
              type: object
      404:
        description: Projet ou Domaine non trouvé
      500:
        description: Erreur serveur
    """
    try:
        result = get_repo().add_relation(
            source_label="Project",
            source_id=project_id,
            relation_type="IN_DOMAIN",
            target_label="Domain",
            target_id=domain_id
        )
        if not result:
            return jsonify({"error": "Project or Domain not found"}), 404
        return jsonify({"message": "Domain added to Project", "relation": result}), 201
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

# ---------------------------
# POST add technology to project
# ---------------------------
@projects_bp.route("/projects/<project_id>/technologies/<technology_id>", methods=["POST"])
def add_technology_to_project(project_id, technology_id):
    """
    Ajoute une technologie à un projet
    ---
    tags:
      - Projects
    parameters:
      - name: project_id
        in: path
        type: string
        required: true
        description: ID du projet
      - name: technology_id
        in: path
        type: string
        required: true
        description: ID de la technologie
    responses:
      201:
        description: Technologie ajoutée au projet
        schema:
          type: object
          properties:
            message:
              type: string
            relation:
              type: object
      404:
        description: Projet ou Technologie non trouvé
      500:
        description: Erreur serveur
    """
    try:
        result = get_repo().add_relation(
            source_label="Project",
            source_id=project_id,
            relation_type="USES",
            target_label="Technology",
            target_id=technology_id
        )
        if not result:
            return jsonify({"error": "Project or Technology not found"}), 404
        return jsonify({"message": "Technology added to Project", "relation": result}), 201
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

# ---------------------------
# PUT update project
# ---------------------------
@projects_bp.route('/projects/<project_id>', methods=['PUT'])
def update_project(project_id):
    """
    Met à jour un projet existant
    ---
    tags:
      - Projects
    parameters:
      - name: project_id
        in: path
        type: string
        required: true
        description: ID du projet
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            titre:
              type: string
            description:
              type: string
            localisation:
              type: string
            nombre_places:
              type: integer
            statut:
              type: string
    responses:
      200:
        description: Projet mis à jour
        schema:
          type: object
          properties:
            projects:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: string
                  titre:
                    type: string
                  description:
                    type: string
                  localisation:
                    type: string
                  nombre_places:
                    type: integer
                  statut:
                    type: string
                  created_at:
                    type: string
                  updated_at:
                    type: string
      400:
        description: JSON invalide
      404:
        description: Projet non trouvé
      409:
        description: Projet déjà existant
      500:
        description: Erreur serveur
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON"}), 400

        if "nombre_places" in data:
            try:
                data["nombre_places"] = int(data["nombre_places"])
            except (ValueError, TypeError):
                return jsonify({"error": "nombre_places must be an integer"}), 400

        try:
            project = get_repo().update_node("Project", project_id, data)
        except ConstraintError:
            return jsonify({"error": "Project with this titre already exists"}), 409

        if not project:
            return jsonify({"error": "Project not found"}), 404

        return jsonify({"projects": [project]}), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

# ---------------------------
# DELETE project
# ---------------------------
@projects_bp.route('/projects/<project_id>', methods=['DELETE'])
def delete_project(project_id):
    """
    Supprime un projet existant
    ---
    tags:
      - Projects
    parameters:
      - name: project_id
        in: path
        type: string
        required: true
        description: ID du projet
    responses:
      200:
        description: Projet supprimé
      404:
        description: Projet non trouvé
      500:
        description: Erreur serveur
    """
    try:
        deleted = get_repo().delete_node("Project", project_id)
        if not deleted:
            return jsonify({"error": "Project not found"}), 404
        return jsonify({"message": "Project deleted successfully"}), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
