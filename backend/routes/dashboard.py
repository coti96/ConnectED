from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.dashboard import DashboardModel

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def get_dashboard_data():
    current_user = get_jwt_identity()
    email = current_user['email']
    
    # 1. Stats globales
    stats = DashboardModel.get_stats(email)
    
    # 2. Activité récente
    activity = DashboardModel.get_recent_activity(email)
    
    return jsonify({
        "user": current_user,
        "stats": stats,
        "recent_activity": activity
    })
