from neo4j.time import DateTime
from neo4j.exceptions import ConstraintError
from datetime import datetime
import uuid

class NodeRepository:
    
    def __init__(self, driver):
        self.driver = driver

    def _serialize_node(self, node):
        """Converts Neo4j node objects to serializable dictionaries."""
        node_data = dict(node)
        for key, value in node_data.items():
            if isinstance(value, DateTime):
                node_data[key] = value.iso_format()
        return node_data

    def get_by_id(self, label, node_id):
        """Retourne un dictionnaire JSON correspondant au node trouvé, ou None."""
        query = f"MATCH (n:{label} {{id: $id}}) RETURN n"
        with self.driver.session() as session:
            result = session.run(query, id=node_id)
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
        Retourne le node (dict).
        """
        properties = properties.copy()
        properties["id"] = str(uuid.uuid4())
        properties["created_at"] = datetime.utcnow().isoformat()

        props_string = ", ".join([f"{key}: ${key}" for key in properties.keys()])
        query = f"CREATE (n:{label} {{ {props_string} }}) RETURN n"
        
        with self.driver.session() as session:
            result = session.run(query, **properties)
            record = result.single()
            if not record:
                raise Exception("Node creation failed")
            return self._serialize_node(record["n"])

    def create_node_with_relation(self, label, properties, relation_type, target_label, target_id):
        """
        Crée un node et le relie immédiatement à un node existant.
        Retourne le node, ou None si le node cible est introuvable.
        """
        properties = properties.copy()
        properties["id"] = str(uuid.uuid4())
        properties["created_at"] = datetime.utcnow().isoformat()

        props_string = ", ".join([f"{key}: ${key}" for key in properties.keys()])
        query = f"""
        MATCH (target:{target_label} {{id: $target_id}})
        CREATE (n:{label} {{ {props_string} }})
        MERGE (n)-[:{relation_type}]->(target)
        RETURN n
        """
        params = {"target_id": target_id, **properties}

        with self.driver.session() as session:
            result = session.run(query, **params)
            record = result.single()
            if not record:
                return None
            return self._serialize_node(record["n"])
        
    def add_relation(self,source_label, source_id,relation_type,target_label,target_id, relation_properties=None):
        relation_properties = relation_properties or {}
        props_string = ""
        if relation_properties:
            props_string = "{" + ", ".join(
                [f"{key}: ${key}" for key in relation_properties.keys()]
            ) + "}"
        query = f"""
        MATCH (source:{source_label} {{id: $source_id}})
        MATCH (target:{target_label} {{id: $target_id}})
        MERGE (source)-[r:{relation_type} {props_string}]->(target)
        RETURN source, target, r
        """
        params = {
            "source_id": source_id,
            "target_id": target_id,
            **relation_properties
        }

        with self.driver.session() as session:
            result = session.run(query, **params)
            record = result.single()
            if not record:
                return None

            return {
                "source": self._serialize_node(record["source"]),
                "target": self._serialize_node(record["target"]),
                "relation": relation_type
            }

    def update_node(self, label, node_id, properties):
        """
        Met à jour les propriétés d'un node existant.
        Retourne le node mis à jour.
        """
        properties = properties.copy()
        properties.pop("id", None)
        properties.pop("created_at", None)
        properties["updated_at"] = datetime.utcnow().isoformat()

        set_string = ", ".join([f"n.{key} = ${key}" for key in properties.keys()])
        query = f"""
        MATCH (n:{label} {{id: $id}})
        SET {set_string}
        RETURN n
        """
        params = {"id": node_id, **properties}

        with self.driver.session() as session:
            result = session.run(query, **params)
            record = result.single()
            if not record:
                return None
            return self._serialize_node(record["n"])

    def delete_node(self, label, node_id):
        """
        Supprime un node par son id.
        Retourne True si supprimé, False si introuvable.
        """
        query = f"""
        MATCH (n:{label} {{id: $id}})
        WITH n, count(n) AS found
        DETACH DELETE n
        RETURN found
        """
        with self.driver.session() as session:
            result = session.run(query, id=node_id)
            record = result.single()
            return record is not None and record["found"] > 0