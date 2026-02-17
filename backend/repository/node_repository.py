from neo4j.time import DateTime
from neo4j.exceptions import ConstraintError
from datetime import datetime
import uuid


class NodeRepository:
    def __init__(self, driver):
        self.driver = driver

    def _serialize_node(self, node):
        node_data = dict(node)
        for key, value in node_data.items():
            if isinstance(value, DateTime):
                node_data[key] = value.iso_format()
        return node_data

    def get_by_id(self, label, id):
        """Retourne un dictionnaire JSON correspondant au node trouvé, ou None."""
        query = f"""
        MATCH (n:{label} {{id: $id}})
        RETURN n
        """
        with self.driver.session() as session:
            result = session.run(query, id=id)
            record = result.single()
            if record:
                return self._serialize_node(record["n"])
            return None

    def get_nodes_by_label(self, label, order_by=None):
        """Retourne une liste de dictionnaires JSON pour tous les nodes du label donné."""
        query = f"MATCH (n:{label}) RETURN n"
        if order_by:
            query += f" ORDER BY n.{order_by}"
        with self.driver.session() as session:
            result = session.run(query)
            return [self._serialize_node(record["n"]) for record in result]

    def create_node(self, label, properties):
        """
        Crée un node dans Neo4j avec un ID et created_at.
        Retourne le node sérialisé (dict).
        """
        properties = properties.copy()  #
        properties["id"] = str(uuid.uuid4())
        properties["created_at"] = datetime.utcnow().isoformat()

        props_string = ", ".join([f"{key}: ${key}" for key in properties.keys()])
        query = f"""
        CREATE (n:{label} {{ {props_string} }})
        RETURN n
        """
        with self.driver.session() as session:
            result = session.run(query, **properties)  
            record = result.single()
            if not record:
                raise Exception("Node creation failed")
            return self._serialize_node(record["n"])