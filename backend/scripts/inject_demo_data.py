import sys
import os
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import db

def inject_data():
    driver = db.get_db()
    with driver.session() as session:
        print("🚀 Starting data injection...")

        # 1. Setup Users (Ensure they exist and have correct roles)
        # Marie (Student)
        session.run("""
        MERGE (u:User {email: 'marie@etudiant.com'})
        SET u.nom = 'Dupont', u.prenom = 'Marie', u.role = 'etudiant', 
            u.password_hash = '$2b$12$FDJaarTh9m1TayILD281.OnOGLWqxlR/vJaKEGSlFXTWY8y1dKX32'
        """)
        
        # Jean (Creator)
        session.run("""
        MERGE (u:User {email: 'jean@createur.com'})
        SET u.nom = 'Martin', u.prenom = 'Jean', u.role = 'creator',
            u.password_hash = '$2b$12$FDJaarTh9m1TayILD281.OnOGLWqxlR/vJaKEGSlFXTWY8y1dKX32'
        """)

        # 2. Add Technologies to Marie (for recommendations)
        print("🔹 Adding technologies to Marie...")
        techs = ['Python', 'React', 'Data Science', 'Machine Learning']
        for tech in techs:
            session.run("""
            MATCH (u:User {email: 'marie@etudiant.com'})
            MERGE (t:Technology {libelle: $tech})
            MERGE (u)-[:HAS_TECH]->(t)
            """, tech=tech)

        # 3. Create Projects for Jean
        print("🔹 Creating projects for Jean...")
        projects = [
            {
                'titre': 'Plateforme IA Santé',
                'description': 'Développement d\'une IA pour le diagnostic médical assisté.',
                'domaine': 'Santé',
                'techs': ['Python', 'Machine Learning', 'TensorFlow']
            },
            {
                'titre': 'App Mobile Écologie',
                'description': 'Application pour suivre son empreinte carbone au quotidien.',
                'domaine': 'Environnement',
                'techs': ['React Native', 'Node.js', 'MongoDB']
            }
        ]
        
        for p in projects:
            session.run("""
            MATCH (u:User {email: 'jean@createur.com'})
            MERGE (proj:Project {titre: $titre})
            SET proj.description = $desc, 
                proj.statut = 'en_cours',
                proj.created_at = datetime(),
                proj.nombre_places = 3,
                proj.deadline = datetime() + duration('P30D')
            
            MERGE (u)-[:CREATED_BY]->(proj)
            
            FOREACH (t_name IN $techs | 
                MERGE (t:Technology {libelle: t_name})
                MERGE (proj)-[:REQUIRES_TECH]->(t)
            )
            """, titre=p['titre'], desc=p['description'], techs=p['techs'])

        # 4. Create Applications for Marie
        print("🔹 Creating applications for Marie...")
        
        # S'assurer que les projets existent d'abord (au cas où les données CSV ne sont pas là)
        projects_to_ensure = [
            {'title': 'Analyse de données IA', 'desc': 'Projet de Data Science pour analyser des tendances.'},
            {'title': 'Plateforme E-commerce Bio', 'desc': 'Site web de vente de produits bio locaux.'},
            {'title': 'Application Mobile Fitness', 'desc': 'App mobile pour suivre ses performances sportives.'}
        ]
        
        for p in projects_to_ensure:
            session.run("""
            MERGE (p:Project {titre: $title})
            ON CREATE SET p.description = $desc, p.created_at = datetime()
            """, title=p['title'], desc=p['desc'])

        # App 1: Accepted (Analyse de données IA)
        session.run("""
        MATCH (u:User {email: 'marie@etudiant.com'})
        MATCH (p:Project {titre: 'Analyse de données IA'})
        MERGE (u)-[r:APPLIED_TO]->(p)
        SET r.status = 'ACCEPTED', 
            r.date = datetime() - duration('P2D'),
            r.motivation_message = "J'ai hâte de commencer ce projet data !"
        """)
        
        # App 2: Pending (Plateforme E-commerce Bio)
        session.run("""
        MATCH (u:User {email: 'marie@etudiant.com'})
        MATCH (p:Project {titre: 'Plateforme E-commerce Bio'})
        MERGE (u)-[r:APPLIED_TO]->(p)
        SET r.status = 'PENDING', 
            r.date = datetime() - duration('P5D'),
            r.motivation_message = "Je maîtrise React et Node.js, je serais ravie d'aider."
        """)
        
        # App 3: Rejected (Application Mobile Fitness)
        session.run("""
        MATCH (u:User {email: 'marie@etudiant.com'})
        MATCH (p:Project {titre: 'Application Mobile Fitness'})
        MERGE (u)-[r:APPLIED_TO]->(p)
        SET r.status = 'REJECTED', 
            r.date = datetime() - duration('P10D'),
            r.motivation_message = "Le sport c'est ma passion !"
        """)

        # 5. Create Messages
        print("🔹 Creating messages...")
        # Jean -> Marie
        session.run("""
        MATCH (sender:User {email: 'jean@createur.com'})
        MATCH (receiver:User {email: 'marie@etudiant.com'})
        CREATE (sender)-[:SENT]->(m:Message {
            content: "Bonjour Marie, votre profil m'intéresse pour le projet IA.",
            timestamp: datetime() - duration('P1D')
        })-[:TO]->(receiver)
        """)
        
        # Marie -> Jean
        session.run("""
        MATCH (sender:User {email: 'marie@etudiant.com'})
        MATCH (receiver:User {email: 'jean@createur.com'})
        CREATE (sender)-[:SENT]->(m:Message {
            content: "Merci Jean ! Je suis disponible pour en discuter.",
            timestamp: datetime() - duration('PT2H')
        })-[:TO]->(receiver)
        """)

        print("✅ Data injection complete!")

if __name__ == "__main__":
    try:
        inject_data()
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        db.close()
