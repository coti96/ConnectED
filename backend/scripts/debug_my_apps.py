import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.application import ApplicationModel
from database import db

def check_my_apps():
    print("Checking applications for marie@etudiant.com...")
    
    # 1. Vérifier direct dans Neo4j
    driver = db.get_db()
    with driver.session() as session:
        query = """
        MATCH (u:User {email: 'marie@etudiant.com'})-[r:APPLIED_TO]->(p:Project)
        RETURN u.email, r.status, p.titre, r.motivation_message
        """
        result = session.run(query)
        records = list(result)
        print(f"Neo4j Raw Count: {len(records)}")
        for record in records:
            print(f"- {record['p.titre']} ({record['r.status']}) - Msg: {record.get('r.motivation_message', 'N/A')}")

    # 2. Vérifier via le modèle (ce que l'API renvoie)
    try:
        apps = ApplicationModel.get_my_applications('marie@etudiant.com')
        print(f"\nModel Output Count: {len(apps)}")
        print(apps)
    except Exception as e:
        print(f"Model Error: {e}")

if __name__ == "__main__":
    check_my_apps()
