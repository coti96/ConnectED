from database import db
from datetime import datetime

class ApplicationModel:
    @staticmethod
    def create(user_email, project_id):
        driver = db.get_db()
        with driver.session() as session:
            # Vérifier si déjà candidat
            check_query = """
            MATCH (u:User {email: $email})-[r:APPLIED_TO]->(p:Project)
            WHERE elementId(p) = $project_id
            RETURN r
            """
            existing = session.run(check_query, email=user_email, project_id=project_id).single()
            if existing:
                return None, "Vous avez déjà postulé à ce projet."

            # Créer la candidature
            query = """
            MATCH (u:User {email: $email})
            MATCH (p:Project) WHERE elementId(p) = $project_id
            CREATE (u)-[r:APPLIED_TO {
                date: datetime(),
                status: 'PENDING'
            }]->(p)
            RETURN r
            """
            session.run(query, email=user_email, project_id=project_id)
            return True, None

    @staticmethod
    def get_by_project(project_id):
        driver = db.get_db()
        with driver.session() as session:
            query = """
            MATCH (u:User)-[r:APPLIED_TO]->(p:Project)
            WHERE elementId(p) = $project_id
            RETURN u, r, p
            """
            result = session.run(query, project_id=project_id)
            
            applications = []
            for record in result:
                user = dict(record['u'].items())
                app_data = dict(record['r'].items())
                
                # Nettoyage
                if 'password_hash' in user: del user['password_hash']
                if 'date' in app_data: app_data['date'] = str(app_data['date'])
                
                applications.append({
                    'applicant': user,
                    'status': app_data.get('status', 'PENDING'),
                    'date': app_data.get('date'),
                    'application_id': record['r'].element_id
                })
            return applications

    @staticmethod
    def get_my_applications(email):
        driver = db.get_db()
        with driver.session() as session:
            # Récupération plus robuste des propriétés
            query = """
            MATCH (u:User {email: $email})-[r:APPLIED_TO]->(p:Project)
            RETURN p, r
            """
            result = session.run(query, email=email)
            
            my_apps = []
            for record in result:
                # Convertir le noeud Project en dictionnaire
                project_node = record['p']
                # Convertir les propriétés du noeud en dictionnaire
                project = dict(project_node.items())
                
                # Récupérer l'ID (soit via 'id' property si elle existe, soit via element_id)
                # IMPORTANT: Neo4j Python driver 5.x utilise element_id pour l'ID interne
                if 'id' not in project:
                    project['id'] = project_node.element_id
                
                # Convertir la relation APPLIED_TO en dictionnaire
                app_rel = record['r']
                app_data = dict(app_rel.items())
                
                # Nettoyage des dates
                for key in ['created_at', 'deadline']:
                    if key in project: 
                        project[key] = str(project[key])
                        
                if 'date' in app_data: 
                    app_data['date'] = str(app_data['date'])
                
                # Construction de l'objet de retour
                my_apps.append({
                    'project': project,
                    'status': app_data.get('status', 'PENDING'),
                    'date': app_data.get('date'),
                    'motivation_message': app_data.get('motivation_message', '')
                })
            return my_apps

    @staticmethod
    def update_status(project_id, applicant_email, new_status):
        driver = db.get_db()
        with driver.session() as session:
            query = """
            MATCH (u:User {email: $email})-[r:APPLIED_TO]->(p:Project)
            WHERE elementId(p) = $project_id
            SET r.status = $status
            RETURN r
            """
            result = session.run(query, email=applicant_email, project_id=project_id, status=new_status)
            return result.single() is not None
