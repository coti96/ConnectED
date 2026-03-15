from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.application import ApplicationModel
from models.project import ProjectModel
from models.user import UserModel
from models.notification import NotificationModel
from utils.roles import normalize_role

applications_bp = Blueprint('applications', __name__)


def can_manage_project(email, project_id):
    user_node = UserModel.find_by_email(email)
    role = normalize_role(user_node.get("role")) if user_node else None
    if role == "admin":
        return True

    project = ProjectModel.get_by_id(project_id)
    creator_email = project.get("creator", {}).get("email") if project else None
    return creator_email == email

# --- Candidat ---

@applications_bp.route('/projects/<project_id>/apply', methods=['POST', 'OPTIONS'])
@jwt_required()
def apply_to_project(project_id):
    if request.method == 'OPTIONS':
        return jsonify({}), 200
        
    current_user = get_jwt_identity()
    email = current_user['email'] if isinstance(current_user, dict) else current_user

    project = ProjectModel.get_by_id(project_id)
    creator_email = project.get("creator", {}).get("email") if project else None
    if creator_email and creator_email == email:
        return jsonify({"error": "Vous ne pouvez pas postuler à votre propre projet"}), 400
    
    success, error = ApplicationModel.create(email, project_id)
    if error:
        return jsonify({"error": error}), 400
        
    return jsonify({"message": "Candidature envoyée avec succès"}), 201


@applications_bp.route('/projects/<project_id>/apply', methods=['DELETE', 'OPTIONS'])
@jwt_required()
def cancel_application(project_id):
    if request.method == 'OPTIONS':
        return jsonify({}), 200

    current_user = get_jwt_identity()
    email = current_user['email'] if isinstance(current_user, dict) else current_user

    ok = ApplicationModel.cancel(email, project_id)
    if not ok:
        return jsonify({"error": "Impossible d'annuler la candidature (déjà traitée ou inexistante)"}), 400

    return jsonify({"message": "Candidature annulée"}), 200

@applications_bp.route('/my-applications', methods=['GET', 'OPTIONS'])
@jwt_required()
def get_my_applications():
    if request.method == 'OPTIONS':
        return jsonify({}), 200
        
    current_user = get_jwt_identity()
    email = current_user['email'] if isinstance(current_user, dict) else current_user
    
    apps = ApplicationModel.get_my_applications(email)
    return jsonify({"applications": apps})

# --- Créateur de Projet ---

@applications_bp.route('/projects/<project_id>/applications', methods=['GET', 'OPTIONS'])
@jwt_required()
def get_project_applications(project_id):
    if request.method == 'OPTIONS':
        return jsonify({}), 200
        
    current_user = get_jwt_identity()
    email = current_user['email'] if isinstance(current_user, dict) else current_user
    if not can_manage_project(email, project_id):
        return jsonify({"error": "Accès refusé"}), 403
    
    apps = ApplicationModel.get_by_project(project_id)
    return jsonify({"applications": apps})

@applications_bp.route('/projects/<project_id>/applications/<applicant_email>/status', methods=['PUT', 'OPTIONS'])
@jwt_required()
def update_application_status(project_id, applicant_email):
    if request.method == 'OPTIONS':
        return jsonify({}), 200
        
    current_user = get_jwt_identity()
    email = current_user['email'] if isinstance(current_user, dict) else current_user
    if not can_manage_project(email, project_id):
        return jsonify({"error": "Accès refusé"}), 403
    
    data = request.get_json()
    new_status = data.get('status')
    
    if new_status not in ['ACCEPTED', 'REJECTED', 'PENDING']:
        return jsonify({"error": "Statut invalide"}), 400

    if new_status == 'ACCEPTED':
        info = ApplicationModel.get_acceptance_info(project_id, applicant_email)
        if info:
            capacity = info.get("capacity")
            accepted_count = info.get("accepted_count", 0)
            current_status = info.get("current_status")
            if capacity is not None and current_status != 'ACCEPTED' and accepted_count >= int(capacity):
                return jsonify({"error": "Plus de places disponibles pour ce projet"}), 400
        
    success = ApplicationModel.update_status(project_id, applicant_email, new_status)
    if not success:
        return jsonify({"error": "Impossible de mettre à jour la candidature"}), 400

    project = ProjectModel.get_by_id(project_id)
    titre = project.get("titre") if project else "un projet"
    NotificationModel.create_for_user(
        applicant_email,
        "application_status",
        f"Votre candidature au projet \"{titre}\" a été mise à jour : {new_status}.",
        {"project_id": project.get("id") if project else project_id, "status": new_status},
    )
        
    return jsonify({"message": "Statut mis à jour"})
