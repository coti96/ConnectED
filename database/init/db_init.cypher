// ============================================================================
// 1️⃣ CONTRAINTES (UNIQUE)
// ============================================================================
CREATE CONSTRAINT user_email_unique IF NOT EXISTS FOR (u:User) REQUIRE u.email IS UNIQUE;
CREATE CONSTRAINT project_id_unique IF NOT EXISTS FOR (p:Project) REQUIRE p.project_id IS UNIQUE;
CREATE CONSTRAINT tech_libelle_unique IF NOT EXISTS FOR (t:Technology) REQUIRE t.libelle IS UNIQUE;
CREATE CONSTRAINT domain_libelle_unique IF NOT EXISTS FOR (d:Domain) REQUIRE d.libelle IS UNIQUE;

// ============================================================================
// 2️⃣ DOMAINES
// ============================================================================
CALL {
    LOAD CSV WITH HEADERS FROM 'file:///domains.csv' AS row
    CREATE (:Domain {libelle: row.libelle, created_at: datetime()})
} IN TRANSACTIONS;

// ============================================================================
// 3️⃣ TECHNOLOGIES
// ============================================================================
CALL {
    LOAD CSV WITH HEADERS FROM 'file:///technologies.csv' AS row
    MATCH (d:Domain {libelle: row.domain_libelle})
    CREATE (t:Technology {libelle: row.libelle, created_at: datetime()})
    MERGE (t)-[:IN_DOMAIN]->(d)
} IN TRANSACTIONS;

// ============================================================================
// 4️⃣ UTILISATEURS
// ============================================================================
CALL {
    LOAD CSV WITH HEADERS FROM 'file:///users.csv' AS row
    CREATE (:User {
        email: row.email,
        password_hash: row.password_hash,
        role: row.role,
        nom: row.nom,
        prenom: row.prenom,
        ville: row.ville,
        bio_courte: row.bio_courte,
        ecole: row.ecole,
        filiere: row.filiere,
        fonction: row.fonction,
        entreprise: row.entreprise,
        created_at: datetime(row.created_at)
    })
} IN TRANSACTIONS;

// ============================================================================
// 5️⃣ RELATIONS UTILISATEURS ↔ TECHNOLOGIES
// ============================================================================
CALL {
    LOAD CSV WITH HEADERS FROM 'file:///relations_user_tech.csv' AS row
    MATCH (u:User {email: row.user_email})
    MATCH (t:Technology {libelle: row.tech_libelle})
    MERGE (u)-[:HAS_TECH]->(t)
} IN TRANSACTIONS;

// ============================================================================
// 6️⃣ PROJETS
// ============================================================================
CALL {
    LOAD CSV WITH HEADERS FROM 'file:///projects.csv' AS row
    CREATE (:Project {
        project_id: toInteger(row.project_id),
        titre: row.titre,
        description: row.description,
        localisation: row.localisation,
        statut: row.statut,
        nombre_places: toInteger(row.nombre_places),
        created_at: datetime()
    })
} IN TRANSACTIONS;

// ============================================================================
// 7️⃣ RELATIONS PROJETS ↔ TECHNOLOGIES
// ============================================================================
CALL {
    LOAD CSV WITH HEADERS FROM 'file:///relations_project_tech.csv' AS row
    MATCH (p:Project {project_id: toInteger(row.project_id)})
    MATCH (t:Technology {libelle: row.tech_libelle})
    MERGE (p)-[:REQUIRES_TECH]->(t)
} IN TRANSACTIONS;

// ============================================================================
// 8️⃣ RELATIONS UTILISATEURS ↔ PROJETS (APPLICATIONS)
// ============================================================================
CALL {
    LOAD CSV WITH HEADERS FROM 'file:///relations_user_project_applied.csv' AS row
    MATCH (u:User {email: row.user_email})
    MATCH (p:Project {project_id: toInteger(row.project_id)})
    MERGE (u)-[r:APPLIED_TO]->(p)
    SET r.status = row.status,
        r.motivation_message = row.motivation_message,
        r.created_at = datetime(row.created_at)
} IN TRANSACTIONS;

// ============================================================================
// 9️⃣ RELATIONS UTILISATEURS ↔ PROJETS (MEMBRES ACCEPTÉS)
// ============================================================================
CALL {
    LOAD CSV WITH HEADERS FROM 'file:///relations_user_project_member.csv' AS row
    MATCH (u:User {email: row.user_email})
    MATCH (p:Project {project_id: toInteger(row.project_id)})
    MERGE (u)-[r:MEMBER_OF]->(p)
    SET r.joined_at = datetime(row.joined_at)
} IN TRANSACTIONS;

