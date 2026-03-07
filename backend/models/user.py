from database import db

class UserModel:
    @staticmethod
    def create(email, password_hash, nom, prenom, role):
        driver = db.get_db()
        with driver.session() as session:
            # Vérifier existence
            existing = session.run("MATCH (u:User {email: $email}) RETURN u", email=email).single()
            if existing:
                return None, "Cet email est déjà utilisé"

            # Création
            query = """
            CREATE (u:User {
                email: $email,
                password_hash: $password_hash,
                nom: $nom,
                prenom: $prenom,
                role: $role,
                created_at: datetime()
            })
            RETURN u
            """
            
            # Label spécifique
            role_label = ""
            if role == 'etudiant': role_label = ":Student"
            elif role == 'professionnel': role_label = ":Pro"
            elif role == 'encadrant': role_label = ":Encadrant"
                
            if role_label:
                query = query.replace(":User", f":User{role_label}")
            
            result = session.run(query, email=email, password_hash=password_hash, 
                               nom=nom, prenom=prenom, role=role)
            return result.single()['u'], None

    @staticmethod
    def find_by_email(email):
        driver = db.get_db()
        with driver.session() as session:
            result = session.run("MATCH (u:User {email: $email}) RETURN u", email=email).single()
            return result['u'] if result else None

    @staticmethod
    def get_all():
        driver = db.get_db()
        with driver.session() as session:
            result = session.run("MATCH (u:User) RETURN u")
            return [dict(record['u'].items()) for record in result]

    @staticmethod
    def get_profile_with_techs(email):
        driver = db.get_db()
        with driver.session() as session:
            query = """
            MATCH (u:User {email: $email})
            OPTIONAL MATCH (u)-[:HAS_TECH]->(t:Technology)
            RETURN u, collect(t.libelle) as technologies
            """
            result = session.run(query, email=email).single()
            if not result: return None
            
            user_data = dict(result['u'].items())
            user_data['technologies'] = result['technologies']
            return user_data

    @staticmethod
    def update_profile(email, data, technologies=None):
        driver = db.get_db()
        with driver.session() as session:
            # Update basic fields
            fields = []
            params = {'email': email}
            allowed = ['nom', 'prenom', 'ville', 'bio_courte', 'ecole', 'filiere', 'entreprise', 'fonction']
            
            for field in allowed:
                if field in data:
                    fields.append(f"u.{field} = ${field}")
                    params[field] = data[field]
            
            if fields:
                query = f"MATCH (u:User {{email: $email}}) SET {', '.join(fields)} RETURN u"
                session.run(query, **params)
            
            # Update technologies
            if technologies is not None and isinstance(technologies, list):
                session.run("""
                MATCH (u:User {email: $email})-[r:HAS_TECH]->()
                DELETE r
                """, email=email)
                
                for tech in technologies:
                    session.run("""
                    MATCH (u:User {email: $email})
                    MERGE (t:Technology {libelle: $tech})
                    MERGE (u)-[:HAS_TECH]->(t)
                    """, email=email, tech=tech)
            return True
