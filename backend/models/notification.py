import json
from database import db


class NotificationModel:
    @staticmethod
    def create_for_user(email, notif_type, message, data=None):
        driver = db.get_db()
        payload = json.dumps(data or {})
        with driver.session() as session:
            query = """
            MATCH (u:User {email: $email})
            CREATE (n:Notification {
                id: randomUUID(),
                type: $type,
                message: $message,
                data: $data,
                read: false,
                created_at: datetime()
            })
            MERGE (u)-[:HAS_NOTIFICATION]->(n)
            RETURN n.id as id
            """
            record = session.run(query, email=email, type=notif_type, message=message, data=payload).single()
            return record["id"] if record else None

    @staticmethod
    def list_for_user(email, limit=20):
        driver = db.get_db()
        with driver.session() as session:
            query = """
            MATCH (u:User {email: $email})-[:HAS_NOTIFICATION]->(n:Notification)
            RETURN n
            ORDER BY n.created_at DESC
            LIMIT $limit
            """
            result = session.run(query, email=email, limit=int(limit))
            items = []
            for record in result:
                node = record["n"]
                data = dict(node.items())
                for k, v in list(data.items()):
                    if hasattr(v, "iso_format"):
                        data[k] = v.iso_format()
                try:
                    data["data"] = json.loads(data.get("data") or "{}")
                except Exception:
                    data["data"] = {}
                items.append(data)
            return items

    @staticmethod
    def unread_count(email):
        driver = db.get_db()
        with driver.session() as session:
            query = """
            MATCH (u:User {email: $email})-[:HAS_NOTIFICATION]->(n:Notification)
            WHERE n.read = false
            RETURN count(n) as c
            """
            record = session.run(query, email=email).single()
            return record["c"] if record else 0

    @staticmethod
    def mark_read(email, notif_id):
        driver = db.get_db()
        with driver.session() as session:
            query = """
            MATCH (u:User {email: $email})-[:HAS_NOTIFICATION]->(n:Notification {id: $id})
            SET n.read = true
            RETURN n.id as id
            """
            record = session.run(query, email=email, id=notif_id).single()
            return record is not None

