import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import db

def debug_projects():
    print("Listing all projects in Neo4j...")
    
    driver = db.get_db()
    with driver.session() as session:
        query = """
        MATCH (p:Project)
        RETURN elementId(p) as id, p.titre as titre, p.description as description, p.statut as statut, p.domaine as domaine
        """
        result = session.run(query)
        records = list(result)
        print(f"Total Projects found: {len(records)}")
        
        for record in records:
            print(f"ID: {record['id']}")
            print(f"  Title: {record['titre']}")
            print(f"  Desc: {record['description'][:50] if record['description'] else 'None'}")
            print(f"  Status: {record['statut']}")
            print(f"  Domain: {record['domaine']}")
            print("-" * 20)

if __name__ == "__main__":
    debug_projects()
