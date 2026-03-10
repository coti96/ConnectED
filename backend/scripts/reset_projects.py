import sys
import os
from datetime import datetime, timedelta

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import db

def clean_and_inject_projects():
    print("🧹 Cleaning all projects and re-injecting fresh data...")
    
    driver = db.get_db()
    with driver.session() as session:
        # 1. Delete ALL projects and related relationships
        session.run("MATCH (p:Project) DETACH DELETE p")
        print("✅ All existing projects deleted.")
        
        # 2. Define fresh projects with ALL properties
        projects = [
            {
                'titre': 'Plateforme IA Santé',
                'description': "Développement d'une IA pour le diagnostic médical assisté à partir d'imagerie.",
                'domaine': 'Santé',
                'statut': 'en_cours',
                'nombre_places': 3,
                'techs': ['Python', 'TensorFlow', 'OpenCV']
            },
            {
                'titre': 'App Mobile Écologie',
                'description': "Application mobile pour suivre et réduire son empreinte carbone au quotidien.",
                'domaine': 'Environnement',
                'statut': 'en_cours',
                'nombre_places': 2,
                'techs': ['React Native', 'Node.js', 'MongoDB']
            },
            {
                'titre': 'Marketplace Bio Locale',
                'description': "Plateforme de mise en relation entre producteurs bio locaux et consommateurs.",
                'domaine': 'Web Development',
                'statut': 'en_cours',
                'nombre_places': 4,
                'techs': ['Vue.js', 'Express', 'PostgreSQL']
            },
            {
                'titre': 'Jeu Vidéo VR Histoire',
                'description': "Expérience immersive en réalité virtuelle pour apprendre l'histoire de France.",
                'domaine': 'Réalité Virtuelle',
                'statut': 'en_cours',
                'nombre_places': 2,
                'techs': ['Unity', 'C#', 'Blender']
            },
            {
                'titre': 'Vote Sécurisé Blockchain',
                'description': "Système de vote électronique décentralisé et transparent.",
                'domaine': 'Blockchain',
                'statut': 'en_cours',
                'nombre_places': 3,
                'techs': ['Solidity', 'Ethereum', 'Web3.js']
            }
        ]
        
        # 3. Create projects
        print("🔹 Creating fresh projects...")
        for p in projects:
            session.run("""
            MATCH (u:User {email: 'jean@createur.com'})
            CREATE (proj:Project {
                titre: $titre,
                description: $desc,
                domaine: $domaine,
                statut: $statut,
                nombre_places: $places,
                created_at: datetime(),
                deadline: datetime() + duration('P60D')
            })
            MERGE (u)-[:CREATED_BY]->(proj)
            
            FOREACH (t_name IN $techs | 
                MERGE (t:Technology {libelle: t_name})
                MERGE (proj)-[:REQUIRES_TECH]->(t)
            )
            """, 
            titre=p['titre'], 
            desc=p['description'], 
            domaine=p['domaine'],
            statut=p['statut'],
            places=p['nombre_places'],
            techs=p['techs']
            )
            
        print("✅ Projects injected successfully!")

if __name__ == "__main__":
    clean_and_inject_projects()
