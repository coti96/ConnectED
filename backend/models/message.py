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
                id: randomUUID(),
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
        driver = db.get_db()
        with driver.session() as session:
            query = """
            MATCH (u:User {email: $email})
            CALL {
                WITH u
                MATCH (u)-[:SENT]->(m:Message)-[:TO]->(other:User)
                RETURN other.email as other_email, max(m.timestamp) as last_ts
                UNION
                WITH u
                MATCH (other:User)-[:SENT]->(m:Message)-[:TO]->(u)
                RETURN other.email as other_email, max(m.timestamp) as last_ts
            }
            WITH u, other_email, max(last_ts) as last_ts
            MATCH (other:User {email: other_email})
            OPTIONAL MATCH (other)-[:SENT]->(lm_in:Message)-[:TO]->(u)
            WHERE lm_in.timestamp = last_ts
            OPTIONAL MATCH (u)-[:SENT]->(lm_out:Message)-[:TO]->(other)
            WHERE lm_out.timestamp = last_ts
            WITH u, other, last_ts, coalesce(lm_in, lm_out) as last_message
            OPTIONAL MATCH (other)-[:SENT]->(unread:Message)-[:TO]->(u)
            WHERE unread.read = false
            RETURN other, last_message, count(unread) as unread_count
            ORDER BY last_message.timestamp DESC
            """
            result = session.run(query, email=user_email)
            
            conversations = []
            
            for record in result:
                user_node = record['other']
                user_data = dict(user_node.items())
                for key, value in list(user_data.items()):
                    if hasattr(value, 'iso_format'):
                        user_data[key] = value.iso_format()
                
                # Nettoyage et déduplication (au cas où la requête renvoie des doublons)
                if 'password_hash' in user_data: del user_data['password_hash']
                
                last_msg = record.get("last_message")
                last_content = None
                last_ts = None
                if last_msg:
                    last_content = last_msg.get("content")
                    ts = last_msg.get("timestamp")
                    if hasattr(ts, "iso_format"):
                        last_ts = ts.iso_format()
                    else:
                        last_ts = str(ts)

                user_data["last_message"] = last_content
                user_data["last_timestamp"] = last_ts
                user_data["unread_count"] = record.get("unread_count", 0)
                conversations.append(user_data)
                    
            return conversations

    @staticmethod
    def mark_read(viewer_email, other_email):
        driver = db.get_db()
        with driver.session() as session:
            query = """
            MATCH (viewer:User {email: $viewer}) 
            MATCH (other:User {email: $other})
            MATCH (other)-[:SENT]->(m:Message)-[:TO]->(viewer)
            WHERE m.read = false
            SET m.read = true
            RETURN count(m) as c
            """
            record = session.run(query, viewer=viewer_email, other=other_email).single()
            return record["c"] if record else 0

    @staticmethod
    def get_messages(user1_email, user2_email, limit=100, before=None, since=None):
        driver = db.get_db()
        with driver.session() as session:
            if since:
                query = """
                MATCH (u1:User {email: $email1})
                MATCH (u2:User {email: $email2})
                MATCH (sender:User)-[:SENT]->(m:Message)-[:TO]->(receiver:User)
                WHERE (sender = u1 AND receiver = u2) OR (sender = u2 AND receiver = u1)
                  AND m.timestamp > datetime($since)
                RETURN m, sender
                ORDER BY m.timestamp ASC
                LIMIT $limit
                """
                result = session.run(
                    query,
                    email1=user1_email,
                    email2=user2_email,
                    limit=int(limit),
                    since=since,
                )
            else:
                query = """
                MATCH (u1:User {email: $email1})
                MATCH (u2:User {email: $email2})
                MATCH (sender:User)-[:SENT]->(m:Message)-[:TO]->(receiver:User)
                WHERE (sender = u1 AND receiver = u2) OR (sender = u2 AND receiver = u1)
                  AND ($before IS NULL OR m.timestamp < datetime($before))
                RETURN m, sender
                ORDER BY m.timestamp DESC
                LIMIT $limit
                """
                result = session.run(
                    query,
                    email1=user1_email,
                    email2=user2_email,
                    limit=int(limit),
                    before=before,
                )
            
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
            if not since:
                messages.reverse()
            return messages
