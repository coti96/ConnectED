from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.project import ProjectModel
from models.user import UserModel
from utils.roles import normalize_role

admin_bp = Blueprint('admin', __name__)


def require_admin(email):
    user = UserModel.find_by_email(email)
    role = normalize_role(user.get("role")) if user else None
    return role == "admin"


@admin_bp.route('/admin/projects', methods=['GET', 'OPTIONS'])
@jwt_required()
def admin_list_projects():
    if request.method == 'OPTIONS':
        return jsonify({}), 200

    current_user = get_jwt_identity()
    email = current_user['email'] if isinstance(current_user, dict) else current_user
    if not require_admin(email):
        return jsonify({"error": "Accès refusé"}), 403

    return jsonify({"projects": ProjectModel.get_all()})


@admin_bp.route('/admin/projects/<project_id>/status', methods=['PUT', 'OPTIONS'])
@jwt_required()
def admin_set_project_status(project_id):
    if request.method == 'OPTIONS':
        return jsonify({}), 200

    current_user = get_jwt_identity()
    email = current_user['email'] if isinstance(current_user, dict) else current_user
    if not require_admin(email):
        return jsonify({"error": "Accès refusé"}), 403

    data = request.get_json() or {}
    status = data.get("status")
    if status not in {"en_cours", "ferme"}:
        return jsonify({"error": "Statut invalide"}), 400

    ok = ProjectModel.set_status(project_id, status)
    if not ok:
        return jsonify({"error": "Projet introuvable"}), 404
    return jsonify({"message": "OK"})

