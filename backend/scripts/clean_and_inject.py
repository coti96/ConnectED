import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import db

def clean_duplicates():
    print("Cleaning duplicate applications for Marie...")
    
    driver = db.get_db()
    with driver.session() as session:
        # Supprimer TOUTES les relations APPLIED_TO pour Marie
        query_delete = """
        MATCH (u:User {email: 'marie@etudiant.com'})-[r:APPLIED_TO]->(p:Project)
        DELETE r
        """
        session.run(query_delete)
        print("✅ Deleted all existing applications.")
        
        # Réinjecter PROPREMENT (une seule fois)
        print("🔹 Re-creating single applications...")
        
        # 1. Accepted - Analyse de données IA (En s'assurant qu'on prend UN SEUL projet si multiples)
        session.run("""
        MATCH (u:User {email: 'marie@etudiant.com'})
        MATCH (p:Project {titre: 'Analyse de données IA'})
        WITH u, p LIMIT 1
        MERGE (u)-[r:APPLIED_TO]->(p)
        SET r.status = 'ACCEPTED', 
            r.date = datetime() - duration('P2D'),
            r.motivation_message = "J'ai hâte de commencer ce projet data !"
        """)
        
        # 2. Pending - Plateforme E-commerce Bio
        session.run("""
        MATCH (u:User {email: 'marie@etudiant.com'})
        MATCH (p:Project {titre: 'Plateforme E-commerce Bio'})
        WITH u, p LIMIT 1
        MERGE (u)-[r:APPLIED_TO]->(p)
        SET r.status = 'PENDING', 
            r.date = datetime() - duration('P5D'),
            r.motivation_message = "Je maîtrise React et Node.js, je serais ravie d'aider."
        """)
        
        # 3. Rejected - Application Mobile Fitness
        session.run("""
        MATCH (u:User {email: 'marie@etudiant.com'})
        MATCH (p:Project {titre: 'Application Mobile Fitness'})
        WITH u, p LIMIT 1
        MERGE (u)-[r:APPLIED_TO]->(p)
        SET r.status = 'REJECTED', 
            r.date = datetime() - duration('P10D'),
            r.motivation_message = "Le sport c'est ma passion !"
        """)
        
        print("✅ Clean injection complete!")

if __name__ == "__main__":
    clean_duplicates()
