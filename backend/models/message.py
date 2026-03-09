from database import db
from datetime import datetime

class MessageModel:
    @staticmethod
    def create(sender_email, receiver_email, content):
        driver = db.get_db()
        with driver.session() as session:
            # Créer le message et les relations
            query = """
            MATCH (sender:User {email: $sender_email})
            MATCH (receiver:User {email: $receiver_email})
            CREATE (m:Message {
                content: $content,
                timestamp: datetime(),
                read: false
            })
            CREATE (sender)-[:SENT]->(m)
            CREATE (m)-[:TO]->(receiver)
            RETURN m
            """
            result = session.run(query, sender_email=sender_email, receiver_email=receiver_email, content=content)
            record = result.single()
            return record is not None

    @staticmethod
    def get_conversations(user_email):
        """Récupère la liste des personnes avec qui l'utilisateur a discuté"""
        driver = db.get_db()
        with driver.session() as session:
            # Cette requête cherche tous les messages envoyés OU reçus par l'utilisateur
            # et retourne l'AUTRE personne impliquée.
            query = """
            MATCH (u:User {email: $email})
            OPTIONAL MATCH (u)-[:SENT]->(:Message)-[:TO]->(other1:User)
            OPTIONAL MATCH (other2:User)-[:SENT]->(:Message)-[:TO]->(u)
            WITH u, collect(DISTINCT other1) + collect(DISTINCT other2) as others
            UNWIND others as other
            WITH DISTINCT other
            WHERE other IS NOT NULL
            RETURN other
            """
            result = session.run(query, email=user_email)
            
            conversations = []
            seen_emails = set()
            
            for record in result:
                user_node = record['other']
                user_data = dict(user_node.items())
                
                # Nettoyage et déduplication (au cas où la requête renvoie des doublons)
                if 'password_hash' in user_data: del user_data['password_hash']
                
                if user_data['email'] not in seen_emails and user_data['email'] != user_email:
                    conversations.append(user_data)
                    seen_emails.add(user_data['email'])
                    
            return conversations

    @staticmethod
    def get_messages(user1_email, user2_email):
        """Récupère l'historique des messages entre deux utilisateurs"""
        driver = db.get_db()
        with driver.session() as session:
            query = """
            MATCH (u1:User {email: $email1})
            MATCH (u2:User {email: $email2})
            MATCH (sender:User)-[:SENT]->(m:Message)-[:TO]->(receiver:User)
            WHERE (sender = u1 AND receiver = u2) OR (sender = u2 AND receiver = u1)
            RETURN m, sender
            ORDER BY m.timestamp ASC
            """
            result = session.run(query, email1=user1_email, email2=user2_email)
            
            messages = []
            for record in result:
                msg_data = dict(record['m'].items())
                # Conversion sécurisée du timestamp
                if hasattr(msg_data['timestamp'], 'iso_format'):
                    msg_data['timestamp'] = msg_data['timestamp'].iso_format()
                else:
                    msg_data['timestamp'] = str(msg_data['timestamp'])
                    
                msg_data['sender_email'] = record['sender']['email']
                messages.append(msg_data)
            return messages
