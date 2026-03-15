from database import db
from datetime import datetime
from neo4j.graph import Node
import logging

class ProjectModel:
    @staticmethod
    def _project_id(node: Node):
        if not node:
            return None
        pid = node.get("id")
        if pid:
            return pid
        return getattr(node, "element_id", None)

    @staticmethod
    def get_all():
        driver = db.get_db()
        with driver.session() as session:
            query = """
            MATCH (p:Project)
            OPTIONAL MATCH (p)<-[:CREATED_BY]-(u:User)
            OPTIONAL MATCH (p)-[:REQUIRES_TECH]->(t:Technology)
            OPTIONAL MATCH ()-[a:APPLIED_TO {status: 'ACCEPTED'}]->(p)
            RETURN p, u, collect(DISTINCT t.libelle) as technologies, count(DISTINCT a) as accepted_count
            """
            result = session.run(query)
            
            projects = []
            for record in result:
                project_data = dict(record["p"].items())
                # Conversion des dates Neo4j en string
                for key, value in project_data.items():
                    if hasattr(value, 'iso_format'):
                        project_data[key] = value.iso_format()
                        
                project_data['id'] = ProjectModel._project_id(record["p"])
                project_data['technologies'] = record["technologies"]
                project_data['accepted_count'] = record.get("accepted_count", 0)
                
                if record["u"]:
                    project_data['creator'] = {
                        'nom': record["u"].get('nom'),
                        'prenom': record["u"].get('prenom'),
                        'email': record["u"].get('email')
                    }
                projects.append(project_data)
            return projects

    @staticmethod
    def get_by_id(project_id):
        driver = db.get_db()
        with driver.session() as session:
            query = """
            MATCH (p:Project)
            WHERE p.id = $project_id OR elementId(p) = $project_id
            OPTIONAL MATCH (p)<-[:CREATED_BY]-(u:User)
            OPTIONAL MATCH (p)-[:REQUIRES_TECH]->(t:Technology)
            OPTIONAL MATCH ()-[a:APPLIED_TO {status: 'ACCEPTED'}]->(p)
            OPTIONAL MATCH (m:User)-[:MEMBER_OF]->(p)
            RETURN p, u, collect(DISTINCT t.libelle) as technologies, count(DISTINCT a) as accepted_count,
                   collect(DISTINCT {email: m.email, nom: m.nom, prenom: m.prenom}) as members
            """
            result = session.run(query, project_id=project_id)
            record = result.single()
            
            if not record:
                return None
                
            project_data = dict(record["p"].items())
            # Conversion des dates Neo4j en string
            for key, value in project_data.items():
                if hasattr(value, 'iso_format'):
                    project_data[key] = value.iso_format()

            project_data['id'] = ProjectModel._project_id(record["p"])
            project_data['technologies'] = record["technologies"]
            project_data['accepted_count'] = record.get("accepted_count", 0)
            project_data['members'] = record.get("members") or []
            
            if record["u"]:
                project_data['creator'] = {
                    'nom': record["u"].get('nom'),
                    'prenom': record["u"].get('prenom'),
                    'email': record["u"].get('email')
                }
            return project_data

    @staticmethod
    def create(data, email):
        # ... (reste du code inchangé, mais on doit tout réécrire car Write écrase le fichier)
        driver = db.get_db()
        with driver.session() as session:
            query = """
            MATCH (u:User {email: $email})
            CREATE (p:Project {
                id: randomUUID(),
                titre: $titre,
                description: $description,
                statut: 'en_cours',
                nombre_places: $nombre_places,
                deadline: datetime($deadline),
                created_at: datetime()
            })
            MERGE (u)-[:CREATED_BY]->(p)
            WITH p
            MERGE (d:Domain {libelle: $domaine})
            MERGE (p)-[:IN_DOMAIN]->(d)
            RETURN p
            """
            
            params = {
                'email': email,
                'titre': data['titre'],
                'description': data['description'],
                'domaine': data['domaine'],
                'nombre_places': int(data.get('nombre_places', 1)),
                'deadline': data['deadline']
            }
            
            result = session.run(query, **params)
            record = result.single()
            if not record:
                return None
            project_id = record["p"].get('id')
            
            # Add technologies
            if 'technologies' in data and isinstance(data['technologies'], list):
                for tech in data['technologies']:
                    session.run("""
                    MATCH (p:Project {id: $pid})
                    MERGE (t:Technology {libelle: $tech})
                    MERGE (p)-[:REQUIRES_TECH]->(t)
                    """, pid=project_id, tech=tech)
            
            return project_id

    @staticmethod
    def set_status(project_id, status):
        driver = db.get_db()
        with driver.session() as session:
            query = """
            MATCH (p:Project)
            WHERE p.id = $project_id OR elementId(p) = $project_id
            SET p.statut = $status
            RETURN p
            """
            record = session.run(query, project_id=project_id, status=status).single()
            return record is not None

    @staticmethod
    def get_recommended(email):
        driver = db.get_db()
        with driver.session() as session:
            # 1. On cherche d'abord des correspondances directes (via technologies)
            query = """
            MATCH (u:User {email: $email})
            MATCH (u)-[:HAS_TECH]->(t:Technology)<-[:REQUIRES_TECH]-(p:Project)
            WHERE NOT (u)-[:CREATED_BY]->(p) 
              AND (p.statut = 'en_cours' OR p.statut IS NULL)
            
            WITH p, collect(DISTINCT t.libelle) as common_techs, count(DISTINCT t) as score
            
            OPTIONAL MATCH (p)-[:REQUIRES_TECH]->(all_t:Technology)
            WITH p, common_techs, score, collect(DISTINCT all_t.libelle) as all_techs
            
            OPTIONAL MATCH (p)<-[:CREATED_BY]-(creator:User)
            OPTIONAL MATCH ()-[a:APPLIED_TO {status: 'ACCEPTED'}]->(p)
            
            RETURN p, score, common_techs, all_techs, creator, count(DISTINCT a) as accepted_count
            ORDER BY score DESC LIMIT 10
            """
            
            result = session.run(query, email=email)
            recommendations = []
            
            for record in result:
                data = dict(record["p"].items())
                # Conversion des dates
                for key, value in data.items():
                    if hasattr(value, 'iso_format'):
                        data[key] = value.iso_format()

                data['id'] = ProjectModel._project_id(record["p"])
                data['match_score'] = record["score"]
                data['common_technologies'] = record["common_techs"]
                data['technologies'] = record["all_techs"]
                data['accepted_count'] = record.get("accepted_count", 0)
                
                if record["creator"]:
                    data['creator'] = {
                        'nom': record["creator"].get('nom'),
                        'prenom': record["creator"].get('prenom')
                    }
                recommendations.append(data)
                
            # 2. Si aucune recommandation par techno, on renvoie les projets récents par défaut
            if not recommendations:
                logging.info("Aucune recommandation par techno pour %s, fallback sur projets récents", email)
                fallback_query = """
                MATCH (p:Project)
                WHERE (p.statut = 'en_cours' OR p.statut IS NULL)
                OPTIONAL MATCH (p)-[:REQUIRES_TECH]->(t:Technology)
                OPTIONAL MATCH (p)<-[:CREATED_BY]-(creator:User)
                OPTIONAL MATCH ()-[a:APPLIED_TO {status: 'ACCEPTED'}]->(p)
                RETURN p, collect(DISTINCT t.libelle) as all_techs, creator, count(DISTINCT a) as accepted_count
                ORDER BY p.created_at DESC LIMIT 5
                """
                result = session.run(fallback_query)
                for record in result:
                    data = dict(record["p"].items())
                    for key, value in data.items():
                        if hasattr(value, 'iso_format'):
                            data[key] = value.iso_format()
                            
                    data['id'] = ProjectModel._project_id(record["p"])
                    data['match_score'] = 0 # Pas de match spécifique
                    data['common_technologies'] = []
                    data['technologies'] = record["all_techs"]
                    data['accepted_count'] = record.get("accepted_count", 0)
                    
                    if record["creator"]:
                        data['creator'] = {
                            'nom': record["creator"].get('nom'),
                            'prenom': record["creator"].get('prenom')
                        }
                    recommendations.append(data)

            return recommendations
