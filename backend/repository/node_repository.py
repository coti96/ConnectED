from neo4j.time import DateTime


class NodeRepository:

    def __init__(self, driver):
        self.driver = driver


    def _serialize_node(self, node):
        node_data = dict(node)
        for key, value in node_data.items():
            if isinstance(value, DateTime):
                node_data[key] = value.iso_format()
        return node_data
   
    # GET BY ID
   
    def get_by_id(self, label, id):
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


    # GET BY LABEL
    def get_nodes_by_label(self, label, order_by=None):
        with self.driver.session() as session:
            query = f"MATCH (n:{label}) RETURN n"
            if order_by:
                query += f" ORDER BY n.{order_by}"
            result = session.run(query)
            return [
                self._serialize_node(record["n"])
                for record in result
            ]
