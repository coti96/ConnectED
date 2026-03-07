from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.application import ApplicationModel
from models.project import ProjectModel
from models.user import UserModel

applications_bp = Blueprint('applications', __name__)

# --- Candidat ---

@applications_bp.route('/projects/<project_id>/apply', methods=['POST'])
@jwt_required()
def apply_to_project(project_id):
    current_user = get_jwt_identity()
    
    # Empêcher de postuler à son propre projet
    # (Logique déjà en partie gérée par le front, mais sécurité supplémentaire)
    
    success, error = ApplicationModel.create(current_user['email'], project_id)
    if error:
        return jsonify({"error": error}), 400
        
    return jsonify({"message": "Candidature envoyée avec succès"}), 201

@applications_bp.route('/my-applications', methods=['GET'])
@jwt_required()
def get_my_applications():
    current_user = get_jwt_identity()
    apps = ApplicationModel.get_my_applications(current_user['email'])
    return jsonify({"applications": apps})

# --- Créateur de Projet ---

@applications_bp.route('/projects/<project_id>/applications', methods=['GET'])
@jwt_required()
def get_project_applications(project_id):
    current_user = get_jwt_identity()
    
    # Vérifier que l'utilisateur est bien le créateur du projet
    # TODO: Ajouter une vérification stricte ici
    
    apps = ApplicationModel.get_by_project(project_id)
    return jsonify({"applications": apps})

@applications_bp.route('/projects/<project_id>/applications/<applicant_email>/status', methods=['PUT'])
@jwt_required()
def update_application_status(project_id, applicant_email):
    current_user = get_jwt_identity()
    data = request.get_json()
    new_status = data.get('status')
    
    if new_status not in ['ACCEPTED', 'REJECTED', 'PENDING']:
        return jsonify({"error": "Statut invalide"}), 400
        
    success = ApplicationModel.update_status(project_id, applicant_email, new_status)
    if not success:
        return jsonify({"error": "Impossible de mettre à jour la candidature"}), 400
        
    return jsonify({"message": "Statut mis à jour"})
