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
        
    def add_relation(self, source_label, source_id, relation_type, target_label, target_id, relation_properties=None):
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

    # ─────────────────────────────────────────────
    # MÉTHODES FILTER
    # ─────────────────────────────────────────────

    def get_domains_filtered(self, libelle=None, used_in_project_id=None, technology_id=None):
        """
        Filtre les domaines selon différents critères.
        - libelle           : recherche partielle (CONTAINS) sur le libelle
        - used_in_project_id: domaines utilisés par un projet donné
        - technology_id     : domaines contenant une technologie donnée
        """
        conditions = []
        params = {}

        match_clauses = "MATCH (n:Domain)"

        if used_in_project_id:
            match_clauses = "MATCH (p:Project {id: $used_in_project_id})-[:IN_DOMAIN]->(n:Domain)"
            params["used_in_project_id"] = used_in_project_id

        if technology_id:
            match_clauses += "\nMATCH (t:Technology {id: $technology_id})-[:IN_DOMAIN]->(n)"
            params["technology_id"] = technology_id

        if libelle:
            conditions.append("toLower(n.libelle) CONTAINS toLower($libelle)")
            params["libelle"] = libelle

        where_clause = ("WHERE " + " AND ".join(conditions)) if conditions else ""

        query = f"""
        {match_clauses}
        {where_clause}
        RETURN DISTINCT n
        ORDER BY n.libelle
        """

        with self.driver.session() as session:
            result = session.run(query, **params)
            return [self._serialize_node(record["n"]) for record in result]

    def get_technologies_filtered(self, libelle=None, domain_id=None, used_in_project_id=None):
        """
        Filtre les technologies selon différents critères.
        """
        conditions = []
        params = {}

        match_clauses = "MATCH (n:Technology)"

        if domain_id:
            match_clauses = "MATCH (n:Technology)-[:IN_DOMAIN]->(:Domain {id: $domain_id})"
            params["domain_id"] = domain_id

        if used_in_project_id:
            # Correction: REQUIRES_TECH au lieu de USES
            match_clauses += "\nMATCH (:Project {id: $used_in_project_id})-[:REQUIRES_TECH]->(n)"
            params["used_in_project_id"] = used_in_project_id

        if libelle:
            conditions.append("toLower(n.libelle) CONTAINS toLower($libelle)")
            params["libelle"] = libelle

        where_clause = ("WHERE " + " AND ".join(conditions)) if conditions else ""

        query = f"""
        {match_clauses}
        {where_clause}
        RETURN DISTINCT n
        ORDER BY n.libelle
        """

        with self.driver.session() as session:
            result = session.run(query, **params)
            return [self._serialize_node(record["n"]) for record in result]

    def get_projects_filtered(self, titre=None, localisation=None, domain_id=None, technology_id=None, statut=None):
        """
        Filtre les projets selon différents critères.
        """
        conditions = []
        params = {}

        match_clauses = "MATCH (n:Project)"

        if domain_id:
            match_clauses = "MATCH (n:Project)-[:IN_DOMAIN]->(:Domain {id: $domain_id})"
            params["domain_id"] = domain_id

        if technology_id:
            # Correction: REQUIRES_TECH au lieu de USES
            match_clauses += "\nMATCH (n)-[:REQUIRES_TECH]->(:Technology {id: $technology_id})"
            params["technology_id"] = technology_id

        if titre:
            conditions.append("toLower(n.titre) CONTAINS toLower($titre)")
            params["titre"] = titre

        if localisation:
            conditions.append("toLower(n.localisation) CONTAINS toLower($localisation)")
            params["localisation"] = localisation

        if statut:
            conditions.append("n.statut = $statut")
            params["statut"] = statut

        where_clause = ("WHERE " + " AND ".join(conditions)) if conditions else ""

        query = f"""
        {match_clauses}
        {where_clause}
        RETURN DISTINCT n
        ORDER BY n.titre
        """

        with self.driver.session() as session:
            result = session.run(query, **params)
            return [self._serialize_node(record["n"]) for record in result]

    def get_users_filtered(self, name=None, technology_id=None, project_id=None):
        """
        Filtre les utilisateurs selon différents critères.
        """
        conditions = []
        params = {}

        match_clauses = "MATCH (n:User)"

        if technology_id:
            # Correction: HAS_TECH au lieu de HAS_TECHNOLOGY
            match_clauses = "MATCH (n:User)-[:HAS_TECH]->(:Technology {id: $technology_id})"
            params["technology_id"] = technology_id

        if project_id:
            # Correction: APPLIED_TO au lieu de PARTICIPATES_IN (pour l'instant)
            match_clauses += "\nMATCH (n)-[:APPLIED_TO]->(:Project {id: $project_id})"
            params["project_id"] = project_id

        if name:
            conditions.append("toLower(n.nom) CONTAINS toLower($name) OR toLower(n.prenom) CONTAINS toLower($name)")
            params["name"] = name

        where_clause = ("WHERE " + " AND ".join(conditions)) if conditions else ""

        query = f"""
        {match_clauses}
        {where_clause}
        RETURN DISTINCT n
        ORDER BY n.nom
        """

        with self.driver.session() as session:
            result = session.run(query, **params)
            return [self._serialize_node(record["n"]) for record in result]

    def get_recommended_projects(self, user_id, domain_id=None, localisation=None, max_results=10):
        """
        Retourne des projets recommandés pour un utilisateur basé sur les technologies qu'il possède.
        """
        filters = []
        if domain_id:
            filters.append("(p)-[:IN_DOMAIN]->(:Domain {id: $domain_id})")
        if localisation:
            filters.append("toLower(p.localisation) CONTAINS toLower($localisation)")

        filter_cypher = ("WHERE " + " AND ".join(filters)) if filters else ""

        # Note: On utilise REQUIRES_TECH au lieu de USES pour être cohérent avec le seed
        query = f"""
        MATCH (u:User {{id: $user_id}})-[:HAS_TECH]->(t:Technology)<-[:REQUIRES_TECH]-(p:Project)
        {filter_cypher}
        RETURN DISTINCT p
        LIMIT $max_results
        """

        params = {
            "user_id": user_id,
            "max_results": max_results,
        }
        if domain_id:
            params["domain_id"] = domain_id
        if localisation:
            params["localisation"] = localisation

        with self.driver.session() as session:
            result = session.run(query, **params)
            return [self._serialize_node(record["p"]) for record in result]
