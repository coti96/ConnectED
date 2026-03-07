from database import db

class DashboardModel:
    @staticmethod
    def get_stats(user_email):
        driver = db.get_db()
        with driver.session() as session:
            # Récupérer les statistiques globales
            query = """
            MATCH (u:User {email: $email})
            
            // Compter les candidatures envoyées
            OPTIONAL MATCH (u)-[r1:APPLIED_TO]->(p1:Project)
            WITH u, count(r1) as applications_sent
            
            // Compter les projets créés
            OPTIONAL MATCH (u)-[:CREATED]->(p2:Project)
            WITH u, applications_sent, count(p2) as projects_created
            
            // Compter les messages non lus (si on gérait le statut 'read')
            // Pour l'instant, on compte juste le nombre total de messages reçus
            OPTIONAL MATCH (other:User)-[:SENT]->(m:Message)-[:TO]->(u)
            WITH u, applications_sent, projects_created, count(m) as messages_received
            
            RETURN {
                applications_sent: applications_sent,
                projects_created: projects_created,
                messages_received: messages_received
            } as stats
            """
            result = session.run(query, email=user_email)
            return result.single()['stats']

    @staticmethod
    def get_recent_activity(user_email):
        driver = db.get_db()
        with driver.session() as session:
            # Récupérer les dernières candidatures
            query_apps = """
            MATCH (u:User {email: $email})-[r:APPLIED_TO]->(p:Project)
            RETURN p.titre as project_title, r.status as status, r.date as date
            ORDER BY r.date DESC LIMIT 5
            """
            apps = []
            for record in session.run(query_apps, email=user_email):
                apps.append({
                    'type': 'application',
                    'title': record['project_title'],
                    'status': record['status'],
                    'date': str(record['date'])
                })

            # Récupérer les derniers projets créés
            query_projects = """
            MATCH (u:User {email: $email})-[:CREATED]->(p:Project)
            RETURN p.titre as title, p.created_at as date
            ORDER BY p.created_at DESC LIMIT 5
            """
            projects = []
            for record in session.run(query_projects, email=user_email):
                projects.append({
                    'type': 'project',
                    'title': record['title'],
                    'date': str(record['date'])
                })

            return apps + projects
