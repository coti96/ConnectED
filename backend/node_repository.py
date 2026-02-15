from database import db


def get_nodes_by_label(label, order_by=None):
    driver = db.get_db()

    with driver.session() as session:
        query = f"MATCH (n:{label}) RETURN n"
        
        if order_by:
            query += f" ORDER BY n.{order_by}"
        
        result = session.run(query)

        nodes_list = []

        for record in result:
            node = record["n"]
            node_data = dict(node)
            node_data["id"] = node.element_id

            for key in ['created_at', 'deadline']:
                if key in node_data and node_data[key] is not None:
                    node_data[key] = str(node_data[key])

            nodes_list.append(node_data)

        return nodes_list
