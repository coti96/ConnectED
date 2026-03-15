from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.dashboard import DashboardModel
from models.user import UserModel
from utils.roles import normalize_role
import logging

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard', methods=['GET', 'OPTIONS'])
@jwt_required()
def get_dashboard_data():
    if request.method == 'OPTIONS':
        return jsonify({}), 200
        
    current_user = get_jwt_identity()
    email = current_user['email'] if isinstance(current_user, dict) else current_user
    user_node = UserModel.find_by_email(email)
    user = {
        "email": email,
        "role": normalize_role(user_node.get("role")) if user_node else None,
        "nom": user_node.get("nom") if user_node else None,
        "prenom": user_node.get("prenom") if user_node else None
    }
    
    # 1. Stats globales
    try:
        stats = DashboardModel.get_stats(email)
    except Exception as e:
        logging.exception("Error fetching dashboard stats")
        stats = {"applications_sent": 0, "projects_created": 0, "messages_received": 0}
    
    # 2. Activité récente
    try:
        activity = DashboardModel.get_recent_activity(email)
    except Exception as e:
        logging.exception("Error fetching dashboard activity")
        activity = []
    
    return jsonify({
        "user": user,
        "stats": stats,
        "recent_activity": activity
    })
