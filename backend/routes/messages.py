from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.message import MessageModel
from models.user import UserModel

messages_bp = Blueprint('messages', __name__)

@messages_bp.route('/messages', methods=['POST'])
@jwt_required()
def send_message():
    current_user = get_jwt_identity()
    email = current_user['email'] if isinstance(current_user, dict) else current_user
    data = request.get_json()
    
    receiver_email = data.get('receiver_email')
    content = data.get('content')
    
    if not receiver_email or not content:
        return jsonify({"error": "Destinataire et contenu requis"}), 400
        
    # Vérifier que le destinataire existe
    receiver = UserModel.find_by_email(receiver_email)
    if not receiver:
        return jsonify({"error": "Utilisateur introuvable"}), 404
        
    success = MessageModel.create(email, receiver_email, content)
    if not success:
        return jsonify({"error": "Erreur lors de l'envoi"}), 500
        
    return jsonify({"message": "Message envoyé"}), 201

@messages_bp.route('/conversations', methods=['GET', 'OPTIONS'])
@jwt_required()
def get_conversations():
    if request.method == 'OPTIONS':
        return jsonify({}), 200
        
    current_user = get_jwt_identity()
    # Gestion sécurisée de l'identité
    email = current_user['email'] if isinstance(current_user, dict) else current_user
    
    conversations = MessageModel.get_conversations(email)
    return jsonify({"conversations": conversations})

@messages_bp.route('/messages/<other_email>', methods=['GET', 'OPTIONS'])
@jwt_required()
def get_chat_history(other_email):
    if request.method == 'OPTIONS':
        return jsonify({}), 200
        
    current_user = get_jwt_identity()
    # Gestion sécurisée de l'identité
    email = current_user['email'] if isinstance(current_user, dict) else current_user
    
    messages = MessageModel.get_messages(email, other_email)
    return jsonify({"messages": messages})
