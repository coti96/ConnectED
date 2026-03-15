from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.notification import NotificationModel

notifications_bp = Blueprint('notifications', __name__)


@notifications_bp.route('/notifications', methods=['GET', 'OPTIONS'])
@jwt_required()
def list_notifications():
    if request.method == 'OPTIONS':
        return jsonify({}), 200

    current_user = get_jwt_identity()
    email = current_user['email'] if isinstance(current_user, dict) else current_user
    limit = request.args.get("limit", "20")
    items = NotificationModel.list_for_user(email, limit=limit)
    unread = NotificationModel.unread_count(email)
    return jsonify({"notifications": items, "unread": unread})


@notifications_bp.route('/notifications/<notif_id>/read', methods=['PUT', 'OPTIONS'])
@jwt_required()
def mark_notification_read(notif_id):
    if request.method == 'OPTIONS':
        return jsonify({}), 200

    current_user = get_jwt_identity()
    email = current_user['email'] if isinstance(current_user, dict) else current_user
    ok = NotificationModel.mark_read(email, notif_id)
    if not ok:
        return jsonify({"error": "Notification introuvable"}), 404
    return jsonify({"message": "OK"})

