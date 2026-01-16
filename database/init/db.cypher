// ============================================================================
// 1. SCHÉMA & INTÉGRITÉ (L'équivalent de PRIMARY KEY et UNIQUE INDEX)
// ============================================================================

// Garantit que deux utilisateurs ne peuvent pas avoir le même email
CREATE CONSTRAINT user_email_unique IF NOT EXISTS FOR (u:User) REQUIRE u.email IS UNIQUE;

// Garantit l'unicité des IDs métiers
CREATE CONSTRAINT project_id_unique IF NOT EXISTS FOR (p:Project) REQUIRE p.project_id IS UNIQUE;
CREATE CONSTRAINT tech_libelle_unique IF NOT EXISTS FOR (t:Technology) REQUIRE t.libelle IS UNIQUE;
CREATE CONSTRAINT domain_libelle_unique IF NOT EXISTS FOR (d:Domain) REQUIRE d.libelle IS UNIQUE;


// ============================================================================
// 2. DONNÉES DE RÉFÉRENCE (Tables 'domains' et 'technologies')
// ============================================================================

// Création des Domaines (Table 'domains')
MERGE (web:Domain {libelle: 'Développement Web'}) SET web.created_at = datetime();
MERGE (data:Domain {libelle: 'Data Science'}) SET data.created_at = datetime();
MERGE (design:Domain {libelle: 'Design UI/UX'}) SET design.created_at = datetime();

// Création des Technologies (Table 'technologies' + Foreign Key 'domain_id')
// En graphe, la FK devient une relation directe [:IN_DOMAIN]
MERGE (js:Technology {libelle: 'JavaScript'})-[:IN_DOMAIN]->(web);
MERGE (react:Technology {libelle: 'React'})-[:IN_DOMAIN]->(web);
MERGE (node:Technology {libelle: 'Node.js'})-[:IN_DOMAIN]->(web);
MERGE (py:Technology {libelle: 'Python'})-[:IN_DOMAIN]->(data);
MERGE (tf:Technology {libelle: 'TensorFlow'})-[:IN_DOMAIN]->(data);
MERGE (figma:Technology {libelle: 'Figma'})-[:IN_DOMAIN]->(design);


// ============================================================================
// 3. UTILISATEURS (Fusion des tables 'users', 'profiles', 'profiles_student/pro')
// ============================================================================

// --- Un Étudiant ---
// Note : On utilise deux labels (:User et :Student) pour filtrer facilement
CREATE (alice:User:Student {
    email: 'alice@student.com',
    password_hash: '$2b$10$xyz...', // Hash simulé
    role: 'etudiant',
    nom: 'Durand',
    prenom: 'Alice',
    ville: 'Lyon',
    bio_courte: 'Étudiante passionnée par le front-end.',
    ecole: 'Epitech',
    filiere: 'Web Development',
    created_at: datetime()
})
WITH alice
MATCH (web:Domain {libelle: 'Développement Web'})
MATCH (react:Technology {libelle: 'React'})
MERGE (alice)-[:INTERESTED_IN]->(web)
MERGE (alice)-[:HAS_TECH]->(react)

// --- Un Professionnel ---
WITH alice
CREATE (bob:User:Pro {
    email: 'bob@company.com',
    password_hash: '$2b$10$abc...',
    role: 'professionnel',
    nom: 'Martin',
    prenom: 'Bob',
    ville: 'Paris',
    fonction: 'Lead Developer',
    entreprise: 'TechCorp',
    created_at: datetime()
})
WITH alice, bob
MATCH (data:Domain {libelle: 'Data Science'})
MATCH (py:Technology {libelle: 'Python'})
MERGE (bob)-[:INTERESTED_IN]->(data)
MERGE (bob)-[:HAS_TECH]->(py)


// ============================================================================
// 4. PROJETS (Table 'projects' + Relations créateur et technos)
// ============================================================================

WITH alice, bob
CREATE (proj:Project {
    project_id: 101,
    titre: 'Analyse de données IA',
    description: 'Plateforme de détection de fraude basée sur le comportement.',
    localisation: 'Hybride',
    statut: 'en_cours',
    nombre_places: 3,
    deadline: datetime('2026-06-01T23:59:59'),
    created_at: datetime()
})
WITH alice, bob, proj
MATCH (data:Domain {libelle: 'Intelligence Artificielle'})
MATCH (py:Technology {libelle: 'Python'})
MERGE (bob)-[:CREATOR_OF]->(proj)      // Remplace 'creator_id'
MERGE (proj)-[:IN_DOMAIN]->(data)      // Remplace 'domain_id'
MERGE (proj)-[:REQUIRES_TECH]->(py)    // Remplace la table 'project_techno'


// ============================================================================
// 5. INTERACTION & WORKFLOW (Tables 'project_applications' et 'project_members')
// ============================================================================

// --- Alice postule au projet de Bob ---
WITH alice, bob, proj
MERGE (alice)-[app:APPLIED_TO]->(proj)
SET app.status = 'en_attente',
    app.motivation_message = 'Je maîtrise React et j’aimerais apprendre Python sur ce projet.',
    app.created_at = datetime()

// --- Ajout d'un membre déjà accepté (Lucas) ---
// Note : On ajoute bob et proj dans le WITH pour qu'ils soient encore connus après
WITH bob, proj 
CREATE (lucas:User:Student {
    email: 'lucas@ecole.fr',
    nom: 'Lefebvre',
    prenom: 'Lucas',
    role: 'etudiant',
    ecole: 'Insa'
})
MERGE (lucas)-[:MEMBER_OF {joined_at: datetime()}]->(proj)

// ============================================================================
// 6. NOTIFICATIONS (Table 'notifications')
// ============================================================================

// Maintenant "bob" et "proj" sont bien définis ici grâce au WITH précédent
WITH bob, proj
CREATE (n:Notification {
    notification_id: 500,
    message: 'Nouvelle candidature reçue pour votre projet IA',
    date_sent: datetime(),
    read: false
})
MERGE (n)-[:FOR_USER]->(bob)
MERGE (n)-[:ABOUT_PROJECT]->(proj);