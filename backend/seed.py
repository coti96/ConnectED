from app import app
from database import db
from models.user import UserModel
from models.project import ProjectModel
from models.message import MessageModel
from models.application import ApplicationModel
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

def run_seed():
    print("🌱 Starting Database Seeding...")
    
    # 1. Nettoyer la base (Optionnel, pour éviter les doublons lors des tests répétés)
    # db.get_db().session().run("MATCH (n) DETACH DELETE n") 
    # print("🧹 Database cleared!")

    # 2. Créer des utilisateurs
    users = [
        # --- CRÉATEURS ---
        {
            "email": "jean@createur.com", "password": "password123", 
            "nom": "Dupont", "prenom": "Jean", "role": "creator",
            "bio": "Entrepreneur passionné par la Tech et l'écologie.",
            "technologies": ["Business", "Marketing", "GreenTech"]
        },
        {
            "email": "sarah@createur.com", "password": "password123",
            "nom": "Connor", "prenom": "Sarah", "role": "creator",
            "bio": "Chercheuse en IA, focus sur la sécurité et l'éthique.",
            "technologies": ["AI", "Robotics", "C++", "Python"]
        },
        {
            "email": "thomas@createur.com", "password": "password123",
            "nom": "Anderson", "prenom": "Thomas", "role": "creator",
            "bio": "Architecte logiciel, passionné par la réalité virtuelle.",
            "technologies": ["Unity", "C#", "VR", "Blockchain"]
        },
        # --- ÉTUDIANTS ---
        {
            "email": "marie@etudiant.com", "password": "password123",
            "nom": "Curie", "prenom": "Marie", "role": "student",
            "bio": "Étudiante en Data Science, adore Python et le Machine Learning.",
            "technologies": ["Python", "Pandas", "Scikit-Learn", "SQL"]
        },
        {
            "email": "paul@etudiant.com", "password": "password123",
            "nom": "Atreides", "prenom": "Paul", "role": "student",
            "bio": "Développeur Web Fullstack, spécialiste Angular/Java.",
            "technologies": ["Angular", "Java", "Spring Boot", "Docker"]
        },
        {
            "email": "lucie@etudiant.com", "password": "password123",
            "nom": "Skywalker", "prenom": "Lucie", "role": "student",
            "bio": "Designer UX/UI qui code un peu. Fan de React.",
            "technologies": ["Figma", "React", "CSS", "TypeScript"]
        }
    ]

    print(f"👤 Creating {len(users)} users...")
    for u in users:
        # On hash le mot de passe ici pour être sûr
        pw_hash = bcrypt.generate_password_hash(u['password']).decode('utf-8')
        
        # Vérifions si l'user existe
        existing = UserModel.find_by_email(u['email'])
        if not existing:
            # UserModel.create attend : email, password_hash, nom, prenom, role
            UserModel.create(u['email'], pw_hash, u['nom'], u['prenom'], u['role'])
            
            # Mettre à jour le profil avec bio et technos
            UserModel.update_profile(u['email'], {
                "bio_courte": u['bio'],
                "ecole": "ESIEE Paris" if u['role'] == 'student' else "Tech Corp",
                "ville": "Paris"
            }, u['technologies'])
            
            print(f"   ✅ Created: {u['email']}")
        else:
            print(f"   ⚠️ Skipped: {u['email']} (already exists)")

    # 3. Créer des projets
    projects = [
        {
            "titre": "Eco-Marketplace Bio",
            "description": "Plateforme de vente directe pour producteurs locaux bio. Nous cherchons un dev Back et un Marketing.",
            "technologies": ["React", "Node.js", "MongoDB", "Marketing"],
            "creator_email": "jean@createur.com",
            "domaine": "Web Development",
            "nombre_places": 3,
            "deadline": "2026-12-31"
        },
        {
            "titre": "App Mobile Fitness Coach",
            "description": "Application iOS/Android de coaching sportif avec suivi nutritionnel.",
            "technologies": ["Flutter", "Firebase", "UX Design"],
            "creator_email": "jean@createur.com",
            "domaine": "Mobile App",
            "nombre_places": 2,
            "deadline": "2026-09-30"
        },
        {
            "titre": "IA Détection de Fraude",
            "description": "Système de détection d'anomalies bancaires en temps réel utilisant le Deep Learning.",
            "technologies": ["Python", "TensorFlow", "Big Data", "Security"],
            "creator_email": "sarah@createur.com",
            "domaine": "Artificial Intelligence",
            "nombre_places": 4,
            "deadline": "2027-01-01"
        },
        {
            "titre": "Metaverse Éducatif",
            "description": "Environnement VR pour apprendre l'histoire en immersion.",
            "technologies": ["Unity", "C#", "VR", "3D Modeling"],
            "creator_email": "thomas@createur.com",
            "domaine": "Virtual Reality",
            "nombre_places": 5,
            "deadline": "2027-06-30"
        },
        {
            "titre": "Plateforme de Vote Blockchain",
            "description": "Système de vote décentralisé et transparent pour les associations.",
            "technologies": ["Blockchain", "Solidity", "Web3", "React"],
            "creator_email": "thomas@createur.com",
            "domaine": "Blockchain",
            "nombre_places": 3,
            "deadline": "2026-11-30"
        }
    ]

    print(f"🚀 Creating {len(projects)} projects...")
    created_projects = []
    for p in projects:
        # Vérifier si le projet existe déjà (pour éviter doublons si on relance)
        # Ici on simplifie en créant toujours (ou on pourrait vérifier par titre)
        proj_id = ProjectModel.create(p, p['creator_email'])
        if proj_id:
            created_projects.append({"id": proj_id, "title": p['titre'], "creator": p['creator_email']})
            print(f"   ✅ Created Project: {p['titre']} by {p['creator_email']}")

    # 4. Simuler des interactions (Candidatures & Messages)
    print("🤝 Simulating interactions...")
    
    # Marie (Python/Data) postule au projet IA de Sarah
    ia_project = next((p for p in created_projects if "IA" in p['title']), None)
    if ia_project:
        # Note: ApplicationModel.create ne prend pas de message pour l'instant
        ApplicationModel.create(ia_project['id'], "marie@etudiant.com")
        print(f"   📩 Marie applied to '{ia_project['title']}'")
        
        # Sarah envoie un message à Marie
        MessageModel.create("sarah@createur.com", "marie@etudiant.com", "Salut Marie, ton profil m'intéresse. On peut discuter ?")
        print("   💬 Sarah messaged Marie")

    # Paul (Java/Angular) postule mais... pas de projet Java ici (c'est fait exprès pour tester)
    # Il va quand même envoyer un message à Jean
    MessageModel.create("paul@etudiant.com", "jean@createur.com", "Bonjour Jean, faites-vous du Java ?")
    print("   💬 Paul messaged Jean")

    print("\n✅ SEEDING COMPLETE! You can now login with:")
    print("   - marie@etudiant.com / password123 (Student)")
    print("   - paul@etudiant.com / password123 (Student)")
    print("   - jean@createur.com / password123 (Creator)")
    print("   - sarah@createur.com / password123 (Creator)")

if __name__ == "__main__":
    with app.app_context():
        run_seed()
