import os
from neo4j import GraphDatabase

# 1. On définit les variables au niveau du module (MAJUSCULES pour les constantes)
# IMPORTANT: Le nom du service dans docker-compose est 'db', pas 'neo4j'
URI = os.getenv("NEO4J_URI", "bolt://db:7687")
USER = os.getenv("NEO4J_USER", "neo4j")
PASSWORD = os.getenv("NEO4J_PASSWORD", "connected_password")

class Neo4jDatabase:
    def __init__(self):
        self.driver = None

    def connect(self):
        if not self.driver:
            # 2. Ici, on utilise les variables globales définies plus haut
            try:
                self.driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
                # Test de connexion immédiat
                self.driver.verify_connectivity()
                print(f"✅ Connecté à Neo4j sur {URI}")
            except Exception as e:
                print(f"❌ Erreur de connexion Neo4j ({URI}): {e}")
                self.driver = None
                raise e

    def get_db(self):
        if not self.driver:
            self.connect()
        return self.driver

    def close(self):
        if self.driver:
            self.driver.close()
            self.driver = None

# 3. On crée l'instance unique
db = Neo4jDatabase()