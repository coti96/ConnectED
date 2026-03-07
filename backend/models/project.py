from database import db
from datetime import datetime

class ProjectModel:
    @staticmethod
    def get_all():
        driver = db.get_db()
        with driver.session() as session:
            query = """
            MATCH (p:Project)
            OPTIONAL MATCH (p)<-[:CREATED_BY]-(u:User)
            OPTIONAL MATCH (p)-[:REQUIRES_TECH]->(t:Technology)
            RETURN p, u, collect(t.libelle) as technologies
            """
            result = session.run(query)
            
            projects = []
            for record in result:
                project_data = dict(record["p"].items())
                project_data['id'] = record["p"].element_id
                project_data['technologies'] = record["technologies"]
                
                if record["u"]:
                    project_data['creator'] = {
                        'nom': record["u"].get('nom'),
                        'prenom': record["u"].get('prenom'),
                        'email': record["u"].get('email')
                    }
                projects.append(project_data)
            return projects

    @staticmethod
    def create(data, email):
        driver = db.get_db()
        with driver.session() as session:
            query = """
            MATCH (u:User {email: $email})
            CREATE (p:Project {
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
            project_id = result.single()['p'].element_id
            
            # Add technologies
            if 'technologies' in data and isinstance(data['technologies'], list):
                for tech in data['technologies']:
                    session.run("""
                    MATCH (p:Project) WHERE elementId(p) = $pid
                    MERGE (t:Technology {libelle: $tech})
                    MERGE (p)-[:REQUIRES_TECH]->(t)
                    """, pid=project_id, tech=tech)
            
            return project_id

    @staticmethod
    def get_recommended(email):
        driver = db.get_db()
        with driver.session() as session:
            query = """
            MATCH (u:User {email: $email})
            MATCH (u)-[:HAS_TECH]->(t:Technology)<-[:REQUIRES_TECH]-(p:Project)
            WHERE NOT (u)-[:CREATED_BY]->(p) AND p.statut = 'en_cours'
            
            WITH p, collect(t.libelle) as common_techs, count(t) as score
            OPTIONAL MATCH (p)-[:REQUIRES_TECH]->(all_t:Technology)
            WITH p, common_techs, score, collect(all_t.libelle) as all_techs
            OPTIONAL MATCH (p)<-[:CREATED_BY]-(creator:User)
            
            RETURN p, score, common_techs, all_techs, creator
            ORDER BY score DESC LIMIT 10
            """
            
            result = session.run(query, email=email)
            recommendations = []
            
            for record in result:
                data = dict(record["p"].items())
                data['id'] = record["p"].element_id
                data['match_score'] = record["score"]
                data['common_technologies'] = record["common_techs"]
                data['technologies'] = record["all_techs"]
                
                if record["creator"]:
                    data['creator'] = {
                        'nom': record["creator"].get('nom'),
                        'prenom': record["creator"].get('prenom')
                    }
                recommendations.append(data)
            return recommendations
